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
TARGETS := priv unpriv priv-html unpriv-html

# Declare phony targets
.PHONY: all $(TARGETS) clean

# Default target builds all
all: $(TARGETS)

# Build with preinstalled docker container; first install it with:
#   docker pull riscvintl/riscv-docs-base-container-image:latest
docker:
	cd .. && docker run -it -v .:/build riscvintl/riscv-docs-base-container-image:latest /bin/sh -c 'cd ./build; make $(MAKEFLAGS)'

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

# Temporary files to clean up for LaTeX build
JUNK := *.pdf *.aux *.log *.bbl *.blg *.toc *.out *.fdb_latexmk *.fls *.synctex.gz

# Privileged ISA build
priv: priv-isa-asciidoc.pdf

priv-isa-asciidoc.pdf: $(SRCDIR)/riscv-privileged.adoc $(SRCDIR)/*.adoc
	@echo "Building Privileged ISA"
	rm -f $@.tmp
	asciidoctor-pdf $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<
	mv $@.tmp $@

# Unprivileged ISA build
unpriv: unpriv-isa-asciidoc.pdf

unpriv-isa-asciidoc.pdf: $(SRCDIR)/riscv-unprivileged.adoc $(SRCDIR)/*.adoc
	@echo "Building Unprivileged ISA"
	rm -f $@.tmp
	asciidoctor-pdf $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<
	mv $@.tmp $@

# Privileged ISA HTML build
priv-html: priv-isa-asciidoc.html

priv-isa-asciidoc.html: $(SRCDIR)/riscv-privileged.adoc
	@echo "Building Privileged ISA HTML"
	asciidoctor $(ASCIIDOCTOR_OPTS) --out-file=$@ $<

# Unprivileged ISA HTML build
unpriv-html: unpriv-isa-asciidoc.html

unpriv-isa-asciidoc.html: $(SRCDIR)/riscv-unprivileged.adoc
	@echo "Building Unprivileged ISA HTML"
	asciidoctor $(ASCIIDOCTOR_OPTS) --out-file=$@ $<

clean:
	@if [ -f priv-isa-asciidoc.pdf ]; then \
		echo "Removing priv-isa-asciidoc.pdf"; \
		rm -f priv-isa-asciidoc.pdf; \
	fi
	@if [ -f unpriv-isa-asciidoc.pdf ]; then \
		echo "Removing unpriv-isa-asciidoc.pdf"; \
		rm -f unpriv-isa-asciidoc.pdf; \
	fi
	@if [ -f priv-isa-asciidoc.html ]; then \
		echo "Removing priv-isa-asciidoc.html"; \
		rm -f priv-isa-asciidoc.html; \
	fi
	@if [ -f unpriv-isa-asciidoc.html ]; then \
		echo "Removing unpriv-isa-asciidoc.html"; \
		rm -f unpriv-isa-asciidoc.html; \
	fi
