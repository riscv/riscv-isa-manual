//## 2.5 Control Transfer Instructions
//### Unconditional Jumps

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode', attr: ['7', 'JAL'], type: 8},
  {bits: 5,  name: 'rd', attr: ['5', 'dest'], type: 2},
  {bits: 8,  name: 'imm[19:12]', attr: ['8'], type: 3},
  {bits: 1,  name: '[11]', attr: ['1'], type: 3},
  {bits: 10, name: 'imm[10:1]', attr: ['10', 'offset[20:1]'], type: 3},
  {bits: 1,  name: '[20]', attr: ['1'], type: 3},
], config:{fontsize: 12}}
....

