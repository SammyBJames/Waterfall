# Phase 2: final review

Set the plan's status to `final review`. The scope is `<stack-base>...HEAD`, from the top of the stack. Take a tree fingerprint (`"${CLAUDE_PLUGIN_ROOT}/scripts/tree.sh" fingerprint`).

## 1. Launch the panel

Choose specialists by what the diff touches; when in doubt, include one.

| Specialist | Run it when the change… |
|---|---|
| `waterfall:correctness-reviewer` | always |
| `waterfall:simplicity-reviewer` | always |
| `waterfall:security-reviewer` | handles outside input, auth, sessions or secrets; builds paths, shell commands, queries or URLs; or crosses a sandbox or plugin boundary |
| `waterfall:reliability-reviewer` | writes persistent state, runs concurrent or background work, uses the network or IPC, or adds migrations |
| `waterfall:performance-reviewer` | touches queries, loops over growing data, hot request or render paths, or large payloads, at a scale where cost matters |
| `waterfall:tests-reviewer` | has two or more full-tier steps that work together, or tests added after the step reviews |
| `waterfall:design-reviewer` | adds modules, layers or public APIs, or departs from the plan's design |

Log skipped specialists and why in the plan. Launch the chosen ones in parallel, in one message, each with the plan path, the scope, each step's branch and commit (to tag findings), the Follow-ups list (known issues, not to be re-reported), and a report file `.claude/plans/<feature>/final-<specialist>.md`. Keep their IDs, and check the fingerprint when they finish.

## 2. Validate

1. Merge findings that share a root cause, noting every specialist that raised them.
2. Send `traced` blocking findings to validators, one per report with its round and finding numbers, all in one message. Rejected ones close; downgraded ones become if-minor or accepted risks.
3. Mark each remaining finding valid, invalid (rebut with evidence) or deferred (say why). Check proven and confirmed findings' evidence rather than re-deriving it. Apply if-minor findings only when small and simplifying.
4. Log each valid blocking finding as an escape in the Record of the step that introduced it, noting whether it was within that step's tier.
5. Decide which Follow-ups belong in this change; any that change the plan need the user's approval.

## 3. Fix

Make small fixes yourself. Give larger ones to a `waterfall:implementer` as a fix task: the plan path and each report path with its finding numbers, launched with `model: "opus"` when a fix spans several steps or modules. Put each fix on the branch that introduced the problem, lowest branch first (`git.md`); a cross-cutting fix goes on the lowest branch where it fits. Every bug fix gets a regression test. Run the checks on each branch you touch and on the top branch.

## 4. Re-review

For each specialist with open findings, append your answers to its report file under `## Orchestrator response (round <k>)` as `F<n>: fixed (branch and commit) | rebutted (evidence) | deferred (why)`, then SendMessage it the round. Don't message specialists with nothing open. Repeat validate → fix → re-review for at most 3 rounds. Settle a finding as soon as a round passes with no new evidence, settle the rest after round 3, and log each settled dispute in the plan and the final overview.

If the fixes added code, SendMessage the simplicity reviewer the fixes (the commits, or the diff in review mode) to check that each is the smallest fix for its finding, then run one validate → fix round on what it reports.

## 5. Docs and specs

Bring the README, design docs, requirements status and API spec in line with what was built, each update on the branch whose step introduced the behavior. Then do the Finish phase in `SKILL.md`.
