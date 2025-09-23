[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: 'STORE-FP', type: 8},
  {bits: 5,  name: 'imm[4:0]',  attr: 'offset',   type: 3},
  {bits: 3,  name: 'width',     attr: 'H',        type: 8},
  {bits: 5,  name: 'rs1',       attr: 'base',     type: 4},
  {bits: 5,  name: 'rs2',       attr: 'src',      type: 4},
  {bits: 12, name: 'imm[11:5]', attr: 'offset',   type: 3},
]}
....