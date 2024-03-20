
// [cols="4,1,1,1,8,4,1,1,8,4,1,1,8"]
[cols="<,<,<,<,<,<,<,<,<,<,<,<,<",options="headers"]
|===
5+| Integer               4+| Integer               4+| FP

| funct3 | | | |            | funct3 | | |             | funct3 | | |
| OPIVV  |V| | |            | OPMVV{nbsp}  |V| |             | OPFVV  |V| |
| OPIVX  | |X| |            | OPMVX{nbsp}  | |X|             | OPFVF  | |F|
| OPIVI  | | |I|            |        | | |             |        | | |
|===

[cols="<,<,<,<,<,<,<,<,<,<,<,<,<",options="headers"]
|===
5+| funct6                  4+| funct6                 4+| funct6

| 000000 |V|X|I| vadd       | 000000 |V| | vredsum     | 000000 |V|F| vfadd
| 000001 | | | |            | 000001 |V| | vredand     | 000001 |V| | vfredusum
| 000010 |V|X| | vsub       | 000010 |V| | vredor      | 000010 |V|F| vfsub
| 000011 | |X|I| vrsub      | 000011 |V| | vredxor     | 000011 |V| | vfredosum
| 000100 |V|X| | vminu      | 000100 |V| | vredminu    | 000100 |V|F| vfmin
| 000101 |V|X| | vmin       | 000101 |V| | vredmin     | 000101 |V| | vfredmin
| 000110 |V|X| | vmaxu      | 000110 |V| | vredmaxu    | 000110 |V|F| vfmax
| 000111 |V|X| | vmax       | 000111 |V| | vredmax     | 000111 |V| | vfredmax
| 001000 | | | |            | 001000 |V|X| vaaddu      | 001000 |V|F| vfsgnj
| 001001 |V|X|I| vand       | 001001 |V|X| vaadd       | 001001 |V|F| vfsgnjn
| 001010 |V|X|I| vor        | 001010 |V|X| vasubu      | 001010 |V|F| vfsgnjx
| 001011 |V|X|I| vxor       | 001011 |V|X| vasub       | 001011 | | |
| 001100 |V|X|I| vrgather   | 001100 | | |             | 001100 | | |
| 001101 | | | |            | 001101 | | |             | 001101 | | |
| 001110 | |X|I| vslideup   | 001110 | |X| vslide1up   | 001110 | |F| vfslide1up
| 001110 |V| | |vrgatherei16|        | | |             |        | | |           
| 001111 | |X|I| vslidedown | 001111 | |X| vslide1down | 001111 | |F| vfslide1down
|===

// [cols="4,1,1,1,8,4,1,1,8,4,1,1,8"]
|===
5+| funct6                  4+| funct6                 4+| funct6

| 010000 |V|X|I| vadc       | 010000 |V| | VWXUNARY0   | 010000 |V| | VWFUNARY0
|        | | | |            | 010000 | |X| VRXUNARY0   | 010000 | |F| VRFUNARY0
| 010001 |V|X|I| vmadc      | 010001 | | |             | 010001 | | |
| 010010 |V|X| | vsbc       | 010010 |V| | VXUNARY0    | 010010 |V| | VFUNARY0
| 010011 |V|X| | vmsbc      | 010011 | | |             | 010011 |V| | VFUNARY1
| 010100 | | | |            | 010100 |V| | VMUNARY0    | 010100 | | |
| 010101 | | | |            | 010101 | | |             | 010101 | | |
| 010110 | | | |            | 010110 | | |             | 010110 | | |
| 010111 |V|X|I| vmerge/vmv | 010111 |V| | vcompress   | 010111 | |F| vfmerge/vfmv
| 011000 |V|X|I| vmseq      | 011000 |V| | vmandn      | 011000 |V|F| vmfeq
| 011001 |V|X|I| vmsne      | 011001 |V| | vmand       | 011001 |V|F| vmfle
| 011010 |V|X| | vmsltu     | 011010 |V| | vmor        | 011010 | | |
| 011011 |V|X| | vmslt      | 011011 |V| | vmxor       | 011011 |V|F| vmflt
| 011100 |V|X|I| vmsleu     | 011100 |V| | vmorn       | 011100 |V|F| vmfne
| 011101 |V|X|I| vmsle      | 011101 |V| | vmnand      | 011101 | |F| vmfgt
| 011110 | |X|I| vmsgtu     | 011110 |V| | vmnor       | 011110 | | |
| 011111 | |X|I| vmsgt      | 011111 |V| | vmxnor      | 011111 | |F| vmfge
|===

// [cols="4,1,1,1,8,4,1,1,8,4,1,1,8"]
|===
5+| funct6                  4+| funct6                 4+| funct6

