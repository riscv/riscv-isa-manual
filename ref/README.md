# Normative Tag Reference Files

This directory contains reference files used to track changes to normative (specification-defining) text in the RISC-V ISA manual.

## Purpose

Normative tags mark text that defines official RISC-V specification behavior. Changes to this text can have significant implications for hardware and software implementations. These reference files serve as a baseline to detect when normative text is:

- **Added** - New normative requirements introduced
- **Modified** - Existing normative text changed
- **Deleted** - Normative requirements removed

## Files

| File | Description |
|------|-------------|
| `riscv-unprivileged-norm-tags.json` | Normative tags from the Unprivileged Specification |
| `riscv-privileged-norm-tags.json` | Normative tags from the Privileged Specification |

## How It Works

1. **Tag Extraction**: During the build process (`make build-tags`), normative tags are extracted from AsciiDoc source files using a custom Asciidoctor backend (`docs-resources/converters/tags.rb`).

2. **Change Detection**: The `detect_tag_changes.rb` script compares the newly extracted tags against these reference files to identify additions, modifications, and deletions.

3. **CI Integration**: The GitHub Actions workflow (`.github/workflows/check-normative-tags.yml`) runs this check on every PR and push to detect normative changes.

4. **Automatic Updates**: When PRs are merged to `main`, new tags (additions) are automatically added to these reference files. Modifications and deletions require manual review.

## Change Types and Actions

| Change Type | CI Behavior | Action Required |
|-------------|-------------|-----------------|
| Addition | Pass (auto-update on merge) | None - automatically tracked |
| Modification | Fail | Manual review and update |
| Deletion | Fail | Manual review and update |

## Bypassing the Check

For intentional normative changes that have been reviewed and approved:

1. Add the `normative-change-approved` label to the PR
2. The check will report changes but not fail the build
3. Update the reference files manually after merge if needed

## Updating Reference Files Manually

If you need to update the reference files after an intentional normative change:

```bash
# Build the current tags
make build-tags

# Copy the new reference files
cp build/riscv-unprivileged-norm-tags.json ref/
cp build/riscv-privileged-norm-tags.json ref/

# Commit the changes
git add ref/
git commit -m "Update normative tag reference files"
```

## JSON Structure

Each reference file contains a JSON object with:

```json
{
  "tags": {
    "norm:tag-name": "The normative text content...",
    ...
  }
}
```

The tag names correspond to AsciiDoc anchors prefixed with `norm:` in the source files.

## Related Files

- `docs-resources/tools/detect_tag_changes.rb` - Change detection script
- `docs-resources/converters/tags.rb` - Tag extraction backend
- `.github/workflows/check-normative-tags.yml` - CI workflow
- `.github/scripts/create-tag-change-issue.js` - Issue creation script
- `scripts/check-tag-changes.sh` - Local pre-commit check script
