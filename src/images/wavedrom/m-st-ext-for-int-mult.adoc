//# 8 "M" Standard Extension for Integer Multiplication and Division, Version 2.0
//## 8.1 Multiplication Operations

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode', attr: ['7', 'OP', 'OP-32'], type: 8},
  {bits: 5,  name: 'rd',     attr: ['5', 'dest', 'dest'], type: 2},
  {bits: 3,  name: 'funct3', attr: ['3', 'MUL/MULH[[S]U]', 'MULW'], type: 8},
  {bits: 5,  name: 'rs1',    attr: ['5', 'multiplicand', 'multiplicand'], type: 4},
  {bits: 5,  name: 'rs2',    attr: ['5', 'multiplier', 'multiplier'], type: 4},
  {bits: 7,  name: 'funct7', attr: ['7', 'MULDIV', 'MULDIV'], type: 8},
]}
....

//[wavedrom, ,]
//....
//{reg: [
//  {bits: 7,  name: 'opcode', attr: 'OP-32',         type: 8},
//  {bits: 5,  name: 'rd',     attr: 'dest',          type: 2},
//  {bits: 3,  name: 'funct3',  attr: 'MULW',          type: 8},
//  {bits: 5,  name: 'rs1',    attr: 'multiplicand',  type: 4},
//  {bits: 5,  name: 'rs2',    attr: 'multiplier',    type: 4},
//  {bits: 7,  name: 'funct7', attr: 'MULDIV',        type: 8},
//]}
//....


