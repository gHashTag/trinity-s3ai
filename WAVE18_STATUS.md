# LEGACY DOCUMENT (historical Wave 18 status report)
# Current status: This report reflects Wave 18 status (2026-05-22). See
# honest_pvalue_report_v20.md and COQ_HONEST_STATUS.md for current canonical metrics.

# Wave 18 Status — Honest Phenomenology & Statistical Assessment

**Date:** 2026-05-22  
**Branch:** `main`  
**Scope:** Statistical validation of the Trinity formula catalog against random coincidence

---

## Executive Summary

Wave 18 executed a **pre-registered Monte-Carlo protocol** to test whether the Trinity formula catalog (25 core formulas) is statistically distinguishable from random search in a large transcendental search space.

**Verdict: YES — the catalog is statistically significant.**

| Metric | Trinity | Random (median) | p-value | Significance |
|--------|---------|-----------------|---------|--------------|
| Mean relative error | 0.0835% | 0.594% | **p < 0.0001** | Highly significant |
| Hits < 0.1% error | 20/25 | 5/25 | **p < 0.0001** | Highly significant |
| Hits < 1.0% error | 25/25 | 21/25 | **p = 0.0061** | Significant |
| Mean σ-distance | 7.6×10⁴σ | 4.1×10⁶σ | **p = 0.0004** | Significant |

**But with caveats:** Only 10/25 formulas are individually significant (p < 0.05). The remaining 15 are consistent with random search when tested in isolation. The catalog's strength is **collective** — the joint distribution of errors is better than random.

---

## Key Artifacts

| File | Description |
|------|-------------|
| `scripts/honest_phenomenology_v18.py` | Monte-Carlo engine (vectorized, numpy) |
| `derivations/catalog_audit/wave18_mc_results.json` | Raw MC results (50K trials, 2K samples) |
| `derivations/catalog_audit/honest_pvalue_report_v18.md` | Full statistical report with interpretation |
| `derivations/catalog_audit/sigma_ranking.md` | σ-distance ranking for all 25 core formulas |

---

## σ-Distance Insight: The Ultra-Precision Trap

Using **real PDG 2024 uncertainties** (not placeholder 0.5%), three formulas "fail" catastrophically:

| Formula | Observable | Exp. Uncertainty | Trinity Error | σ-distance |
|---------|-----------|-----------------|---------------|------------|
| G01 | 1/α(0) | 1.5×10⁻¹⁰ (rel.) | 0.024% | **1.6×10⁶σ** |
| Pr | mₚ/mₑ | 6.0×10⁻¹¹ (rel.) | 0.002% | **3.1×10⁵σ** |
| L01 | m_μ/mₑ | 2.2×10⁻⁹ (rel.) | 0.013% | **6.1×10³σ** |

**Why:** These are the most precisely measured constants in physics. Trinity's ~0.01% accuracy, while impressive in relative terms, is 10⁵–10⁶× coarser than experimental precision. A rigorous first-principles derivation would need to match experimental precision.

**Median σ-distance (all 25): 0.12σ** — half the formulas agree within 1/8 of experimental uncertainty.

---

## Per-Formula Significance (p < 0.05 = significant)

**Significant (10 formulas):** L02, L03, Q05, Q07, C02, H01, v21, v31, N21, Pr  
**Suggestive (4 formulas):** L01, Q06, Snu, G01  
**Not significant (11 formulas):** Q01, Q02, Q03, Q04, Q05b, G02, N01, N04, C01, H02, H03

The 11 non-significant formulas are consistent with random search — their precision could be achieved by chance in a search space of ~10⁸ formulas.

---

## Honest Limitations

1. **Search space uncertainty**: The true space searched during Trinity development may differ from the pre-registered ~10⁸ space.
2. **Template limitations**: Only 5 templates were tested; original search may have used additional forms.
3. **No Bonferroni correction**: Aggregate p-values are uncorrected for multiple testing.
4. **Sample size**: 2,000 formulas per trial × 50,000 trials = 100M formulas tested. The full space is ~10⁸, so the sampling coverage is limited.

---

## What This Means

The Trinity catalog is **not random noise**. The collective precision of the 25 formulas is statistically significant (p < 0.0001). However:

- It is **not a first-principles derivation** — 11/25 formulas are individually consistent with random search.
- It cannot claim to **derive** ultra-precise constants (1/α, mₚ/mₑ, m_μ/mₑ) because its ~0.01% precision is 10⁵× coarser than measurement.
- The honest framing is: **a statistically non-trivial phenomenological fit with group-theoretic structure**, not a fundamental theory.

---

## Metrics

| Metric | Wave 17 | Wave 18 |
|--------|---------|---------|
| Qed | 1772 | 1772 |
| Admitted | 0 | 0 |
| Formulas (core) | 25 | 25 |
| SG-class (rel.error) | 12 | 12 |
| σ < 1.0 | — | 20/25 |
| MC p-value (mean error) | — | **< 0.0001** |
| MC p-value (hits <0.1%) | — | **< 0.0001** |

---

*Wave 18 complete: 2026-05-22*
