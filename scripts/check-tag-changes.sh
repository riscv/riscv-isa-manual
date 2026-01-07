#!/bin/bash
set -e  # Exit on error

echo
echo '|=========================|'
echo '| Building normative tags |'
echo '|=========================|'
make build-tags

echo
echo '|===================================|'
echo '| Checking unprivileged tag changes |'
echo '|===================================|'
ruby docs-resources/tools/detect_tag_changes.rb \
  --update-reference \
  ref/riscv-unprivileged-norm-tags.json \
  build/riscv-unprivileged-norm-tags.json

echo
echo '|=================================|'
echo "| Checking privileged tag changes |"
echo '|=================================|'
ruby docs-resources/tools/detect_tag_changes.rb \
  --update-reference \
  ref/riscv-privileged-norm-tags.json \
  build/riscv-privileged-norm-tags.json

echo "Tag change checks completed successfully."
