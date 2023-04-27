//## 12.6 Single-Precision Floating-Point Computational Instructions for ZFH Chapter

[wavedrom, ,svg]
....
{reg: [
  {bits: 7, name: 'opcode', attr: ['7','OP-FP','OP-FP','OP-FP','OP-FP'],    type: 8},
  {bits: 5, name: 'rd',     attr: ['5','dest','dest','dest','dest'],     type: 2},
  {bits: 3, name: 'rm',  attr: ['3','RM', 'RM', 'MIN/MAX', 'RM'],       type: 8},
  {bits: 5, name: 'rs1',    attr: ['5','src1', 'src1', 'src1', 'src'],     type: 4},
  {bits: 5, name: 'rs2',    attr: ['5','src2', 'src2', 'src2', '0'],     type: 4},
  {bits: 2, name: 'fmt',    attr: ['2','H', 'H', 'H', 'H'],        type: 8},
  {bits: 5, name: 'funct5', attr: ['5', 'FADD/FSUB', 'FMUL/FDIV', 'FMIN-MAX', 'FSQRT'], type: 8},
]}
....