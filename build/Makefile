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
# for generating documentation in various formats (PDF, HTML).
#
# Building with a preinstalled docker container is recommended.
# Install by running:
#
#   docker pull riscvintl/riscv-docs-base-container-image:latest
#

# Build Targets
TARGETS_PDF := riscv-privileged.pdf riscv-unprivileged.pdf
TARGETS_HTML := riscv-privileged.html riscv-unprivileged.html
TARGETS_EPUB := riscv-privileged.epub riscv-unprivileged.epub
TARGETS := $(TARGETS_PDF) $(TARGETS_HTML) $(TARGETS_EPUB)

SHORT_TARGETS := priv-pdf unpriv-pdf  priv-html unpriv-html priv-epub unpriv-epub

# Declare phony targets
.PHONY: all docker clean $(SHORT_TARGETS)

# Default target builds all
all: $(TARGETS)

define run_with_docker
	cd .. && docker run -it -v `pwd`:/build riscvintl/riscv-docs-base-container-image:latest /bin/sh -c 'export LANG=C.utf8; cd ./build; $(1)'
endef

# Run natively if command exists, otherwise run with docker
define maybe_run_with_docker
	@if command -v $(1) &> /dev/null; \
	then \
		$(1) $(2); \
	else \
		$(call run_with_docker, $(1) $(2)); \
	fi
endef

docker:
	$(call run_with_docker, make -$(MAKEFLAGS) all)

# Asciidoctor options
ASCIIDOCTOR_OPTS := -a compress \
                    --attribute=mathematical-format=svg \
                    --failure-level=ERROR \
                    --require=asciidoctor-bibtex \
                    --require=asciidoctor-diagram \
                    --require=asciidoctor-mathematical \
                    --trace

# Source directory
SRCDIR := ../src
ALL_SRCS := $(shell find $(SRCDIR) -type f)

# Privileged ISA build
priv-pdf: riscv-privileged.pdf

riscv-privileged.pdf: $(SRCDIR)/riscv-privileged.adoc $(ALL_SRCS)
	@echo "Building Privileged ISA"
	@rm -f $@.tmp
	$(call maybe_run_with_docker, asciidoctor-pdf, $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<)
	@mv $@.tmp $@

# Unprivileged ISA build
unpriv-pdf: riscv-unprivileged.pdf

riscv-unprivileged.pdf: $(SRCDIR)/riscv-unprivileged.adoc $(ALL_SRCS)
	@echo "Building Unprivileged ISA"
	@rm -f $@.tmp
	$(call maybe_run_with_docker, asciidoctor-pdf, $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<)
	@mv $@.tmp $@

# Privileged ISA HTML build
priv-html: riscv-privileged.html

riscv-privileged.html: $(SRCDIR)/riscv-privileged.adoc $(ALL_SRCS)
	@echo "Building Privileged ISA HTML"
	@rm -f $@.tmp
	$(call maybe_run_with_docker, asciidoctor, $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<)
	@mv $@.tmp $@

# Unprivileged ISA HTML build
unpriv-html: riscv-unprivileged.html

riscv-unprivileged.html: $(SRCDIR)/riscv-unprivileged.adoc $(ALL_SRCS)
	@echo "Building Unprivileged ISA HTML"
	@rm -f $@.tmp
	$(call maybe_run_with_docker, asciidoctor, $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<)
	@mv $@.tmp $@

priv-epub: riscv-privileged.epub

riscv-privileged.epub: $(SRCDIR)/riscv-privileged.adoc $(ALL_SRCS)
	@echo "Building Privileged ISA EPUB"
	@rm -f $@.tmp
	$(call maybe_run_with_docker, asciidoctor-epub3, $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<)
	@mv $@.tmp $@

unpriv-epub: riscv-unprivileged.epub

riscv-unprivileged.epub: $(SRCDIR)/riscv-unprivileged.adoc $(ALL_SRCS)
	@echo "Building Unprivileged ISA EPUB"
	@rm -f $@.tmp
	$(call maybe_run_with_docker, asciidoctor-epub3, $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<)
	@mv $@.tmp $@

clean:
	rm -f $(TARGETS) $(addsuffix .tmp,$(TARGETS))
