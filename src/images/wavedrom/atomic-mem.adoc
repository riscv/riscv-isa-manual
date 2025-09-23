//## 9.4 Atomic Memory Operations

[wavedrom, ,svg]
....
{reg: [
  {bits: 7, name: 'opcode',     type: 8, attr: ['7','AMO','AMO','AMO','AMO','AMO','AMO','AMO']},
  {bits: 5, name: 'rd',         type: 2, attr: ['5','dest','dest','dest','dest','dest','dest','dest']},
  {bits: 3, name: 'funct3',     type: 8, attr: ['3','width','width','width','width','width','width','width']},
  {bits: 5, name: 'rs1',        type: 4, attr: ['5','addr','addr','addr','addr','addr','addr','addr']},
  {bits: 5, name: 'rs2',        type: 4, attr: ['5','src','src','src','src','src','src','src']},
  {bits: 1, name: 'rl',         type: 8, attr: ['1']},
  {bits: 1, name: 'aq',         type: 8, attr: ['1']},
  {bits: 6, name: 'funct5',     type: 8, attr: ['5','AMOSWAP.W/D', 'AMOADD.W/D', 'AMOAND.W/D', 'AMOOR.W/D', 'AMOXOR.W/D', 'AMOMAX[U].W/D','AMOMIN[U].W/D']},
], config: {bits: 32}}
....
