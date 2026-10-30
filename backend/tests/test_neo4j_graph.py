"""Door 2 graph queries against an isolated real Neo4j service."""

import pytest

from login_investigator.knowledge_base.neo4j_graph import GraphUnavailable, Neo4jQueries, GraphSettings


def test_unavailable_graph_has_a_fixed_public_error():
    graph = Neo4jQueries(GraphSettings('bolt://127.0.0.1:1', 'reader', 'test-only'), None)
    try:
        with pytest.raises(GraphUnavailable, match='Neo4j is unavailable'):
            graph.lookup_account('amelia.ward')
    finally:
        graph.close()
