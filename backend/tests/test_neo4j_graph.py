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


def test_graph_connection_timeout_bounds_a_server_that_never_answers():
    import socket
    import threading
    import time
    from concurrent.futures import ThreadPoolExecutor

    release = threading.Event()
    with socket.socket() as listener:
        listener.bind(('127.0.0.1', 0))
        listener.listen()
        listener.settimeout(15)

        def silent_server():
            with listener.accept()[0]:
                release.wait(15)

        server = threading.Thread(target=silent_server)
        server.start()
        graph = Neo4jQueries(GraphSettings(f'bolt://127.0.0.1:{listener.getsockname()[1]}',
                                          'reader', 'test-only'), None)
        started = time.monotonic()
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                pending = executor.submit(graph.lookup_account, 'amelia.ward')
                try:
                    with pytest.raises(GraphUnavailable, match='Neo4j is unavailable'):
                        pending.result(timeout=8)
                finally:
                    release.set()
            assert time.monotonic() - started < 8
        finally:
            release.set()
            server.join(timeout=16)
            graph.close()
