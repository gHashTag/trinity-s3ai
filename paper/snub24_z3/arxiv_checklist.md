# arXiv Submission Checklist — snub24_z3

Use this checklist when submitting to arXiv.org or to Journal of Mathematical Physics.

## Paper metadata

- [ ] **Title:** "Z_3 tripartition of the snub 24-cell as a flavour structure"
- [ ] **Authors:** Trinity S^3AI Collaboration
- [ ] **Primary arXiv category:** math.GR (Group Theory)
- [ ] **Secondary categories:** math-ph, hep-th, math.CO
- [ ] **Abstract:** (copy from snub24_z3.tex abstract)
- [ ] **Comments:** 10 pages, 1 table, ancillary files include Coq + Lean 4 proofs
- [ ] **Report number:** (if applicable)

## Author account

- [ ] **arXiv account created/available** (each author must have an arXiv account)
- [ ] **Endorsement:** math.GR requires endorsement; ensure at least one author is endorsed in math.GR or a related category (e.g., math-ph, hep-th)
- [ ] **ORCID:** link ORCID iDs if available

## Files uploaded

- [ ] `snub24_z3.tex` — main LaTeX source (clean, no comments, no \input of local files)
- [ ] `snub24_z3.bbl` — bibliography embedded inline (or included as .bbl; arXiv does not run BibTeX)
- [ ] No external image files referenced (paper uses tikz inline and text tables only)
- [ ] `anc/Snub24CellZ3.v` — Coq formalisation
- [ ] `anc/Snub24Z3.lean` — Lean 4 formalisation
- [ ] `anc/README.md` — explanation of ancillary files

## License

- [ ] **arXiv license selected:**
  - Recommended: "arXiv.org perpetual, non-exclusive license" (standard)
  - Alternative: "Creative Commons Attribution license (CC BY)" if the project prefers open licensing

## Compilation check

- [ ] PDF compiles cleanly with `pdflatex` from the submission directory
- [ ] No missing packages (amsart, amsmath, amssymb, amsthm, mathtools, hyperref, url, booktabs, array, xcolor, tikz)
- [ ] No overfull/underfull hbox warnings that obscure text
- [ ] All citations resolve (no [?] in PDF)
- [ ] All cross-references resolve (no ?? in PDF)

## Journal-specific notes (J. Math. Phys.)

- [ ] Follow AIP author guidelines: https://pubs.aip.org/aip/jmp/authors/manuscript
- [ ] Submit via PeerX-Press or the AIP submission portal
- [ ] Suggest referees in cover letter (Dechant, Wilson)
- [ ] IncludeORCID iDs for all authors if available

## Post-submission

- [ ] Note the arXiv identifier (e.g., arXiv:2505.XXXXX)
- [ ] Update the repository README with the arXiv link
- [ ] Tweet/toot the submission (optional)
- [ ] Add the paper to the project bibliography

---

**Last updated:** 2026-05-23
**Paper version:** v1.0 (clean copy for submission)
