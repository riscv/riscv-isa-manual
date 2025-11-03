# RISC-V ISA Manual - AI Coding Agent Instructions

## Project Overview

This repository contains the **RISC-V Instruction Set Architecture (ISA) Manual** with two volumes:
- **Volume I**: Unprivileged Architecture (`src/riscv-unprivileged.adoc`)
- **Volume II**: Privileged Architecture (`src/riscv-privileged.adoc`)

The documentation is written in **AsciiDoc** format and uses a sophisticated **normative rules tagging system** to extract machine-readable compliance requirements from the specification text.

## Critical Architecture Concepts

### Normative Rules System (Core Innovation)

This project implements a unique dual-representation system for specification requirements:

1. **Human-readable spec**: AsciiDoc files in `src/` containing tagged normative text
2. **Machine-readable rules**: Generated JSON/XLSX in `build/` for tooling/verification

**Data Flow:**
```
src/*.adoc (with norm: tags)
  → build/*-norm-tags.json (extracted tags via custom AsciiDoctor backend)
  → normative_rule_defs/*.yaml (mappings + metadata)
  → build/norm-rules.json + build/norm-rules.xlsx (final outputs)
```

**Tag-to-Rule Relationships:**
- **1:1 (common)**: One tag → one rule (e.g., `[[norm:rv32i_xreg_sz]]`)
- **many:1**: Multiple rules share one tag (e.g., `slti_op`, `sltiu_op` → `norm:slti_sltiu_op`)
- **1:many**: One rule needs multiple tags for completeness

See `tagging_normative_rules.adoc` for the complete tagging methodology.

### Build System Architecture

**Docker-based build** (required): Uses `riscvintl/riscv-docs-base-container-image:latest`
- Avoids local dependency hell (AsciiDoctor + 5 plugins + Ruby + fonts)
- Supports rootless Docker and Podman with SELinux handling
- Working directories at `build/*-norm-tags.json.workdir/` are temporary

**Key Makefile targets:**
```bash
make build          # Everything: PDF + HTML + EPUB + tags + norm-rules
make build-pdf      # Just PDFs
make build-tags     # Just normative tag extraction
make build-norm-rules # Just norm-rules.json and norm-rules.xlsx
```

**Critical build dependencies:**
- `docs-resources/` submodule (themes, fonts, converters, schemas, tools)
- Must clone with `--recurse-submodules` or run `git submodule update --init --recursive`

## File Organization Patterns

### Source Structure
- `src/<topic>.adoc`: Individual chapters (e.g., `rv32.adoc`, `machine.adoc`)
- `src/riscv-{privileged,unprivileged}.adoc`: Top-level documents that include all chapters
- Each chapter has corresponding `normative_rule_defs/<topic>.yaml`

### Normative Rule Definition Files (`normative_rule_defs/*.yaml`)

**Schema location**: `docs-resources/schemas/defs-schema.json`

**Example pattern** (from `rv32.yaml`):
```yaml
normative_rule_definitions:
  - name: addi_op                    # Unique rule name (lowercase, underscores)
    summary: ADDI operation          # Brief description
    tags: ["norm:addi_op"]          # Tag(s) from adoc files

  - names: [slti_op, sltiu_op]      # Many:1 - multiple rules, one tag
    tags: ["norm:slti_sltiu_op"]

  - name: lh_rv64i_op                # 1:many - one rule, multiple tags
    summary: lh 64-bit sign extension
    tags: ["norm:lw_rv64i_op", "norm:subword_rv64i_load"]
```

**Naming conventions** (see `tagging_normative_rules.adoc`):
- Instructions: `<instr>_op`, `<instr>_enc`, `<instr>_<descriptor>`
- CSRs: `<csr>_sz`, `<csr>_acc`, `<csr>_mode`, `<csr>_op`
- CSR fields: `<csr>-<field>_sz`, `<csr>-<field>_acc` (note: dash separator)
- Parameters: `<param>_param` (must match UDB names)

### AsciiDoc Tagging Patterns

**Paragraph tags:**
```asciidoc
[[norm:rv32i_xreg_sz]]
For RV32I, the 32 `x` registers are each 32 bits wide, i.e., `XLEN=32`.
```

**Inline tags** (for tables, lists, mid-paragraph):
```asciidoc
[#norm:x0eq0]#Register `x0` is hardwired with all bits equal to 0.#
```

