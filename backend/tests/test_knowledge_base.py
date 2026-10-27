"""Door 2: build and read a knowledge base using real PostgreSQL and offline embeddings."""

import asyncio
import shutil
import re
from collections.abc import Iterator
from dataclasses import replace
from pathlib import Path

import pytest
import tiktoken
from langchain_core.embeddings import Embeddings
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from login_investigator.knowledge_base import build_knowledge_base, open_knowledge_base
from login_investigator.postgres import ServerSettings, create_fresh_database, drop_database

DATASET = Path(__file__).resolve().parents[1] / "data/datasets/default"


@pytest.fixture
def build_database(fresh_database: ServerSettings) -> Iterator[ServerSettings]:
    database = create_fresh_database(replace(fresh_database, database="postgres"))
    yield database
    drop_database(database)


class FakeEmbedder(Embeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[1.0] + [0.0] * 1535 for _ in texts]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]


def sample_dataset(tmp_path: Path) -> Path:
    shutil.copytree(DATASET / "org", tmp_path / "org")
    own = tmp_path / "corpus/own"
    own.mkdir(parents=True)
    (own / "sample.md").write_text('''---
id: "sample"
title: "Access policy"
kind: "policy"
version: "1.0"
date: "2026-09-01"
---
# Access policy

## Scope

Access to payroll needs approval from thomas.price.
''')
    return tmp_path


def test_build_makes_organisation_and_contextual_passage_readable(
    build_database: ServerSettings, tmp_path: Path,
):
    dataset = sample_dataset(tmp_path)

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        async with open_knowledge_base(build_database) as kb:
            people = await kb.organisation_records("people")
            assert len(people) == 50
            chunks = await kb.chunks()
            assert len(chunks) == 1
            assert chunks[0].id == "sample@1.0#access-policy/scope/1"
            assert chunks[0].text.startswith("Access policy | Access policy > Scope\n")
            assert "payroll needs approval" in chunks[0].text

    asyncio.run(check())


def test_numbered_runbook_steps_survive_whole(
    build_database: ServerSettings, tmp_path: Path,
):
    dataset = sample_dataset(tmp_path)
    for path in (DATASET / "corpus/own").glob("run-*.md"):
        shutil.copy(path, dataset / "corpus/own" / path.name)
    long_step = "1. " + "Keep the warning attached to this step. " * 60
    path = dataset / "corpus/own/sample.md"
    path.write_text(path.read_text().replace('kind: "policy"', 'kind: "runbook"')
                    + "\n\n## Steps\n\n" + long_step)

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        async with open_knowledge_base(build_database) as kb:
            chunks = await kb.chunks()
        steps_seen = 0
        for path in (DATASET / "corpus/own").glob("run-*.md"):
            passages = [chunk.text for chunk in chunks if chunk.id.startswith(path.stem + "@")]
            steps = re.findall(r"^\d+\. .*?(?=^\d+\. |^## |\Z)", path.read_text(), re.M | re.S)
            for step in steps:
                assert sum(step.strip() in passage for passage in passages) == 1, step
                steps_seen += 1
        assert steps_seen >= 19
        assert sum(long_step.strip() in chunk.text for chunk in chunks) == 1

    asyncio.run(check())


def test_long_sections_split_within_headings_and_preserve_context(
    build_database: ServerSettings, tmp_path: Path,
):
    dataset = sample_dataset(tmp_path)
    path = dataset / "corpus/own/sample.md"
    long_text = "\n\n".join(f"Rule {i}: Approval is required for sensitive access." for i in range(100))
    path.write_text(path.read_text() + "\n\n## Controls\n\n" + long_text)

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        async with open_knowledge_base(build_database) as kb:
            chunks = await kb.chunks()
        controls = [chunk for chunk in chunks if "/controls/" in chunk.id]
        assert len(controls) > 1
        encoding = tiktoken.get_encoding("cl100k_base")
        for chunk in controls:
            header, content = chunk.text.split("\n", 1)
            assert header == "Access policy | Access policy > Controls"
            assert len(encoding.encode(content)) <= 350
            assert "payroll" not in content
        assert all(any(f"Rule {i}:" in chunk.text for chunk in controls) for i in range(100))
        assert re.fullmatch(r"sample@1.0#access-policy/controls/\d+", controls[0].id)

    asyncio.run(check())


