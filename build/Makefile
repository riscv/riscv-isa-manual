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
priv-pdf: riscv-privileged.pdf

riscv-privileged.pdf: $(SRCDIR)/riscv-privileged.adoc $(SRCDIR)/*.adoc
	@echo "Building Privileged ISA"
	rm -f $@.tmp
	asciidoctor-pdf $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<
	mv $@.tmp $@

# Unprivileged ISA build
unpriv-pdf: riscv-unprivileged.pdf

riscv-unprivileged.pdf: $(SRCDIR)/riscv-unprivileged.adoc $(SRCDIR)/*.adoc
	@echo "Building Unprivileged ISA"
	rm -f $@.tmp
	asciidoctor-pdf $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<
	mv $@.tmp $@

# Privileged ISA HTML build
priv-html: riscv-privileged.html

riscv-privileged.html: $(SRCDIR)/riscv-privileged.adoc
	@echo "Building Privileged ISA HTML"
	asciidoctor $(ASCIIDOCTOR_OPTS) --out-file=$@ $<

# Unprivileged ISA HTML build
unpriv-html: riscv-unprivileged.html

riscv-unprivileged.html: $(SRCDIR)/riscv-unprivileged.adoc
	@echo "Building Unprivileged ISA HTML"
	asciidoctor $(ASCIIDOCTOR_OPTS) --out-file=$@ $<

priv-epub: riscv-privileged.epub

riscv-privileged.epub: $(SRCDIR)/riscv-privileged.adoc
	@echo "Building Privileged ISA EPUB"
	asciidoctor-epub3 $(ASCIIDOCTOR_OPTS) --out-file=$@ $<

unpriv-epub: riscv-unprivileged.epub

riscv-unprivileged.epub: $(SRCDIR)/riscv-unprivileged.adoc
	@echo "Building Unprivileged ISA EPUB"
	asciidoctor-epub3 $(ASCIIDOCTOR_OPTS) --out-file=$@ $<

clean:
	@if [ -f riscv-privileged.pdf ]; then \
		echo "Removing riscv-privileged.pdf"; \
		rm -f riscv-privileged.pdf; \
	fi
	@if [ -f riscv-unprivileged.pdf ]; then \
		echo "Removing riscv-unprivileged.pdf"; \
		rm -f riscv-unprivileged.pdf; \
	fi
	@if [ -f riscv-privileged.html ]; then \
		echo "Removing riscv-privileged.html"; \
		rm -f riscv-privileged.html; \
	fi
	@if [ -f riscv-unprivileged.html ]; then \
		echo "Removing riscv-unprivileged.html"; \
		rm -f riscv-unprivileged.html; \
	fi
	@if [ -f riscv-privileged.epub ]; then \
		echo "Removing riscv-privileged.epub"; \
		rm -f riscv-privileged.epub; \
	fi
	@if [ -f riscv-unprivileged.epub ]; then \
		echo "Removing riscv-unprivileged.epub"; \
		rm -f riscv-unprivileged.epub; \
	fi
