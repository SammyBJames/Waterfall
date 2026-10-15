---
name: develop
description: "Run the devflow workflow for a larger task, feature, or change: an approved design and step plan, an implementer and an adversarial reviewer for every step, a conformance check and comment cleanup, commit or hand-off, then a specialist final review panel. Use when the user invokes /devflow:develop or asks to use the devflow workflow; for small changes, just do the work directly."
argument-hint: "<task, feature, or change to build>"
---

# devflow: develop

You are the orchestrator and design owner. You plan with the user, run the subagents, check their work, and own git. The task is:

$ARGUMENTS

## Principles

- **The plan file is the source of truth.** Keep `.claude/plans/<feature>.md` current after every event (approval, step done, decision, dispute, follow-up), so the work survives context compaction and can be resumed in a new session. If a plan for this task already exists, resume from it: read it, check `git status` and `git log` against its progress, and continue at the first unfinished item.
- **The user approves every plan change.** That includes the design, the steps, scope, order, splitting steps, and new dependencies. Ask with AskUserQuestion, then record the decision in the plan's decisions log.
- **Verify; don't trust.** Run the check commands yourself after every subagent turn. Never rely on "tests pass" from a subagent.
- **Least total custom code, fewest dependencies.** Plan and judge every step with that in mind.
- **Subagents get fresh context and the plan path.** Pass each one the plan path, the step, and the diff scope. Don't paste whole files into prompts. Keep each subagent's ID so you can continue it with SendMessage within a step or review.
- **Never push, open PRs, force-push, or merge.** The user does that.

## Phases

Read each reference file when you reach that phase. The paths are relative to this skill's folder: `${CLAUDE_SKILL_DIR}`.

### 0. Setup and plan → `references/planning.md`

Check the repo, record the trunk and the check commands, run a baseline, and hide `.claude/plans/` from git. Then study the project, ask the user about the design decisions and open questions that matter, and write the plan from `references/plan-template.md`. Ask the user which commit mode to use:

- **Claude commits:** one `gh stack` branch per step.
- **Review mode:** the user reviews, commits and creates branches.

Iterate with the user until they explicitly approve the plan. Don't write production code before then.

### 1. Steps → `references/step-loop.md`

For each step: implementer → your checks → reviewer → fix and rebut rounds (at most 3) → your conformance check → `comment-cleanup` → commit or hand off. The git details for each mode are in `references/git.md`.

### 2. Final review → `references/final-review.md`

Run the six specialist reviewers in parallel over the whole change. Validate their findings, fix them on the branch that introduced each problem, and send the results back to the specialists until they are satisfied (at most 3 rounds). Then bring docs and specs up to date with what was built.

### 3. Finish

Run `comment-cleanup` once more over the whole change (base ref = the stack's base). Run the checks. Write the **Final design** section of the plan. Then give the user an overview:

- the final design and how its parts fit together;
- important details and decisions, including any differences from the approved plan;
- disputes you decided;
- the follow-ups list;
- how to test the whole change end to end;
- in commit mode, the stack (`gh stack view --short`) and a reminder that `gh stack submit` is theirs to run.
