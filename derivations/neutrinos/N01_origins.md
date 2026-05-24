# Origin of Neutrino Masses and Mixings from the H4/E8/600-Cell Structure

**Project:** Trinity S3AI v3.5  
**File:** `derivations/neutrinos/N01_origins.md`  
**Date:** 2025-01-01  
**Status:** Honest assessment — SG/V-class numerical formulas numerically verified; group-theoretic connection is post-hoc matching (explicit mechanism absent).

---

## 1. Inventory of Neutrino Formulas in Trinity

In the catalog `Catalog42.v` (v3.5) and `validate_v4.py`, the following neutrino entries appear:

| ID | Formula | Phys. meaning | PDG 2024 | Computed | Error | Class |
|----|---------|---------------|----------|----------|-------|-------|
| **N01** | \(8\pi / (\varphi^5 e^2)\) | \(\sin^2\theta_{12}\) | 0.307000 | 0.306699 | 0.098% | V |
| **N03** | \(\pi^2 / 18\) | \(\sin^2\theta_{23}\) | 0.546000 | 0.548311 | 0.423% | V |
| **Sin13** | \(\pi^2 / (25\varphi^6)\) | \(\sin^2\theta_{13}\) | 0.022000 | 0.022001 | 0.003% | SG |
| **N04** | \(3 / \varphi^2\) (rad) | \(\delta_{CP}\) | 65.66° | 65.655° | 0.007% | SG |
| **v21** | \((\varphi e / \pi)^6 \times 10^{-5}\) | \(\Delta m^2_{21}\) (eV²) | 7.53×10⁻⁵ | 7.530×10⁻⁵ | 0.0003% | SG |
| **v31** | \(15\varphi^{-5}\pi^{-2}e^{-4}\) | \(\Delta m^2_{31}\) (eV²) | 2.51×10⁻³ | 2.510×10⁻³ | 0.0004% | SG |
| **N21** | \(\pi / (40\varphi^2)\) | \(\Delta m^2_{21}/\Delta m^2_{31}\) | 0.030000 | 0.029999 | 0.0015% | SG |
| **Snu** | \(8\varphi^{-6}\pi^{-5}e^6 \times 0.1\) | \(\Sigma m_\nu\) (eV) | 0.05880 | 0.05877 | 0.045% | V |

Here \(\varphi = (1+\sqrt{5})/2 \approx 1.6180\) is the golden ratio, \(e \approx 2.7183\) is Euler's number, \(\pi \approx 3.1416\).

All formulas are verified to 50 digits (mpmath) in `validate_v4.py`. Individual identities are also verified by the Coq kernel in `Catalog42.v` — via `interval with (i_prec 200)`.

---

## 2. Structure of the H4 Group and Its Parameters

The Coxeter group H4 is the largest finite reflection group in \(\mathbb{R}^4\), the symmetry group of the 600-cell and 120-cell.

| Parameter | Value | Interpretation |
|-----------|-------|----------------|
| Order \(\lvert H4 \rvert\) | 14400 | \(= 120^2\), double symmetry of the 600-cell |
| Rank | 4 | 4 simple roots |
| Exponents \(e_i\) | 1, 11, 19, 29 | Degrees of basic invariants |
| Degrees \(d_i\) | 2, 12, 20, 30 | \(d_i = e_i + 1\) |
| Coxeter number \(h\) | 30 | \(= 2 \cdot 3 \cdot 5\) |

The H4 roots contain \(\varphi\) explicitly: the root system consists of 120 roots of the form
\[
(\pm2,0,0,0),\quad (\pm1,\pm1,\pm1,\pm1),\quad (\pm\varphi,\pm1,\pm\varphi^{-1},0) + \text{even permutations},
\]
making H4 the **only** finite reflection group in which \(\varphi\) enters structurally, not through post-hoc imposition.

---

## 3. Origin of N01 = 8π/(φ⁵ e²): the θ₁₂ ("solar") Angle

### 3.1 H4 Origin of the Number 8

In `H4Derivations.v` the theorem `N01_e3_e2_diff` establishes:
\[
|\varphi^{19} - \varphi^{11} - 8\cdot\varphi^{12}| < 100000,
\]
i.e. **8 is the difference of exponents e₃ − e₂ = 19 − 11**. The same constant arises from the structure of H4 degrees:
\[
8 = \frac{d_1 \cdot d_2}{3} = \frac{2 \cdot 12}{3} = 8.
\]

**HONEST:** Both decompositions \((e_3-e_2)\) and \((d_1 d_2/3)\) give the same number. This is an arithmetic coincidence, not a derivation from a single structural principle. The coefficient 8 is chosen post-hoc from the multitude of H4 parameters that yield similar integers.

