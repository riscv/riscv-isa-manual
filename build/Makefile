# Makefile

# Build Targets
TARGETS := priv unpriv

.PHONY: all $(TARGETS)

all: $(TARGETS)

ASCIIDOCTOR_OPTS := --attribute=mathematical-format=svg \
                    --failure-level=ERROR \
                    --require=asciidoctor-bibtex \
                    --require=asciidoctor-diagram \
                    --require=asciidoctor-mathematical \
                    --trace

SRCDIR := ../src

# Privilege ISA
priv: priv-isa-asciidoc.pdf

priv-isa-asciidoc.pdf: $(SRCDIR)/riscv-isa-unpr-conv-review.adoc
	@echo "Building Privilege ISA"
	asciidoctor-pdf $(ASCIIDOCTOR_OPTS) --out-file=$@ $<

# Unprivilege ISA
unpriv: unpriv-isa-asciidoc.pdf

unpriv-isa-asciidoc.pdf: $(SRCDIR)/riscv-isa-unpr-conv-review.adoc
	@echo "Building Unprivilege ISA"
	asciidoctor-pdf $(ASCIIDOCTOR_OPTS) --out-file=$@ $<

clean:
	@if [ -f priv-isa-asciidoc.pdf ]; then \
		echo "Removing priv-isa-asciidoc.pdf"; \
		rm -f priv-isa-asciidoc.pdf; \
	fi
	@if [ -f unpriv-isa-asciidoc.pdf ]; then \
		echo "Removing unpriv-isa-asciidoc.pdf"; \
		rm -f unpriv-isa-asciidoc.pdf; \
	fi
