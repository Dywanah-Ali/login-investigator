"""Move operator ports between selected versions without removing their data volumes."""

import json
import re
import socket
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

from .graph_service import GraphService, check_serving_protection, docker
from .neo4j_graph import GraphSettings, GraphUnavailable


class GraphAddressUnavailable(GraphUnavailable):
    """Credential-safe operator diagnosis for a failed address move."""


@dataclass(frozen=True)
class GraphAddress:
    bolt: int = 7687
    http: int = 7474

    def __post_init__(self) -> None:
        if self.bolt == self.http or any(not 1 <= p <= 65535 for p in (self.bolt, self.http)):
            raise ValueError('Graph ports must be distinct valid TCP ports')


@dataclass
class Binding:
    service: GraphService
    bolt: str
    http: str
    changed: bool = False

    @classmethod
    def read(cls, marker: Path, *, outgoing: bool = False) -> 'Binding | None':
        # Recovery must still work if the outgoing completion marker was lost/corrupted.
        # Its canonical directory identifies the container; ownership is checked below.
        value = ({'build_id': marker.parent.name, 'container': 'li-graph-' + marker.parent.name}
                 if outgoing else json.loads(marker.read_text()))
        if marker.name != 'complete.json':
            raise GraphAddressUnavailable('Invalid retained graph marker path.')
        if (not re.fullmatch(r'[0-9a-f]{32}', value['build_id'])
                or value['container'] != 'li-graph-' + value['build_id']
                or marker.parent.name != value['build_id']):
            raise GraphAddressUnavailable('Invalid retained graph descriptor.')
        service = GraphService(value['container'], marker.parent)
        if outgoing and not docker('ps', '--all', '--filter', 'name=^/' + service.name + '$',
                                   '--format', '{{.Names}}'):
            return None  # Missing outgoing containers hold no ports either.
        if not service.owns('container', service.name) or not service.owns('volume', service.volume):
            raise GraphAddressUnavailable('Graph container or data volume ownership could not be verified.')
        if docker('inspect', '--format', '{{.State.Running}}', service.name) != 'true':
            if outgoing:
                return None  # A stopped outgoing container holds no ports; preserve it intact.
            raise GraphAddressUnavailable('Start the incoming complete graph pair before selection.')
        ports = json.loads(docker('inspect', '--format', '{{json .HostConfig.PortBindings}}', service.name))
        def port(key: str) -> str:
            bindings = ports.get(key) or []
            if len(bindings) != 1 or bindings[0]['HostIp'] != '127.0.0.1':
                raise GraphAddressUnavailable('Expected one localhost binding for each serving port.')
            # HostConfig records an empty port for ephemeral allocation; read the actual binding.
            return str(int(docker('port', service.name, key).rsplit(':', 1)[1]))
        return cls(service, port('7687/tcp'), port('7474/tcp'))

    def start(self, bolt: str, http: str, *, verify: bool) -> None:
        self.service.container_created = False
        uri = self.service.start(read_only=True, bolt_port=bolt, http_port=http)
        if verify:
            values = dotenv_values(self.service.directory / '.env')
            settings = GraphSettings(uri, values.get('LI_GRAPH_USER') or '', values.get('LI_GRAPH_PASSWORD') or '')
            self.service.wait(settings)
            check_serving_protection(settings)

    def recreate(self, bolt: str, http: str, *, verify: bool = True) -> None:
        self.changed = True
        docker('stop', self.service.name)
        docker('rm', self.service.name)
        self.start(bolt, http, verify=verify)

    def restore(self, *, verify: bool) -> None:
        if not self.changed:
            return
        # A failed create/start can leave a stopped or half-started container.
        if self.service.owns('container', self.service.name):
            docker('rm', '--force', self.service.name)
        self.start(self.bolt, self.http, verify=verify)
        self.changed = False


class AddressMove:
    def __init__(self, incoming: Path, outgoing: Path | None, address: GraphAddress):
        self.address = address
        incoming_binding = Binding.read(incoming)
        assert incoming_binding is not None
        self.incoming = incoming_binding
        self.outgoing = Binding.read(outgoing, outgoing=True) if outgoing is not None and outgoing != incoming else None

    def preflight(self) -> None:
        allowed = {self.incoming.service.name}
        if self.outgoing is not None:
            allowed.add(self.outgoing.service.name)
        holders: set[str] = set()
        fixed_ports = {str(self.address.bolt), str(self.address.http)}
        names = docker('ps', '--format', '{{.Names}}').splitlines()
        for name in names:
            ports = json.loads(docker('inspect', '--format', '{{json .NetworkSettings.Ports}}', name))
            for bindings in ports.values():
                for binding in bindings or []:
                    port = binding['HostPort']
                    if port in fixed_ports and binding['HostIp'] in {'127.0.0.1', '0.0.0.0', '::', ''}:
                        if name not in allowed:
                            raise GraphAddressUnavailable(f'Fixed graph port {port} is held by another container. Selection unchanged.')
                        holders.add(port)
        for port in fixed_ports:
            if port not in holders:
                try:
                    with socket.socket() as probe:
                        probe.bind(('127.0.0.1', int(port)))
                except OSError:
                    raise GraphAddressUnavailable(f'Fixed graph port {port} is held by another process. Selection unchanged.') from None

    def move(self) -> None:
        self.preflight()
        bolt, http = str(self.address.bolt), str(self.address.http)
        if self.incoming.bolt == bolt and self.incoming.http == http:
            return
        if self.outgoing is not None and (self.outgoing.bolt == bolt or self.outgoing.http == http):
            self.outgoing.recreate('', '', verify=False)
        self.incoming.recreate(bolt, http)

    def restore(self) -> None:
        # Free incoming fixed ports before restoring the outgoing version.
        failures = []
        for binding, verify in ((self.incoming, True), (self.outgoing, False)):
            if binding is not None:
                try:
                    binding.restore(verify=verify)
                except Exception:  # noqa: BLE001 - Attempt both recoveries; never expose driver credentials.
                    failures.append(binding.service.name)
        if failures:
            raise GraphAddressUnavailable('Graph address recovery needs operator attention: ' + ', '.join(failures))