def test_attack_only_build_cleans_text_and_packs_whole_procedure_examples(
    build_database: ServerSettings, tmp_path: Path,
):
    shutil.copytree(DATASET / "org", tmp_path / "org")
    attack = tmp_path / "corpus/attack"
    shutil.copytree(DATASET / "corpus/attack", attack)
    sources = {path.name: path.read_bytes() for path in attack.glob("*.md")}

    async def check():
        await build_knowledge_base(tmp_path, build_database, FakeEmbedder())
        async with open_knowledge_base(build_database) as kb:
            chunks = await kb.chunks()
        assert len({chunk.metadata["id"] for chunk in chunks}) == 13
        for chunk in chunks:
            assert "References" not in chunk.text
            assert "(Citation:" not in chunk.text
            assert "https://" not in chunk.text and "http://" not in chunk.text
            assert "<code>" not in chunk.text and "</code>" not in chunk.text
        examples = [chunk for chunk in chunks if "/procedure-examples/" in chunk.id]
        assert len(examples) < 185
        assert any(chunk.text.count("### ") > 1 for chunk in examples)
        encoding = tiktoken.get_encoding("cl100k_base")
        for chunk in examples:
            assert len(encoding.encode(chunk.text.split("\n", 1)[1])) <= 350
        # Every source example stays together, with its heading, after the agreed cleaning.
        for path in attack.glob("*.md"):
            text = path.read_text()
            if "## Procedure examples" not in text:
                continue
            section = text.split("## Procedure examples\n", 1)[1].split("\n## ", 1)[0]
            for example in re.split(r"(?=^### )", section, flags=re.M):
                if not example.strip():
                    continue
                cleaned = re.sub(r"\(Citation: [^)]*\)", "", example)
                cleaned = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", cleaned)
                cleaned = cleaned.replace("<code>", "").replace("</code>", "").strip()
                assert any(cleaned in chunk.text for chunk in examples), path.name
        assert {path.name: path.read_bytes() for path in attack.glob("*.md")} == sources

    asyncio.run(check())


def test_reader_can_read_but_cannot_change_the_knowledge_base(
    build_database: ServerSettings, tmp_path: Path,
):
    from login_investigator.knowledge_base import reader_settings
    dataset = sample_dataset(tmp_path)

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        async with open_knowledge_base(reader_settings(build_database)) as kb:
            assert len(await kb.organisation_records("people")) == 50
            assert len(await kb.chunks()) == 1
            # Permission is a database boundary. Try actual DML and DDL through that connection.
            for statement in (
                "DELETE FROM chunks", "UPDATE people SET country = 'XX'",
                "CREATE TABLE forbidden (id text)", "CREATE TEMP TABLE forbidden (id text)",
            ):
                with pytest.raises(DBAPIError) as caught:
                    async with kb.engine.begin() as connection:
                        await connection.execute(text(statement))
                assert getattr(caught.value.orig, "sqlstate", None) == "42501"

    asyncio.run(check())


