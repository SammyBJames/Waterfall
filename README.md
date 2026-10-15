# devflow

A Claude Code plugin for plan-first development with adversarial review.

1. **Plan.** `/devflow:develop <task>` studies the project, asks about the design decisions that matter, and writes a plan to `.claude/plans/<feature>.md`, which is excluded from git. The plan has the design, small steps that each keep the build green, and the check commands. Nothing is built until you approve it, and every later change to the plan needs your approval too.
2. **Each step.** The `implementer` builds the step, test-first where it makes sense. The `reviewer` attacks it for bugs, security, reliability, performance, design and simplicity, and dead code, and checks new tests with mutations in a throwaway snapshot worktree. They argue findings out with evidence for at most 3 rounds, then the orchestrator decides and flags the decision to you. The orchestrator then checks the step against the plan, requirements and standards, and runs `comment-cleanup`.
3. **Hand-off.** In commit mode, each step is committed on its own `gh stack` branch. In review mode, you get a `change-summary` (how it works, What Changed / What to Test, a commit message) and commit it yourself.
4. **Final review.** Six specialists review the whole change in parallel: correctness, security, reliability, performance, tests and design. Each fix goes on the branch that introduced the problem, then docs and specs are updated, comments get a final cleanup, and you get an overview of the final design.

Nothing is ever pushed. `gh stack submit` is yours to run.

## Commands

| Command | What it does |
|---|---|
| `/devflow:develop <task>` | Runs the full workflow. Rerun it in a new session to resume from the plan file. |
| `/devflow:review [base-ref] [--panel]` | Reviews the working tree or a branch, with one reviewer or the six-specialist panel. |
| `/devflow:comment-cleanup [base-ref \| files]` | Doc comment on every function, sparing inline comments, no history in comments. |
| `/devflow:change-summary [base-ref]` | How it works, PR description, and commit message. |

## Install

Requires the GitHub CLI with the [`gh stack`](https://gh.io/stacks) extension for commit mode (`gh extension install github/gh-stack`).

```bash
# From a clone; edits apply after /reload-plugins
claude plugin marketplace add ~/Repositories/Skills
# Or straight from GitHub, no clone needed
claude plugin marketplace add <owner>/<repo>

claude plugin install devflow@sam-skills
```

To update: `git pull`, or `claude plugin marketplace update sam-skills && claude plugin update devflow@sam-skills`.

## Layout

- `skills/develop/`: the orchestrator. `SKILL.md` gives the overview, and `references/` holds the planning, step loop, final review, git and plan template.
- `skills/review-standards/`: rules every reviewer loads (evidence, severity, snapshot worktree, mutation testing, report format), plus one checklist per review dimension in `references/`.
- `agents/`: `implementer`, the step `reviewer`, and six `*-reviewer` specialists.

Run `claude plugin validate .` after you make changes.
