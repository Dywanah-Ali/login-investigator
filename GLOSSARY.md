# Login Investigator v2

The Login Investigator analyses a synthetic authentication log and investigates it with an AI agent.
v2 moves the v1 application into a new shell without changing what it does.

## Language

**Port**:
The whole effort of moving v1 into the v2 shell.
_Avoid_: Migration, rewrite

**Parity**:
v2 gives the same results as v1 for the same input, proven by the Port's acceptance gate.
_Avoid_: Same behaviour, behaves like v1

**Investigation**:
One line of inquiry by the analyst: their questions, the agent's answers and tool calls, and any
incident report, kept under one ID so it can be reopened. v1 shows it on screen as a "case".
_Avoid_: Conversation, thread, chat, session

**Finding**:
One suspicious pattern a detection rule caught in the log, with its IPs, users, counts, time window
and evidence rows. The core and the agent call it a finding; the screens and the API call the same
thing an **Alert**, as v1's screen did. The two words never name different things.
_Avoid_: Incident, detection, event

**Rule severity**:
A **Finding**'s default review priority, Low, Medium or High, fixed per detection rule by one core
policy (ticket 26). It says how urgently to review the pattern, not whether an account was taken
over. It differs from an **Investigation**'s report severity, which weighs all the evidence and can
rate the case higher or lower; the Alerts screen says so beside the badge.
_Avoid_: Risk score, confidence, incident severity
