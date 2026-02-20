# Contributing to the RISC-V ISA Manual

Thanks for your interest in contributing! This guide covers how to set up your environment, build locally, and submit changes.

## Install dependencies

### 1 - Clone with submodules
This repository uses the `docs-resources` submodule.

```bash
git clone --recurse-submodules https://github.com/riscv/riscv-isa-manual.git
```

If you already cloned the repo, initialize the submodules:

```bash
git submodule update --init --recursive
```

### 2 - Recommended: use the docs container image
Building with the container is the most consistent approach.

- Install Docker (or Podman).
- Pull the base image:

```bash
docker pull riscvintl/riscv-docs-base-container-image:latest
```

### 3 - Alternative: local toolchain
Local builds are available, but require the full documentation toolchain (Ruby, Asciidoctor, and related extensions). Follow the dependency list in the RISC-V Documentation Developer Guide:

https://github.com/riscv/docs-dev-guide

## Build locally

From the repo root:

```bash
make build
```

Common targets:

```bash
make build-pdf
make build-html
make build-epub
```

Outputs land in the `build/` directory.

## Contributing changes

- Create a branch for your change.
- Keep commits focused and include clear messages.
- Run the relevant build target(s) before opening a PR.
- Open a pull request with a short summary of what changed and why.

## PR checklist (as applicable)

- Run the relevant build target(s), such as `make build`, `make build-pdf`, or `make build-html`.
- Add or update references/citations in `src/resources/riscv-spec.bib` when needed.
- Under development by the Documentation SIG: Normative Rules and Antora integration.

## Repository structure

- `src/` is the canonical AsciiDoc content used by `make` builds. `src/riscv-unprivileged.adoc` and `src/riscv-privileged.adoc` are the entrypoints that include chapter files.
- `modules/` contains the Antora site sources. `modules/unpriv/pages` and `modules/priv/pages` mirror chapter files for the site, and `modules/*/nav.adoc` controls navigation.
- `docs-resources/` is a submodule with shared themes, converters, schemas, and tooling.
- `normative_rule_defs/` contains one YAML definition file per chapter for normative rules.
- `build/` is generated output.

## Adding a new extension (AsciiDoc)

NOTE: New RISC-V specifications may only be developed by RISC-V International members through the formal ratification process and in accordance with the applicable Technical Steering Committee policies. Specifications cannot be introduced arbitrarily or by submitting an unsolicited pull request.

1. Create `src/<extension>.adoc` with the new chapter content.
2. Add an `include::` line in the appropriate entrypoint (`src/riscv-unprivileged.adoc` or `src/riscv-privileged.adoc`) in the correct order.

## Sign your commits

All contributions must be signed. Use either SSH (recommended) or GPG.

# Signing GitHub Commits — Step by Step

## Option A: Sign commits with SSH (recommended)

### 1. Generate an SSH key (skip if you already have one)
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### 2. Add the public key to GitHub
```bash
cat ~/.ssh/id_ed25519.pub
```
GitHub → Settings → **SSH and GPG keys** → **New SSH key**  
Key type: **Signing key**

### 3. Configure Git to use SSH signing
```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

### 4. Create a signed commit
```bash
git commit -m "message"
```

### 5. Verify locally
```bash
git log --show-signature -1
```

---

## Option B: Sign commits with GPG

### 1. Install GPG
- macOS:
```bash
brew install gnupg
```
- Ubuntu/Debian:
```bash
sudo apt-get install gnupg
```
- Windows: Install **Gpg4win**

### 2. Generate a GPG key
```bash
gpg --full-generate-key
```

### 3. List keys and copy the key ID
```bash
gpg --list-secret-keys --keyid-format=long
```

### 4. Configure Git to sign commits
```bash
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true
```

### 5. Export the public key and add it to GitHub
```bash
gpg --armor --export YOUR_KEY_ID
```
GitHub → Settings → **SSH and GPG keys** → **New GPG key**

### 6. Create a signed commit
```bash
git commit -m "message"
```

### 7. Verify locally
```bash
git log --show-signature -1
```
