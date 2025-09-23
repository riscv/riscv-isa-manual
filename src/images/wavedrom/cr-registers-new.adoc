[wavedrom, ,svg]
....
### CR : Register
${wd({reg: [
  {bits: 2, name: 'op',     type: 8},
  {bits: 5, name: 'rs2',    type: 4},
  {bits: 5, name: 'rd / rs1', type: 7},
  {bits: 4, name: 'funct4', type: 8},

  {bits: 2, name: 'op',     type: 8},
  {bits: 5, name: 'imm',    type: 3},
  {bits: 5, name: 'rd / rs1', type: 7},
  {bits: 1, name: 'imm',    type: 3},
  {bits: 3, name: 'funct3', type: 8},

  {bits: 2, name: 'op',     type: 8},
  {bits: 5, name: 'rs2',    type: 4},
  {bits: 6, name: 'imm',    type: 3},
  {bits: 3, name: 'funct3', type: 8},

  {bits: 2, name: 'op',     type: 8},
  {bits: 3, name: 'rd`',    type: 2},
  {bits: 8, name: 'imm',    type: 3},
  {bits: 3, name: 'funct3', type: 8},

  {bits: 2, name: 'op',     type: 8},
  {bits: 3, name: 'rd`',    type: 2},
  {bits: 2, name: 'imm',    type: 3},
  {bits: 3, name: 'rs1`',   type: 4},
  {bits: 3, name: 'imm',    type: 3},
  {bits: 3, name: 'funct3', type: 8},

  {bits: 2, name: 'op',     type: 8},
  {bits: 3, name: 'rs2`',   type: 4},
  {bits: 2, name: 'imm',    type: 3},
  {bits: 3, name: 'rs1`',   type: 4},
  {bits: 3, name: 'imm',    type: 3},
  {bits: 3, name: 'funct3', type: 8},

  {bits: 2, name: 'op',     type: 8},
  {bits: 3, name: 'rs2`',   type: 4},
  {bits: 2, name: 'funct2', type: 8},
  {bits: 3, name: 'rd` / rs1`',   type: 7},
  {bits: 6, name: 'funct6', type: 8},

  {bits: 2, name: 'op',     type: 8},
  {bits: 5, name: 'offset', type: 3},
  {bits: 3, name: 'rd` / rs1`',   type: 7},
  {bits: 3, name: 'offset', type: 3},
  {bits: 3, name: 'funct3', type: 8},

  {bits: 2,  name: 'op',     type: 8},
  {bits: 11, name: 'jump target', type: 3},
  {bits: 3,  name: 'funct3', type: 8},
], config: {
  hflip: true,
  compact: true,
  bits: 16 * 9, lanes: 9,
  margin: {right: width / 4},
  label: {right: ['CR : Register', 'CI : Immediate', 'CSS : Stack-relative Store', 'CIW : Wide Immediate', 'CL : Load', 'CS : Store', 'CA : Arithmetic', 'CB : Branch/Arithmetic', 'CJ : Jump']}
}})}
....