"""Offline diagnostic: fair turns for focused routes and the broad route.

Python standard library only. No search, model call, or application change.
Run: python3 .scratch/knowledge-base/research/22-evidence-selection-replay.py
"""

import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "22-retrieval-experiment-20261029T113502902914Z-initial.json"
MANIFEST = HERE / "22-retrieval-experiment-cases.json"


def fair_select(routes, limit):
    """One unseen candidate per route per round; never consult expected evidence."""
    if limit < 0:
        raise ValueError("limit must be nonnegative")
    selected = []
    seen = set()
    positions = [0] * len(routes)
    while len(selected) < limit:
        progress = False
        for i, route in enumerate(routes):
            while positions[i] < len(route) and route[positions[i]] in seen:
                positions[i] += 1
            if positions[i] == len(route):
                continue
            candidate = route[positions[i]]
            positions[i] += 1
            selected.append(candidate)
            seen.add(candidate)
            progress = True
            if len(selected) == limit:
                break
        if not progress:
            break
    return selected


def score(ids, gold):
    return {
        "ranks": {g: ids.index(g) + 1 if g in ids else None for g in gold},
        "all_required": all(g in ids for g in gold) if gold else None,
    }


def main():
    # Mechanism checks include overlaps, empty routes, exhaustion and hard budgets.
    assert fair_select([["a", "b"], ["a", "c"]], 3) == ["a", "c", "b"]
    assert fair_select([[], ["a", "b"]], 20) == ["a", "b"]
    assert fair_select([], 20) == []
    assert fair_select([["a"]], 0) == []
    disjoint = [[f"{route}-{rank}" for rank in range(30)] for route in range(3)]
    ids = fair_select(disjoint, 20)
    assert len(ids) == len(set(ids)) == 20
    assert [sum(c.startswith(f"{route}-") for c in ids) for route in range(3)] == [7, 7, 6]
    manifest = json.loads(MANIFEST.read_text())
    source = json.loads(SOURCE.read_text())
    assert hashlib.sha256(MANIFEST.read_bytes()).hexdigest() == source["manifest_sha256"]
    rows = []
    for case, previous in zip(manifest["cases"], source["cases"], strict=True):
        assert case["id"] == previous["id"]
        # Only planned needs enter the ledger. N03's omitted need must remain omitted.
        route_specs = [(n["id"], n["query"]) for n in case["needs"]
                       if n["id"] in case["focused_need_ids"]]
        route_specs.append(("broad_discovery", case["question"]))
        ledgers = [{"route": name, "query": query,
                    "candidates": source["queries"][hashlib.sha256(query.encode()).hexdigest()]["top20"],
                    "assessment": "unreviewed", "supporting_passages": []}
                   for name, query in route_specs]
        lists = [row["candidates"] for row in ledgers]
        selected20 = fair_select(lists, 20)
        selected5 = fair_select(lists, 5)
        for ledger in ledgers:
            ledger["selected20"] = [c for c in ledger["candidates"] if c in selected20]
            ledger["not_selected20"] = [c for c in ledger["candidates"] if c not in selected20]
        # Gold is read only by the offline scorer, after selection and ledger construction.
        gold = list(dict.fromkeys(g for n in case["needs"] for g in n["gold"]))
        row = {"id": case["id"], "ledger": ledgers,
               "previous_rrf20": score(previous["methods"]["focused_broad"]["top20"], gold),
               "fair20": {"ids": selected20, **score(selected20, gold)},
               "fair5_stress_only": {"ids": selected5, **score(selected5, gold)},
               "order_sensitivity20": [score(fair_select(list(order), 20), gold)
                                       for order in itertools.permutations(lists)]}
        rows.append(row)
        print(json.dumps({"case": case["id"], "rrf20": row["previous_rrf20"]["all_required"],
                          "fair20": row["fair20"]["all_required"],
                          "fair5": row["fair5_stress_only"]["all_required"]}))
    output = {
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "manifest_sha256": source["manifest_sha256"],
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Post-result development replay, no new evidence or held-out claim. Fair route allocation is not semantic sufficiency. Five-passages stress is not T23 reranking.",
        "method": "Unchanged initial query lists. Focused needs in manifest order, then broad. One new candidate per route per round. All route orders also reported without choosing a winner.",
        "cases": rows,
    }
    path = HERE / "22-evidence-selection-replay.json"
    with path.open("x") as stream:
        json.dump(output, stream, indent=2)
        stream.write("\n")
    print(f"Saved {path.name}; no external calls.")


if __name__ == "__main__":
    main()
