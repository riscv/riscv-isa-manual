//# "D" Standard Extension for Double-Precision Floating-Point, Version 2.2
//## 13.3 Double-Precision Load and Store Instructions

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7','LOAD-FP'],  type: 8},
  {bits: 5,  name: 'rd',        attr: ['5','dest'],     type: 2},
  {bits: 3,  name: 'width',     attr: ['3','D'],    type: 8},
  {bits: 5,  name: 'rs1',       attr: ['5','base'],     type: 4},
  {bits: 12, name: 'imm[11:0]', attr: ['12','offset[11:0]'],   type: 3},
]}
....

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7','STORE-FP'], type: 8},
  {bits: 5,  name: 'imm[4:0]',  attr: ['5','offset[4:0]'],   type: 3},
  {bits: 3,  name: 'width',     attr: ['3','D'],    type: 8},
  {bits: 5,  name: 'rs1',       attr: ['5','base'],     type: 4},
  {bits: 5,  name: 'rs2',       attr: ['5','src'],      type: 4},
  {bits: 7, name: 'imm[11:5]', attr: ['7','offset[11:5]'],   type: 3},
]}
....



