[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7', 'OP-IMM-32', 'OP-IMM-32', 'OP-IMM-32'], type: 8},
  {bits: 5,  name: 'rd',        attr: ['5', 'dest', 'dest', 'dest'], type: 2},
  {bits: 3,  name: 'funct3',    attr: ['3', 'SLLIW', 'SRLIW', 'SRAIW'], type: 8},
  {bits: 5,  name: 'rs1',       attr: ['5', 'src', 'src', 'src'], type: 4},
  {bits: 5,  name: 'imm[4:0]',  attr: ['5', 'shamt[4:0]', 'shamt[4:0]', 'shamt[4:0]'], type: 3},
  {bits: 1,  name: '[5]',    attr: ['1', '0', '0', '0'], type: 3},
  {bits: 6,  name: 'imm[11:6]', attr: ['6', '000000', '000000', '010000'], type: 8}
]}
....
