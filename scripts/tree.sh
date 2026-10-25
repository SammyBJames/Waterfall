#!/usr/bin/env bash
# Snapshot helpers for Waterfall. They read the user's working tree (tracked,
# staged and untracked files, but not ignored ones) without touching its
# index, branches or stashes. Run them from anywhere inside the user's repo.
#
#   tree.sh fingerprint     print a hash of the working tree
#   tree.sh snapshot        print a commit of the working tree on top of HEAD
#   tree.sh worktree        create a detached worktree of a fresh snapshot and print its path
#   tree.sh remove <path>   remove a worktree made by `tree.sh worktree`
set -euo pipefail

repo=$(git rev-parse --show-toplevel)

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

case "${1:-}" in
  fingerprint) write_tree ;;
  snapshot) snapshot ;;
  worktree)
    base=$(mktemp -d "${TMPDIR:-/tmp}/waterfall-review.XXXXXX")
    git -C "$repo" worktree add --quiet --detach "$base/review" "$(snapshot)"
    echo "$base/review"
    ;;
  remove)
    wt=${2:?usage: tree.sh remove <path>}
    case "$wt" in
      */waterfall-review.*/review) ;;
      *) echo "tree.sh: refusing to remove $wt: not a Waterfall review worktree" >&2; exit 1 ;;
    esac
    git -C "$repo" worktree remove --force "$wt"
    rmdir "$(dirname "$wt")"
    ;;
  *) echo "usage: tree.sh fingerprint | snapshot | worktree | remove <path>" >&2; exit 2 ;;
esac
