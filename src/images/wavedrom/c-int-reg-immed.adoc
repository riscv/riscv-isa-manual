//c-int-reg-immed.adoc

[wavedrom, ,svg]
....
{reg: [
  {bits: 2, name: 'op',        type: 3, attr: ['2','C1', 'C1', 'C1']},
  {bits: 5, name: 'imm[4:]',  type: 1, attr: ['5','nzimm[4:0]', 'imm[4:0]', 'nzimm[4|6|8:7|5]']},
  {bits: 5, name: 'rd/rs1',    type: 5, attr: ['5','dest != 0', 'dest != 0', '2']},
  {bits: 1, name: 'imm[5]',    type: 5, attr: ['1','nzimm[5]', 'imm[5]', 'nzimm[9]']},
  {bits: 3, name: 'funct3',    type: 5, attr: ['3','C.ADDI', 'C.ADDIW', 'C.ADDI16SP']},
], config: {bits: 16}}
....
