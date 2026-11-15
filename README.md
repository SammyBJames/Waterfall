# Waterfall

A Claude Code plugin for plan-first development with skeptical, proportionate review.

1. **Plan.** `/waterfall:develop <task>` studies the project and its **lessons file** (what earlier Waterfall tasks in this repo learned), and a `researcher` looks for proven solutions to the problem, or to similar problems whose solutions can be adapted, so the design starts from a proven approach instead of a naive one. Claude asks every design decision up front and writes a plan to `.claude/plans/<feature>.md`, which is excluded from git. The plan has the design, a **Quality bar** (users, threat model, target scale, accepted risks) that every finding and fix is judged against, and small steps grouped into **batches**, split where stopping to review would catch a mistake before later work builds on it. A change that spans layers starts with a **walking skeleton**, the thinnest real path through every layer. A `plan-reviewer` then walks the plan step by step, lists its **load-bearing assumptions**, and scores its **confidence** in each batch. Assumptions that only running something can settle go to a `prototyper`, which runs throwaway **spikes**; ones it accepts get a signpost (the evidence that would show it failing) and a hedge. Review and spikes repeat until every batch is high-confidence.
2. **Each batch** runs in a `batch-orchestrator` with a fresh context, so long-finished steps don't fill the main session.
   - **Each step:** the batch orchestrator writes a **step brief** against the code as it stands. The brief fixes the step's intent, the exact contracts it consumes and produces, the tests that prove each done-criterion and what's out of scope, and suggests an approach. The `implementer` (Sonnet, or Opus for steps the plan marks hard) builds from the brief, test-first where it makes sense, without over-engineering. It chooses the internals itself, may take a better approach than the suggested one, and stops to ask rather than guess when the brief falls short. It iterates with scoped commands and runs the full check suite once at the end. The `reviewer` checks the step for bugs, security, reliability, performance, design, unnecessary complexity and conformance to the plan. It mutation-checks new tests and reports only findings worth their fix. Light-tier steps (no logic changes) get a lighter, cheaper review. A finding blocks only if it passes one of five gates (failing checks, unmet contract, proven defect, in-model threat, bloat). Blocking findings that are traced but not proven go to an independent `validator` before anyone fixes them, and the batch orchestrator rules on which to fix; the implementer fixes them rather than arguing. Review rounds are capped at 5, with no new goalposts in re-reviews, and large fix rounds go to a fresh implementer. In commit mode, each step is committed on its own `gh stack` branch; in review mode, you get a `change-summary` and commit it yourself.
   - **The batch panel:** specialists review the batch in parallel. Correctness and simplicity always run; security, reliability, performance, tests and design run when the batch touches their area. Each fix goes on the batch branch that introduced the problem. Then Claude pushes the batch and opens a **draft PR** for each branch, with a title and description written from the change, for you to review and mark ready yourself.
3. **Between batches,** the main session runs a **boundary review**: an after-action review (what was supposed to happen, what happened, why they differ, what to keep and change), a check of each assumption's signpost against what the batch found, a look at whether the remaining contracts still hold or a simpler path has opened up, and a pre-mortem on the next batch. It then keeps the plan, refines it, or re-plans (the `plan-reviewer` checks any re-plan), tells you the PRs and what changed, and adds what the batch taught it to the lessons file. The next batch orchestrator checks its own steps against the code as built before it starts.
4. **Final review.** With more than one batch, specialists review the whole change for what only shows across batches: requirements met only end to end, contracts used inconsistently, drift from the design. Since earlier PRs may already be in peer review, fixes go forward on a new branch at the top of the stack, with its own draft PR. You get an overview of the final design.

**You choose the checkpoints** up front: stop after **each step** or **each batch** for your review, approve the **plan** and let the batches run through, or **none**, where Claude approves its own plan once it's high-confidence and runs the whole change on its own. In every mode, only a **major change** (to the design, scope, Quality bar, dependencies, a contract already in PRs, or a decision you made) stops for you; Claude decides minor ones itself, logs them, and reports them.

**Questions don't stall the work.** Claude asks everything it can during planning. When a batch needs a major decision later, it sends the question to the main session, which notifies you and asks, while the batch carries on with whatever doesn't depend on the answer.

**Checks run once per tree.** `scripts/checks.py` runs the plan's check suite in parallel groups and stores the result by the working tree's content. The implementer runs it once per step; the orchestrators verify from the stored result, and reviewers never rerun the suite. Reviewers build and mutate in **pooled review worktrees** that keep their build output between uses, so their builds are incremental and never contend for your build directory.

Claude only pushes to open draft PRs, and never changes a branch once it's pushed. It never force-pushes, marks a PR ready or merges.

Waterfall is opinionated about size: reviewers are told to favour the least total custom code and the fewest dependencies, so expect findings that remove code as often as ones that add it.

