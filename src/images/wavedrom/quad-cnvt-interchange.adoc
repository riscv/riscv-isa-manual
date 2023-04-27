//14 conv-mv

[wavedrom, ,svg]
....
{reg: [
  {bits: 7, name: 'opcode', attr: ['7', 'OP-FP', 'OP-FP','OP-FP','OP-FP'], type: 8},
  {bits: 5, name: 'rd',     attr: ['5','dest','dest','dest','dest'], type: 2},
  {bits: 3, name: 'rm',     attr: ['3','RM','RM','RM','RM'], type: 8},
  {bits: 5, name: 'rs1',    attr: ['5','src','src','src','src'], type: 4},
  {bits: 5, name: 'rs2',    attr: ['5','Q', 'S', 'Q', 'D'], type: 4},
  {bits: 2, name: 'fmt',    attr: ['2','S','Q', 'D', 'Q'],      type: 8},
  {bits: 5, name: 'funct5', attr: ['5','FCVT.S.Q', 'FCVT.Q.S', 'FCVT.D.Q', 'FCVT.Q.D'], type: 8},
]}
....


