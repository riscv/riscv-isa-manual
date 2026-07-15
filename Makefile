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
#   docker pull ghcr.io/riscv/riscv-docs-base-container-image:latest
#

DOCS := riscv-spec

RELEASE_TYPE ?= draft
DATE ?= $(shell date +%Y%m%d)
MONTHYEAR := $(shell date -j -f "%Y%m%d" "$(DATE)" +"%B %Y" 2>/dev/null || date -d "$(DATE)" +"%B %Y")
YEAR := $(shell date -j -f "%Y%m%d" "$(DATE)" +"%Y" 2>/dev/null || date -d "$(DATE)" +"%Y")

CITATION_DESCRIPTION := $(DATE)-$(RELEASE_TYPE)
ifeq ($(RELEASE_TYPE), draft)
  WATERMARK_OPT := -a draft-watermark
  RELEASE_DESCRIPTION := DRAFT—NOT AN OFFICIAL RELEASE
else ifeq ($(RELEASE_TYPE), intermediate)
  WATERMARK_OPT :=
  RELEASE_DESCRIPTION := Intermediate Release
else ifeq ($(RELEASE_TYPE), official)
  WATERMARK_OPT :=
  RELEASE_DESCRIPTION := Official Release
  CITATION_DESCRIPTION := $(DATE)
else
  $(error Unknown build type; use RELEASE_TYPE={draft, intermediate, official})
endif

RELEASE_DESCRIPTION_HTML := $(RELEASE_DESCRIPTION).  © RISC-V International, $(YEAR).

DOCKER_BIN ?= docker
DOCKER_INTERACTIVE=--init $(shell [ -t 0 ] && echo "-t")
SKIP_DOCKER ?= $(shell if command -v ${DOCKER_BIN}  >/dev/null 2>&1 ; then echo false; else echo true; fi)
DOCKER_IMG := ghcr.io/riscv/riscv-docs-base-container-image:latest
ifneq ($(SKIP_DOCKER),true)
    DOCKER_IS_PODMAN = \
        $(shell ! ${DOCKER_BIN}  -v | grep podman >/dev/null ; echo $$?)
    ifeq "$(DOCKER_IS_PODMAN)" "1"
        # Modify the SELinux label for the host directory to indicate
        # that it can be shared with multiple containers. This is apparently
        # only required for Podman, though it is also supported by Docker.
        DOCKER_VOL_SUFFIX = :z
        DOCKER_EXTRA_VOL_SUFFIX = ,z
    else
        DOCKER_IS_ROOTLESS = \
            $(shell ! ${DOCKER_BIN} info -f '{{println .SecurityOptions}}' | grep rootless >/dev/null ; echo $$?)
        ifneq "$(DOCKER_IS_ROOTLESS)" "1"
            # Rooted Docker requires this flag so that the files it creates are
            # owned by the current user instead of root. Rootless docker does not
            # require it, and Podman doesn't either since it is always rootless.
            DOCKER_USER_ARG := --user $(shell id -u)
        endif
    endif

    DOCKER_CMD = \
        ${DOCKER_BIN} run --rm \
            ${DOCKER_INTERACTIVE} \
            -v ${PWD}/$@.workdir:/build${DOCKER_VOL_SUFFIX} \
            -v ${PWD}/src:/src:ro${DOCKER_EXTRA_VOL_SUFFIX} \
            -v ${PWD}/normative_rule_defs:/normative_rule_defs:ro${DOCKER_EXTRA_VOL_SUFFIX} \
            -v ${PWD}/docs-resources:/docs-resources:ro${DOCKER_EXTRA_VOL_SUFFIX} \
            -w /build \
            $(DOCKER_USER_ARG) \
            ${DOCKER_IMG} \
            /bin/sh -c
    DOCKER_QUOTE := "
else
    DOCKER_CMD = \
        cd $@.workdir &&
endif

ifdef UNRELIABLE_BUT_FASTER_INCREMENTAL_BUILDS
WORKDIR_SETUP = mkdir -p $@.workdir && ln -sfn ../../src ../../normative_rule_defs ../../docs-resources $@.workdir/
WORKDIR_TEARDOWN = mv $@.workdir/$@ $@
else
WORKDIR_SETUP = \
    rm -rf $@.workdir && \
    mkdir -p $@.workdir && \
    ln -sfn ../../src ../../normative_rule_defs ../../docs-resources $@.workdir/

