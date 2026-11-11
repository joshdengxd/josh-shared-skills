---
name: deploy-to-staging
description: Put a chosen build on the staging environment through a CI workflow and GitOps sync, after the user confirms exactly what will be deployed; also covers a short-lived environment for an unmerged branch. Use when the user says "deploy to stage" or /deploy-to-staging.
---

# Deploy to Staging

## What you need
- A build to deploy: a specific identifier, or "newest build of the main branch".
- Target environment and region. The repo's agent rules file lists the defaults.

## Procedure
1. **Pick the build.** If the user gave a pattern that matches several builds, show the candidates and let them choose; never choose on their behalf. Pass the chosen identifier explicitly in the trigger.
2. **Confirm.** Show build, commit, environment and region in one block and wait for a yes.
3. **Trigger** the deploy workflow with the `gh` CLI.
4. **Follow it through.** The workflow raises a GitOps change; wait for that change to merge, then wait for the GitOps controller (for example Argo CD) to report the application as synced and healthy.
5. **Report** the outcome, and notify the team channel if the project uses one.

## Branch environments (before merge)
For an unmerged branch: build and tag the branch, create a temporary environment from that build (for example a short-lived Kubernetes pod), and tell the user its expiry (default: a few days), how to reach it (the routing header or URL) and how to remove it early. Then `run-e2e-automation` runs against it, and people do their manual QA there, before anyone merges.

## After merge
When staging reports healthy, run `run-e2e-automation` again on staging. The release only goes ahead when that run is clean.

## Limits
- Staging only; never production.
- If anything about build, environment or region is unclear, ask.
