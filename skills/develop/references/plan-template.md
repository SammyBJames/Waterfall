# <Feature title>

Status: draft | approved (YYYY-MM-DD, by user | by orchestrator) | in progress | final review | done
Commit mode: claude-commits | review
Checkpoints: each step | each batch | plan | none
Trunk: <branch>    Stack base: <branch>    Remote: <name> | none
PR template: <path> | none
Lessons: <path to lessons.md>
Task: <the user's request, verbatim>

## Context
What exists today, and the relevant requirements, design docs and spec sections, with paths.

## Research
From `research.md`: the approaches considered, the one chosen and why it beats the naive approach, and the pitfalls the steps below must handle, each with the step that handles it or the accepted risk.

## Design
The approach: data model, interfaces and API shape, data flow, error handling, existing code to reuse, and what is deliberately left out.

## Quality bar
Every finding and fix is judged against this section.
- Users and environment: who runs this and where.
- Threat model: who can send input, and what is trusted.
- Target scale: data sizes, request rates, devices.
- Accepted risks: failure modes this change won't handle, and why.

## Assumptions
What the batches take for granted that, if wrong, would change a contract, the design or several steps. Checked at every batch boundary.
| ID | Assumption | Relied on by | Status | Signpost | Hedge |
|---|---|---|---|---|---|
| A1 | | batches, steps | verified (how) / accepted / failed (boundary <b>) | evidence that would show it failing | what the plan does then |

## Decisions
| # | Decision | Chosen | Why | By |
|---|---|---|---|---|
| D1 | | | | user / orchestrator / research / spike / plan review / dispute |

## Open questions
| ID | Question | Recommendation | Blocks | Status |
|---|---|---|---|---|
| B1-Q1 | | | steps or PRs that depend on it | open / provisional (what was built on it) / answered (D<n>) |

## Project checks
Full suite: `.claude/plans/<feature>/checks.json`, run with `"${CLAUDE_PLUGIN_ROOT}/scripts/checks.py" <that path>`, once per step.
| Check | Group | Baseline |
|---|---|---|
| | | pass, or the existing failures |

Scoped commands for iterating:
| To run | Command |
|---|---|
| one package's tests | |
| one test or file | |
| one package's lint | |

CI-only checks: the checks that can't run here, and why.

## Plan review
Rounds run; spikes run (with their answers); then one line per finding and assumption: what it was and its outcome (plan changed, verified, settled by spike, accepted, rebutted).

## Batches
Steps are numbered through the whole plan, not within each batch: the numbers name their briefs, reviews and PR files.

### Batch 1: <title>
- Status: planned | building | panel review | drafts open | done
- Confidence: high | medium | low, and what keeps it below high.
- Delivers: what trunk gains if this batch merges alone, and why that's safe without the later batches.
- Contracts: the schemas, APIs, formats or names that later batches depend on, or none.
- PRs: `#<n> <branch> — <title>`, one per step, in stack order (after the drafts are open).
- Record: one line from the batch orchestrator (specialists run, blocking findings and how they ended); the batch log's path; and the boundary review's outcome (no change, refined, or re-planned, and why).

#### [ ] 1. <title>
- Branch: <name> (in review mode, the user's branch, recorded after they commit)
- Review: full | light (why)
- Implementer: sonnet | opus (why)
- Goal: what the step delivers, in a sentence or two.
- Files: the files it's expected to create or change, by path.
- Interfaces: consumes (exact names and signatures, from existing code or earlier steps); produces (exact names and signatures that later steps rely on, or the contract it must meet). Internals are left to the implementer.
- Docs and spec: updates, if any.
- Done when: `criterion → test name or command`, one per line. For a criterion only a person can check, say how.

### Batch 2: <title>
…

## Final review
Specialists run and skipped (why); rounds; findings and outcomes; the fix branch and its PR, or "skipped: one batch".

## Follow-ups
Out-of-scope problems found along the way: where, and why it matters.

## Final design
Written at the end: the design as built, differences from the approved design, and how to test the whole change end to end.
