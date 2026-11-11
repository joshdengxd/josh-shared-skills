---
name: ticket-refine
description: Work through a tracker ticket (Jira or GitHub issue) with the user until it is clear enough to implement, then keep one living summary on the ticket. Use when the user says "refine this ticket", names a ticket, or runs /ticket-refine.
---

# Ticket Refine

A short conversation that replaces guessing later. The agent researches and proposes; the user decides.

## Stage 1: Read
Open the ticket, its comments and linked items. If the ticket already carries a refinement summary, start from it. If the ticket is closed, ask the user whether to continue before doing anything.

## Stage 2: Research
Start a research subagent to look through the code and docs. It reports back: where the change would land, patterns the codebase already uses for similar work, and risks. It makes no edits.

## Stage 3: Decide together
Take the open points one at a time: scope, approach, affected files, edge cases, acceptance criteria, what is explicitly out of scope. For each point, suggest an answer with a reason and let the user accept or change it. Settle small points quickly; spend the time on the ones that could send the work in different directions.

## Stage 4: Write it up
Draft the summary: what and why, decisions taken, where to change, acceptance criteria, out of scope, remaining risks. Check that:
- each acceptance criterion is something a reviewer can actually check, and comes from a decision in stage 3;
- no question is left open.

## Stage 5: Publish
Show the draft and wait for the user's go-ahead. Then post it as the ticket's single refinement summary. On later runs, revise that summary in place rather than adding another.

## Creating a ticket
When a new ticket is needed, lay out its fields (title, type, component, priority, labels) and wait for confirmation before creating it.
