//## 14.5 Quad-Precision Floating-Point Classify Instruction

[wavedrom, ,svg]
....
{reg: [
  {bits: 7, name: 'opcode', attr: ['7','OP-FP'], type: 8},
  {bits: 5, name: 'rd',     attr: ['5','dest'], type: 2},
  {bits: 3, name: 'rm',     attr: ['3','001'], type: 8},
  {bits: 5, name: 'rs1',    attr: ['5','src'], type: 4},
  {bits: 5, name: 'rs2',    attr: ['5','0'], type: 8},
  {bits: 2, name: 'fmt',    attr: ['2','Q'], type: 8},
  {bits: 5, name: 'funct5', attr: ['5','FCLASS'], type: 8},
]}
....

