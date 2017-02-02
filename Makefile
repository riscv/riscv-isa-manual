#=======================================================================
# Makefile for generating latex documents
#-----------------------------------------------------------------------
#
# This is a simple makefile for generating latex documents. It will
# run bibtex, generate eps from xfig figures, and make pdfs. The
# makefile supports builds in non-source directories: just make a
# build directory, copy the makefile there, and change the srcdir
# variable accordingly.
#
# Note that the makefile assumes that the default dvips/ps2pdfwr 
# commands "do the right thing" for fonts in pdfs. This is true on 
# Athena/Linux and Fedora Core but is not true for older redhat installs ...
#
# At a minimum you should just change the main variable to be
# the basename of your toplevel tex file. If you use a bibliography 
# then you should set the bibfile variable to be the name of your
# .bib file (assumed to be in the source directory).
#

srcdir  = .

docs_with_bib = riscv-spec riscv-privileged 
docs_without_bib =

srcs = $(wildcard *.tex)
figs = $(wildcard figs/*)
bibs = riscv-spec.bib

#=======================================================================
# You shouldn't need to change anything below this
#=======================================================================

default : pdf

#------------------------------------------------------------
# PDF

pdfs_with_bib = $(addsuffix .pdf, $(docs_with_bib))
pdfs_without_bib = $(addsuffix .pdf, $(docs_without_bib))
pdfs = $(pdfs_with_bib) $(pdfs_without_bib)

pdf : $(pdfs)
.PHONY: pdf open

open: $(pdfs)
	open $(pdfs)

$(pdfs_with_bib): %.pdf: %.tex $(srcs) $(figs) $(bibs)
	pdflatex $*
	bibtex $*
	pdflatex $*
	pdflatex $*

$(pdfs_without_bib): %.pdf: %.tex $(srcs) $(figs)
	pdflatex $*
	pdflatex $*

junk += $(pdfs) *.aux *.log *.bbl *.blg *.toc *.out

#------------------------------------------------------------
# Other Targets

clean :
	rm -rf $(junk) *~ \#*
