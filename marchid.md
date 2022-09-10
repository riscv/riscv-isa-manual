Open-Source RISC-V Architecture IDs
========================================

Every RISC-V hart provides an marchid CSR that encodes its base
microarchitecture.  Any hart may report an architecture ID of 0, indicating
unspecified origin.  Commercial implementations (those with nonzero mvendorid)
may encode any value in marchid with the most-significant bit set, with the
low-order bits formatted in a vendor-specific manner.  Open-source
implementations (which may or may not have a nonzero mvendorid) have the
most-significant bit clear, with a globally unique pattern in the low-order
bits.

This document contains the canonical list of open-source RISC-V implementations
and their architecture IDs.  Open-source project maintainers may make pull
requests against this repository to request the allocation of an architecture
ID.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Project Name  | Maintainers                     | Point of Contact                                            | Architecture ID   | Project URL                                         
------------- | ------------------------------- | ----------------------------------------------------------- | ----------------- | --------------------------------------------------- 
Rocket        | SiFive, UC Berkeley             | [Andrew Waterman](mailto:andrew@sifive.com), SiFive         | 1                 | https://github.com/chipsalliance/rocket-chip
BOOM          | UC Berkeley                     | [Christopher Celio](mailto:celio@berkeley.edu)              | 2                 | https://github.com/riscv-boom/riscv-boom
CVA6          | OpenHW Group                    | [Florian Zaruba](mailto:florian@openhwgroup.org), OpenHW Group | 3                 | https://github.com/openhwgroup/cva6             
CV32E40P      | OpenHW Group                    | [Davide Schiavone](mailto:davide@openhwgroup.org), OpenHW Group | 4                 | https://github.com/openhwgroup/cv32e40p
Spike         | SiFive, UC Berkeley             | [Andrew Waterman](mailto:andrew@sifive.com), SiFive         | 5                 | https://github.com/riscv/riscv-isa-sim              
E-Class       | IIT Madras                      | [Neel Gala](mailto:neelgala@gmail.com)                      | 6                 | https://gitlab.com/shaktiproject/cores/e-class
ORCA          | VectorBlox                      | [Joel Vandergriendt](mailto:joel@vectorblox.com)            | 7                 | https://github.com/vectorblox/orca
SCR1          | Syntacore                       | [Dmitri Pavlov](mailto:dmitri.pavlov@syntacore.com), Syntacore| 8               | https://github.com/syntacore/scr1
YARVI         | Tommy Thorn's Priceless Services| [Tommy Thorn](mailto:tommy-github2@thorn.ws)                | 9                 | https://github.com/tommythorn/yarvi
RVBS          | Alexandre Joannou, University of Cambridge| [Alexandre Joannou](mailto:aj443@cl.cam.ac.uk)    | 10                | https://github.com/CTSRD-CHERI/RVBS
SweRV EH1     | Western Digital Corporation     | [Thomas Wicki](mailto:Thomas.Wicki@wdc.com)                 | 11                | https://github.com/chipsalliance/Cores-SweRV
MSCC          | Rongcui Dong                    | [Rongcui Dong](mailto:rongcuid@outlook.com)                | 12 | https://github.com/rongcuid/MSCC
BlackParrot   | The World                       | [Michael B. Taylor](mailto:prof.taylor@gmail.com), U. Washington | 13 |  https://github.com/black-parrot 
BaseJump Manycore   | U. Washington             | [Michael B. Taylor](mailto:prof.taylor@gmail.com), U. Washington | 14 |  https://github.com/bespoke-silicon-group/bsg_manycore 
C-Class       | IIT Madras                      | [Neel Gala](mailto:neelgala@gmail.com)                      | 15                 | https://gitlab.com/shaktiproject/cores/c-class
SweRV EL2     | Western Digital Corporation     | [Thomas Wicki](mailto:Thomas.Wicki@wdc.com)                 | 16                | https://github.com/chipsalliance/Cores-SweRV-EL2
SweRV EH2     | Western Digital Corporation     | [Thomas Wicki](mailto:Thomas.Wicki@wdc.com)                 | 17                | https://github.com/chipsalliance/Cores-SweRV-EH2
SERV          | Olof Kindgren Enterprises       | [Olof Kindgren](mailto:olof.kindgren@gmail.com)             | 18                | https://github.com/olofk/serv
NEORV32       | Stephan Nolting                 | [Stephan Nolting](mailto:stnolting@gmail.com)               | 19                | https://github.com/stnolting/neorv32
CV32E40X      | OpenHW Group                    | [Arjan Bink](mailto:arjan.bink@silabs.com), Silicon Laboratories | 20           | https://github.com/openhwgroup/cv32e40x
CV32E40S      | OpenHW Group                    | [Arjan Bink](mailto:arjan.bink@silabs.com), Silicon Laboratories | 21           | https://github.com/openhwgroup/cv32e40s
Ibex          | lowRISC                         | [lowRISC Hardware Team](mailto:hardware@lowrisc.org)        | 22                | https://github.com/lowRISC/ibex
RudolV        | Jörg Mische                     | [Jörg Mische](mailto:bobbl@gmx.de)                          | 23                | https://github.com/bobbl/rudolv
Steel Core    | Rafael Calcada                  | [Rafael Calcada](mailto:rafaelcalcada@gmail.com)            | 24                | https://github.com/rafaelcalcada/steel-core
XiangShan     | ICT, CAS                        | [XiangShan Team](mailto:xiangshan-all@ict.ac.cn)            | 25                | https://github.com/OpenXiangShan/XiangShan
Hummingbirdv2 E203  | Nuclei System Technology  | [Can Hu](mailto:canhu@nucleisys.com), Nuclei System Technology  | 26            | https://github.com/riscv-mcu/e203_hbirdv2
Hazard3       | Luke Wren                       | [Luke Wren](mailto:wren6991@gmail.com)                       | 27                | https://github.com/wren6991/hazard3
CV32E41P      | OpenHW Group                    | [Mark Hill](mailto:mark.hill@huawei.com), OpenHW Group        | 28            | https://github.com/openhwgroup/cv32e41p
Rift          | Jianhu Lab, WUT                 | [Ruige Lee](mailto:295054118@whut.edu.cn)                     | 29            | [RiftCore](https://github.com/whutddk/RiftCore), [Rift2Core](https://github.com/whutddk/Rift2Core)
RISu064       | Wenting Zhang                   | [Wenting Zhang](mailto:zephray@outlook.com)                 | 30                | https://github.com/zephray/RISu064
