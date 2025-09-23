//c-cj-format-ls

//[wavedrom, ,svg]
//....
//{reg: [
//	{bits: 2,  name: 'op', 		type: 4,  attr: ['2','CI','CI']},
//	{bits: 10, name: 'imm',		type: 2,  },
//	{bits: 4,  name: 'funct3' 	type: 4,  attr:['3','CJ','CJAL']},
//] config: {bits: 16}}
//....


[wavedrom, ,svg]
....
{reg: [
  {bits: 2, name: 'op',     type: 8, attr: ['2','C1','C1']},
  {bits: 11, name: 'imm',   type: 2, attr: ['11','offset[11|4|9:8|10|6|7|3:1|5]','offset[11|4|9:8|10|6|7|3:1|5]']},
  {bits: 3, name: 'funct3', type: 8, attr: ['3','C.J','C.JAL']},
], config: {bits: 16}}
....



