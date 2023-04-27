[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7', 'OP-IMM', 'OP-IMM', 'OP-IMM'], type: 8},
  {bits: 5,  name: 'rd',        attr: ['5', 'dest', 'dest', 'dest'], type: 2},
  {bits: 3,  name: 'funct3',    attr: ['3', 'SLLI', 'SRLI', 'SRAI'], type: 8},
  {bits: 5,  name: 'rs1',       attr: ['5', 'src', 'src', 'src'], type: 4},
  {bits: 6,  name: 'imm[5:0]',  attr: ['6', 'shamt[5:0]', 'shamt[5:0]', 'shamt[5:0]'], type: 3},
  {bits: 6,  name: 'imm[11:6]', attr: ['6', '000000', '000000', '010000'], type: 8}
]}
....
