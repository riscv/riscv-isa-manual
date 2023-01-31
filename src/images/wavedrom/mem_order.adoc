//## 2.7 Memory Ordering Instructions

[wavedrom,mem-order ,]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7', 'MISC-MEM'], type: 8},
  {bits: 5,  name: 'rd', attr: ['5', '0'], type: 2},
  {bits: 3,  name: 'funct3', attr: ['3', 'FENCE'], type: 8},
  {bits: 5,  name: 'rs1', attr: ['5', '0'], type: 4},
  {bits: 1,  name: 'SW', attr: 1},
  {bits: 1,  name: 'SR', attr: 1},
  {bits: 1,  name: 'SO', attr: 1},
  {bits: 1,  name: 'SI', attr: 1},
  {bits: 1,  name: 'PW', attr: 1},
  {bits: 1,  name: 'PR', attr: 1},
  {bits: 1,  name: 'PO', attr: 1},
  {bits: 1,  name: 'PI', attr: 1},
  {bits: 4,  name: 'fm', attr: ['4', 'FM'], type: 8},
]}
....
