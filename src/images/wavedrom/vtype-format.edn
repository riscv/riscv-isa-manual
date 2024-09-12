[wavedrom,,svg]
....
{reg: [
  {bits: 3, name: 'vlmul[2:0]'},
  {bits: 3, name: 'vsew[2:0]'},
  {bits: 1, name: 'vta'},
  {bits: 1, name: 'vma'},
  {bits: 23, name: 'reserved'},
  {bits: 1, name: 'vill'},
]}
....

NOTE: This diagram shows the layout for RV32 systems, whereas in
general `vill` should be at bit XLEN-1.

.`vtype` register layout
[cols=">2,4,10"]
[%autowidth,float="center",align="center",options="header"]
|===
|     Bits | Name       | Description

|   XLEN-1 | vill       | Illegal value if set
| XLEN-2:8 | 0          | Reserved if non-zero
|        7 | vma        | Vector mask agnostic
|        6 | vta        | Vector tail agnostic
|      5:3 | vsew[2:0]  | Selected element width (SEW) setting
|      2:0 | vlmul[2:0] | Vector register group multiplier (LMUL) setting
|===