## Commands

| Command | What it does |
|---|---|
| `/waterfall:develop <task>` | Runs the full workflow. Rerun it in a new session to resume from the plan file. |
| `/waterfall:review [base-ref] [--panel]` | Reviews the working tree or a branch, with one reviewer or the seven-specialist panel. |
| `/waterfall:comment-cleanup [base-ref \| files]` | Doc comment on every function, sparing inline comments, no history in comments. |
| `/waterfall:change-summary [base-ref \| base...head]` | How it works, PR title and description, and commit message. |

## Install

Requirements:

- macOS or Linux (on Windows, use WSL). The hook and helper scripts are shell and Python scripts.
- `git` 2.31 or later and `bash`, for the snapshot and worktree helpers.
- `python3`, for the check runner and the hook that keeps reviewers out of your working tree.
- For draft PRs: the GitHub CLI, signed in (`gh auth login`), and a GitHub remote. Without them, PR titles and descriptions are written to files instead.
- For commit mode: the [`gh stack`](https://gh.io/stacks) extension (`gh extension install github/gh-stack`).

```bash
# Straight from GitHub
claude plugin marketplace add SammyBJames/Waterfall
# Or from a local clone, to edit it (changes apply after /reload-plugins)
git clone https://github.com/SammyBJames/Waterfall.git
claude plugin marketplace add ./Waterfall

claude plugin install waterfall@waterfall
```

To update: `claude plugin marketplace update waterfall && claude plugin update waterfall@waterfall`, or `git pull` in a local clone.

## Layout

- `skills/develop/`: the main orchestrator. `SKILL.md` gives the overview, and `references/` holds planning, the plan template, lessons, the step loop, batch review, draft PRs, the batch-boundary re-plan, the final review and git.
- `skills/review-standards/`: rules every reviewer loads (evidence levels, weighing findings against the Quality bar, blocking gates, calibration examples, review worktrees, report format), plus one checklist per review dimension in `references/`, each with what not to report; the tests checklist holds the mutation-testing procedure.
- `skills/comment-cleanup/`, `skills/change-summary/`: run in a forked Sonnet subagent.
- `agents/`: the `researcher`, `plan-reviewer` and `prototyper` for planning; the `batch-orchestrator`; the `implementer`, the step `reviewer` and the `validator`; and seven `*-reviewer` specialists for the batch and final panels. Any of them may spawn subagents of its own.
- `scripts/tree.sh`: working-tree fingerprint, snapshot commit, pooled review worktrees, and the repo's shared directory for the lessons file, all without touching your index. Review worktrees live in `~/.cache/waterfall/<repo>/wt/` (or `$WATERFALL_CACHE`); `tree.sh clean` deletes them and their build output.
- `scripts/checks.py`: runs a plan's check suite once per working tree and caches the result in `~/.cache/waterfall/<repo>/checks/`.
- `hooks/hooks.json` and `scripts/guard-review-writes.py`: block every Waterfall agent except the implementer and batch orchestrator from editing anything outside its review worktree and report files. The hook can't tell which agent spawned a subagent, so it doesn't cover subagents those agents start; they're told to use read-only agents or pass on the same rules, and the orchestrator's tree fingerprint catches any edits.

Models: the main orchestrator, researcher and plan reviewer run on Fable at `high` effort, where planning judgment pays off most. The `develop` skill asks for Fable only for the turn it starts, so run `/model fable` first to keep the whole session on it. The batch orchestrator runs on Opus at `high`; the reviewers, validator and prototyper on Opus at `medium`; and the implementer and the `comment-cleanup` and `change-summary` skills on Sonnet at `medium`. The plan names Opus for hard steps, and the batch orchestrator escalates when a step proves hard.

## Tuning

Each step's **Record** in its batch log (`.claude/plans/<feature>/batch-<b>-log.md`) logs its review tier, rounds, blocking findings by gate and ruling, if-minor findings applied and skipped, mutation results, fresh and escalated implementers, and deviations. Each batch's boundary review (`boundary-<b>.md`) records what differed from the plan and why. Compare those across real tasks when you change the prompts:

- **Precision:** many findings rejected by the validator, rebutted or deferred mean the reviewers are too noisy.
- **Recall:** escapes (problems a later review found in an earlier step or batch) mean the reviews are too lax, or the step's tier was too low. Fixes forward for earlier batches mean the plan review missed a contract.
- **Rounds:** many review rounds per step mean the implementer needs a stronger model or clearer steps.
- **Plan confidence:** a boundary review that re-plans a batch rated high, or a failed assumption that had no signpost, means the plan review or spikes missed something.

Run `claude plugin validate .` after you make changes.

## License

[GPL-3.0-or-later](LICENSE). You may use, modify and share Waterfall; if you distribute a modified version, you must release its source under the same license.
