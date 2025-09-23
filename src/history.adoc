[[history]]
== History and Acknowledgments

=== "Why Develop a new ISA?" Rationale from Berkeley Group

We developed RISC-V to support our own needs in research and education,
where our group is particularly interested in actual hardware
implementations of research ideas (we have completed eleven different
silicon fabrications of RISC-V since the first edition of this
specification), and in providing real implementations for students to
explore in classes (RISC-V processor RTL designs have been used in
multiple undergraduate and graduate classes at Berkeley). In our current
research, we are especially interested in the move towards specialized
and heterogeneous accelerators, driven by the power constraints imposed
by the end of conventional transistor scaling. We wanted a highly
flexible and extensible base ISA around which to build our research
effort.

A question we have been repeatedly asked is "Why develop a new ISA?"
The biggest obvious benefit of using an existing commercial ISA is the
large and widely supported software ecosystem, both development tools
and ported applications, which can be leveraged in research and
teaching. Other benefits include the existence of large amounts of
documentation and tutorial examples. However, our experience of using
commercial instruction sets for research and teaching is that these
benefits are smaller in practice, and do not outweigh the disadvantages:

* *Commercial ISAs are proprietary.* Except for SPARC V8, which is an
open IEEE standard cite:[sparcieee1994] , most owners of commercial ISAs carefully guard
their intellectual property and do not welcome freely available
competitive implementations. This is much less of an issue for academic
research and teaching using only software simulators, but has been a
major concern for groups wishing to share actual RTL implementations. It
is also a major concern for entities who do not want to trust the few
sources of commercial ISA implementations, but who are prohibited from
creating their own clean room implementations. We cannot guarantee that
all RISC-V implementations will be free of third-party patent
infringements, but we can guarantee we will not attempt to sue a RISC-V
implementor.
* *Commercial ISAs are only popular in certain market domains.* The most
obvious examples at time of writing are that the ARM architecture is not
well supported in the server space, and the Intel x86 architecture (or
for that matter, almost every other architecture) is not well supported
in the mobile space, though both Intel and ARM are attempting to enter
each other's market segments. Another example is ARC and Tensilica,
which provide extensible cores but are focused on the embedded space.
This market segmentation dilutes the benefit of supporting a particular
commercial ISA as in practice the software ecosystem only exists for
certain domains, and has to be built for others.
* *Commercial ISAs come and go.* Previous research infrastructures have
been built around commercial ISAs that are no longer popular (SPARC,
MIPS) or even no longer in production (Alpha). These lose the benefit of
an active software ecosystem, and the lingering intellectual property
issues around the ISA and supporting tools interfere with the ability of
interested third parties to continue supporting the ISA. An open ISA
might also lose popularity, but any interested party can continue using
and developing the ecosystem.
* *Popular commercial ISAs are complex.* The dominant commercial ISAs
(x86 and ARM) are both very complex to implement in hardware to the
level of supporting common software stacks and operating systems. Worse,
nearly all the complexity is due to bad, or at least outdated, ISA
design decisions rather than features that truly improve efficiency.
* *Commercial ISAs alone are not enough to bring up applications.* Even
if we expend the effort to implement a commercial ISA, this is not
enough to run existing applications for that ISA. Most applications need
a complete ABI (application binary interface) to run, not just the
user-level ISA. Most ABIs rely on libraries, which in turn rely on
operating system support. To run an existing operating system requires
implementing the supervisor-level ISA and device interfaces expected by
the OS. These are usually much less well-specified and considerably more
complex to implement than the user-level ISA.
* *Popular commercial ISAs were not designed for extensibility.* The
dominant commercial ISAs were not particularly designed for
extensibility, and as a consequence have added considerable instruction
encoding complexity as their instruction sets have grown. Companies such
as Tensilica (acquired by Cadence) and ARC (acquired by Synopsys) have
built ISAs and toolchains around extensibility, but have focused on
embedded applications rather than general-purpose computing systems.
* *A modified commercial ISA is a new ISA.* One of our main goals is to
support architecture research, including major ISA extensions. Even
small extensions diminish the benefit of using a standard ISA, as
compilers have to be modified and applications rebuilt from source code
to use the extension. Larger extensions that introduce new architectural
state also require modifications to the operating system. Ultimately,
the modified commercial ISA becomes a new ISA, but carries along all the
legacy baggage of the base ISA.

Our position is that the ISA is perhaps the most important interface in
a computing system, and there is no reason that such an important
interface should be proprietary. The dominant commercial ISAs are based
on instruction-set concepts that were already well known over 30 years
ago. Software developers should be able to target an open standard
hardware target, and commercial processor designers should compete on
implementation quality.

