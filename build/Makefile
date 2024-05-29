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
TARGETS_PDF := priv-pdf unpriv-pdf
TARGETS_HTML := priv-html unpriv-html
TARGETS_EPUB := priv-epub unpriv-epub
TARGETS := $(TARGETS_PDF) $(TARGETS_HTML) $(TARGETS_EPUB)

# Declare phony targets
.PHONY: all $(TARGETS) clean

# Default target builds all
all: $(TARGETS)

# Build with preinstalled docker container; first install it with:
#   docker pull riscvintl/riscv-docs-base-container-image:latest
docker:
	cd .. && docker run -it -v `pwd`:/build riscvintl/riscv-docs-base-container-image:latest /bin/sh -c 'export LANG=C.utf8; cd ./build; make -$(MAKEFLAGS) $(TARGETS)'

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
priv-pdf: priv-isa.pdf

priv-isa.pdf: $(SRCDIR)/riscv-privileged.adoc $(SRCDIR)/*.adoc
	@echo "Building Privileged ISA"
	rm -f $@.tmp
	asciidoctor-pdf $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<
	mv $@.tmp $@

# Unprivileged ISA build
unpriv-pdf: unpriv-isa.pdf

unpriv-isa.pdf: $(SRCDIR)/riscv-unprivileged.adoc $(SRCDIR)/*.adoc
	@echo "Building Unprivileged ISA"
	rm -f $@.tmp
	asciidoctor-pdf $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<
	mv $@.tmp $@

# Privileged ISA HTML build
priv-html: priv-isa.html

priv-isa.html: $(SRCDIR)/riscv-privileged.adoc
	@echo "Building Privileged ISA HTML"
	asciidoctor $(ASCIIDOCTOR_OPTS) --out-file=$@ $<

# Unprivileged ISA HTML build
unpriv-html: unpriv-isa.html

unpriv-isa.html: $(SRCDIR)/riscv-unprivileged.adoc
	@echo "Building Unprivileged ISA HTML"
	asciidoctor $(ASCIIDOCTOR_OPTS) --out-file=$@ $<

priv-epub: priv-isa.epub

priv-isa.epub: $(SRCDIR)/riscv-privileged.adoc
	@echo "Building Privileged ISA EPUB"
	asciidoctor-epub3 $(ASCIIDOCTOR_OPTS) --out-file=$@ $<

unpriv-epub: unpriv-isa.epub

unpriv-isa.epub: $(SRCDIR)/riscv-unprivileged.adoc
	@echo "Building Unprivileged ISA EPUB"
	asciidoctor-epub3 $(ASCIIDOCTOR_OPTS) --out-file=$@ $<

clean:
	@if [ -f priv-isa.pdf ]; then \
		echo "Removing priv-isa.pdf"; \
		rm -f priv-isa.pdf; \
	fi
	@if [ -f unpriv-isa.pdf ]; then \
		echo "Removing unpriv-isa.pdf"; \
		rm -f unpriv-isa.pdf; \
	fi
	@if [ -f priv-isa.html ]; then \
		echo "Removing priv-isa.html"; \
		rm -f priv-isa.html; \
	fi
	@if [ -f unpriv-isa.html ]; then \
		echo "Removing unpriv-isa.html"; \
		rm -f unpriv-isa.html; \
	fi
	@if [ -f priv-isa.epub ]; then \
		echo "Removing priv-isa.epub"; \
		rm -f priv-isa.epub; \
	fi
	@if [ -f unpriv-isa.epub ]; then \
		echo "Removing unpriv-isa.epub"; \
		rm -f unpriv-isa.epub; \
	fi
