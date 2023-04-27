//# 6 RV64I Base Integer Instruction Set, Version 2.1
//## 6.2 Integer Computational Instructions
//### Integer Register-Immediate Instructions

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7', 'OP-IMM-32'], type: 8},
  {bits: 5,  name: 'rd',        attr: ['5', 'dest'], type: 2},
  {bits: 3,  name: 'funct3',     attr: ['3', 'ADDIW'], type: 8},
  {bits: 5,  name: 'rs1',       attr: ['5', 'src'], type: 4},
  {bits: 12, name: 'imm[11:0]', attr: ['12', 'I-immediate[11:0]'], type: 3}
]}
....

