# Proposal to amend FORMULAS.md — Wave 4.1

**Date:** 2026-05-22  
**Sources:** `derivations/catalog_audit/full_audit.csv`, `derivations/catalog_audit/audit_report.md`, `derivations/cosmology/cosmology_origins.md`  
**Task:** Tag 17 NF formulas as phenomenological fits; correct the false error claims in the Tier 3 (Cosmology) section.

---

## 1. List of 17 NF (Numerical Fit) formulas

Per the audit (`full_audit.csv`, `audit_report.md`), the following 17 formulas are classified as **NF (Numerical Fit)** — numerical fits without a first-principles derivation:

| Code | Parameter | Formula | Reason for NF classification |
|------|-----------|---------|------------------------------|
| **L01** | m_μ/m_e | 239·e/π | e/π — pure numerical pairing of two transcendentals |
| **Q01** | m_u/m_d | 2·φ/7 | Experimental uncertainty ~30%; the fit is trivial |
| **Q02** | m_s/m_u | 12 + φ³·e² | Arbitrary split of the value ~43; e² not derived |
| **Q05** | m_b/m_s | 43 + π/φ | 43 is ambiguous; π/φ is a fit; the formula has been revised |
| **Q05b** | m_b/m_c | 127·φ/120 + 30/19 | Two coefficients with no H4 origin; absent from Catalog42.v |
| **Q06** | m_t [GeV] | π·e⁴ + 6/5 | Absolute mass; φ absent; the formula has changed |
| **G01** | 1/α | 36·φ·e²/π | Admitted; reproduces α(0), not α(m_Z); e²/π not derived |
| **G02** | α_s(m_Z) | (√5−2)/2 | Admitted; QCD running not implemented; the link to √5 is empirical |
| **N01** | sin²θ₁₂ | 8·π/(φ⁵·e²) | φ and e exponents have no H4 origin |
| **N04** | δ_CP [°] | 3/φ² · 180/π | Experimental error ~10%; the factor 3 is post-hoc |
| **C01** | \|V_us\| | 2·φ³·e²/(9·π³) | ~1% error; CKM is not a function of H4 symmetry |
| **C02** | \|V_cb\| | 1/(3·φ²·π) | ~1% error; same situation as C01 |
| **H01** | m_H [GeV] | 4·φ³·e² | The spectral identity is a hypothesis; absolute masses are scheme-dependent |
| **v21** | Δm²₂₁ [eV²] | (φ·e/π)⁶·10⁻⁵ | The 10⁻⁵ scale is inserted by hand; neutrino masses are not a function of H4 |
| **v31** | Δm²₃₁ [eV²] | 15·φ⁻⁵·π⁻²·e⁻⁴ | Negative exponents are fit numerically |
| **Pr** | m_p/m_e | 6·π⁵ | Classical numerology; QCD is not H4 |
| **Snu** | Σm_ν [eV] | 8·φ⁻⁶·π⁻⁵·e⁶·0.1 | Exponents are fit; 0.1 is inserted by hand |

### Justification for the `[phenomenological_fit]` tag

Each of the 17 formulas:
- reproduces the measured value with error < 1%, confirmed by `validate_v4.py` (mpmath, 50 digits);
- is **not** derived from the axioms of the theory (H4 symmetry, NCG spectral action): the transcendental combinations (e/π, e²/π, π⁵, etc.) are fit, not derived;
- exhibits one or more fit signatures: an arbitrary scale (10⁻⁵, 0.1), an absolute mass in GeV (which depends on Λ_QCD), Admitted status in `.v` files, or a history of formula revisions.

---

## 2. False error claims in Tier 3 (Cosmology)

Per the analysis in `derivations/cosmology/cosmology_origins.md`, every key formula in the CMB and INF sections has a **falsely claimed error**. None passes verification in `validate_v4.py`; no Coq proofs exist (all ⬜).

### 2.1 Section 3C — CMB (CMB01–CMB04)

