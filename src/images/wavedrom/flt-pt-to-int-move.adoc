// 16.3 Instructions for moving bit patterns between floating-point and integer registers.

[wavedrom, ,svg]
....
{reg: [
  {bits: 7, name: 'opcode', attr: ['7','OP-FP','OP-FP'],  type: 8},
  {bits: 5, name: 'rd',     attr: ['5','dest','dest'],   type: 2},
  {bits: 3, name: 'rm',  attr: ['3','000','000'], type: 8},
  {bits: 5, name: 'rs1',    attr: ['5','src','src'],   type: 4},
  {bits: 5, name: 'rs2',    attr: ['5','0','0'],   type: 4},
  {bits: 2, name: 'fmt',    attr: ['2','H','H'],      type: 8},
  {bits: 5, name: 'funct5', attr: ['5','FMV.X.H','FMV.H.X'],  type: 8},
]}
....