# Git and stacking

**Never** push, run `gh stack submit`, `gh stack push` or `gh stack merge`, force-push, or delete branches. Never stash, reset or discard the user's changes without asking. The plan file is excluded from git, so it is never staged.

## Commit mode (Claude commits, one `gh stack` branch per step)

**Commit messages** are one line in the repository's style. Check `git log --format=%s -30` once and match its tense, capitalization, prefixes and length.

**Before staging,** run `git status --porcelain`. Every path should be one this step meant to change. Look into anything unexpected (build output, scratch files, editor files) instead of committing it.

- **Step 1:** before the implementer starts, with a clean tree on the stack base, run `gh stack init --base <stack-base> <branch-1>`. After the hand-off checks pass:
  ```bash
  git add -A && git commit -m "<message>"
  ```
- **Steps 2 and later:** implement on top of the previous step's branch. After the checks pass, create the next branch and commit in one go:
  ```bash
  gh stack add -Am "<message>" <branch-n>
  ```
- **Check:** `gh stack view --short` shows each step on its own branch, in order.

**Fixing an earlier branch** (final review):

1. With a clean tree, `git checkout <branch>`. Make the fix and run the checks.
2. Commit it on that branch with a one-line message.
3. Run `gh stack rebase --upstack` to carry the fix up the stack.
4. If there are conflicts, resolve them so that both sides' intent is kept, run `git add`, then `gh stack rebase --continue`. If a conflict needs a judgment call, run `gh stack rebase --abort` and ask the user.
5. When you're done, `gh stack top`, then run the checks on the top branch.

Fix the lowest affected branch first, so each rebase carries the earlier fixes upward.

## Review mode (the user reviews, commits and creates branches)

You never commit or create branches. Before the hand-off, record a **hand-off snapshot** so you can see later whether the user changed anything before committing:

```bash
repo=$(git rev-parse --show-toplevel); idx=$(mktemp)
cp "$(git -C "$repo" rev-parse --git-path index)" "$idx"
GIT_INDEX_FILE=$idx git -C "$repo" add -A
GIT_INDEX_FILE=$idx git -C "$repo" commit-tree "$(GIT_INDEX_FILE=$idx git -C "$repo" write-tree)" -p HEAD -m "devflow hand-off"; rm "$idx"
```

Save the printed SHA in the step's **Record** line.

**Before the next step,** check all of these:

- the working tree is clean;
- `HEAD` has moved past the commit the step started from;
- the current branch is not trunk, and is not the previous step's branch.

If any check fails, ask the user instead of guessing. Run `git diff <hand-off-sha> HEAD` and read any edits the user made. Record the branch and commit in the plan.

**Final-review fixes:** group them by the branch that introduced each problem, lowest branch first. For each branch, ask the user to check it out (or ask permission to check it out yourself). Make the fixes uncommitted, then hand over a `change-summary`. Wait for the user to commit and restack before you move to the next branch.
