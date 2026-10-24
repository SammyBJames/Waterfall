# Phase 0: setup and plan

## Setup

1. **Repo state.** Run `git status --porcelain`, `git branch --show-current` and `git log --oneline -5`. If the tree isn't clean, ask the user whether to commit, stash or include the changes; never stash or discard them yourself.
2. **Trunk.** `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`, or `git symbolic-ref --short refs/remotes/origin/HEAD`. If the user is on another branch, ask whether to stack on it or on trunk.
3. **Hide plans.** Make sure `.claude/plans/` is in `$(git rev-parse --git-common-dir)/info/exclude`. Don't edit `.gitignore`.
4. **Check commands.** Find the build, typecheck, lint, format-check and test commands, preferring what CI runs (`.github/workflows/`), then `CLAUDE.md`, `CONTRIBUTING.md` and the build files. Note any that need Docker or devices. Record each in a quiet form that prints failures but not passes (`cargo test -q`, `pytest -q`, `vitest run --reporter=dot`); every agent runs them as recorded.
5. **Baseline.** Run them once and record the failures that already exist.
6. **Tools.** If commit mode is possible, check that `gh stack --version` works.

## Study and ask

Read what the task touches: requirements, design docs, API spec, the relevant modules and tests, and recent history on those paths. Use Explore agents for wide searches and keep only their conclusions.

Ask with AskUserQuestion about each decision with a real trade-off that the code and requirements don't settle: data model, API shape, scope, dependency or custom code, migrations, UX. Recommend an option and give each option's cost. Decide conventional defaults yourself and log them.

Draft the **Quality bar** and ask about anything the project doesn't settle. Set it honestly: reviewers hold the code to it, and a local single-user tool doesn't need a public service's defenses.

Also ask for the **commit mode**: Claude commits each step on its own `gh stack` branch, or the user reviews, commits and creates branches. In commit mode, propose **branch names** that follow the repo's pattern (`git branch -a`), or `<feature>/<nn>-<step-slug>`.

## Write the plan

Write `.claude/plans/<feature>.md` from `plan-template.md`, where `<feature>` is a short slug. Each step:

- is reviewable in about 10 minutes and makes sense as one PR in a stack;
- leaves every check green without depending on a later step;
- builds on the previous one, foundations first (schema and core logic, then API, then UI);
- includes its own tests, docs and spec updates;
- has done-criteria that each name the test (by the behavior it checks) or command that proves it.

Give each step a **review tier**. **Light** is for steps with no new or changed logic: docs, comments, config values, renames and moves, behavior-preserving mechanical refactors, test-only changes, generated code. **Full** is for everything else, and always for security, persistence, concurrency, migrations and public APIs. When unsure, choose full. Keep light work in its own steps where that's natural.

Show the user a short summary and the file path. Revise until they explicitly approve, then set `Status: approved (<date>)`, and set it to `in progress` when Phase 1 starts.
