//### Figure 2.4
//Types of immediate produced by RISC-V instructions. The fields are labeled with the instruction bits used to construct their value. Sign extension always uses inst[31].
//#### I-immediate

[wavedrom, ,svg]
....
{reg: [
  {bits: 1,  name: '[20]'},
  {bits: 4,  name: 'inst[24:21]'},
  {bits: 6,  name: 'inst[30:25]'},
  {bits: 21,  name: '— inst[31] —', type: 7},
], config:{fontsize: 12, label:{right: 'I-immediate'}}}
....
//#### S-immediate

[wavedrom, ,svg]
....
{reg: [
  {bits: 1,  name: '[7]'},
  {bits: 4,  name: 'inst[11:8]'},
  {bits: 6,  name: 'inst[30:25]'},
  {bits: 21,  name: '— inst[31] —', type: 7},
], config:{fontsize: 12, label:{right: 'S-immediate'}}}
....
//#### B-immediate

[wavedrom, ,svg]
....
{reg: [
  {bits: 1,  name: '0', type: 5},
  {bits: 4,  name: 'inst[11:8]'},
  {bits: 6,  name: 'inst[30:25]'},
  {bits: 1,  name: '[7]'},
  {bits: 20, name: '— inst[31] —', type: 7},
], config:{fontsize: 12, label:{right: 'B-immediate'}}}
....
//#### U-immediate

[wavedrom, ,svg]
....
{reg: [
  {bits: 12, name: '0', type: 5},
  {bits: 8,  name: 'inst[19:12]'},
  {bits: 11, name: 'inst[30:20]'},
  {bits: 1,  name: '[31]', type: 7},
], config:{fontsize: 12, label:{right: 'U-immediate'}}}
....
//#### J-immediate

[wavedrom, ,svg]
....
{reg: [
  {bits: 1,  name: '0', type: 5},
  {bits: 4,  name: 'inst[24:21]'},
  {bits: 6,  name: 'inst[30:25]'},
  {bits: 1,  name: '[20]'},
  {bits: 8,  name: 'inst[19:12]'},
  {bits: 12, name: '— inst[31] —', type: 7},
], config:{fontsize: 12, label:{right: 'J-immediate'}}}
....
