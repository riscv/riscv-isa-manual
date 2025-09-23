[[risc-v-isa]]
= The RISC-V Instruction Set Manual: Volume II: Privileged Architecture
:description: Volume II - Privileged Architecture
:company: RISC-V.org
:revnumber: 20240411
//:revremark: Pre-release version
//development: assume everything can change
//stable: assume everything could change
//frozen: of you implement this version you assume the risk that something might change because of the public review cycle  but we expect little to no change.
//ratified: you can implement this and be assured nothing will change. if something needs to change due to an errata or enhancement, it will come out in a new extension. we do not revise extensions.
:url-riscv: http://riscv.org
:doctype: book
:colophon:
:pdf-theme: ../src/resources/themes/riscv-spec.yml
:pdf-fontsdir: ../src/resources/fonts/
:preface-title: Preamble
:appendix-caption: Appendix
:imagesdir: images
:title-logo-image: image:risc-v_logo.png[pdfwidth=3.25in,align=center]
//:page-background-image: image:draft.png[opacity=20%]
//:title-page-background-image: none
//:back-cover-image: image:backpage.png[opacity=25%]
// Settings:
:experimental:
:reproducible:
:imagesoutdir: images
:bibtex-file: ../src/resources/riscv-spec.bib
:bibtex-order: alphabetical
:bibtex-style: apa
:bibtex-format: asciidoc
:bibtex-throw: false
:icons: font
:lang: en
:listing-caption: Example
:sectnums:
:sectnumlevels: 5
:toc: left
:toclevels: 4 
:source-highlighter: pygments
ifdef::backend-pdf[]
:source-highlighter: rouge
endif::[]
:table-caption: Table
:figure-caption: Figure
:xrefstyle: short 
:chapter-refsig: Chapter
:section-refsig: Section
:appendix-refsig: Appendix
:data-uri:
:hide-uri-scheme:
:stem: latexmath
:footnote:
:le: &#8804;
:ge: &#8805;
:ne: &#8800;
:approx: &#8776;
:inf: &#8734;

_Contributors to all versions of the spec in alphabetical order (please contact
editors to suggest corrections): Krste Asanović, Peter Ashenden, Rimas
Avižienis, Jacob Bachmeyer, Allen J. Baum, Jonathan Behrens, Paolo Bonzini, Ruslan Bukin,
Christopher Celio, Chuanhua Chang, David Chisnall, Anthony Coulter, Palmer Dabbelt, Monte
Dalrymple, Paul Donahue, Greg Favor, Dennis Ferguson,  Marc Gauthier, Andy Glew,
Gary Guo, Mike Frysinger, John Hauser, David Horner, Olof
Johansson, David Kruckemyer, Yunsup Lee, Daniel Lustig, Andrew Lutomirski, Prashanth Mundkur,
Jonathan Neuschäfer, Rishiyur
Nikhil, Stefan O'Rear, Albert Ou, John Ousterhout, David Patterson, Dmitri
Pavlov, Kade Phillips, Josh Scheid, Colin Schmidt, Michael Taylor, Wesley Terpstra, Matt Thomas, Tommy Thorn, Ray
VanDeWalker, Megan Wachs, Steve Wallach, Andrew Waterman, Claire Wolf,
and Reinoud Zandijk.._

_This document is released under a Creative Commons Attribution 4.0 International License._

_This document is a derivative of the RISC-V
privileged specification version 1.9.1 released under following license: ©2010-2017 Andrew Waterman, Yunsup Lee, Rimas
Avižienis, 
David Patterson, Krste Asanović. Creative Commons Attribution 4.0 International License._

include::priv-preface.adoc[]
include::priv-intro.adoc[]
include::priv-csrs.adoc[]
include::machine.adoc[]
include::smstateen.adoc[]
include::indirect-csr.adoc[]
include::smepmp.adoc[]
include::smcntrpmf.adoc[]
include::rnmi.adoc[]
include::smcdeleg.adoc[]
include::supervisor.adoc[]
include::sstc.adoc[]
include::sscofpmf.adoc[]
include::hypervisor.adoc[]
include::priv-insns.adoc[]
include::priv-history.adoc[]
include::bibliography.adoc[]
