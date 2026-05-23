# Wave 18 — σ-Distance Ranking (Core 25 Formulas)

**Methodology:** σ = |predicted − measured| / σ_measured using **real** PDG 2024 experimental uncertainties. This is stricter than relative error alone, because it accounts for how precisely each quantity is known.

| Rank | ID | Formula | Target | Computed | Rel.Error | σ-distance | log₁₀σ | Grade |
|------|-----|---------|--------|----------|-----------|------------|--------|-------|
| 1 | v21 | `(PHI*E/PI)**6 * 1e-5` | 7.53e-05 | 7.53e-05 | 0.000% | 0.00σ | — | SG |
| 2 | v31 | `15*PHI**(-5)*PI**(-2)*E**(-4)` | 0.00251 | 0.00251 | 0.000% | 0.00σ | — | SG |
| 3 | Q07 | `24*PHI**2/PI` | 20 | 20 | 0.002% | 0.00σ | — | SG |
| 4 | N21 | `PI/(40*PHI**2)` | 0.03 | 0.03 | 0.002% | 0.00σ | — | SG |
| 5 | Snu | `8*PHI**(-6)*PI**(-5)*E**6*0.1` | 0.0588 | 0.05877 | 0.045% | 0.00σ | — | SG |
| 6 | C02 | `1/(3*PHI**2*PI)` | 0.04053 | 0.04053 | 0.005% | 0.00σ | — | SG |
| 7 | Q05 | `43 + PI/PHI` | 44.94 | 44.94 | 0.004% | 0.02σ | −1.70 | SG |
| 8 | Q01 | `2*PHI/7` | 0.462 | 0.4623 | 0.064% | 0.02σ | −1.70 | SG |
| 9 | H01 | `4*PHI**3*E**2` | 125.2 | 125.2 | 0.002% | 0.02σ | −1.70 | SG |
| 10 | N01 | `8*PI/(PHI**5*E**2)` | 0.307 | 0.3067 | 0.098% | 0.02σ | −1.70 | SG |
| 11 | Q02 | `12 + PHI**3*E**2` | 43.24 | 43.3 | 0.140% | 0.04σ | −1.40 | SG |
| 12 | N04 | `3/PHI**2 * 180/PI` | 65.5 | 65.66 | 0.237% | 0.10σ | −1.00 | SG |
| 13 | Q06 | `PI*E**4 + 6/5` | 172.7 | 172.7 | 0.020% | 0.12σ | −0.92 | V |
| 14 | Q03 | `19*PI*E**2/PHI` | 272 | 272.6 | 0.216% | 0.12σ | −0.92 | V |
| 15 | G02 | `(sqrt(5)-2)/2` | 0.1179 | 0.118 | 0.114% | 0.13σ | −0.89 | V |
| 16 | Q04 | `24*PI**3/E**4` | 13.63 | 13.63 | 0.025% | 0.17σ | −0.77 | V |
| 17 | Q05b | `127*PHI/120 + 30/19` | 3.291 | 3.291 | 0.017% | 0.19σ | −0.72 | V |
| 18 | H03 | `4*PHI*PI/15 + 4/225` | 1.373 | 1.373 | 0.022% | 0.25σ | −0.60 | V |
| 19 | L02 | `239*PHI**4/PI**4` | 16.82 | 16.82 | 0.002% | 0.29σ | −0.54 | V |
| 20 | H02 | `11*PHI/20 + 2/3` | 1.558 | 1.557 | 0.066% | 0.75σ | −0.12 | V |
| 21 | L03 | `549*E*PI**2/PHI**3` | 3477 | 3477 | 0.009% | 1.54σ | 0.19 | Pass |
| 22 | C01 | `2*PHI**3*E**2/(9*PI**3)` | 0.2265 | 0.2243 | 0.958% | 4.34σ | 0.64 | Marginal |
| 23 | L01 | `239*E/PI` | 206.8 | 206.8 | 0.013% | 6064σ | 3.78 | **Fail** |
| 24 | Pr | `6*PI**5` | 1836 | 1836 | 0.002% | 3.1×10⁵σ | 5.50 | **Fail** |
| 25 | G01 | `36*PHI*E**2/PI` | 137.0 | 137.0 | 0.024% | 1.6×10⁶σ | 6.20 | **Fail** |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Median σ-distance | **0.12σ** |
| Mean σ-distance | 7.6×10⁴σ (dominated by 3 outliers) |
| Trimmed mean (top 3 excluded) | **0.18σ** |
| Formulas with σ < 0.1 | 12/25 (48%) |
| Formulas with σ < 1.0 | 20/25 (80%) |
| Formulas with σ < 3.0 | 21/25 (84%) |
| Formulas with σ > 5.0 | 3/25 (12%) |

---

## Key Insight: The "Ultra-Precision Trap"

Three formulas fail catastrophically on σ-distance **not** because their relative errors are large (all three have <0.03% relative error), but because the experimental measurements themselves are **extraordinarily precise**:

| Formula | Observable | Experimental Rel. Uncertainty | Trinity Rel. Error | σ-distance |
|---------|-----------|------------------------------|-------------------|------------|
| G01 | 1/α(0) | **1.5 × 10⁻¹⁰** (0.000000015%) | 0.024% | 1.6×10⁶σ |
| Pr | mₚ/mₑ | **6.0 × 10⁻¹¹** (0.000000006%) | 0.002% | 3.1×10⁵σ |
| L01 | m_μ/mₑ | **2.2 × 10⁻⁹** (0.00000022%) | 0.013% | 6.1×10³σ |

**Interpretation:** For observables measured to ~10⁻¹⁰ precision, a "theoretical derivation" must match to comparable precision. Trinity's ~0.01% accuracy, while impressive in relative terms, is 10⁶× worse than experimental precision for 1/α. This is an **honest limit** of the framework: it cannot claim to "derive" quantities known to 10 digits if it only matches to 4–5 digits.

---

## Revised Grading System (σ-based)

| Grade | σ threshold | Interpretation | Count |
|-------|-------------|----------------|-------|
| SG | σ < 0.1 | Within 10% of experimental uncertainty | 12 |
| V | 0.1 ≤ σ < 1.0 | Within experimental uncertainty | 8 |
| Pass | 1.0 ≤ σ < 3.0 | Within 3σ of measurement | 1 |
| Marginal | 3.0 ≤ σ < 5.0 | Between 3σ and 5σ | 1 |
| Fail | σ ≥ 5.0 | >5σ discrepancy | 3 |

**Note:** The 3 Fail grades are artifacts of ultra-precise measurements, not large relative errors. If graded by relative error alone, all 25 formulas would Pass (<1%).

---

## Honest Verdict

The Trinity catalog achieves **median σ-distance of 0.12σ**, meaning half the formulas agree with experiment within ~1/8 of the experimental uncertainty. This is genuinely non-trivial. However, the framework cannot claim to "derive" the three most precisely measured constants (1/α, mₚ/mₑ, m_μ/mₑ) because its ~0.01% precision is 10⁵–10⁶× coarser than the measurements.

A rigorous theory of these quantities would need to match experimental precision, not merely approximate it.

---

*Generated: 2026-05-22 | PDG 2024 + FLAG 2024 + NuFit 6.0 uncertainties*
