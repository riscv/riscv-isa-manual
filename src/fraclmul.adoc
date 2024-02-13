=== Fractional Lmul example

This appendix presents a non-normative example to help explain where
compilers can make good use of the fractional LMUL feature.

Consider the following (admittedly contrived) loop written in C:

----
void add_ref(long N,
    signed char *restrict c_c, signed char *restrict c_a, signed char *restrict c_b,
    long *restrict l_c, long *restrict l_a, long *restrict l_b,
    long *restrict l_d, long *restrict l_e, long *restrict l_f,
    long *restrict l_g, long *restrict l_h, long *restrict l_i,
    long *restrict l_j, long *restrict l_k, long *restrict l_l,
    long *restrict l_m) {
  long i;
  for (i = 0; i < N; i++) {
    c_c[i] = c_a[i] + c_b[i]; // Note this 'char' addition that creates a mixed type situation
    l_c[i] = l_a[i] + l_b[i];
    l_f[i] = l_d[i] + l_e[i];
    l_i[i] = l_g[i] + l_h[i];
    l_l[i] = l_k[i] + l_j[i];
    l_m[i] += l_m[i] + l_c[i] + l_f[i] + l_i[i] + l_l[i];
  }
}
----

The example loop has a high register pressure due to the many input variables
and temporaries required. The compiler realizes there are two datatypes within
the loop: an 8-bit 'char' and a 64-bit 'long *'. Without fractional LMUL, the
compiler would be forced to use LMUL=1 for the 8-bit computation and LMUL=8 for
the 64-bit computation(s), to have equal number of elements on all computations
within the same loop iteration. Under LMUL=8, only 4 registers are available
to the register allocator. Given the large number of 64-bit variables and 
temporaries required in this loop, the compiler ends up generating a lot of 
spill code. The code below demonstrates this effect:

----
.LBB0_4:                                # %vector.body
                                        # =>This Inner Loop Header: Depth=1
	add	s9, a2, s6
	vsetvli	s1, zero, e8,m1,ta,mu
	vle8.v	v25, (s9)
	add	s1, a3, s6
	vle8.v	v26, (s1)
	vadd.vv	v25, v26, v25
	add	s1, a1, s6
	vse8.v	v25, (s1)
	add	s9, a5, s10
	vsetvli	s1, zero, e64,m8,ta,mu
	vle64.v	v8, (s9)
	add	s1, a6, s10
	vle64.v	v16, (s1)
	add	s1, a7, s10
	vle64.v	v24, (s1)
	add	s1, s3, s10
	vle64.v	v0, (s1)
	sd	a0, -112(s0)
	ld	a0, -128(s0)
	vs8r.v	v0, (a0) # Spill LMUL=8
	add	s9, t6, s10
	add	s11, t5, s10
	add	ra, t2, s10
	add	s1, t3, s10
	vle64.v	v0, (s9)
	ld	s9, -136(s0)
	vs8r.v	v0, (s9) # Spill LMUL=8
	vle64.v	v0, (s11)
	ld	s9, -144(s0)
	vs8r.v	v0, (s9) # Spill LMUL=8
	vle64.v	v0, (ra)
	ld	s9, -160(s0)
	vs8r.v	v0, (s9) # Spill LMUL=8
	vle64.v	v0, (s1)
	ld	s1, -152(s0)
	vs8r.v	v0, (s1) # Spill LMUL=8
	vadd.vv	v16, v16, v8
	ld	s1, -128(s0)
	vl8r.v	v8, (s1) # Reload LMUL=8
	vadd.vv	v8, v8, v24
	ld	s1, -136(s0)
	vl8r.v	v24, (s1) # Reload LMUL=8
	ld	s1, -144(s0)
	vl8r.v	v0, (s1) # Reload LMUL=8
	vadd.vv	v24, v0, v24
	ld	s1, -128(s0)
	vs8r.v	v24, (s1) # Spill LMUL=8
	ld	s1, -152(s0)
	vl8r.v	v0, (s1) # Reload LMUL=8
	ld	s1, -160(s0)
	vl8r.v	v24, (s1) # Reload LMUL=8
	vadd.vv	v0, v0, v24
	add	s1, a4, s10
	vse64.v	v16, (s1)
	add	s1, s2, s10
	vse64.v	v8, (s1)
	vadd.vv	v8, v8, v16
	add	s1, t4, s10
	ld	s9, -128(s0)
	vl8r.v	v16, (s9) # Reload LMUL=8
	vse64.v	v16, (s1)
	add	s9, t0, s10
	vadd.vv	v8, v8, v16
	vle64.v	v16, (s9)
	add	s1, t1, s10
	vse64.v	v0, (s1)
	vadd.vv	v8, v8, v0
	vsll.vi	v16, v16, 1
	vadd.vv	v8, v8, v16
	vse64.v	v8, (s9)
	add	s6, s6, s7
	add	s10, s10, s8
	bne	s6, s4, .LBB0_4
----

If instead of using LMUL=1 for the 8-bit computation, the compiler is allowed
to use a fractional LMUL=1/2, then the 64-bit computations can be performed
using LMUL=4 (note that the same ratio of 64-bit elements and 8-bit elements is
preserved as in the previous example). Now the compiler has 8 available
registers to perform register allocation, resulting in no spill code, as
shown in the loop below:

----
.LBB0_4:                                # %vector.body
                                        # =>This Inner Loop Header: Depth=1
	add	s9, a2, s6
	vsetvli	s1, zero, e8,mf2,ta,mu // LMUL=1/2 !
	vle8.v	v25, (s9)
	add	s1, a3, s6
	vle8.v	v26, (s1)
	vadd.vv	v25, v26, v25
	add	s1, a1, s6
	vse8.v	v25, (s1)
	add	s9, a5, s10
	vsetvli	s1, zero, e64,m4,ta,mu // LMUL=4
	vle64.v	v28, (s9)
	add	s1, a6, s10
	vle64.v	v8, (s1)
	vadd.vv	v28, v8, v28
	add	s1, a7, s10
	vle64.v	v8, (s1)
	add	s1, s3, s10
	vle64.v	v12, (s1)
	add	s1, t6, s10
	vle64.v	v16, (s1)
	add	s1, t5, s10
	vle64.v	v20, (s1)
	add	s1, a4, s10
	vse64.v	v28, (s1)
	vadd.vv	v8, v12, v8
	vadd.vv	v12, v20, v16
	add	s1, t2, s10
	vle64.v	v16, (s1)
	add	s1, t3, s10
	vle64.v	v20, (s1)
	add	s1, s2, s10
	vse64.v	v8, (s1)
	add	s9, t4, s10
	vadd.vv	v16, v20, v16
	add	s11, t0, s10
	vle64.v	v20, (s11)
	vse64.v	v12, (s9)
	add	s1, t1, s10
	vse64.v	v16, (s1)
	vsll.vi	v20, v20, 1
	vadd.vv	v28, v8, v28
	vadd.vv	v28, v28, v12
	vadd.vv	v28, v28, v16
	vadd.vv	v28, v28, v20
	vse64.v	v28, (s11)
	add	s6, s6, s7
	add	s10, s10, s8
	bne	s6, s4, .LBB0_4
----
