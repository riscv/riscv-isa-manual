//These instructions use the CR format.

[wavedrom, ,svg]
....
{reg: [
  {bits: 2, name: 'op', type: 8, attr: ['2','C2', 'C2']},
  {bits: 5, name: 'rs2',     type: 4, attr: ['5','0', '0']},
  {bits: 5, name: 'rs1',     type: 4, attr: ['5','src≠0', 'src≠0']},
  {bits: 4, name: 'funct4',  type: 8, attr: ['4','C.JR', 'C.JALR']},
], config: {bits: 16}}
....

