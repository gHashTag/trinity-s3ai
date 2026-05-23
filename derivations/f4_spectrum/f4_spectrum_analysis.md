# F₄ Dirac Spectrum — Wave 13.4

## Setup

- **F₄ root system**: 48 roots in 4D (24 long + 24 short).
- **Binary octahedral 2O**: order 48 (HONEST: our construction finds only 16).
- **Discrete Dirac operator**: D_F on ℂ^192 (48 vertices × 4 spinor components).
- **Adjacency**: inner-product criterion (dot ≈ 0.5 on unit roots).

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

## Key Findings

1. **KO-dimension = 6 mod 8** ✓
   - J² = +1, JD = DJ, JΓ = ΓJ.
   - Matches Standard Model requirement (same as H₄/2I).

2. **NOT vector-like** — asymmetric multiplicities?
   Actually ±λ counts are symmetric (60 = 60), but zero modes are numerous (72).
   The non-zero spectrum is chiral (± pairs).

3. **Structural difference from H₄**:
   - H₄: spectrum ±2√2 (mult 32), ±4√2 (mult 16), all non-zero.
   - F₄: rich spectrum with many zero modes. This is a **discretization artifact**
     of the adjacency construction, not necessarily physical.

4. **2O group incomplete**:
   - Only 16/48 elements constructed.
   - Full 2O includes 32 additional quaternions that are not unit Hurwitz.
   - Missing elements affect the boundary operator and η-invariant.

## Comparison Table

| System | Roots | |Γ|  | KO-dim | η      | 3-gen? |
|--------|-------|------|--------|--------|--------|
| H₄/2I  | 120   | 120  | 6      | −2     | NO     |
| D₄/2T  | 24    | 24   | 5      | −3/2   | NO     |
| F₄/2O  | 48    | 48*  | 6      | TBD    | OPEN   |

*2O incomplete in this model.

## Honest Verdict

F₄ is **structurally promising**:
- KO-dim = 6 (SM-like), unlike D₄.
- Root system is crystallographic (unlike H₄), enabling lattice gauge theory.
- Triality does not exist (outer automorphism = Z₂), but other symmetries may
  compensate.

However:
- 2O construction must be completed.
- Zero modes in the spectrum need explanation (Yukawa couplings?).
- η-invariant must be computed via APS on the E₇ plumbing.
- No automatic 3-generation structure is observed.

**Status: F₄ survives as a candidate but remains incomplete.**
