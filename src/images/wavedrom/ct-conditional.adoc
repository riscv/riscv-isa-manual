//### Conditional Branches

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7', 'BRANCH', 'BRANCH', 'BRANCH'], type: 8},
  {bits: 5,  name: 'imm[4:1|11]',  attr: ['5', 'offset[4:1|11]', 'offset[4:1|11]', 'offset[4:1|11]'], type: 3},
  {bits: 3,  name: 'funct3',     attr: ['3', 'BEQ/BNE', 'BLT[U]', 'BGE[U]'], type: 8},
  {bits: 5,  name: 'rs1', attr: ['5', 'src1', 'src1', 'src1'], type: 4},
  {bits: 5,  name: 'rs2', attr: ['5', 'src2','src2', 'src2'], type: 4},
  {bits: 7,  name: 'imm[12|10:5]', attr: ['7', 'offset[12|10:5]', 'offset[12|10:5]', 'offset[12|10:5]'], type: 3},
], config:{fontsize: 10}}
....
