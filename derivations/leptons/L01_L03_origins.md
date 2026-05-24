# Origin of Lepton Mass Ratios L01–L03 from H4 / E8

**Project:** Trinity S3AI v3.5  
**Date:** 2026-05-22  
**Status:** Honest assessment: numerical coincidences confirmed; group-theoretic origin partially justified, partially post-hoc matching.

---

## 1. Problem Statement

The three "leptonic" formulas (L01–L03) within Trinity give the mass ratios of charged leptons:

| Formula | Expression | Physical meaning | Class | Error |
|---------|-----------|------------------|-------|-------|
| **L01** | \(239 \cdot e / \pi\) | \(m_\mu / m_e\) (pole) | V | 0.0135% |
| **L02** | \(239 \cdot \varphi^4 / \pi^4\) | \(m_\tau / m_\mu\) (pole) | SG | 0.0025% |
| **L03** | \(549 \cdot e \cdot \pi^2 / \varphi^3\) | \(m_\tau / m_e\) (pole) | SG | 0.0069% |

Here \(\varphi = (1 + \sqrt{5})/2\) is the golden ratio, \(e = 2.71828…\) is Euler's number, \(\pi = 3.14159…\).

PDG 2024 targets:

- \(m_\mu / m_e = 206.7682830\)
- \(m_\tau / m_\mu = 16.8166\)
- \(m_\tau / m_e = 3477.23\)

Computed values:

- \(L01 = 239e/\pi \approx 206.796\) (error 0.0135%)
- \(L02 = 239\varphi^4/\pi^4 \approx 16.817\) (error 0.0025%)
- \(L03 = 549 e \pi^2 / \varphi^3 \approx 3476.99\) (error 0.0069%)

---

## 2. Structure of the H4 and E8 Groups

### 2.1 H4 Parameters

The Coxeter group H4 is the largest exceptional finite reflection group in ℝ⁴, the symmetry group of the 600-cell and 120-cell.

| Parameter | Value |
|-----------|-------|
| Order \(\lvert H4 \rvert\) | 14400 = 2⁶·3²·5² |
| Rank | 4 |
| Exponents \(e_i\) | 1, 11, 19, 29 |
| Degrees \(d_i\) | 2, 12, 20, 30 |
| Coxeter number \(h\) | 30 = 2·3·5 |

The H4 root system contains **120 roots**, constructed from \(\varphi\):
\[
(\pm 2, 0, 0, 0),\quad (\pm 1, \pm 1, \pm 1, \pm 1),\quad (\pm\varphi, \pm 1, \pm 1/\varphi, 0) + \text{even permutations}.
\]
H4 is the **only** finite reflection group whose root system explicitly contains \(\varphi\).

### 2.2 E8 and Projection onto H4

The E8 root system contains **240 roots**. E8 projects onto H4 as follows: an affine subsystem of E8 → H4 × H4 (decomposition of the "double" 600-cell), whereby E8 splits into two "shells" of 120 roots each.

Key fact: the connection between E8 and H4 is realized via a projection using \(\varphi\)-rational coefficients. The smallest H4 exponent \(e_1 = 1\) creates a "projection defect" of 1, i.e.:

\[
\boxed{239 = 240 - 1 = |E8\text{ roots}| - e_1}
\]

---

## 3. Origin of the Integer Coefficients

### 3.1 The Number 239 (L01 and L02)

The file `H4Derivations.v` contains the theorem `L01_E8_projection_defect`, establishing that 239 arises as the **E8 projection defect**:

> *L01 = 239: |E8| − e₁ (projection defect)*
> Derivation: The E8 root system minus first exceptional coordinate

Geometrically: projecting 240 E8 roots onto the 4-dimensional H4 space, the first exponent \(e_1 = 1\) is "removed" (corresponding to the direction perpendicular to the projection plane). 239 effective roots remain.

**HONEST assessment:** This is a post-hoc interpretation. The theorem `L01_E8_projection_defect` in `H4Derivations.v` only proves the inequality \(|248 - 239\varphi| < 139\) — a relation with the dimension \(\mathfrak{e}_8 = 248\). The identity \(239 = |E8| - e_1\) is an arithmetic fact, not a consequence of any physical mechanism.

### 3.2 The Number 549 (L03)

From the comment in `Catalog42.v`:

\[
549 = e_3 \cdot e_4 - d_1 = 19 \cdot 29 - 2 = 551 - 2
\]

Here:
- \(e_3 = 19\) — the third H4 exponent,
- \(e_4 = 29 = h - 1\) — the largest H4 exponent (always equal to the Coxeter number minus 1),
- \(d_1 = 2\) — the smallest H4 degree (corresponds to U(1) charge quantization).

