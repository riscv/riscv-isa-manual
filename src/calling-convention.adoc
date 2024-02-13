[appendix]
== Calling Convention for Vector State (Not authoritative - Placeholder Only)

NOTE: This Appendix is only a placeholder to help explain the
conventions used in the code examples, and is not considered frozen or
part of the ratification process.  The official RISC-V psABI document
is being expanded to specify the vector calling conventions.

In the RISC-V psABI, the vector registers `v0`-`v31` are all caller-saved.
The `vl` and `vtype` CSRs are also caller-saved.

Procedures may assume that `vstart` is zero upon entry.  Procedures may
assume that `vstart` is zero upon return from a procedure call.

NOTE: Application software should normally not write `vstart` explicitly.
Any procedure that does explicitly write `vstart` to a nonzero value must
zero `vstart` before either returning or calling another procedure.

The `vxrm` and `vxsat` fields of `vcsr` have thread storage duration.

Executing a system call causes all caller-saved vector registers
(`v0`-`v31`, `vl`, `vtype`) and `vstart` to become unspecified.

NOTE: This scheme allows system calls that cause context switches to avoid
saving and later restoring the vector registers.

NOTE: Most OSes will choose to either leave these registers intact or reset
them to their initial state to avoid leaking information across process
boundaries.
