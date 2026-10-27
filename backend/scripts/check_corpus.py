"""Check the delivered own corpus against the Codex brief, the organisation tables and truth.json.

From backend/: uv run python -m scripts.check_corpus
Exits 1 when any check fails. Lengths are reported in words. No network or keys are needed.
"""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

from login_investigator.corpus_check import check_corpus, read_brief

BACKEND = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = BACKEND / "data" / "datasets" / "default"
DEFAULT_BRIEF = BACKEND.parent / ".scratch" / "knowledge-base" / "codex-brief.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--brief", type=Path, default=DEFAULT_BRIEF)
    args = parser.parse_args(argv)
    report = check_corpus(args.dataset_dir, read_brief(args.brief.read_text(encoding="utf-8")))

    print("| Document | Kind | Words | Sections | Longest section |")
    print("|---|---|---|---|---|")
    for length in report.lengths:
        print(f"| {length.id} | {length.kind} | {length.words} | {length.sections} "
              f"| {length.longest_section_words} |")
    by_kind: dict[str, list[int]] = defaultdict(list)
    for length in report.lengths:
        by_kind[length.kind].append(length.words)
    print("\n| Kind | Documents | Fewest words | Most words |")
    print("|---|---|---|---|")
    for kind, words in sorted(by_kind.items()):
        print(f"| {kind} | {len(words)} | {min(words)} | {max(words)} |")

    verdict = "Failed" if report.errors else "Passed"
    plural = "" if len(report.errors) == 1 else "s"
    print(f"\n{verdict}: {len(report.lengths)} documents, {len(report.errors)} error{plural}")
    for error in report.errors:
        print(f"- {error}")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
