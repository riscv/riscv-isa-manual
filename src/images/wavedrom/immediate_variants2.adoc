## 2.3 Immediate Encoding Variants
### Figure 2.3

RISC-V base instruction formats showing immediate variants.

${wd({reg: [
  {bits: 7,  name: 'opcode'},
  {bits: 5,  name: 'rd'},
  {bits: 3,  name: 'func3'},
  {bits: 5,  name: 'rs1'},
  {bits: 5,  name: 'rs2'},
  {bits: 7,  name: 'funct7'}
], config: {label: {right: 'R-Type'}}})}

${wd({reg: [
  {bits: 7,  name: 'opcode'},
  {bits: 5,  name: 'rd'},
  {bits: 3,  name: 'func3'},
  {bits: 5,  name: 'rs1'},
  {bits: 12, name: 'imm[11:0]', type: 3},
], config: {label: {right: 'I-Type'}}})}

${wd({reg: [
  {bits: 7,  name: 'opcode'},
  {bits: 5,  name: 'imm[4:0]', type: 3},
  {bits: 3,  name: 'func3'},
  {bits: 5,  name: 'rs1'},
  {bits: 5,  name: 'rs2'},
  {bits: 7,  name: 'imm[11:5]', type: 3}
], config: {label: {right: 'S-Type'}}})}

${wd({reg: [
  {bits: 7,  name: 'opcode'},
  {bits: 1,  name: '[11]',      type: 3},
  {bits: 4,  name: 'imm[4:1]',  type: 3},
  {bits: 3,  name: 'func3'},
  {bits: 5,  name: 'rs1'},
  {bits: 5,  name: 'rs2'},
  {bits: 6,  name: 'imm[10:5]', type: 3},
  {bits: 1,  name: '[12]',      type: 3}
], config: {label: {right: 'B-Type'}}})}

${wd({reg: [
  {bits: 7,  name: 'opcode'},
  {bits: 5,  name: 'rd'},
  {bits: 20, name: 'imm[31:12]', type: 3}
], config: {label: {right: 'U-Type'}}})}

${wd({reg: [
  {bits: 7,  name: 'opcode'},
  {bits: 5,  name: 'rd'},
  {bits: 8,  name: 'imm[19:12]', type: 3},
  {bits: 1,  name: '[11]',       type: 3},
  {bits: 10, name: 'imm[10:1]',  type: 3},
  {bits: 1,  name: '[20]',       type: 3}
], config: {label: {right: 'J-Type'}}})}