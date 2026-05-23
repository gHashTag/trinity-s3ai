# F₄ Dirac Spectrum — Wave 14.3

## Setup

- **Binary octahedral 2O**: order **48** (COMPLETE — all 48 elements constructed and verified).
- **2O construction**:
  - 24 Hurwitz units (binary tetrahedral 2T): 8 integer units ±1,±i,±j,±k + 16 half-units (±1±i±j±k)/2.
  - 24 coset elements: 2T · (1+i)/√2, where (1+i)/√2 has order 8.
- **Discrete Dirac operator**: D_F on ℂ^192 (48 vertices × 4 spinor components).
- **Adjacency**: inner-product criterion (dot ≈ 0.5 on unit quaternions).
  - Short-short edges → 24-cell graph (degree 8).
  - Long-long edges → D4 root graph (degree 8).
  - Short-long edges → none (dot = 0 or ±1/√2).

## 2O Verification

| Check | Result |
|-------|--------|
| Order | **48** ✓ |
| All norms = 1 | **PASS** ✓ |
| Group closure | **PASS** ✓ (0 missing products out of 48×48) |
| Multiplication table | 48 × 48 |

## Spectrum

| λ          | Multiplicity |
|------------|-------------|
| ±1.5227    | 4           |
| ±1.4142    | 4           |
| ±1.0000    | 12          |
| ±0.8660    | 12          |
| ±0.7071    | 8           |
| ±0.6567    | 4           |
| ±0.5000    | 16          |
| 0.0000     | 72          |

**Total**: 60 positive, 60 negative, 72 zero.

**Comparison with Wave 13.4**: The spectrum is **identical**. This is because the 48 normalized F4 roots already coincide with the 48 elements of 2O. The conceptual fix (correct group identification) does not alter the numerical spectrum, confirming the geometric consistency of the model.

## η-Invariant

| Quantity | Value |
|----------|-------|
| Discrete η (cutoff 10⁻⁶) | **0.0** |
| Target η (APS plumbing, S³/2O) | **−7/4 = −1.75** |
| Discrepancy | **Integer vs fractional** |

**Explanation**: The discrete Dirac operator anticommutes with Γ⁵, so non-zero eigenvalues come in exact ±λ pairs. Counting signs gives n_pos = n_neg, hence η = 0 for any symmetric cutoff. The true η-invariant requires zeta-regularized spectral asymmetry, not mere sign counting. The mismatch is expected and honestly documented.

## Key Findings

1. **2O construction COMPLETE** ✓
   - 48/48 elements found.
   - All norms = 1, group closure verified.
   - Multiplication table size 48×48.

2. **KO-dimension = 6 mod 8** ✓
   - J² = +1, JD = DJ, JΓ = ΓJ, DΓ = −ΓD.
   - Matches Standard Model requirement (same as H₄/2I).

3. **Vector-like spectrum**
   - n_pos = n_neg = 60.
   - Discrete η = 0 (not −7/4).
   - Chiral symmetry preserved (D anticommutes with Γ⁵).

4. **Zero modes abundant**
   - 72 zero modes out of 192 eigenvalues (37.5%).
   - Likely a discretization artifact of the adjacency construction.
   - Physical interpretation requires Yukawa couplings or mass terms.

## Comparison Table

| System | Roots/|Γ|  | |Γ|  | KO-dim | η (discrete) | η (target) | 3-gen? |
|--------|-------------|------|--------|--------------|------------|--------|
| H₄/2I  | 120         | 120  | 6      | 0            | −2         | NO     |
| D₄/2T  | 24          | 24   | 5      | 0            | −3/2       | NO     |
| F₄/2O  | 48          | 48   | 6      | **0**        | **−7/4**   | OPEN   |

*2O is now complete in this model. η target is the APS plumbing value for S³/2O.

## Honest Verdict

Completing the 2O construction **does not change the F4 conclusion**:

- **KO-dim = 6** (SM-like) ✓
- **Spectrum symmetric** (n_pos = n_neg) ✓
- **Chiral symmetry preserved** (DΓ = −ΓD) ✓
- **η = 0** in the discrete model, not the target −7/4. This is a **fundamental limitation of sign-counting** vs zeta regularization, not a bug.
- **Zero modes remain abundant** (72/192). Their physical role is unclear without Yukawa couplings.
- **No automatic 3-generation structure** is observed.

F4 remains **structurally promising** (crystallographic, KO-dim = 6) but **incomplete** as a phenomenological model. The missing ingredients are:
1. A mechanism to lift the 72 zero modes (Yukawa / Higgs sector).
2. A spectral action or heat-kernel regularization that reproduces η = −7/4.
3. A 3-generation pattern (possibly from a sublattice or twisting).

**Status: F4 survives as a candidate but remains incomplete. The 2O group is now fully constructed and verified.**
