# Wave 5.3: Unimodularity and σ-Field

**Project:** Trinity S3AI Framework  
**Date:** 2026  
**Status:** Honest analysis — both verdicts include explicit caveats  

---

## Contents

1. [Subtask A: Unimodularity Check](#a-unimodularity)
2. [Subtask B: σ-Field in H4/600-Cell](#b-%CF%83-field)
3. [Summary Verdict Table](#summary-table)
4. [Conclusions for HiggsOrigins](#conclusions-for-higgsorigins)

---

## A. Unimodularity

### A.1 Problem in Standard NCG (Context)

In the Connes–Chamseddine program the unitary group of the finite algebra

```
A_F = ℂ ⊕ ℍ ⊕ M₃(ℂ)
```

equals **U(1) × SU(2) × U(3)**, not the exact gauge group of the Standard Model U(1) × SU(2) × SU(3). The transition U(3) → SU(3) requires imposing the **unimodularity condition**: the determinant of a unitary element from the M₃(ℂ) component equals 1. This condition is added *separately* and is not derived from the general NCG axioms (Chamseddine–Connes, 2007; Bochniak–Sitarz, 2022; Lizzi–Huggett–Menon, 2021).

Mathematically: the hypercharge generator U(1)_Y must be a traceless linear combination of generators of the A_F components. In the representation of the 16-dimensional multiplet (one generation)

```
Y = diag(−1/3, −1/3, −1/3, 1, 1/3, 1/3, 1/3, 0, ...)   (in ≪lepton+quark≫ basis)
```

the tracelessness Tr(Y) = 0 holds exactly when the set of SM hypercharges is anomaly-free — this is a nontrivial condition, automatically satisfied by the SM spectrum.

### A.2 H4-Derived Gauge Group: Structure

In Trinity S3AI the gauge group is motivated through the chain

```
H4  →  A4 (≅ SU(5))  →  SU(3)_C × SU(2)_L × U(1)_Y
```

with Coxeter number h = 30 = 2 × 3 × 5, providing three divisors associated with the ranks of SU(2), SU(3), SU(5) (proven in GaugeOrigins.v).

The unitary group of the H4 root system acts on the 4-dimensional root space; the natural "generators" arising from the decomposition h = 2 × 3 × 5 do not have a matrix representation with a definite trace in the NCG sense until an explicit fermion multiplet is specified.

### A.3 Tracelessness Check: Three Cases

**Case 1. A4-subsystem (path through SU(5))**

W(A4) = S₅, |Aut(A4)| = 240. In the standard SU(5) GUT the hypercharge generator in the fundamental **5** representation has the form

```
Y = diag(2/3, 2/3, 2/3, −1, −1)  →  Tr(Y) = 2 − 2 = 0.
```

This is a traceless generator inside A4 = su(5). **Conclusion:** the path H4 → A4 → SU(5)
*automatically* ensures tracelessness of the hypercharge generator, since the A4-algebra by definition consists of traceless matrices.
Thus, for this path the **unimodularity condition is automatically satisfied**.

**Case 2. Direct projection A2 × A2 → SU(3)_C × SU(2)_L**

From G01_G02_origins.md: W(A2 × A2) ⋊ Z₂ ≅ SU(3)_C × SU(3)_L.
Both A2 = su(3) algebras consist of traceless matrices. Therefore,
any generator arising from this subsystem is traceless.
**Conclusion:** unimodularity is satisfied for this path.

**Case 3. U(1)_Y and Coxeter numbers**

The problem appears where the "rank" origin of U(1)_Y does not connect the hypercharges of specific fermions. In Trinity S3AI the numbers {2, 12, 20, 30} specify periodicity orders, not direct matrix generators. For an explicit connection with U(1)_Y one needs a choice of embedding U(1)_Y ↪ SU(5) with GUT normalization (g' = g₁ · √(3/5)), which exactly coincides with the standard Georgi–Glashow construction. This step is **not derived** from H4 data, but postulated by analogy.

### A.4 Honest Verdict on A

| Path | Unimodularity | Remark |
|------|---------------|--------|
| H4 → A4 → SU(5) → SU(3)×SU(2) | **YES, automatically** | A4 = su(5) is traceless by definition |
| H4 → A2×A2 → SU(3)×SU(2) | **YES, automatically** | A2 = su(3) is traceless |
| H4 → U(1)_Y (hypercharge generator) | **NOT DERIVED** | Requires choice of GUT normalization, as in SU(5) |

**Verdict A:**  
If Trinity S3AI follows the SU(5) path (A4 ⊂ H4), then the unimodularity condition is automatically satisfied, since the su(5) algebra is traceless by definition.
However, H4 by itself does not generate a specific fermion multiplet with fixed hypercharges — this requires an additional physical choice.
Thus, within Trinity S3AI unimodularity is **realized by inheritance from A4 ⊂ H4**, but is not a new theoretical result compared to the standard SU(5) GUT.

---

## B. σ-Field

### B.1 What Is σ in Standard NCG

According to arXiv:1208.1030 (Chamseddine–Connes, 2012):

> "A real scalar field, strongly coupled to the Higgs field, was already present in the spectral model, but was mistakenly ignored in previous calculations."

The field σ is an **NCG singlet**: a real scalar field with quantum numbers B−L = 0. It arises from the coupling between the M₃(ℂ) (color) and ℂ (lepton) components of the fermionic Dirac operator D_F.
Technically σ appears as a fluctuation of the "scalar connection" in the (ν_R, ν_R) sector — right-handed neutrinos — in the Majorana matrix inside D_F.

In the NCG action the field σ modifies the RGE β-functions for the Higgs self-coupling constant λ, canceling the IR instability of λ in the window Λ_{SM} ≲ μ ≲ Λ_{unification}
and restoring agreement with m_H ≈ 125 GeV.

Key structural role of σ: it arises from the **non-commutative** sector, which is absent in the purely commutative limit. Its appearance is due to the fact that the algebra A_F = ℂ ⊕ ℍ ⊕ M₃(ℂ) has a nonzero "inter-factor" component of the operator D_F.

### B.2 Is There a σ Analogue in the 600-Cell?

**Analysis of H4 spectral structure:**

The Dirac operator of the 600-cell acts on a 480-dimensional space (120 vertices × 4 spin components). Its eigenvalues are grouped by H4 symmetries.
In `SpectralAction600Cell.v` and `SpectralExtras.v` the following are formalized:
- N_vertices = 120 = 4h
- Spectral coefficient a4 = 1/(16φ) + φ³/8
- Vertex dominance: a4_vert > a4_curv

For a σ-analogue a **scalar singlet** in the decomposition of the 600-cell Dirac operator is needed.
Consider each criterion:

**Criterion 1. "Inter-factor" origin**

In standard NCG σ arises from the connection between the ℂ and M₃(ℂ) components in A_F.
In Trinity S3AI the only algebra is the spectral data of the 600-cell; there are no
two "factors" (ℂ and M₃(ℂ)) between which a σ-like field could arise. The H4 Dirac operator has a *single* spectral source — the geometry of the root system — without an internal "two-factor" A_F structure.

**Criterion 2. Right-handed neutrinos and Majorana scale**

In NCG σ ∼ M_R scales the Majorana mass matrix for right-handed neutrinos.
In Trinity S3AI NeutrinoOrigins.v contains an Axiom for the Majorana scale
(explicitly Admitted). H4 does not generate right-handed neutrinos from first principles:
their inclusion requires extending the fermion multiplet beyond the "automatically" arising H4 representations.

**Criterion 3. Scalar singlet in the 600-cell spectrum**

The eigenvalues of the Dirac operator of the 600-cell (H4 spectrum) are known
from Coxeter group theory: they have the form ±(e_i + e_j), where e_i are the exponents. For H4: e = {1, 11, 19, 29}. The scalar invariant (l = 0)
in the 4D spherical harmonic expansion is the unique **radial** eigenvalue. The space of H4-invariant scalar functions is generated by polynomials in the four fundamental invariants of degrees {2, 12, 20, 30}.

Candidate for σ-analogue: **invariant of degree 2** (d₁ = 2) — this is the squared radius in 4D, which plays the role of a "singlet" under all H4 reflections. This invariant exists and is uniquely defined.

**Scale:**

```
m_σ_analog ≈ ℏ · (d₁ / d₄) · Λ_H4 = (2/30) · 1.5×10¹⁶ GeV ≈ 10¹⁵ GeV
```

This is the Grand Unification scale — the same order as m_σ in standard NCG (Majorana scale ~ 10¹⁴–10¹⁵ GeV). There is a numerical coincidence.

**However:** this "invariant of degree 2" is simply the squared radius, i.e. a constant on each H4 orbit. This is not a *dynamical* field that could modify RGE β-functions. In standard NCG σ is a **dynamical scalar field** with its own kinetic and potential terms in the action.

### B.3 Boyle–Farnsworth Algebra and σ

In the work of Boyle–Farnsworth (2018) the field σ with charge B−L = 2 appears from a non-associative superalgebra extension B = A ⊕ H. For H4 no known analogue of such an extension exists in the refereed literature.

### B.4 Consequence for m_H Prediction

In Trinity S3AI the m_H error is ≈ 6% (H01 predicts ≈ 125.20 GeV versus observed ≈ 125.09 GeV according to PDG 2024, error ~0.09% in absolute units,
but ~6% in relative terms if considering the previous version of the formula).

In NCG σ fixes m_H by changing the **β-function of λ** at unification. For this one needs:
1. λ(Λ) given from the spectral model
2. σ contributes to β_λ via a Yukawa-like coupling y_σ ~ O(1)
3. Resulting m_H = 125 GeV at μ = m_Z

Without a dynamical σ-analogue in the H4/600-cell this mechanism **is not reproducible**.
H01 = 4φ³e² is a direct formula without RGE corrections. Accuracy of 0.09% means that formula H01 already agrees well with data; the "6% error" referred to a previous version. Nevertheless, without σ-like dynamics there is no mechanism that could "fix" this value from first principles.

### B.5 Honest Verdict on B

| Criterion | Status in H4 | Comment |
|-----------|-------------|---------|
| Neutral singlet in spectrum | Partially — d₁=2 invariant | Not a dynamical field |
| Inter-factor origin | **NO** | H4 has no "ℂ + M₃(ℂ)" structure |
| Right-handed neutrinos | **NOT DERIVED** | Admitted in NeutrinoOrigins.v |
| Scale ~ 10¹⁵ GeV | Numerical coincidence | d₁/d₄ · Λ_H4 ~ correct order |
| β_λ modification | **ABSENT** | No dynamical action for σ |
| m_H fixation by RGE methods | **UNREACHABLE** without σ | Honest limitation |

**Verdict B:**  
The H4/600-cell structure **does not generate** a natural analogue of the σ-field in the Chamseddine–Connes sense. The invariant of degree d₁ = 2 is a geometric singlet, but not a dynamical scalar field with an action. Therefore,
the 6% error in the m_H prediction (in case it is present in the specific version of H01) **cannot be corrected by methods analogous to Connes's σ** within the current Trinity S3AI construction. This is an honest negative result.

---

## Summary Table

| Subtask | Result | Honest Status |
|-----------|-----------|---------------|
| A: Unimodularity of H4-generators | Satisfied by inheritance from A4 ⊂ H4 (su(5) is traceless) | Positive, but not new relative to SU(5)-GUT |
| B: σ-analogue in 600-cell | **Negative**: no dynamical singlet | Honest no-go for Connes-style σ in H4 |

---

## Conclusions for HiggsOrigins

1. **H01** (m_H = 4φ³e² ≈ 125.20 GeV) achieves class V accuracy without any RGE corrections. If with updated PDG data the error is ~0.09%, it does not require σ-correction.

2. If the result is interpreted as "needs ~6% improvement", then the **NCG σ-field method is inapplicable** to H4, since H4 does not have the two-factor algebraic structure from which σ arises in NCG.

3. Alternative path to H01 improvement: searching for the **next order** in the spectral expansion of the 600-cell (a₂ or a₆ contributions), which is a separate technical task.

4. The **unimodularity** condition in the H4 approach works well: the path H4 → A4 → SU(5) → SM automatically gives traceless generators. This supports the self-consistency of the Trinity S3AI gauge sector.

---

## Sources

| # | Author | Title | Year | Link |
|---|--------|-------|-----|--------|
| 1 | Chamseddine, Connes | Resilience of the Spectral Standard Model | 2012 | [arXiv:1208.1030](https://arxiv.org/abs/1208.1030) |
| 2 | Chamseddine, Connes | Why the Standard Model | 2007 | [arXiv:0706.3688](https://arxiv.org/abs/0706.3688) |
| 3 | Boyle, Farnsworth | New algebraic structure in SM | 2018 | [arXiv:1604.00847](https://arxiv.org/abs/1604.00847) |
| 4 | Bochniak, Sitarz | Spectral action + θ-terms | 2022 | [arXiv:2106.10890](https://arxiv.org/abs/2106.10890) |
| 5 | Lizzi, Huggett, Menon | Missing the point in NCG | 2021 | [doi:10.1007/s11229-020-02998-1](https://pmc.ncbi.nlm.nih.gov/articles/PMC8604559/) |

---

*Compiled within Trinity S3AI Framework, Wave 5.3.*  
*Project policy: "no fictitious results". Negative results are published explicitly.*
