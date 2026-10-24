# Phase 1: the step loop

Do the steps in order and update the plan after each stage. `"${CLAUDE_PLUGIN_ROOT}/scripts/tree.sh" fingerprint` hashes the working tree without touching the index; use it to confirm reviewers left the tree alone.

## 1. Prepare

- **Commit mode:** you're on the right branch with a clean tree (`git.md`).
- **Review mode:** the user has committed the previous step (`git.md`). If they edited the code first, read their changes.

## 2. Implement

Launch `devflow:implementer` with the plan path, step number, scope (working tree vs `HEAD`) and any notes from earlier steps. Keep its ID.

- **BLOCKED:** recommend an option, get the user's approval, update the plan, then continue the implementer, or start a fresh one if the step changed a lot.
- **DONE:** run the checks yourself and compare with the baseline. Send failures back.

**Escalate** to a fresh implementer launched with `model: "opus"` when the implementer can't make the step work (rather than the plan being wrong), when checks still fail after one send-back, or when a finding stays open after round 2 because its fixes keep failing. Give it the plan path, step, scope and a note on what was tried; the work stays in the tree. Log the escalation in the Record.

## 3. Review

Take the fingerprint. Launch `devflow:reviewer` with the plan path and step, the scope and changed files, the review tier, your check results (what passed, and the output of failures beyond the baseline), and the report file `.claude/plans/<feature>/step-<n>-review.md`. Keep its ID. When it returns, compare the fingerprint; if the tree changed, undo only the reviewer's changes and tell the user.

The reviewer, implementer and validator all append to the report file.

**Light tier:** skim `git diff --stat` and the diff first. If the step changes logic, review it as full and note that. Otherwise launch the reviewer with `model: "sonnet"` and allow 1 fix round. If it reports `NEEDS FULL REVIEW`, launch a fresh reviewer at full tier. You may raise a tier yourself; lowering one needs the user's approval.

Then loop, for at most 3 rounds:

1. If the verdict is APPROVE, stop.
2. Answer the reviewer's Questions yourself (read the code or ask the implementer), and add confirmed ones to the report file as findings.
3. Send blocking findings that are `traced` and not yet validated to a `devflow:validator`, with the plan path, report file, round and finding numbers. Confirmed ones stay blocking, downgraded ones become if-minor or accepted risks, and rejected ones close. If no blocking finding remains, stop.
4. SendMessage the implementer the round, the report file, and the findings to answer: every open blocking finding plus the if-minor ones you chose.
5. Run the checks.
6. SendMessage the reviewer the round and the check results, and ask it to re-review from the file.

**If-minor findings:** apply one only if the fix is small and leaves the code simpler or clearer. Batch them to the implementer, including after the loop stops, and check those fixes yourself; don't send them back to the reviewer.

**Settling:** settle a finding yourself as soon as a round passes with no new evidence from either side, and after round 3 settle whatever is still open. Treat unproven new findings on code the fixes didn't touch as out of scope. Log each settled dispute in the decisions table and flag it at hand-off.

Out-of-scope items go to **Follow-ups**. A problem that an earlier step introduced is an escape; log it in that step's Record.

## 4. Conformance

The reviewer has checked the step against its plan entry. Read its Conformance section and `git diff --stat`: every changed file should belong to this step. Read diff hunks only where something looks off, such as an unexpected file, an unmet or unclear criterion, a reported deviation, or design you know better than the reviewer. Also check what the reviewer can't see: decisions made with the user during this session. Send problems to the implementer and its fix to the reviewer, with a separate 3-round limit.

## 5. Comment cleanup

Run the `comment-cleanup` skill on the working tree vs `HEAD`, then the checks, and confirm its diff touches only comments.

## 6. Hand-off

- **Commit mode:** commit on the step's branch (`git.md`), then tell the user in two or three lines what the step did, its branch and commit, and any disputes or new follow-ups.
- **Review mode:** save a hand-off snapshot (`git.md`), run `change-summary`, and give the user its three sections verbatim, plus disputes and new follow-ups. Wait for the user to say they've committed.

Tick the step and fill in its Record.
