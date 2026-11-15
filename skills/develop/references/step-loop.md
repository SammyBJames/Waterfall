# The step loop

You are the batch orchestrator. Do your batch's steps in order. Set the batch's status to `building` in the plan when its first step starts.

Two helpers:

- `"${CLAUDE_PLUGIN_ROOT}/scripts/checks.py" <checks config>` runs the plan's full suite and stores the result, pass or fail, for that exact tree. If a failure looks flaky or environmental (a port in use, a service that's down) and not caused by the change, add `--rerun` once; a failure that repeats is real.
- `"${CLAUDE_PLUGIN_ROOT}/scripts/tree.sh" fingerprint` hashes the working tree without touching the index. Use it to confirm reviewers left the tree alone.

## 1. Prepare

- **Commit mode:** you're on the right branch with a clean tree (`git.md`).
- **Review mode:** the user has committed the previous step (`git.md`). If they edited the code first, read their changes.
- **First step of a later batch:** check what happened to the earlier batches' PRs (`git.md`, Before a later batch).

## 2. Brief

Write the step's brief to `.claude/plans/<feature>/step-<n>-brief.md`, against the code as it is now, not as the plan imagined it. The implementer works from the brief instead of the plan.

A brief records the decisions the implementer can't make alone and leaves the rest to them. Don't write function bodies, internal names or a file-by-file procedure; sketch code only for an algorithm the contracts and tests don't determine. A line that decides nothing ("handle errors appropriately") is a gap, and a brief longer than the code it describes has written the code. It usually fits on a page:

- **Intent:** what the step delivers and why: the requirement it serves and what later steps need from it. This guides the implementer where the brief is silent.
- **Contracts** (fixed): what the step consumes, as earlier steps actually built it, and what it must produce that later steps, the plan's contracts or the spec rely on: exact names, signatures, routes, schemas and pinned values. Names only this step uses are the implementer's.
- **Done when** (fixed): each done-criterion, with the behavior its test should check and the command that proves it.
- **Approach** (a starting point): the plan's approach, the research pitfalls and spike results (`spikes.md`) that apply, the existing code to reuse or follow, by path, and the files you expect it to touch.
- **Constraints** (fixed): the Design, Quality bar, Decisions and lessons that bear on this step, a line each, and the plan sections to read if more is needed.
- **Out of scope** (fixed): what neighbouring steps own, and anything the implementer might be tempted to change but mustn't.
- **Settled:** the ambiguities you settled while writing the brief, and how.
- **Commands:** the scoped commands for iterating, the checks config path, and the baseline (the checks that already failed before this step).

If writing the brief shows that the step can't be built as planned, that's a ruling if it stays within the step, and a question otherwise.

## 3. Implement

Launch `waterfall:implementer` with the brief path and the scope (working tree vs `HEAD`), with `model: "opus"` when the step names Opus. Keep its ID. It reports one of:

- **NEEDS_CONTEXT:** answer from the plan or the code, add the answer to the brief's Settled section, and SendMessage it to the implementer, which resumes it. An answer that would change the plan is a question.
- **BLOCKED:** give it what it needs: an answer, the work split into smaller pieces, or an escalation (below). If the step can't be built as planned, it's a question.
- **DONE_WITH_CONCERNS:** settle what you can by reading the code, and pass the rest to the reviewer.
- **DONE:** run `checks.py`. It should print a stored result; if it starts a run, the tree changed after the implementer's run, so find out what changed. Send failures beyond the baseline back.

The implementer's **Choices** (departures from the brief's Approach, files beyond it) are its to make while the fixed parts of the brief hold.

**Escalate** to a fresh implementer with `model: "opus"` when the implementer can't make the step work and the brief isn't the problem, when checks still fail after one send-back, or when a finding stays open after round 2 because its fixes keep failing. Give it the brief, the scope and what was tried; the work stays in the tree.

## 4. Review

