# RISC-V Instruction Set Manual

[![RISC-V ISA Build](https://github.com/riscv/riscv-isa-manual/actions/workflows/isa-build.yml/badge.svg)](https://github.com/riscv/riscv-isa-manual/actions/workflows/isa-build.yml)

This repository contains the source files for the RISC-V Instruction Set Manual, which consists of the Unprivileged and Privileged volumes. The preface of each document indicates the version of each standard that has been formally ratified by RISC-V International.

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/). See the [LICENSE](LICENSE) file for details.

The RISC-V Instruction Set Manual is organized into the following volumes:

- Volume I: Unprivileged Architecture
- Volume II: Privileged Architecture

## Official and Draft Versions

- **Official versions** of the specifications are available at the [RISC-V International website](https://riscv.org/specifications/).
- **Compiled versions of the most recent drafts** of the specifications can be found on the [GitHub releases page](https://github.com/riscv/riscv-isa-manual/releases/latest).
- **HTML snapshots of the latest commit** can be viewed at the following locations:
  - [Unprivileged spec](https://riscv.github.io/riscv-isa-manual/snapshot/unprivileged/)
  - [Privileged spec](https://riscv.github.io/riscv-isa-manual/snapshot/privileged/)
- **Older official versions** of the specifications are archived at the [GitHub releases archive](https://github.com/riscv/riscv-isa-manual/releases/tag/archive).

The canonical list of **open-source RISC-V implementations' marchid CSR values** is available in the [marchid.md file](https://github.com/riscv/riscv-isa-manual/blob/main/marchid.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, build instructions, and contribution guidelines.
If you would like to contribute to this documentation, please refer to the [Documentation Developer's Guide](https://github.com/riscv/docs-dev-guide).

The recommended method for building the PDF files is to use the Docker Image, as described in the [RISC-V Docs Base Container Image repository](https://github.com/riscv/riscv-docs-base-container-image).

Alternative build methods, such as local builds and GitHub Action builds, are also available and described in the Documentation Developer's Guide.

## Images not rendered for EPUB files

If the eBook reader does not support embedded images, uncomment `:data-uri:` lines in `src/riscv-privileged.adoc` and `src/riscv-unprivileged.adoc`.

### Known devices that cannot handle embedded images

- PocketBook InkPad 3

## Repo Activity

![Alt](https://repobeats.axiom.co/api/embed/ccec87dc4502f2ed7c216b670b5ed8efc33a1d4c.svg "Repobeats analytics image")
