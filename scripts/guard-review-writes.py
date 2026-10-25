#!/usr/bin/env python3
"""PreToolUse hook that keeps Waterfall reviewers from editing the user's tree.

Every Waterfall agent except the implementer (the reviewers and the validator)
may write only inside a snapshot worktree made by tree.sh (a path containing
/waterfall-review.) or under .claude/plans/, where report files live. Other
agents pass through unchecked. Exit code 2 blocks the tool call and shows the
message to the agent.
"""
import json
import os
import sys

event = json.load(sys.stdin)
agent = event.get("agent_type") or ""
if not agent.startswith("waterfall:") or agent == "waterfall:implementer":
    sys.exit(0)

tool_input = event.get("tool_input") or {}
path = os.path.normpath(tool_input.get("file_path") or tool_input.get("notebook_path") or "")
if "/waterfall-review." in path or "/.claude/plans/" in path:
    sys.exit(0)

print(
    f"Waterfall reviewers must not edit the user's tree ({path}). "
    "Make experiments in a snapshot worktree from scripts/tree.sh instead.",
    file=sys.stderr,
)
sys.exit(2)
