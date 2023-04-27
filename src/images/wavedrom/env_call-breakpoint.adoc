//## 2.8 Environment Call and Breakpoints

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7', 'SYSTEM', 'SYSTEM'], type: 8},
  {bits: 5,  name: 'rd',    attr: ['5', '0', '0'], type: 2},
  {bits: 3,  name: 'funct3', attr: ['3', 'PRIV', 'PRIV'], type: 8},
  {bits: 5,  name: 'rs1',   attr: ['5', '0', '0'], type: 4},
  {bits: 12, name: 'func12', attr: ['12', 'ECALL', 'EBREAK'], type: 8},
]}
....
