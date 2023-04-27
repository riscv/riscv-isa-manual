//## 13.5 Double-Precision Floating-Point Conversion and Move Instructions


[wavedrom, ,svg]
....
{reg: [
  {bits: 7, name: 'opcode', attr: ['7','OP-FP','OP-FP'], type: 8},
  {bits: 5, name: 'rd',     attr: ['5','dest','dest'], type: 2},
  {bits: 3, name: 'rm',     attr: ['3','RM','RM'], type: 8},
  {bits: 5, name: 'rs1',    attr: ['5','src','src'], type: 4},
  {bits: 5, name: 'rs2',    attr: ['5','W[U]/L[U]','W[U]/L[U]'], type: 4},
  {bits: 2, name: 'fmt',    attr: ['2','D','D'], type: 8},
  {bits: 5, name: 'funct5', attr: ['5','FCVT.int.D','FCVT.D.int'], type: 8},
]}
....

