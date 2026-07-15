#!/usr/bin/env bash
#
# gen-changebar-diff.sh — emit the changed AsciiDoc line ranges for changebars.
#
# Prints a JSON object mapping each changed .adoc source file to the list of
# line ranges (in the *working-tree* version of the file) that differ from a
# base ref. changebar.rb consumes this to place margin bars.
#
# Usage:
#   scripts/gen-changebar-diff.sh [BASE_REF] > changes.json
#
# BASE_REF defaults to origin/main. The comparison uses the merge base
# (git diff BASE...HEAD), i.e. "everything this branch changed since it forked",
# which matches what a reviewer expects to see marked. Uncommitted working-tree
# edits are included too, so you can preview changes before committing.
#
# Requires: git, awk. Run from the repo root (the Makefile does).

set -euo pipefail

BASE_REF="${1:-origin/main}"

# Resolve the merge base so we compare against the fork point, not the tip of
# the base branch. Fall back to comparing directly against BASE_REF if no common
# ancestor exists (e.g. unrelated histories).
if MERGE_BASE="$(git merge-base "$BASE_REF" HEAD 2>/dev/null)"; then
  DIFF_BASE="$MERGE_BASE"
else
  DIFF_BASE="$BASE_REF"
fi

# --unified=0 gives one hunk per changed region with exact new-file line spans.
# We include staged + unstaged working-tree changes (no ".." end ref) so a build
# reflects the tree being rendered.
#
# awk parses hunk headers `@@ -old +new,count @@`:
#   - a pure addition/modification (count>0) marks lines new..new+count-1
#   - a pure deletion (count==0) marks the single line `new` so the removal is
#     still visibly flagged at the point content was cut.
git diff --no-color --unified=0 --diff-filter=ACMR "$DIFF_BASE" -- '*.adoc' \
  | awk '
    /^\+\+\+ / {
      path = $2
      sub(/^b\//, "", path)
      next
    }
    /^@@ / {
      # field looks like +new or +new,count
      hunk = $3
      sub(/^\+/, "", hunk)
      n = split(hunk, a, ",")
      start = a[1] + 0
      count = (n > 1) ? a[2] + 0 : 1
      if (count == 0) { lo = start; hi = start }        # deletion point
      else            { lo = start; hi = start + count - 1 }
      ranges[path] = ranges[path] sep[path] "[" lo "," hi "]"
      sep[path] = ","
    }
    END {
      printf "{"
      first = 1
      for (p in ranges) {
        if (!first) printf ","
        printf "\n  \"%s\": [%s]", p, ranges[p]
        first = 0
      }
      printf "\n}\n"
    }
  '
