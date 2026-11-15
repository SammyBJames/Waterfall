#!/usr/bin/env bash
# Snapshot and worktree helpers for Waterfall. They read the user's working
# tree (tracked, staged and untracked files, but not ignored ones) without
# touching its index, branches or stashes. Run them from anywhere inside the
# user's repo.
#
#   tree.sh fingerprint     print a hash of the working tree
#   tree.sh snapshot        print a commit of the working tree on top of HEAD
#   tree.sh worktree        check out a fresh snapshot in a pooled review worktree and print its path
#   tree.sh release <path>  give a review worktree back to the pool (alias: remove)
#   tree.sh shared          print the repo's shared Waterfall directory (lessons), creating it
#   tree.sh clean           delete this repo's idle review worktrees and their build output
#
# Review worktrees live in ${WATERFALL_CACHE:-~/.cache/waterfall}/<repo>/wt/<n>,
# outside the repo and off tmpfs. Each keeps its ignored build output (target/,
# node_modules/, .venv/) between uses, so builds there are incremental. A lock
# per worktree keeps two agents out of the same one. The first
# WATERFALL_REVIEW_SLOTS (default 4) are kept; extra ones made when all are busy
# are deleted on release.
set -euo pipefail

repo=$(git rev-parse --show-toplevel)
common=$(git -C "$repo" rev-parse --path-format=absolute --git-common-dir)
if [ "$(basename "$common")" = .git ]; then main=$(dirname "$common"); else main=$common; fi
root=${WATERFALL_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/waterfall}/$(basename "$main")-$(printf %s "$common" | { sha1sum 2>/dev/null || shasum; } | cut -c1-8)
pool=$root/wt
slots=${WATERFALL_REVIEW_SLOTS:-4}
stale_minutes=360

# Prints the tree hash of the working tree, built in a throwaway copy of the index.
write_tree() {
  local idx tree
  idx=$(mktemp)
  cp "$(git -C "$repo" rev-parse --path-format=absolute --git-path index)" "$idx"
  GIT_INDEX_FILE=$idx git -C "$repo" add -A
  tree=$(GIT_INDEX_FILE=$idx git -C "$repo" write-tree)
  rm -f "$idx"
  echo "$tree"
}

# Prints a commit of the working tree whose parent is HEAD.
snapshot() {
  git -C "$repo" commit-tree "$(write_tree)" -p HEAD -m "Waterfall snapshot"
}

# Takes the lock for pool slot $1, clearing it first if its holder has been gone for hours.
lock() {
  local l=$pool/$1.lock
  if [ -d "$l" ] && [ -n "$(find "$l" -maxdepth 0 -mmin +"$stale_minutes")" ]; then rmdir "$l" 2>/dev/null || true; fi
  mkdir "$l" 2>/dev/null
}

# Checks out a fresh snapshot in a free pool slot, creating the worktree if needed, and prints its path.
acquire() {
  local snap n wt
  snap=$(snapshot)
  mkdir -p "$pool"
  n=1
  until lock "$n"; do n=$((n + 1)); done
  wt=$pool/$n
  if [ "$n" -gt "$slots" ]; then touch "$pool/$n.extra"; fi
  if [ "$(git -C "$wt" rev-parse --path-format=absolute --git-common-dir 2>/dev/null)" = "$common" ]; then
    git -C "$wt" checkout --quiet --detach --force "$snap"
    git -C "$wt" clean -fdq
    echo "tree.sh: reused review worktree $n; its ignored build output and dependencies are still there" >&2
  else
    rm -rf "$wt"
    git -C "$repo" worktree prune
    git -C "$repo" worktree add --quiet --detach "$wt" "$snap"
    echo "tree.sh: new review worktree $n; install dependencies in it once (they persist)" >&2
  fi
  echo "$wt"
}

# Unlocks a review worktree, deleting it if it was an extra beyond the kept slots.
release() {
  local wt=${1:?usage: tree.sh release <path>} n
  wt=${wt%/}
  case "$wt" in
    "$pool"/[0-9]*) n=${wt##*/} ;;
    *) echo "tree.sh: refusing to release $wt: not a Waterfall review worktree" >&2; exit 1 ;;
  esac
  if [ -e "$pool/$n.extra" ]; then
    git -C "$repo" worktree remove --force "$wt" 2>/dev/null || rm -rf "$wt"
    rm -f "$pool/$n.extra"
  fi
  rmdir "$pool/$n.lock" 2>/dev/null || true
}

case "${1:-}" in
  fingerprint) write_tree ;;
  snapshot) snapshot ;;
  worktree) acquire ;;
  release | remove) release "${2:-}" ;;
  shared)
    mkdir -p "$main/.claude/waterfall"
    exclude=$common/info/exclude
    mkdir -p "$(dirname "$exclude")"
    grep -qxF '.claude/waterfall/' "$exclude" 2>/dev/null || echo '.claude/waterfall/' >>"$exclude"
    echo "$main/.claude/waterfall"
    ;;
  clean)
    for wt in "$pool"/[0-9]*; do
      [ -d "$wt" ] || continue
      n=${wt##*/}
      case $n in *[!0-9]*) continue ;; esac
      if lock "$n"; then
        git -C "$repo" worktree remove --force "$wt" 2>/dev/null || rm -rf "$wt"
        rm -f "$pool/$n.extra"
        rmdir "$pool/$n.lock"
      else
        echo "tree.sh: review worktree $n is in use; left it" >&2
      fi
    done
    git -C "$repo" worktree prune
    ;;
  *) echo "usage: tree.sh fingerprint | snapshot | worktree | release <path> | shared | clean" >&2; exit 2 ;;
esac
