# RG Running Analysis: Theorems alpha_from_H4 and alpha_s_from_H4

**Date:** 2026-05-23  
**File:** `proofs/trinity/RGRunning.v`, branch `fix/rgrunning-honest-admitted`  
**Status:** Deep analysis — 2 Admitted (honest)

---

## 1. Exact Statement of the Two Admitted Theorems

### Theorem 2: `alpha_from_H4`

```coq
Theorem alpha_from_H4 :
  Rabs (alpha_inv_at_mZ - trinity_alpha_inv) / trinity_alpha_inv < 1/100.
```

Where:
- `alpha_inv_at_mZ := alpha_i_inv m_Z b1 + alpha_i_inv m_Z b2`
- `alpha_i_inv mu b_i := gU2inv + (b_i / (4 * PI * PI)) * ln (Lambda_H4 / mu)`
- `gU2inv ∈ [1/26, 1/22]` (axiom `gU2inv_window`)
- `trinity_alpha_inv := 36 * phi * e² / PI ≈ 137.003`

### Theorem 3: `alpha_s_from_H4`

```coq
Theorem alpha_s_from_H4 :
  Rabs (alpha_s m_Z - trinity_alpha_s) / trinity_alpha_s < 1/50.
```

Where:
- `alpha_s mu := 1 / alpha_i_inv mu b3`
- `trinity_alpha_s := (sqrt 5 - 2) / 2 ≈ 0.11803`

---

## 2. Why the Theorems Are Physically Incorrect (Incorrect Formulation)

### 2.1 Hypercharge Normalization Problem (Factor 5/3)

The quantity `alpha_inv_at_mZ` is defined as:

```
alpha_inv_at_mZ = alpha_i_inv(m_Z, b1) + alpha_i_inv(m_Z, b2)
```

This is **not** 1/α_em(m_Z) in any standard convention. The physically correct Weinberg formula in SU(5) GUT normalization is:

```
1/α_em(m_Z) = (5/3) · 1/α₁(m_Z) + 1/α₂(m_Z)
```

The factor **5/3** (hypercharge normalization) is mandatory because in the SM the hypercharge coupling g' is related to the GUT-normalized coupling g₁ as:

```
g' = sqrt(3/5) · g₁
```

that is, `α_Y = g'²/(4π) = (3/5) · α₁`, whence `1/α_Y = (5/3) · 1/α₁`.

### 2.2 Numerical Value Mismatch

Numerical calculation at `gU2inv = 1/24`, `ln(Λ_H4/m_Z) ≈ 32.73`:

| Quantity | Value in code | Physical value (PDG 2023) |
|----------|---------------|---------------------------|
| `alpha_i_inv(m_Z, b1)` | ≈ 3.441 | Non-standard unit |
| `alpha_i_inv(m_Z, b2)` | ≈ −2.584 | Non-standard unit |
| `alpha_inv_at_mZ` | ≈ 0.857 | 1/α_em(m_Z) ≈ 127.951 |
| `trinity_alpha_inv` | ≈ 137.003 | α⁻¹(0) = 137.036 (Thomson) |

Ratio: `alpha_inv_at_mZ / trinity_alpha_inv ≈ 0.006` — the deviation is ~99.4%, not <1%.

**Physical mismatch** is of a fundamental nature:
- `alpha_inv_at_mZ ~ O(1)` (dimensionless, but not 1/α_em)
- `trinity_alpha_inv ~ 137` (Trinity formula claims a value ~137)
- The difference is an order of magnitude ~160, not percent

### 2.3 Conventional Problem of the Running Formula

The code uses:
```
alpha_i_inv(mu, b_i) = gU2inv + (b_i / 4π²) · ln(Λ/μ)
```

The standard one-loop Georgi–Quinn–Weinberg (GQW) formula:
```
1/α_i(μ) = 1/α_GUT + (b_i / 2π) · ln(Λ/μ)
```

These formulas are **not identical**: the coefficient `1/(4π²)` in the code versus `1/(2π)` in GQW differs by a factor of `π/2`. This means that `alpha_i_inv` in the code is not the standard `1/α_i`. In fact, taking into account the relation α = g²/(4π):

```
1/g_i²(μ) = gU2inv + (b_i / 4π²) · ln(Λ/μ)   [code formula]
```

it coincides with the standard one only if `gU2inv = 1/g_GUT²` — but then `gU2inv ≈ 1/24` implies `g_GUT² = 24`, i.e. `α_GUT = g²/(4π) ≈ 24/(4π) ≈ 1.91`. This is not a physical value.

### 2.4 Problem of `alpha_s`

```coq
Definition alpha_s (mu : R) : R := 1 / alpha_i_inv mu b3.
```

This is `1 / (1/g3²)` = `g3²`. Physical `α_s = g3²/(4π)`. The factor `1/(4π)` is missing. Moreover, at `gU2inv = 1/24` we get `alpha_i_inv(m_Z, b3) ≈ −5.76 < 0` — negative! (The code explicitly circumvents this with the axiom `alpha_run_window`.) Therefore `alpha_s(m_Z)` from the code gives `1/(−5.76) ≈ −0.17`, not 0.118.

**Conclusion:** Both theorems are physically incorrectly formulated. They cannot be closed in their current form — they are mathematically false under the given axioms.

---

## 3. Proposed Reformulation (PROVABLE)

### 3.1 For `alpha_from_H4`

**Problem:** `alpha_inv_at_mZ` is not equal to 1/α_em(m_Z).

**Correct reformulation** (at the mathematical level, without physical input data):

