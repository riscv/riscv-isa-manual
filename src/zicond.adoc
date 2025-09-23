[[Zicond]]
== "Zicond" Extension for Integer Conditional Operations, Version 1.0.0

[[intro]]
=== Introduction
The Zicond extension defines a simple solution that provides most of the benefit and all of the flexibility one would desire to support conditional arithmetic and conditional-select/move operations, while remaining true to the RISC-V design philosophy.
The instructions follow the format for R-type instructions with 3 operands (i.e., 2 source operands and 1 destination operand).
Using these instructions, branchless sequences can be implemented (typically in two-instruction sequences) without the need for instruction fusion, special provisions during the decoding of architectural instructions, or other microarchitectural provisions.

One of the shortcomings of RISC-V, compared to competing instruction set architectures, is the absence of conditional operations to support branchless code-generation: this includes conditional arithmetic, conditional select and conditional move operations.
The design principles of RISC-V (e.g. the absence of an instruction-format that supports 3 source registers and an output register) make it unlikely that direct equivalents of the competing instructions will be introduced.

Yet, low-cost conditional instructions are a desirable feature as they allow the replacement of branches in a broad range of suitable situations (whether the branch turns out to be unpredictable or predictable) so as to reduce the capacity and aliasing pressures on BTBs and branch predictors, and to allow for longer basic blocks (for both the hardware and the compiler to work with).

=== Zicond specification

The "Conditional" operations extension provides a simple solution that provides most of the benefit and all of the flexibility one would desire to support conditional arithmetic and conditional-select/move operations, while remaining true to the RISC-V design philosophy.
The instructions follow the format for R-type instructions with 3 operands (i.e., 2 source operands and 1 destination operand).
Using these instructions, branchless sequences can be implemented (typically in two-instruction sequences) without the need for instruction fusion, special provisions during the decoding of architectural instructions, or other microarchitectural provisions.

The following instructions comprise the Zicond extension:

[%header,cols="^1,^1,4,8"]
|===
|RV32
|RV64
|Mnemonic
|Instruction

|&#10003;
|&#10003;
|czero.eqz _rd_, _rs1_, _rs2_
|<<#insns-czero-eqz>>

|&#10003;
|&#10003;
|czero.nez _rd_, _rs1_, _rs2_
|<<#insns-czero-nez>>

|===

[NOTE]
====
Architecture Comment: defining additional comparisons, in addition to equal-to-zero and not-equal-to-zero, does not offer a benefit due to the lack of immediates or an additional register operand that the comparison takes place against. 
====

Based on these two instructions, synthetic instructions (i.e., short instruction sequences) for the following *conditional arithmetic* operations are supported:

* conditional add, if zero
* conditional add, if non-zero
* conditional subtract, if zero
* conditional subtract, if non-zero
* conditional bitwise-and, if zero
* conditional bitwise-and, if non-zero
* conditional bitwise-or, if zero
* conditional bitwise-or, if non-zero
* conditional bitwise-xor, if zero
* conditional bitwise-xor, if non-zero

Additionally, the following *conditional select* instructions are supported:

* conditional-select, if zero
* conditional-select, if non-zero

More complex conditions, such as comparisons against immediates, registers, single-bit tests, comparisons against ranges, etc. can be realized by composing these new instructions with existing instructions.

=== Instructions (in alphabetical order)

