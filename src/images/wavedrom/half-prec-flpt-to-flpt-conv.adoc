//## 16.3 Half-Precision Floating Point to Floating Point Conversion Instructions

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7','OP-FP','OP-FP','OP-FP','OP-FP','OP-FP','OP-FP'],  type: 8},
  {bits: 5,  name: 'rd',        attr: ['5','dest','dest','dest','dest','dest','dest'],     type: 2},
  {bits: 3,  name: 'rm',        attr: ['3','RM','RM','RM','RM','RM','RM'],        type: 8},
  {bits: 5,  name: 'rs1',       attr: ['5','src','src','src','src','src','SRC'],     type: 4},
  {bits: 5,  name: 'rs2',       attr: ['5','H','S','H','D','H','Q'],   type: 3},
  {bits: 2,  name: 'fmt',       attr: ['2','S','H','D','H','Q','H'],   type: 2},
  {bits: 5,  name: 'funct5',    attr: ['5','FCVT.S.H','FCVT.H.S','FCVT.D.H','FCVT.H.D','FCVT.Q.H','FCVT.H.Q'],    type: 8},
]}
....