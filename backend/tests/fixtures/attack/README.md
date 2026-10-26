# MITRE ATT&CK test sample

`enterprise-attack-20.0-sample.json` is a 59-object subset of Enterprise ATT&CK 20.0,
from MITRE's `attack-stix-data` commit `20664a889568dce884a1dac0ec7b12ae3a199f51`.
The adjacent `LICENSE.txt` is copied unchanged from that commit.

The sample retains the thirteen selected techniques and mitigations, their mitigation links,
one Password Spraying procedure example and its actor, one detection strategy and its eight
analytics, and the release collection metadata. The collection's full-bundle contents list
is omitted. All retained descriptions and references are MITRE's source text.

Tests read this file locally. They never download the full bundle or call an external model.
