
//rv64i int-reg-reg
//### Integer Register-Register Operations

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7', 'OP', 'OP', 'OP-32', 'OP-32', 'OP-32'], type: 8},
  {bits: 5,  name: 'rd',        attr: ['5', 'dest', 'dest', 'dest', 'dest', 'dest'], type: 2},
  {bits: 3,  name: 'funct3',    attr: ['3', 'SLL/SRL', 'SRA', 'ADDW', 'SLLW/SRLW', 'SUBW/SRAW'], type: 8},
  {bits: 5,  name: 'rs1',       attr: ['5', 'src1', 'src1', 'src1', 'src1', 'src1'], type: 4},
  {bits: 5,  name: 'rs2',       attr: ['5', 'src2', 'src2', 'src2', 'src2', 'src2'], type: 4},
  {bits: 7,  name: 'funct7',    attr: ['7', '000000', '010000', '000000', '000000', '010000'], type: 8}
]}
....

//[wavedrom, ,svg]
//....
//{reg: [
//  {bits: 7,  name: 'opcode',    attr: 'OP-32', type: 8},
//  {bits: 5,  name: 'rd',        attr: 'dest', type: 2},
//  {bits: 3,  name: 'funct3',     attr: ['ADDW', 'SLLW', 'SRLW', 'SUBW', 'SRAW'], type: 8},
//  {bits: 5,  name: 'rs1',       attr: 'src1', type: 4},
//  {bits: 5,  name: 'rs2',       attr: 'src2', type: 4},
//  {bits: 7,  name: 'funct7', attr: [0, 0, 0, 32, 32], type: 8}
//]}
//....
