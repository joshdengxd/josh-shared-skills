---
name: live-env-local-test
description: Check a local change inside a real non-production environment by sending selected requests to your local dev server, driven with Chrome DevTools MCP. Run it in a separate subagent after the implementation task. Also covers testing several unmerged PRs together. Use when the user says "test this against staging locally" or /live-env-local-test.
---

# Live Environment Local Test

Run your local build as part of a real environment without deploying it. Designed as a **post-task check**: after an agent implements a change, a separate subagent proves the user-visible behaviour in a browser.

## Ground rules
- Non-production environments only; refuse a production address.
- Any throwaway local tweak needed to make this work (for example a proxy entry) is noted when made and removed before anything is committed. Look at the final `git diff` to confirm.

## Procedure
1. Start the dev server locally and note its port.
2. Arrange routing so that requests carrying a marker header (for example `X-Route-To: <your-machine>`) reach the local server while everyone else's traffic is unaffected. How this is done depends on the environment's gateway or proxy.
3. Using Chrome DevTools MCP, open the page, send the marker header, and walk through the flow described by the acceptance criteria.
4. Watch the console and network panels for errors or surprising calls. Take a screenshot for each criterion.
5. Report pass or fail per criterion, with the evidence.
6. Stop the server, undo the routing, and revert the throwaway tweaks.

## Several PRs at once
To see unmerged work from different branches together, combine them in a scratch checkout, treat the branches as read-only, run the same flow, and delete the scratch checkout afterwards. Never push to a branch you do not own.
