[[naming]]
== ISA Extension Naming Conventions

This chapter describes the RISC-V ISA extension naming scheme that is
used to concisely describe the set of instructions present in a hardware
implementation, or the set of instructions used by an application binary
interface (ABI).
[NOTE]
====
The RISC-V ISA is designed to support a wide variety of implementations
with various experimental instruction-set extensions. We have found that
an organized naming scheme simplifies software tools and documentation.
====
=== Case Sensitivity

The ISA naming strings are case insensitive.

=== Base Integer ISA

RISC-V ISA strings begin with either RV32I, RV32E, RV64I, RV64E, or RV128I
indicating the supported address space size in bits for the base integer
ISA.

=== Instruction-Set Extension Names

Standard ISA extensions are given a name consisting of a single letter.
For example, the first four standard extensions to the integer bases
are: "M" for integer multiplication and division, "A" for atomic
memory instructions, "F" for single-precision floating-point
instructions, and "D" for double-precision floating-point
instructions. Any RISC-V instruction-set variant can be succinctly
described by concatenating the base integer prefix with the names of the
included extensions, e.g., "RV64IMAFD".

We have also defined an abbreviation "G" to represent the
"IMAFDZicsr_Zifencei" base and extensions, as this is intended to
represent our standard general-purpose ISA.

Standard extensions to the RISC-V ISA are given other reserved letters,
e.g., "Q" for quad-precision floating-point, or "C" for the 16-bit
compressed instruction format.

Some ISA extensions depend on the presence of other extensions, e.g.,
"D" depends on "F" and "F" depends on "Zicsr". These dependencies
may be implicit in the ISA name: for example, RV32IF is equivalent to
RV32IFZicsr, and RV32ID is equivalent to RV32IFD and RV32IFDZicsr.

=== Version Numbers

Recognizing that instruction sets may expand or alter over time, we
encode extension version numbers following the extension name. Version
numbers are divided into major and minor version numbers, separated by a
"p". If the minor version is "0", then "p0" can be omitted from
the version string. Changes in major version numbers imply a loss of
backwards compatibility, whereas changes in only the minor version
number must be backwards-compatible. For example, the original 64-bit
standard ISA defined in release 1.0 of this manual can be written in
full as "RV64I1p0M1p0A1p0F1p0D1p0", more concisely as
"RV64I1M1A1F1D1".

We introduced the version numbering scheme with the second release.
Hence, we define the default version of a standard extension to be the
version present at that time, e.g., "RV32I" is equivalent to
"RV32I2".

=== Underscores

Underscores "_" may be used to separate ISA extensions to improve
readability and to provide disambiguation, e.g., "RV32I2_M2_A2".

Because the "P" extension for Packed SIMD can be confused for the
decimal point in a version number, it must be preceded by an underscore
if it follows a number. For example, "rv32i2p2" means version 2.2 of
RV32I, whereas "rv32i2_p2" means version 2.0 of RV32I with version 2.0
of the P extension.

=== Additional Standard Extension Names

Standard extensions can also be named using a single "Z" followed by
an alphabetical name and an optional version number. For example,
"Zifencei" names the instruction-fetch fence extension described in
<<zifencei>>; "Zifencei2" and
"Zifencei2p0" name version 2.0 of same.

The first letter following the "Z" conventionally indicates the most
closely related alphabetical extension category, IMAFDQCVH. For the
"Zfa" extension for additional floating-point instructions, for example, the letter "f"
indicates the extension is related to the "F" standard extension. If
multiple "Z" extensions are named, they should be ordered first by
category, then alphabetically within a category—for example,
"Zicsr_Zifencei_Zam".

All multi-letter extensions, including those with the "Z" prefix, must be
separated from other multi-letter extensions by an underscore, e.g.,
"RV32IMACZicsr_Zifencei".

=== Supervisor-level Instruction-Set Extensions

Standard extensions that extend the supervisor-level virtual-memory
architecture are prefixed with the letters "Sv", followed by an alphabetical
name and an optional version number, or by a numeric name with no version number.
Other standard extensions that extend
the supervisor-level architecture are prefixed with the letters "Ss",
followed by an alphabetical name and an optional version number.  Such
extensions are defined in Volume II.

Standard supervisor-level extensions should be listed after standard
unprivileged extensions. If multiple supervisor-level extensions are
listed, they should be ordered alphabetically.

=== Hypervisor-level Instruction-Set Extensions

Standard extensions that extend the hypervisor-level architecture are prefixed
with the letters "Sh".
If multiple hypervisor-level extensions are listed, they should be ordered
alphabetically.

NOTE: Many augmentations to the hypervisor-level archtecture are more
naturally defined as supervisor-level extensions, following the scheme
described in the previous section.
The "Sh" prefix is used by the few hypervisor-level extensions that have no
supervisor-visible effects.

=== Machine-level Instruction-Set Extensions

Standard machine-level instruction-set extensions are prefixed with the
letters "Sm".

Standard machine-level extensions should be listed after standard
lesser-privileged extensions. If multiple machine-level extensions are
listed, they should be ordered alphabetically.

=== Non-Standard Extension Names

Non-standard extensions are named using a single "X" followed by an
alphabetical name and an optional version number. For example,
"Xhwacha" names the Hwacha vector-fetch ISA extension; "Xhwacha2"
and "Xhwacha2p0" name version 2.0 of same.

Non-standard extensions must be listed after all standard extensions, and,
like other multi-letter extensions, must be separated from other multi-letter
extensions by an underscore.
For example, an ISA with non-standard extensions Argle and
Bargle may be named "RV64IZifencei_Xargle_Xbargle".

If multiple non-standard extensions are listed, they should be ordered
alphabetically.

=== Subset Naming Convention

<<isanametable>> summarizes the standardized extension
names. The table also defines the canonical
order in which extension names must appear in the name string, with
top-to-bottom in table indicating first-to-last in the name string,
e.g., RV32IMACV is legal, whereas RV32IMAVC is not.

[[isanametable]]
.Standard ISA extension names.
[%autowidth,float="center",align="center",cols="<,^,^",options="header",]
|===
|Subset |Name |Implies

|Base ISA | |

|Integer |I |

|Reduced Integer |E |

3+|*Standard Unprivileged Extensions*

|Integer Multiplication and Division |M |Zmmul

|Atomics |A |

|Single-Precision Floating-Point |F |Zicsr

|Double-Precision Floating-Point |D |F

|General |G |IMAFDZicsr_Zifencei

|Quad-Precision Floating-Point |Q |D

|16-bit Compressed Instructions |C |

|B Extension |B |

|Packed-SIMD Extensions |P |

|Vector Extension |V |D

|Hypervisor Extension |H |

|Control and Status Register Access |Zicsr |

|Instruction-Fetch Fence |Zifencei |

|Total Store Ordering |Ztso |

3+|*Standard Supervisor-Level Extensions*

|Supervisor-level extension "def" |Ssdef |

3+|*Standard Machine-Level Extensions*

|Machine-level extension "jkl" |Smjkl |

3+|*Non-Standard Extensions*

|Non-standard extension "mno" |Xmno |
|===
