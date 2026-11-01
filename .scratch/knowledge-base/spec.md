# Spec: the knowledge base, phases 0 and 1

Status: ready-for-agent
Written: 25 October 2026, from the wayfinder map `map.md` and its resolved decision tickets 02 to 08,
read in full with their comments. Source of truth for this initiative's scope from this point on.
The API contract in `docs/api-contract.md` is part of this spec by reference; the additions it
needs are listed under "API contract changes" and are made in the build ticket that first needs
them. Existing terms (Investigation, Finding, Alert, Rule severity) are defined in the root
`GLOSSARY.md`; new terms, Dataset among them, are listed under Further Notes for `domain-modeling`.
Revised on 25 October 2026 after Codex's review; the triage and the author's six rulings are in
`reviews/spec-review-2026-10-25-triage.md`.

T46 revision, 30 October 2026: this spec now describes the approved Neo4j migration target.
T47–T49 implement and accept it; the existing application remains on the prior implementation
until that sequence completes. Resolved T02/T19/T20/T24 records remain historical evidence.

Every decision below cites the ticket that made it, as `T04 d6` (ticket 04, decision 6) or `T05 R3`
(ticket 05, ruling 3). A decision that no ticket made, and that the author ruled while this spec
was written, is marked **[spec ruling]**. The author ruled eight on 25 October 2026, one pop-up at a
time, each the recommended option; each is a row in the decisions log at the end. A decision the
author ruled on Codex's review is marked **[review ruling N]**; there are six, each a row in the
same log.

## Problem Statement

The Login Investigator flags suspicious sign-ins with four detection rules and lets an analyst
question an AI agent about them. The agent can see only the sign-in log and IP reputation
lookups. When a rule fires, the analyst still has to find out by hand who the account belongs to,
which groups it is in, which systems it can reach and how sensitive they are, who else shares its
laptop or network address, and whether a document explains the activity away (an approved trip, a
helpdesk ticket, a laptop handover) or makes it worse (an MFA exception, a policy breach, a known
attack technique). Today an alert is a flagged row, not an explained risk.

The analyst wants the agent to answer three questions for a flagged sign-in, with evidence they can
check: what happened, who and what it can reach, and whether it is actually a threat (T05 R1). The
author wants this built so it can be inspected, repeated and handed over: every claim the agent
makes must be traceable to a record or a passage, and every gate must be measured, not trusted.

## Solution

A knowledge base inside the app, built around a knowledge graph of the synthetic organisation with
hybrid text retrieval over a corpus of its documents. Semantic and keyword search find candidate
passages; the graph decides and explains what an account can reach (map, reference shape).

From the analyst's side:

- The Alerts table shows each finding's stable ID in its first column, and the Investigate button
  asks the agent about exactly that finding (T07 d7, T05 d5).
- In the Investigator chat, the analyst asks for an investigation. Nothing runs unless asked
  (T05 R3). The agent runs a fixed playbook in code: account context, reachable assets, peers by
  device and network, documents that clear the activity, documents that aggravate it. While it
  runs, the five steps stack on the screen (T07 d4).
- The answer gives a verdict, the three blast radii as counts, the graph path one line per hop, and
  short citation tags L (log), G (graph) and D (document) (T07 d2, d3, d6, d9).
- A third column holds two tabs. **Evidence** lists every cited record and passage for the
  investigation, downloadable as JSON (T07 d1, d5). **Graph** draws only the walk the agent made,
  read-only, with a click that lights the matching evidence (T08 d1 to d8).
- When nothing in the corpus answers a question, the agent says so, with the closest misses shown
  (T03 d1). When a document clears the activity, the agent says the alert is benign and cites it
  (T04 d8).
- The report cannot be written until every required playbook step has run, or it names the step
  that could not run and why (T05 d11).

From the author's side:

- One generator writes the whole synthetic world, its log and its answer key (T04 d1, d15).
- One PostgreSQL database with pgvector holds the organisation's tables, the document chunks, their
  vectors and their keyword index, rebuilt from the files on every build (T02 d1, d5, d6).
- The app refuses to start on a database built from older files than the ones on disk.
- A second eval question file measures retrieval and answers separately, with per-question hard
  gates, and the Port's eval keeps passing unchanged beside it (T06 d1 to d8).
- Native Neo4j Browser inspection shows the graph and a finding's neighbourhood (T46).
  This replaces the Gephi/GEXF workflow after the author's walkthrough; the in-app Graph tab remains.
- Langfuse mirrors traces and eval runs behind a switch; the repo stays the source of truth
  (T06 d10).

