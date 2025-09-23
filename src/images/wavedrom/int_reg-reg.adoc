//### Integer Register-Register Operations

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',    attr: ['7', 'OP', 'OP', 'OP', 'OP'], type: 8},
  {bits: 5,  name: 'rd',        attr: ['5', 'dest', 'dest', 'dest','dest'], type: 2},
  {bits: 3,  name: 'funct3',     attr: ['3', 'ADD/SLT[U]', 'AND/OR/XOR', 'SLL/SRL', 'SUB/SRA'], type: 8},
  {bits: 5,  name: 'rs1',       attr: ['5', 'src1', 'src1', 'src1', 'src1'], type: 4},
  {bits: 5,  name: 'rs2',       attr: ['5', 'src2', 'src2', 'src2', 'src2'], type: 4},
  {bits: 7,  name: 'funct7', attr: ['7', 0, 0, 0, 32], type: 8}
]}
....