Alternatively:
\[
549 = 18h + 9 = 18 \cdot 30 + 9 \quad (\text{Coxeter number})
\]
or \(549 = 600 - 51\) (number of vertices of the 600-cell minus 51 — without direct group-theoretic interpretation).

**HONEST assessment:** The decomposition \(e_3 \cdot e_4 - d_1\) is arithmetically exact, but the connection of this product of exponents to lepton masses is not derived from any first-principles mechanism. It is a coefficient consistency, not a proof.

---

## 4. Origin of the Transcendental Structure

### 4.1 Weight Analysis

Write the formulas in the form \(\text{const} \cdot e^a \cdot \pi^b \cdot \varphi^c\):

| Formula | \(a\) (power of \(e\)) | \(b\) (power of \(\pi\)) | \(c\) (power of \(\varphi\)) |
|---------|--------|---------|---------|
| L01 | 1 | −1 | 0 |
| L02 | 0 | −4 | 4 |
| L03 | 1 | 2 | −3 |

Product L01·L02:

\[
L01 \cdot L02 = 239^2 \cdot e \cdot \varphi^4 / \pi^5, \quad \text{weights: } (a=1, b=-5, c=4)
\]

Ratio \(L01 \cdot L02 / L03\):

\[
\frac{L01 \cdot L02}{L03} = \frac{239^2}{549} \cdot \left(\frac{\varphi}{\pi}\right)^7 \approx 104.046 \cdot 0.00961 \approx 1.0002
\]

This confirms the **chain**:

\[
\boxed{m_\tau / m_e \approx (m_\mu / m_e) \cdot (m_\tau / m_\mu), \quad \text{accuracy } 0.02\%}
\]

which is a trivial consistency requirement. In `Bounds_LeptonMasses.v` this is proven by the theorem `chain_L01_L02_approx_L03`.

### 4.2 Algebraic Properties of Powers of φ

From `CorePhi.v` (proven lemmas):

\[
\varphi^2 = \varphi + 1, \quad \varphi^3 = 2\varphi + 1, \quad \varphi^4 = 3\varphi + 2
\]

Fibonacci coefficients: \(\varphi^n = F(n)\varphi + F(n-1)\).

- **Power 4 in L02:** \(\varphi^4 = 3\varphi + 2\), exponent 4 = rank of H4. This is an exact coincidence: the rank of the group and the power coincide.
- **Power −3 in L03:** \(1/\varphi^3 = 1/(2\varphi+1)\), exponent 3 = number of fermion generations in the SM.

**HONEST assessment:** The connection "rank of H4 = 4 = power in L02" and "3 generations = power in L03" is a correspondence that can be stated, but cannot be derived from first principles.

### 4.3 Physical Meaning of the Pair (e, π)

- The number \(\pi\) enters through the volume/area of spherical harmonics; in the spectral action on a 4-manifold, zeta functions give factors \(\pi^k\).
- The number \(e\) is related to quasiclassical exponents (instanton contributions, heat kernels).

**HONEST assessment:** This is motivation, not derivation. The specific combination \(e/\pi\) in L01 does not follow from any known spectral calculation.

---

## 5. Step-by-Step Derivation

### 5.1 L01: \(m_\mu/m_e = 239 \cdot e/\pi\)

**Step 1 (rigorous):** E8 has 240 roots. The smallest H4 exponent \(e_1 = 1\). Arithmetically: \(240 - 1 = 239\).

**Step 2 (postulate):** The projection E8 → H4 assigns weight 1 to each "normal" root, weight 0 to the defective one. Number of active roots = 239.

**Step 3 (numerical fitting):** The ratio of transcendental constants \(e/\pi\) normalizes 239 to the value \(\approx 206.8\). This coincides with \(m_\mu/m_e\) to 0.014% accuracy.

**Rigorously proven (Coq):** `L01_is_m_mu_over_m_e` in `Catalog42.v` — that \(|239e/\pi - m_\mu/m_e| / (m_\mu/m_e) < 10^{-3}\).

**Not derived:** Why the ratio \(e/\pi\), and not another transcendental combination.

---

### 5.2 L02: \(m_\tau/m_\mu = 239 \cdot \varphi^4/\pi^4\)

**Step 1 (rigorous):** \(\varphi^4 = 3\varphi + 2\) — exact algebraic identity (proven in `CorePhi.v`, lemma `phi_fourth`).

**Step 2 (postulate):** Power 4 = rank of H4. This is a hypothesized connection: the observed "depth" of the lepton hierarchy reflects the dimension of H4.

