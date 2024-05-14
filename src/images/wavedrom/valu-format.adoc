Formats for Vector Arithmetic Instructions under OP-V major opcode

////
31       26  25   24      20 19      15 14   12 11      7 6     0
  funct6   | vm  |   vs2    |    vs1   | 0 0 0 |    vd   |1010111| OP-V (OPIVV)
  funct6   | vm  |   vs2    |    vs1   | 0 0 1 |  vd/rd  |1010111| OP-V (OPFVV)
  funct6   | vm  |   vs2    |    vs1   | 0 1 0 |  vd/rd  |1010111| OP-V (OPMVV)
  funct6   | vm  |   vs2    | imm[4:0] | 0 1 1 |    vd   |1010111| OP-V (OPIVI)
  funct6   | vm  |   vs2    |    rs1   | 1 0 0 |    vd   |1010111| OP-V (OPIVX)
  funct6   | vm  |   vs2    |    rs1   | 1 0 1 |    vd   |1010111| OP-V (OPFVF)
  funct6   | vm  |   vs2    |    rs1   | 1 1 0 |  vd/rd  |1010111| OP-V (OPMVX)
     6        1        5          5        3        5        7
////

[wavedrom,,svg]
....
{reg: [
  {bits: 7, name: 0x57, attr: 'OPIVV'},
  {bits: 5, name: 'vd', type: 2},
  {bits: 3, name: 0},
  {bits: 5, name: 'vs1', type: 2},
  {bits: 5, name: 'vs2', type: 2},
  {bits: 1, name: 'vm'},
  {bits: 6, name: 'funct6'},
]}
....

[wavedrom,,svg]
....
{reg: [
  {bits: 7, name: 0x57, attr: 'OPFVV'},
  {bits: 5, name: 'vd / rd', type: 7},
  {bits: 3, name: 1},
  {bits: 5, name: 'vs1', type: 2},
  {bits: 5, name: 'vs2', type: 2},
  {bits: 1, name: 'vm'},
  {bits: 6, name: 'funct6'},
]}
....

[wavedrom,,svg]
....
{reg: [
  {bits: 7, name: 0x57, attr: 'OPMVV'},
  {bits: 5, name: 'vd / rd', type: 7},
  {bits: 3, name: 2},
  {bits: 5, name: 'vs1', type: 2},
  {bits: 5, name: 'vs2', type: 2},
  {bits: 1, name: 'vm'},
  {bits: 6, name: 'funct6'},
]}
....

[wavedrom,,svg]
....
{reg: [
  {bits: 7, name: 0x57, attr: ['OPIVI']},
  {bits: 5, name: 'vd', type: 2},
  {bits: 3, name: 3},
  {bits: 5, name: 'imm[4:0]', type: 5},
  {bits: 5, name: 'vs2', type: 2},
  {bits: 1, name: 'vm'},
  {bits: 6, name: 'funct6'},
]}
....

[wavedrom,,svg]
....
{reg: [
  {bits: 7, name: 0x57, attr: 'OPIVX'},
  {bits: 5, name: 'vd', type: 2},
  {bits: 3, name: 4},
  {bits: 5, name: 'rs1', type: 4},
  {bits: 5, name: 'vs2', type: 2},
  {bits: 1, name: 'vm'},
  {bits: 6, name: 'funct6'},
]}
....

[wavedrom,,svg]
....
{reg: [
  {bits: 7, name: 0x57, attr: 'OPFVF'},
  {bits: 5, name: 'vd', type: 2},
  {bits: 3, name: 5},
  {bits: 5, name: 'rs1', type: 4},
  {bits: 5, name: 'vs2', type: 2},
  {bits: 1, name: 'vm'},
  {bits: 6, name: 'funct6'},
]}
....

[wavedrom,,svg]
....
{reg: [
  {bits: 7, name: 0x57, attr: 'OPMVX'},
  {bits: 5, name: 'vd / rd', type: 7},
  {bits: 3, name: 6},
  {bits: 5, name: 'rs1', type: 4},
  {bits: 5, name: 'vs2', type: 2},
  {bits: 1, name: 'vm'},
  {bits: 6, name: 'funct6'},
]}
....
