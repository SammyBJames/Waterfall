# Batch boundary review

When a batch orchestrator reports a batch `DONE`, decide whether the rest of the plan still gives the best result given what the batch taught you, before the next batch builds on it. The decision is yours as design owner.

Work from the batch orchestrator's report, its batch log and the plan, and read code only where an answer depends on it. Write the review to `.claude/plans/<feature>/boundary-<b>.md`. Keep it proportionate: when the report shows no deviations, surprises or signposts, it is a few lines and the outcome is "no change".

## 1. After-action review

1. **What was supposed to happen:** the batch's Delivers, Contracts and steps as planned.
2. **What happened:** the contracts as built, deviations and rulings, planned versus actual effort, surprises, escapes and the panel's findings. Add any peer review comments on earlier PRs (`gh pr view <n> --json reviews,comments`).
3. **Why they differ:** the cause of each difference that matters. Product causes (a wrong assumption, a missed requirement, code that wasn't as the plan thought) can change the plan. Process causes (a vague brief, a missing check, a recurring review finding) go to the lessons file.
4. **Sustain and improve:** what worked and should be repeated in the next batch, and what should change.

## 2. Assumptions

For each assumption in the plan's table that isn't verified yet, and each that this batch touched, compare its signpost with what the batch found. Mark it **verified** (with the evidence), **open** or **failed**. A failed assumption calls for its hedge, or a re-plan if the hedge no longer fits. Add any new load-bearing assumption the batch revealed, with its signpost and hedge.

## 3. Look ahead

Judge whether the rest of the plan still holds. Leave exact files, names and signatures to the next batch orchestrator, which checks its steps against the code as built before it starts.

- **Contracts and order.** Each contract the remaining batches rely on still serves them as it was built, and the next batch's steps still make sense in the planned order.
- **A better path.** Has this batch shown a simpler way to do what's left: an existing helper, a pattern that worked, a step that is no longer needed? Prefer removing work to adding it.
- **Pre-mortem.** Imagine the next batch has gone badly and forced a change to the PRs just opened. Write down the two or three likeliest reasons, and settle any that are plausible by reading the code or giving a `waterfall:prototyper` a spike.

Look at later batches only where the review or the assumptions put them in question; each gets its own boundary review.

## 4. Decide

Choose one outcome, record it in the batch's Record in the plan, and set the batch's status to `done`:

- **No change:** the plan holds as written.
- **Refine:** minor changes (`SKILL.md`, Checkpoints), such as reordered, split, merged or removed steps, new done-criteria, or different implementer models or review tiers. Make them in the plan and log each in Decisions.
- **Re-plan:** a major change, or any change to batches or contracts beyond refining them. Draft the change in the plan, then run the planning loop on the changed batches (`planning.md`, Review until confident), telling the plan reviewer which batches changed and what has been built. A major change always goes to the user.

## 5. Report and continue

- **Hand over.** End the review with a `## For batch <b+1>` section for the next batch orchestrator: the contracts it consumes where they were built differently from the plan, the sustain and improve items that apply to it, the signposts to watch, and the plan changes you made.
- **Tell the user** the batch's PRs (number, title and URL, in stack order), what its panel found and changed, the key differences from the plan and their causes, assumptions that changed status, and the outcome with any minor changes you made.
- **Lessons.** Add the process causes, the sustain and improve items and the batch orchestrator's lesson candidates to the lessons file (`lessons.md`) where they'd change what an agent does next time.
- **Continue.** With checkpoints `each step` or `each batch`, stop here until the user says to go on and approves any proposed changes. Otherwise launch the next `waterfall:batch-orchestrator` right away, unless it depends on a major change that is waiting for the user. After the last batch, go to the final review.
