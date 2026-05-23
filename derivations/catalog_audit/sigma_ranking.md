# Wave 20 — σ-Distance Ranking (26 Formulas, Post-δ_CP Withdrawal)

**Methodology:** σ = |predicted − measured| / σ_measured using **real** PDG 2024 + NuFit 6.0 experimental uncertainties. δ_CP (N04) withdrawn at >5σ; replaced by sin²θ_13, sin²θ_23, sin²θ_W, |V_ub|, λ_Higgs.

| Rank | ID | Formula | Target | Computed | Rel.Error | σ-distance | log₁₀σ | Grade |
|------|-----|---------|--------|----------|-----------|------------|--------|-------|
| 1 | v21 | `(PHI*E/PI)**6 * 1e-5` | 7.53e-05 | 7.53e-05 | 0.000% | 0.00σ | — | SG |
| 2 | v31 | `15*PHI**(-5)*PI**(-2)*E**(-4)` | 0.00251 | 0.00251 | 0.000% | 0.00σ | — | SG |
| 3 | Q07 | `24*PHI**2/PI` | 20 | 20.0003 | 0.002% | 0.00σ | — | SG |
| 4 | N21 | `PI/(40*PHI**2)` | 0.03 | 0.03 | 0.002% | 0.00σ | — | SG |
| 5 | Sin13 | `PI**2/(25*PHI**6)` | 0.0220 | 0.02200 | 0.003% | 0.00σ | — | SG |
| 6 | Snu | `8*PHI**(-6)*PI**(-5)*E**6*0.1` | 0.0588 | 0.05877 | 0.045% | 0.00σ | — | SG |
| 7 | C02 | `1/(3*PHI**2*PI)` | 0.04053 | 0.04053 | 0.005% | 0.00σ | — | SG |
| 8 | Lambda | `sqrt(PHI)/(PI**2)` | 0.129 | 0.1289 | 0.091% | 0.01σ | −2.00 | SG |
| 9 | Q05 | `43 + PI/PHI` | 44.94 | 44.94 | 0.004% | 0.02σ | −1.70 | SG |
| 10 | Q01 | `2*PHI/7` | 0.462 | 0.4623 | 0.064% | 0.02σ | −1.70 | SG |
| 11 | N01 | `8*PI/(PHI**5*E**2)` | 0.307 | 0.3067 | 0.098% | 0.02σ | −1.70 | SG |
| 12 | Q02 | `12 + PHI**3*E**2` | 43.24 | 43.30 | 0.140% | 0.04σ | −1.40 | SG |
| 13 | H02 | `11*PHI/20 + 2/3` | 1.558 | 1.557 | 0.066% | 0.06σ | −1.22 | SG |
| 14 | N03 | `PI**2/18` | 0.546 | 0.5483 | 0.423% | 0.11σ | −0.96 | V |
| 15 | Q03 | `19*PI*E**2/PHI` | 272 | 272.6 | 0.216% | 0.12σ | −0.92 | V |
| 16 | Q04 | `24*PI**3/E**4` | 13.63 | 13.63 | 0.025% | 0.17σ | −0.77 | V |
| 17 | L02 | `239*PHI**4/PI**4` | 16.82 | 16.82 | 0.002% | 0.29σ | −0.54 | V |
| 18 | H01 | `4*PHI**3*E**2` | 125.1 | 125.2 | 0.074% | 0.84σ | −0.08 | V |
| 19 | H03 | `4*PHI*PI/15 + 4/225` | 1.372 | 1.373 | 0.094% | 1.07σ | 0.03 | Pass |
| 20 | C03 | `1/(39*PHI**2*E)` | 0.00382 | 0.00360 | 5.680% | 1.09σ | 0.04 | Pass |
| 21 | L03 | `549*E*PI**2/PHI**3` | 3477 | 3477 | 0.009% | 1.54σ | 0.19 | Pass |
| 22 | C01 | `2*PHI**3*E**2/(9*PI**3)` | 0.2265 | 0.2243 | 0.958% | 4.34σ | 0.64 | Marginal |
| 23 | G03 | `3/(8*PHI)` | 0.2234 | 0.2318 | 3.762% | 84.03σ | 1.92 | **Fail** |
| 24 | L01 | `239*E/PI` | 206.8 | 206.8 | 0.014% | 6064σ | 3.78 | **Fail** |
| 25 | Pr | `6*PI**5` | 1836 | 1836 | 0.002% | 3.1×10⁵σ | 5.50 | **Fail** |
| 26 | G01 | `36*PHI*E**2/PI` | 137.0 | 137.0 | 0.024% | 1.6×10⁶σ | 6.20 | **Fail** |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Median σ-distance | **0.085σ** |
| Mean σ-distance | 7.3×10⁴σ (dominated by 4 outliers) |
| Trimmed mean (top 4 excluded) | **0.38σ** |
| Formulas with σ < 0.1 | 13/26 (50%) |
| Formulas with σ < 1.0 | 18/26 (69%) |
| Formulas with σ < 3.0 | 21/26 (81%) |
| Formulas with σ > 5.0 | 5/26 (19%) |

