"""Own one isolated Neo4j Community container and data volume for a version.

This development service deliberately retains Community administrative powers. It is
not a least-privilege production deployment (AUD-068).
"""

import os
import secrets
import subprocess
import time
from pathlib import Path
from typing import Any, LiteralString

from neo4j import GraphDatabase, Query
from neo4j.exceptions import DriverError, Neo4jError

from .neo4j_graph import GraphSettings, GraphUnavailable

IMAGE = 'neo4j:2026.10.1'


def docker(*arguments: str) -> str:
    try:
        return subprocess.run(['docker', *arguments], check=True, capture_output=True,
                              text=True, timeout=90).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        raise GraphUnavailable('Neo4j container operation failed. Start Docker Desktop and ensure '
                               'neo4j:2026.10.1 is available with docker pull neo4j:2026.10.1.') from None


def execute(settings: GraphSettings, query: LiteralString, database: str = 'neo4j',
            **parameters: Any) -> list[dict[str, Any]]:
    """Preparation/security commands deliberately use WRITE access, testing the server lock."""
    with GraphDatabase.driver(settings.uri, auth=(settings.user, settings.password),
                              connection_timeout=3, connection_acquisition_timeout=5,
                              max_transaction_retry_time=0, telemetry_disabled=True) as driver:
        with driver.session(database=database) as session:
            return session.run(Query(query, timeout=10), parameters).data()


def private_env(path: Path, contents: str) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as handle:
        handle.write(contents)


class GraphService:
    def __init__(self, name: str, directory: Path):
        self.name = name
        self.volume = name + '-data'
        self.directory = directory
        self.creation_attempted = False
        self.volume_created = False
        self.container_created = False

    def start(self, *, read_only: bool, bolt_port: str = '', http_port: str = '') -> str:
        arguments = ['create', '--name', self.name,
                     '--label', 'purpose=li-graph-version', '--label', 'li.owner=' + self.name,
                     '--publish', f'127.0.0.1:{bolt_port}:7687', '--volume', self.volume + ':/data',
                     '--env', 'NEO4J_server_memory_heap_initial__size=256m',
                     '--env', 'NEO4J_server_memory_heap_max__size=512m',
                     '--env', 'NEO4J_server_memory_pagecache_size=256m']
        if read_only:
            arguments += ['--env', 'NEO4J_server_databases_read__only=neo4j',
                          '--publish', f'127.0.0.1:{http_port}:7474',
                          '--env', 'NEO4J_browser_post__connect__cmd=access-mode read']
        else:
            arguments += ['--env-file', str(self.directory / 'builder' / '.env')]
        self.creation_attempted = True
        try:
            docker(*arguments, IMAGE)
        finally:
            # A timeout can happen after the daemon created the container. Inspect only this
            # run's unique name and ownership label; never sweep other resources.
            self.container_created = self.owns('container', self.name)
        docker('start', self.name)
        return self.uri()

    def uri(self) -> str:
        binding = docker('port', self.name, '7687/tcp')
        return 'bolt://127.0.0.1:' + str(int(binding.rsplit(':', 1)[1]))

    def wait(self, settings: GraphSettings) -> None:
        deadline = time.monotonic() + 120
        while time.monotonic() < deadline:
            try:
                execute(settings, 'RETURN 1 AS ready')
                return
            except (DriverError, Neo4jError):
                time.sleep(1)
        raise GraphUnavailable('Neo4j did not become ready within 120 seconds. Check Docker Desktop resources.')

    def prepare(self) -> GraphSettings:
        docker('version', '--format', '{{.Server.Version}}')
        docker('image', 'inspect', IMAGE, '--format', '{{.Id}}')
        self.creation_attempted = True
        try:
            docker('volume', 'create', '--label', 'purpose=li-graph-version',
                   '--label', 'li.owner=' + self.name, self.volume)
        finally:
            self.volume_created = self.owns('volume', self.volume)
        password = secrets.token_urlsafe(32)
        (self.directory / 'builder').mkdir(mode=0o700)
        private_env(self.directory / 'builder' / '.env', 'NEO4J_AUTH=neo4j/' + password + '\n')
        settings = GraphSettings(self.start(read_only=False), 'neo4j', password)
        self.wait(settings)
        return settings

    def seal(self, builder: GraphSettings) -> GraphSettings:
        password = secrets.token_urlsafe(32)
        execute(builder, 'CREATE USER li_serving SET PASSWORD $password CHANGE NOT REQUIRED',
                'system', password=password)
        serving = GraphSettings(builder.uri, 'li_serving', password)
        execute(serving, 'DROP USER neo4j', 'system')
        private_env(self.directory / '.env', 'LI_GRAPH_USER=li_serving\nLI_GRAPH_PASSWORD=' + password + '\n')
        docker('stop', self.name)
        docker('rm', self.name)
        self.container_created = False
        (self.directory / 'builder' / '.env').unlink()
        (self.directory / 'builder').rmdir()
        serving = GraphSettings(self.start(read_only=True), 'li_serving', password)
        self.wait(serving)
        return serving

    def owns(self, kind: str, name: str) -> bool:
        template = '{{ index .Config.Labels "li.owner" }}' if kind == 'container' else '{{ index .Labels "li.owner" }}'
        try:
            result = subprocess.run(['docker', kind, 'inspect', '--format', template, name],
                                    capture_output=True, text=True, timeout=15, check=False)
        except (OSError, subprocess.SubprocessError):
            raise GraphUnavailable('Docker resource ownership could not be checked; retain recovery state') from None
        if result.returncode == 0:
            return result.stdout.strip() == self.name
        if any(message in result.stderr.lower() for message in ('no such object', 'no such container', 'no such volume')):
            return False
        raise GraphUnavailable('Docker resource ownership could not be checked; retain recovery state')

    def remove(self) -> None:
        if not self.creation_attempted and not self.container_created and not self.volume_created:
            return
        failures = []
        for kind, name, arguments in (
            ('container', self.name, ('rm', '--force', self.name)),
            ('volume', self.volume, ('volume', 'rm', self.volume)),
        ):
            known = self.container_created if kind == 'container' else self.volume_created
            if known or self.owns(kind, name):
                try:
                    docker(*arguments)
                except GraphUnavailable:
                    failures.append(kind)
        if failures:
            raise GraphUnavailable('Isolated graph cleanup failed; retained build state requires recovery')
        self.container_created = self.volume_created = False


