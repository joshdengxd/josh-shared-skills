---
name: prod-release-gate
description: Coach a production release one stage at a time: the agent prepares, checks and explains, pauses for an explicit go-ahead at each stage, and a person performs every production action. Includes a rollback plan up front and health checks before the rollout widens. Use when the user says "release to production" or /prod-release-gate.
---

# Production Release Gate

The agent is the co-pilot, not the pilot. It gathers facts and gives a recommendation; the human decides and operates the production controls.

## Preparation (before stage 1)
- Confirm the build identifier and find the team's release checklist.
- Write the rollback plan first: what to revert or redeploy, and the exact steps. Keep it visible for the whole release.
- Draft the release notes and the release record. Show the drafts; nothing is created until the user approves them.

## Stages
Run these in order. At the end of each, summarize what happened and wait for the user to say go before the next one.

1. **Scope.** List what is shipping since the last release: merged changes, authors, anything risky.
2. **Record.** Create the release record from the approved draft.
3. **Build health.** Watch CI for the build until it is green; report any failure with its cause.
4. **First exposure.** Tell the user which console action starts the rollout (for example the sync or the first traffic share). The user performs it.
5. **Health check.** Compare error rate, latency and the key business metric against the baseline, using the dashboards and log search. Give a clear recommendation, **proceed** or **hold**, with the numbers.
6. **Widen.** Repeat stages 4 and 5 for each larger traffic share.
7. **Close out.** Update the release record and notify the people who need to know.

## If the recommendation is hold
Stop, present the rollback plan, and let the user choose. Do not widen, retry or improvise.

## Boundaries
- The agent never performs a production control action itself.
- Stages are never combined, and none is skipped.
