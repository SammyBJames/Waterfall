# Phase 0: setup and plan

## Setup

1. **Repo state.** Run `git status --porcelain`, `git branch --show-current` and `git log --oneline -5`. If the working tree isn't clean, ask the user how to handle it (commit, stash, or include it) before you go further. Never stash or discard their changes yourself.
2. **Trunk.** Use `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`, or `git symbolic-ref --short refs/remotes/origin/HEAD` as a fallback. If the user is on a branch other than trunk, ask whether to stack the work on top of that branch or on trunk.
3. **Hide plans from git.** Make sure `.claude/plans/` is listed in `$(git rev-parse --git-common-dir)/info/exclude`, and append it if not. Don't edit `.gitignore`.
4. **Check commands.** Find the build, typecheck, lint, format-check and test commands. Look first in the CI workflows (`.github/workflows/`), since they show what has to pass. Then check `CLAUDE.md`, `CONTRIBUTING.md`, `package.json` scripts, `Cargo.toml` and workspace layout, `Makefile` or `justfile`, `pyproject.toml`, and Gradle tasks. Prefer the commands CI runs. Note any that need Docker or devices.
5. **Baseline.** Run the commands once and record any failures that already exist, so no step gets blamed for them.
6. **Tools.** If the user might pick commit mode, check that `gh stack --version` works.

## Study the project

Read what the task touches: `CLAUDE.md`, `CONTRIBUTING.md`, the requirements, design docs and API spec, the relevant modules, their tests, and recent history (`git log` on those paths). For wide searches, use Explore agents and keep only their conclusions. Work out the current design before proposing a new one.

## Ask before you plan

Use AskUserQuestion for each decision that has a real trade-off or that the code and requirements don't settle: data model, API shape, the boundaries of the change, a new dependency versus custom code, migration strategy, and UX behavior. Put your recommendation first and explain each option's cost. Don't ask about things that have a conventional default; decide those, and list them as decisions in the plan.

Also ask:

- **Commit mode:** Claude commits (stacked branches via `gh stack`, one branch per step) or review mode (the user reviews, commits and creates branches).
- **Branch names** (commit mode): follow the repo's existing branch names if there's a pattern (`git branch -a`). Otherwise use `<feature>/<nn>-<step-slug>`. List the names in the plan for approval.

## Write the plan

Write `.claude/plans/<feature-slug>.md` from `plan-template.md`. Good steps:

- are small enough to review in about 10 minutes, and make sense as a single PR in a stack;
- leave the project building with all checks green (a step must never depend on a later one to compile or pass);
- are ordered so each builds on the last, foundations first: schema and core logic, then API, then UI;
- include their own tests, doc updates and spec updates, not a separate "docs" or "tests" step at the end;
- have done-criteria someone else could check.

Show the user the plan: a short summary in chat plus the path to the file. Revise until they explicitly approve. Then set `Status: approved`, record the date, and start Phase 1. Every later change to the plan needs the user's approval again.
