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
| Four Coq-formal No-Go Theorems NGT1–NGT4 | **verified** (`Qed.`) | [`proofs/trinity/NoGoTheorems.v`](../proofs/trinity/NoGoTheorems.v) |
| Additional No-Go results NGT-5 (D₄/24-cell), NGT-6 (no σ-field under string/orbifold rescue), NGT-7 (F₄ 3-generation hierarchy) | **verified** at paper / analysis level (not yet Coq-formalised in `NoGoTheorems.v`) | [`paper/CHANGELOG_v1_to_v2.md`](../paper/CHANGELOG_v1_to_v2.md), [`ROADMAP.md`](../ROADMAP.md), [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md) |
| `Qed.`+`Defined.` count (comment-stripped, Wave 17) | **verified** at **1 790** across **81** `.v` files in the canonical tree (52 in `proofs/trinity/` with **1 063** `Qed.`+`Def.`) | run [`scripts/count_admitted_honest.py`](../scripts/count_admitted_honest.py); see [`HONESTY_MANIFEST.md`](../HONESTY_MANIFEST.md) |
| Real `Admitted.` count (comment-stripped, Wave 17) | **0** across the canonical tree (all surface "Admitted" strings in `proofs/trinity/` are inside historical comments) | [`scripts/count_admitted_honest.py`](../scripts/count_admitted_honest.py) JSON output |
| 14 refutation theorems (`*_refuted`) | **verified** | `proofs/trinity/` |
| Track B: Cl(p,q) universal property, Cl(0,6) ≅ M₈(R)⊕M₈(R), Bott 8-periodicity | **open_conjecture** — Wave 17 honest counter reports 0 real `Admitted.`; load-bearing statements remain as cited `Axiom`s (Lounesto 2001 Table 16.3; Wieser–Song 2022 §6; Atiyah–Bott–Shapiro 1964 Table 3; Lawson–Michelsohn 1989 Prop. I.4.1) | [`proofs/clifford_cl8/`](../proofs/clifford_cl8/) |
| Chirality analysis | **open_conjecture** for the full physical claim; NGT3 (the chirality No-Go on the 600-cell) is `Qed.` in `NoGoTheorems.v` | `derivations/chirality/ChiralityAnalysis.v` |
| Lean 4 build of `TrinityLean` | **red** on `main` as of `0832b72` — `H4RootSystem.lean` parse error and `Snub24Z3.lean` Mathlib synthesis issues; tracked as follow-up, not in scope of the review-readiness docs PR | [`.github/workflows/lean.yml`](../.github/workflows/lean.yml), [`TrinityLean/`](../TrinityLean/) |

**Next milestone.** Promote NGT-5..7 from paper / analysis level to
Coq-formal theorems in `proofs/trinity/NoGoTheorems.v`; fix the
`TrinityLean` parse / synthesis failures so the Lean side matches the
Coq side; replace the citation-backed `Axiom`s in `proofs/clifford_cl8/`
with in-tree proofs over the next waves of Track B.

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
| σ-field for H4 | **high_risk_or_falsified** | NGT2 in `NoGoTheorems.v` (Coq-formal `Qed.`); reinforced by paper-level NGT-6 (no σ-field under string / orbifold rescue) — see [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md) |
| E₈ plumbing / B-matrix η convergence to −2 | **high_risk_or_falsified** — Wave 17 honesty notes state the η discrepancy does not converge to −2 and the B-matrix is a heuristic, not rigorously derived | [`paper/CHANGELOG_v1_to_v2.md`](../paper/CHANGELOG_v1_to_v2.md) |
| String / heterotic / F-theory / orbifold rescue of the SM mass hierarchy | **high_risk_or_falsified** — no known string compactification selects H4 / F4; toy Z₂ orbifold ~2× vs required ~5000× improvement on Yukawa eigenvalue ratio | [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md) §"Wave 17.2 Findings", `derivations/string_correspondence/` |
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
| Paper draft v2 (Wave 17) — negative-result framing | **draft, review-ready per Wave 17 report** | [`paper/wave17_paper_v2.pdf`](../paper/wave17_paper_v2.pdf), [`paper/wave17_paper_v2.tex`](../paper/wave17_paper_v2.tex), [`paper/CHANGELOG_v1_to_v2.md`](../paper/CHANGELOG_v1_to_v2.md) |
| Seminar talk v2 (Wave 17) | **draft, review-ready per Wave 17 report** | [`talks/wave17_talk.pdf`](../talks/wave17_talk.pdf), [`talks/wave17_talk.tex`](../talks/wave17_talk.tex), [`talks/QANDA_PREP.md`](../talks/QANDA_PREP.md) |
| arXiv submission tarball | **prepared** | [`trinity-s3ai-arxiv.tar.gz`](../trinity-s3ai-arxiv.tar.gz), [`paper/arxiv_checklist.md`](../paper/arxiv_checklist.md) |
| Citation metadata | **verified** | [`CITATION.cff`](../CITATION.cff), [`CITATION.bib`](../CITATION.bib) |
| Zenodo deposit | **planned** (DOI pending) | [`scripts/prepare_zenodo.md`](../scripts/prepare_zenodo.md) |
| Post-Wave-17 roadmap (Tracks A / B / C) | **published** | [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md) |
| External validation | **not yet sought** | — |

**Next milestone.** arXiv submission (Track C: negative-result paper)
and Zenodo deposit; update DOI badge in the root README when assigned.
Tracks A (honest phenomenology / p-value) and B (Cl(8) formalisation)
continue per [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md).
No Theory-of-Everything or prize-level claim is made or planned.

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