**Scope (map, author's ruling 20 October 2026).** Phase 0, Foundation: graph store, synthetic data
generator with written ground truth, text corpus, hybrid retrieval with re-ranking, the eval harness
with its first questions, read-only agent tools over graph and corpus. Gate: the eval harness runs
end to end, retrieval and answer layers measured separately. Phase 1, Blast radius: slice 2
(spray-to-compromise blast radius) plus spread and shared ground. Gate: eval pass on the phase 1
questions, and the author accepts the live screen. The initiative closes there.

## User Stories

**The analyst, alerts**

1. As an analyst, I want every alert to carry a short stable ID shown as the first column of the
   Alerts table, so that I can name a finding in chat and match it to the report and the evidence.
2. As an analyst, I want the same log to give the same finding IDs every time, so that an ID I wrote
   down yesterday still points at the same alert today.
3. As an analyst, I want the Investigate button to put a question carrying the finding ID into the
   chat, so that the agent investigates exactly that alert rather than guessing it from my words.
4. As an analyst, I want the four detection rules to behave exactly as they do today, so that
   nothing I have learned about the alerts changes under me.
5. As an analyst, I want the new successful spray (S6) to appear on the Alerts screen like the other
   planted attacks, so that I can investigate a spray that actually got in.
6. As an analyst, I want the benign look-alikes that the rules can catch to appear as alerts too, so
   that I can see the investigator clear what the rules wrongly flag.

**The analyst, asking for an investigation**

7. As an analyst, I want the investigation to start only when I ask for it in chat, so that nothing
   runs and nothing is spent without my say.
8. As an analyst, I want to ask a narrow question ("who owns this laptop?") and get a narrow answer,
   so that a lookup does not run the whole playbook.
9. As an analyst, I want to ask for a full investigation in my own words, so that I do not have to
   learn a command syntax.
10. As an analyst, I want to see the five investigation steps stack on screen while they run, so
    that I know the full playbook is under way and how far it has got.
11. As an analyst, I want the step list to fold into the Tools used drawer once the answer arrives,
    so that the chat stays readable afterwards.
12. As an analyst, I want the Port's quick tools to keep their single status line, so that short
    lookups do not clutter the chat.
13. As an analyst, I want to follow up with questions after an investigation, so that I can dig into
    anything the answer raised.
14. As an analyst, I want to ask about an innocent change that no rule flags, such as a laptop swap,
    and be told it is innocent with the record that shows it, so that the agent never raises a false
    alarm where an explanation exists.

**The analyst, reading the answer**

15. As an analyst, I want the answer to state who the account belongs to, its department and its
    privilege groups, so that I know whose account it is.
16. As an analyst, I want the answer to say which assets the account can reach and how sensitive
    each is, so that I can judge the damage a compromise could do.
17. As an analyst, I want the answer to say who else shares the account's device and network
    address that week, so that I can see where the problem may spread.
18. As an analyst, I want the three radii (groups, assets, peers) as counts with the worst item
    named, so that I see the scale without reading a long list.
19. As an analyst, I want the full lists of groups, assets and peers in the evidence panel, so that
    I can check every item when I need to.
20. As an analyst, I want the graph path written one line per hop, each hop a short sentence with its
    own citation tag, so that I can read the path aloud and check each step.
21. As an analyst, I want a clear verdict (threat, benign, or cannot tell) on one coloured surface,
    so that my eye finds the conclusion first.
22. As an analyst, I want a benign verdict to name the document that cleared it in a "Cleared by"
    line, so that I can see why the alert was dismissed.
23. As an analyst, I want the answer to say when a document makes the activity worse, such as an MFA
    exception on a compromised account, so that I learn why the attack worked.
24. As an analyst, I want an attack technique mapped from MITRE ATT&CK to be stated as "consistent
    with" until the evidence supports more, so that the agent never overstates its case.
25. As an analyst, I want every factual claim tagged with a short citation (L1, G1, D1), so that I
    can see where each claim came from.
26. As an analyst, I want citation tags in a calm link colour, so that I can tell they are clickable
    without them shouting.
27. As an analyst, I want a warning in amber when a citation could not be verified, so that I never
    mistake an unchecked claim for a checked one.
28. As an analyst, I want the agent to say plainly when the knowledge base has nothing on my
    question, and show the closest misses, so that I can trust its silence as much as its answers.
29. As an analyst, I want the agent to say "cannot tell" when the evidence is weak, so that a guess is
    never dressed as a finding.
30. As an analyst, I want the agent to report an instruction found inside a log field or a document
    as evidence of an attack, never obey it, so that planted text cannot steer my investigation.

**The analyst, the evidence panel**

31. As an analyst, I want a third column beside the chat listing every cited record and passage for
    the investigation, so that all the proof sits in one place across turns.
32. As an analyst, I want a click on a citation tag to highlight its row in the evidence panel, so
    that I can check a claim in one move.
33. As an analyst, I want document and log text in the panel shown as plain text, so that nothing in
    the data can render as a link, an image or markup.
34. As an analyst, I want to download the evidence as a JSON file, so that I can hand the case to a
    colleague or keep it with my notes.
35. As an analyst, I want the download to hold only what the panel shows, never the prompt or the
    memory file, so that nothing internal leaves with it.
36. As an analyst, I want the third column to fold under the chat on a narrow screen, so that the
    app stays usable on a small window.

**The analyst, the graph panel**

37. As an analyst, I want a Graph tab beside the Evidence tab that draws the walk the agent made for
    the answer I am reading, so that I can see the path as a picture.
38. As an analyst, I want the graph to show only the nodes and edges the walk returned, so that the
    picture never suggests a link the agent did not find.
39. As an analyst, I want the graph laid out top to bottom in playbook order (account, groups,
    assets, shared devices and addresses, peers), so that I read it the same way every time.
40. As an analyst, I want shape to say type (circle person, rounded box group, square asset, diamond
    device, pill address), so that I can tell nodes apart without reading every label.
41. As an analyst, I want the account under investigation as the one dark node and restricted assets
    marked with a small red R, so that the important nodes stand out.
42. As an analyst, I want internal assets and the many peers folded into one node with a count, so
    that a wide radius does not make the panel long.
43. As an analyst, I want a click on an edge to switch to the Evidence tab and light its row and hop
    line, so that a highlight never hides in a tab I cannot see.
44. As an analyst, I want a click on a node to light every evidence row that touches it, so that I
    see everything the answer said about it.
45. As an analyst, I want an edge the walk returned but the answer never cited to say "Walked, not
    cited in the answer" with its record ID, so that I know the difference between found and used.
46. As an analyst, I want the Graph tab always present, with one quiet line when no walk ran, so that
    the controls never move under me.
47. As an analyst, I want the graph to be read-only, with no dragging, connecting or deleting, so
    that the picture cannot drift from the record.
48. As an analyst, I want every graph label as plain text, clipped when long, with the full value and
    record ID on hover, so that labels stay readable and safe.

**The analyst, the report**

49. As an analyst, I want the incident report to be written only after every required playbook step
    has run, so that the report is never partial.
50. As an analyst, I want a step that could not run to be named in the report in one plain line with
    its reason, so that silence never reads as a clean result.
51. As an analyst, I want the report to keep the Port's shape, PDF and severity scale, so that what I
    already use keeps working.

**The author, the synthetic world**

52. As the author, I want one seeded generator to write the organisation, the log and the answer key
    together, so that the world cannot fall out of step with itself.
53. As the author, I want the Port's 50 users and five planted stories kept exactly, so that the
    Port's eval survives with the fewest changes.
54. As the author, I want six departments, three privilege groups, ten assets with sensitivity and
    owner, a device register and a VPN pool drawn around the users, so that there are three
    different blast radii to test.
55. As the author, I want the log to gain an MFA result and a device ID per row, so that "why did the
    spray work" and "same device, different user" become facts.
56. As the author, I want each dataset to live as one folder (tables, log, answer key, corpus,
    README), so that the world travels as one unit and a swap is naming another folder.
57. As the author, I want the generator to write S6's blast radius into the answer key and a test to
    recompute it from the tables, so that the answer key cannot quietly disagree with the world.
58. As the author, I want four planted gaps (no incident write-ups, nothing on the backup server, no
    retention policy, two users no document names), so that refusal is tested on plausible
    questions with no source.

**The author, the corpus**

59. As the author, I want thirteen MITRE ATT&CK pages fetched from the STIX bundle at one pinned
    version with MITRE's licence beside them, so that technique text is accurate and properly
    licensed.
60. As the author, I want the 27 own documents written by a standalone Codex session from a brief
    kept in the repo, so that the writer never knows the exam.
61. As the author, I want a consistency script to check every document's front matter, its owner
    against the agreed team names, and mentioned people, devices and assets against the tables,
    so that facts in the corpus are checked by code and humans read only for feel.
62. As the author, I want realism traits planted (a superseded policy, a leaver, a runbook with no
    technique ID, one instruction-like paragraph), so that the corpus has the mess a real one has.

**The author, the store and the build**

63. As the author, I want the knowledge base in my installed PostgreSQL with pgvector, so that I run
    one database I already know.
64. As the author, I want the database rebuilt from the files for each test session and each eval
    run, then dropped, so that no run inherits another's state.
65. As the author, I want the running app's database built once by one build command and kept until
    I rebuild it, so that my investigations never trigger a rebuild.
66. As the author, I want the app to refuse to start, with the build command in the message, when the
    world's files no longer match the files its database was built from, so that it never answers
    from an old world.
67. As the author, I want a test that needs PostgreSQL to fail loudly with the start command when the
    service is down, never skip, so that a missing database is never mistaken for a pass.
68. As the author, I want the agent to use hand-written read-only functions, with PostgreSQL
    reader privileges and database-enforced graph-data write prevention. Neo4j Community's
    administrative access is an accepted development limitation under T46, not least privilege.
69. As the author, I want a graph integrity check to run every time the graph is built and fail on
    the first mismatch, so that a silent build error never becomes a confident wrong answer.
70. As the author, I want tested native Neo4j Browser views of the organisation and a finding's
    neighbourhood, with build identity and display limits visible, so I can inspect the graph
    by eye without a separate Gephi export (T46 supersedes T08 d9 for future builds).

**The eval runner (the author or Codex, without Claude)**

71. As the eval runner, I want a second question file for the knowledge base beside the frozen Port
    file, so that "does the new thing work" never hides "does what worked still work".
72. As the eval runner, I want every gold chunk ID found among the 20 fused candidates and among
    the chunks the model received, per question, so that a broken search and a broken ranking each
    fail the run.
73. As the eval runner, I want every graph question's walk to return exactly the gold set, so that an
    extra or missing record is caught as a bug.
74. As the eval runner, I want every citation to resolve and every gold ID to be cited, so that the
    right evidence was used, not just found.
75. As the eval runner, I want say-no questions graded from the tool verdict at 100%, so that refusals
    and benign twins never slip.
76. As the eval runner, I want the playbook check and the canary check at 100%, with canaries counted
    as security, so that the process and the injection defence are graded, not assumed.
77. As the eval runner, I want the retrieval layer runnable alone, calling search and walk directly
    with no model, so that retrieval is checked exactly and cheaply on every build.
78. As the eval runner, I want the refusal threshold chosen offline from saved scores on a separate
    tuning file, so that the refusal test never passes by construction.
79. As the eval runner, I want the re-ranker and BM25 each kept only if an on-versus-off comparison
    shows they help, so that complexity is earned by measurement.
80. As the eval runner, I want a faithfulness judge from another model family to report a rate with
    its interval, never failing a run, so that I get an early warning without gating on noise.
81. As the eval runner, I want the version fingerprint to cover the judge, the embedder, the
    re-ranker, chunking and the corpus version, so that two runs are comparable only when they
    should be.
82. As the eval runner, I want every check rescored from the saved run file with no model call, so
    that a scoring fix never needs a new paid run.

**The author, observability**

83. As the author, I want Langfuse traces of dev investigations and eval runs behind one switch that
    is off by default, so that I learn the platform without making the app depend on it.
84. As the author, I want the JSON result file written before anything goes to Langfuse, and an
    upload failure shown loudly in the summary, so that the repo stays the evidence.
85. As the author, I want my judge labels made in Langfuse to come back only through an export script
    into a repo file, so that nothing at runtime reads from Langfuse.

**The reviewer (the build loop's code review)**

86. As the reviewer, I want each build ticket to name the decision it implements, so that I can check
    the code against the decision and not against my guess.
87. As the reviewer, I want every new Python file clean under the type checker with no ignore entry,
    so that the new code starts at the bar the Port set.

## Implementation Decisions

### The synthetic world and the dataset (T04)

- **One generator, extended** (T04 d1). The Port's seeded generator keeps its seed, its seven-day
  window ending 8 October 2026 09:00 UTC, its 50 users, two offices, home addresses, three decoys
  and stories S1 to S5 exactly. The organisation is drawn around them in the same generator.
- **The organisation** (T04 d2 to d5): six departments (Engineering, Finance, HR, Sales, Operations,
  IT); three privilege groups (IT Admins, Finance Approvers, HR Data Owners, 3 to 5 members each);
  ten assets with sensitivity (internal, confidential, restricted) and an owner, as T04 d3 lists;
  one laptop per user plus two shared machines used by three users each, across a department; a
  networks table with the four-address VPN pool handed out in turn.
- **Two new log columns** (T04 d4, d7): `device_id` and `mfa_result` (`pass`, `fail`, `none`,
  `denied`; `denied` unused and reserved). They flow through the loader's column list from the
  generator. The four rules do not read them (T05 d15).
- **[spec ruling] `device_id` is empty for unregistered devices.** Attacker sign-ins (S1 to S6) carry
  an empty `device_id`, because the attacker's machine was never registered. Employee sign-ins from a
  phone are empty too: personal phones are not in the device register (124 rows, 7.7% of employee
  rows in the Port's log; amended at ticket 11 from "about 3 to 5%"). An empty value is a clue,
  never proof of an attack, as in real sign-in logs. Twins B2 and B3 keep their laptops. No scenario
  is built around personal devices; the empty share exists so the data stays realistic.
- **S6** (T04 d6): a new attacker address with its own saved reputation file sprays many accounts
  and succeeds once on an IT Admins member, on a day that overlaps neither S1 nor S2, followed by
  two more sign-ins from that address. Both compromised accounts (S3's and S6's targets) are on the
  documented MFA exception list, so their rows carry `mfa_result = none`.
- **[author's ruling, 26 October 2026] S4 is intentionally unresolved.** Keep the existing
  successful sign-in to Olivia's account from the Russian source address and `mfa_result = pass`.
  Do not add her to the MFA exception list. The event warrants investigation for its unusual
  country, but the available evidence establishes neither authorisation nor compromise, Olivia's
  physical location, who completed MFA, or an attack mechanism. The knowledge-base answer key
  records these limits explicitly; evaluation accepts a suspicious event with an unknown cause
  and must not demand confirmed compromise or a named MFA attack. This is an evidence limit on
  an existing story, not a fifth absent topic or a new retrieval verdict. No new incident record,
  email, web or SIEM data is required; the corpus stays at 27 own documents. The Port's original
  events and ground-truth shape remain unchanged.
- **Three benign twins** (T04 d8), each cleared by one document: B1 approved travel (a Sales user in
  Germany for three days, travel notice), B2 reset burst (a user failing repeatedly from their own
  laptop, then succeeding, helpdesk ticket), B3 laptop swap (a user's rows switch `device_id`
  mid-week, IT handover record). S6 and the twins fall on days that do not overlap the old stories
  S1 to S5 (T04 conditions).
- **[spec ruling] B2 fails at least 20 times within an hour, then succeeds.** T04 d8 said eight
  failures and set the condition that each twin must trip the Port's rules. The brute-force rule
  needs 20 failures on one account from one address within an hour, and success-after-failures needs
  10 failures in the hour before a success; eight trips neither, and the rules may not change
  (T05 d15). The condition outranks the number. B2 now trips brute force and success after failures.
- **[spec ruling] B3 is tested by asking about it directly.** None of the four rules reads
  `device_id`, so B3 can never appear as an alert. The knowledge-base question file asks the agent
  about the laptop change; it passes only if it finds the IT handover record and calls the change
  benign. T04 d8's rule-tripping condition applies to B1 and B2.
- **One folder per dataset** (T04 d13): organisation tables (people, groups, memberships, assets,
  grants, devices, device assignments, networks), the log, `truth.json`, the own corpus, the ATT&CK
  corpus with MITRE's licence, and a README naming the seed and the ATT&CK version. The generator
  writes everything but the two corpus folders.
- **[spec ruling] The regenerated world is the dataset folder called `default`.** The app's setting
  names a dataset folder instead of a single log file, and replaces the Port's log-path setting in
  the regeneration ticket. The Port's old log file is retired, since the regenerated log keeps all
  its stories. Swapping worlds is naming another folder; the eval runner's isolation keeps working
  the same way.
- **[spec ruling] The Port's ground-truth file stays.** The Port's scorer reads it for S5's planted
  text, to grade the injection questions; the pattern names its checks use come from the Port's
  question file, not from this file. The run fingerprint also lists it. The generator keeps writing it in its current shape beside
  `truth.json`, so the Port exam stays frozen (T06 d8). `truth.json` is the knowledge base's answer
  key. One generator writes both from one world, so they cannot disagree.
- **The answer key** (T04 d15, T06 d2): `truth.json` holds each story S1 to S6, S6's blast radius
  (groups held, assets reached, users sharing its device, expected
  citation document IDs), each twin with verdict `benign` and its clearing document ID, the MFA
  exception list, and the four absent topics (T04 d14). Gold paths and radii are written from the
  planted story, never computed afterwards as a shortest path.
- **Chosen when the tables are built** (T04 conditions): group membership, S6's target, the leaver's
  name, the two never-mentioned users. Written into `truth.json`.
- **The Port's exam after regeneration** (T04 d17): the Port's eval questions pass unchanged; where a
  new story changes a whole-log count, the expected value is updated with its reason recorded.
  Port-level questions are added for S6 only. Ticket 43 extends the exception to expected facts:
  Q02 and Q04 gain checks for S6, with nothing removed (decisions log, 26 October 2026). This gate passes before any corpus or retrieval work.

### The corpus (T03, T04)

- **Thirteen ATT&CK pages** (T04 d9): T1110 and its four sub-techniques, T1078 with the
  domain-accounts sub-technique, T1621, T1021, and the four linked mitigations, fetched from the
  STIX bundle by a script kept in the repo, assembled from linked objects (T03 d3), version pinned
  in the dataset README and in each page's front matter.
- **Twenty-seven own documents** (T04 d10, d11): the fifteen core documents and twelve noise
  documents T04 lists, with the realism traits planted inside them.
- **Front matter** (T04 d12): `id`, `title`, `kind` (policy, runbook, register, record, meeting,
  email, guidance, attack), `owner`, `department`, `date`, `version`, `status`, `supersedes`.
  **Author's ruling, 26 October 2026:** internal documents name a responsible team in `owner`,
  such as Security or IT Support, not an employee username. Ticket 15 records the allowed team
  names and each document's assignment in the brief. The owner field does not establish a link
  to a login account. ATT&CK pages identify their external publisher with `owner: mitre` and
  `department: external`; these are provenance labels, not accounts. This supersedes T04 d12's
  username requirement for document owners. Asset ownership in the organisation tables is unchanged.
  Mentions of users, devices, assets and technique IDs are found by ingestion from the text, never
  hand-written.
- **The Codex brief and the consistency script** (T04 d16): the brief lives in the initiative
  folder, carries the organisation's facts, the 27-file list with headers, the traits as counted
  requirements, the forbidden topics and the format, and never mentions evals, planted stories or
  reasons. The script validates every front matter, checks internal owners against the agreed team
  names in the brief, and checks mentioned usernames, devices and assets against the tables
  (allowing the one leaver). It checks the four absent topics stay absent
  and reports lengths. Nothing in the corpus names a real company or person.

### The store and the build (T02, T03)

- **Two stores, one version** (T46 supersedes T02 d1): Neo4j Community serves graph queries;
  PostgreSQL with pgvector owns passage text, metadata, embeddings and keyword search.
  Neo4j holds organisation entities, typed relationships and passage references joined by
  stable chunk IDs and `mentions` edges, not duplicate passage text. PostgreSQL organisation
  reference tables remain for independent checks and existing consumers during migration.
  Source files remain authoritative. Neo4j 2026.10.1 and Python driver 6.1.0 were proved on
  the Intel Mac; build tickets pin their adopted versions and recheck changed behaviours.
- **Service prerequisites** (T02 d4, extended by T46): PostgreSQL remains the installed service;
  Neo4j build/serving instances are separately managed and isolated. Tests that require either
  service fail loudly with the appropriate start instruction, never silently skip.
- **Fresh resources per test session and eval run** (T02 d5, extended by T46): use unique
  PostgreSQL databases, graph resources, source snapshots and state files. Clean failed builds;
  prove isolation from the active pair. Tests not requiring these services remain service-free.
- **The files are the truth** (T02 d6). The loader is the sync job; the database is a build artefact,
  never edited by hand. Full rebuild on every build (incremental sync is AUD-033).
- **[spec ruling, extended by T46] The running app's pair is built once and stays.** "Every run" means every
  build, never a question or a chat session. A build happens at the start of each test session, at
  the start of each eval run, and when the author or Codex runs the one build command after the
  world's files change. Nothing watches the files. Capture an immutable source snapshot;
  build and independently validate both stores before publishing a credential-free pointer
  naming their shared build ID, fingerprint and source snapshot. Adopt the new pair on a
  planned restart. Retain the previous pair and matching snapshot for explicit rollback by
  selection and restart. Do not publish a partial pair or automatically delete prior versions.
  Measure interruption during actual application integration; no maximum has been assumed.
- **[spec ruling] The staleness guard.** Every build records in the database a fingerprint of the
  dataset folder's files (hidden entries skipped; T18 decision 3) together with the embedding model, the vector length and the chunking
  settings. Under T46, startup recomputes it from the selected immutable source snapshot and
  checks both stores' matching build identity and readiness. All login analysis, retrieval and
  graph reads use that selected version. Editing working source inputs prepares a future
  rebuild; it does not mutate the published snapshot. Tampering with the selected snapshot
  or mixing versions is refused. **[review ruling 6]** On
  a mismatch, the server does not start: startup fails loudly with fixed text naming the build command. This is
  stricter than today's invalid log, where the server starts and the dataset endpoints answer with
  an error. The app never combines a database with a different source world. T18's no-build
  startup remains: without a published knowledge base, start with the existing non-KB behaviour.
- **Read-only controls** (T02 d8, qualified by T46): tools are hand-written parameterised core
  functions, with no model-written SQL or Cypher. PostgreSQL retains separate builder and reader
  roles. Neo4j uses isolated writable preparation, retired builder credentials and graph-data
  read-only serving before publication. Verify write refusal, restart persistence and builder
  separation; Community's administrative powers remain the explicit exception below.
- **Agent memory stays in SQLite** (T02 d9; AUD-032).
- **T46 development-stage ruling, 30 October 2026:** Neo4j Community is selected for development
  under the approved migration tickets despite lacking a restricted reader identity. Its serving
  account's administrative powers are an explicitly accepted development-stage limitation,
  not evidence of least privilege. Carry graph-data write prevention and separate writable
  builds from the proof into integration tests. Before production use, review permissions, recovery,
  availability, monitoring and cost, including an Enterprise upgrade or another suitable
  control. AUD-068 tracks that future gate. The approved build sequence is T47 to T49;
  implementation starts separately under each ticket's model-confirmation rule. The exception
  does not weaken PostgreSQL reader separation or permit model-written queries or agent writes.
- **[author's ruling, 25 October 2026] Our code reaches its tables through SQLAlchemy Core**, not
  its ORM, on the psycopg driver (`postgresql+psycopg://`). The tables are defined in code and
  created at each build. One engine and its connection pool are shared with LangChain's store,
  whose `PGEngine` is an SQLAlchemy engine. The read-only role is a second engine with its own
  connection string. Queries stay hand-written, parameterised functions in the core (T02 d8).
  Server-level work (the ping, creating and dropping a database) stays on psycopg directly, as
  ticket 09 built it.

### Chunking, embedding and retrieval (T03)

- **Chunks** (T03 d3): cut at Markdown headings, then by token size only inside an over-long section,
  overlap never crossing a section. Every chunk begins with a context header: document title,
  section path, and technique or incident ID. Sizes per kind (note 03, section 3.2) are confirmed
  against the real corpus in the corpus-delivery ticket.
- **Chunking rulings at T16** (author, 27 October 2026, measured in T16's length comparison):
  - Email, guidance, meeting, record and register documents take the policy row: 350 tokens,
    overlap 30 to 50.
  - Runbooks keep their row. A numbered step always lands whole in one chunk, proven by a test.
  - ATT&CK pages: the `## References` section is not chunked; inline `(Citation: ...)` markers are
    removed from chunk text; Markdown links keep their visible text and lose the address; the
    stray `<code>` tags are removed. The files stay unchanged. A test fails if the converter's
    format changes so that any of these slips back in.
  - ATT&CK procedure examples are packed into chunks of up to 350 tokens, several per chunk, each
    example whole, under the field group's context header (note 03's one chunk per field group),
    instead of one chunk per example.
- **Chunk storage** (T02 d7): in the table LangChain's PostgreSQL store creates, with typed filter
  columns (document type, technique ID, incident ID, version, effective date) and a JSON column for
  per-kind details. A field becomes a column only when filtering on it proves necessary (T03 d6).
- **Identifiers are labels, not prose** (T03 d4): single-value identifiers are typed columns; mentions
  of accounts, hosts and other entities live in a chunk-to-entity link table, which also feeds the
  graph's `mentions` edges. Phase 0 records the keyword parser's output for one technique ID,
  hostname, IP address and email address.
- **Embeddings** (T03 d2): `openai/text-embedding-3-small` through OpenRouter at 1,536 dimensions,
  with the context-length check switched off. Model name and vector length in one configuration
  place; a change is a rebuild. No local models.
- **Keyword leg** (T02 d3): PostgreSQL's built-in text ranking first. BM25 is added only if the
  on-versus-off comparison says so (T06 d9).
- **Filters** (T03 d6): applied inside both the vector and keyword queries before their limits.
  Vector search stays exact, with no approximate index, in phases 0 and 1. The agent picks typed
  options on the tool; code builds the filter; the model never writes one.
- **Fusion** (T03 d7, T02 d10): our own reciprocal rank fusion, k = 60, equal legs, 20 plus 20
  candidates, 1-based ranks. Every candidate's dense rank, keyword rank, raw cosine distance, raw
  keyword score and fused score is recorded. Three library traps, each with a test: the fusion
  function is set explicitly; both candidate limits are set explicitly; a fresh hybrid-search
  configuration is built per call, proven by a two-question regression test.
- **Re-ranker** (T03 d5): `cohere/rerank-v3.5` through OpenRouter's rerank endpoint, our own
  document compressor behind LangChain's compression-retriever seam, 20 re-ordered to the best 5,
  behind a switch. Its score drives the verdict.
- **Three verdicts in code** (T03 d1): the corpus search returns `none`, `weak` or `found` with the
  chunks, computed from recorded scores before the model sees anything. The `none` rule stays off
  until the threshold is calibrated on the tuning file (T06 d4); until then the system answers and
  the eval shows how often it should have refused. If the re-ranker is switched off, `none` falls
  back to the empty-result rule, and the tuning file is re-scored with whatever score source
  remains to calibrate a threshold on it (T06 d9). The empty-result rule alone cannot refuse on a
  non-empty corpus, since exact vector search always returns candidates; the switch rule under
  "The eval" guards this.
  Author's T22 ruling (29 October 2026): before calibration, return `weak` with an explicit
  `not_calibrated` reason and keep the `none` rule disabled. Do not invent a relevance threshold.
  Author's T23 ruling (29 October 2026): a search that returns zero passages gives `none` with
  reason `empty_result`, with the re-ranker on or off. It is a counted fact and needs no threshold.
- **Pinned versions** (T02, T03 conditions): `langchain-postgres` 0.0.19, `langchain-text-splitters`
  and `tiktoken` pinned exactly; one OpenRouter key for chat, embeddings and re-ranking.

### The graph (T02, T06, T08)

- **App lifecycle (T46, replacing the T19/T24 in-memory preparation detail):** each backend
  process opens one knowledge-base context owning its PostgreSQL pool and Neo4j driver. Check
  source freshness, pair identity/readiness, graph integrity and serving protection before
  accepting questions. Reuse these clients across investigations with short-lived per-query
  sessions; close both on shutdown or partial startup failure. Do not rebuild a graph on a
  question. Adopt rebuilt versions only on controlled restart; no automatic hot replacement.
  Preserve T18's no-build behaviour. T48 verifies this integration and measures interruption.
- **Execution and errors (T46):** preserve the named synchronous graph operations for existing
  tool callers; move network waits off the event loop at asynchronous callers. Use bounded
  calls, fixed public failures and explicit cleanup. Test cancellation and concurrent
  investigations without leaking per-call state. No database-native objects cross core results.

- **VPN address meaning (author, 28 October 2026):** the synthetic VPN pool represents
  session-assigned addresses reused over time, following the remote-access policy. It is not a
  public-exit pool. Matching an address across different sessions establishes reuse only, not
  shared-device use, simultaneous connectivity, exposure or spread. No new telemetry is approved.
- **Address-sharing context removed (author, 1 November 2026, T25 gate):** sharing an address
  answers no investigation question the data supports. The attacker's address is already
  covered by `search_logins(ip=...)` and the spray finding; co-users of office and VPN addresses
  cannot single anyone out without allocation records (AUD-073). The radius, the answer key,
  `find_peers` and later agent/screen presentation carry no address-sharing context. T50 removes
  it. Supersedes the 28 October 2026 rulings that retained it as labelled supporting context.
- **Address grouping (author, 28 October 2026):** superseded on 1 November 2026 by the removal
  above; see [T25](issues/25-peers-and-corpus-search-tools.md).
- **Relationship dates (author, 28 October 2026):** optional user-supplied start and end times
  filter login-based graph relationships; omitted bounds use the available log period. Follow
  the existing log tools' UTC convention (start included, end excluded). Results state the
  requested/effective period and available coverage; they must not imply complete coverage
  outside the available records. Organisation permissions remain a snapshot, not historical
  permissions. This supersedes fixed "that week" wording for these relationships.

- **Walked in Neo4j** (T46 supersedes T02 d2), through fixed parameterised queries behind named
  core operations. Chunks remain reference nodes joined to entities by `mentions` edges; their
  text and search metadata stay in PostgreSQL. Preserve exact IDs, records, deterministic path
  ordering and date semantics. Retire NetworkX query/export paths at T49; no second permanent
  graph engine or transient Gephi exporter is required in the selected final architecture.
- **No `used address` edges (author, 1 November 2026, T50):** the build draws no `used address`
  edges, because nothing reads them once address-sharing context is removed. Network nodes stay
  as organisation facts, with their `mentions` links. The log keeps every sign-in, so a later
  phase can rebuild the edges from source. The superseded rule follows as history.
- **[review ruling 1, superseded 1 November 2026] "Used address" edges come from the log.** No organisation table links a person
  to a network address; the log is already the truth for who signed in from where. The build draws
  one `used address` edge per distinct user and network address pair in the log, for addresses in
  the networks table. The row filter (for example, successful sign-ins only) is fixed in the
  graph-build ticket and written beside the radius in `truth.json`. These edges serve the peers-by-
  network step and the Graph tab (T08 d6). No copy of them is written as a table, so the two cannot
  drift.
- **Code walks, the agent reads** (T05 R5): one core function computes the radius for phase 1's fixed
  questions and returns it already joined. The same function is what the generator's answer-key test
  recomputes, so the tool and the key share one implementation. The hop-by-hop walk is a seam for
  phase 4, not built.
- **The integrity check** (T06 comment of 24 October 2026; strengthened by review ruling 1): one core
  function runs whenever the graph is built and fails loudly on the first mismatch. It compares
  identities, not only counts: a count is necessary but not sufficient, since a swap of two valid
  links keeps every count right. The check reads its sources with its own code, never through the
  build's.

  | Source | Becomes | Check |
  |---|---|---|
  | A row in an entity table | one node | the set of node IDs per type equals the set of row IDs; each node's attributes that a walk reads (sensitivity, owner, department) equal its row's values |
  | A row in a link table | one edge | the set of (source ID, target ID, type) per type equals the set read from the rows |
  | A distinct user and address pair in the log | no edge since 1 November 2026 (was one `used address` edge) | no `used address` edge exists |
  | A chunk | one node | the set of chunk node IDs equals the database's chunk IDs |
  | A chunk-to-entity link | one `mentions` edge | each chunk's `mentions` edges equal its rows in the link table, an empty set included |

  Plus no isolated node of type person, group, asset or device. A chunk with no `mentions` edge is
  valid when its text names no entity, as the row above checks; a network address no one used may
  stand alone. The retrieval layer reports the check as its precondition.
- **Native inspection** (T46 supersedes T08 d9 and the future maintenance of T20's export):
  use Neo4j Browser against the intended read-only serving graph, with tested queries for the
  organisation and a finding's exact neighbourhood. Verify node/edge identities, build identity,
  styling and display/result limits. Record the author's walkthrough before retiring the
  Gephi command and its GEXF-specific tests. The Browser shows passage references, not automatic
  PostgreSQL passage-text joins. No replacement portable GEXF deliverable is promised. Historical
  T20 evidence remains. Browser is an admin inspection tool, not the in-app saved-evidence Graph tab.

### The IDs (T05)

- **IDs are made from content, never from storage order** (T05 d5), because the database is rebuilt
  on every build and the eval's answer key points at these IDs.
- **Finding: `F-<rule>-<hash8>`**, the rule slug plus an eight-character hash of the finding's
  defining fields (rule, users, addresses, first and last seen), following the pattern Elastic
  Security, Splunk and Sigma share. A new field on the core's finding and on the Alerts reply. The
  four rules' logic is untouched (T05 d15). The exact hash fields and slug rules are fixed in the
  finding-ID ticket.
- **Chunk: `<doc-slug>@<version>#<section-path>/<ordinal>`.** The need for a stable identifier is
  backed by Anthropic's citation documentation; the shape is this initiative's own design.
- **Graph record: the ID the generator writes into the world's files.**
- **[spec ruling] These formats win over the placeholder examples in tickets 07 and 08** (`F-0006`,
  `reg-mfa-exceptions#7`, `mem-0117`), which were illustrations on a sketch.

### The agent, its tools and its playbook (T05)

- **Seven typed tools in one tuple** (T05 d1): the Port's three unchanged except one added field
  (ticket 43: each finding in `find_suspicious_activity`'s output carries what its address did
  in the tool call's window and drops the rule's own success and failure counts, and a
  brute-force or spraying finding whose address signed in gets one code-built sentence on its
  summary saying so, for the agent only; the core finding and the Alerts reply are unchanged),
  plus
  `investigate_alert(finding_id, start?, end?)`, `lookup_account(account_id)`,
  `find_peers(account_id | device_id, start?, end?)` and
  `search_corpus(question, doc_type, technique_id)`. No router tool, no sub-agent. All hand-written,
  parameterised, read-only. The model and agent are still created in exactly one function each.
- **The investigation package** (T05 d2, d3): `investigate_alert` bundles playbook steps 2 to 6 into
  one package with a named section per step (account context, reachable assets, peers, clearing
  documents, aggravating documents), each with its own verdict and citations, computed and ordered
  in code. Spray and brute-force targets are a section of it, empty for other rules. The clearing
  and aggravating searches are built in code from the finding's record, never from the chat
  (T05 R5).
- **Progress per internal step** (T05 d2, T07 d4), streamed through the Port's custom stream.
- **Content plus artifact** (T05 d4): every knowledge-base tool returns a short labelled text for the
  model and a full artifact (cited chunks with text and IDs, graph records, every recorded score,
  the verdict), saved by the checkpointer, read by the eval and the screen, never sent to the model.
  Phase 0 proves the artifact survives the SQLite memory round trip (T05 conditions).
- **T24 browser compatibility (author, 29 October 2026):** accept `lookup_account` in the
  existing tool progress event and show “Looking up account context…” in the existing single
  status line; label its saved tool result. This small part of the widened tool-name list moves
  forward from T36 so the phase-0 lookup works in chat. The remaining names and step stack stay
  with T36; no new screen or evidence panel is introduced.
- **Package caps** (T05 d12): five chunks per corpus search; assets and peers paged with a
  `truncated` flag in the content; full lists in the artifact.
- **Citations** (T05 d6, T07 d6): short per-answer labels L, G and D, numbered per answer, resolved in
  code against the investigation's artifacts after the model answers. A label that resolves to
  nothing sends the model back once with a correction; a second failure shows the answer with the
  amber unverified warning. This is the per-turn light gate (T05 R4).
- **One resolver** (T07 hand-offs, T08 hand-offs): the code that resolves citations for the screen's
  `evidence` and projects the `graph` is the same code the eval's `cites` check uses, so screen and
  exam cannot disagree.
- **The playbook is one data structure in the core** (T05 d14): a list of steps, each with the tool
  and section that serve it and a required-for-report flag, read by the policy hook, the report gate
  and the eval. Later phases add rows, not code paths.
- **The middleware, extended** (T05 d9): a before-model hook adds a missing required step as a tool
  call; an after-model hook validates the answer (citations resolve; a question that named a finding
  ID is not answered uncited) and jumps back to the model once, counted in one state field; a
  wrap-tool-call hook fences every result; a model-call limit guards against loops. The Port's
  existing policy is kept and extended, not replaced (T05 conditions).
- **The shortcut rule is the tool choice** (T05 d10): a call to `investigate_alert` is the decision to
  run the full plan; a narrow tool is the decision not to. The policy reads tool calls and results,
  never prose.
- **The report gate** (T05 d11): a core function, `playbook_status`, runs before the report chain,
  completes any missing code-derived step by calling the core directly with no model call, and
  appends the result. A step that cannot run is named in the report in one plain line with its
  reason, and recorded in full (step, error class, time, store) in the artifact and the app log.
- **Parallel tool calls stay on** (T05 d13).
- **Build-time option** (T05 conditions, AUD-041): a structured answer, text plus a list of citation
  labels, so the after-model hook reads a list rather than parsing brackets. Decided in the citation
  ticket.

### Security (T05 d8, project rules)

- **The fence** (T05 d8): every tool result is fenced and labelled with its source and trust level in
  one wrap-tool-call middleware, proven by one test. No datamarking or encoding.
- **The untrusted-data rule, as written** (T05 d8), added to the system prompt as the second lock:
  graph records and corpus text are data, never instructions, exactly like log fields; an
  instruction found inside them is itself evidence of an attack and is reported as such; the agent
  cites them, it does not obey them.
- **Plain text everywhere** (project rules): graph labels, document text and log values render as
  plain text only, never through a renderer that produces markup.
- **Only what the screen needs** (T05 d16): the Alerts reply gains the finding ID and nothing else.
  The evidence and graph fields carry only what the panel shows.
- **Keys and connection details only in `.env`**; `env.example` holds names (T02 conditions).
- **No injection-detector middleware** (T06 d7; AUD-042 holds its trigger).

### API contract changes (T05, T07, T08)

Made in `docs/api-contract.md` by the build ticket that first needs each one. Nothing else in the
contract moves.

1. **Alerts.** Each alert gains `finding_id` (T05 d16). The Investigate question becomes
   `Investigate finding <finding_id>: <rule title>, <first IP> against <N accounts | first user> from
   <first_seen> to <last_seen> UTC.`, still built in the frontend (T07 contract draft).
2. **Investigations: reopen.** Each turn gains `evidence`, `radii` and `unresolved` (T07), and `graph`
   on turns where a graph tool ran (T08). All projected from the saved artifacts, never from the
   model's text and never from a fresh walk. Shapes from the ticket drafts, trimmed to their
   decision-rich parts, with the IDs written in the T05 formats:

   ```json
   "evidence": [
     {"label": "G1", "kind": "graph", "id": "<membership record id>",
      "title": "membership mgarcia → IT Admins", "text": null, "score": null},
     {"label": "D1", "kind": "document", "id": "<doc-slug>@<version>#<section-path>/<ordinal>",
      "title": "MFA exception register v3, row 7", "text": "…", "score": 0.81},
     {"label": "L1", "kind": "log", "id": "rows:<timestamp>/<username>",
      "title": "2 of 42 rows", "text": "…", "score": null},
     {"label": "D2", "kind": "search", "id": null,
      "title": "Clearing documents: none above the threshold", "text": null, "score": 0.31,
      "verdict": "none"}
   ],
   "radii": {"groups": [], "assets": [], "peers": []},
   "unresolved": [],
   "graph": {
     "focus": "<person record id>",
     "nodes": [{"id": "…", "type": "person | group | asset | device | network", "label": "…",
                "sub": "…", "sensitivity": "restricted", "count": 9, "members": ["…"]}],
     "edges": [{"id": "<record id>", "source": "…", "target": "…", "type": "member of",
                "step": 1, "label": "G1 or null"}]
   }
   ```

   `kind` is `log`, `graph`, `document` or `search`. `text`, `label` and `sub` render as plain text
   only. `radii` is present only where the investigation tool ran. A folded node's `id` starts with
   `fold:` and carries `members`; this naming is Claude's design from T08, not researched. Codex's
   review of 25 October 2026 did not cover it, so it stays open for review. An edge's `label` is the citation whose resolved records contain it,
   or `null` when the walk returned it uncited.
3. **Investigations: artifact download.** `GET /api/investigations/{id}/artifact.json`, served as an
   attachment, carrying the same evidence and graph payload for the whole investigation and nothing
   from the prompt or the memory file (T07 d5).
4. **Investigations: ask.** A new stream event `step`,
   `{"call_id": "…", "step": 3, "of": 5, "name": "peers", "phase": "start" | "end" | "error"}`,
   emitted only by the investigation tool. The `tool` event's name list widens from three registered
   tools to seven; nothing else about it changes.
5. **Configuration and errors.** The log-path setting becomes a dataset setting naming a folder; new
   settings name the database connection (in `.env`), the Langfuse switch, and the re-ranker switch.
   **[author's ruling, 28 October 2026] One reading rule for every `LI_` setting,** in the app, the
   build command and the scripts: the environment first, then `.env`, then the default. `.env` is
   read with `dotenv_values`, never loaded into the process environment. The settings that predate
   the rule are brought into line by the phase 0 cleanup ticket.
   A stale database, by the staleness guard, stops the server from starting, with fixed text that
   names the build command and never echoes a path. Unlike today's startup failures, no endpoint
   answers in this state (review ruling 6).

### The screens (T07, T08)

- **Alerts**: the finding ID as the first column (T07 d7). The details panel gains no context section.
- **Investigator**: a third column on the right of the chat, folding under it on narrow screens, with
  an Evidence tab and a Graph tab, built from the Port's shell and shadcn/ui pieces (T07 d1, T08 d2).
- **Evidence tab** (T07 d1, d5): every cited record and passage for the investigation; a click on a tag
  in the answer highlights its row; a download button for the JSON.
- **The answer's hop lines and radii tiles** (T07 d2, d3): an indented list, one hop per line with its
  tag; three tiles with number, worst item and a "See list" link into the panel.
- **The step stack** (T07 d4): five steps stack while the investigation tool runs, then collapse into
  Tools used; the Port's tools keep one status line. **Build condition:** the ticket starts with a
  short research step into how Anthropic and OpenAI document streaming progress for multi-step
  agents, and records the patterns borrowed.
- **The visual hierarchy rule** (T07 d9), checked by the author's screenshot review in light and dark
  mode: (1) the verdict and the "Cleared by" line are the one coloured surface, red for threat, green
  for benign, amber for cannot tell; (2) "Not checked" and unverified citations are amber and never
  hidden; (3) radii tiles and path block are bordered boxes without colour; (4) citation tags are
  small, monospace, in the app's calm link blue; (5) prose stays plain. No new colours.
- **Graph tab** (T08 d1 to d8): the walk only; organisation nodes only, no document chunks; restricted
  assets one by one, the many folded with a count; the click rule of T08 d5 including the uncited
  case; the drawing rules of T08 d6 (layered by playbook step, shape per type, dark focus node, red R,
  relation labels, one label per fan, side-routed row-skipping edges, small arrowheads, plain clipped
  labels with hover, no step captions, a header and a legend), checked by the author's screenshot
  review in light and dark mode; an empty state line when no walk ran.
- **Drawing library** (T08 d8): React Flow plus dagre, read-only, nodes as our own components in the
  app's colour variables; dragging, connecting and deleting switched off with a test. Own SVG plus
  dagre is the fallback if the switch-off list proves heavy. Both MIT, licences recorded.
- **Not decided here, settled at build with the author's screenshot review** (map): exact colours and
  dark-mode shades, dagre spacing and node sizes, the list of switched-off behaviours.

### The eval (T06)

- **Two exams, one scorer** (T06 d8). The Port's question file stays frozen with its 90% overall and
  100% security targets. A second file for the knowledge base, with its own gates and its own lines
  in the summary, never blended. Its questions carry `type`, `gold` (chunk IDs, record IDs, path)
  and `split` (`test` or `tune`).
- **New deterministic check kinds** `retrieval`, `cites`, `verdict`, `playbook`, and one model-graded
  kind `judge`, marked so rescoring skips it. The saved answer keeps each tool's artifact, so
  retrieval rescores from the file with no model call.
- **[review ruling 2] The gold items choose the checks.** Gold chunk IDs get the two
  document-retrieval checks below; gold record IDs get the graph gate; a mixed question carries both
  and gets both. A say-no question may carry an empty gold evidence set, but states its expected
  verdict and keeps every other check that applies to it.
- **Retrieval gate** (T06 d1): every gold chunk ID among the 20 fused candidates and among the chunks
  the model received across the investigation. Either miss fails the run. The rank of the first gold
  chunk is recorded. No rate, no borrowed target.
- **Graph gate** (T06 d2): every question with gold record IDs has a walk that returns exactly the
  gold record set.
- **Answer gate** (T06 d5): every label resolves and every gold ID is cited. Say-no questions are
  graded from the artifacts first (an absent topic needs verdict `none`; a twin needs a benign
  conclusion with its clearing document cited), then the wording by pattern as the Port's checks do.
  100% on say-no, every run. Extra resolved citations are neither punished nor counted.
- **Process gates** (T06 d7): on every "is this a threat" question, `playbook_status` reports every
  required step run before the conclusion, read from state. Canaries in a log field and a corpus
  paragraph are never obeyed, flagged `security`, at 100%.
- **The phase 1 mix** (T06 d3): about 30 questions, about 10 say-no (three twins, four absent topics,
  two false-presupposition traps, one underspecified), about 12 mixed and multi-hop (at least two
  through a busy node), about 8 graph and text lookups as the control group. B3's twin question is
  asked about the laptop change directly. Every question carries a provenance line, and gold IDs or
  an expected verdict, or it is dropped. An absent-topic question carries verdict `none` and no gold
  IDs.
- **Calibration** (T06 d4): a separate tuning file of 30 to 60 query-plus-chunk pairs labelled by the
  author, scored once by the re-ranker, scores saved, threshold chosen offline. It never overlaps the
  test questions.
- **The judge** (T06 d6): a stronger model from another family through OpenRouter, binary per claim
  with fixed steps, reason before verdict, markdown stripped first, three trials with majority, about
  ten answers per run, every verdict and reason stored. Reported with its interval, never failing a
  run in phase 1. Once the author's labels exist, judge-versus-author agreement is reported as
  Cohen's kappa, computed in code. Judge prompt and model hashed into the fingerprint. The exact model is a phase 0
  build choice.
- **The retrieval layer alone** (T06 d8): a path that calls the search and the walk directly, never
  through the agent, once per build, with the integrity check as its precondition.
- **The wider fingerprint** (T06 d8): judge prompt and model, embedding and re-ranker names, chunking
  settings and corpus version; the dirty-path list gains the knowledge-base paths. API mode unchanged.
- **Switches settled by measurement** (T06 d9): the re-ranker and BM25 each run on and off over the
  retrieval layer on the same questions. A switch stays on only if it passes more questions on the
  second retrieval check, or the same number with better first-gold ranks. A tie goes to off.
  Recorded at phase 1's close, and re-run per phase and whenever the corpus changes shape.
- **[review ruling 3] A setting wins only if refusal still works.** Either setting of a switch is
  accepted only if the say-no checks pass with it, verdicts included. If the re-ranker off cannot
  give `none` where the questions need it, the re-ranker stays on and the reason is recorded. The
  verdict is computed in code, so this costs no model call.
- **Intervals** (T06 hand-offs): Wilson intervals computed in code in the summary.

### Langfuse (T06 d10, AUD-036)

- One callback handler in the agent-building function; the two question files uploaded as datasets;
  each eval run an experiment run stamped with the same fingerprint and commit as the JSON file;
  every check verdict a boolean score; the judge's verdict and reason a score with a comment.
- Off by default; one environment variable turns it on; the key is loaded only when on and never
  written to a result. The JSON file is written first; an upload failure is logged loudly and noted
  in the summary. Only human labels flow back, through an export script into a repo file. Nothing at
  runtime reads from Langfuse. A masking hook is wired from day one.
- **[review ruling 4] Proven with the switch on, too.** Deterministic tests with a fake Langfuse
  destination, at the existing doors: the JSON result is written before any upload; an upload
  failure is reported loudly in the summary and the JSON survives it; the masking hook is applied to
  what is sent; human labels return only through the export script. The live evidence is one real
  eval run visible in Langfuse, which is AUD-036's closure.
- What leaves the machine, all synthetic: question text, log fields, corpus chunks, tool arguments,
  answers. When the author's access ends around 21 January 2027, the switch goes off and nothing else
  changes.

## Testing Decisions

- **T46 migration acceptance:** T47 proves reference-only graph ingestion and independent
  integrity, complete lookup/radius/path/date equivalence and isolated read-only handoff. T48
  proves coherent source selection across application readers, paired activation/rollback,
  saved-evidence continuity, connection/cancellation/concurrency handling and native inspection.
  T49 runs the backend/frontend/type/review safety net and agreed live eval gates before the
  working application switches, measures interruption/recovery and retires obsolete paths.
  Keep frozen gold unchanged; T45/AUD-062 retrieval gaps are not waived by graph migration.
  Full commands for adopted manual tasks are tested and recorded in the admin manual.

- **T24 persistence baseline (author, 29 October 2026):** document the lookup artifact's fields
  and persistence path, separating model content from saved evidence. With a fake model and
  disposable SQLite memory, measure baseline storage and growth after 1, 10 and 50 repeated
  lookups in one conversation, including checkpoint/intermediate-write counts and stored bytes
  as well as database file size; record the method. Close and reopen memory and verify the
  original artifact without querying the knowledge base again. Run the existing report
  restart/download test to retain downloads without a model. Measurements establish a baseline,
  not a performance gate. Retention, archival, deduplication, checkpoint pruning and separate
  artifact storage remain deferred under AUD-065; no migration or evidence panel is added here.

**What makes a good test here.** A test checks behaviour through a door, never a private detail
behind it: what a function returns, what the API sends, what the screen shows. A deterministic
check is a hard pass or fail; anything the model decides is graded by the eval, never by a unit test.
Each gate gets a break-the-gate test that corrupts one input and proves the gate fails (T06).

**The six doors** (agreed with the author, 25 October 2026). A door is the place where a piece of
work proves it is done.

| # | Door | What is tested there | Prior art |
|---|---|---|---|
| 1 | The dataset generator | The world's tables, log and answer key agree; the Port's stories keep their rows; B1 and B2 trip the rules; S6 and the twins fall on days apart from S1 to S5 | The generator tests |
| 2 | **The knowledge-base door in the core** (new) | One function opens a dataset's knowledge base; every query is a named function on it: investigate a finding, look up an account, find peers, search the corpus, project the walk. Tested here: independent graph integrity and corruption checks, including valid-but-swapped endpoints and changed attributes; unmentioned chunk references; reference IDs/mentions matching PostgreSQL without text duplication; exact S6 gold records/paths and dated peers; unchanged fusion/filter/verdict/cap contracts; PostgreSQL reader write refusal and Neo4j serving write refusal; matching build identities, source snapshots and stale/incomplete-pair refusal; native inspection query results matching the same core neighbourhood. T46 replaces GEXF-specific checks after native inspection acceptance | The core tests for rules, search and stats |
| 3 | The agent with a fake model | The fence on every tool result; the before-model hook adding a missing step; the after-model hook sending the model back once on an unresolved label; the model-call limit; `playbook_status` completing a step and naming one that cannot run; the artifact surviving the SQLite round trip; with Langfuse switched on against a fake destination, the callback handler sending traces with the masking hook applied | The agent and investigation-policy tests with their fake model |
| 4 | The API through the test client | `finding_id` on alerts; `evidence`, `radii`, `unresolved` and `graph` on reopen, projected from the artifact; the artifact download carrying nothing beyond its fields; `step` events only from the investigation tool; the widened `tool` names; the server refusing to start on a stale database, with fixed text | The investigations and startup API tests |
| 5 | The screens with a fake API | The finding ID column; the Investigate question carrying the ID; the evidence panel and its highlight; plain-text rendering of every data field; the step stack and its collapse; the Graph tab's click rule, empty state and read-only switch-off test | The Investigator and Alerts page tests with the fake API, and the repository-rules test |
| 6 | The eval runner | Everything the model decides: the knowledge-base question file with its gates, the Port file unchanged, the retrieval layer alone, the judge as a smoke alarm, the on-versus-off comparisons with the refusal condition. Deterministic runner tests here: which checks each question's gold items select; the kappa calculation; with Langfuse on against a fake destination, the JSON written before upload, an upload failure reported with the JSON intact, and labels returning only through the export script | The scoring, results and question-file tests; the eval runner itself |

- **[spec ruling] Door 2 uses a fake embedder and a fake re-ranker,** handed in at the door the way
  the agent tests hand in a fake model, so the test suite stays key-free and offline. It still needs
  the real PostgreSQL and, for graph integration, isolated Neo4j resources built fresh and
  failing loudly if prerequisites are missing. Only the eval's retrieval layer
  and the one-string embedder check call OpenRouter (T03 conditions).
- **Doors 1 to 5 are code, gated by tests and the build loop's two-axis code review**
  (standards and spec, findings triaged; Matt Pocock's skill, `mp-code-review` in both Claude Code
  and Codex). **[author's ruling, 25 October 2026]** Whichever agent builds a ticket
  runs this review itself; no review by the other agent is required. Door 6 is the agent's
  judgement, gated by the eval set (the author's verification rule). A change to the agent's
  behaviour is accepted only on an eval run (project rules).
- **The safety net**: the backend tests, the frontend tests and the Port's eval pass after every
  change. The core-boundary test keeps the core free of FastAPI and frontend imports, now including
  the knowledge-base modules. The no-real-keys test covers the new settings.
- **Types**: every new Python file is clean under the type checker and never joins its ignore list.
- **The author's looks**, recorded as dated lines on their build tickets, never as screenshots: the
  live screen on S6, one twin and one answer with no walk, with every drawn edge matching a hop line
  or a "walked, not cited" line (T07, T08 phase 1 acceptance); native Browser inspection of the
  organisation and finding neighbourhood (T46 replaces the future Gephi requirement);
  one real eval run seen in Langfuse (AUD-036).

## Out of Scope

- Phases 2 (incident history), 3 (travel and network facts, account type), 4 (attack paths and risk
  score) and the GRC view. Planned features with their own specs later (map scope ruling).
- Any change to the four detection rules' logic (T05 d15), to the Port's behaviour beyond what this
  spec names, or to v1. A fifth rule for new devices was considered for B3 and not taken.
- Document chunks drawn on the graph; expansion on demand; a graph route of its own (T08).
- A Gephi download endpoint; GraphML (T08 d9).
- The judge's reason on the screen (T07 d8; AUD-043).
- A per-question must-not-cite set and citation precision (T06 d5).
- Injection-detector middleware (AUD-042); the parent-graph seam and a knowledge-base sub-agent
  (AUD-040).
- Moving agent memory to PostgreSQL (AUD-032); incremental sync (AUD-033); Cohere Rerank 5 (AUD-035).
- A file watcher that rebuilds the database on its own; the build stays one explicit command.
- More attack stories, more twins, more row signals and a longer baseline (AUD-037 to AUD-039).
- Replacing gpt-4o-mini (AUD-031), which keeps its own deadline.
- The bootcamp's deliverables.

## Further Notes

**Build order handed off by the tickets** (T04, T05, T06, T07, T08 hand-offs). `to-tickets` cuts
it into tracer-bullet tickets; the order is the dependency floor, not the ticket list.

| # | Item | Phase |
|---|---|---|
| 1 | pgvector on the Intel Mac; the database fixture failing loudly | 0 |
| 2 | Regeneration: generator, tables, log with two new columns, S6, twins, `truth.json`, the `default` dataset folder, the loader and setting change; the Port's tests and eval pass on it | 0 |
| 3 | The finding ID in the core; the Port's tests and eval pass | 0 |
| 4 | The ATT&CK fetch script and pinned version | 0 |
| 5 | The Codex brief and the consistency script, then the corpus delivery | 0 |
| 6 | Ingestion: chunking, embeddings, the link table, the build and read-only roles, the build command and the staleness guard | 0 |
| 7 | The graph build (no `used address` edges since 1 November 2026), and its integrity check; native Neo4j inspection and the author's walkthrough after T46; T20's GEXF delivery remains historical | 0 |
| 8 | The first knowledge-base questions with their gold IDs or expected verdicts, written before retrieval first runs (map, evaluation stance) | 0 |
| 9 | Hybrid retrieval with fusion, filters, the re-ranker switch and the three verdicts | 0 |
| 10 | The playbook list, the four new tools with content plus artifact, the artifact round trip | 0 |
| 11 | The three hooks, the fence, `playbook_status` and the report gate | 0 |
| 12 | The eval: new check kinds, the knowledge-base question file wired into the runner, the retrieval layer alone, the wider fingerprint, the judge and its kappa report, intervals; first questions passing end to end | 0 |
| 13 | Langfuse behind its switch, tested with the switch off and with it on against a fake destination; one real eval run seen in Langfuse | 0 |
| 14 | The API additions: `finding_id` on Alerts, evidence, radii, graph, artifact download, step events | 1 |
| 15 | The screens: finding ID column, evidence panel, step stack (after its research step), Graph tab | 1 |
| 16 | The tuning file and calibration; the `none` rule switched on | 1 |
| 17 | The full phase 1 question set; the on-versus-off comparisons with the refusal condition; the author's acceptance of the live screen | 1 |

**[spec ruling] The phase split.** Phase 0 builds everything behind the screen and proves it with
tests and the eval on a first handful of questions. Phase 1 adds the API additions, the screens,
calibration and the full question set, because phase 1's gate is the author's look at the live
screen. **[review ruling 5]** The Alerts `finding_id` field is one of those API additions; the
core's finding ID it carries is built in phase 0.

**New terms for the glossary** (for `domain-modeling`, not added by this spec): knowledge base,
playbook, investigation package, artifact, blast radius, peer, benign twin, verdict (`none`, `weak`,
`found`), citation label, evidence panel, absent topic, canary, build, staleness guard, dataset,
integrity check.

**Risks worth naming.** gpt-4o-mini retires on 14 January 2027 (AUD-031); a long phase 1 may cross
that date and force a model change mid-initiative, gated by both eval files. The author's Langfuse
access ends around 21 January 2027. The cost table in research note 05 rests on estimates; the first
real trace replaces it. The rebuild time and cost are guesses until the first real build measures
them.

### Decisions log

| Date | Decision | Reason |
|---|---|---|
| 2026-10-25 | Spec written from the map and tickets 02 to 08 | The decision tickets were complete; the map's frontier was the spec |
| 2026-10-25 | Six test doors, one new: the knowledge-base door in the core | Author's ruling: retrieval and the walk are plain code, checked exactly and cheaply at one door that covers the tools, the API, the eval and the export |
| 2026-10-25 | Author's ruling: B2 makes at least 20 failures within an hour, then succeeds | T04 d8's eight failures trip no rule; its own condition says a twin must trip the rules, and the rules may not change (T05 d15) |
| 2026-10-25 | Author's ruling: B3 is tested by asking the agent about the laptop change directly | No rule reads `device_id`, so B3 can never appear as an alert; a fifth rule was not taken |
| 2026-10-25 | Author's ruling: the regenerated world is the dataset folder `default`; the setting names a folder; the old log file is retired | Resolves T04 d13's "current path kept as the `default` dataset"; two near-copies of one log could drift |
| 2026-10-25 | Author's ruling: the Port's ground-truth file stays beside `truth.json` | The Port's scorer reads it and the Port exam stays frozen (T06 d8); one generator writes both |
| 2026-10-25 | Author's ruling: door 2's tests use a fake embedder and re-ranker | Keeps the suite key-free, offline and free; the eval's retrieval layer uses the real services |
| 2026-10-25 | Author's ruling: API additions and screens in phase 1, everything else in phase 0 | Phase 1's gate is the live screen |
| 2026-10-25 | Author's ruling: the ID formats of T05 d5 win over the placeholder examples in T07 and T08 | IDs made from content survive rebuilds; counters shift when a finding is added |
| 2026-10-25 | Author's ruling: the running app's database is built once by an explicit command and stays; a staleness guard refuses to start on a database built from older files | Raised by the author's question on what "every run" means; without the guard, changed files and an old database would give confident answers from an old world |
| 2026-10-25 | Codex reviewed the spec (`reviews/spec-review-2026-10-25-codex.md`); Claude triaged it in a fresh session (`reviews/spec-review-2026-10-25-triage.md`): 13 findings agreed, one new finding (N1) added | The spec's author should not judge findings on its own spec alone |
| 2026-10-25 | Review ruling 1: the integrity check compares identities, not only counts; `used address` edges come from the log and are checked against it; a chunk may have no `mentions` edge; no isolated person, group, asset or device | A count is necessary but not sufficient, as reconciliation practice says; the log is already the truth for who signed in from where; the old allowed list protected nobody, since every user has a laptop |
| 2026-10-25 | Review ruling 2: the gold items choose the checks; a say-no question may carry no gold IDs but states its expected verdict | Graph records are never document candidates, and absent topics have no gold document; the rules as written failed or dropped valid questions |
| 2026-10-25 | Review ruling 3: a retrieval setting wins only if the say-no checks pass with it; T06 d9's re-score and re-run clauses restored | With the re-ranker off, the empty-result rule never fires on a non-empty corpus, so a tie going to off would remove the refusal path |
| 2026-10-25 | Review ruling 4: Langfuse proven with the switch on, against a fake destination, plus one real eval run seen in Langfuse | Switched-off tests cannot prove the promises made about it; AUD-036 closes on a visible run |
| 2026-10-25 | Review ruling 5: the Alerts `finding_id` field ships in phase 1; the core's finding ID stays in phase 0 | Aligns the build table with the phase-split ruling; nothing in phase 0 reads the field |
| 2026-10-25 | Review ruling 6: a stale database stops the server from starting; the comparison with today's invalid-log behaviour removed | Keeps the staleness-guard ruling; today's invalid log starts the server with endpoint errors, which is not what the ruling says |
| 2026-10-25 | Correction: the reason for keeping the Port's ground-truth file is that the scorer reads S5's planted text from it; pattern names come from the question file. The ruling is unchanged | Codex's finding R10, verified at `backend/evals/scoring.py:44` and `:144` |
| 2026-10-25 | Author's ruling at the ticket cut: the test that recomputes S6's radius from the tables moves from door 1 (the generator) to door 2 (the knowledge-base door), in build ticket 19 | The radius function belongs to the graph, which first exists in ticket 19; a second, table-only calculation in the generator ticket could drift from the tool's |
| 2026-10-25 | Author's ruling at the ticket cut: every phase 1 build ticket waits for ticket 29, phase 0's gate | The map proves each phase before the next is built; a screen built on unproven retrieval may need rework |
| 2026-10-25 | Build tickets 09 to 42 cut from this spec with `mp-to-tickets`; the author kept the 34-ticket granularity | Each ticket fits one fresh session |
| 2026-10-25 | Fixes from the review with no ruling needed: twins' scheduling restored (R8), kappa report restored (R7), first questions before retrieval in the build order (R5), "saved" removed from the reputation sentence (R12), Investigation used for the saved object and Dataset moved to the new terms (R13) | Each restores what the source tickets, the map, the code or the glossary already say |
| 2026-10-25 | Author's ruling at ticket 09: build tickets close on the safety net, a clean type checker and the build loop's two-axis code review (`mp-code-review`) with its findings triaged. Codex's review is removed from the standing criteria of tickets 09 to 41, from the Testing Decisions and from the reviewer's user stories | Claude wrote "independent review by Codex" into this spec from the author's global defaults without a ruling; the author ruled that default does not apply to this project |
| 2026-10-25 | Author's ruling: Matt Pocock's skills go back to their original names in Claude Code (`implement`, `tdd`, `to-tickets` and the rest), matching Codex's copies; only Claude Code's review keeps `mp-code-review`. Live references in this spec and tickets 09 to 41 name the review for both builders; dated history keeps the names used at the time | Codex builds some tickets too, so a closing condition must name a skill both builders have; Claude Code ships a built-in `code-review`, so that one name would clash |
| 2026-10-25 | Author's ruling: Codex's copy of the review skill is renamed `code-review` to `mp-code-review` too, with its two callers (`implement`, `tdd`) updated, so both builders share every name. Tickets 09 to 41 name the review once, `mp-code-review` | One name per skill for both builders, with no exception to remember |
| 2026-10-25 | Author's ruling: our table access uses SQLAlchemy Core on the psycopg driver, sharing one engine and pool with LangChain's store; no ORM; server-level tasks stay on psycopg | No ticket had decided the access layer. LangChain's `PGEngine` is an SQLAlchemy engine (LangChain's PGVectorStore docs), so one engine serves both; tables in code fit the fresh build; migrations, ORM objects and database portability bring nothing here |
| 2026-10-26 | Author's ruling before ticket 11: `device_id` is empty on attacker rows and on a small seeded share (about 3 to 5%) of ordinary employee rows; twins B2 and B3 keep their laptops. Ticket 11's agreement test checks only filled-in device IDs | Raised by the author: T04 d4 said every row carries a device and T11's test said each belongs to the row's user, which would put the victim's laptop on attacker rows. Real sign-in logs (Microsoft Entra ID) leave the device ID empty for unregistered machines, and employees on personal or public devices look the same, so empty must not become a perfect attack marker |
| 2026-10-26 | Author's ruling at ticket 11: the sign-ins that come through the VPN pool are new log rows added in ticket 12, with S6 and the twins. Ticket 11 writes the four pool addresses into the networks table in their hand-out order | The Port's rows cannot change their addresses, so VPN sign-ins are new rows that change whole-log counts; ticket 12 already owns count changes, so every count moves once, in one ticket |
| 2026-10-26 | Author's ruling at ticket 11, amending the device ruling above: the empty employee rows are exactly the phone sign-ins (124 rows, 7.7%), with no further random share | Measured at the build: the register holds no phones, and the Port's user-agent text cannot change, so a laptop ID on an iPhone row would be wrong; every empty value then has a visible reason in its own row. Adding company phones to the register was not taken. Consequence noted on tickets 19 and 25: an empty device ID is not a device, so it makes no device edge and two empty rows are never peers by device |
| 2026-10-26 | Author's ruling at ticket 11's review: each privileged group has one member from outside its home department. IT Admins take one from Engineering; Finance Approvers one from Operations and HR Data Owners one from Finance, chosen by Claude for fit | T04 d2 calls the groups cross-cutting; drawn from one department only they were sub-departments. Raised by the spec review |
| 2026-10-26 | Author chose S4 option 2: keep MFA passed and explain an unexpected prompt approved by Olivia, supported by one additional incident record. Own corpus grows from 27 to 28 documents; T12 reserves its ID, T15 defines its evidence and T16 delivers it | A passed authentication step does not establish the account owner's intent. Separate log observations, user statement and responder assessment; leave credential acquisition unknown. No application code or dataset changed in this decision session |
| 2026-10-26 | Author deferred the expanded S4 authentication-attack story as premature for this phase. Supersedes the option-2 implementation requirement above: no additional incident document, no new email, web or SIEM evidence requirement; own corpus restored to 27. S4 authentication explanation remains open and existing dataset unchanged | The proposed explanation requires evidence beyond the current login dataset. Olivia's unsolicited statement was rejected as too convenient; no replacement mechanism has been agreed |
| 2026-10-26 | Author agreed S4 is an intentionally unresolved suspicious sign-in. Keep the event and MFA pass; no exception, added incident record or telemetry source. T12 records the known facts and unknowns in the KB answer key; KB evaluation accepts uncertainty without demanding compromise or a mechanism | Supersedes the earlier open S4 question. A source address does not establish physical location, and authentication success does not establish authorisation. No dataset or application code changed |
| 2026-10-26 | Author's ruling at ticket 43: T05 d1's "the Port's three tools unchanged" gains one exception. `find_suspicious_activity` adds one agent-only field per finding with what the finding's address did overall (successes, failures, the accounts it signed in to). `Finding`, `Finding.to_dict()` and the Alerts reply stay unchanged | Each rule builds its finding from its own rows only, so a spraying finding's `success_count` is always 0; the agent read S6 as a spray that got nowhere, though it signed in to amelia.ward three times (AUD-047). A prompt line alone was judged unreliable; changing the core finding would break ticket 32's "`finding_id` and nothing else" |
| 2026-10-26 | Author's ruling at ticket 43: the frozen Port question file (T06 d8) changes in place for Q02 and Q04 only. Each gains checks for S6 (Q02: names `45.148.10.80` and amelia.ward, states three successes; Q04: names amelia.ward, looks up `45.148.10.80`); no check is removed. T04 d17's exception is read as covering expected facts, not only counts | S6 made Q02's "no attempt succeeded" half false and left Q04 blind to the one account the grown world compromises: in T13 no Q04 answer named amelia.ward, and the eval could not see it. Duplicate S6 questions would leave the stale check in place |
| 2026-10-26 | Author's ruling at ticket 43, amending the row above for Q04: the check is "flags amelia.ward as possibly compromised (S6)". It passes hedged wording and fails an answer that never raises compromise about her | An agent raises a concern with its evidence; the verdict is the analyst's (as for S4). Merely naming her let T13 run 1 pass while listing her only as a new-country sign-in |
| 2026-10-26 | Author's ruling 8 at ticket 43, amending ruling 4's row: the agent's view of each finding also drops the rule's own `success_count` and `failure_count` (`event_count` stays); the system prompt gains one line to flag an account a spraying or brute-force address signed in to as possibly compromised; Q02's account check must tie amelia.ward to a success | T43's eval (`2026-10-26-173622-f853f368`): with the true count beside the finding's `success_count: 0`, the model repeated the zero and twice wrote "all failures". Q02's account check passed on the list of targeted accounts |
| 2026-10-26 | Author's ruling 9 at ticket 43: in the agent's view, a brute-force or spraying finding whose address signed in during the window gets one sentence on its summary, built in code from `address_activity`, naming the success count and accounts. `Finding.summary` and the Alerts reply stay unchanged. One paid run; if Q02 still misses 2/3, T43 closes with the Q04 fix and AUD-047 waits for phase 1's investigation tool | T43's second run (`2026-10-26-180147-6900ff93`): the code-enforced lookups worked at once, while prose instructions left Q02 at 0/3, once with a wrong count of 1. The model copies the summary sentence, so the true sentence is built in code |
| 2026-10-26 | Author chose responsible teams as internal document owners, separate from login accounts. T15 records and validates allowed owner teams; body mentions still resolve against the organisation tables, with the one leaver allowed. ATT&CK pages keep external-publisher labels `owner: mitre`, `department: external`. Supersedes T04 d12's owner-as-username rule and d16's owner-against-people check; asset ownership unchanged | The document responsibility label need not identify anyone who signed in during the captured week. The author explicitly approved team ownership after T14's review exposed the unnecessary coupling |
| 2026-10-27 | Author's rulings at ticket 16 on chunk sizes and ATT&CK cleaning (P1 to P4c): five unplanned own kinds take the policy row; runbook steps stay whole under a test; ATT&CK references, citation markers, link addresses and `<code>` tags stay out of chunk text with the files unchanged; procedure examples packed per field group. See "Chunking rulings at T16" | T16's token measurement: no own section outside runbooks exceeds 244 tokens; three runbook step sections exceed 350; ATT&CK reference lists reach 17,282 of T1078's 26,414 tokens; 185 one-sentence procedure examples would each become a chunk that can outrank the explanation. Search indexes what explains; what proves is kept in the files |
| 2026-10-28 | Author's rulings at ticket 18 on the staleness guard: with no build published, the server starts without a knowledge base and logs fixed text naming the build command; a build that cannot be checked (PostgreSQL down, database, fingerprint or reader login missing) stops the server; the fingerprint skips hidden entries; `LI_KNOWLEDGE_BASE_STATE` names the pointer file for app and build; the "cannot be checked" text names both the reader's login and the rebuild. See T18's Answer, decisions 1 to 5 | Absence gives no answers, so it cannot mislead, and today's tests stay free of PostgreSQL; a guard that cannot check must not let things through; hidden entries are tooling state, found in `default/` during T18; tests and eval servers must never meet the real build; PostgreSQL gives no error code that separates a refused login from a missing database |
| 2026-10-28 | Author's ruling after T18 (AUD-059): every `LI_` setting is read from the environment first, then `.env`, then the default, in the app, the build command and the scripts. Supersedes T18 decision 4's "environment only" for `LI_KNOWLEDGE_BASE_STATE`. Existing settings are aligned by the phase 0 cleanup ticket; new settings follow the rule from T19 on | Three reading habits existed (PostgreSQL settings, the build's dataset folder, the app's paths), and T18's fingerprint turned the dataset-folder split into a refusal to start. The PostgreSQL settings already follow this rule; the author changes settings in `.env`; the environment winning keeps tests and eval runs isolated. The rule is fixed before more settings arrive (re-ranker switch in T23), so the cleanup does not undo later work |
| 2026-10-28 | Author agreed the VPN pool represents session-assigned addresses reused over time, following the existing remote-access policy; public-exit interpretation rejected. T19 reviews the value and wording of the ten S6 matches before choosing a time window | Address reuse alone establishes neither shared-device use nor exposure or spread. No removal of matches, dataset change or additional telemetry approved; see T19 Answer decision 2 and AUD-060 |
| 2026-10-28 | Author agreed to retain S6 VPN address-reuse matches as clearly labelled supporting context outside exposed-account counts. T19 aligns results, answer key and tests; later agent/screen presentation keeps the distinction | Ten later sign-ins from different recorded laptops establish address reuse, not exposure or spread. Match identities stay; time window remains undecided. Qualifies earlier network-peer blast-radius wording; see T19 decision 3 |
| 2026-10-28 | Author approved optional start/end dates for find_peers and investigate_alert, passed to the shared graph calculation. User dates take precedence; omitted bounds use available log records. Results state period and coverage; permissions remain a snapshot | Reuses existing log-tool date conventions and supports user-directed investigations instead of a fixed week. Supersedes earlier fixed-week wording for login-based relationships; S6 default-period expectations retained. See T19 decision 4 and T25/T26 criteria |
| 2026-10-28 | Author chose all shared organisation addresses grouped by address, retaining S6's ten VPN matches and adding 43 office matches to context and the answer key | The independent graph walk exposed that the old key omitted ordinary office sharing. Neither group establishes exposure or spread, and overlapping groups are not additive people. T19 decision 5; B-092 |
| 2026-10-28 | Author approved preparing and integrity-checking the graph once per backend process at startup, then reusing it across agent questions. T24 owns lifecycle integration, cleanup, tests and startup timing; a rebuilt dataset is adopted on restart | Avoids first-question preparation delay while preserving verification before use. Existing no-build behaviour remains; no automatic hot replacement or per-conversation database connection. T19 core unchanged |
| 2026-10-29 | Author's rulings at T21: a twin question states its expected outcome as `conclusion: "benign"`, beside `type`, `gold`, `split` and the provenance line; `verdict` stays the search tool's `none`, `weak` or `found`. K04, the first S6 mixed question, carries two of S6's three expected documents; the next-steps runbook waits for a phase 1 question that asks what to do next | The search tool's verdict is computed in code and the twin's conclusion is the investigator's judgement, so one name for both would blur the two layers. The answer gate demands every gold ID be cited, so gold beyond what a question asks would grade the agent on evidence it was not asked for |
| 2026-10-29 | Author's T22 ruling: until calibration, corpus search returns `weak` with `not_calibrated`, keeping the `none` rule disabled | The first retrieval implementation must not invent a relevance threshold or imply measured confidence. Scores remain available for T39 calibration |
| 2026-10-29 | Author's T23 ruling, qualifying the T22 row: a search that returns zero passages gives `none` with reason `empty_result`, with the re-ranker on or off. Any non-empty result stays `weak` / `not_calibrated` until T39; the threshold-based `none` rule stays disabled | Zero passages is a counted fact, not a relevance judgement, so it needs no threshold. Only a filter can empty a result, since exact vector search always returns candidates; K05 and K06 are unaffected |
| 2026-10-29 | Author approved four T24 persistence checks: document artifact contents/storage path, measure storage at baseline and after 1/10/50 repeated lookups, verify original evidence after close/reopen without querying the source, and retain report downloads without a model | Establish correctness and a measured storage baseline before adding more tools. No new performance threshold or storage architecture; broader scaling decisions deferred under AUD-065 |
| 2026-10-29 | Author approved minimal T24 browser compatibility: accept lookup_account progress, use the existing status line, and label its saved tool result | The old stream parser rejects unknown tool names. Move this one name forward from T36 so the lookup works end to end; remaining names, step stack and evidence panel stay in their later tickets |
| 2026-10-30 | Author accepted Community's retained administrative access as a development-stage limitation so T46 may continue. Prove graph-data write prevention and build isolation; review permissions, recovery, availability, monitoring and cost before production use, including a possible Enterprise upgrade. No Neo4j selection or application migration approved | Distinguish current development from the future shared analyst service. Official documentation provides an edition-upgrade path, but an upgrade alone does not configure or prove production safeguards. PostgreSQL reader separation and fixed read-only agent tools remain unchanged |
| 2026-10-30 | Subsequent T46 ruling: select Neo4j Community for graph queries and PostgreSQL/pgvector for passage content/search, with stable passage references in Neo4j. Prepare verified matching pairs from immutable source snapshots; adopt by restart and retain the previous complete version for rollback. Replace Gephi export with tested native Browser inspection and the author's walkthrough; preserve the in-app Graph tab and saved evidence. Approve consolidated build tickets 47–49 and their dependency chain; application coding starts separately | Author approved the design and three-ticket proposal after reviewing the security tradeoff, proof results, ownership split, rollback lifecycle and native-visualisation documentation. Supersedes T02's one-store/NetworkX choice and T08/T20's future GEXF requirement, while retaining their history. Proof establishes feasibility, not final reference-only ingestion, integrated downtime or production readiness; those remain explicit acceptance work |
| 2026-11-01 | T25 gate: author ruled that sharing an address answers no investigation question in this app, added no allocation evidence (AUD-073, possible phase 3 feature), and removed address-sharing context everywhere: the network form of `find_peers`, the radius context, the answer key, tests and spec. T50 performs the removal and blocks T25 and T26 | Research note 25: first-party sources use the address pivot only from an attacker's address, which `search_logins` and the spray finding already cover; vendors suppress company office and VPN addresses; a pool address names one person only with an allocation record the log lacks. A ruled-useless output should not reach the model (T43). Reverses the 2026-10-28 rows retaining the ten VPN matches and adding the 43 office matches (T19 d3, d5); keeps the VPN address meaning and relationship-date rows |
| 2026-11-01 | T50 pre-build ruling: keep network nodes, drop `used address` edges. The build draws no such edges; the integrity check asserts none exist; network nodes stay as organisation facts with their `mentions` links | After the T25 removal nothing reads the edges; the radius was their only reader. Keep facts about the world, remove derived links nobody reads. The graph is rebuilt from source and the log keeps every sign-in, so a later phase can redraw the edges with the allocation records it would need anyway (AUD-073). Supersedes review ruling 1's edge rule and the 2026-10-25 row's edge clause; T08 d6's Graph tab loses address edges |
| 2026-11-01 | Author approved T52 as the next decision ticket to review phase 0 and 1 agent objectives and reliability evidence, blocking T45 and T26. T25, T27 and T51 remain independently available | Confirm objective coverage and assess bounded Sentinel-inspired proposals before retrieval/package decisions. No capability, scope or evaluation-policy change is approved by opening the review; approved outcomes flow to downstream build and evaluation tickets |
| 2026-11-01 | Author revised the immediate order to T51, then T52, before T45 and T26 | Finish the approved answer-key cleanup and verified pair activation before the objectives/reliability review. Priority only; existing dependencies and scope remain unchanged |
