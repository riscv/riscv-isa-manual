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
#   docker pull riscvintl/riscv-docs-base-container-image:latest
#

DOCS := riscv-privileged riscv-unprivileged

RELEASE_TYPE ?= draft

ifeq ($(RELEASE_TYPE), draft)
  WATERMARK_OPT := -a draft-watermark
  RELEASE_DESCRIPTION := DRAFT---NOT AN OFFICIAL RELEASE
else ifeq ($(RELEASE_TYPE), intermediate)
  WATERMARK_OPT :=
  RELEASE_DESCRIPTION := Intermediate Release
else ifeq ($(RELEASE_TYPE), official)
  WATERMARK_OPT :=
  RELEASE_DESCRIPTION := Official Release
else
  $(error Unknown build type; use RELEASE_TYPE={draft, intermediate, official})
endif

DATE ?= $(shell date +%Y%m%d)
DOCKER_BIN ?= docker
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
NORM_RULE_DEF_DIR := normative_rule_defs
DOC_NORM_TAG_SUFFIX := -norm-tags.json

DOCS_PDF := $(addprefix $(BUILD_DIR)/, $(addsuffix .pdf, $(DOCS)))
DOCS_HTML := $(addprefix $(BUILD_DIR)/, $(addsuffix .html, $(DOCS)))
DOCS_EPUB := $(addprefix $(BUILD_DIR)/, $(addsuffix .epub, $(DOCS)))
DOCS_NORM_TAGS := $(addprefix $(BUILD_DIR)/, $(addsuffix $(DOC_NORM_TAG_SUFFIX), $(DOCS)))
NORM_RULES_JSON := $(BUILD_DIR)/norm-rules.json
NORM_RULES_HTML := $(BUILD_DIR)/norm-rules.html

ENV := LANG=C.utf8
XTRA_ADOC_OPTS :=

ASCIIDOCTOR_PDF := $(ENV) asciidoctor-pdf
ASCIIDOCTOR_HTML := $(ENV) asciidoctor
ASCIIDOCTOR_EPUB := $(ENV) asciidoctor-epub3
ASCIIDOCTOR_TAGS := $(ENV) asciidoctor --backend tags --require=./docs-resources/converters/tags.rb
CREATE_NORM_RULE_TOOL := docs-resources/tools/create_normative_rules.rb
CREATE_NORM_RULE_RUBY := ruby $(CREATE_NORM_RULE_TOOL)

OPTIONS := --trace \
           -a compress \
           -a mathematical-format=svg \
           -a pdf-fontsdir=docs-resources/fonts \
           -a pdf-theme=docs-resources/themes/riscv-pdf.yml \
           $(WATERMARK_OPT) \
           -a revnumber='$(DATE)' \
           -a revremark='$(RELEASE_DESCRIPTION)' \
           -a docinfo=shared \
           $(XTRA_ADOC_OPTS) \
           -D build \
           --failure-level=WARN
REQUIRES := --require=asciidoctor-bibtex \
            --require=asciidoctor-diagram \
            --require=asciidoctor-lists \
            --require=asciidoctor-mathematical \
            --require=asciidoctor-sail

.PHONY: all build clean build-container build-no-container build-docs build-pdf build-html build-epub build-tags docker-pull-latest submodule-check
.PHONY: build-norm-rules build-norm-rules-json build-norm-rules-html

all: build

# Check if the docs-resources/global-config.adoc file exists. If not, the user forgot to check out submodules.
ifeq ("$(wildcard docs-resources/global-config.adoc)","")
  $(warning You must clone with --recurse-submodules to automatically populate the submodule 'docs-resources'.")
  $(warning Checking out submodules for you via 'git submodule update --init --recursive'...)
  $(shell git submodule update --init --recursive)
endif

build-pdf: $(DOCS_PDF)
build-html: $(DOCS_HTML)
build-epub: $(DOCS_EPUB)
build-tags: $(DOCS_NORM_TAGS)
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
	@echo -e '\n  Built \e]8;;file://$(abspath $@)\e\\$@\e]8;;\e\\\n'

$(BUILD_DIR)/%.html: $(SRC_DIR)/%.adoc $(ALL_SRCS)
	$(WORKDIR_SETUP)
	$(DOCKER_CMD) $(DOCKER_QUOTE) $(ASCIIDOCTOR_HTML) $(OPTIONS) $(REQUIRES) $< $(DOCKER_QUOTE)
	$(WORKDIR_TEARDOWN)
	@echo -e '\n  Built \e]8;;file://$(abspath $@)\e\\$@\e]8;;\e\\\n'

$(BUILD_DIR)/%.epub: $(SRC_DIR)/%.adoc $(ALL_SRCS)
	$(WORKDIR_SETUP)
	$(DOCKER_CMD) $(DOCKER_QUOTE) $(ASCIIDOCTOR_EPUB) $(OPTIONS) $(REQUIRES) $< $(DOCKER_QUOTE)
	$(WORKDIR_TEARDOWN)
	@echo -e '\n  Built \e]8;;file://$(abspath $@)\e\\$@\e]8;;\e\\\n'

$(BUILD_DIR)/%-norm-tags.json: $(SRC_DIR)/%.adoc $(ALL_SRCS) docs-resources/converters/tags.rb
	$(WORKDIR_SETUP)
	$(DOCKER_CMD) $(DOCKER_QUOTE) $(ASCIIDOCTOR_TAGS) $(OPTIONS) -a tags-match-prefix='norm:' -a tags-output-suffix='-norm-tags.json' $(REQUIRES) $< $(DOCKER_QUOTE)
	$(WORKDIR_TEARDOWN)

$(NORM_RULES_JSON): $(DOCS_NORM_TAGS) $(NORM_RULE_DEF_FILES) $(CREATE_NORM_RULE_TOOL)
	$(WORKDIR_SETUP)
	cp -f $(DOCS_NORM_TAGS) $@.workdir
	mkdir -p $@.workdir/build
	$(DOCKER_CMD) $(DOCKER_QUOTE) $(CREATE_NORM_RULE_RUBY) -j $(NORM_TAG_FILE_ARGS) $(NORM_RULE_DEF_ARGS) $(NORM_RULE_DOC2URL_ARGS) $@ $(DOCKER_QUOTE)
	$(WORKDIR_TEARDOWN)

$(NORM_RULES_HTML): $(DOCS_NORM_TAGS) $(NORM_RULE_DEF_FILES) $(CREATE_NORM_RULE_TOOL) $(DOCS_HTML)
	$(WORKDIR_SETUP)
	cp -f $(DOCS_NORM_TAGS) $@.workdir
	mkdir -p $@.workdir/build
	$(DOCKER_CMD) $(DOCKER_QUOTE) $(CREATE_NORM_RULE_RUBY) -h $(NORM_TAG_FILE_ARGS) $(NORM_RULE_DEF_ARGS) $(NORM_RULE_DOC2URL_ARGS) $@ $(DOCKER_QUOTE)
	$(WORKDIR_TEARDOWN)

# Update docker image to latest
docker-pull-latest:
	${DOCKER_BIN} pull ${DOCKER_IMG}

clean:
	@echo "Cleaning up generated files..."
	rm -rf $(BUILD_DIR)
	@echo "Cleanup completed."