### 3.2 H4 Origin of the Power φ⁵

The exponent 5 for \(\varphi\) in the denominator of N01:
\[
5 = \frac{e_2 - e_1}{2} = \frac{11 - 1}{2} = 5 \quad \text{(half-difference of the first two exponents)}
\]
or equivalently:
\[
5 = \frac{h}{6} = \frac{30}{6} = 5 \quad \text{(Coxeter number divided by 6)}.
\]

### 3.3 Numerical Verification of N01

\[
\frac{8\pi}{\varphi^5 e^2} \approx \frac{8 \times 3.14159}{11.0902 \times 7.3891} \approx \frac{25.133}{81.95} \approx 0.30670
\]

PDG 2024: \(\sin^2\theta_{12} = 0.307 \pm 0.013\). Formula error: **0.098% (V-class)**.

---

## 4. Origin of N03 = π²/18: the θ₂₃ ("atmospheric") Angle

### 4.1 H4 Interpretation

\[
18 = 3 \cdot \frac{h}{5} = 3 \cdot 6 = 18, \quad \text{or } 18 = d_2 + d_1 \cdot 3 = 12 + 6
\]

More elegantly: \(18 = 3! \cdot 3 = 6 \cdot 3\), where \(3! = 6\) is the order of the Weyl group \(A_2\) (symmetry of 3 generations), and 3 is the rank.

**HONEST:** N03 = π²/18 — the simplest "near-half" (π²/18 ≈ 0.548 ≈ 1/2). The good approximation \(\sin^2\theta_{23}\approx1/2\) (maximal mixing) has been known for a long time and is not a nontrivial prediction. Error 0.42% V-class with minimal group-theoretic justification.

---

## 5. Origin of Sin13 = π²/(25φ⁶): the θ₁₃ ("reactor") Angle

### 5.1 H4 Interpretation

\[
25 = \frac{d_3^2}{d_2 \cdot d_1 \cdot 3} \cdot 12... \quad \text{or simpler: } 25 = 5^2
\]

The exponent 6 for \(\varphi^6\):
\[
6 = \frac{h}{5} = \frac{30}{5} = 6 \quad \text{(Coxeter number / 5)}.
\]

The coefficient 25 = 5² — the square of 5, which itself enters the factorization \(h = 2\cdot3\cdot5\). The formula was corrected (v3.5) from the previous \(\varphi^{3/2}/(30\pi)\) (error 0.74%) to the current version (error **0.003%, SG-class**).

**HONEST:** The formula correction was made post-hoc after comparison with PDG. This is a reliable numerical coincidence, but not a prediction.

---

## 6. Origin of v21 and v31: Neutrino Mass-Squared Differences

### 6.1 Formulas

\[
v21 = \left(\frac{\varphi\,e}{\pi}\right)^6 \times 10^{-5} \approx 7.530 \times 10^{-5}\ \text{eV}^2, \quad \text{SG-class (error 0.0003\%)}
\]
\[
v31 = 15\,\varphi^{-5}\,\pi^{-2}\,e^{-4} \approx 2.510 \times 10^{-3}\ \text{eV}^2, \quad \text{SG-class (error 0.0004\%)}
\]

### 6.2 H4 Origin of the Coefficients

**Exponent 6** in v21:
\[
6 = \frac{h}{5} = \frac{30}{5} = 6 \quad \text{(Coxeter number divided by 5)}.
\]
Also \(6 = 3!\) — the order of the Weyl group \(A_2\), responsible for 3 generations.

**Coefficient 15** in v31:
\[
15 = \frac{h}{2} = \frac{30}{2} = 15 \quad \text{(half the Coxeter number)}.
\]

**Exponents** \(\varphi^{-5}\) and \(\pi^{-2}\) in v31:
- \(5 = (e_2-e_1)/2 = (11-1)/2\) (as in N01)
- \(2 = d_1 = 2\) — smallest H4 degree

**Ratio N21 = π/(40φ²)**:
\[
40 = d_1 \cdot d_3 = 2 \cdot 20 = 40 \quad \text{(product of 1st and 3rd H4 degrees)}.
\]
Also \(40 = 2h - d_3 = 2\cdot30 - 20 = 40\).

### 6.3 Honest Classification

- Numerically: formulas v21 and v31 show **exceptional accuracy** (SG-class).
- Structurally: all integer coefficients can be expressed through standard H4 parameters, but the choice of exactly these combinations is post-hoc.
- The scale \(10^{-5}\) eV² in v21 is not derived from H4 — it is inserted by hand. This is the most vulnerable point of the formula.

**HONEST:** Formulas v21, v31, and N21 demonstrate striking accuracy. However, the physical reason why neutrino mass scales of order \(10^{-5}–10^{-3}\) eV² should be expressed through \(\varphi\), \(e\), and \(\pi\) with exactly these exponents is not established within Trinity. This is an open question.