We are far from the first to contemplate an open ISA design suitable for
hardware implementation. We also considered other existing open ISA
designs, of which the closest to our goals was the OpenRISC
architecture cite:[openriscarch]. We decided against adopting the OpenRISC ISA for several
technical reasons:

* OpenRISC has condition codes and branch delay slots, which complicate
higher performance implementations.
* OpenRISC uses a fixed 32-bit encoding and 16-bit immediates, which
precludes a denser instruction encoding and limits space for later
expansion of the ISA.
* OpenRISC does not support the 2008 revision to the IEEE 754
floating-point standard.
* The OpenRISC 64-bit design had not been completed when we began.

By starting from a clean slate, we could design an ISA that met all of
our goals, though of course, this took far more effort than we had
planned at the outset. We have now invested considerable effort in
building up the RISC-V ISA infrastructure, including documentation,
compiler tool chains, operating system ports, reference ISA simulators,
FPGA implementations, efficient ASIC implementations, architecture test
suites, and teaching materials. Since the last edition of this manual,
there has been considerable uptake of the RISC-V ISA in both academia
and industry, and we have created the non-profit RISC-V Foundation to
protect and promote the standard. The RISC-V Foundation website at
https://riscv.org contains the latest information on the Foundation
membership and various open-source projects using RISC-V.

=== History from Revision 1.0 of ISA manual

The RISC-V ISA and instruction-set manual builds upon several earlier
projects. Several aspects of the supervisor-level machine and the
overall format of the manual date back to the T0 (Torrent-0) vector
microprocessor project at UC Berkeley and ICSI, begun in 1992. T0 was a
vector processor based on the MIPS-II ISA, with Krste Asanović as main
architect and RTL designer, and Brian Kingsbury and Bertrand Irrisou as
principal VLSI implementors. David Johnson at ICSI was a major
contributor to the T0 ISA design, particularly supervisor mode, and to
the manual text. John Hauser also provided considerable feedback on the
T0 ISA design.

The Scale (Software-Controlled Architecture for Low Energy) project at
MIT, begun in 2000, built upon the T0 project infrastructure, refined
the supervisor-level interface, and moved away from the MIPS scalar ISA
by dropping the branch delay slot. Ronny Krashinsky and Christopher
Batten were the principal architects of the Scale Vector-Thread
processor at MIT, while Mark Hampton ported the GCC-based compiler
infrastructure and tools for Scale.

A lightly edited version of the T0 MIPS scalar processor specification
(MIPS-6371) was used in teaching a new version of the MIT 6.371
Introduction to VLSI Systems class in the Fall 2002 semester, with Chris
Terman and Krste Asanović as lecturers. Chris Terman contributed most of
the lab material for the class (there was no TA!). The 6.371 class
evolved into the trial 6.884 Complex Digital Design class at MIT, taught
by Arvind and Krste Asanović in Spring 2005, which became a regular
Spring class 6.375. A reduced version of the Scale MIPS-based scalar
ISA, named SMIPS, was used in 6.884/6.375. Christopher Batten was the TA
for the early offerings of these classes and developed a considerable
amount of documentation and lab material based around the SMIPS ISA.
This same SMIPS lab material was adapted and enhanced by TA Yunsup Lee
for the UC Berkeley Fall 2009 CS250 VLSI Systems Design class taught by
John Wawrzynek, Krste Asanović, and John Lazzaro.

The Maven (Malleable Array of Vector-thread ENgines) project was a
second-generation vector-thread architecture. Its design was led by
Christopher Batten when he was an Exchange Scholar at UC Berkeley
starting in summer 2007. Hidetaka Aoki, a visiting industrial fellow
from Hitachi, gave considerable feedback on the early Maven ISA and
microarchitecture design. The Maven infrastructure was based on the
Scale infrastructure but the Maven ISA moved further away from the MIPS
ISA variant defined in Scale, with a unified floating-point and integer
register file. Maven was designed to support experimentation with
alternative data-parallel accelerators. Yunsup Lee was the main
implementor of the various Maven vector units, while Rimas Avižienis was
the main implementor of the various Maven scalar units. Yunsup Lee and
Christopher Batten ported GCC to work with the new Maven ISA.
Christopher Celio provided the initial definition of a traditional
vector instruction set ("Flood") variant of Maven.

Based on experience with all these previous projects, the RISC-V ISA
definition was begun in Summer 2010, with Andrew Waterman, Yunsup Lee,
Krste Asanović, and David Patterson as principal designers. An initial
version of the RISC-V 32-bit instruction subset was used in the UC
Berkeley Fall 2010 CS250 VLSI Systems Design class, with Yunsup Lee as
TA. RISC-V is a clean break from the earlier MIPS-inspired designs. John
Hauser contributed to the floating-point ISA definition, including the
sign-injection instructions and a register encoding scheme that permits
internal recoding of floating-point values.