| 100000 |V|X|I| vsaddu     | 100000 |V|X| vdivu       | 100000 |V|F| vfdiv
| 100001 |V|X|I| vsadd      | 100001 |V|X| vdiv        | 100001 | |F| vfrdiv
| 100010 |V|X| | vssubu     | 100010 |V|X| vremu       | 100010 | | |
| 100011 |V|X| | vssub      | 100011 |V|X| vrem        | 100011 | | |
| 100100 | | | |            | 100100 |V|X| vmulhu      | 100100 |V|F| vfmul
| 100101 |V|X|I| vsll       | 100101 |V|X| vmul        | 100101 | | |
| 100110 | | | |            | 100110 |V|X| vmulhsu     | 100110 | | |
| 100111 |V|X| | vsmul      | 100111 |V|X| vmulh       | 100111 | |F| vfrsub
| 100111 | | |I| vmv<nr>r   |        | | |             |        | | |
| 101000 |V|X|I| vsrl       | 101000 | | |             | 101000 |V|F| vfmadd
| 101001 |V|X|I| vsra       | 101001 |V|X| vmadd       | 101001 |V|F| vfnmadd
| 101010 |V|X|I| vssrl      | 101010 | | |             | 101010 |V|F| vfmsub
| 101011 |V|X|I| vssra      | 101011 |V|X| vnmsub      | 101011 |V|F| vfnmsub
| 101100 |V|X|I| vnsrl      | 101100 | | |             | 101100 |V|F| vfmacc
| 101101 |V|X|I| vnsra      | 101101 |V|X| vmacc       | 101101 |V|F| vfnmacc
| 101110 |V|X|I| vnclipu    | 101110 | | |             | 101110 |V|F| vfmsac
| 101111 |V|X|I| vnclip     | 101111 |V|X| vnmsac      | 101111 |V|F| vfnmsac
|===

// [cols="4,1,1,1,8,4,1,1,8,4,1,1,8"]
|===
5+| funct6                  4+| funct6                 4+| funct6

| 110000 |V| | | vwredsumu  | 110000 |V|X| vwaddu      | 110000 |V|F| vfwadd
| 110001 |V| | | vwredsum   | 110001 |V|X| vwadd       | 110001 |V| | vfwredusum
| 110010 | | | |            | 110010 |V|X| vwsubu      | 110010 |V|F| vfwsub
| 110011 | | | |            | 110011 |V|X| vwsub       | 110011 |V| | vfwredosum
| 110100 | | | |            | 110100 |V|X| vwaddu.w    | 110100 |V|F| vfwadd.w
| 110101 | | | |            | 110101 |V|X| vwadd.w     | 110101 | | |
| 110110 | | | |            | 110110 |V|X| vwsubu.w    | 110110 |V|F| vfwsub.w
| 110111 | | | |            | 110111 |V|X| vwsub.w     | 110111 | | |
| 111000 | | | |            | 111000 |V|X| vwmulu      | 111000 |V|F| vfwmul
| 111001 | | | |            | 111001 | | |             | 111001 | | |      
| 111010 | | | |            | 111010 |V|X| vwmulsu     | 111010 | | |
| 111011 | | | |            | 111011 |V|X| vwmul       | 111011 | | |
| 111100 | | | |            | 111100 |V|X| vwmaccu     | 111100 |V|F| vfwmacc
| 111101 | | | |            | 111101 |V|X| vwmacc      | 111101 |V|F| vfwnmacc
| 111110 | | | |            | 111110 | |X| vwmaccus    | 111110 |V|F| vfwmsac
| 111111 | | | |            | 111111 |V|X| vwmaccsu    | 111111 |V|F| vfwnmsac
|===

<<<

.VRXUNARY0 encoding space
[cols="2,14"]
|===
|  vs2  |

| 00000 | vmv.s.x
|===

.VWXUNARY0 encoding space
[cols="2,14"]
|===
|  vs1  |

| 00000 | vmv.x.s
| 10000 | vcpop
| 10001 | vfirst
|===

.VXUNARY0 encoding space
[cols="2,14"]
|===
|  vs1  |

| 00010 | vzext.vf8
| 00011 | vsext.vf8
| 00100 | vzext.vf4
| 00101 | vsext.vf4
| 00110 | vzext.vf2
| 00111 | vsext.vf2
|===

.VRFUNARY0 encoding space
[cols="2,14"]
|===
|  vs2  |

| 00000 | vfmv.s.f
|===

.VWFUNARY0 encoding space
[cols="2,14"]
|===
|  vs1  |

| 00000 | vfmv.f.s
|===

.VFUNARY0 encoding space
[cols="2,14"]
|===
| vs1 | name

2+| single-width converts
| 00000 | vfcvt.xu.f.v
| 00001 | vfcvt.x.f.v
| 00010 | vfcvt.f.xu.v
| 00011 | vfcvt.f.x.v
| 00110 | vfcvt.rtz.xu.f.v
| 00111 | vfcvt.rtz.x.f.v
| |
2+| widening converts
| 01000 | vfwcvt.xu.f.v
| 01001 | vfwcvt.x.f.v
| 01010 | vfwcvt.f.xu.v
| 01011 | vfwcvt.f.x.v
| 01100 | vfwcvt.f.f.v
| 01110 | vfwcvt.rtz.xu.f.v
| 01111 | vfwcvt.rtz.x.f.v
| |
2+| narrowing converts
| 10000 | vfncvt.xu.f.w
| 10001 | vfncvt.x.f.w
| 10010 | vfncvt.f.xu.w
| 10011 | vfncvt.f.x.w
| 10100 | vfncvt.f.f.w
| 10101 | vfncvt.rod.f.f.w
| 10110 | vfncvt.rtz.xu.f.w
| 10111 | vfncvt.rtz.x.f.w
|===

.VFUNARY1 encoding space
[cols="2,14"]
|===
|  vs1  | name

| 00000 | vfsqrt.v
| 00100 | vfrsqrt7.v
| 00101 | vfrec7.v
| 10000 | vfclass.v
|===


.VMUNARY0 encoding space
[cols="2,14"]
|===
|  vs1  |

| 00001 | vmsbf
| 00010 | vmsof
| 00011 | vmsif
| 10000 | viota
| 10001 | vid
|===