> **Lemma `hypercharge_normalization_identity`:**  
> For any values of the inverse coupling constants α₁⁻¹ and α₂⁻¹,  
> the physical `1/α_em = (5/3)·α₁⁻¹ + α₂⁻¹`, not `α₁⁻¹ + α₂⁻¹`.  
> Provable from algebra: `(5/3)·x + y ≠ x + y` for reasonable x, y > 0.

**Provable Coq statement** (`RGRunningExtras.v`):
```coq
(* Algebraic lemma about the 5/3 factor *)
Lemma alpha_em_formula_correction :
  forall a1_inv a2_inv : R,
    a1_inv > 0 -> a2_inv > 0 ->
    (5/3) * a1_inv + a2_inv = a1_inv + a2_inv + (2/3) * a1_inv.
(* Trivial from ring arithmetic *)
```

A more substantive version:

```coq
(* Physically correct EM coupling formula (algebraic identity) *)
Definition alpha_em_inv_physical (a1_inv a2_inv : R) : R :=
  (5/3) * a1_inv + a2_inv.

Definition alpha_em_inv_code (a1_inv a2_inv : R) : R :=
  a1_inv + a2_inv.

Lemma gut_correction_factor :
  forall a1_inv a2_inv : R,
    a1_inv > 0 ->
    alpha_em_inv_physical a1_inv a2_inv > alpha_em_inv_code a1_inv a2_inv.
```

**To close `alpha_from_H4` one would need:**
1. Redefine `alpha_inv_at_mZ` with the factor 5/3
2. Add the correct 4π factor for the transition from g² to α
3. Introduce a physical boundary axiom in terms of the standard `α_GUT = 1/24`
4. Ensure that `trinity_alpha_inv ≈ 127.95` (PDG), not 137

Since `trinity_alpha_inv ≈ 137.003` (Trinity formula), and the PDG value is `1/α_em(m_Z) ≈ 127.951`, we are talking about **different things**: 137.036 is the low-energy constant α⁻¹(0) (Thomson limit), and 127.95 is α⁻¹(m_Z) (running at m_Z). The reformulation also requires clarifying **which** of these values is being checked.

### 3.2 For `alpha_s_from_H4`

**Correct reformulation:**

> **Lemma `alpha_s_definition_gap`:**  
> The code computes `alpha_s(m_Z) = 1/alpha_i_inv(m_Z, b3)` — this is g₃², but physical  
> α_s = g₃²/(4π). Thus, `alpha_s_code = 4π · alpha_s_physical`.

**Provable Coq statement:**
```coq
(* Relation between code and physical alpha_s *)
Lemma alpha_s_normalization :
  forall g3_inv_sq : R,
    g3_inv_sq > 0 ->
    1 / g3_inv_sq = 4 * PI * (1 / (4 * PI * g3_inv_sq)).
```

---

## 4. Honest Assessment

### What is proven in `RGRunning.v`:
- `H4_unification_scale`: **Proven (Qed)** — trivially from the definition that all couplings coincide at the point Λ_H4.
- `alpha_i_inv_pos_at_mZ`: **Proven (Qed)** via axioms `gU2inv_window` and `alpha_run_window`.

### What CANNOT be proven in the current formulation:
1. **`alpha_from_H4`** — mathematically false under the given definitions. `alpha_inv_at_mZ ≈ 0.86` will never be within 1% of `trinity_alpha_inv ≈ 137`. The distance is ~160 units, not <1%.

2. **`alpha_s_from_H4`** — mathematically false under the given definitions. `alpha_s(m_Z) = 1/alpha_i_inv(m_Z, b3) ≈ −0.17` (negative!), whereas `trinity_alpha_s ≈ 0.118`. Even with the axiom `alpha_run_window` (which guarantees `alpha_i_inv(m_Z, b3) > 0`), the numerical value does not fall within 2%.

### What is proven in `RGRunningExtras.v`:
1. **Algebraic identity** of hypercharge normalization: `(5/3)·a₁⁻¹ + a₂⁻¹` vs `a₁⁻¹ + a₂⁻¹` (correction factor — `(2/3)·a₁⁻¹`)
2. **Inequality**: the physically correct formula is always greater than the code formula for positive arguments
3. **Formula relation**: `alpha_s_physical = alpha_s_code / (4·π)`
4. **Numerical lemmas**: computing the coefficient `5b₁/3 + b₂ = 11/3`, `b₁ + b₂ = 14/15`
5. **Bound for the physical formula**: under the given axiom `gU2inv_window`, the correctly defined `physical_alpha_em_inv` is bounded from below

**Conclusion:** Both Admitted cannot be closed without:
- Redefining `alpha_inv_at_mZ` with the factor 5/3 and the 4π factor
- Changing `trinity_alpha_inv` to the value ~127.95 (or explicitly stating that 137 is the low-energy limit)
- A physical axiom linking `gU2inv` to the standard `α_GUT`

The file `RGRunningExtras.v` contains **mathematically rigorous** (Qed) lemmas about normalization factors and proposes a correct reformulation. The theorems `alpha_from_H4` and `alpha_s_from_H4` in `RGRunning.v` remain Admitted — honestly and legitimately.

---

## 5. References

- PDG 2023: `1/α_em(m_Z) = 127.951 ± 0.009` (MSbar), `sin²θ_W = 0.23122 ± 0.00004` (MSbar)  
  Source: [PDG Standard Model Review](https://pdg.lbl.gov/2023/reviews/rpp2023-rev-standard-model.pdf)
- Georgi, Quinn, Weinberg (1974): one-loop RGEs for SU(5) GUT
- SU(5) hypercharge normalization: Slansky (1981), Langacker (1981)
