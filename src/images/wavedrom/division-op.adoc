//## 8.2 Division Operations

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode', attr: ['7', 'OP', 'OP-32'], type: 8},
  {bits: 5,  name: 'rd',     attr: ['5', 'dest', 'dest'], type: 2},
  {bits: 3,  name: 'funct3',  attr: ['3','DIV[U]/REM[U]', 'DIV[U]W/REM[U]W'], type: 8},
  {bits: 5,  name: 'rs1',    attr: ['5', 'dividend', 'dividend'], type: 4},
  {bits: 5,  name: 'rs2',    attr: ['5', 'divisor', 'divisor'], type: 4},
  {bits: 7,  name: 'funct7', attr: ['7', 'MULDIV', 'MULDIV'], type: 8},
]}
....

//[wavedrom, ,svg]
//....
//{reg: [
//  {bits: 7,  name: 'opcode', attr: 'OP-32',         type: 8},
//  {bits: 5,  name: 'rd',     attr: 'dest',          type: 2},
//  {bits: 3,  name: 'funct3',  attr: ['DIVW', 'DIVUW', 'REMW', 'REMUW'],          type: 8},
//  {bits: 5,  name: 'rs1',    attr: 'dividend',      type: 4},
//  {bits: 5,  name: 'rs2',    attr: 'divisor',       type: 4},
//  {bits: 7,  name: 'funct7', attr: 'MULDIV',        type: 8},
//]}
//....
