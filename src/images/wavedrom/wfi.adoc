//

[wavedrom, ,svg]

....
{reg: [
  {bits: 7, name: 'opcode', type: 8, attr: ['7','SYSTEM'],},
  {bits: 5, name: 'rd', type: 2, attr: ['5','0'],},
  {bits: 3, name: 'funct3', type: 8, attr: ['3','PRIV'],},
  {bits: 5, name: 'rs1', type: 4, attr: ['5','0'],},
  {bits: 12, name: 'funct12', type: 8, attr: ['12','WFI',]},
], config: {bits: 32}}
....