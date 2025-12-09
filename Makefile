# Makefile for RISC-V ISA Manuals
#
# This work is licensed under the Creative Commons Attribution-ShareAlike 4.0
# International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-sa/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
#
# SPDX-License-Identifier: CC-BY-SA-4.0
#
# Description:
#
# This Makefile is designed to automate the process of building and packaging
# the documentation for RISC-V ISA Manuals. It supports multiple build targets
# for generating documentation in various formats (PDF, HTML, EPUB).
#
# Building with a preinstalled docker container is recommended.
# Install by running:
#
#   docker pull riscvintl/riscv-docs-base-container-image:small


# --- Configuration & Defaults ---
DOCS := riscv-privileged riscv-unprivileged
RELEASE_TYPE ?= draft
DATE ?= $(shell date +%Y%m%d)

# Build tuning:
#   FAST=1, only build PDFs (for tight dev loop)
#   DEBUG=1, keep --timings and --trace
FAST ?= 0
DEBUG ?= 0

# Output Directory
BUILD_DIR := build
SRC_DIR   := src

# Container Runtime (Auto-detect Podman or use Docker)
DOCKER_BIN ?= $(shell command -v podman >/dev/null 2>&1 && echo podman || echo docker)
DOCKER_IMG := riscvintl/riscv-docs-base-container-image:small

# --- Release Watermarking ---
ifeq ($(RELEASE_TYPE), draft)
    WATERMARK_OPT := -a draft-watermark
    RELEASE_DESC  := DRAFT---NOT AN OFFICIAL RELEASE
else ifeq ($(RELEASE_TYPE), intermediate)
    WATERMARK_OPT :=
    RELEASE_DESC  := Intermediate Release
else ifeq ($(RELEASE_TYPE), official)
    WATERMARK_OPT :=
    RELEASE_DESC  := Official Release
else
    $(error Unknown RELEASE_TYPE. Use: draft, intermediate, or official)
endif

# --- Docker/Container Flags ---
DOCKER_USER_ARG :=
ifneq ($(shell id -u),0)
    ifeq ($(notdir $(DOCKER_BIN)),docker)
        DOCKER_USER_ARG := --user $(shell id -u):$(shell id -g)
    endif
endif

VOL_SUFFIX := :z

DOCKER_RUN_CMD := $(DOCKER_BIN) run --rm \
    $(DOCKER_USER_ARG) \
    -v "$(PWD)":/build$(VOL_SUFFIX) \
    -w /build \
    $(DOCKER_IMG)

# --- Asciidoctor Configuration ---

# Only pay for timings/trace when debugging
ADOC_DEBUG_OPTS :=
ifeq ($(DEBUG),1)
    ADOC_DEBUG_OPTS := --timings --trace
endif

ENV_VARS := LANG=C.utf8
COMMON_OPTS := $(ADOC_DEBUG_OPTS) \
    -a compress \
    -a mathematical-format=svg \
    -a pdf-fontsdir=docs-resources/fonts \
    -a pdf-theme=docs-resources/themes/riscv-pdf.yml \
    $(WATERMARK_OPT) \
    -a revnumber='$(DATE)' \
    -a revremark='$(RELEASE_DESC)' \
    -a docinfo=shared \
    -D $(BUILD_DIR) \
    --failure-level=WARN

REQUIRES := --require=asciidoctor-bibtex \
            --require=asciidoctor-diagram \
            --require=asciidoctor-lists \
            --require=asciidoctor-sail

# --- File Lists ---
DOCS_PDF  := $(DOCS:%=$(BUILD_DIR)/%.pdf)
DOCS_HTML := $(DOCS:%=$(BUILD_DIR)/%.html)
DOCS_EPUB := $(DOCS:%=$(BUILD_DIR)/%.epub)
DOCS_TAGS := $(DOCS:%=$(BUILD_DIR)/%-norm-tags.json)