def test_mentions_are_derived_from_text_and_resolve_to_known_entities(
    build_database: ServerSettings, tmp_path: Path,
):
    dataset = sample_dataset(tmp_path)
    path = dataset / "corpus/own/sample.md"
    path.write_text(path.read_text().replace("payroll", "asset-erp") + '''

## Devices

Daniel Hughes uses LT-DHUGHES. IT Admins may investigate T1110.003.
Do not mistake thomas.pricey for thomas.price.

## Unlinked

Keep records clear and accurate.

## Near matches

thomas.pricey uses LT-DHUGHES2.
''')

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        async with open_knowledge_base(build_database) as kb:
            links = await kb.mentions()
            chunks = await kb.chunks()
        scope = {(link["entity_type"], link["entity_id"]) for link in links
                 if "/scope/" in link["chunk_id"]}
        assert scope == {("person", "user-thomas.price"), ("asset", "asset-erp")}
        devices = {link["entity_id"] for link in links if "/devices/" in link["chunk_id"]}
        assert devices == {"user-daniel.hughes", "dev-laptop-daniel.hughes",
                           "group-it-admins", "user-thomas.price"}
        assert not any("/unlinked/" in link["chunk_id"] for link in links)
        assert not any("/near-matches/" in link["chunk_id"] for link in links)
        chunk = next(chunk for chunk in chunks if "/devices/" in chunk.id)
        assert chunk.metadata["technique_ids"] == ["T1110.003"]

    asyncio.run(check())


def test_duplicate_chunk_addresses_fail_instead_of_overwriting_evidence(
    build_database: ServerSettings, tmp_path: Path,
):
    dataset = sample_dataset(tmp_path)
    path = dataset / "corpus/own/sample.md"
    path.write_text(path.read_text() + "\n\n## Scope\n\nA different statement.\n")
    with pytest.raises(ValueError, match="Duplicate chunk ID"):
        asyncio.run(build_knowledge_base(dataset, build_database, FakeEmbedder()))


def test_incomplete_embedding_response_fails_instead_of_dropping_passages(
    build_database: ServerSettings, tmp_path: Path,
):
    class IncompleteEmbedder(FakeEmbedder):
        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            return []

    with pytest.raises(ValueError, match="Embedding response"):
        asyncio.run(build_knowledge_base(sample_dataset(tmp_path), build_database, IncompleteEmbedder()))


def test_rebuild_publishes_only_complete_database_and_preserves_chunk_ids(
    fresh_database: ServerSettings, tmp_path: Path,
):
    from login_investigator.knowledge_base import rebuild_knowledge_base
    import json
    dataset = sample_dataset(tmp_path / "dataset")
    state = tmp_path / "active.json"
    created: list[ServerSettings] = []

    async def check():
        for _ in range(2):
            report = await rebuild_knowledge_base(dataset, fresh_database, FakeEmbedder(), state)
            database = replace(fresh_database, database=report.database)
            created.append(database)
            assert report.documents == 1 and report.chunks == 1
            assert report.organisation_rows["people"] == 50
            assert report.vector_dimensions == [1536]
            assert report.keyword_index is True
            assert json.loads(state.read_text())["database"] == database.database
        async with open_knowledge_base(created[0]) as first, open_knowledge_base(created[1]) as second:
            assert [chunk.id for chunk in await first.chunks()] == [chunk.id for chunk in await second.chunks()]
        assert created[0].database != created[1].database
        saved = state.read_bytes()
        (dataset / "corpus/own/sample.md").write_text("broken front matter")
        with pytest.raises(ValueError):
            await rebuild_knowledge_base(dataset, fresh_database, FakeEmbedder(), state)
        assert state.read_bytes() == saved

    try:
        asyncio.run(check())
    finally:
        for database in created:
            drop_database(database)


