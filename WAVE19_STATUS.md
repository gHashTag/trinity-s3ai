# Wave 19 Status — Data Paper

**Date:** 2026-05-22  
**Branch:** `main`  
**Scope:** Draft data paper "H₄ Numerological Atlas" for PLOS ONE submission

---

## Executive Summary

Wave 19 drafted a **data paper** documenting the Trinity formula catalog as a reproducible dataset, with zero theoretical claims. The paper makes the honest case: the catalog is a statistically non-trivial collection of numerical correlations, not a fundamental theory.

**Target journal:** PLOS ONE (hep-th or Interdisciplinary Physics)  
**Alternative:** Data in Brief (Elsevier) or Scientific Data (Nature)

---

## Key Artifacts

| File | Description | Pages |
|------|-------------|-------|
| `paper/wave19_data_paper.tex` | Main manuscript (LaTeX) | 9 |
| `paper/wave19_data_paper.pdf` | Compiled PDF | 9 |
| `paper/plos_one_submission_checklist.md` | Submission requirements | — |
| `paper/zenodo_prep.md` | Archive preparation | — |

---

## Paper Structure

1. **Title**: "H₄ Numerological Atlas: A Catalog of Standard Model Parameter Formulas"
2. **Abstract**: Dataset description, 25 formulas, MC validation, availability
3. **Introduction**: Motivation, prior art (Koide, Connes, Furey), gap = no honest statistical catalog
4. **Data Description**: Table 1 (all 25 formulas with σ-distance), classification (S vs NF), mass schemes
5. **Methods**: Search space, validation pipeline, pre-registered MC protocol
6. **Data Records**: JSON schema, GitHub structure, Coq files
7. **Technical Validation**: MC results (Table 2), per-formula significance, limitations
8. **Usage Notes**: Reproduction instructions
9. **Data Availability**: GitHub + Zenodo DOI (pending)

---

## Critical Honesty Rules Followed

- **ZERO claims** that H₄ "derives" the Standard Model
- Language: "correlates", "numerically fitted", "statistically non-trivial"
- Explicit "Ultra-Precision Trap" discussion: 3 formulas fail σ-distance because experimental precision is 10⁵–10⁶× better than catalog precision
- All 5 limitations listed honestly (search space uncertainty, template limitations, manual bias, no Bonferroni, upper-limit observables)

---

## Metrics

| Metric | Wave 18 | Wave 19 |
|--------|---------|---------|
| Qed | 1772 | 1772 |
| Admitted | 0 | 0 |
| Core formulas | 25 | 25 |
| Papers | 1 (boundary finding) | +1 (data paper) |
| MC p-value | < 0.0001 | documented in paper |

---

## Next Steps (pending user action)

1. **Author list**: Fill in `[Author List TBD]` in tex file
2. **Cover letter**: Draft and customize for PLOS ONE
3. **Zenodo**: Enable webhook, create release `v1.0-wave19`, obtain DOI
4. **Supplementary materials**: Create zip archive with scripts + data
5. **Submission**: Upload to PLOS ONE via Editorial Manager
6. **Figures**: Optional histograms for σ-distance and MC distribution

---

*Wave 19 complete: 2026-05-22*
