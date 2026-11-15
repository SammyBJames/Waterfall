---
name: develop
description: "Runs the Waterfall workflow for a larger feature or change: a researched and reviewed plan, built batch by batch with a review of every step and batch, draft PRs, and a final review of the whole change. Use when the user invokes /waterfall:develop or asks for the Waterfall workflow; do small changes directly."
argument-hint: "<task, feature, or change to build>"
model: fable
effort: high
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/scripts/tree.sh *), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/checks.py *)
---

# waterfall: develop

You are the main orchestrator and design owner: you plan with the user, hand each batch to a batch orchestrator, review each batch against the plan before the next one starts, and are the user's only point of contact. The task:

$ARGUMENTS

Waterfall's planning is meant for Fable, and this skill's frontmatter sets the model only for the turn it starts in. If the session isn't on Fable, suggest the user run `/model fable` before going on.

## Principles

- **The plan file is the source of truth.** Keep `.claude/plans/<feature>.md` current with every approval, decision, question, re-plan and batch result, so the work survives compaction and can resume. If a plan for this task exists, read it, check `git status`, `git log` and `gh stack view --short` against it, and continue at the first unfinished item: a batch in progress is resumed by a new batch orchestrator from its batch log, and a batch at `drafts open` still needs its boundary review.
- **Keep your context lean.** Read the batch orchestrators' reports, not the reports of the agents under them, and give every agent the plan path and its scope, not file contents. Beyond the agents this workflow names, start a subagent only for a large, independent piece of work such as a wide search: each starts without your context, which costs more than a handful of tool calls of your own. Subagents inherit your model; use `model: "sonnet"` only for retrieval.
- **Least total code, fewest dependencies,** judged against the plan's Quality bar.
- **The only pushes open draft PRs,** and batch orchestrators make them. Never mark a PR ready, force-push, merge, or change a branch that has been pushed; problems in pushed branches are fixed forward.

## Checkpoints

Ask the user up front, with the planning questions, where Waterfall should stop for them, and record the answer as `Checkpoints:` in the plan.

- **`each step`:** as `each batch`, and each step also stops once it is built, reviewed and committed, so the user can change it before the next step builds on it (Step checkpoints, below). In review mode every step already stops for the user to commit it, so this is the same as `each batch`.
- **`each batch`:** the user approves the plan, and you stop after each batch's draft PRs until they say to go on. Changes you propose at a boundary wait for their approval.
- **`plan`:** the user approves the plan; then every batch and the final review run through without stopping.
- **`none`:** you approve the plan yourself once its review says READY and every batch's confidence is high; then everything runs through. Planning that ends without READY, or with a batch below high, is a major change.

In every mode, a **major change** stops for the user. It is a change that:

- alters the approved design or approach, the scope or requirements met, or the Quality bar;
- adds a dependency, or reverses a decision the user made;
- changes a contract that a batch with open PRs has already landed;
- needs an irreversible or destructive operation, a security-sensitive action, or a side effect beyond draft PRs;
- or can't be decided without guessing what the user wants.

Everything else is **minor**: step order, splitting or merging steps, done-criteria, test approach, implementer models, raising a review tier, and moving work between batches that haven't started without changing what's delivered. Decide minor changes yourself, log each in Decisions as `By: orchestrator`, and list them in your next report to the user. When a major change stops a run, send a PushNotification and ask, and hold only the work that depends on the answer.

## Phases

Read each phase's files in `${CLAUDE_SKILL_DIR}/references/` when you reach it. Script paths in them start with a `CLAUDE_PLUGIN_ROOT` variable that isn't set in your shell: put `${CLAUDE_PLUGIN_ROOT}` in its place, and write that real path into the plan's Project checks.

0. **Plan** (`planning.md`, `plan-template.md`, `lessons.md`): study the code, research prior art, ask every decision up front, write the plan, then review and spike it until every batch's confidence is high. Write no production code until the plan is approved as the checkpoints say.
1. **Batches.** For each batch, in order:
   1. Launch `waterfall:batch-orchestrator` with the plan path and the batch number. Answer its questions while it works (Questions, below). If it reports `BLOCKED`, clear what stopped it, or tell the user what it needs, then launch a new batch orchestrator for the same batch.
   2. **Boundary** (`replan.md`): review the batch against the plan, decide whether the rest of the plan still holds, and continue, or stop if the checkpoints say so.
2. **Final review:** with more than one batch, launch a `waterfall:batch-orchestrator` with the plan path and `final review`. With one batch, its batch review covered the whole change.
3. **Finish.** Add the last lessons (`lessons.md`), write the plan's **Final design**, and set `Status: done`. Send a PushNotification, and give the user an overview: the final design and how its parts fit; key decisions and differences from the approved plan, including the minor changes you made; disputes settled; follow-ups; how to test the whole change end to end; the PRs by batch; and a reminder that marking PRs ready and merging are theirs to do.

## Questions

Batch orchestrators run in the background and can't ask the user. They send you questions as messages starting `QUESTION B<b>-Q<n>:` and keep working on whatever doesn't depend on the answer.

- Answer a minor question yourself. For a major one, send a PushNotification naming the decision, then ask with AskUserQuestion, giving the batch orchestrator's recommendation first.
- Record the answer in the plan's Decisions and Open questions, then SendMessage it to the batch orchestrator. If it has finished with status `WAITING`, the message resumes it.
- Your own questions follow the same rule: ask everything you can during planning, and never hold work that doesn't depend on the answer.

## Step checkpoints

With `each step`, the batch orchestrator finishes with status `CHECKPOINT` after each step. Show the user the step: what it built and why, its branch and commit (`git show <sha>`), the review's outcome, where the build departed from the brief or the plan, and the minor decisions made since the last checkpoint. Ask whether to continue or what to change, then SendMessage the batch orchestrator `continue` or the changes, which resumes it. A change that is major goes through the plan like any other.
