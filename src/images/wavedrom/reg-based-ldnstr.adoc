//Register-Based loads and Stores


[wavedrom, ,svg]
....
{reg: [
  {bits: 2, name: 'op', attr: ['2', 'C0', 'C0', 'C0', 'C0', 'C0'], type: 8},
  {bits: 3, name: 'rd`',  attr: ['3', 'dest', 'dest','dest','dest','dest'], type: 3},
  {bits: 2, name: 'imm', attr:['2', 'offset[2|6]', 'offset[7:6]', 'offset[7:6]', 'offset[2|6]', 'offset[7:6]'], type: 2},
  {bits: 3, name: 'rs1`', attr: ['3', 'base', 'base', 'base', 'base', 'base'], type: 2},
  {bits: 3, name: 'imm',  attr: ['3', 'offset[5:3]', 'offset[5:3]', 'offset[5|4|8]', 'offset[5:3]', 'offset[5:3]'], type: 3},
  {bits: 3, name: 'funct3',  attr: ['3', 'C.LW', 'C.LD', 'C.LQ', 'C.FLW', 'C.FLD'], type: 8},
], config: {bits: 16}}
....

