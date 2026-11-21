Formats for Vector Configuration Instructions under OP-V major opcode

////
 31 30         25 24      20 19      15 14   12 11      7 6     0
 0 |        zimm[10:0]      |    rs1   | 1 1 1 |    rd   |1010111| vsetvli
 1 |   1|  zimm[ 9:0]       | uimm[4:0]| 1 1 1 |    rd   |1010111| vsetivli
 1 |   000000    |   rs2    |    rs1   | 1 1 1 |    rd   |1010111| vsetvl
 1        6            5          5        3        5        7
////

[wavedrom,,svg]
....
{reg: [
  {bits: 7,  name: 0x57, attr: 'vsetvli'},
  {bits: 5,  name: 'rd', type: 4},
  {bits: 3,  name: 7},
  {bits: 5,  name: 'rs1', type: 4},
  {bits: 11, name: 'vtypei[10:0]', type: 5},
  {bits: 1,  name: '0'},
]}
....

[wavedrom,,svg]
....
{reg: [
  {bits: 7,  name: 0x57, attr: 'vsetivli'},
  {bits: 5,  name: 'rd', type: 4},
  {bits: 3,  name: 7},
  {bits: 5,  name: 'uimm[4:0]', type: 5},
  {bits: 10, name: 'vtypei[9:0]', type: 5},
  {bits: 1, name: '1'},
  {bits: 1,  name: '1'},
]}
....

[wavedrom,,svg]
....
{reg: [
  {bits: 7,  name: 0x57, attr: 'vsetvl'},
  {bits: 5,  name: 'rd', type: 4},
  {bits: 3,  name: 7},
  {bits: 5,  name: 'rs1', type: 4},
  {bits: 5,  name: 'rs2', type: 4},
  {bits: 6,  name: 0x00},
  {bits: 1,  name: 1},
]}
....