NORM_RULES_JSON := $(BUILD_DIR)/norm-rules.json
NORM_RULES_HTML := $(BUILD_DIR)/norm-rules.html
NORM_RULE_DEFS  := $(wildcard normative_rule_defs/*.yaml)
RUBY_TOOL       := docs-resources/tools/create_normative_rules.rb

# Decide what "build" means:
#   FAST=1  -> PDFs only
#   FAST=0  -> full pipeline
ifeq ($(FAST),1)
    BUILD_TARGETS := build-pdf
else
    BUILD_TARGETS := build-pdf build-html build-epub build-norm-rules
endif

# --- Targets ---

.PHONY: all build clean help docker-pull
.PHONY: build-pdf build-html build-epub build-norm-rules

all: build

build: $(BUILD_TARGETS) ## Build selected formats (controlled by FAST)

help: ## Show this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m [FAST=1] [DEBUG=1]\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

build-pdf: $(DOCS_PDF)        ## Build PDFs
build-html: $(DOCS_HTML)      ## Build HTML
build-epub: $(DOCS_EPUB)      ## Build EPUB
build-norm-rules: $(NORM_RULES_JSON) $(NORM_RULES_HTML) ## Build normative rule artefacts

# Ensure resources submodule is present
docs-resources/global-config.adoc:
	@echo "Checking out submodules..."
	git submodule update --init --recursive

# --- Build Macros ---
# Usage: $(call run-asciidoctor, backend-format, source-file)
define run-asciidoctor
	@mkdir -p $(BUILD_DIR)
	@echo "Building $(2) -> $@"
	$(DOCKER_RUN_CMD) /bin/sh -c "$(ENV_VARS) asciidoctor$(if $(filter pdf,$(1)),-pdf,$(if $(filter epub3,$(1)),-epub3,)) \
	    $(COMMON_OPTS) $(REQUIRES) -b $(1) $(2)"
endef

# --- Pattern Rules ---

$(BUILD_DIR)/%.pdf: $(SRC_DIR)/%.adoc docs-resources/global-config.adoc
	$(call run-asciidoctor,pdf,$<)

$(BUILD_DIR)/%.html: $(SRC_DIR)/%.adoc docs-resources/global-config.adoc
	$(call run-asciidoctor,html5,$<)

$(BUILD_DIR)/%.epub: $(SRC_DIR)/%.adoc docs-resources/global-config.adoc
	$(call run-asciidoctor,epub3,$<)

# Normative Tags Extraction
$(BUILD_DIR)/%-norm-tags.json: $(SRC_DIR)/%.adoc docs-resources/global-config.adoc
	@mkdir -p $(BUILD_DIR)
	$(DOCKER_RUN_CMD) /bin/sh -c "$(ENV_VARS) asciidoctor \
	    $(COMMON_OPTS) $(REQUIRES) --backend tags \
	    --require=./docs-resources/converters/tags.rb \
	    -a tags-match-prefix='norm:' \
	    -a tags-output-suffix='-norm-tags.json' $<"

# Normative Rules Aggregation
$(NORM_RULES_JSON): $(DOCS_TAGS) $(NORM_RULE_DEFS)
	@echo "Generating Normative Rules JSON..."
	$(DOCKER_RUN_CMD) ruby $(RUBY_TOOL) \
	    -j $(foreach t,$(DOCS_TAGS),-t $(t)) \
	    $(foreach d,$(NORM_RULE_DEFS),-d $(d)) \
	    $(foreach doc,$(DOCS),-tag2url $(BUILD_DIR)/$(doc)-norm-tags.json $(doc).html) \
	    $@

$(NORM_RULES_HTML): $(DOCS_TAGS) $(NORM_RULE_DEFS) $(DOCS_HTML)
	@echo "Generating Normative Rules HTML..."
	$(DOCKER_RUN_CMD) ruby $(RUBY_TOOL) \
	    -h $(foreach t,$(DOCS_TAGS),-t $(t)) \
	    $(foreach d,$(NORM_RULE_DEFS),-d $(d)) \
	    $(foreach doc,$(DOCS),-tag2url $(BUILD_DIR)/$(doc)-norm-tags.json $(doc).html) \
	    $@

# --- Utilities ---

docker-pull: ## Update the docker image
	$(DOCKER_BIN) pull $(DOCKER_IMG)

clean: ## Clean build artifacts
	rm -rf $(BUILD_DIR)
