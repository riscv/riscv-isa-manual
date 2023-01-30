#HEADER_SOURCE := ../src/riscv-privileged.adoc
HEADER_SOURCE := ../src/riscv-isa-unpr-conv-review.adoc
PDF_RESULT := priv-isa-asciidoc.pdf
#PDF_RESULT := unpriv-isa-asciidoc.pdf
# Not all document sources are yet listed here.  Not just adoc files but
# images/ and resources/ content.  Once they are the target can remove the
# phony use.
SOURCES := $(HEADER_SOURCE)

all: $(PDF_RESULT)

.PHONY: $(PDF_RESULT)
$(PDF_RESULT): $(SOURCES)
	asciidoctor-pdf \
    --attribute=mathematical-format=svg \
    --failure-level=ERROR \
    --require=asciidoctor-bibtex \
    --require=asciidoctor-diagram \
    --require=asciidoctor-mathematical \
    --trace \
    --out-file=$@ \
    $(HEADER_SOURCE)
