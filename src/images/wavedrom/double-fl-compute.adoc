//## 13.4 Double-Precision Floating-Point Computational Instructions

[wavedrom, ,svg]
....
{reg: [
  {bits: 7, name: 'opcode', attr: ['7','OP-FP','OP-FP','OP-FP','OP-FP'], type: 8},
  {bits: 5, name: 'rd',     attr: ['5','dest','dest','dest','dest'], type: 2},
  {bits: 3, name: 'rm',     attr: ['3','RM','RM','MIN/MAX','RM'], type: 8},
  {bits: 5, name: 'rs1',    attr: ['5','src1','src1','src1','src'], type: 4},
  {bits: 5, name: 'rs2',    attr: ['5','src2','src2','src2','0'], type: 4},
  {bits: 2, name: 'fmt',    attr: ['2','D','D','D','D'], type: 8},
  {bits: 5, name: 'funct5', attr: ['5','FADD/FSUB', 'FMUL/FDIV', 'FMIN-MAX', 'FSQRT'], type: 8},
]}
....

[wavedrom, ,svg]
....
{reg: [
  {bits: 7, name: 'opcode', attr: ['7','F[N]MADD/F[N]MSUB'],    type: 8},
  {bits: 5, name: 'rd',     attr: ['5','dest'],     type: 2},
  {bits: 3, name: 'rm',     attr: ['3','RM'],       type: 8},
  {bits: 5, name: 'rs1',    attr: ['5','src'],      type: 4},
  {bits: 5, name: 'rs2',    attr: ['5','src2'],     type: 4},
  {bits: 2, name: 'fmt',    attr: ['2','D'],        type: 8},
  {bits: 5, name: 'rs3',    attr: ['5','src3'],    type: 8},
]}
....

//[wavedrom, ,]
//....
//{reg: [
//  {bits: 7, name: 'opcode', attr: 'OP-FP',    type: 8},
//  {bits: 5, name: 'rd',     attr: 'dest',     type: 2},
//  {bits: 3, name: 'funct3',  attr: ['MIN', 'MAX'], type: 8},
//  {bits: 5, name: 'rs1',    attr: 'src1',     type: 4},
//  {bits: 5, name: 'rs2',    attr: 'src2',     type: 4},
//  {bits: 2, name: 'fmt',    attr: 'D',        type: 8},
//  {bits: 5, name: 'funct5', attr: 'FMIN-MAX', type: 8},
//]}
//....

//[wavedrom, ,]
//....
//{reg: [
//  {bits: 7, name: 'opcode', attr: ['FMADD', 'FNMADD', 'FMSUB', 'FNMSUB'],    type: 8},
//  {bits: 5, name: 'rd',     attr: 'dest',     type: 2},
//  {bits: 3, name: 'funct3',  attr: 'RM', type: 8},
//  {bits: 5, name: 'rs1',    attr: 'src1',     type: 4},
//  {bits: 5, name: 'rs2',    attr: 'src2',     type: 4},
//  {bits: 2, name: 'fmt',    attr: 'D',        type: 8},
//  {bits: 5, name: 'rs3',    attr: 'src3',     type: 4},
//]}
//....

