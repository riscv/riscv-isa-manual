HEADER_SOURCE := ../src/riscv-isa-unpr-conv-review.adoc
PDF_RESULT := unpriv-isa-asciidoc.pdf
# Not all document sources are yet listed here.  Not just adoc files but
# images/ and resources/ content.  Once they are the target can remove the
# phony use.
SOURCES := $(HEADER_SOURCE)
PDF-THEME := ../src/resources/themes/riscv-spec.yml

all: $(PDF_RESULT)

.PHONY: $(PDF_RESULT)
$(PDF_RESULT): $(SOURCES)
	asciidoctor-pdf \
    --attribute=mathematical-format=svg \
    --attribute=pdf-fontsdir=../src/resources/fonts \
    --attribute=pdf-theme=../src/resources/themes/riscv-spec.yml \
    --theme default-with-font-fallbacks \
    --failure-level=ERROR \
    --require=asciidoctor-bibtex \
    --require=asciidoctor-diagram \
    --require=asciidoctor-mathematical \
    --trace \
    --out-file=$@ \
    $(HEADER_SOURCE)
