---
name: log-analysis
description: Answer questions with log search and metrics dashboards: debug incidents, size a change, test an assumption before a design decision, back a proposal with numbers, watch a release, or read an A/B test. Use when the user asks "what is going on", "how often does X happen", "is it safe to change Y", "did the release hold", or runs /log-analysis.
---

# Log Analysis

Logs and metrics are evidence. This skill turns a question into a small, reproducible investigation and reports what the data does and does not show. Debugging is one use among several. Examples use a made-up stack.

## Kinds of question
| Kind | Example | You deliver |
|---|---|---|
| Incident | "some users get a 502 at checkout" | probable cause, supporting data, next check |
| Sizing | "who still calls the old endpoint?" | volume, trend, biggest callers |
| Assumption | "can we drop this parameter?" | numbers that back or contradict it |
| Proposal | "should retries be capped?" | before/after figures and charts |
| Baseline | "what does normal look like here?" | typical latency, error rate, peak load |
| Release watch | "is the new version healthy?" | comparison with the previous period |
| A/B test | "did variant B help?" | effect size with its uncertainty, guardrails |

## Working method
1. **Sharpen the question.** Write down the measurable version and what result would change the decision.
2. **Plan the evidence.** Which service, which field, which period, which comparison period.
3. **Run it small first.** Start in a lower environment; widen scope only when the shape is clear. Pin the time window explicitly so a rerun gives the same answer.
4. **Make it repeatable.** Include the exact queries in the answer, and link the saved search or dashboard so others can rerun them.
5. **Follow a request through services** by its correlation id from the entry point onward; note where it vanishes or slows.
6. **Report in this order:** the answer in a sentence; the evidence; limits (sampling, retention, missing fields); what to check next. Say which statements were observed and which are guesses.

## Example
Question: "Can we retire the `v1` response format?"
Plan: count requests per format and per client over the last month.
Finding: v1 is under 1% of traffic from three clients; two have a newer client available. Recommendation: deprecate with notice to the third.

## A/B tests
Before looking at results, check there is one primary metric, guardrail metrics (errors, latency), a planned duration and sample size, and stable assignment. Report an interval, not only a point value. Do not call a winner from a short good run; look for a hidden drop in a segment. If the setup is unsound, say that instead.

## Cautions
- Ask before querying production data.
- Aggregate; never export personal data.
- A pattern in the data is not yet a cause.
