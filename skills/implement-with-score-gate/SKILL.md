---
name: implement-with-score-gate
description: Implement a refined ticket in an isolated worktree, then have a fresh subagent give the result a 0-10 score plus a list of problems; fix and re-score with a new subagent until the score reaches the threshold the user set, then open a PR (never merge). Use when the user says "implement this ticket" or runs /implement-with-score-gate.
---

# Implement with Score Gate

The agent that wrote the code is biased toward it. A fresh subagent that never saw the implementer's reasoning checks the result and gives a score. The user decides what score is good enough.

## What this is
- A cross-check pattern: implement, then an independent subagent gives a score from 0 to 10 and a concrete problem list, then fix, then a different independent subagent scores again.
- The score and the pass line are **set by the user (or agreed with the agent) per task**. A stricter pass line for risky changes, a looser one for small fixes.

## What this is not
- Not a fixed rubric. There is no built-in set of dimensions: the scorer judges the diff against the ticket's acceptance criteria and any extra criteria the user names.
- Not an automatic merge. The score only decides whether the PR is opened or more work is needed.

## Inputs
- Refined ticket (acceptance criteria), repo, base branch.
- **Pass line** (for example 8/10). If the user did not give one, ask before step 4.
- Optional: max fix rounds (suggest 3), extra criteria to score on.

## Steps
1. Create a worktree and branch from the base branch. Never work on the base branch.
2. Implement what the refined ticket says. Add or update tests.
3. Run the project's checks (type check, lint, unit tests). Fix failures before scoring.
4. Spawn a NEW subagent (fresh context, read-only). Give it only: the acceptance criteria, any extra criteria, the diff, the check output. It returns:
   - a score 0-10;
   - the problems that cost points, each with file:line and why;
   - anything it could not judge.
5. If score >= pass line: continue to step 6.
   If score < pass line: fix the listed problems, rerun checks, and score again with another NEW subagent. At the max rounds, stop and give the remaining list to the human.
6. Open a PR that mentions the ticket without closing it automatically. State the final score and any problems that remain in the description. Leave it for a person to merge.

## Rules
- The scorer never sees the implementer's reasoning or earlier scores.
- Never lower the pass line to get through; only the user can change it.
- Merge is always a human action.
- Verification that needs a real environment or a full criteria table is done by `verify-against-criteria` and `live-env-local-test`; this skill is the improve loop around them.