WORKDIR_TEARDOWN = \
    mv $@.workdir/$@ $@ && \
    rm -rf $@.workdir
endif

SRC_DIR := src
BUILD_DIR := build
REF_DIR := ref
NORM_RULE_DEF_DIR := normative_rule_defs
DOC_NORM_TAG_SUFFIX := -norm-tags.json

DOCS_PDF := $(addprefix $(BUILD_DIR)/, $(addsuffix .pdf, $(DOCS)))
DOCS_HTML := $(addprefix $(BUILD_DIR)/, $(addsuffix .html, $(DOCS)))
DOCS_EPUB := $(addprefix $(BUILD_DIR)/, $(addsuffix .epub, $(DOCS)))
DOCS_NORM_TAGS := $(addprefix $(BUILD_DIR)/, $(addsuffix $(DOC_NORM_TAG_SUFFIX), $(DOCS)))
REF_NORM_TAGS := $(addprefix $(REF_DIR)/, $(addsuffix $(DOC_NORM_TAG_SUFFIX), $(DOCS)))
NORM_RULES_JSON := $(BUILD_DIR)/norm-rules.json
NORM_RULES_HTML := $(BUILD_DIR)/norm-rules.html

ENV := LANG=C.utf8
XTRA_ADOC_OPTS :=

ASCIIDOCTOR_PDF := $(ENV) asciidoctor-pdf
ASCIIDOCTOR_HTML := $(ENV) asciidoctor
ASCIIDOCTOR_EPUB := $(ENV) asciidoctor-epub3
ASCIIDOCTOR_TAGS := $(ENV) asciidoctor --backend tags --require=./docs-resources/converters/tags.rb
CREATE_NORM_RULE_TOOL := docs-resources/tools/create_normative_rules.py
CREATE_NORM_RULE_PYTHON := python3 $(CREATE_NORM_RULE_TOOL)

OPTIONS_TAGS := --trace \
           -a compress \
           -a pdf-fontsdir=docs-resources/fonts \
           -a pdf-theme=docs-resources/themes/riscv-pdf.yml \
           $(WATERMARK_OPT) \
           -a revnumber='$(DATE)' \
           -a monthyear='$(MONTHYEAR)' \
           -a revcite='$(CITATION_DESCRIPTION)' \
           -a revremark='$(RELEASE_DESCRIPTION)' \
           -a docinfo=shared \
           $(XTRA_ADOC_OPTS) \
           -D build \
           --failure-level=WARN
OPTIONS := $(OPTIONS_TAGS) \
           -r ./src/lib/volume-xrefs.rb \
           -r ./src/lib/macros.rb
REQUIRES := --require=asciidoctor-bibtex \
            --require=asciidoctor-diagram \
            --require=asciidoctor-lists \
            --require=asciidoctor-sail

.PHONY: all build clean build-container build-no-container build-docs build-pdf build-html build-epub build-tags docker-pull-latest submodule-check
.PHONY: build-norm-rules build-norm-rules-json build-norm-rules-html update-ref check-ref check-xref-fallbacks build-changebar-pdf

all: build

