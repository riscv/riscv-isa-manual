
//FNMSUP and FNMADD

[wavedrom, ,svg]
....
{reg: [
  {bits: 7, name: 'opcode', attr: ['FMADD', 'FNMADD', 'FMSUB', 'FNMSUB'],    type: 8},
  {bits: 5, name: 'rd',     attr: 'dest',     type: 2},
  {bits: 3, name: 'funct3',  attr: 'RM', type: 8},
  {bits: 5, name: 'rs1',    attr: 'src1',     type: 4},
  {bits: 5, name: 'rs2',    attr: 'src2',     type: 4},
  {bits: 2, name: 'fmt',    attr: 'S',        type: 8},
  {bits: 5, name: 'rs3',    attr: 'src3',     type: 4},
]}
....

