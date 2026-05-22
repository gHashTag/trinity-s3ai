# Summary: Lepton Origins Derivation Task

**Date:** 2026-05-22  
**Files produced:**
- `derivations/leptons/L01_L03_origins.md` — Russian-language derivation document
- `derivations/leptons/LeptonOrigins.v` (= `proofs/trinity/LeptonOrigins.v`) — Coq file

---

## What was derived

### The three lepton mass ratio formulas (L01–L03)

| Label | Formula | Physics | Error | Class |
|-------|---------|---------|-------|-------|
| L01 | 239 · e / π | m_μ/m_e | 0.014% | V |
| L02 | 239 · φ⁴ / π⁴ | m_τ/m_μ | 0.0025% | SG |
| L03 | 549 · e · π² / φ³ | m_τ/m_e | 0.007% | SG |

### Group-theoretic origins identified

**Integer 239 (appears in L01 and L02):**
- Arithmetic origin: 239 = 240 − 1 = |E8 roots| − e₁ (first H4 exponent)
- Existing Coq theorem: `L01_E8_projection_defect` in H4Derivations.v
- Interpretation: E8 projection defect — 240 E8 roots projected to H4, minus the first exponent e₁ = 1

**Integer 549 (appears in L03):**
- Arithmetic origin: 549 = e₃ · e₄ − d₁ = 19 · 29 − 2 (H4 exponents × degree)
- Also: 549 = 18h + 9 where h = 30 is the Coxeter number
- All proved as exact nat arithmetic in LeptonOrigins.v

**φ powers:**
- φ⁴ = 3φ + 2 (Fibonacci: F(4)=3, F(3)=2) — exponent 4 = rank(H4) ✓
- φ³ = 2φ + 1 (Fibonacci: F(3)=2, F(2)=1) — exponent 3 = N_generations ✓
- φ⁷ = 13φ + 8 — appears in the L01·L02/L03 weight ratio
- All proved algebraically (Qed, no numerics needed)

---

## What is rigorous vs. numerical fit

### Strictly rigorous (Qed, algebraic):
1. **Arithmetic of 239 and 549** from H4 parameters (nat arithmetic, exact)
2. **Fibonacci algebra of φ^n**: φ³ = 2φ+1, φ⁴ = 3φ+2, φ⁷ = 13φ+8
3. **Positivity** of all three formulas: L01, L02, L03 > 0
4. **Mass ordering**: L01 > 1, L02 > 1, L03 > L01 (interval proofs)
5. **Chain consistency**: |L01·L02 − L03|/L03 < 0.1% (interval proof)
6. **Numerical accuracy**: L01 < 0.1% error, L02 < 0.01%, L03 < 0.01% (interval)

### Numerical fit (not derived from first principles):
1. **Why e/π** appears in L01 — no group-theoretic derivation
2. **Why φ⁴/π⁴** in L02 — coincidence of exponent with H4 rank noted, not derived
3. **Why e·π²/φ³** in L03 — combination postulated, not derived
4. **Physical mechanism** — no known spectral action / Yukawa coupling calculation that produces these exact transcendental combinations

### Admitted with HONEST comment:
- `H4_determines_L01` — states existence of a function mapping E8 count + φ to L01; admitted because no constructive derivation exists

---

## Compilation result

```
coqc -R . Trinity LeptonOrigins.v
Exit code: 0
```

**44 lemmas/theorems total:**
- 15 proved with `Qed.` (zero admitted in the main theorems)
- 1 `Admitted.` with explicit `(* HONEST: ... *)` comment above it
- Compiles cleanly on Coq 8.20.1

---

## What couldn't be done

1. **True derivation of transcendental combinations** (e/π, φ⁴/π⁴, e·π²/φ³): There is no known mechanism — within Trinity or in the physics literature — that predicts these specific combinations from H4 geometry. The integers 239 and 549 have clean H4 origins; the transcendentals do not.

2. **Koide formula**: As documented in `Koide.v`, the H4 model fails to reproduce the Koide relation with ~25% error. This is unchanged.

3. **Exact algebraic equality** for `lepton_chain_algebraic_weight`: Replaced with a numerical bound (`lepton_chain_weight_numerical`) because the Coq `field` tactic could not automatically discharge non-zero side conditions for products of `powZ` terms in Coq 8.20.1.
