//c-cb-format-ls

[wavedrom, ,svg]
....
{reg: [
  {bits: 2, name: 'op', type: 8, attr: ['2','C1', 'C1']},
  {bits: 5, name: 'imm', type: 3, attr: ['5','offset[7:6|2:1|5]', 'offset[7:6|2:1|5]']},
  {bits: 3, name: 'rs1′',     type: 4, attr: ['3','src', 'src']},
  {bits: 3, name: 'imm',    type: 3, attr: ['3','offset[8|4:3]', 'offset[8|4:3]'],},
  {bits: 3, name: 'funct3',    type: 8, attr: ['3','C.BEQZ', 'C.BNEZ'],},
], config: {bits: 16}}
....