**Step 3 (numerical fitting):** \(239\varphi^4/\pi^4 \approx 16.817\), experimental value \(16.8166\), error 0.0025%.

**Rigorously proven (Coq):** `L02_is_m_tau_over_m_mu` in `Catalog42.v`.

**Also rigorous:** \(\varphi^4 = 3\varphi + 2\) (Fibonacci algebra, `phi_fourth`).

**Not derived:** Why exactly the 4th power, and not the 2nd or 6th.

---

### 5.3 L03: \(m_\tau/m_e = 549 \cdot e \cdot \pi^2 / \varphi^3\)

**Step 1 (rigorous):** \(549 = e_3 \cdot e_4 - d_1 = 19 \cdot 29 - 2\) — identity from H4 exponents and degrees.

**Step 2 (rigorous):** \(\varphi^3 = 2\varphi + 1\) — exact algebraic identity (proven in `CorePhi.v`, lemma `phi_cubed_alt`).

**Step 3 (postulate):** Power 3 = number of fermion generations (recorded in `Catalog42.v` as `N_generations_exact = 3`).

**Step 4 (numerical fitting):** \(549 e \pi^2 / \varphi^3 \approx 3476.99\), experimental value \(3477.23\), error 0.007%.

**Rigorously proven (Coq):** `L03_is_m_tau_over_m_e` in `Catalog42.v`.

**Not derived:** Why the combination \(e \cdot \pi^2\), and not another.

---

## 6. Relation to Coq Theorems

| Theorem (file) | What is proven | Status |
|----------------|---------------|--------|
| `L01_E8_projection_defect` (H4Derivations.v) | \(\lvert 248 - 239\varphi \rvert < 139\) | Qed |
| `L01_is_m_mu_over_m_e` (Catalog42.v) | Relative error of L01 < 0.1% | Qed |
| `L02_is_m_tau_over_m_mu` (Catalog42.v) | Relative error of L02 < 0.01% | Qed |
| `L03_is_m_tau_over_m_e` (Catalog42.v) | Relative error of L03 < 0.01% | Qed |
| `phi_fourth` (CorePhi.v) | \(\varphi^4 = 3\varphi + 2\) | Qed |
| `phi_cubed_alt` (CorePhi.v) | \(\varphi^3 = 2\varphi + 1\) | Qed |
| `chain_L01_L02_approx_L03` (Bounds_LeptonMasses.v) | \(L01 \cdot L02 \approx L03\) (accuracy 1%) | Qed |

New theorems are placed in the file `LeptonOrigins.v`.

---

## 7. Honest Final Assessment

### What is rigorously proven:

1. **Arithmetic:** \(239 = 240 - 1\), \(549 = 19 \cdot 29 - 2\) — these are arithmetic identities with H4 parameters.
2. **Algebra of φ:** \(\varphi^4 = 3\varphi+2\), \(\varphi^3 = 2\varphi+1\) — exact algebraic lemmas.
3. **Numerical coincidences:** All three formulas reproduce PDG values with accuracy < 0.014% (Coq `interval`).
4. **Chain consistency:** \(L01 \cdot L02 / L03 \approx 1.0002\) (deviation 0.02%).

### What is numerical fitting (not derived):

1. **Transcendental pair** \((e, \pi)\): no derivation from first principles for why exactly these combinations.
2. **Powers of transcendental numbers** (4 in L02, −3 in L03, −1 in L01): coincidence with H4 rank and number of generations — an observation, not a proof.
3. **Connection of coefficients 239, 549 to lepton masses:** the integers have an H4 interpretation, but the mechanism linking them to physical masses is unknown.

### What remains open:

- Why the Koide formula (Koide) \(Q = 2/3\) does not follow from H4 (documented in `Koide.v`).
- What mass generation mechanism (Higgs, Yukawa, or something else) realizes these formulas within H4 compactification.

---

## 8. File References

- `proofs/trinity/CorePhi.v` — φ algebra, lemmas `phi_sq`, `phi_cubed_alt`, `phi_fourth`
- `proofs/trinity/H4Derivations.v` — theorem `L01_E8_projection_defect`
- `proofs/trinity/Catalog42.v` — formulas L01_V, L02_SG, L03_SG and the theorems proving them
- `proofs/trinity/Bounds_LeptonMasses.v` — numerical bounds and theorem `chain_L01_L02_approx_L03`
- `proofs/trinity/H4GaugeEmbedding.v` — H4 structure: exponents, degrees, Coxeter number
- `derivations/leptons/LeptonOrigins.v` — new theorems on structural identities

---

*Compiled by: Trinity S3AI subagent, 2026-05-22*
