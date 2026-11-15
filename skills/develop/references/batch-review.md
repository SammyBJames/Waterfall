# Batch review

You are the batch orchestrator. After the batch's last step is handed off, set the batch's status to `panel review`. The scope is `<batch-base>...<batch-top>`: the base is the previous batch's top branch, or the stack base for batch 1 (in review mode, the branches recorded in the plan). Take a tree fingerprint (`"${CLAUDE_PLUGIN_ROOT}/scripts/tree.sh" fingerprint`).

## 1. Launch the panel

Choose specialists by what the batch's diff touches; when in doubt, include one.

| Specialist | Run it when the batch… |
|---|---|
| `waterfall:correctness-reviewer` | always |
| `waterfall:simplicity-reviewer` | always |
| `waterfall:security-reviewer` | handles outside input, auth, sessions or secrets; builds paths, shell commands, queries or URLs; or crosses a sandbox or plugin boundary |
| `waterfall:reliability-reviewer` | writes persistent state, runs concurrent or background work, uses the network or IPC, or adds migrations |
| `waterfall:performance-reviewer` | touches queries, loops over growing data, hot request or render paths, or large payloads, at a scale where cost matters |
| `waterfall:tests-reviewer` | has two or more full-tier steps that work together, or tests added after the step reviews |
| `waterfall:design-reviewer` | adds modules, layers, public APIs or contracts that later batches depend on, or departs from the plan's design |

Log skipped specialists and why. Launch the chosen ones in parallel, in one message, each with:

- the plan path, the batch number and the scope;
- each step's branch and commit, to tag findings;
- the `checks.py` result for the batch's top branch;
- the Follow-ups list and your batch log, whose known issues, rulings and deferred findings are settled and not to be re-reported;
- a report file, `.claude/plans/<feature>/batch-<b>-<specialist>.md`.

Keep their IDs, and check the fingerprint when they finish.

## 2. Validate

1. Merge findings that share a root cause, noting every specialist that raised them.
2. Send `traced` blocking findings to `waterfall:validator`s, one per report with its round and finding numbers, all in one message. Rejected ones close; downgraded ones become if-minor or accepted risks.
3. Rule on each remaining finding: valid, invalid (rebut with evidence) or deferred (say why). Check the evidence of proven and confirmed findings instead of re-deriving it. Apply an if-minor finding only when its fix is small and leaves the code simpler.
4. Log each valid blocking finding in your batch log as an escape of the step that introduced it, noting whether it was within that step's review tier.
5. Decide which Follow-ups belong in this batch; any that change the plan are questions.

## 3. Fix

Put each fix on the batch branch that introduced the problem, lowest branch first (`git.md`, Fixing a branch in the current batch). A cross-cutting fix goes on the lowest branch where it fits. A problem from an earlier batch is fixed forward on this batch's lowest fitting branch, never on the earlier batch's branch, and logged.

Make small fixes yourself. Give larger ones to a fresh `waterfall:implementer`, with `model: "opus"` when a fix spans several steps or modules. An implementer never switches branches, so check the branch out yourself and give it one fix task for that branch: the plan path, the briefs of the steps the fixes touch, the checks config and baseline, and each report path with its finding numbers. Commit and restack before the next branch.

Every bug fix gets a regression test, and fixes follow the comment rules in the `comment-cleanup` skill. Run `checks.py` on each branch you change, and on the batch's top branch after the restack.

## 4. Re-review

For each specialist with open findings, append your answers to its report file under `## Orchestrator response (round <k>)` as `F<n>: fixed (branch and commit) | rebutted (evidence) | deferred (why)`, then SendMessage it the round. Repeat validate → fix → re-review for at most 5 rounds, counted from those sections in the report files, not from memory. Settle a finding as soon as a round passes with no new evidence, and settle the rest after round 5. Log each settled dispute in the plan's Decisions.

If the fixes added code, SendMessage the simplicity reviewer the fix commits (the diff, in review mode) to check that each is the smallest fix for its finding, then run one validate → fix round on what it reports.

## 5. Docs and specs

Bring the README, design docs, requirements status and API spec in line with what the batch built, each update on the branch whose step introduced the behavior. Run `checks.py` on the batch's top branch.

## 6. Draft PRs and report

If an open question in the plan concerns these PRs, finish with `WAITING`. Otherwise open the batch's draft PRs (`draft-prs.md`), set the batch's status to `drafts open`, fill in the batch's PRs and a one-line Record in the plan (specialists run, blocking findings and how they ended), and send the main orchestrator your report.