=== History from Revision 2.0 of ISA manual

Multiple implementations of RISC-V processors have been completed,
including several silicon fabrications, as shown in
<<silicon, Fabricated RISC-V testchips table>>.

[[silicon]]
[%autowidth,float="center",align="center",cols="^,^,^,^",options="header",]
|===
|Name |Tapeout Date |Process |ISA
|Raven-1 |May 29, 2011 |ST 28nm FDSOI |RV64G1_Xhwacha1
|EOS14 |April 1, 2012 |IBM 45nm SOI |RV64G1p1_Xhwacha2
|EOS16 |August 17, 2012 |IBM 45nm SOI |RV64G1p1_Xhwacha2
|Raven-2 |August 22, 2012 |ST 28nm FDSOI |RV64G1p1_Xhwacha2
|EOS18 |February 6, 2013 |IBM 45nm SOI |RV64G1p1_Xhwacha2
|EOS20 |July 3, 2013 |IBM 45nm SOI |RV64G1p99_Xhwacha2
|Raven-3 |September 26, 2013 |ST 28nm SOI |RV64G1p99_Xhwacha2
|EOS22 |March 7, 2014 |IBM 45nm SOI |RV64G1p9999_Xhwacha3
|===

The first RISC-V processors to be fabricated were written in Verilog and
manufactured in a pre-production FDSOI technology from ST as the Raven-1
testchip in 2011. Two cores were developed by Yunsup Lee and Andrew
Waterman, advised by Krste Asanović, and fabricated together: 1) an RV64
scalar core with error-detecting flip-flops, and 2) an RV64 core with an
attached 64-bit floating-point vector unit. The first microarchitecture
was informally known as "TrainWreck", due to the short time available
to complete the design with immature design libraries.

Subsequently, a clean microarchitecture for an in-order decoupled RV64
core was developed by Andrew Waterman, Rimas Avižienis, and Yunsup Lee,
advised by Krste Asanović, and, continuing the railway theme, was
codenamed "Rocket" after George Stephenson's successful steam
locomotive design. Rocket was written in Chisel, a new hardware design
language developed at UC Berkeley. The IEEE floating-point units used in
Rocket were developed by John Hauser, Andrew Waterman, and Brian
Richards. Rocket has since been refined and developed further, and has
been fabricated two more times in FDSOI (Raven-2, Raven-3), and five
times in IBM SOI technology (EOS14, EOS16, EOS18, EOS20, EOS22) for a
photonics project. Work is ongoing to make the Rocket design available
as a parameterized RISC-V processor generator.

EOS14-EOS22 chips include early versions of Hwacha, a 64-bit IEEE
floating-point vector unit, developed by Yunsup Lee, Andrew Waterman,
Huy Vo, Albert Ou, Quan Nguyen, and Stephen Twigg, advised by Krste
Asanović. EOS16-EOS22 chips include dual cores with a cache-coherence
protocol developed by Henry Cook and Andrew Waterman, advised by Krste
Asanović. EOS14 silicon has successfully run at 1.25 GHz. EOS16 silicon suffered
from a bug in the IBM pad libraries. EOS18 and EOS20 have successfully
run at 1.35 GHz.

Contributors to the Raven testchips include Yunsup Lee, Andrew Waterman,
Rimas Avižienis, Brian Zimmer, Jaehwa Kwak, Ruzica Jevtić, Milovan
Blagojević, Alberto Puggelli, Steven Bailey, Ben Keller, Pi-Feng Chiu,
Brian Richards, Borivoje Nikolić, and Krste Asanović.

Contributors to the EOS testchips include Yunsup Lee, Rimas Avižienis,
Andrew Waterman, Henry Cook, Huy Vo, Daiwei Li, Chen Sun, Albert Ou,
Quan Nguyen, Stephen Twigg, Vladimir Stojanović, and Krste Asanović.

Andrew Waterman and Yunsup Lee developed the C++ ISA simulator
"Spike", used as a golden model in development and named after the
golden spike used to celebrate completion of the US transcontinental
railway. Spike has been made available as a BSD open-source project.

Andrew Waterman completed a Master's thesis with a preliminary design of
the RISC-V compressed instruction set cite:[waterman-ms].

Various FPGA implementations of the RISC-V have been completed,
primarily as part of integrated demos for the Par Lab project research
retreats. The largest FPGA design has 3 cache-coherent RV64IMA
processors running a research operating system. Contributors to the FPGA
implementations include Andrew Waterman, Yunsup Lee, Rimas Avižienis,
and Krste Asanović.

