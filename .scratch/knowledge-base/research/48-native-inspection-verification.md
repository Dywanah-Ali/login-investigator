# T48 native inspection runtime evidence

30 October 2026. Separate offline pair; no application selection change or provider call.

## Identity and scope

- Build: `05f15cfcb66b48aaa7e2c5cfddd116c3`.
- Source fingerprint: `e928c8dc54a9747896a58215fb06886664a601a3ea0c8de690af6ed3515f3afa`.
- PostgreSQL: `li_kb_b4be6e8097c8`.
- Neo4j Community 2026.10.1; Python driver 6.1.0.
- Bundled Browser reports `neo4j-browser-2026.10.21+0`.
- Serving user `li_serving`; server write protection checked through `open_version`.
- Browser HTTP and Bolt bound to 127.0.0.1 only. Community administrative limitation remains AUD-068.
- Offline vectors establish graph evidence only, not live retrieval quality.

## What was verified

A fresh Playwright Chromium context authenticated using the build's private `.env` without
printing credentials or recording login traces. Browser itself showed:

| View/check | Result |
| --- | --- |
| Organisation query | 170 nodes, 326 relationships |
| S6 `F-password-spraying-d06a7545` | 55 nodes, 64 relationships: 7 grants, 2 memberships, 55 address-use edges |
| S6 table | Correct build/fingerprint, node_count 55, relationship_count 64, complete TRUE |
| Read mode | Browser's post-connect command selected read; Settings confirmed |
| Automatically connect result nodes | Off in fresh context; explicitly checked off for exact-view comparison |
| Visualization node limit 10 | Canvas showed 10 nodes / 7 relationships and “Initial display limit hit at 10 nodes. Edit settings.” |
| Table with truncated canvas | Still 55 nodes / 64 relationships / complete TRUE |
| Visualization limit restored to 1000 | Full 55/64 canvas restored |
| Record limit 1 | One-row saved query still showed full 55/64 graph |
| Styling | Imported explicit Entity style: blue, size 45, stable-ID captions; grants red, device-use green, address-use purple |
| Captions | Stable IDs visible when zoomed in; whole-view zoom can hide captions |

The organisation view excludes passage references, not organisation relationships. Passage nodes
remain reference-only. Browser does not join text from PostgreSQL. Shared-address context is
visually present but is not an exposure count or evidence of overlapping sessions.

## Runtime corrections retained

- B-119: missing local pinned image restored before testing.
- B-120: default data has no finding with device peers; the integration fixture now plants one
  in its own source copy and verifies directed identities independently.
- B-121: manual command path corrected for `uv --directory backend`.
- B-122: `:config` unavailable in this bundled UI. Use Settings. GraSS import requires confirming
  its preview; only explicit label/type rules are retained, so unused generic defaults were removed.
- B-123: `:params` evaluates Cypher, so generated keys must be identifiers rather than JSON keys.
  Values remain escaped; the actual generated expression is included in the regression test.

## Acceptance boundary

The author subsequently completed the live organisation and S6 walkthrough, confirmed settings,
and supplied screenshots of the matching identity, organisation counts and S6 table (55/64,
complete TRUE). The author explicitly accepted Browser as the replacement and instructed Gephi
retirement. The command, writer, public export method and format-specific tests are now removed.
Historical T20 evidence remains. Post-retirement checks passed and T48 is resolved.
The working application's selection pointer retains SHA-256
`09412e45a833a4a780144c7342506e3f480527b8855b410e88ac9889c4c2d993`.
The isolated pair is retained for the live walkthrough. Ports may change on restart; regenerate
inspection output after a restart rather than treating recorded addresses as permanent.

## Verification results

- Initial focused native inspection plus retained Gephi regression run: 11 passed in 265.43 s.
- Final native suite, including real Cypher evaluation of generated parameter maps: 2 passed
  in 238.66 s. The fixture includes a deliberately planted device peer in disposable data.
- Frontend: 150 passed in 44.53 s. Both type checks pass. Lint exits successfully with the
  same six existing AUD-009 warnings.
- Browser's Save and open in tab retained the finding query in the Queries sidebar after reload.
- Full backend: 710 passed cleanly in 1439.60 s (23:59). Collection preceded the final
  parameter-syntax test addition; both final native tests passed separately as above. No live
  paid agent evaluation: prompts, tool contracts and answer behaviour are unchanged. T49
  retains the migration evaluation gates.

The final bundle is `backend/.graph-versions/05f15cfcb66b48aaa7e2c5cfddd116c3/walkthrough/`.
Both organisation and finding queries were saved through Save and open in tab. The manual's
passage-reference table query streamed 320 records. The headless verification context was closed;
its saved queries do not populate the author's separate browser profile. The files remain the
repeatable source for loading that profile.

Final retirement verification: 53 knowledge-base, graph and native-inspection tests passed in
160.11 seconds; Pyright clean. Both retirement review axes are clear. The earlier 710-test full
run preceded retirement; the 53-test run verifies the affected code after removal. Frontend
source is unchanged and its 150-test/type/lint evidence remains as recorded above.
