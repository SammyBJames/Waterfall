# Phase 0: setup and plan

## Setup

1. **Repo state.** Run `git status --porcelain`, `git branch --show-current` and `git log --oneline -5`. If the tree isn't clean, ask the user whether to commit, stash or include the changes; don't stash or discard them yourself.
2. **Trunk.** `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`, or `git symbolic-ref --short refs/remotes/origin/HEAD`. If the user is on another branch, ask whether to stack on it or on trunk.
3. **Hide plans.** Make sure `.claude/plans/` is in `$(git rev-parse --git-common-dir)/info/exclude`. Don't edit `.gitignore`.
4. **Lessons.** Run `"${CLAUDE_PLUGIN_ROOT}/scripts/tree.sh" shared` and read `lessons.md` in the directory it prints, if it exists. Apply it throughout planning, and record its path in the plan.
5. **Checks.** Find the build, typecheck, lint, format-check and test commands, preferring what CI runs (`.github/workflows/`), then `CLAUDE.md`, `CONTRIBUTING.md`, the build files and the lessons file. Write them to `.claude/plans/<feature>/checks.json` (the header of `checks.py` documents the format):
   - Use quiet forms that print failures but not passes (`cargo test -q`, `pytest -q`, `vitest run --reporter=dot`).
   - Put checks that share a toolchain or build directory in one **group**, in the order they should run. Separate groups run in parallel.
   - Include checks that need Docker or devices only if they can run here, and say in the plan which ones only CI runs.
   - The checks run on uncommitted work, so a check that compares against the index or `HEAD` (regenerate a file, then `git diff --exit-code`) fails on correct changes. Rewrite it to compare fresh output with the working-tree file (generate to a temporary file and `diff` the two), and note the rewrite in the plan.
   - Record **scoped commands** for iterating: one package's tests, one test file or filter, one package's lint.
6. **Baseline.** Run `"${CLAUDE_PLUGIN_ROOT}/scripts/checks.py" .claude/plans/<feature>/checks.json` (again while it exits 3) and record the failures that already exist.
7. **Tools.** If commit mode is possible, check that `gh stack --version` works.
8. **PRs.** Find the GitHub remote (`git remote -v`) and check `gh auth status`. Without either, tell the user that each batch's PR titles and descriptions will be written to files instead. Note the repo's PR template if it has one (`.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE/`, `docs/pull_request_template.md`).

## Study and research

Read what the task touches: requirements, design docs, API spec, the relevant modules and tests, and recent history on those paths.

As soon as you can state the problem, launch `waterfall:researcher` with:

- the problem in a few sentences, and the sub-problems that aren't routine (this task's hard parts, such as concurrency or migrations), not the glue;
- the constraints you know: language, frameworks, existing dependencies, and a rough Quality bar;
- how deep to go: `quick` for a well-trodden problem, `standard` by default, `broad` only where the approach is genuinely open;
- the report file `.claude/plans/<feature>/research.md`.

Keep studying while it runs. When it returns, read its summary and the report sections you need. Each real alternative it found becomes an option in your questions to the user, with its cost and who uses it. If you choose against its recommendation, log why in Decisions.

## Ask, up front

Settle every decision you can now, so the batches never wait on one. Ask with AskUserQuestion in as few calls as possible, recommend an option, and give each option's cost. Decide conventional defaults yourself and log them.

- **While the researcher runs,** ask what doesn't depend on its findings: checkpoints, the Quality bar, scope, commit mode and branch names.
- **After it returns,** ask about each decision with a real trade-off that the code, requirements and research don't settle: approach, data model, API shape, dependency or custom code, migrations, UX.

The questions always include:

- **Quality bar:** draft it and ask about anything the project doesn't settle. Set it honestly: reviewers hold the code to it, and a local single-user tool doesn't need a public service's defenses.
- **Commit mode:** Claude commits each step on its own `gh stack` branch, or the user reviews, commits and creates branches. In commit mode, propose branch names that follow the repo's pattern (`git branch -a`), or `<feature>/<nn>-<step-slug>`.
- **Checkpoints:** `each step`, `each batch`, `plan` or `none` (`SKILL.md`, Checkpoints). Recommend `each batch` for a first run on a repo or a change with open design questions, and `plan` otherwise. `each step` suits a change the user wants to steer closely, at the cost of their time at every step.

## Write the plan

