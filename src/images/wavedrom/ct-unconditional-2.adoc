//ct-unconditional-2

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',     attr: ['7', 'JALR'], type: 8},
  {bits: 5,  name: 'rd',         attr: ['5', 'dest'], type: 2},
  {bits: 3,  name: 'funct3',     attr: ['3', '0'], type: 8},
  {bits: 5,  name: 'rs1',        attr: ['5', 'base'], type: 4},
  {bits: 12, name: 'imm[11:0]',  attr: ['12', 'offset[11:0]'], type: 3},
]}
....
