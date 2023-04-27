//### RV64I
//These instructions reserved as HINTs in the latest spec: https://github.com/riscv/riscv-isa-manual/releases (4.4)
//All RV32I NOPs plus:
//ADDIW x0, ? ( ${ 1 << 17 } )
[wavedrom, ,svg]
....
{reg:[
    {name: 'OP-IMM-32', bits: 7,  attr: 0b0011011},
    {name: 'rd',     bits: 5,  attr: 0},
    {name: 'funct3',  bits: 3,  attr: 'ADDIW'},
    {bits: 17}
], config: {hspace: width}}
....
//Extra bit for the shift ammont:
//{SLLI, SRLI, SRAI} x0, ? ( ${ 3 * 1 << 10} )

[wavedrom, ,svg]
....
{reg: [
    {name: 'OP-IMM', bits: 7, attr: 0b0010011},
    {name: 'rd',     bits: 5, attr: 0},
    {name: 'funct3',  bits: 3, attr: ['SLLI', 'SRLI', 'SRAI']},
    {bits: 10},
    {name: 'imm?',   bits: 7, attr: [1, 33, 33]}
], config: {hspace: width}}
....
//{SLLIW, SRLIW, SRAIW} x0, ?( ${ 3 * 1 << 10} )

[wavedrom, ,svg]
....
{reg:[
    {name: 'OP-IMM-32', bits: 7,  attr: 0b0011011},
    {name: 'rd',     bits: 5,  attr: 0},
    {name: 'funct3',  bits: 3,  attr: ['SLLIW', 'SRLIW', 'SRAIW']},
    {bits: 10},
    {name: 'imm?',   bits: 7, attr: [0, 32, 32]}
], config: {hspace: width}}
....
//SLL, SLT, SRA ( ??? )
//{ADDW, SLLW, SRLW, SUBW, SRAW} x0, ?, ? ( ${ 5 * 1 << 10 } )

[wavedrom, ,svg]
....
{reg:[
    {name: 'OP-32', bits: 7,  attr: 0b0111011},
    {name: 'rd',     bits: 5,  attr: 0},
    {name: 'funct3',  bits: 3, attr: ['ADDW', 'SLLW', 'SRLW', 'SUBW', 'SRAW']},
    {bits: 10},
    {name: 'funct7',  bits: 7, attr: [0, 0, 32, 0, 32]}
], config: {hspace: width}}
....

//RV64I_extra = (
//  4 * 31 +
//  5 * 31 +
//  31
//`
