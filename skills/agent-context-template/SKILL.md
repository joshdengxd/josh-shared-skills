---
name: agent-context-template
description: Create or improve a repo's agent context (AGENTS.md or CLAUDE.md plus a small context index) so agents follow the project's architecture and current syntax. Use when starting agent-assisted work in a repo or when agents keep making the same mistakes.
---

# Agent Context Template

Good context is short, specific and discoverable. Put the rules at the top; push detail into an index the agent opens only when needed (progressive context discovery).

## Steps
1. Inspect the repo: layout, build/test/lint commands, framework versions, conventions.
2. Write `AGENTS.md` (under ~100 lines) using the template below.
3. Create `docs/context/INDEX.md`: one line per topic file ("when to read it"), plus the topic files: architecture constraints, framework guidance for the versions actually used, testing conventions, deployment.
4. Test it: give a fresh agent a small task and see whether it follows the constraints. Fix gaps in the context, not in the prompt.

## AGENTS.md template
```
# Project
One paragraph: what it is, who uses it.

## Look before asking
Search code, docs and the ticket first. Ask the user only when they cannot answer it.

## Commands
build / test / lint / run (exact commands)

## Architecture constraints
- Layers and allowed dependencies (a small table)
- Where new code goes

## Conventions
Naming, error handling, testing. Current framework versions and the syntax to use (and deprecated patterns to avoid).

## Boundaries
Never touch: generated files, migrations without review, production configs.

## Context index
See docs/context/INDEX.md
```

## Maintenance
When an agent makes a repeated mistake, add the rule here. When a rule stops being true, delete it.
