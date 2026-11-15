#!/usr/bin/env python3
"""PreToolUse hook that keeps Waterfall's reviewing agents from editing the user's tree.

Every Waterfall agent except the implementer and the batch orchestrator (the
reviewers, the validator, the researcher, the plan reviewer and the prototyper)
may write only inside a review worktree made by tree.sh (under the Waterfall
cache) or under .claude/plans/, where report files live. Other agents, including
any these agents spawn, pass through unchecked. Exit code 2 blocks the tool call
and shows the message to the agent.
"""
import json
import os
import sys

WRITERS = {"waterfall:implementer", "waterfall:batch-orchestrator"}

event = json.load(sys.stdin)
agent = event.get("agent_type") or ""
if not agent.startswith("waterfall:") or agent in WRITERS:
    sys.exit(0)

cache = os.environ.get("WATERFALL_CACHE") or os.path.join(
    os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "waterfall")
cache = os.path.normpath(cache) + os.sep
tool_input = event.get("tool_input") or {}
path = os.path.normpath(tool_input.get("file_path") or tool_input.get("notebook_path") or "")
if path.startswith(cache) or "/.claude/plans/" in path:
    sys.exit(0)

print(
    f"Waterfall reviewing agents must not edit the user's tree ({path}). "
    "Experiment in a review worktree from `scripts/tree.sh worktree` instead.",
    file=sys.stderr,
)
sys.exit(2)
