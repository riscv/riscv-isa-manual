//c-sp load and store, css format--is this correct?

[wavedrom, ,svg]
....
{reg: [
  {bits: 2, name: 'op',     type: 8, attr: ['2','C2','C2','C2','C2','C2']},
  {bits: 5, name: 'rs2',    type: 4, attr: ['5','src', 'src', 'src', 'src', 'src']},
  {bits: 6, name: 'imm',    type: 3, attr: ['6','offset[5:2|7:6]', 'offset[5:3|8:6]', 'offset[5:4|9:6]', 'offset[5:2|7:6]','offset[5:3|8:6]']},
  {bits: 3, name: 'funct3', type: 8, attr: ['3','C.SWSP', 'C.SDSP', 'C.SQSP', 'C.FSWSP', 'C.FSDSP']},
], config: {bits: 16}}
....



