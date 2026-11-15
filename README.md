# Josh's shared skills

Agent skills for a team's delivery cycle: from a vague ticket to a production release, with a human at every irreversible step. Written for Claude Code and Codex. All examples use a fictional stack (a TypeScript/React app, GitHub Actions, Argo CD, a Splunk-style log search).

<p align="center"><a href="assets/cycle.svg?raw=true"><img src="assets/cycle.svg" alt="Delivery cycle: refine, build and evaluate, run at scale, ship, investigate with data, foundations" width="100%"></a><br><sub>Click the diagram to open it full size.</sub></p>

## Ticket workflow

Four skills carry one ticket from idea to review, with the same states everywhere:

| State | Set by |
|---|---|
| Backlog | `create-ticket` |
| Refined | `refine-ticket` |
| In progress | `implement-and-verify-ticket`, when work starts (its PR uses `Refs #N`, never a closing keyword) |
| In review | `land-ticket` (merged, deployed, re-checked; the person tries it) |
| Done | a person, after trying it |

Asking an agent to implement or land a ticket (or starting `drain-refined`) is the approval for that stage's state moves and its landing comment; anything else posted on a ticket (new tickets, refinement summaries) is shown to the user first. The skills stay generic. Each project states its own settings in `AGENTS.md` under "Ticket workflow settings" (tracker, default branch, board or labels, commands, deploy); `agent-context-template` has the block.

## Skill groups

### 1. Refine
Flow: an epic or feature is turned into a spec or PRD (the agent drafts, you review), the spec is broken down into tickets, and each ticket is refined. Drafting the spec has no skill yet.

| Skill | What it does |
|---|---|
| `create-ticket` | Splits a PRD (or one request) into tickets with a fixed format, checkable acceptance criteria and dependencies. Drafts locally; creates them in the tracker, in dependency order, only after the user approves. Re-runs skip tickets already created. |
| `refine-ticket` | Refines a ticket with the user into an implementation-ready spec. One consensus comment, updated on re-run. The user approves before anything is posted; then the ticket moves to Refined. |

### 2. Build, evaluate, improve
Implement a task, then evaluate the result with independent subagents, and feed the findings back until it passes. The implementer never grades itself.

| Skill | Role in the loop |
|---|---|
| `implement-and-verify-ticket` | Implements in a worktree. Gate: type check, lint, unit tests and the e2e tests covering the change pass, and a fresh subagent checks every acceptance criterion with evidence: in a browser (Chrome DevTools MCP) where it can be seen, otherwise by a test or API call. Fix and re-verify with a new subagent until it passes; opens a PR. |
| `verify-against-criteria` | Evaluation: read-only code review of the diff, verdict (PASS / PASS-with-remarks / GAPS / DEFECTS) with evidence per acceptance criterion. |
| `live-env-local-test` | Evaluation: routes chosen requests from a real non-production environment to the local server and checks the flow in the browser (Chrome DevTools MCP). |

`verify-against-criteria` and `live-env-local-test` run as a **follow-up step in a separate subagent**: the implementer finishes, a fresh agent that never saw its reasoning checks the result.

### 3. Run it at scale
| Skill | What it does |
|---|---|
| `drain-refined` | Unattended: takes every Refined ticket, groups compatible ones into PRs, and per group runs a fresh implementer, a fresh behaviour verifier and a fresh code reviewer, with bounded fix rounds, then opens the PR and runs `land-ticket`. One group at a time; the orchestrator keeps only a ledger. A group that cannot pass is split, then skipped with a comment; a failed landing stops the run. Starting it is the approval for its merges; tickets end in In review. |

### 4. Ship
Before the merge, a private environment is built from the branch; the automated suite runs there and people do manual QA. After the merge, the build goes to staging and the suite runs again. Only a clean run goes to production.

| Skill | What it does |
|---|---|
| `deploy-to-staging` | Triggers a deploy workflow with an explicit tag and waits for the GitOps sync. Also builds a short-lived private environment from an unmerged branch. The user confirms tag, environment and region. |
| `run-e2e-automation` | Runs the end-to-end suite on a chosen non-production environment, classifies each failure as real, flaky or environmental, and reports a verdict. |
| `land-ticket` | After the user says "land it": checks green, merge, confirm the merge, wait for the deploy, a fresh subagent re-checks the criteria on the deployed site, ticket to In review with evidence and a checklist for the person. Never moves a ticket to Done. |
| `prod-release-gate` | Release checklist with a stop after every step, canary go/no-go from metrics and logs, rollback prepared first. A human performs every production action. |

### 5. Investigate with data
| Skill | What it does |
|---|---|
| `log-analysis` | Turns a question into queries, links and dashboards, and answers with evidence. Used before the work (sizing, assumptions, evidence for specs and designs) and after release (monitoring, debugging, A/B test analysis). Debugging is only one mode. |

### 6. Foundations
| Skill | What it does |
|---|---|
| `wrap-up` | Closes a session: saves the successful path as long-term memory so the next session follows it, updates docs, tidies, commits, reports. |
| `agent-context-template` | An `AGENTS.md` and a small context index (progressive context discovery) so agents follow the project's architecture and current syntax. |

## Design principles

1. **Producer is not the checker.** Every gate runs in a fresh context.
2. **Human on the irreversible step.** Merge (asked for, or approved by starting `drain-refined`), production actions, and new content posted on a ticket (tickets, refinement summaries).
3. **Bounded loops.** A few fix rounds, then a human decides.
4. **Compact orchestration.** Orchestrators plan and keep a ledger; subagents do the work.
5. **Evidence over opinion.** Decisions come with queries, counts and charts.
6. **Memory of what worked.** `wrap-up` captures the successful path.
7. **Small tickets.** Refinement splits work until each ticket can be implemented and verified in one sitting. Together with bounded loops, that keeps each run short and its cost predictable.

## Trust ladder

Today a person confirms every irreversible step, and the agents do the work in between. A step moves up a rung only after the team has a record of its gate being reliable:

1. **Agent proposes, person does.** Production actions today.
2. **Agent does, person approves each result.** Merges (the request to land is the approval) and ticket summaries (shown before posting) today.
3. **Agent does, person samples.** `drain-refined`: merges of tickets whose checks, browser verification and code review are green; the person tries each one in In review.
4. **Agent does, person is told.** Only for steps with a long clean record and a cheap undo.

Moving a step up is a team decision that changes the skill's own rules (for example "merge is always a human decision"), never something an agent decides for itself.

## Install

Copy a folder from `skills/` into `.claude/skills/` (Claude Code) or `~/.codex/skills/` (Codex). Skills are plain markdown; adapt the commands to your stack.

## License

MIT.
