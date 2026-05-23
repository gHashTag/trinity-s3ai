# Tech Tree — Trinity S3AI

A layered status map of the repository, written for a reviewer who
wants to see the *whole stack* without reading the deep audits first.
Each layer states: what it contains, what status its claims have (per
[`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md)), and what the next milestone
is.

This document is updated when the underlying state changes. The
authoritative ground truth for every layer lives in the linked files;
this is a reading map, not a duplicate.

---

## Layer 0 — Infrastructure

What is in scope: CI workflows, formatters, anti-numerology gate,
honest counter, build scripts, GitHub Pages deploy, Cargo workspaces,
Coq build system.

| Aspect | Status | Pointer |
|--------|--------|---------|
| CI: anti-numerology → Coq build → Python validators | **verified** (runs on every PR) | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) |
| Rust CI for `trinity_rust/` and `games/trinity_fold/` | **verified** | [`.github/workflows/rust.yml`](../.github/workflows/rust.yml) |
| Pages deploy of GOLDEN BRIDGE canvas | **verified** | [`.github/workflows/pages.yml`](../.github/workflows/pages.yml); live at <https://t27.ai/trinity-s3ai/> |
| Release bundle (Coq + PDF) | **verified** | [`.github/workflows/release.yml`](../.github/workflows/release.yml) |
| Lean 4 / Mathlib aux | **verified** (scaffolding only) | [`.github/workflows/lean.yml`](../.github/workflows/lean.yml) |
| No secrets in tree | **verified** | [`SECURITY.md`](../SECURITY.md) |

**Next milestone.** Keep the gate green; ratchet the Rust workspace's
clippy from warnings-only to deny on PRs once the game crates stabilise.

---

## Layer 1 — Claim ledger

What is in scope: the rules that tell a reviewer how to read every
statement in the rest of the repository.

| Aspect | Status | Pointer |
|--------|--------|---------|
| Five-status vocabulary (`verified` / `empirical_fit` / `open_conjecture` / `high_risk_or_falsified` / `unverified`) | **verified** (used by code and docs) | [`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md) |
| No-overclaim rule (no ToE, no prize claims) | **verified** (policy) | [`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md) §2 |
| Honest counter (comment-stripped Coq statistics) | **verified** | [`scripts/count_admitted_honest.py`](../scripts/count_admitted_honest.py), [`HONESTY_MANIFEST.md`](../HONESTY_MANIFEST.md) |
| Anti-numerology gate (mechanical tag check) | **verified** | [`scripts/anti_numerology_gate.py`](../scripts/anti_numerology_gate.py) |
| Headline-claim classification table | **verified** (this revision) | [`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md) §4 |

**Next milestone.** Sweep older `*_v44.md`, `*_v46.md`, `IMPACT_*`
documents to either remove them or front them with a "historical"
banner pointing at this layer.

---

## Layer 2 — Formal proofs

What is in scope: Coq proofs (and Lean scaffolding) of mathematical
content, including the four No-Go theorems and the interval bounds.

| Aspect | Status | Pointer |
|--------|--------|---------|
| Four No-Go Theorems NGT1–NGT4 | **verified** | [`proofs/trinity/NoGoTheorems.v`](../proofs/trinity/NoGoTheorems.v) |
| `Qed.` count (comment-stripped) | **verified** at 1 762 across 79 `.v` files | [`HONESTY_MANIFEST.md`](../HONESTY_MANIFEST.md) |
| Real `Admitted.` count | **5**, each tagged | [`HONESTY_MANIFEST.md`](../HONESTY_MANIFEST.md) §2 |
| 14 refutation theorems (`*_refuted`) | **verified** | `proofs/trinity/` |
| Track B: Cl(p,q) universal property, Cl(0,6) ≅ M₈(R)⊕M₈(R), Bott 8-periodicity | **open_conjecture** (4 `Admitted` with citations) | [`proofs/clifford_cl8/`](../proofs/clifford_cl8/) |
| Chirality analysis | **open_conjecture** (1 `Admitted`, `[OPEN_PROBLEM]`) | `derivations/chirality/ChiralityAnalysis.v` |

**Next milestone.** Discharge the 4 Track B Admitteds with mechanical
or citation-driven proofs; close the chirality `[OPEN_PROBLEM]` or
record it as a permanent open question.

---

## Layer 3 — Geometry (H4, 600-cell, Clifford)

What is in scope: pure-mathematical content of the H4 root system,
the 600-cell polytope, reflection subgroups, and the Clifford-algebra
strand.

| Aspect | Status | Pointer |
|--------|--------|---------|
| H4 root system, order 14 400, 120 roots, rank 4 | **verified** | `H4Derivations.v`, [`trinity_rust/`](../trinity_rust/) |
| Reflection subgroup chain underlying gauge assignment ansatz | **verified** as mathematics, **open_conjecture** as physics | `H4Derivations.v` |
| Dirac spectrum on 600-cell (Clifford realisation) | **empirical_fit** numerically; reported with figures | [`p1_dirac_spectrum_600cell_report.txt`](../p1_dirac_spectrum_600cell_report.txt), [`p1_spectrum_analysis.png`](../p1_spectrum_analysis.png) |
| Cl(8) / J₃(O) / triality (Track B) | **open_conjecture** (see Layer 2) | `proofs/clifford_cl8/` |

**Next milestone.** Document, in one place, which geometric facts are
purely mathematical (so they will outlive the No-Go) and which are
physics-dependent.

---

## Layer 4 — NCG / Lagrangian

What is in scope: noncommutative-geometry spectral triple, σ-field,
spectral action, attempted derivation of the Standard Model Lagrangian.

| Aspect | Status | Pointer |
|--------|--------|---------|
| Spectral triple construction | **open_conjecture** (`Axiom` scaffolding) | `SpectralExtras.v` |
| σ-field for H4 | **high_risk_or_falsified** | NGT2 in `NoGoTheorems.v` |
| Spectral action computation | **empirical_fit** numerically | [`spectral_action_compute.py`](../spectral_action_compute.py), [`spectral_action_results.md`](../spectral_action_results.md) |
| SM Lagrangian "from H4" | **open_conjecture** with substantial fit content | [`LAGRANGIAN_HONEST_STATUS.md`](../LAGRANGIAN_HONEST_STATUS.md), [`lagrangian_roadmap.md`](../lagrangian_roadmap.md) |
| Yukawa coupling derivation | **empirical_fit** | [`yukawa_from_h4_derivation.md`](../yukawa_from_h4_derivation.md), [`yukawa_h4_results.json`](../yukawa_h4_results.json) |
| RG running of gauge couplings | **verified** (numerical scheme) | [`RG_RUNNING_PROVEN.md`](../RG_RUNNING_PROVEN.md), `RGRunningExtras.v` |

**Next milestone.** Either close the gap between the spectral-action
construction and the SM Lagrangian fits, or downgrade the relevant
documents from "derivation" wording to "fit" wording with a
cross-reference to the relevant No-Go theorem.

---

## Layer 5 — Numerical fits and validation

What is in scope: the 59 catalogued numerical matches, error windows,
falsifiability assessments, and risky predictions.

| Aspect | Status | Pointer |
|--------|--------|---------|
| 59 formulas matching PDG 2024 within stated windows | **empirical_fit** (with `Qed.` bound checks) | [`Catalog42_corrected.v`](../Catalog42_corrected.v) |
| 11 SG-class formulas (< 0.01 % error) | **empirical_fit** | README §"Coq Proof Statistics" |
| 14 V-class formulas (0.01–0.3 % error) | **empirical_fit** | README §"Coq Proof Statistics" |
| Falsifiability protocol | **verified** as a protocol; the predictions themselves are **open_conjecture** | [`Trinity_Falsifiability_Assessment.md`](../Trinity_Falsifiability_Assessment.md) |
| Risky predictions (DUNE, JUNO, LHC) | **open_conjecture** | [`RISKY_PREDICTIONS.md`](../RISKY_PREDICTIONS.md) and per-experiment files |
| Honest p-value report | **verified** as a computation | [`honest_pvalue_report.txt`](../honest_pvalue_report.txt) |

**Next milestone.** Maintain the SG/V-class numbers as PDG updates land.

---

## Layer 6 — GOLDEN BRIDGE game

What is in scope: the hypothesis-discovery puzzle deployed at
<https://t27.ai/trinity-s3ai/>, and its Rust workspace.

| Aspect | Status | Pointer |
|--------|--------|---------|
| Five-ring Cargo workspace with inward-only deps | **verified** by tests | `games/trinity_fold/crates/app/tests/ring_boundaries.rs` |
| `ClaimStatus` enum on every tile | **verified** | `games/trinity_fold/crates/ring0_core/` |
| Falsification floor (any falsified tile → bridge collapses) | **verified** | `games/trinity_fold/crates/ring1_constraints/` |
| Static canvas rendered to GitHub Pages | **verified** | live at <https://t27.ai/trinity-s3ai/> |
| "Game proves a Theory of Everything" | **not claimed** | [`games/trinity_fold/README.md`](../games/trinity_fold/README.md) |

**Next milestone.** Keep the tile catalogue honest: every new tile must
have a `ClaimStatus` and a citation if its status is stronger than
`unverified`.

---

## Layer 7 — Publication

What is in scope: the paper, arXiv submission, citation metadata.

| Aspect | Status | Pointer |
|--------|--------|---------|
| Paper draft v2 (Wave 17) | **draft** | [`paper/wave17_paper_v2.pdf`](../paper/wave17_paper_v2.pdf), [`paper/wave17_paper_v2.tex`](../paper/wave17_paper_v2.tex) |
| arXiv submission tarball | **prepared** | [`trinity-s3ai-arxiv.tar.gz`](../trinity-s3ai-arxiv.tar.gz), [`paper/arxiv_checklist.md`](../paper/arxiv_checklist.md) |
| Citation metadata | **verified** | [`CITATION.cff`](../CITATION.cff), [`CITATION.bib`](../CITATION.bib) |
| Zenodo deposit | **planned** (DOI pending) | [`scripts/prepare_zenodo.md`](../scripts/prepare_zenodo.md) |
| External validation | **not yet sought** | — |

**Next milestone.** arXiv submission and Zenodo deposit; update DOI
badge in the root README when assigned.

---

## What the tech tree is *not*

- It is not a roadmap with dates. See [`ROADMAP.md`](../ROADMAP.md) and
  [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md).
- It is not a substitute for the audits in
  [`HONESTY_MANIFEST.md`](../HONESTY_MANIFEST.md) and
  [`COQ_HONEST_STATUS.md`](../COQ_HONEST_STATUS.md); when those
  disagree with this file, those win and this file should be updated.
- It is not a list of every formula; that is what
  [`TRACEABILITY.md`](../TRACEABILITY.md) and
  [`FORMULAS.md`](../FORMULAS.md) are for.