def check_serving_protection(settings: GraphSettings) -> dict[str, str]:
    """Refuse publication unless data/schema writes and access-mode changes are rejected."""
    outcomes = {}
    from typing import LiteralString
    writes: dict[str, LiteralString] = {
        'create': 'CREATE (:ProtectionProbe)',
        'update': "MATCH (n:Entity) SET n.protection_probe=true",
        'relationship': 'MATCH (n:Entity) WITH n LIMIT 1 CREATE (n)-[:PROTECTION_PROBE]->(n)',
        'delete_relationship': 'MATCH ()-[r]->() WITH r LIMIT 1 DELETE r',
        'delete': 'MATCH (n:Entity) WITH n LIMIT 1 DETACH DELETE n',
        'index': 'CREATE INDEX protection_probe FOR (n:Entity) ON (n.protection_probe)',
    }
    for name, query in writes.items():
        try:
            execute(settings, query)
        except Neo4jError as error:
            if error.code != 'Neo.ClientError.General.WriteOnReadOnlyAccessDatabase':
                raise GraphUnavailable('Could not verify graph-data write prevention') from None
            outcomes[name] = error.code
        else:
            raise GraphUnavailable('Graph serving permits a write; this version cannot be published')
    modes: dict[str, LiteralString] = {
        'access_mode': 'ALTER DATABASE neo4j SET ACCESS READ WRITE',
        'configuration': "CALL dbms.setConfigValue('server.databases.read_only', '')",
    }
    for name, query in modes.items():
        try:
            execute(settings, query, 'system')
        except Neo4jError as error:
            if error.code not in {'Neo.ClientError.Statement.UnsupportedAdministrationCommand',
                                   'Neo.ClientError.Procedure.ProcedureNotFound'}:
                raise GraphUnavailable('Could not verify serving access-mode protection') from None
            outcomes[name] = error.code
        else:
            raise GraphUnavailable('Graph serving permits changing access mode')
    return outcomes
