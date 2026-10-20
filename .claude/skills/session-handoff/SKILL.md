---
name: session-handoff
description: Use when the user says "session handoff", "wrap up session", "hand off", "handoff summary", or wants a structured end-of-session summary before clearing context. Writes a structured handoff (decisions, shipped changes, key files, running state, verification steps, deferrals, open questions) to a fixed file — `<repo>/.scratch/handoff/SESSION_HANDOFF.md`, overwritten each run — so either Claude Code or Codex can continue in a fresh session.
---

# Session Handoff

Produce a repeatable end-of-session summary so the user can clear context or switch between Claude Code and Codex without losing continuity. The next agent should be able to pick up by reading this summary alone.

This is a **context-handoff artifact**, not a status report. The audience is a future instance of you, not a stakeholder.

Copied from the author's VPS Manager workspace on 20 October 2026 and adapted to this repo: the fixed file and backup folder live under `.scratch/handoff/`, the memory path is this project's auto-memory folder, and the project's written artifacts live under `.scratch/<initiative>/` (maps, tickets, specs, research) and `docs/` (logs, audit register, contracts).

## When to invoke

User says: "session handoff", "wrap up session", "hand off", "handoff summary", "let's wrap up", "summarize before I clear", or any near-equivalent. Also invoke proactively if the user says they're about to `/clear` without having run it yet.

## How to produce the summary