**Critical**: Tags must start with `norm:` prefix. Use underscores (not hyphens) in tag names except when representing dotted names (e.g., `fence.tso` → `fence-tso`).

## Development Workflows

### Building Locally
```bash
# Pull latest Docker image (recommended before builds)
make docker-pull-latest

# Build everything (uses all cores)
make -j$(nproc)

# Build specific format
make build-pdf
make build-html

# Clean all generated files
make clean
```

**Important**: Do NOT run `asciidoctor` directly unless you replicate all the `REQUIRES` flags from the Makefile (bibtex, diagram, lists, mathematical, sail).

### Adding/Editing Normative Rules

1. **Tag the text in `src/*.adoc`:**
   ```asciidoc
   [#norm:new_instr_op]#Instruction performs XYZ operation.#
   ```

2. **Define rule in `normative_rule_defs/*.yaml`:**
   ```yaml
   - name: new_instr_op
     summary: Instruction XYZ operation
     tags: ["norm:new_instr_op"]
   ```

3. **Rebuild to validate:**
   ```bash
   make build-tags build-norm-rules
   ```

4. **Check output**: Inspect `build/norm-rules.json` or `build/norm-rules.xlsx`

### CI/CD Behavior

**GitHub Actions** (`.github/workflows/isa-build.yml`):
- Builds on push to `main` and all PRs
- Generates PDF, HTML, EPUB for both volumes
- Creates GitHub Pages deployment at `https://<org>.github.io/riscv-isa-manual/snapshot/{privileged,unprivileged}/`
- Workflow dispatch can create releases with versioned artifacts

## Project-Specific Conventions

### Release Types
Set via `RELEASE_TYPE={draft, intermediate, official}` (default: `draft`):
- `draft`: Adds watermark, description "DRAFT---NOT AN OFFICIAL RELEASE"
- `intermediate`: No watermark, "Intermediate Release"
- `official`: No watermark, "Official Release"

### Document State Markup
Use `:revremark:` variable and admonitions per `docs-resources/README.md`:
- Discussion → "assume everything can change"
- Development → "limited change expected"
- Stable → "change is unlikely"
- Frozen → "extremely unlikely to change"
- Ratified → "no changes allowed"

### Submodule Management
`docs-resources/` is a Git submodule pointing to `riscv/docs-resources`:
- Contains shared themes, fonts, Ruby converters, JSON schemas
- Makefile auto-checks and initializes if missing
- To update: `cd docs-resources && git pull origin main && cd .. && git add docs-resources`

## Integration Points

### External Dependencies
- **Docker/Podman**: Build container with AsciiDoctor + plugins
- **riscv/docs-resources**: Shared documentation tooling (submodule)
- **riscv-unified-db (UDB)**: External metadata source referenced by normative rules but not stored here

### Custom Build Components
- `docs-resources/converters/tags.rb`: Custom AsciiDoctor backend for extracting `norm:` tags to JSON
- `docs-resources/tools/create_normative_rules.rb`: Ruby script merging tags + definitions → output files
- `docs-resources/schemas/*.json`: JSON schemas validating YAML inputs and JSON outputs

## Common Pitfalls

1. **Forgetting submodule initialization**: Results in `docs-resources/global-config.adoc` missing → build failure
2. **Tag naming errors**: Using spaces, starting with non-letter, or forgetting `norm:` prefix
3. **Misaligned YAML definitions**: Tag referenced in YAML but not present in any `.adoc` file
4. **Docker SELinux issues**: On Podman systems, Makefile automatically adds `:z` volume suffix
5. **Incremental build issues**: Use `UNRELIABLE_BUT_FASTER_INCREMENTAL_BUILDS=1` with caution (can produce stale outputs)

## Quick Reference

**Key files to understand the system:**
- `Makefile`: Build orchestration
- `tagging_normative_rules.adoc`: Complete tagging guide
- `normative_rule_defs/rv32.yaml`: Well-commented example of rule definitions
- `docs-resources/normative-rules.md`: General normative rules concepts
- `docs-resources/schemas/defs-schema.json`: YAML definition schema

**Testing your changes:**
```bash
# Full build test
make clean && make -j$(nproc)

# Verify normative rules only
make build-tags build-norm-rules
cat build/norm-rules.json | jq '.normative_rules[] | select(.name=="your_rule_name")'
```