---

## Key Insight: The "Ultra-Precision Trap"

Four formulas fail catastrophically on σ-distance **not** because their relative errors are large, but because the experimental measurements are extraordinarily precise (or, for G03, because the formula itself is off by 3.8%):

| Formula | Observable | Exp. Rel. Uncertainty | Trinity Rel. Error | σ-distance | Reason |
|---------|-----------|----------------------|-------------------|------------|--------|
| G01 | 1/α(0) | **1.5 × 10⁻¹⁰** | 0.024% | 1.6×10⁶σ | Ultra-precise measurement |
| Pr | mₚ/mₑ | **6.0 × 10⁻¹¹** | 0.002% | 3.1×10⁵σ | Ultra-precise measurement |
| L01 | m_μ/mₑ | **2.2 × 10⁻⁹** | 0.014% | 6.1×10³σ | Ultra-precise measurement |
| G03 | sin²θ_W | **4.5 × 10⁻⁴** | 3.762% | 84σ | Formula genuinely off |

**Note:** G03 (sin²θ_W = 3/(8φ) ≈ 0.2318) disagrees with the experimental value 0.22336 by 3.8%, well outside the 0.04% uncertainty. This is a genuine failure, not an ultra-precision artifact.

---

## Revised Grading System (σ-based)

| Grade | σ threshold | Interpretation | Count |
|-------|-------------|----------------|-------|
| SG | σ < 0.1 | Within 10% of experimental uncertainty | 13 |
| V | 0.1 ≤ σ < 1.0 | Within experimental uncertainty | 5 |
| Pass | 1.0 ≤ σ < 3.0 | Within 3σ of measurement | 3 |
| Marginal | 3.0 ≤ σ < 5.0 | Between 3σ and 5σ | 1 |
| Fail | σ ≥ 5.0 | >5σ discrepancy | 4 |

**Note:** The 3 ultra-precision Fails are artifacts of measurement precision, not large relative errors. G03 is a genuine formula failure. If graded by relative error alone, 24/26 formulas Pass (<1%).

---

## Honest Verdict

The Trinity catalog achieves **median σ-distance of 0.085σ**, meaning half the formulas agree with experiment within ~1/12 of the experimental uncertainty. This is genuinely non-trivial. However:
- The framework cannot "derive" the three most precisely measured constants (1/α, mₚ/mₑ, m_μ/mₑ) because its ~0.01% precision is 10⁵–10⁶× coarser than the measurements.
- The sin²θ_W formula (G03) is a genuine failure at 84σ, not rescued by relative-error framing.
- **Monte-Carlo p-value (500k trials):** Mean relative error p = 0.077 (not significant); SG-hit count p < 0.0001 (highly significant). The catalog's *density* of ultra-precise hits is non-random, but the *average* precision is achievable by random search.
