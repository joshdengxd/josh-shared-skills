# Josh's shared skills

Agent skills for a team's delivery cycle: from a vague ticket to a production release, with a human at every irreversible step. Written for Claude Code and Codex. All examples use a fictional stack (a TypeScript/React app, GitHub Actions, Argo CD, a Splunk-style log search).

<p align="center"><a href="assets/cycle.svg?raw=true"><img src="assets/cycle.svg" alt="Delivery cycle: refine, build and evaluate, run at scale, ship, investigate with data, foundations" width="100%"></a><br><sub>Click the diagram to open it full size.</sub></p>

## Skill groups

### 1. Refine
Flow: an epic or feature is turned into a spec (the agent drafts, you review), the spec is broken down into tickets, and each ticket is refined. Only the last step has a skill today.

| Skill | What it does |
|---|---|
| `ticket-refine` | Refines a ticket with the user into an implementation-ready spec. One consensus comment, updated on re-run. The user approves before anything is posted. |

### 2. Build, evaluate, improve
Implement a task, then evaluate the result with independent subagents, and feed the findings back until it passes. The implementer never grades itself.

| Skill | Role in the loop |
|---|---|
| `implement-with-score-gate` | Implements in a worktree; a fresh subagent gives a 0-10 score and a problem list; fix and re-score with a new subagent until the pass line is reached; opens a PR. The score and the pass line are set by the user per task; there is no fixed rubric. |
| `verify-against-criteria` | Evaluation: read-only verdict (PASS / PASS-with-remarks / GAPS / DEFECTS) with evidence per acceptance criterion. |
| `live-env-local-test` | Evaluation: routes chosen requests from a real non-production environment to the local server and checks the flow in the browser (Chrome DevTools MCP). |

`verify-against-criteria` and `live-env-local-test` run as a **post-task hook in a separate subagent**: the implementer finishes, a fresh agent that never saw its reasoning checks the result.

### 3. Run it at scale
| Skill | What it does |
|---|---|
| `issue-batch-drain` | Groups refined issues into PRs. For each group, one fresh implementer agent runs group 2's loop, then a separate fresh verifier agent checks it. One group at a time; the orchestrator keeps a running ledger. The user approves the plan. |

### 4. Ship
| Skill | What it does |
|---|---|
| `deploy-to-staging` | Triggers a deploy workflow with an explicit tag and waits for the GitOps sync. The user confirms tag, environment and region. |
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
2. **Human on the irreversible step.** Merge, production actions, posting on a ticket.
3. **Bounded loops.** A few fix rounds, then a human decides.
4. **Compact orchestration.** Orchestrators plan and keep a ledger; subagents do the work.
5. **Evidence over opinion.** Decisions come with queries, counts and charts.
6. **Memory of what worked.** `wrap-up` captures the successful path.

## Install

Copy a folder from `skills/` into `.claude/skills/` (Claude Code) or `~/.codex/skills/` (Codex). Skills are plain markdown; adapt the commands to your stack.

## License

MIT.