Write `.claude/plans/<feature>.md` from `plan-template.md`, where `<feature>` is a short slug. The plan states what each step delivers and why. Leave line-level detail to the step brief and internals to the implementer.

Each **step**:

- is reviewable in about 10 minutes and makes sense as one PR in a stack;
- leaves every check green without depending on a later step;
- builds on the previous one, foundations first (schema and core logic, then API, then UI);
- includes its own tests, docs and spec updates;
- names the files it creates or changes, and the interfaces it consumes and produces: exact names and signatures where earlier steps or existing code fix them, and the contract it must meet where they don't;
- has done-criteria that each name the test (by the behavior it checks) or command that proves it;
- has a **review tier**. Light is for steps with no new or changed logic: docs, comments, config values, renames and moves, mechanical refactors that preserve behavior, test-only changes, generated code. Full is for everything else, and always for security, persistence, concurrency, migrations and public APIs. When unsure, choose full, and keep light work in its own steps where that's natural;
- has an **implementer model**: Sonnet by default, Opus for a step that is hard to get right (subtle concurrency or state, an unfamiliar API, an intricate algorithm, a cross-module refactor). Escalating after a failed Sonnet attempt pays for the work twice.

Group consecutive steps into **batches**. Each batch gets its own specialist panel and draft PRs, and once its PRs exist Waterfall never rewrites it.

Put a batch boundary where stopping to review pays off: right after the steps that settle something later work builds on (a data model, a contract, a core algorithm, a risky approach), so a mistake there is caught before anything is stacked on it. Don't split where the work that follows can't be wrong in a way the review would catch. There is no target size: a batch is as many steps as it takes to reach the next such point, and a change with no such point has one batch. Each batch:

- merges to trunk on its own: checks green, nothing half-built that users can reach (keep it unwired or behind a flag), and migrations that later batches only add to;
- lands the contracts later batches build on (schemas, public APIs, data formats, config and flag names) already shaped for those later needs.

**Walking skeleton.** When the change spans layers or components that haven't worked together before (storage, API and UI, for example), make batch 1 the thinnest real end-to-end path through every layer, with the real wiring and minimal behavior, kept unwired from users or behind a flag. Every contract is then exercised and reviewed before later batches flesh it out. When the only question is whether the layers can connect at all, a prototyper's throwaway skeleton during planning answers it more cheaply.

**Assumptions.** List the plan's load-bearing assumptions: what the batches take for granted that, if wrong, would change a contract, the design or several steps. Each one ends up verified, or accepted with a **signpost** (the evidence a batch would show if it were failing) and a **hedge** (what the plan would do then).

## Review until confident

Launch `waterfall:plan-reviewer` with the plan path, the research report path, and the report file `.claude/plans/<feature>/plan-review.md`. Keep its ID. It reports findings, assumptions (each to settle by a spike, a question or acceptance) and a **confidence** score for each batch. Then loop:

1. **Spikes.** Give every `spike` assumption to a `waterfall:prototyper`, with the plan path, the assumptions' IDs and questions, and the report file `.claude/plans/<feature>/spikes.md`. Independent assumptions can go to several prototypers in parallel.
2. **Questions.** While the spikes run, decide minor `ask` assumptions yourself and ask the user the major ones together.
3. **Revise.** Change the plan for each finding and spike result, or rebut the finding with evidence. A change to a decision the user made goes to the user. Update the Assumptions section and each batch's confidence.
4. **Re-review.** Append your answers and changes under `## Orchestrator response (round <k>)` in the report file, and SendMessage the reviewer the round.

Stop when the reviewer says READY: no open blocking finding and every batch high. After 5 rounds, counted from the `## Orchestrator response (round <k>)` sections in the report file, settle what's still open yourself. Log the review in the plan's Plan review section.

## Approve

Summarize the plan in a few lines: the batches and their steps, the confidence in each and what raised it, the approach chosen from the research and what was rejected, what the plan review changed, and anything you settled over a dispute.

- **Checkpoints `each step`, `each batch` or `plan`:** show the user the summary and the file path, and revise until they explicitly approve. If a revision changes batches, steps or contracts, send the reviewer the changes as a new round first.
- **Checkpoints `none`:** the plan is approved when the reviewer says READY; tell the user the summary and that building has started. If the reviewer still says REVISE after round 5, or a batch is below high, show the user the plan and what is still open, and wait for them.

Then set `Status: approved (<date>, by user | by orchestrator)`, and set it to `in progress` when Phase 1 starts.