Take the fingerprint. Launch `waterfall:reviewer` with the plan path, the brief path, the scope and changed files, the review tier, the implementer's Choices and unsettled Concerns, the checks result (the RESULT line, plus the output of failures beyond the baseline), and the report file `.claude/plans/<feature>/step-<n>-review.md`. Keep its ID. When it returns, compare the fingerprint; if the tree changed, undo only the reviewer's changes and log it.

**Light tier:** skim the diff first. If the step changes logic, review it as full and log that. Otherwise launch the reviewer with `model: "sonnet"` and allow 1 fix round. If it reports `NEEDS FULL REVIEW`, launch a fresh reviewer at full tier. You may raise a tier yourself; lowering one is a question.

Then loop, for at most 5 rounds. Before each round, count the `## Orchestrator rulings (round <k>)` sections in the report file, so the limit holds after your context is compacted.

1. If the verdict is APPROVE, the loop ends. Send any if-minor findings worth fixing (item 4) to the implementer in one batch, then read the fix and confirm `checks.py` yourself; they don't go back to the reviewer.
2. Answer the reviewer's Questions by reading the code, and add confirmed ones to the report file as findings.
3. Send blocking findings that are `traced` and not yet validated to a `waterfall:validator`, with the plan path, report file, round and finding numbers. Confirmed ones stay blocking, downgraded ones become if-minor or accepted risks, and rejected ones close.
4. **Rule on what's left.** For each open blocking finding, decide: fix, or defer with a reason judged against the Quality bar. Add an if-minor finding only if its fix is small and leaves the code simpler or clearer. Append your rulings to the report file under `## Orchestrator rulings (round <k>)`. If nothing is left to fix, stop.
5. Send the round, the report file and the finding numbers to fix to the step's implementer with SendMessage, or to a fresh one (below). Rule on any it reports `not fixed`, in the report file.
6. Run `checks.py`.
7. SendMessage the reviewer the round and the checks result, and ask it to re-review from the file.

**Fresh implementers.** A continued implementer re-reads its whole context every turn. Launch a fresh `waterfall:implementer` for a fix round from round 3 on, when the last one's completion notice showed more than about 120k tokens, or when the fixes are in code another implementer wrote. Give it the brief path, the review file and round, and the finding numbers, and say that the step is already built in the working tree.

**Settling.** Settle a finding yourself as soon as a round passes with no new evidence, and after round 5 settle whatever is still open. Treat unproven new findings on code the fixes didn't touch as out of scope. Log each settled dispute in your batch log, and in the plan's Decisions if it affects later steps.

**Out of scope and escapes.** Out-of-scope items go to the plan's Follow-ups. A problem an earlier step introduced is an escape: log it against that step. If that step is in an earlier batch, its branch is pushed, so fix the problem forward in this step if it's small and in this step's area, or add it to Follow-ups for the final review.

## 5. Conformance

Read the review's Conformance section and `git diff --stat`. A changed file the brief didn't expect is fine when the implementer's Choices explain it. Read diff hunks only where something looks off: an unexplained file, a contract that differs from the brief, an unmet or unclear criterion, or a change that reaches into another step's area. Send problems to the implementer and its fix to the reviewer, for at most 5 rounds.

## 6. Hand-off

Confirm `checks.py` shows a PASS, or only baseline failures, for the final tree.

- **Commit mode:** commit on the step's branch (`git.md`).
- **Review mode:** save a hand-off snapshot (`git.md`), run `change-summary`, and send its sections to the main orchestrator as a question (`QUESTION B<b>-Q<n>: step <n> is ready for you to review and commit`), with disputes and new follow-ups. Wait for its answer that the user has committed.

Tick the step in the plan, and append its Record to your batch log: commit or hand-off SHA; tier as run; rounds; blocking findings by gate and ruling (fixed, deferred, settled, or rejected or downgraded by the validator); if-minor applied and skipped; mutations killed and survived; implementers used (fresh or escalated, and why); deviations and rulings.

With `Checkpoints: each step` in commit mode, stop at a step checkpoint now. After the batch's last step, go to the batch review (`batch-review.md`).
