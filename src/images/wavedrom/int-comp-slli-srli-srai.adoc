//FROM ## 2.4 Integer Computational Instructions
//### Integer Register-Immediate Instructions
//

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7', 'OP-IMM', 'OP-IMM', 'OP-IMM'], type: 8},
  {bits: 5,  name: 'rd',        attr: ['5', 'dest', 'dest', 'dest'], type: 2},
  {bits: 3,  name: 'funct3',     attr: ['3', 'SLLI', 'SRLI', 'SRAI'], type: 8},
  {bits: 5,  name: 'rs1',       attr: ['5', 'src', 'src', 'src'], type: 4},
  {bits: 5,  name: 'imm[4:0]',  attr: ['5', 'shamt[4:0]', 'shamt[4:0]', 'shamt[4:0]'], type: 3},
  {bits: 7,  name: 'imm[11:5]', attr: ['7', 0, 0, 32], type: 8}
]}
....


