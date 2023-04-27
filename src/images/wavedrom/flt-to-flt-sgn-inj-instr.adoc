// 16.3 Floating point to floating point sign injection instructions.

[wavedrom, ,svg]
....
{reg: [
  {bits: 7, name: 'opcode', attr: ['7','OP-FP'],  type: 8},
  {bits: 5, name: 'rd',     attr: ['5','dest'],   type: 2},
  {bits: 3, name: 'funct3',  attr: ['3','J[N]/JX'], type: 8},
  {bits: 5, name: 'rs1',    attr: ['5','src1'],   type: 4},
  {bits: 5, name: 'rs2',    attr: ['5','src2'],   type: 4},
  {bits: 2, name: 'fmt',    attr: ['2','H'],      type: 8},
  {bits: 5, name: 'funct5', attr: ['5','FSGNJ'],  type: 8},
]}
....