1. **Review the full conversation**, not just the last few turns. Handoffs miss things when they only summarize recent context.
2. **Pull state from these sources (in order):**
   - Plan or design files referenced this session — name them by their actual path. In this project: the current initiative's `map.md`, its tickets under `issues/`, its `spec.md`, research notes under `research/`, and the logs and register under `docs/`.
   - The host task/plan state — any in-progress or pending tasks.
   - Background processes you started — record the owning host, real OS PID if known, command, working directory, and stop method. Host-specific shell IDs alone cannot transfer to the other agent.
   - Files created or modified this session — you know what you touched; don't grep to re-discover.
   - Memory files written or updated (Claude Code's auto-memory folder for this repo; Codex has none).
   - Unresolved questions — things you asked the user that never got a clear answer, or things the user asked that got deflected.
3. **Do NOT audit the filesystem.** This is synthesis of what happened in THIS session. No `git log`, no broad file sweeps. If you didn't touch it this session, it doesn't belong here. (The one exception is the previous handoff itself — see step 4.)
4. **READ the existing handoff first, then overwrite it:** `<repo>/.scratch/handoff/SESSION_HANDOFF.md`.
   - Reading it is **not** the filesystem audit banned in step 3 — it is one known file, and it is the only record of what the *previous* session left open.
   - Read it for a reason: **preserve unresolved context without asserting stale status.** Carry items verified open this session; label the remaining relevant items "carried, not reverified". Do not mine backup handoffs or claim that old lists are still live. Note in "Where it started" that this handoff supersedes the previous one. The incoming agent verifies relevant current state before acting.
   - Then overwrite — only the latest handoff is kept, no archive in the working file (the offered backup in step 5 is the one deliberate exception). Read before overwriting regardless of which host performs the write. The file's first two lines are a staleness header (see the template). Do NOT update memory from this skill. Then post a **short confirmation in chat** — path + a one-line count (e.g. "Handoff saved to `…/SESSION_HANDOFF.md` — 4 decisions, 3 open items"). Do not reprint the full handoff in chat.
5. **Offer the backup — EVERY run, one host question UI offer, or a concise chat question if that UI is unavailable or disallowed (the author's design, 2026-08-04).** Immediately after the chat confirmation, offer to copy the just-written handoff into `<repo>/.scratch/handoff/handoff-backup/`. Why: the working file is overwrite-by-design, so a single routine run silently destroys a handoff the author cared about; the offer makes the safety systematic while keeping the decision theirs.
   - **Naming format — preserve it exactly:** `SESSION_HANDOFF_<Topic_Slug>_<DD-MM-YYYY_HH-MM>_bk.md`. Topic slug = short Title_Case_With_Underscores derived from this handoff's title (e.g. `Knowledge_Base_Ticket02_Store_Chosen`); datetime = **now, DD-MM-YYYY_HH-MM local time** (hour+minute added 2026-08-04 at the author's request so same-day handoffs never collide). Suffix `_bk`. Show the full proposed filename in the pop-up option so the author accepts with one click or adjusts via "Other".
   - **Embed a recommendation in the option label:** sessions with rulings, spec decisions, or builds → "(Recommended)"; routine sessions → offer plainly with no recommendation. The offer itself always appears; only the recommendation varies.
   - **Declining changes nothing** — no copy, no second ask. On accept, copy the file, verify the copy exists with nonzero size, and confirm in one line.

## Output template — use exactly this structure, every time

```
# Session Handoff — <one-line title of what this session was about>
*Saved: <YYYY-MM-DD> · Topic: <one-line topic>*

## Where it started
<2-3 sentences: what the user asked for, key framing or constraints that emerged>

## Decisions locked + what shipped
- <decision or change> — <why, and where it lives (absolute path if a file)>
- ...

## Key files for next session
- `<absolute path>` — <why the next agent should read this first>
- Plan file: `<path>` (if a plan drove the session)
- Memory files touched: `<paths>` (if any)

## Running state
- Background processes: <owning agent + command + working directory + OS PID if known + stop method; host handle only as supplementary detail> — or "none"
- Dev servers / ports: <url + port> — or "none"
- Open worktrees / branches: <paths> — or "none"

## Verification — how to confirm things still work
- `<command>` — <expected outcome>
- ...

## Deferred + open questions
- Deferred: <item> — <why pushed to later>
- Open: <question needing the user's input> — <context>

## Pick up here
<1-2 sentences: the single most likely next action for a fresh agent>
```

A project's own `CLAUDE.md` may require one extra, clearly named section for a specific stretch of work; add it exactly where that file says, and change nothing else in the template.

## Hard rules

1. **Write to the fixed file, overwrite, keep only the latest.** Always write to `<repo>/.scratch/handoff/SESSION_HANDOFF.md` (overwrite — no archive of old handoffs **in the working file**; the ONE exception is the offered backup copy to `handoff-backup/`, step 5, which exists precisely because the working file is overwritten), then a short chat confirmation only (not the full handoff). Never update memory from this skill.
2. **Never invent state.** If a section has nothing to report, write "none" — do not omit the section. Structure stability is the whole point.
3. **Absolute paths always.** The next agent may have a different working directory.
4. **If a plan file drove the session, name it first** in "Key files" so the next agent reads it before anything else.
5. **No emojis, no hype, no "great job" summaries.** Terse and concrete — paths, commands, shell IDs, decisions. Match the tone of a seasoned engineer handing off at end-of-shift.
6. **Background process ownership is critical.** Record real process details in `Running state`. Mark a PID unknown rather than inventing it. Finish or stop writes before another agent takes over; a Claude or Codex session handle is not an OS PID.
7. **This repo may become public.** `<repo>` in this file means the repository root, the folder holding `CLAUDE.md`; resolve it to an absolute path when you write. The handoff file and its backups are git-ignored, so they may hold absolute paths. They still hold no keys, no personal names and no email addresses, same as every other file here.

## Anti-patterns — do not do these

- Summarizing the last 3 turns and calling it a handoff.
- Listing files by relative path.
- Skipping the "Running state" section because "nothing is running" — write "none" instead.
- Dumping the full handoff into chat. The full handoff goes to the file; chat gets only the short confirmation.
- Writing to any path other than the fixed `SESSION_HANDOFF.md`, or keeping old handoffs around outside `handoff-backup/`. One working file, always overwritten; backups only through the step-5 offer, never silently.
- Skipping the backup offer, or making the backup without asking. The offer appears EVERY run; the copy happens only on the author's yes.
- Adding a "what went well / what went poorly" retrospective. This isn't a retro.
- Recommending next steps beyond the single "Pick up here" line. The next agent decides; you just hand off.
