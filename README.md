# Waterfall

A Claude Code plugin for plan-first development with skeptical, proportionate review.

1. **Plan.** `/waterfall:develop <task>` studies the project, asks about the design decisions that matter, and writes a plan to `.claude/plans/<feature>.md`, which is excluded from git. The plan has the design, a **Quality bar** (users, threat model, target scale, accepted risks) that every finding and fix is judged against, small steps that each keep the build green, each with a review tier and done-criteria that name the test or command proving them, and the check commands. Nothing is built until you approve it, and every later change to the plan needs your approval too.
2. **Each step.** The `implementer` (Sonnet, escalated to Opus when it struggles) builds the step, test-first where it makes sense, without over-engineering. The `reviewer` checks it for bugs, security, reliability, performance, design, unnecessary complexity and conformance to the plan. It mutation-checks new tests in a throwaway snapshot worktree, and reports only findings worth their fix. Light-tier steps (no logic changes) get a lighter, cheaper review. A finding blocks only if it passes one of five gates (failing checks, unmet contract, proven defect, in-model threat, bloat). Blocking findings that are traced but not proven go to an independent `validator` before anyone fixes them. The rest are argued out with evidence for at most 3 rounds, with no new goalposts in re-reviews. Then the orchestrator confirms conformance and runs `comment-cleanup`.
3. **Hand-off.** In commit mode, each step is committed on its own `gh stack` branch. In review mode, you get a `change-summary` (how it works, What Changed / What to Test, a commit message) and commit it yourself.
4. **Final review.** Specialists review the whole change in parallel. Correctness and simplicity always run; security, reliability, performance, tests and design run when the change touches their area. Each fix goes on the branch that introduced the problem, and the simplicity reviewer checks that the fixes stayed small. Then docs and specs are updated, comments get a final cleanup, and you get an overview of the final design.

Nothing is ever pushed. `gh stack submit` is yours to run.

## Commands

| Command | What it does |
|---|---|
| `/waterfall:develop <task>` | Runs the full workflow. Rerun it in a new session to resume from the plan file. |
| `/waterfall:review [base-ref] [--panel]` | Reviews the working tree or a branch, with one reviewer or the seven-specialist panel. |
| `/waterfall:comment-cleanup [base-ref \| files]` | Doc comment on every function, sparing inline comments, no history in comments. |
| `/waterfall:change-summary [base-ref]` | How it works, PR description, and commit message. |

## Install

Requires the GitHub CLI with the [`gh stack`](https://gh.io/stacks) extension for commit mode (`gh extension install github/gh-stack`), and `python3` for the hook that keeps reviewers out of your working tree.

```bash
# From a clone; edits apply after /reload-plugins
claude plugin marketplace add ~/Repositories/Skills
# Or straight from GitHub, no clone needed
claude plugin marketplace add <owner>/<repo>

claude plugin install waterfall@sam-skills
```

To update: `git pull`, or `claude plugin marketplace update sam-skills && claude plugin update waterfall@sam-skills`.

## Layout

- `skills/develop/`: the orchestrator. `SKILL.md` gives the overview, and `references/` holds the planning, step loop, final review, git and plan template.
- `skills/review-standards/`: rules every reviewer loads (evidence levels, weighing findings against the Quality bar, blocking gates, calibration examples, snapshot worktree, mutation testing, report format), plus one checklist per review dimension in `references/`, each with what not to report.
- `skills/comment-cleanup/`, `skills/change-summary/`: run in a forked Sonnet subagent.
- `agents/`: `implementer`, the step `reviewer`, the `validator`, and seven `*-reviewer` specialists.

Models follow Anthropic's guidance: Opus agents run at `medium` effort (Opus 5.5's default), and the Sonnet implementer and skills at `medium` (recommended for well-specified agentic coding). The orchestrator moves the implementer to Opus when a step proves hard.
- `scripts/tree.sh`: working-tree fingerprint, snapshot commit, and snapshot worktrees, all without touching your index.
- `hooks/hooks.json` and `scripts/guard-review-writes.py`: block reviewer and validator agents from editing anything outside their snapshot worktree and report files.

## Tuning

Each step's **Record** line in the plan logs its review tier, rounds, blocking findings by gate and outcome, if-minor findings applied and skipped, mutation results, model escalations, and escapes. Compare those across real tasks when you change the prompts:

- **Precision:** many findings rejected by the validator, rebutted or deferred mean the reviewers are too noisy.
- **Recall:** escapes (problems a later review found in an earlier step) mean the reviews are too lax, or the step's tier was too low.
- **Rounds:** many review rounds per step mean the implementer needs a stronger model or clearer steps.

Run `claude plugin validate .` after you make changes.
