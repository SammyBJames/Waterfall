# <Feature title>

Status: draft | approved (YYYY-MM-DD) | in progress | final review | done
Commit mode: claude-commits | review
Trunk: <branch>    Stack base: <branch>
Task: <the user's request, verbatim>

## Context
What exists today, and the relevant requirements, design docs and spec sections (with paths). Keep it short.

## Design
The approach and how the parts fit together: data model, interfaces and API shape, data flow, and error handling. Include what is deliberately left out. Point to existing code that will be reused.

## Decisions
| # | Decision | Chosen | Why | By |
|---|---|---|---|---|
| D1 | | | | user / orchestrator |

Disputes the orchestrator settled after the round limit go here too, marked "dispute".

## Project checks
| Check | Command | Baseline |
|---|---|---|
| build | | pass |
| test | | pass, or the failures that already existed |

## Steps

### [ ] 1. <title>
- Branch: <name> (commit mode)
- Goal: what this step delivers, in one or two sentences.
- Files: the main files or modules expected to change.
- Tests: what to test, including edge cases and failure paths.
- Docs and spec: what to update, if anything.
- Done when: criteria someone else could check.
- Record: (filled in as the step runs) commit or hand-off snapshot SHA, review rounds, disputes, deviations.

### [ ] 2. ...

## Follow-ups
Out-of-scope problems found along the way, each with where it is and why it matters. The final review handles them or passes them to the user.

## Final design
(Written at the end.) The design as built, the important details, differences from the approved design, and how to test the whole change end to end.
