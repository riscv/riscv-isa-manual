//## 2.4 Integer Computational Instructions
//### Integer Register-Immediate Instructions

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7', 'OP-IMM', 'OP-IMM'], type: 8},
  {bits: 5,  name: 'rd',        attr: ['5', 'dest', 'dest'], type: 2},
  {bits: 3,  name: 'funct3',     attr: ['3', 'ADDI/SLTI[U]', 'ANDI/ORI/XORI'], type: 8},
  {bits: 5,  name: 'rs1',       attr: ['5', 'src', 'src'], type: 4},
  {bits: 12, name: 'imm[11:0]', attr: ['12', 'I-immediate[11:0]', 'I-immediate[11:0]'], type: 3}
]}
....

//<snio>
