"""Prepare contextual passages from source files without changing those files."""

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
import tiktoken

from login_investigator.corpus_check import split_front_matter


@dataclass(frozen=True)
class Chunk:
    id: str
    text: str
    metadata: dict[str, object]


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def pack_whole(parts: Iterable[str], size: int) -> list[str]:
    """Keep steps intact even if a single step exceeds the target; never duplicate a step."""
    encoding = tiktoken.get_encoding("cl100k_base")
    result: list[str] = []
    current = ""
    for part in parts:
        part = part.strip()
        if not part:
            continue
        combined = f"{current}\n\n{part}" if current else part
        if current and len(encoding.encode(combined)) > size:
            result.append(current)
            current = part
        else:
            current = combined
    if current:
        result.append(current)
    return result


def clean_attack(body: str) -> str:
    """Source stays intact. References and their inline markers are not search evidence."""
    if body.count("\n## References\n") != 1:
        raise ValueError("ATT&CK reference section format changed; review the converter")
    body = body.split("\n## References\n", 1)[0]
    body = re.sub(r"\(Citation: [^)]*\)", "", body)
    body = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", body)
    return body.replace("<code>", "").replace("</code>", "")


def sections(body: str) -> Iterable[tuple[list[str], str]]:
    """Heading paths define sections, except examples which stay in their field group."""
    headings: list[str] = []
    lines: list[str] = []
    for line in body.splitlines():
        match = re.match(r"^(#{1,6}) (.+)$", line)
        in_examples = len(headings) >= 2 and headings[1] == "Procedure examples"
        if match and not (in_examples and len(match[1]) > 2):
            if "\n".join(lines).strip():
                yield headings, "\n".join(lines).strip()
            headings = headings[:len(match[1]) - 1] + [match[2]]
            lines = []
        else:
            lines.append(line)
    if "\n".join(lines).strip():
        yield headings, "\n".join(lines).strip()


def read_chunks(dataset: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted((dataset / "corpus").rglob("*.md")):
        fields, body = split_front_matter(path.read_text(encoding="utf-8"))
        if fields["kind"] == "attack":
            body = clean_attack(body)
        for headings, content in sections(body):
            header = f"{fields['title']} | {' > '.join(headings)}"
            section_path = "/".join(slug(heading) for heading in headings)
            splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                encoding_name="cl100k_base", chunk_size=350, chunk_overlap=40,
            )
            if headings[-1:] == ["Procedure examples"] and fields["kind"] == "attack":
                passages = pack_whole(re.split(r"(?=^### )", content, flags=re.MULTILINE), 350)
                if any(len(tiktoken.get_encoding("cl100k_base").encode(p)) > 350 for p in passages):
                    raise ValueError("ATT&CK procedure example exceeds 350 tokens; review the source")
            elif fields["kind"] == "runbook" and re.search(r"^\d+\. ", content, re.M):
                passages = pack_whole(re.split(r"(?=^\d+\. )", content, flags=re.MULTILINE), 350)
            else:
                passages = splitter.split_text(content)
            for ordinal, passage in enumerate(passages, 1):
                technique_ids = sorted(set(re.findall(r"\bT\d{4}(?:\.\d{3})?\b", header + "\n" + passage)))
                source_technique = re.match(r"^(T\d{4}(?:\.\d{3})?):", str(fields["title"]))
                chunks.append(Chunk(
                    f"{fields['id']}@{fields['version']}#{section_path}/{ordinal}",
                    f"{header}\n{passage}",
                    {**fields, "document_type": fields["kind"], "effective_date": fields["date"],
                     "section_path": section_path, "technique_ids": technique_ids,
                     "technique_id": source_technique[1] if source_technique else
                         (technique_ids[0] if len(technique_ids) == 1 else None)},
                ))
    seen: set[str] = set()
    for chunk in chunks:
        if chunk.id in seen:
            raise ValueError(f"Duplicate chunk ID: {chunk.id}; make document/section names distinct")
        seen.add(chunk.id)
    if not chunks:
        raise ValueError("The corpus contains no passages to build")
    return chunks
