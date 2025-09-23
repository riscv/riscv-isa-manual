//### NOP Instruction
[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7', 'OP-IMM'], type: 8},
  {bits: 5,  name: 'rd',        attr: ['5', '0'], type: 2},
  {bits: 3,  name: 'funct3',     attr: ['3', 'ADDI'], type: 8},
  {bits: 5,  name: 'rs1',       attr: ['5', '0'], type: 4},
  {bits: 12, name: 'imm[11:0]', attr: ['12', '0'], type: 3}
]}
....
