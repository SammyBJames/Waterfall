---
name: develop
description: "Runs the Waterfall workflow for a larger feature or change: an approved plan, an implementer and reviewer for each step, then a specialist final review. Use when the user invokes /waterfall:develop or asks for the Waterfall workflow; do small changes directly."
argument-hint: "<task, feature, or change to build>"
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/scripts/tree.sh *)
---

# waterfall: develop

You are the orchestrator and design owner: you plan with the user, run the subagents, check their work, and own git. The task:

$ARGUMENTS

## Principles

- **The plan file is the source of truth.** Update `.claude/plans/<feature>.md` after every event (approval, step done, decision, dispute, follow-up) so the work survives compaction and can resume. If a plan for this task exists, read it, check `git status` and `git log` against it, and continue at the first unfinished item.
- **The user approves every plan change:** design, steps, scope, order, splits and new dependencies. Ask with AskUserQuestion and log the decision.
- **Verify; don't trust.** Run the plan's check commands yourself after every turn that changes code.
- **Least total code, fewest dependencies.** Every finding and fix must be worth the code it adds under the plan's Quality bar.
- **Keep your context lean.** Give subagents the plan path, step and scope, not file contents, and keep their IDs to continue them with SendMessage. Agents write reports under `.claude/plans/<feature>/`; read only what you need, and pass file paths and finding numbers between agents instead of copying findings.
- **Never push, open PRs, force-push or merge.**

## Phases

Read each phase's files in `${CLAUDE_SKILL_DIR}/references/` when you reach it.

0. **Plan** (`planning.md`, `plan-template.md`). Write no production code until the user explicitly approves the plan.
1. **Steps** (`step-loop.md`, `git.md`). Per step: implementer → your checks → reviewer at the step's tier → validator for unproven blocking findings → fix rounds → conformance → `comment-cleanup` → commit or hand-off.
2. **Final review** (`final-review.md`).
3. **Finish.** Run `comment-cleanup` over the whole change (base ref: the stack base), then the checks. In commit mode, commit its changes on the top branch; in review mode, hand them to the user. Write the plan's **Final design**, and set `Status: done`. Give the user an overview: the final design and how its parts fit; key decisions and differences from the approved plan; disputes you settled; follow-ups; how to test the whole change end to end; and in commit mode, `gh stack view --short` and a reminder that `gh stack submit` is theirs to run.
