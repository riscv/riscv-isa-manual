//## 16.X Load and Store Instructions
//### c-cs-format-ls

[wavedrom, ,svg]
....
{reg: [
  {bits: 2, name: 'op',     type: 8, attr: ['2', 'C0','C0','C0','C0','C0']},
  {bits: 3, name: 'rs2`',   type: 3, attr: ['3', 'src','src','src','src','src']},
  {bits: 2, name: 'imm',    type: 2, attr: ['2', 'offset[2|6]','offset[7:6]','offset[7:6]','offset[2|6]','offset[7:6]']},
  {bits: 3, name: 'rs1`',   type: 3, attr: ['3', 'base','base','base','base','base']},
  {bits: 3, name: 'imm',    type: 3, attr: ['3', 'offset[5:3]','offset[5:3]','offset[5|4|8]','offset[5:3]','offset[5:3]']},
  {bits: 3, name: 'funct3', type: 8, attr: ['3', 'C.SW','C.SD','C.SQ','C.FSW','C.FSD']},
], config: {bits: 16}}
....


