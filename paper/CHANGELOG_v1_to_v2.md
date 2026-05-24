# CHANGELOG: wave13_paper.tex → wave17_paper_v2.tex

**Date:** 2026-05-23
**Base document:** `paper/wave13_paper.tex` (Wave 13.5)
**New document:** `paper/wave17_paper_v2.tex` (Wave 17.3)

---

## Page Count

| Version | Pages | Delta |
|---------|-------|-------|
| v1 (wave13) | 6 | — |
| v2 (wave17) | 10 | **+4** |

---

## New Sections Added

### 1. Section 5 — Extended Boundary Findings (Waves 16–17)
A new main section inserted between the original Boundary theorems (now §4) and Discussion (now §6).

#### 5.1 F₄ Yukawa Test (Obstruction Theorem 7)
- Describes the numerical scan of 5 models per fermion type
- Reports the D₄ triality structural cap at ~20:1
- Documents that symmetric models fail (χ² > 9 for all fermion types)
- Documents that weighted/block models fit only with 3–4 free parameters lacking geometric origin
- **Obstruction Theorem 7:** F₄ cannot produce the observed 3-generation hierarchy without external parameters

#### 5.2 E₈ Plumbing Convergence
- Reports η values for reduced model (20 vertices): sign-count η = 0
- Reports η values for full model (128 vertices, heuristic B):
  - sign-count η = −64
  - soft-cutoff regularization converges to η ≈ −65.93 as ε → 0
- APS target: η = −2
- Honest assessment: discrete η does NOT converge to −2 with current heuristic B
- B-matrix rigorous derivation remains open

### 2. Updated Sections

#### Abstract
- Updated Coq stats: 1375 Qed (was 1183), 0 Admitted (was 81)
- Added F₄ Yukawa boundary finding mention
- Added experimental consistency (JUNO, DESI) and tension (DUNE δ_CP)
- Expanded boundary theorems from 5 to 7 Boundary theorems

#### §2.4 Formal Proof Infrastructure
- Qed: 1375 (was 1183)
- Admitted: 0 (was 81)
- Added Axiom count: 77
- Added file count: 79 .v files
- Updated Lean 4 port: 9 modules (was 4)

#### §6 Discussion (was §5)
- Added "Experimental falsification registry" subsection
  - JUNO 2025 Δm²₂₁ consistent at 0.25σ
  - DESI DR2 normal hierarchy consistent
  - DUNE δ_CP >3σ tension reaffirmed
- Added "Formal verification status" subsection
  - 0 Admitted achieved in Wave 16
  - 77 Axioms + 1 inline admit documented
  - Lean 4 port: 9 modules
- Added comparison to Gürsey–Ramond program

#### §7 Conclusion (was §6)
- Added mention of F₄ Yukawa failure

#### Appendix A — Coq Proof Statistics
- Qed: 1375 (was 1183)
- Admitted: 0 (was 81)
- Axioms: 77 (new line)
- Refutations: 7 (was 6; added BT-7)
- Files: 79 (was 49)

#### Appendix B — Lean 4 Port Status
- Updated to 9 modules (was 4)
- Added CorePhi.lean, DiracOperator.lean

#### Appendix C — Python Validation Results
- Added yukawa_scan.py result
- Added b_matrix_derivation.py result

#### Appendix D — Falsification Registry
- Added JUNO 2025 consistency for Δm²₂₁
- Added DESI DR2 consistency for normal hierarchy
- Updated DUNE δ_CP status to >3σ tension

#### References
- Added JUNO 2025 (arXiv:2511.14593)
- Added DESI DR2 (Phys. Rev. D 112, 083515)
- Added Ramond "Exceptional groups and physics" (arXiv:hep-th/0112261)
- Added Gürsey–Ramond–Sikivie E₆ model (Phys. Lett. B 60, 177)

---

## New Theorems Added

| ID | Name | Section | Status |
|----|------|---------|--------|
| BT-7 | F₄ cannot produce 3-generation hierarchy | 5.1 | Qed (numerical test) |

---

## Numbers Updated

| Metric | v1 (Wave 13) | v2 (Wave 17) | Delta |
|--------|--------------|--------------|-------|
| Coq Qed | 1183 | **1375** | +192 |
| Coq Admitted | 81 | **0** | −81 |
| Coq Axioms | not stated | **77** | new |
| Coq .v files | 49 | **79** | +30 |
| Lean modules | 4 | **9** | +5 |
| Boundary theorems | 5 | **7** | +2 |
| Refutations | 6 | **7** | +1 |

---

## Honesty Notes

- All numbers match the repo state as of commit `b509d4d` (Wave 16 + Lean pin).
- The F₄ Yukawa result is framed as a "numerical test suggests" failure, not a rigorous proof.
- The E₈ plumbing η discrepancy is honestly labelled: the B-matrix is a heuristic, not rigorously derived.
- The 0 Admitted status applies to the canonical 79-file proof tree; 1 inline `admit` remains in `E6vsH4.v`.
