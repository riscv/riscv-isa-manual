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

# Build Targets
TARGETS_PDF := priv-isa.pdf unpriv-isa.pdf
TARGETS_HTML := priv-isa.html unpriv-isa.html
TARGETS_EPUB := priv-isa.epub unpriv-isa.epub
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

# Privileged ISA build
priv-pdf: priv-isa.pdf

priv-isa.pdf: $(SRCDIR)/riscv-privileged.adoc $(SRCDIR)/*.adoc
	@echo "Building Privileged ISA"
	@rm -f $@.tmp
	$(call maybe_run_with_docker, asciidoctor-pdf, $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<)
	@mv $@.tmp $@

# Unprivileged ISA build
unpriv-pdf: unpriv-isa.pdf

unpriv-isa.pdf: $(SRCDIR)/riscv-unprivileged.adoc $(SRCDIR)/*.adoc
	@echo "Building Unprivileged ISA"
	@rm -f $@.tmp
	$(call maybe_run_with_docker, asciidoctor-pdf, $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<)
	@mv $@.tmp $@

# Privileged ISA HTML build
priv-html: priv-isa.html

priv-isa.html: $(SRCDIR)/riscv-privileged.adoc
	@echo "Building Privileged ISA HTML"
	@rm -f $@.tmp
	$(call maybe_run_with_docker, asciidoctor, $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<)
	@mv $@.tmp $@

# Unprivileged ISA HTML build
unpriv-html: unpriv-isa.html

unpriv-isa.html: $(SRCDIR)/riscv-unprivileged.adoc
	@echo "Building Unprivileged ISA HTML"
	@rm -f $@.tmp
	$(call maybe_run_with_docker, asciidoctor, $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<)
	@mv $@.tmp $@

priv-epub: priv-isa.epub

priv-isa.epub: $(SRCDIR)/riscv-privileged.adoc
	@echo "Building Privileged ISA EPUB"
	@rm -f $@.tmp
	$(call maybe_run_with_docker, asciidoctor-epub3, $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<)
	@mv $@.tmp $@

unpriv-epub: unpriv-isa.epub

unpriv-isa.epub: $(SRCDIR)/riscv-unprivileged.adoc
	@echo "Building Unprivileged ISA EPUB"
	@rm -f $@.tmp
	$(call maybe_run_with_docker, asciidoctor-epub3, $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<)
	@mv $@.tmp $@

clean:
	rm -f $(TARGETS) $(addsuffix .tmp,$(TARGETS))
