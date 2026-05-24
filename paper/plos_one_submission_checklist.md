# PLOS ONE Submission Checklist — Wave 19 Data Paper

**Paper**: "H₄ Numerological Atlas: A Catalog of Standard Model Parameter Formulas"
**Target journal**: PLOS ONE (hep-th or Interdisciplinary Physics)
**Date**: 2026-05-22

---

## Pre-Submission Requirements

### Manuscript Files
- [x] `wave19_data_paper.tex` — LaTeX source
- [x] `wave19_data_paper.pdf` — compiled PDF (9 pages)
- [ ] `wave19_data_paper.bbl` — bibliography (if using BibTeX; currently inline `thebibliography`)

### Cover Letter
- [ ] Draft cover letter emphasizing:
  - This is a **data paper**, not a theory paper
  - No claims about H₄ "deriving" the Standard Model
  - Dataset includes formal proofs, numerical validation, and statistical tests
  - Negative-result companion paper already exists (Wave 17, arXiv:XXXX.XXXXX)

### Statements
- [ ] **Conflict of Interest**: None declared
- [ ] **Funding**: None — curiosity-driven open-source project
- [ ] **Data Availability Statement**: (see below)
- [ ] **Ethics Statement**: Not applicable (no human/animal subjects)

### Figures & Tables
- [x] Table 1: 25-formula catalog (longtable, spans 2 pages)
- [x] Table 2: Monte-Carlo results
- [ ] Optional Figure 1: σ-distance distribution histogram (can add)
- [ ] Optional Figure 2: MC error distribution comparison (can add)

### Supplementary Materials
- [ ] `wave19_supplementary.zip` containing:
  - `validate_v4.py`
  - `honest_phenomenology_v18.py`
  - `wave18_mc_results.json`
  - `sigma_ranking.md`
  - `FORMULAS.md`

---

## PLOS ONE Specific Requirements

### Data Availability Statement (required)
> All data, code, and formal proofs are available in the GitHub repository
> https://github.com/gHashTag/trinity-s3ai under the MIT license (code)
> and CC-BY-4.0 license (data). The dataset is archived on Zenodo
> (DOI: 10.5281/zenodo.XXXXXX, pending).

### Article Type
- Select: **Research Article** (PLOS ONE does not have a dedicated "Data Paper" type, but accepts dataset descriptions as regular articles)
- Alternative: **Methods and Resources** (if available in the submission system)

### Keywords
- Standard Model
- Particle physics phenomenology
- Golden ratio
- Data catalog
- Monte-Carlo validation
- Formal verification

### Subject Areas
- Physics: High Energy Physics - Phenomenology (hep-ph)
- Physics: High Energy Physics - Theory (hep-th)
- Computer Science: Formal Methods

---

## Post-Acceptance Steps

- [ ] Respond to reviewer comments
- [ ] Update Zenodo DOI in final version
- [ ] Tag GitHub release `v1.0-wave19`
- [ ] Update README.md with publication citation
- [ ] Register ORCID for all authors

---

## Alternative Journals (if PLOS ONE rejects)

| Journal | Pros | Cons |
|---------|------|------|
| **Data in Brief** (Elsevier) | Dedicated data journal | APC ~$600 |
| **Scientific Data** (Nature) | High impact | Very competitive; requires novelty |
| **PLOS ONE** | Welcomes methodological and data papers; no APC for some | Broad scope may mean less visibility |
| **SIGMA** | Math-physics focus; free OA | May want more theory |

---

*Checklist created: 2026-05-22*
