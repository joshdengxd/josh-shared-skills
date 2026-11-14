---
name: implement-with-verification-gate
description: Implement a refined ticket in an isolated worktree, then show it works before a PR is opened - type check, lint, unit tests and the e2e tests covering the change pass, and a fresh subagent checks every acceptance criterion (in a browser with Chrome DevTools MCP where it can be seen, otherwise by a test or API call) and records evidence. Fix and re-verify with a new subagent until everything passes, then open a PR (never merge). Use when the user says "implement this ticket" or runs /implement-with-verification-gate.
---

# Implement with Verification Gate

The agent that wrote the code is biased toward it, and "it compiles" is not "it works". So the gate is evidence: the project's own checks, plus every acceptance criterion checked by a fresh subagent that never saw the implementer's reasoning.

## Inputs
- Refined ticket with acceptance criteria (from `ticket-refine`), repo, base branch.
- Optional: max fix rounds (default 3).

If the ticket is too big to implement and verify in one sitting, stop and send it back to refinement to be split.

## Steps
1. **Worktree.** Create a branch and worktree from the base branch. Never work on the base branch.
2. **Implement** what the refined ticket says. Add or update tests, including an end-to-end test for the new behaviour when the project has a suite.
3. **Checks.** Run type check, lint, unit tests and the end-to-end tests that cover the change. All must pass before step 4.
4. **Verification.** Spawn a NEW subagent with fresh context. Give it only: the acceptance criteria, how to reach the app, and the step 3 output. It must not edit files; it may run the app and the existing tests. For each criterion it records:
   - how it checked: in a browser with Chrome DevTools MCP when the behaviour is visible there, otherwise by running an existing test or an API call;
   - what it saw, with evidence (screenshot, test or command output, any console error or failed network call);
   - status: **met**, **not met**, or **could not check** (with the reason).

   It runs the app locally, or follows `live-env-local-test` itself when the change only makes sense inside a real environment.
5. **Decide.**
   - Every check green and every criterion **met**: go to step 6.
   - Otherwise: fix, rerun all of step 3, and verify again with another NEW subagent. At the max rounds, stop and hand the open items to the user.
6. **PR.** Open a PR that mentions the ticket without closing it automatically. The description holds the criteria table (criterion, how checked, status, evidence) and the check results. Leave it for a person to merge.

## Rules
- The verifier never sees the implementer's reasoning or earlier verdicts.
- **Could not check** never counts as met.
- Never skip, disable or loosen a check, and never edit a test just to make it pass.
- Merge is always a human action.
- If this skill already runs inside a subagent that cannot start its own subagents, stop after step 3 and return; the caller starts the verifier and the fix rounds.
- For a code-level review of the diff (where each criterion is implemented, what tests cover it, loose ends), add `verify-against-criteria`. This skill shows behaviour; that one reads the code.
