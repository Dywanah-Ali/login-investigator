# 15: The Codex brief and the consistency script

Type: build
Status: ready-for-agent
Blocked by: 12
Phase: 0

## What to build

Two things the own corpus needs before anyone writes it. First, the brief a standalone Codex session
writes the 27 documents from: it carries the organisation's facts and the list of documents, and
never reveals the exam. Second, a consistency script that checks every document against the
world's tables, so facts in the corpus are checked by code and humans read only for feel.

## Decisions implemented

- T04 d10 and d11 (fifteen core and twelve noise documents, realism traits planted inside them),
  T04 d12 (front matter), T04 d16 (the brief and the script), T04 d14 (the four absent topics stay
  absent).
- User stories 60 to 62.

## Acceptance criteria

- [ ] The brief lives in the initiative folder and carries the organisation's facts, the 27-file list
      with headers and planned document IDs from `truth.json`, the realism traits as counted
      requirements (a superseded policy, a leaver, a runbook with no technique ID, one
      instruction-like paragraph), the forbidden topics and the format.
- [ ] The brief never mentions evals, planted stories or reasons. A recorded word check proves it.
- [ ] The script validates every document's front matter; checks owners and mentioned usernames,
      devices and assets against the tables, allowing the one leaver; checks the four absent topics
      stay absent; checks every document ID `truth.json` expects exists; and reports lengths.
- [ ] The script's tests use small good and bad samples: an unknown username, a missing field and a
      present absent topic each make it fail.
- [ ] Nothing in the brief names a real company or person.
- [ ] The author reads the brief before it goes to Codex; a dated line records it.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and Codex reviews the change.

## Comments