# Check if the docs-resources/global-config.adoc file exists. If not, the user forgot to check out submodules.
ifeq ("$(wildcard docs-resources/global-config.adoc)","")
  $(warning You must clone with --recurse-submodules to automatically populate the submodule 'docs-resources'.")
  $(warning Checking out submodules for you via 'git submodule update --init --recursive'...)
  $(shell git submodule update --init --recursive)
endif

# Changebar PDF: the normal manual with a red bar in the left margin next to
# everything this branch changed relative to CHANGEBAR_BASE (default
# origin/main). The diff is computed on the host by
# scripts/gen-changebar-diff.sh (git isn't available in the build container) and
# consumed by src/lib/changebar.rb via --sourcemap.
# Override the base ref with e.g.: make build-changebar-pdf CHANGEBAR_BASE=v2.0
CHANGEBAR_BASE ?= origin/main
CHANGEBAR_PDF := $(BUILD_DIR)/$(DOCS)-changebar.pdf
CHANGEBAR_DIFF_JSON := changebar-changes.json
CHANGEBAR_OPTS := --sourcemap -r ./src/lib/changebar.rb -a changebar-diff=$(CHANGEBAR_DIFF_JSON)

build-pdf: $(DOCS_PDF)
build-changebar-pdf: $(CHANGEBAR_PDF)
build-html: $(DOCS_HTML) check-xref-fallbacks
build-epub: $(DOCS_EPUB)
build-tags: $(DOCS_NORM_TAGS)
check-xrefs: $(addprefix $(BUILD_DIR)/, $(addsuffix .check-xrefs, $(DOCS)))
check-xref-fallbacks: $(DOCS_HTML)
	@python3 ./scripts/check_xref_fallbacks.py $(DOCS_HTML)

# Regenerate the checked-in normative tags JSON in $(REF_DIR) from the sources.
#
# The tags backend (docs-resources/converters/tags.rb) emits JSON with no
# trailing newline, but pre-commit's end-of-file-fixer requires one, so append
# it when it is missing. Inside a command substitution `tail -c 1` yields the
# empty string exactly when the file already ends in a newline.
update-ref: $(DOCS_NORM_TAGS)
	cp -f $(DOCS_NORM_TAGS) $(REF_DIR)
	@for f in $(REF_NORM_TAGS); do \
	  if [ -n "$$(tail -c 1 "$$f")" ]; then printf '\n' >> "$$f"; fi; \
	done

# Fail if the checked-in normative tags are out of date with respect to the
# sources.
#
# This regenerates them and then asks git whether anything changed, so the check
# can never drift from the updater the way a separate comparison would. Note
# that it rewrites the files in place: on failure the working tree already holds
# the correct content, ready to review and commit.
#
# Only the generated files are examined, not all of $(REF_DIR) -- the hand-written
# documentation living alongside them must not affect this check.
check-ref: update-ref
	@if git diff --quiet -- $(REF_NORM_TAGS); then \
	  echo "Normative tag reference files are up to date."; \
	else \
	  echo "ERROR: normative tag reference files are out of date:"; \
	  echo; \
	  git diff --stat -- $(REF_NORM_TAGS); \
	  echo; \
	  echo "Run 'make update-ref', review the diff, and commit the result."; \
	  exit 1; \
	fi

build-norm-rules-json: $(NORM_RULES_JSON)
build-norm-rules-html: $(NORM_RULES_HTML)
build-norm-rules: build-norm-rules-json build-norm-rules-html
build: build-pdf build-html build-epub build-tags build-norm-rules-json build-norm-rules-html

ALL_SRCS := $(shell git ls-files $(SRC_DIR))

# All normative rule definition input YAML files.
NORM_RULE_DEF_FILES := $(wildcard $(NORM_RULE_DEF_DIR)/*.yaml)

# Add -t to each normative tag input filename and add prefix of "/" to make into absolute pathname.
NORM_TAG_FILE_ARGS := $(foreach relative_pname,$(DOCS_NORM_TAGS),-t /$(relative_pname))

# Add -d to each normative rule definition filename
NORM_RULE_DEF_ARGS := $(foreach relative_pname,$(NORM_RULE_DEF_FILES),-d $(relative_pname))

# Provide mapping from an ISA manual's norm tags JSON file to a URL that one can link to. Used to create links into ISA manual.
NORM_RULE_DOC2URL_ARGS := $(foreach doc_name,$(DOCS),-tag2url /$(BUILD_DIR)/$(doc_name)$(DOC_NORM_TAG_SUFFIX) $(doc_name).html)

# Temporarily make errors warnings. Don't check this in uncommented.
# NORM_RULE_DEF_ARGS := $(NORM_RULE_DEF_ARGS) -w

$(BUILD_DIR)/%.pdf: $(SRC_DIR)/%.adoc $(ALL_SRCS)
	$(WORKDIR_SETUP)
	$(DOCKER_CMD) $(DOCKER_QUOTE) $(ASCIIDOCTOR_PDF) $(OPTIONS) $(REQUIRES) $< $(DOCKER_QUOTE)
	$(WORKDIR_TEARDOWN)
	@printf '\n  Built \033]8;;file://%s\033\\%s\033]8;;\033\\\n\n' "$(abspath $@)" "$@"

$(CHANGEBAR_PDF): $(SRC_DIR)/$(DOCS).adoc $(ALL_SRCS)
	$(WORKDIR_SETUP)
	bash ./scripts/gen-changebar-diff.sh "$(CHANGEBAR_BASE)" > "$@.workdir/$(CHANGEBAR_DIFF_JSON)"
	$(DOCKER_CMD) $(DOCKER_QUOTE) $(ASCIIDOCTOR_PDF) $(OPTIONS) $(CHANGEBAR_OPTS) $(REQUIRES) $< $(DOCKER_QUOTE)
	mv $@.workdir/$(BUILD_DIR)/$(DOCS).pdf $@ && rm -rf $@.workdir
	@printf '\n  Built \033]8;;file://%s\033\\%s\033]8;;\033\\\n\n' "$(abspath $@)" "$@"

$(BUILD_DIR)/%.html: $(SRC_DIR)/%.adoc $(ALL_SRCS)
	$(WORKDIR_SETUP)
	$(DOCKER_CMD) $(DOCKER_QUOTE) $(ASCIIDOCTOR_HTML) $(OPTIONS) -a revremark='$(RELEASE_DESCRIPTION_HTML)' $(REQUIRES) $< $(DOCKER_QUOTE)
	$(WORKDIR_TEARDOWN)
	@printf '\n  Built \033]8;;file://%s\033\\%s\033]8;;\033\\\n\n' "$(abspath $@)" "$@"

$(BUILD_DIR)/%.epub: $(SRC_DIR)/%.adoc $(ALL_SRCS)
	$(WORKDIR_SETUP)
	$(DOCKER_CMD) $(DOCKER_QUOTE) $(ASCIIDOCTOR_EPUB) $(OPTIONS) $(REQUIRES) $< $(DOCKER_QUOTE)
	$(WORKDIR_TEARDOWN)
	@printf '\n  Built \033]8;;file://%s\033\\%s\033]8;;\033\\\n\n' "$(abspath $@)" "$@"

$(BUILD_DIR)/%-norm-tags.json: $(SRC_DIR)/%.adoc $(ALL_SRCS) docs-resources/converters/tags.rb
	$(WORKDIR_SETUP)
	$(DOCKER_CMD) $(DOCKER_QUOTE) $(ASCIIDOCTOR_TAGS) $(OPTIONS_TAGS) -a tags-match-prefix='norm:' -a tags-output-suffix='-norm-tags.json' $(REQUIRES) $< $(DOCKER_QUOTE)
	$(WORKDIR_TEARDOWN)

$(NORM_RULES_JSON): $(DOCS_NORM_TAGS) $(NORM_RULE_DEF_FILES) $(CREATE_NORM_RULE_TOOL)
	$(WORKDIR_SETUP)
	cp -f $(DOCS_NORM_TAGS) $@.workdir
	mkdir -p $@.workdir/build
	$(DOCKER_CMD) $(DOCKER_QUOTE) $(CREATE_NORM_RULE_PYTHON) -j $(NORM_TAG_FILE_ARGS) $(NORM_RULE_DEF_ARGS) $(NORM_RULE_DOC2URL_ARGS) $@ $(DOCKER_QUOTE)
	$(WORKDIR_TEARDOWN)

$(NORM_RULES_HTML): $(DOCS_NORM_TAGS) $(NORM_RULE_DEF_FILES) $(CREATE_NORM_RULE_TOOL) $(DOCS_HTML)
	$(WORKDIR_SETUP)
	cp -f $(DOCS_NORM_TAGS) $@.workdir
	mkdir -p $@.workdir/build
	$(DOCKER_CMD) $(DOCKER_QUOTE) $(CREATE_NORM_RULE_PYTHON) --html $(NORM_TAG_FILE_ARGS) $(NORM_RULE_DEF_ARGS) $(NORM_RULE_DOC2URL_ARGS) $@ $(DOCKER_QUOTE)
	$(WORKDIR_TEARDOWN)

$(BUILD_DIR)/%.check-xrefs: $(SRC_DIR)/%.adoc $(ALL_SRCS)
	$(WORKDIR_SETUP)
	$(DOCKER_CMD) $(DOCKER_QUOTE) $(ASCIIDOCTOR_HTML) -v $(OPTIONS) $(REQUIRES) $< 2>&1 | grep 'possible invalid reference' && exit 1 || [ $$? -eq 0 ] $(DOCKER_QUOTE)
	@[ ! -f $@.workdir/$(BUILD_DIR)/$(notdir $*).html ] && exit 0 || python3 scripts/check_xref_fallbacks.py $@.workdir/$(BUILD_DIR)/$(notdir $*).html

# Update docker image to latest
docker-pull-latest:
	${DOCKER_BIN} pull ${DOCKER_IMG}

clean:
	@echo "Cleaning up generated files..."
	rm -rf $(BUILD_DIR)
	@echo "Cleanup completed."
