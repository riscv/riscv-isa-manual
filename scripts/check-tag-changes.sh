#!/bin/bash
set -e  # Exit on error

echo
echo '|=========================|'
echo '| Building normative tags |'
echo '|=========================|'
make build-tags

# Iterate through all configured specifications
SPECS="unprivileged privileged"
for spec in $SPECS; do
  echo
  echo "|===================================|"
  echo "| Checking $spec tag changes |"
  echo "|===================================|"
  ruby docs-resources/tools/detect_tag_changes.rb \
    --update-reference \
    ref/riscv-$spec-norm-tags.json \
    build/riscv-$spec-norm-tags.json
done

echo
echo "Tag change checks completed successfully."
