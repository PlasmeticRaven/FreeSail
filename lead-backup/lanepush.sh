#!/bin/bash
# lanepush.sh <worktree> <branch> <label>
# Pushes a commit whose tree is exactly the worktree's index (staged) tree to the scratch
# branch <branch> as a fast-forward (never a force): parents are the branch's tip (if any)
# and the worktree's HEAD. Prints commit and tree.
set -euo pipefail
WT=$1; BR=$2; LABEL=$3
cd "$WT"
test -z "$(git diff --name-only)" || { echo "unstaged changes in the trial"; exit 1; }
TREE=$(git write-tree)
BASE=$(git rev-parse HEAD)
OLD=""
git fetch -q origin "$BR" 2>/dev/null && OLD=$(git rev-parse FETCH_HEAD) || OLD=""
PARENTS="-p $BASE"
[ -n "$OLD" ] && PARENTS="-p $OLD $PARENTS"
C=$(git -c user.name=Claude -c user.email=noreply@anthropic.com commit-tree $TREE $PARENTS -m "Trial tree for the cloud: $LABEL

A scratch tree of the lead's (not the trunk).

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DTAvj6mwzAZMm2fER1Bi3U")
git push -q origin $C:refs/heads/$BR
echo "branch $BR commit $C tree $TREE base $BASE"
