"""Native Browser views select identities from the core; they never recalculate radius."""

import json
from collections.abc import Mapping
from dataclasses import asdict
from pathlib import Path
from typing import LiteralString

from login_investigator.knowledge_base.graph_service import GraphService, docker
from login_investigator.knowledge_base.graph_version import open_version
from login_investigator.knowledge_base.neo4j_graph import Neo4jQueries
from login_investigator.loader import load_log
from login_investigator.postgres import ServerSettings
from login_investigator.rules import detect_all
from login_investigator.workers import owned_operation

from .radius import FindingRadius, radius_neighbourhood

IDENTITY: LiteralString = 'MATCH (b:Build) RETURN b.id AS build_id, b.fingerprint AS source_fingerprint'

ORGANISATION: LiteralString = '''MATCH (b:Build {id:$build_id, fingerprint:$fingerprint})
CALL () {
  MATCH (n:Entity) WHERE n.entity_type <> 'chunk'
  RETURN collect(n) AS nodes
}
CALL () {
  MATCH (a:Entity)-[r]->(z:Entity)
  WHERE a.entity_type <> 'chunk' AND z.entity_type <> 'chunk'
  RETURN collect(r) AS relationships
}
RETURN b.id AS build_id, b.fingerprint AS source_fingerprint,
       size(nodes) AS node_count, size(relationships) AS relationship_count,
       nodes, relationships'''

FINDING: LiteralString = '''MATCH (b:Build {id:$build_id, fingerprint:$fingerprint})
CALL () {
  UNWIND $nodes AS id MATCH (n:Entity {id:id})
  RETURN collect(n) AS nodes
}
CALL () {
  UNWIND $edges AS edge
  MATCH (a:Entity {id:edge[0]})-[r]->(z:Entity {id:edge[1]})
  WHERE type(r)=edge[2]
  RETURN collect(r) AS relationships
}
RETURN b.id AS build_id, b.fingerprint AS source_fingerprint,
       size(nodes) AS node_count, size(relationships) AS relationship_count,
       size(nodes)=size($nodes) AND size(relationships)=size($edges) AS complete,
       nodes, relationships'''

STYLE = '''node.Entity {
  size: 45px;
  color: #68BDF6;
  caption: "{id}";
}
relationship.grants {
  color: #D62728;
}
relationship.used_device {
  color: #2CA02C;
}
relationship.used_address {
  color: #9467BD;
}
'''


def finding_parameters(radius: FindingRadius, build_id: str, fingerprint: str) -> dict[str, object]:
    selection = radius_neighbourhood(radius)
    return {'build_id': build_id, 'fingerprint': fingerprint,
            'nodes': selection.nodes, 'edges': selection.edges}


def browser_parameters(parameters: Mapping[str, object]) -> str:
    """Browser evaluates a Cypher map, whose keys cannot be JSON string literals."""
    if set(parameters) - {'build_id', 'fingerprint', 'nodes', 'edges'}:
        raise ValueError('Unsupported inspection parameter')
    return ':params {' + ', '.join(f'{key}: {json.dumps(value)}' for key, value in parameters.items()) + '}\n'


async def prepare_inspection(marker: Path, output: Path, finding_id: str | None = None) -> dict[str, object]:
    """Open/check both stores before writing credential-free inspection instructions."""
    async with open_version(marker, ServerSettings.from_env()) as kb:
        snapshot = marker.parent / 'source'
        if output.resolve().is_relative_to(snapshot.resolve()):
            raise ValueError('Inspection output must be outside the immutable source snapshot')
        descriptor = json.loads(marker.read_text())
        graph = kb.graph_queries
        if not isinstance(graph, Neo4jQueries):
            raise ValueError('Native inspection requires a paired graph version')  # noqa: TRY004 - Preserve the existing invalid-input ValueError contract.
        findings = detect_all(await owned_operation(lambda: load_log(snapshot / 'logins.csv')))
        if finding_id is not None and finding_id not in {f.finding_id for f in findings}:
            raise ValueError('No finding has this ID in the selected source snapshot')
        service = GraphService(descriptor['container'], marker.parent)
        bolt = await owned_operation(service.uri)
        binding = await owned_operation(lambda: docker('port', service.name, '7474/tcp'))
        browser = 'http://127.0.0.1:' + str(int(binding.rsplit(':', 1)[1])) + '/browser/'
        parameters = {'build_id': kb.build_id, 'fingerprint': descriptor['fingerprint']}
        counts = (await owned_operation(lambda: graph._read(ORGANISATION, **parameters)))[0]
        report: dict[str, object] = {
            **parameters, 'browser_url': browser, 'bolt_uri': bolt, 'username': 'li_serving',
            'offline_embeddings': kb.offline_embeddings,
            'organisation_nodes': counts['node_count'], 'organisation_relationships': counts['relationship_count'],
            'findings': [],
        }
        files = {'identity.cypher': IDENTITY + ';\n',
                 'organisation.cypher': ORGANISATION + ';\n',
                 'organisation-parameters.txt': browser_parameters(parameters),
                 'inspection.grass': STYLE}
        entries = []
        for finding in findings:
            if finding_id is not None and finding.finding_id != finding_id:
                continue
            radius = await owned_operation(lambda: kb.finding_radius(finding))  # noqa: B023 - This callback completes within the current iteration.
            params = finding_parameters(radius, kb.build_id or '', descriptor['fingerprint'])
            result = (await owned_operation(lambda: graph._read(FINDING, **params)))[0]  # noqa: B023 - This callback completes within the current iteration.
            if not result['complete']:
                raise ValueError('Browser identities do not match the core neighbourhood')
            stem = finding.finding_id
            files[stem + '-parameters.txt'] = browser_parameters(params)
            files[stem + '-context.json'] = json.dumps(asdict(radius), indent=2) + '\n'
            entries.append({'finding_id': stem, 'rule': finding.rule,
                            'nodes': result['node_count'], 'relationships': result['relationship_count']})
        files['finding.cypher'] = FINDING + ';\n'
        report['findings'] = entries
        files['inspection.json'] = json.dumps(report, indent=2) + '\n'
        # Refuse reuse, so an older inspection cannot be mistaken for this source version.
        output.mkdir(parents=True, exist_ok=False)
        for name, contents in files.items():
            (output / name).write_text(contents)
        return report
