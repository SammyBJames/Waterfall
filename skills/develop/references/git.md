# Git and stacking

Never push, force-push, delete branches, or run `gh stack submit`, `gh stack push` or `gh stack merge`. Never stash, reset or discard the user's changes without asking.

## Commit mode (one `gh stack` branch per step)

**Commit messages** are one line in the repository's style: check `git log --format=%s -30` once and match its tense, capitalization, prefixes and length.

**Before committing,** run `git status --porcelain` and confirm every path belongs to this step. Investigate anything unexpected (build output, scratch or editor files) instead of committing it.

- **Step 1:** before the implementer starts, on a clean stack base, run `gh stack init --base <stack-base> <branch-1>`. At hand-off: `git add -A && git commit -m "<message>"`.
- **Later steps:** implement on top of the previous step's branch. At hand-off, create the branch and commit in one go: `gh stack add -Am "<message>" <branch-n>`.
- `gh stack view --short` should show each step on its own branch, in order.

**Fixing an earlier branch** (final review), lowest affected branch first:

1. With a clean tree, `git checkout <branch>`, make the fix, run the checks, and commit with a one-line message.
2. Run `gh stack rebase --upstack`. Resolve conflicts so both sides' intent is kept, `git add`, then `gh stack rebase --continue`. If a conflict needs a judgment call, `gh stack rebase --abort` and ask the user.
3. When done, `gh stack top` and run the checks on the top branch.

## Review mode (the user reviews, commits and creates branches)

You never commit or create branches. At hand-off, run `"${CLAUDE_PLUGIN_ROOT}/scripts/tree.sh" snapshot`, which commits the working tree without touching the index or any branch, and save the SHA in the step's Record.

**Before the next step,** check that the tree is clean, `HEAD` has moved past the step's starting commit, and the current branch is neither trunk nor the previous step's branch. If any check fails, ask the user. Read the user's edits with `git diff <hand-off-sha> HEAD`, and record the branch and commit in the plan.

**Final-review fixes:** group them by the branch that introduced each problem, lowest first. For each branch, ask the user to check it out (or for permission to do it yourself), make the fixes uncommitted, and hand over a `change-summary`. Wait for the user to commit and restack before moving on.
