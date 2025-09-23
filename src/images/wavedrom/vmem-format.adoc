Format for Vector Load Instructions under LOAD-FP major opcode

////
31 29  28  27 26  25  24      20 19       15 14   12 11      7 6     0
 nf  | mew| mop | vm |  lumop   |    rs1    | width |    vd   |0000111| VL*  unit-stride
 nf  | mew| mop | vm |   rs2    |    rs1    | width |    vd   |0000111| VLS* strided
 nf  | mew| mop | vm |   vs2    |    rs1    | width |    vd   |0000111| VLX* indexed
  3     1    2     1      5           5         3         5       7
////

[wavedrom,,svg]
....
{reg: [
  {bits: 7, name: 0x7, attr: 'VL* unit-stride'},
  {bits: 5, name: 'vd', attr: 'destination of load', type: 2},
  {bits: 3, name: 'width'},
  {bits: 5, name: 'rs1', attr: 'base address', type: 4},
  {bits: 5, name: 'lumop'},
  {bits: 1, name: 'vm'},
  {bits: 2, name: 'mop'},
  {bits: 1, name: 'mew'},
  {bits: 3, name: 'nf'},
]}
....

[wavedrom,,svg]
....
{reg: [
  {bits: 7, name: 0x7, attr: 'VLS* strided'},
  {bits: 5, name: 'vd', attr: 'destination of load', type: 2},
  {bits: 3, name: 'width'},
  {bits: 5, name: 'rs1', attr: 'base address', type: 4},
  {bits: 5, name: 'rs2', attr: 'stride', type: 4},
  {bits: 1, name: 'vm'},
  {bits: 2, name: 'mop'},
  {bits: 1, name: 'mew'},
  {bits: 3, name: 'nf'},
]}
....

[wavedrom,,svg]
....
{reg: [
  {bits: 7, name: 0x7, attr: 'VLX* indexed'},
  {bits: 5, name: 'vd', attr: 'destination of load', type: 2},
  {bits: 3, name: 'width'},
  {bits: 5, name: 'rs1', attr: 'base address', type: 4},
  {bits: 5, name: 'vs2', attr: 'address offsets', type: 2},
  {bits: 1, name: 'vm'},
  {bits: 2, name: 'mop'},
  {bits: 1, name: 'mew'},
  {bits: 3, name: 'nf'},
]}
....
Format for Vector Store Instructions under STORE-FP major opcode

////
31 29  28  27 26  25  24      20 19       15 14   12 11      7 6     0
 nf  | mew| mop | vm |  sumop   |    rs1    | width |   vs3   |0100111| VS*  unit-stride
 nf  | mew| mop | vm |   rs2    |    rs1    | width |   vs3   |0100111| VSS* strided
 nf  | mew| mop | vm |   vs2    |    rs1    | width |   vs3   |0100111| VSX* indexed
  3     1    2     1      5           5         3         5        7
////

[wavedrom,,svg]
....
{reg: [
  {bits: 7, name: 0x27, attr: 'VS* unit-stride'},
  {bits: 5, name: 'vs3', attr: 'store data', type: 2},
  {bits: 3, name: 'width'},
  {bits: 5, name: 'rs1', attr: 'base address', type: 4},
  {bits: 5, name: 'sumop'},
  {bits: 1, name: 'vm'},
  {bits: 2, name: 'mop'},
  {bits: 1, name: 'mew'},
  {bits: 3, name: 'nf'},
]}
....

[wavedrom,,svg]
....
{reg: [
  {bits: 7, name: 0x27, attr: 'VSS* strided'},
  {bits: 5, name: 'vs3', attr: 'store data', type: 2},
  {bits: 3, name: 'width'},
  {bits: 5, name: 'rs1', attr: 'base address', type: 4},
  {bits: 5, name: 'rs2', attr: 'stride', type: 4},
  {bits: 1, name: 'vm'},
  {bits: 2, name: 'mop'},
  {bits: 1, name: 'mew'},
  {bits: 3, name: 'nf'},
]}
....

[wavedrom,,svg]
....
{reg: [
  {bits: 7, name: 0x27, attr: 'VSX* indexed'},
  {bits: 5, name: 'vs3', attr: 'store data', type: 2},
  {bits: 3, name: 'width'},
  {bits: 5, name: 'rs1', attr: 'base address', type: 4},
  {bits: 5, name: 'vs2', attr: 'address offsets', type: 2},
  {bits: 1, name: 'vm'},
  {bits: 2, name: 'mop'},
  {bits: 1, name: 'mew'},
  {bits: 3, name: 'nf'},
]}
....