def test_five_added_document_kinds_follow_policy_sizes(
    build_database: ServerSettings, tmp_path: Path,
):
    dataset = sample_dataset(tmp_path)
    source = dataset / "corpus/own/sample.md"
    template = source.read_text()
    for kind in ("email", "guidance", "meeting", "record", "register"):
        content = template.replace('id: "sample"', f'id: "{kind}"').replace('kind: "policy"', f'kind: "{kind}"')
        content += "\n\n## Detail\n\n" + " ".join(f"Control {i} needs approval." for i in range(150))
        (source.parent / f"{kind}.md").write_text(content)

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        async with open_knowledge_base(build_database) as kb:
            chunks = await kb.chunks()
        encoding = tiktoken.get_encoding("cl100k_base")
        for kind in ("email", "guidance", "meeting", "record", "register"):
            passages = sorted((c for c in chunks if c.id.startswith(kind + "@") and "/detail/" in c.id),
                              key=lambda c: int(c.id.rsplit("/", 1)[1]))
            assert len(passages) > 1
            bodies = [c.text.split("\n", 1)[1] for c in passages]
            assert all(len(encoding.encode(body)) <= 350 for body in bodies)
            # A real overlap, not just a configured number. Word boundaries change token counts.
            for left, right in zip(bodies, bodies[1:]):
                overlap = max(n for n in range(min(len(left), len(right)) + 1)
                              if left.endswith(right[:n]))
                assert 30 <= len(encoding.encode(right[:overlap])) <= 50

    asyncio.run(check())


def test_privileged_reader_is_rejected_before_any_embedding_call(
    build_database: ServerSettings, tmp_path: Path,
):
    from login_investigator.postgres import DatabaseUnavailable

    class MustNotEmbed(FakeEmbedder):
        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            raise AssertionError("Embedding should not run for an invalid reader")

    with pytest.raises(DatabaseUnavailable, match="separate unprivileged role"):
        asyncio.run(build_knowledge_base(sample_dataset(tmp_path), build_database, MustNotEmbed(),
                                         reader_role=build_database.user))


def test_invalid_publication_state_does_not_start_a_build(
    fresh_database: ServerSettings, tmp_path: Path,
):
    from login_investigator.knowledge_base import rebuild_knowledge_base

    class MustNotEmbed(FakeEmbedder):
        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            raise AssertionError("Embedding should not run for invalid publication state")

    dataset = sample_dataset(tmp_path / "dataset")
    state = tmp_path / "active.json"
    state.write_text("[]")
    with pytest.raises(ValueError, match="state file"):
        asyncio.run(rebuild_knowledge_base(dataset, fresh_database, MustNotEmbed(), state))
    assert state.read_text() == "[]"


def test_attack_cleaning_preserves_the_independently_written_visible_text(
    build_database: ServerSettings, tmp_path: Path,
):
    dataset = sample_dataset(tmp_path)
    path = dataset / "corpus/own/sample.md"
    prefix = path.read_text().split("## Scope", 1)[0].replace('kind: "policy"', 'kind: "attack"')
    path.write_text(prefix + '''## Scope

Use [visible policy](https://source.example/reference) and <code>token</code>. (Citation: Hidden Source)

## References

Only the source file should retain this reference.
''')

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        async with open_knowledge_base(build_database) as kb:
            chunks = await kb.chunks()
        assert [chunk.text for chunk in chunks] == [
            "Access policy | Access policy > Scope\nUse visible policy and token."
        ]

    asyncio.run(check())


def test_skipped_heading_levels_and_fenced_commands_keep_their_context(
    build_database: ServerSettings, tmp_path: Path,
):
    dataset = sample_dataset(tmp_path)
    path = dataset / "corpus/own/sample.md"
    prefix = path.read_text().split("## Scope", 1)[0]
    path.write_text(prefix + '''### First

First sibling.

### Second

Check approval before running this command.

```sh
# This is a shell comment, not a heading
printf 'read only'
```

Keep the warning with the command.
''')

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        async with open_knowledge_base(build_database) as kb:
            chunks = await kb.chunks()
        assert [chunk.id for chunk in chunks] == [
            "sample@1.0#access-policy/first/1", "sample@1.0#access-policy/second/1",
        ]
        assert chunks[1].text == (
            "Access policy | Access policy > Second\n"
            "Check approval before running this command.\n\n"
            "```sh\n# This is a shell comment, not a heading\nprintf 'read only'\n```\n\n"
            "Keep the warning with the command."
        )

    asyncio.run(check())
