---
name: run-e2e-automation
description: Run the end-to-end test suite against a chosen non-production environment (a private branch environment before merge, staging after merge), wait for it, and report a clear verdict with failures classified as real, flaky or environmental. Use when the user says "run the automation", "run e2e on staging", or /run-e2e-automation.
---

# Run E2E Automation

The suite is the safety net on both sides of a merge. This skill runs it, reads the result, and tells the user whether the change is safe to move forward.

## When it runs
1. **Before merge**, against the private environment built from the branch.
2. **After merge**, against staging, once the deployment is healthy. A release only proceeds when this run is clean.

Manual QA is separate: people test the exploratory and judgment-heavy paths in the same environment. This skill covers the automated side only and says so in its report.

## Inputs
- Target environment (private or staging) and the build it should be running.
- The suite to run: all, or a named subset.

## Procedure
1. **Check the target.** Confirm the environment is healthy and serving the build you expect. If the build is not the one in question, stop and say so.
2. **Start the suite** through its CI workflow with the `gh` CLI, naming the environment explicitly.
3. **Wait** for completion; follow the run rather than guessing.
4. **Read the results.** For each failure, open the report (logs, screenshots, traces) and classify it:
   - **Real:** the behaviour is wrong; point to the likely change responsible.
   - **Flaky:** passes on rerun or fails the same way on unrelated branches. Rerun the failing tests once to confirm; do not rerun the whole suite repeatedly.
   - **Environmental:** the environment, data or a dependency is at fault.
5. **Report.**
   - Verdict: **clean**, **clean after flaky reruns**, or **blocked**.
   - Counts, the failures with their class and evidence, and what you reran.
   - A recommendation: continue, or fix first.

## Rules
- Non-production environments only.
- Never mark a real failure as flaky to unblock a release.
- Do not edit tests to make them pass; report them.
- The decision to merge or release stays with a person.
