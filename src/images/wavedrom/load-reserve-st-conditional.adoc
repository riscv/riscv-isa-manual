//# 9 "A" Standard Extension for Atomic Instructions, Version 2.1
//## 9.2 Load-Reserved/Store-Conditional Instructions


[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7', 'AMO', 'AMO'], type: 8},
  {bits: 5,  name: 'rd',        attr: ['5', 'dest', 'dest'], type: 2},
  {bits: 3,  name: 'funct3',    attr: ['3', 'width', 'width'], type: 8},
  {bits: 5,  name: 'rs1',       attr: ['5', 'addr', 'addr'], type: 4},
  {bits: 5,  name: 'rs2',       attr: ['5', '0', 'src'], type: 4},
  {bits: 1,  name: 'rl',        attr: ['1', 'ring', 'ring'], type: 8},
  {bits: 1,  name: 'aq',        attr: ['1', 'orde', 'orde'], type: 8},
  {bits: 5,  name: 'funct5',    attr: ['5', 'LR.W/D', 'SC.W/D'], type: 8},
]}
....


