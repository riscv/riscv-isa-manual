# Normative Tag Mismatch Report

This document lists all mismatches between tag names referenced in normative rule YAML definitions and the actual tags present in the AsciiDoc source files.

Generated from: `make build-norm-rules` output

## Summary

Found **78 tag mismatches** across multiple files. Common patterns include:
- Missing `norm:` prefix in YAML references
- Typos in tag names
- Tag names that don't exist in source at all (need to be added)
- Incorrect tag references (wrong field/instruction names)

## Detailed Findings by File

### 1. normative_rule_defs/hypervisor.yaml

| Rule Name | Missing Tag | Likely Issue |
|-----------|-------------|--------------|
| `vsatp-ppn_sz` | `norm:satp-ppn_sz_param` | Tag doesn't exist in source - needs to be added to `supervisor.adoc` |
| `vsatp-asidlen` | `norm:satp-asidlen_param` | Tag doesn't exist - should reference `norm:satp-asid` or create new tag |

**Note**: Found `[[norm:satp-asid]]` in supervisor.adoc line 1006, but YAML references `norm:satp-asidlen_param`

---

### 2. normative_rule_defs/smctr.yaml

| Rule Name | Missing Tag | Actual Tag in Source | Fix Needed |
|-----------|-------------|---------------------|------------|
| `sctrdepth-depth` | `norm:sctrdepth-depth` | Multiple tags exist: `norm:sctrdepth-depth_op0`, `norm:sctrdepth-depth_op1`, `norm:sctrdepth-depth_param` | Update YAML to use correct tags |
| `varios_jump_enc` | `various_jump_enc` | `norm:various_jump_enc` | **Missing `norm:` prefix** - add to tag in YAML |
| `freeze` | `norm:sctrstatus-frozen_set` | `[norm:sctrstatus-frozen_set]` (inline tag, missing `#`) | Fix tag in `smctr.adoc` line 728 - should be `[#norm:sctrstatus-frozen_set]#` |

---

### 3. normative_rule_defs/supervisor.yaml

| Rule Name | Missing Tag | Actual Tag in Source | Fix Needed |
|-----------|-------------|---------------------|------------|
| `satp-mode_sxlen32` | `norm:ssatp-mode_sxlen32` | `[[norm:satp-mode_sxlen32]]` | **Typo**: YAML has extra 's' - change to `norm:satp-mode_sxlen32` |
| `satp-asidlen_param` | `norm:satp-asidlen_param` | Not found | Tag missing from source - needs to be added |
| `satp_op_sfence-vma` | `norm:satp_op_sfence-vma` | Not found | Tag missing from source - needs to be added |
| `norm:load_page_fault_no_r` | `norm:load_page_fault_no_r` | `[norm:load_page_fault_no_r]` (line 1471) | **Missing inline syntax** - should be `[#norm:load_page_fault_no_r]#...#` |

---

### 4. normative_rule_defs/v-st-ext.yaml

| Rule Name | Missing Tag | Status |
|-----------|-------------|--------|
| `vsstatus-vs_op2` | `norm:vsstatus-vs_op2` | Tag missing from source |
| `vcsr-vxsat_op` | `norm:vcsr-vxsat` | Tag missing from source |
| `vector_ls_constant_stride_x0_opt_param` | `norm:vector_ls_constant_stride_x0_opt_param` | Tag missing from source |
| `vsmul_op` | `norm:vsmul_op_sat_vxsat_op_vs_mul` | Tag missing from source |
| `vxsat_op_vsmul` | `norm:vsmul_op_sat_vxsat_op_vs_mul` | Tag missing from source |
| `vmfeq_sNaN_invalid` | `norm:vmfeq_sNaN_invalid_vmfne_sNaN_invalid` | Tag missing from source |
| `vmfne_sNaN_invalid` | `norm:vmfeq_sNaN_invalid_vmfne_sNaN_invalid` | Tag missing from source |
| `vfredosum_op` | `norm:vfredosum_op_maskoff` | Tag missing from source |
| `vfredusum_op` | `norm:vfredupsum_op` | Tag missing from source |
| `vfwredusum_additive_impl` | `norm:vfwredusum_additive_impl` | Tag missing from source |
| `vcpop_op_vl0` | `norm:vcpop_op_vl0` | Tag missing from source |
| `vrgatherei16-vv_sew_lmul` | `norm:vrgatherei16-vv_sew_lmul` | Tag missing from source |

---

### 5. normative_rule_defs/vector-crypto.yaml

| Rule Name | Missing Tag | Status |
|-----------|-------------|--------|
| `veccrypto_vl_vstart_egsconstr` | `norm:veccrypto_vl_egsconstr`, `norm:veccrypto_vstart_egsconstr` | Both tags missing |
| `veccrypto_vl_vstart_rsv` | `norm:veccrypto_vl_rsv`, `norm:veccrypto_vstart_rsv` | Both tags missing |
| `vsm3c-vi_sewn32_rsv` | `norm:vsm3c-vi_sewn32_rsv` | Tag missing from source |
| `vsm4r_op` | `norm:vsm4r_op` | Tag missing from source |