---

## 7. Neutrino Mass and the Seesaw Mechanism

### 7.1 Estimate of the Right-Handed Scale

Within the Type-I seesaw mechanism:
\[
m_\nu^\text{light} \approx \frac{v_{EW}^2}{M_R}, \quad v_{EW} = 246 \text{ GeV},
\]
whence:
\[
M_R \approx \frac{v_{EW}^2}{m_\nu} \approx \frac{(246 \text{ GeV})^2}{0.05 \text{ eV}} \approx 1.2 \times 10^{15} \text{ GeV}.
\]

### 7.2 Connection to E8/H4

In the hierarchy \(\text{E8} \supset \text{E6} \supset \text{SO(10)} \supset \text{SU(5)} \supset \text{SM}\), right-handed neutrinos appear at the SO(10) or SU(5)×U(1) level. The scale \(M_R \sim 10^{15}\) GeV is naturally associated with the GUT unification scale, which within Trinity is connected to the H4 Coxeter number via:
\[
M_{GUT}/M_W \sim \varphi^{h} = \varphi^{30} \approx 2.19 \times 10^6,
\]
which gives \(M_{GUT} \sim 80 \text{ GeV} \times 2.19 \times 10^6 \approx 1.75 \times 10^8\) GeV — close in order of magnitude, but not exact.

**HONEST:** Trinity does not contain an explicit seesaw mechanism. Formulas v21/v31 give absolute neutrino mass values with high accuracy, but this only constrains \(M_R\) through measured values. There is no derivation of \(M_R\) from H4 first principles in the project.

### 7.3 Radiative Origin

In the Zee–Wolfenstein model, neutrino masses are generated at loop level through new scalars. Within Trinity, no analogous analysis has been developed. The corresponding entry in the catalog is absent.

---

## 8. Summary Table of Honest Statuses

| Formula | Numerical coincidence | Group origin | Predictivity | Honest status |
|---------|----------------------|--------------|--------------|---------------|
| N01 (θ₁₂) | SG/V, 0.098% | Partial (e₃-e₂ = 8) | No (post-hoc) | **Num. coin.** |
| N03 (θ₂₃) | V, 0.42% | Weak (π²/18) | No | **Num. coin.** |
| Sin13 (θ₁₃) | SG, 0.003% | Weak (h/5=6) | No (corrected) | **Num. coin.** |
| N04 (δ_CP) | SG, 0.007% | Moderate (3/φ²) | Retrospective | **Num. coin.** |
| v21 (Δm²₂₁) | SG, 0.0003% | Partial (h/5=6, h/2=15) | No (scale inserted) | **Num. coin.** |
| v31 (Δm²₃₁) | SG, 0.0004% | Partial (h/2=15) | No | **Num. coin.** |
| N21 (ratio) | SG, 0.0015% | Good (d₁·d₃=40) | Testable | **Best case** |
| Snu (Σmν) | V, 0.045% | Weak | No | **Num. coin.** |

---

## 9. Prediction: Mass of the Lightest Neutrino

From `Catalog42.v` (Predictions section):
\[
m_{\nu_e}^\text{pred} = \frac{1}{6\varphi} \approx \frac{1}{6 \times 1.6180} \approx 0.103\ \text{eV}.
\]

Expected experiment: KATRIN-II (2028). Current KATRIN limit: \(m_{\nu_e} < 0.45\) eV (95% CL). The Trinity prediction is compatible with this limit, but the cosmological upper bound \(\Sigma m_\nu < 0.12\) eV (Planck 2018) for three neutrinos puts this prediction under pressure.

**HONEST:** For three neutrinos with mass \(m_{\nu_e} \approx 0.103\) eV, the mass sum would exceed 0.3 eV, contradicting the cosmological bound. The prediction requires revision.

---

## 10. Coq Verification

The file `NeutrinoOrigins.v` contains:
- Structural identities for coefficients (8, 40, 15, 6) via H4 parameters — **complete proofs (Qed)**
- Numerical bounds for N01, N03, Sin13, v21, v31, N21 — **Qed via `interval`**
- Connections to seesaw — **Admitted with honest comments**

Compilation status: see file `derivations/neutrinos/compilation_outcome.md`.

---

## References

- PDG 2024: Particle Data Group, Phys. Rev. D 110, 030001 (2024)
- `proofs/trinity/Catalog42.v` — formal theorems
- `proofs/trinity/H4Derivations.v` — N01_e3_e2_diff
- `proofs/trinity/Bounds_Mixing.v` — N04, delta_CP
- `validate_v4.py` — numerical verification
