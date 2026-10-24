# <Feature title>

Status: draft | approved (YYYY-MM-DD) | in progress | final review | done
Commit mode: claude-commits | review
Trunk: <branch>    Stack base: <branch>
Task: <the user's request, verbatim>

## Context
What exists today, and the relevant requirements, design docs and spec sections, with paths.

## Design
The approach: data model, interfaces and API shape, data flow, error handling, existing code to reuse, and what is deliberately left out.

## Quality bar
Every finding and fix is judged against this section.
- Users and environment: who runs this and where.
- Threat model: who can send input, and what is trusted.
- Target scale: data sizes, request rates, devices.
- Accepted risks: failure modes this change won't handle, and why.

## Decisions
| # | Decision | Chosen | Why | By |
|---|---|---|---|---|
| D1 | | | | user / orchestrator / dispute |

## Project checks
| Check | Command (quiet form) | Baseline |
|---|---|---|
| build | | pass |
| test | | pass, or the existing failures |

## Steps

### [ ] 1. <title>
- Branch: <name> (in review mode, the user's branch, recorded after they commit)
- Review: full | light (why)
- Goal: what the step delivers, in a sentence or two.
- Files: the main files or modules it changes.
- Docs and spec: updates, if any.
- Done when: `criterion → test name or command`, one per line. For a criterion only a person can check, say how.
- Record: commit or hand-off SHA; tier as run; rounds; blocking findings by gate and outcome (fixed, withdrawn, rejected or downgraded by the validator, deferred, settled); if-minor applied and skipped; mutations killed/survived; escalations; escapes found later; disputes; deviations.

## Follow-ups
Out-of-scope problems found along the way: where, and why it matters.

## Final design
Written at the end: the design as built, differences from the approved design, and how to test the whole change end to end.
