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
- [ ] The brief records the allowed owner teams and assigns a responsible team to each internal
      document. Owners are not employee usernames and do not create login-account links.
- [ ] The script validates every document's front matter; checks owners against the allowed teams
      in the brief and mentioned usernames, devices and assets against the tables, allowing the one
      leaver; checks the four absent topics
      stay absent; checks every document ID `truth.json` expects exists; and reports lengths.
- [ ] The script's tests use small good and bad samples: an unknown owner team, an unknown mentioned
      username, a missing field and a
      present absent topic each make it fail.
- [ ] Nothing in the brief names a real company or person.
- [ ] The author reads the brief before it goes to Codex; a dated line records it.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 26 October 2026, author: internal documents belong to responsible teams, such as Security or
  IT Support, not to people selected from the login logs. This supersedes T04 d12's username
  requirement for document owners. Record the allowed teams in the brief and validate owners
  against that list. Mentions of people in document contents still resolve against the world;
  the one leaver remains an allowed mention. No new team table or owner-to-account link is required.

- 2026-10-26, author's S4 ruling: the corpus grows from 27 to 28 own documents, adding one incident record for Olivia's unexpected authentication approval. Follow the S4 evidence requirements in the spec: distinguish sign-in observations, her later statement and responder assessment; align UTC times; preserve unknowns. Use the document ID reserved by T12. Do not describe the event as prompt flooding, phishing-proxy compromise or token theft without supporting evidence.

- 2026-10-26, superseding the S4 ruling above: the author deferred the expanded authentication-attack story as premature for this phase. Restore the 27-document plan; no additional S4 incident record or email, web or SIEM evidence is required. S4's authentication explanation is open again on T12.

- 2026-10-26, final S4 ruling: the question is settled as intentional uncertainty, not a missing incident story. Keep the 27-document plan. Do not invent Olivia statements or S4-specific proof of authorisation, compromise or an authentication-attack mechanism. See the spec's S4 ruling.
