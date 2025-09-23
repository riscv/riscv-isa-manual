//# 11 Counters
//## 11.1 Base Counters and Timers

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode', attr: ['7','SYSTEM','SYSTEM','SYSTEM'], type: 8},
  {bits: 5,  name: 'rd',     attr: ['5','dest','dest','dest'],  type: 2},
  {bits: 3,  name: 'funct3',  attr: ['3','CSRRS','CSRRS','CSRRS'],  type: 8},
  {bits: 5,  name: 'rs1',    attr: ['5','0','0','0'], type: 8},
  {bits: 12, name: 'csr',    attr: ['12','RDCYCLE[H]', 'RDTIME[H]','RDINSTRET[H]'], type: 4},
]}
....

