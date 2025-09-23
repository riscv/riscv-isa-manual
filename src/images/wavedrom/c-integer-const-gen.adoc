//c-integer-const-gen

[wavedrom, ,svg]
....
{reg: [
  {bits: 2, name: 'op', type: 3, attr: ['2','C1', 'C1']},
  {bits: 5, name: 'imm[4:0]',    type: 1, attr: ['5','imm[4:0]','imm[16:12]']},
  {bits: 5, name: 'rd',     type: 5, attr: ['5','dest != 0', 'dest != {0, 2}']},
  {bits: 1, name: 'imm[5]',    type: 5, attr: ['1','imm[5]', 'nzimm[17]'],},
  {bits: 3, name: 'funct3',    type: 5, attr: ['3','C.LI', 'C.LUI'],},
], config: {bits: 16}}
....