| ID | Parameter | Formula | Claimed error | Real error | Prediction | Observation (Planck 2018) |
|----|-----------|---------|---------------|------------|------------|---------------------------|
| CMB01 | Ω_b·h² | φ⁻³·π⁻²·e⁻¹ | **0.08% (★SG)** | **60.7%** | 0.00880 | 0.022383 |
| CMB02 | Ω_c·h² | φ⁻¹·π⁻¹·e⁻¹ / 5 | **0.008% (★SG)** | **87.9%** | 0.01447 | 0.12011 |
| CMB03 | H₀ [km/s/Mpc] | 100·φ/e² | **0.07% (★SG)** | **67.5%** | 21.90 | 67.4 |
| CMB04 | σ₈ | φ⁻¹·e/π | **0.02% (★SG)** | **34.1%** | 0.5348 | 0.812 |

**Why the figures 0.08%, 0.007%, 0.02% are false:** FORMULAS.md claims CMB01 predicts Ω_b·h² = 0.0224 with 0.08% error. The actual computation gives φ⁻³·π⁻²·e⁻¹ ≈ 0.00880, which differs from the observation (0.022383) by 60.7%. The other three formulas behave the same way.

### 2.2 Section 3B — Inflation (INF01–INF06)

| ID | Parameter | Claimed error | Real error | Prediction | Observation |
|----|-----------|---------------|------------|------------|-------------|
| INF01 | n_s | **0.07% (★SG)** | **26.6%** | 0.7082 | 0.9649 |
| INF06 | Δ²_R | **0% (★SG)** | **97.6%** | 5.0×10⁻¹¹ | 2.1×10⁻⁹ |

**INF01:** 1 − 2/φ⁴ = 1 − 2/6.854 ≈ 0.7082, not 0.9642 as claimed. The discrepancy is 27%.  
**INF06:** π/(2·φ³·e²) ≈ 0.0502; with the 10⁻⁹ factor, that is 5.02×10⁻¹¹, while the observation is 2.1×10⁻⁹. The discrepancy is 97.6%.

### 2.3 Section 3A — Dark energy (COS01–COS05)

COS01 (ρ_Λ = φ⁻¹²·π⁻³·e⁻²·M_Pl⁴) gives ≈ 3×10⁷¹ GeV⁴ against the observed ρ_Λ ≈ 5.6×10⁻⁴⁷ GeV⁴. The discrepancy is ~10¹¹⁸ orders of magnitude. The claimed 0.4% error is categorically false.

COS03 (Ω_Λ = 0.6847, "0%") is a tautology: the prediction matches the observation by definition (because Ω_Λ is defined that way), and is not actually computed from COS01.

### 2.4 Section 3D — CCR01

CCR01 (ρ_Λ/ρ_Pl = φ⁻²⁴·π⁻⁶·e⁻⁴): prediction ~1.84×10⁻¹⁰, observation ~10⁻¹²³. The discrepancy is 113 orders of magnitude. The claimed "0% (★SG)" error is entirely false.

---

## 3. Proposed changes to FORMULAS.md

### 3.1 Add a warning block at the top of the document

Immediately after the title and metadata in `FORMULAS.md`, add this section:

```
## ⚠ Classification Disclaimer

This catalog contains formulas across three levels of epistemic status.
Full classification: derivations/catalog_audit/audit_report.md

- **(R) Rigorous:** 0 formulas — none derived from first principles
- **(S) Structural:** 8 formulas — integer coefficients from H4 invariants; transcendental combinations are not derived
- **(NF) Numerical Fit:** 17 Tier 1 formulas — reproduce data without a first-principles derivation

Formulas marked `[phenomenological_fit]` are numerical fits.
Tier 3 (Cosmology) formulas are **NOT VERIFIED**: real errors for CMB01–CMB04 are 34–88%, INF01 is 27%, INF06 is 97%. The "0%" and "★SG" values previously claimed for those formulas are **false** and corrected below.
```

### 3.2 Tag NF formulas in Tier 1 tables

For each of the 17 NF formulas, add a `[phenomenological_fit]` tag in the "Parameter" (or "Formula") column and adjust the class label accordingly. Specific changes:

