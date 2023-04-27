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
TARGETS := priv unpriv priv-html unpriv-html priv-latex unpriv-latex

# Declare phony targets
.PHONY: all $(TARGETS) clean

# Default target builds all
all: $(TARGETS)

# Asciidoctor options
ASCIIDOCTOR_OPTS := --attribute=mathematical-format=svg \
                    --failure-level=ERROR \
                    --require=asciidoctor-bibtex \
                    --require=asciidoctor-diagram \
                    --require=asciidoctor-mathematical \
                    --trace

# Source directory
SRCDIR := ../src

# LaTeX source and related files
SRCS := $(wildcard $(SRCDIR)/latex/*.tex)
FIGS := $(wildcard $(SRCDIR)/latex/figs/*)
BIBS := $(SRCDIR)/latex/riscv-spec.bib

# LaTeX build tools
PDFLATEX := TEXINPUTS=$(SRCDIR)/latex: pdflatex -interaction=nonstopmode -halt-on-error
BIBTEX := BIBINPUTS=$(SRCDIR)/latex: bibtex

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

# LaTeX build for Privileged ISA
priv-latex: riscv-privileged.pdf

riscv-privileged.pdf: $(SRCDIR)/latex/riscv-privileged.tex $(SRCS) $(FIGS) $(BIBS)
	$(PDFLATEX) riscv-privileged
	$(BIBTEX) riscv-privileged
	$(PDFLATEX) riscv-privileged
	$(PDFLATEX) riscv-privileged
	
# LaTeX build for Unprivileged ISA
unpriv-latex: riscv-spec.pdf

riscv-spec.pdf: $(SRCDIR)/latex/riscv-spec.tex $(SRCS) $(FIGS) $(BIBS)
	$(PDFLATEX) riscv-privileged
	$(BIBTEX) riscv-privileged
	$(PDFLATEX) riscv-privileged
	$(PDFLATEX) riscv-privileged

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
	@echo "Cleaning up files from LaTeX build"
	@cd $(SRCDIR)/latex; \
	for file in $(JUNK); do \
		if [ -f "$$file" ]; then \
			echo "Removing $$file"; \
			rm -f "$$file"; \
		fi; \
	done
