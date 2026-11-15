# Draft PRs

At the end of each batch, and for the final review's fix branch, open a draft PR for each new branch, in stack order, for the user to review and edit before they open it for peer review. Never mark a PR ready, request reviewers, or edit a PR the user has marked ready.

## 1. Write each PR

For each branch, run `change-summary` with the range `<parent>...<branch>`, where the parent is the branch below it in the stack (the stack base for the first branch). From its output:

- **Title:** its PR title.
- **Body:** its PR description. If the plan names a PR template, fill the template's sections from that description instead, and leave any checklist the author must tick unticked. End the body with one line placing the PR in the change: `Part <k> of <n>: <feature title>, batch <b> (<batch title>).` Don't link to the plan; it isn't in git.

Save each body to `.claude/plans/<feature>/pr-<step>.md` (`pr-final.md` for the final review's fix branch), and put the titles in the batch's PRs line in the plan.

## 2. Check the earlier branches

Run `git fetch <remote>`. Every branch below this batch whose PR isn't merged must match its remote branch (`git rev-parse <branch>` equals `git rev-parse <remote>/<branch>`). If one doesn't, stop and ask the user through the main orchestrator: pushing would overwrite their PR or push a rewrite of it.

## 3. Push and create

- **With `gh stack`** (commit mode, or review mode when `gh stack view` shows the user's branches): from the batch's top branch, run `gh stack submit --auto`. It pushes the stack and creates each new PR as a draft. Never pass `--open`. Then set each new PR's text: `gh pr edit <branch> --title "<title>" --body-file .claude/plans/<feature>/pr-<step>.md`.
- **Without it:** for each branch, lowest first, run `git push -u <remote> <branch>` (never with force; if the push is rejected, stop and ask), then `gh pr create --draft --base <parent> --head <branch> --title "<title>" --body-file .claude/plans/<feature>/pr-<step>.md`.

## 4. Verify

For each branch, `gh pr view <branch> --json number,url,isDraft,baseRefName,title`: it must be a draft on the right base, with the title you wrote. Record each number and URL in the batch's PRs line.

Without a GitHub remote or `gh` auth, skip steps 2–4 and give the user the PR files' paths instead.
