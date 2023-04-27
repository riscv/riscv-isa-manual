//### RV32I
//These instructions reserved as HINTs in the latest spec: https://github.com/riscv/riscv-isa-manual/releases (2.9)
//{ADDI, SLTI, SLTIU, XORI, ORI, ANDI} x0, ? ( ${ 6 * 1 << 17} )
[wavedrom, ,svg]
....
{reg: [
    {name: 'OP-IMM', bits: 7, attr: 0b0010011},
    {name: 'rd',     bits: 5, attr: 0},
    {name: 'funct3',  bits: 3, attr: ['ADDI', 'SLTI', 'SLTIU', 'XORI', 'ORI', 'ANDI']},
    {bits: 17}
], config: {hspace: width}}
....
//{SLLI, SRLI, SRAI} x0, ? ( ${ 3 * 1 << 10} )

[wavedrom, ,svg]
....
{reg:[
    {name: 'OP-IMM', bits: 7, attr: 0b0010011},
    {name: 'rd',     bits: 5, attr: 0},
    {name: 'funct3',  bits: 3, attr: ['SLLI', 'SRLI', 'SRAI']},
    {bits: 10},
    {name: 'imm?',   bits: 7, attr: [0, 0, 32]}
], config: {hspace: width}}
....
//{LUI, AUIPC} x0, ? ( ${ 2 * (1 << 20) } )

[wavedrom, ,svg]
....
{reg:[
    {name: 'opcode', bits: 7,  attr: ['AUIPC', 'LUI']},
    {name: 'rd',     bits: 5,  attr: 0},
    {bits: 20}
], config: {hspace: width}}
....
//{ADD, SUB, SLL, SLT, SLTU, XOR, SRL, SRA, OR, AND} x0, ?, ? ( ${ 10 * 1 << 10} )

[wavedrom, ,svg]
....
{reg:[
    {name: 'OP',     bits: 7, attr: 0b0110011},
    {name: 'rd',     bits: 5, attr: 0},
    {name: 'funct3',  bits: 3, attr: 'ADD SUB SLL SLT SLTU XOR SRL SRA OR AND'.split(' ',
    {bits: 10},
    {name: 'funct7',  bits: 7, attr: [0, 0, 0, 0, 0, 0, 32, 32, 0, 0]}
], config: {hspace: width}}
....

//RV32I_extra = (
//  3 * 31 +
//  31 +
//  7 * 31 +
//  3 * 31 +
//  2 * 31
//)

