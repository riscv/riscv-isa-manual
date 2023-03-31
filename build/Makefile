# Makefile

# Build Targets
TARGETS := priv-pdf unpriv-pdf priv-html unpriv-html

.PHONY: all $(TARGETS)

all: $(TARGETS)

ASCIIDOCTOR_OPTS := --attribute=mathematical-format=svg \
                    --failure-level=ERROR \
                    --require=asciidoctor-bibtex \
                    --require=asciidoctor-diagram \
                    --require=asciidoctor-mathematical \
                    --trace

SRCDIR := ../src

# Privileged ISA
priv: priv-isa-asciidoc.pdf

priv-isa-asciidoc.pdf: $(SRCDIR)/riscv-privileged.adoc $(SRCDIR)/*.adoc
	@echo "Building Privileged ISA"
	rm -f $@.tmp
	asciidoctor-pdf $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<
	mv $@.tmp $@

# Unprivileged ISA
unpriv: unpriv-isa-asciidoc.pdf

unpriv-isa-asciidoc.pdf: $(SRCDIR)/riscv-isa-unpr-conv-review.adoc $(SRCDIR)/*.adoc
	@echo "Building Unprivileged ISA"
	rm -f $@.tmp
	asciidoctor-pdf $(ASCIIDOCTOR_OPTS) --out-file=$@.tmp $<
	mv $@.tmp $@

# Privileged ISA HTML
priv-html: priv-isa-asciidoc.html

priv-isa-asciidoc.html: $(SRCDIR)/riscv-privileged.adoc
	@echo "Building Privilege ISA HTML"
	asciidoctor $(ASCIIDOCTOR_OPTS) --out-file=$@ $<

# Unprivileged ISA HTML
unpriv-html: unpriv-isa-asciidoc.html

unpriv-isa-asciidoc.html: $(SRCDIR)/riscv-isa-unpr-conv-review.adoc
	@echo "Building Unprivilege ISA HTML"
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
