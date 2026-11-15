# Git and stacking

The only pushes are the ones that open draft PRs (`draft-prs.md`). Never force-push, merge, delete branches, mark a PR ready, or run `gh stack merge`, `gh stack push`, `gh stack sync` or `gh stack submit --open`. Once a branch is pushed, never change it again: problems in it are fixed forward on a branch above it. Never stash, reset or discard the user's changes without asking.

## Commit mode (one `gh stack` branch per step)

**Commit messages** are one line in the repository's style: check `git log --format=%s -30` once and match its tense, capitalization, prefixes and length.

**Before committing,** run `git status --porcelain` and confirm every path belongs to this step. Investigate anything unexpected (build output, scratch or editor files) instead of committing it.

- **Step 1:** before the implementer starts, on a clean stack base, run `gh stack init --base <stack-base> <branch-1>`. At hand-off: `git add -A && git commit -m "<message>"`.
- **Later steps,** including the first step of a later batch: implement on top of the previous step's branch. At hand-off, create the branch and commit in one go: `gh stack add -Am "<message>" <branch-n>`.
- `gh stack view --short` should show each step on its own branch, in order.

**Fixing a branch in the current batch** (batch review), lowest affected branch first. Only the current batch's branches, which haven't been pushed:

1. With a clean tree, `git checkout <branch>`, make the fix, run `checks.py`, and commit with a one-line message.
2. Run `gh stack rebase --upstack`. Resolve conflicts so both sides' intent is kept, `git add`, then `gh stack rebase --continue`. If a conflict needs a judgment call, `gh stack rebase --abort` and ask the user through the main orchestrator.
3. When done, `gh stack top` and run `checks.py` on the top branch.

**Fixing forward** (final review): `gh stack top`, make the fixes, run `checks.py`, then `gh stack add -Am "<message>" <fix-branch>`.

## Before a later batch

Before the batch's first step, run `git fetch <remote>` and `gh stack view --short` (in review mode, compare each earlier branch with its remote branch). If an earlier branch moved on the remote or a PR was merged, send the main orchestrator a question saying what changed and asking the user to bring the stack up to date (for example `gh stack sync`) before you build on it. Don't rebase it yourself: that rewrites branches that are already pushed, and only the user can push the result. Then run `checks.py` on the top branch.

## Review mode (the user reviews, commits and creates branches)

You never commit or create branches. At hand-off, run `"${CLAUDE_PLUGIN_ROOT}/scripts/tree.sh" snapshot`, which commits the working tree without touching the index or any branch, and save the SHA in the step's Record in your batch log.

**Before the next step,** check that the tree is clean, `HEAD` has moved past the step's starting commit, and the current branch is neither trunk nor the previous step's branch. If any check fails, ask the user through the main orchestrator. Read the user's edits with `git diff <hand-off-sha> HEAD`, and record the branch and commit in the plan.

**Batch-review fixes:** group them by the branch that introduced each problem, lowest first. For each branch, ask the user through the main orchestrator to check it out (or for permission to do it yourself), make the fixes uncommitted, and hand over a `change-summary`. Wait for the answer that they've committed and restacked before moving on.

**Final-review fixes:** ask the user through the main orchestrator to create the fix branch on top of the stack, make the fixes uncommitted, and hand over a `change-summary`. Wait for the answer that they've committed.

You still open the draft PRs for the user's branches at the end of each batch (`draft-prs.md`).
