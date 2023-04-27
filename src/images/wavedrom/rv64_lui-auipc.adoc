//lui-auipc

[wavedrom, ,svg]
....
{reg: [
  {bits: 7,  name: 'opcode',     attr: ['7', 'LUI', 'AUIPC'], type: 8},
  {bits: 5,  name: 'rd',         attr: ['5', 'dest', 'dest'], type: 2},
  {bits: 20, name: 'imm[31:12]', attr: ['20', 'U-immediate[31:12]', 'U-immediate[31:12]'], type: 3}
]}
....