RISC-V processors have been used in several classes at UC Berkeley.
Rocket was used in the Fall 2011 offering of CS250 as a basis for class
projects, with Brian Zimmer as TA. For the undergraduate CS152 class in
Spring 2012, Christopher Celio used Chisel to write a suite of
educational RV32 processors, named "Sodor" after the island on which
"Thomas the Tank Engine" and friends live. The suite includes a
microcoded core, an unpipelined core, and 2, 3, and 5-stage pipelined
cores, and is publicly available under a BSD license. The suite was
subsequently updated and used again in CS152 in Spring 2013, with Yunsup
Lee as TA, and in Spring 2014, with Eric Love as TA. Christopher Celio
also developed an out-of-order RV64 design known as BOOM (Berkeley
Out-of-Order Machine), with accompanying pipeline visualizations, that
was used in the CS152 classes. The CS152 classes also used
cache-coherent versions of the Rocket core developed by Andrew Waterman
and Henry Cook.

Over the summer of 2013, the RoCC (Rocket Custom Coprocessor) interface
was defined to simplify adding custom accelerators to the Rocket core.
Rocket and the RoCC interface were used extensively in the Fall 2013
CS250 VLSI class taught by Jonathan Bachrach, with several student
accelerator projects built to the RoCC interface. The Hwacha vector unit
has been rewritten as a RoCC coprocessor.

Two Berkeley undergraduates, Quan Nguyen and Albert Ou, have
successfully ported Linux to run on RISC-V in Spring 2013.

Colin Schmidt successfully completed an LLVM backend for RISC-V 2.0 in
January 2014.

Darius Rad at Bluespec contributed soft-float ABI support to the GCC
port in March 2014.

John Hauser contributed the definition of the floating-point
classification instructions.

We are aware of several other RISC-V core implementations, including one
in Verilog by Tommy Thorn, and one in Bluespec by Rishiyur Nikhil.

=== Acknowledgments

Thanks to Christopher F. Batten, Preston Briggs, Christopher Celio,
David Chisnall, Stefan Freudenberger, John Hauser, Ben Keller, Rishiyur
Nikhil, Michael Taylor, Tommy Thorn, and Robert Watson for comments on
the draft ISA version 2.0 specification.

=== History from Revision 2.1

Uptake of the RISC-V ISA has been very rapid since the introduction of
the frozen version 2.0 in May 2014, with too much activity to record in
a short history section such as this. Perhaps the most important single
event was the formation of the non-profit RISC-V Foundation in August
2015. The Foundation will now take over stewardship of the official
RISC-V ISA standard, and the official website `riscv.org` is the best
place to obtain news and updates on the RISC-V standard.

=== Acknowledgments

Thanks to Scott Beamer, Allen J. Baum, Christopher Celio, David
Chisnall, Paul Clayton, Palmer Dabbelt, Jan Gray, Michael Hamburg, and
John Hauser for comments on the version 2.0 specification.

=== History from Revision 2.2

=== Acknowledgments

Thanks to Jacob Bachmeyer, Alex Bradbury, David Horner, Stefan O’Rear,
and Joseph Myers for comments on the version 2.1 specification.

=== History for Revision 2.3

Uptake of RISC-V continues at a breakneck pace.

John Hauser and Andrew Waterman contributed a hypervisor ISA extension
based upon a proposal from Paolo Bonzini.

Daniel Lustig, Arvind, Krste Asanović, Shaked Flur, Paul Loewenstein,
Yatin Manerkar, Luc Maranget, Margaret Martonosi, Vijayanand Nagarajan,
Rishiyur Nikhil, Jonas Oberhauser, Christopher Pulte, Jose Renau, Peter
Sewell, Susmit Sarkar, Caroline Trippel, Muralidaran Vijayaraghavan,
Andrew Waterman, Derek Williams, Andrew Wright, and Sizhuo Zhang
contributed the memory consistency model.

=== Funding

Development of the RISC-V architecture and implementations has been
partially funded by the following sponsors.

* *Par Lab:* Research supported by Microsoft (Award # 024263) and Intel
(Award # 024894) funding and by matching funding by U.C. Discovery (Award
# DIG07-10227). Additional support came from Par Lab affiliates Nokia,
NVIDIA, Oracle, and Samsung.
* *Project Isis:* DoE Award DE-SC0003624.
* *ASPIRE Lab*: DARPA PERFECT program, Award HR0011-12-2-0016. DARPA
POEM program Award HR0011-11-C-0100. The Center for Future Architectures
Research (C-FAR), a STARnet center funded by the Semiconductor Research
Corporation. Additional support from ASPIRE industrial sponsor, Intel,
and ASPIRE affiliates, Google, Hewlett Packard Enterprise, Huawei,
Nokia, NVIDIA, Oracle, and Samsung.

The content of this paper does not necessarily reflect the position or
the policy of the US government and no official endorsement should be
inferred.
