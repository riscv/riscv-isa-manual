# Normative Tag Reference Files

This directory holds a checked-in snapshot of the normative (specification-defining) text extracted from the manual's AsciiDoc sources.

## Purpose

Normative tags mark text that defines official RISC-V specification behaviour. Changes to this text can have significant implications for hardware and software implementations, so the extracted text is committed to the repository. That gives every pull request a reviewable diff of exactly which normative statements were:

- **Added** - new normative requirements introduced
- **Modified** - existing normative text changed
- **Deleted** - normative requirements removed

Downstream consumers (for example UDB) also read these files, so they must always match the sources.

## Files

| File | Description |
|------|-------------|
| `riscv-spec-norm-tags.json` | Normative tags and section structure for the RISC-V ISA Manual |

There is one file per document listed in `DOCS` in the [Makefile](../Makefile).

## JSON Structure

```json
{
  "tags": {
    "norm:tag-name": "The normative text content..."
  },
  "sections": {
    "title": "...",
    "id": "...",
    "children": [],
    "tags": []
  }
}
```

`tags` maps each AsciiDoc anchor prefixed with `norm:` to its extracted text. `sections` mirrors the document's section tree and records which tags live in each section. **Both** keys are part of the snapshot and both must be kept up to date.

## Keeping These Files Up To Date

The files are generated, never hand-edited. If you change tagged text in `src/`, regenerate them in the same pull request:

```bash
make update-ref        # Rebuild the tags and refresh ref/
git diff -- ref/       # Review what your change did to the normative text
git add ref/ && git commit
```

To check without committing:

```bash
make check-ref         # Fails if ref/ does not match a fresh build
```

`check-ref` is `update-ref` followed by `git diff --exit-code`, so if it fails, the corrected files are already sitting in your working tree ready to review and commit.

## How It Works

1. **Extraction** - `make build-tags` runs a custom Asciidoctor backend (`docs-resources/converters/tags.rb`) over the sources, writing `build/riscv-spec-norm-tags.json`.
2. **Refresh** - `make update-ref` copies that output into `ref/`, appending the trailing newline that pre-commit's `end-of-file-fixer` requires.
3. **CI** - the [check-normative-tags workflow](../.github/workflows/check-normative-tags.yml) runs on every pull request and enforces the two checks below.

## CI Behaviour

CI enforces two *separate* things. Keeping them separate matters: conflating them is what previously allowed these files to drift out of date ([#3186](https://github.com/riscv/riscv-isa-manual/issues/3186)).

### 1. Freshness (mechanical, not bypassable)

`make check-ref` requires `ref/` to be **byte-identical** to a fresh build. This is a pure yes/no question with no judgement involved, so it can never be bypassed or approved away. If it fails, run `make update-ref` and commit.

### 2. Normative change review (human judgement)

`docs-resources/tools/detect_tag_changes.py` compares `ref/` as of the pull request's **base commit** against the tags built from your branch, and publishes a report to the workflow's job summary.

| Change type | CI behaviour | Action required |
|-------------|--------------|-----------------|
| Addition | Pass | None; the report notes it for reviewers |
| Modification | Fail | Review, then approve via label (see below) |
| Deletion | Fail | Review, then approve via label (see below) |

This comparison deliberately **normalises whitespace and AsciiDoc formatting** before comparing, so that pure reformatting does not raise a false alarm about a normative change. That fuzziness is correct for a review signal but is *not* a substitute for the byte-exact freshness check above.

## Bypassing the Review Check

For intentional normative changes that have been reviewed and approved:

1. Add the `normative-change-approved` label to the pull request.
2. Modifications and deletions will then report without failing.

The label affects **only** the review check. It does not and cannot bypass the freshness check: an approved normative change still has to ship the regenerated `ref/` files.

## Related Files

- `docs-resources/converters/tags.rb` - tag extraction backend
- `docs-resources/tools/detect_tag_changes.py` - change reporting script
- `../.github/workflows/check-normative-tags.yml` - CI workflow
- `../.github/scripts/create-tag-change-issue.js` - issue creation on merge
- `../Makefile` - `build-tags`, `update-ref` and `check-ref` targets