[#insns-czero-eqz,reftext="Conditional zero, if condition is equal to zero"]
==== czero.eqz

Synopsis::
Moves zero to a register _rd_, if the condition _rs2_ is equal to zero, otherwise moves _rs1_ to _rd_.

Mnemonic::
czero.eqz _rd_, _rs1_, _rs2_

Encoding::
[wavedrom, , svg]
....
{reg:[
    { bits:  7, name: 0x33, attr: ['OP'] },
    { bits:  5, name: 'rd' },
    { bits:  3, name: 0x5, attr: ['CZERO.EQZ']},
    { bits:  5, name: 'rs1', attr: ['value'] },
    { bits:  5, name: 'rs2', attr: ['condition'] },
    { bits:  7, name: 0x7, attr: ['CZERO'] },
]}
....

Description::
If _rs2_ contains the value zero, this instruction writes the value zero to _rd_.  Otherwise, this instruction copies the contents of _rs1_ to _rd_.

This instruction carries a syntactic dependency from both _rs1_ and _rs2_ to _rd_.
Furthermore, if the Zkt extension is implemented, this instruction's timing is independent of the data values in _rs1_ and _rs2_.

SAIL code::
[source,sail]
--
  let condition = X(rs2);
  result : xlenbits = if (condition == zeros()) then zeros()
                                                else X(rs1);
  X(rd) = result;
--

<<<

[#insns-czero-nez,reftext="Conditional zero, if condition is nonzero"]
==== czero.nez

Synopsis::
Moves zero to a register _rd_, if the condition _rs2_ is nonzero, otherwise moves _rs1_ to _rd_.

Mnemonic::
czero.nez _rd_, _rs1_, _rs2_

Encoding::
[wavedrom, , svg]
....
{reg:[
    { bits:  7, name: 0x33, attr: ['OP'] },
    { bits:  5, name: 'rd' },
    { bits:  3, name: 0x7, attr: ['CZERO.NEZ']},
    { bits:  5, name: 'rs1', attr: ['value'] },
    { bits:  5, name: 'rs2', attr: ['condition'] },
    { bits:  7, name: 0x7, attr: ['CZERO'] },
]}
....

Description::
If _rs2_ contains a nonzero value, this instruction writes the value zero to _rd_.  Otherwise, this instruction copies the contents of _rs1_ to _rd_.

This instruction carries a syntactic dependency from both _rs1_ and _rs2_ to _rd_.
Furthermore, if the Zkt extension is implemented, this instruction's timing is independent of the data values in _rs1_ and _rs2_.

SAIL code::
[source,sail]
--
  let condition = X(rs2);
  result : xlenbits = if (condition != zeros()) then zeros()
                                                else X(rs1);
  X(rd) = result;
--

=== Usage examples

The instructions from this extension can be used to construct sequences that perform conditional-arithmetic, conditional-bitwise-logical, and conditional-select operations.

==== Instruction sequences

[%header,cols="4,.^3l,^2"]
|===
|Operation
|Instruction sequence
|Length

|*Conditional add, if zero* +
`rd = (rc == 0) ? (rs1 + rs2) : rs1`
|czero.nez  rd, rs2, rc
add        rd, rs1, rd
.8+.^|2 insns

|*Conditional add, if non-zero* +
`rd = (rc != 0) ? (rs1 + rs2) : rs1`
|czero.eqz  rd, rs2, rc
add        rd, rs1, rd

|*Conditional subtract, if zero* +
`rd = (rc == 0) ? (rs1 - rs2) : rs1`
|czero.nez  rd, rs2, rc
sub        rd, rs1, rd

|*Conditional subtract, if non-zero* +
`rd = (rc != 0) ? (rs1 - rs2) : rs1`
|czero.eqz  rd, rs2, rc
sub        rd, rs1, rd

|*Conditional bitwise-or, if zero* +
`rd = (rc == 0) ? (rs1 \| rs2) : rs1`
|czero.nez  rd, rs2, rc
or         rd, rs1, rd

|*Conditional bitwise-or, if non-zero* +
`rd = (rc != 0) ? (rs1 \| rs2) : rs1`
|czero.eqz  rd, rs2, rc
or         rd, rs1, rd

|*Conditional bitwise-xor, if zero* +
`rd = (rc == 0) ? (rs1 ^ rs2) : rs1`
|czero.nez  rd, rs2, rc
xor        rd, rs1, rd

|*Conditional bitwise-xor, if non-zero* +
`rd = (rc != 0) ? (rs1 ^ rs2) : rs1`
|czero.eqz  rd, rs2, rc
xor        rd, rs1, rd

|*Conditional bitwise-and, if zero* +
`rd = (rc == 0) ? (rs1 & rs2) : rs1`
|and        rd, rs1, rs2
czero.eqz  rtmp, rs1, rc
or         rd, rd, rtmp
.4+.^|3 insns +
(requires 1 temporary)

|*Conditional bitwise-and, if non-zero* +
`rd = (rc != 0) ? (rs1 & rs2) : rs1`
|and        rd, rs1, rs2
czero.nez  rtmp, rs1, rc
or         rd, rd, rtmp

|*Conditional select, if zero* +
`rd = (rc == 0) ? rs1 : rs2`
|czero.nez  rd, rs1, rc
czero.eqz  rtmp, rs2, rc
or         rd, rd, rtmp

|*Conditional select, if non-zero* +
`rd = (rc != 0) ? rs1 : rs2`
|czero.eqz  rd, rs1, rc
czero.nez  rtmp, rs2, rc
or         rd, rd, rtmp

|===