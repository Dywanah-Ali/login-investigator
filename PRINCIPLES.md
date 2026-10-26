# Principles

Core design points for this repository. They hold across tickets and initiatives, and they
outrank convenience. `CLAUDE.md` and `AGENTS.md` point here; both Claude and Codex read this
file before designing or changing agent behaviour, tools or eval checks.

How this file works:

- Each principle has a stable ID. IDs are never reused or renumbered.
- A principle is added or changed only by the author's ruling, recorded with its date and
  source.
- A principle that no longer holds is marked superseded, with the ruling that replaced it.
  It is never deleted.
- Details belong in tickets, the spec and the logs. This file holds the rule, the reason,
  how to apply it, and where it came from.

## P-01: Code owns the facts, the model owns the judgement, the analyst owns the verdict

**Rule.** Code counts, combines and states what is true. When a fact needs numbers from more
than one place, code combines them and hands the model a finished, true sentence, placed where
the model already reads. The model weighs those facts, adds context and explains what they
mean. The analyst decides.

**Why.** In knowledge-base ticket 43, gpt-4o-mini kept writing that a password spray "all
failed", although a field beside the finding showed 3 successful sign-ins. Hiding the
misleading count and adding a prompt instruction did not fix it. The question passed 3/3 only
when code wrote "45.148.10.80 also signed in successfully 3 times, to amelia.ward." into the
summary the model copies. Lookups enforced in code worked at once; prose instructions only
nudged. Code must not take over the meaning, though: if code decided what facts mean, the model
would have no job. A weaker model moves the line toward code for facts. It never moves
judgement into code.

**How to apply.**
- An answer is wrong because the model failed to find or combine a fact: compute the fact in
  code and state it where the model reads.
- An answer is wrong for lack of context: give the model the missing fact and let it judge.
  For example, a benign twin flagged as possibly compromised is cured by its clearing document
  reaching the model, never by code that hard-codes "benign".
- A step the answer depends on is enforced in code, not only asked for in the prompt.

**Source.** Author's agreement after ticket 43, 26 October 2026. Ticket 43 rulings 8 and 9;
B-076.

## P-02: The agent flags a concern; it never pronounces a verdict

**Rule.** The agent raises a concern with its evidence, in hedged words such as "possibly" or
"likely compromised". It never declares an account compromised on its own.

**Why.** A successful sign-in from an attacker's address is strong evidence, but it does not
prove who was at the keyboard or what they intended. The same reasoning left S4 intentionally
unresolved.

**How to apply.** Eval checks must accept hedged wording, and be named for what they test
("flags X as possibly compromised"). Making the agent always hedge would be a prompt change
for its own ticket.

**Source.** Ticket 43, ruling 7, 26 October 2026; the S4 ruling in the spec's decisions log.

## P-03: The model is a floor, not the target

**Rule.** The current model is the cheapest one that passes today's eval. It is not a design
target. Higher-tier work needs higher-tier reasoning.

**Why.** The app may grow toward a tier 1 to tier 3 SOC analyst. That work needs
high-reasoning models, and each higher tier may need a stronger model or a team of models in
an agentic workflow.

**How to apply.** Keep the model behind the one creation seam. Let the eval set decide any
replacement (AUD-031). Do not shape the design around a small model's limits; compensate for
them in code under P-01, in ways a stronger model would still benefit from.

**Source.** Author's direction after ticket 43, 26 October 2026.
