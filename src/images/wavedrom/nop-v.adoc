//# NOP-V

The RISC-V [User-Level ISA Specification](https://riscv.org/specifications/) defines NOP instruction as follows:

* The NOP instruction does not change any user-visible state, except for advancing the pc.
* NOP is encoded as \`ADDI x0, x0, 0\`.

[wavedrom, , ]
----
{reg:[
    {name: 'opcode', bits: 7,  attr: 0b0010011},
    {name: 'rd',     bits: 5,  attr: 0},
    {name: 'funct3',  bits: 3,  attr: 0},
    {name: 'rs1',    bits: 5,  attr: 0},
    {name: 'imm',    bits: 12, attr: 0}
], config: {hspace: width}}
----


NOTE: NOPs can be used to align code segments to microarchitecturally significant address boundaries, or to leave space for inline code modifications. Although **there are many possible ways** to encode a NOP, we define a canonical NOP encoding to allow microarchitectural optimizations as well as for more readable disassembly output.

How many other possible ways to encode NOP?
----
rd = 0
----

Any Integer Computational instruction writing into \`x0\` is NOP.

`
