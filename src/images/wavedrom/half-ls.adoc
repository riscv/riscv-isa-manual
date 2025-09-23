//## 15.1 Half-Precision Load and Store Instructions

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: 'LOAD-FP',  type: 8},
  {bits: 5,  name: 'rd',        attr: 'dest',     type: 2},
  {bits: 3,  name: 'width',     attr: 'H',        type: 8},
  {bits: 5,  name: 'rs1',       attr: 'base',     type: 4},
  {bits: 12, name: 'imm[11:0]', attr: 'offset',   type: 3},
]}

....

