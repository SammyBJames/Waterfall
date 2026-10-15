# Phase 1: the step loop

Do the steps in order. Update the plan file after every stage below.

**Tree fingerprint.** This is a hash of the whole working tree (tracked, staged and untracked, but not ignored files). It doesn't touch the index. Use it to confirm a reviewer left the tree alone.

```bash
repo=$(git rev-parse --show-toplevel); idx=$(mktemp)
cp "$(git -C "$repo" rev-parse --git-path index)" "$idx"
GIT_INDEX_FILE=$idx git -C "$repo" add -A && GIT_INDEX_FILE=$idx git -C "$repo" write-tree; rm "$idx"
```

## 1. Prepare

- **Commit mode:** check that you're on the right branch (see `git.md`) and the tree is clean.
- **Review mode:** check that the user has finished with the previous step (see `git.md`). If they edited the code before committing, read their changes and adjust your picture of the code before you continue.

## 2. Implement

Launch `devflow:implementer`. Tell it:

- the plan path and the step number;
- the diff scope (working tree vs `HEAD`);
- any notes carried over from earlier steps.

Keep its agent ID.

- **BLOCKED:** read its report and form a recommendation. Present the options to the user and update the plan once they approve. Then continue the implementer with SendMessage, or start a fresh one if the step changed a lot.
- **DONE:** run every check command yourself and compare with the baseline. If anything fails, send it back to the implementer.

## 3. Review

Take the tree fingerprint. Launch `devflow:reviewer` with:

- the plan path and the step number;
- the scope: working tree vs `HEAD`, and the files the implementer changed.

Keep its agent ID. When it returns, take the fingerprint again. If the fingerprint changed, the reviewer touched the user's tree. Use `git status` and `git diff` to find and undo only its changes, and tell the user.

Then loop, for **at most 3 rounds**:

1. If the verdict is APPROVE and no Low findings are open, stop.
2. Answer the reviewer's **Questions** yourself (read the code or ask the implementer). Turn any that are confirmed into findings.
3. Send every open finding to the implementer with SendMessage, with Nits marked optional. It replies fixed, rebutted or deferred for each one.
4. Run the checks yourself.
5. Send the implementer's reply to the reviewer with SendMessage. It reports each finding as resolved, withdrawn or still open, plus any new findings and a new verdict.

After 3 rounds, settle any finding that is still open yourself, based on the evidence. Check it yourself if you need to. Record each decision in the plan's decisions log as a dispute, and flag it to the user at hand-off.

Out-of-scope items from either agent go into the plan's **Follow-ups**.

## 4. Conformance check (you)

Read the step's full diff yourself and check it against:

- the plan step's goal, done-criteria, tests and docs or spec updates;
- the design and the decisions log;
- the requirements and API spec;
- the project's standards (`CLAUDE.md`, `CONTRIBUTING.md`, the conventions in nearby code).

If anything doesn't conform, send the problems to the implementer. When it's done, send the fix to the reviewer for a check. This uses the same round limit, counted separately.

## 5. Comment cleanup

Run the `comment-cleanup` skill on the working tree vs `HEAD`. Then run the checks again and confirm the diff since cleanup touches only comments.

## 6. Hand-off

- **Commit mode:** commit the step on its stack branch (see `git.md`). Then tell the user in two or three lines what the step did, its branch and commit, and any disputes you settled or follow-ups you added.
- **Review mode:** save a hand-off snapshot SHA (see `git.md`) in the plan. Run the `change-summary` skill and send the user its three sections (How it works, PR description, Commit message), plus disputes you settled and new follow-ups. Then **wait** for the user to say they've committed before you start the next step.

Tick the step's checkbox and fill in its **Record** line in the plan.