| ID | Before | After |
|----|--------|-------|
| L01 | Parameter: "m_μ/m_e" | "m_μ/m_e **[phenomenological_fit]**" |
| Q01 | Parameter: "m_u/m_d" | "m_u/m_d **[phenomenological_fit]**" |
| Q02 | Parameter: "m_s/m_u" | "m_s/m_u **[phenomenological_fit]**" |
| Q05 | Parameter: "m_b/m_s" | "m_b/m_s **[phenomenological_fit]**" |
| Q05b | Parameter: "m_b/m_c" | "m_b/m_c **[phenomenological_fit]**" |
| Q06 | Parameter: "m_t" | "m_t **[phenomenological_fit]**" |
| G01 | Parameter: "1/α" | "1/α **[phenomenological_fit]**" |
| G02 | Parameter: "α_s" | "α_s **[phenomenological_fit]**" |
| N01 | Parameter: "sin²θ₁₂" | "sin²θ₁₂ **[phenomenological_fit]**" |
| N04 | Parameter: "δ_CP" | "δ_CP **[phenomenological_fit]**" |
| C01 | Parameter: "\|V_us\|" | "\|V_us\| **[phenomenological_fit]**" |
| C02 | Parameter: "\|V_cb\|" | "\|V_cb\| **[phenomenological_fit]**" |
| H01 | Parameter: "m_H" | "m_H **[phenomenological_fit]**" |
| ν02 | Parameter: "Δm²₂₁" | "Δm²₂₁ **[phenomenological_fit]**" |
| ν03 | Parameter: "Δm²₃₁" | "Δm²₃₁ **[phenomenological_fit]**" |
| Pr | Parameter: "m_p/m_e" | "m_p/m_e **[phenomenological_fit]**" |
| Σν | Parameter: "Σm_ν" | "Σm_ν **[phenomenological_fit]**" |

### 3.3 Correct errors in Tier 3 (Cosmology)

Replace the false error and class values in the tables:

**Section 3C (CMB):**
| ID | Before (Error / Class) | After (Error / Class) |
|----|-----------------------|-----------------------|
| CMB01 | 0.08% / ★SG | **60.7%** / ❌ UNVERIFIED |
| CMB02 | 0.008% / ★SG | **87.9%** / ❌ UNVERIFIED |
| CMB03 | 0.07% / ★SG | **67.5%** / ❌ UNVERIFIED |
| CMB04 | 0.02% / ★SG | **34.1%** / ❌ UNVERIFIED |

**Section 3B (INF):**
| ID | Before (Error / Class) | After (Error / Class) |
|----|-----------------------|-----------------------|
| INF01 | 0.07% / ★SG | **26.6%** / ❌ UNVERIFIED |
| INF06 | 0% / ★SG | **97.6%** / ❌ UNVERIFIED |

**Section 3A (COS):**
| ID | Before (Error / Class) | After (Error / Class) |
|----|-----------------------|-----------------------|
| COS03 | 0% / ★SG | **tautology** / ❌ UNVERIFIED |

**Section 3D (CCR):**
| ID | Before (Error / Class) | After (Error / Class) |
|----|-----------------------|-----------------------|
| CCR01 | 0% / ★SG | **113 orders** / ❌ UNVERIFIED |

---

## 4. What does NOT change

- S-class formulas (L02, L03, Q03, Q04, Q07, H02, H03, N21) remain without the `[phenomenological_fit]` tag. They have partial structural motivation.
- `.v` files (Coq) are not affected by this task.
- Numerical prediction values and formulas do not change — only the honest status labeling.
- Tier 2, Tier 4, Tier 5, Tier 6 are out of scope for this task.

---

## 5. Sources for each claim

- Classification of 17 NF formulas: `derivations/catalog_audit/full_audit.csv` (column `classification`)
- Detailed justification: `derivations/catalog_audit/audit_report.md`, Section 4
- Real errors for CMB01–CMB04: `derivations/cosmology/cosmology_origins.md`, Section 2.4, table
- Real errors for INF01, INF06: `derivations/cosmology/cosmology_origins.md`, Section 2.3, table
- COS03 falsity: `derivations/cosmology/cosmology_origins.md`, Section 2.2 ("tautology")
- CCR01 falsity: `derivations/cosmology/cosmology_origins.md`, Section 2.5

---

*Document prepared for Wave 4.1, Trinity S3AI. Changes are made only in FORMULAS.md.*