---

### 6. normative_rule_defs/zfa.yaml

| Rule Name | Missing Tag | Status |
|-----------|-------------|--------|
| `fli-d_op` | `norm:fli-d_op` | Tag missing from source |

---

### 7. normative_rule_defs/zfh.yaml

**Major issues**: Many tags don't exist in source

| Rule Name | Missing Tag | Status |
|-----------|-------------|--------|
| `fsh_op`, `flh_op` | `norm:fsh_flh_op` | Tag missing from source |
| `fsh_atomic_align`, `flh_atomic_align` | `norm:fsd_flh_atomic_align` | **Typo**: `fsd` should be `fsh` |
| `fsh_bits_maintained`, `flh_bits_maintained` | `norm:fsh_flh_bits_maintained` | Tag missing from source |
| Multiple computational ops | `norm:Zfh_computational_instrs` | Tag missing from source |
| Multiple compare ops | `norm:Zfh_compare_instrs` | Tag missing from source |
| `fcvt-w-h_op`, `fcvt-l-h_op` | `norm:fcvt-w-h_fcvt-l-h_op` | Tag missing from source |
| `fcvt-h-w_op`, `fcvt-h-l_op` | `norm:fcvt-h-w_fcvt-h-l_op` | Tag missing from source |
| `fcvt-wu-h_op`, etc. | `norm:fcvt-wu-h_fcvt-lu-h_fcvt-h-wu_fcvt-h-lu_op` | Tag missing from source |
| `fcvt-s-h_op`, `fcvt-h-s_op` | `norm:fcvt-s-h_fcvt-h-s_op` | Tag missing from source |
| `fcvt-d-h_op`, `fcvt-h-d_op` | `norm:fcvt-d-h_fcvt-h-d_op` | Tag missing from source |
| `fcvt-q-h_op`, `fcvt-h-q_op` | `norm:fcvt-q-h_fcvt-h-q_op` | Tag missing from source |
| Sign injection ops | `norm:fsgnj-h_fsgnjn-h_fsgnjx-h_op` | Tag missing from source |
| `fclass-h_op` | `norm:fclass-h_op` | Tag missing from source |
| `zfhmin_instrs` | `norm:zfhmin` | Tag missing from source |
| Multiple `fcvt` ops | `norm:fcvt_long_half_rv64_only` | Tag missing from source |

---

### 8. normative_rule_defs/zicsr.yaml

| Rule Name | Missing Tag | Actual/Status |
|-----------|-------------|---------------|
| `zicsr_rs1_x0` | `norm:Zicsr:csrrw_rs1_x0` | Tag missing - needs `Zicsr:` namespace? |
| `zicsr_order` | `#norm:csrr_order` | **Invalid syntax**: starts with `#` instead of being inline tag |
| `zicsr_fence_ordering` | `norm:csr_fence_ordering` | Tag missing from source |
| `zicsr_strongly_ordered` | `norm:csr_strongly_ordered` | Tag missing from source |

---

### 9. normative_rule_defs/zifencei.yaml

| Rule Name | Missing Tag | Status |
|-----------|-------------|--------|
| `fence_i_op` | `norm:fence_i` | Tag missing from source |

---

## Action Items

### High Priority (Syntax Errors)

1. **smctr.yaml**: Fix `varios_jump_enc` - add `norm:` prefix to tag name
2. **supervisor.yaml**: Fix `satp-mode_sxlen32` - remove extra 's' (change `ssatp` to `satp`)
3. **smctr.adoc line 728**: Fix inline tag syntax: `[norm:sctrstatus-frozen_set]` → `[#norm:sctrstatus-frozen_set]#...#`
4. **supervisor.adoc line 1471**: Fix inline tag syntax for `load_page_fault_no_r`
5. **zicsr.yaml**: Fix tag reference with invalid `#` prefix

### Medium Priority (Tag Typos)

1. **zfh.yaml**: Fix `norm:fsd_flh_atomic_align` → should be `norm:fsh_flh_atomic_align`

### Low Priority (Missing Tags - Need Review)

Many tags are completely missing from source files. For each:
1. Determine if tag should be added to source
2. Determine if YAML reference is incorrect
3. Check if text exists but isn't tagged

**Files needing most attention:**
- `src/zfh.adoc` - missing ~30 tags
- `src/v-st-ext.adoc` - missing ~12 tags
- `src/vector-crypto.adoc` - missing ~6 tags

## Recommended Next Steps

1. **Quick wins**: Fix the syntax errors (High Priority items)
2. **Review with spec authors**: Determine which missing tags should be added to source vs removed from YAML
3. **Systematic tagging**: Add missing tags to source files based on spec author input
4. **Re-run validation**: `make build-norm-rules` to verify fixes
