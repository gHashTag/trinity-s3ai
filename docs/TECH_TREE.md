# Tech Tree — Trinity S3AI

**The goal is not to prove everything by prose; the goal is to make
each claim unlock only after the previous verification layer passes.**
This file is the layered status map of the hypothesis-verification
stack. Lower layers gate higher layers: infrastructure must be green
before the claim ledger is trustworthy; the claim ledger must be green
before formal proofs can be claimed as load-bearing; and so on.

A reviewer who wants to see the *whole stack* without reading the deep
audits first can read this file linearly. Each layer states what it
contains, what is currently **Checked**, what the known **Blind
spots** are, what the **Next unlock** is, and a per-aspect status row
(per [`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md)). The diagram below is
the grep-friendly version of the same layering.

```
+-------------------------------------+
| L7  Publication                     |
| paper v2 / arXiv / Zenodo / talks   |
+-------------------^-----------------+
                    |
+-------------------+-----------------+
| L6  GOLDEN BRIDGE Game              |
| rings, claim cards, falsified floor |
+-------------------^-----------------+
                    |
+-------------------+-----------------+
| L5  Numerical Fits & Validation     |
| 59 formulas, error windows, p-value |
+-------------------^-----------------+
                    |
+-------------------+-----------------+
| L4  NCG / Lagrangian                |
| spectral triple, sigma-field, SM L  |
+-------------------^-----------------+
                    |
+-------------------+-----------------+
| L3  Geometry  (H4 / 600-cell / Cl)  |
| root system, Snub 24-cell, Cl(8)    |
+-------------------^-----------------+
                    |
+-------------------+-----------------+
| L2  Formal Proofs (Coq / Lean)      |
| NGT1..NGT4 Qed, refutation theorems |
+-------------------^-----------------+
                    |
+-------------------+-----------------+
| L1  Claim Ledger                    |
| 5-status vocabulary, no-overclaim   |
+-------------------^-----------------+
                    |
+-------------------+-----------------+
| L0  Infrastructure                  |
| CI, anti-numerology gate, Pages,    |
| honest counter, Cargo + Coq builds  |
+-------------------------------------+
```

This document is updated when the underlying state changes. The
authoritative ground truth for every layer lives in the linked files;
this is a reading map, not a duplicate. No Theory-of-Everything claim
and no prize-level claim is made or planned.

---

## Layer 0 — Infrastructure

What is in scope: CI workflows, formatters, anti-numerology gate,
honest counter, build scripts, GitHub Pages deploy, Cargo workspaces,
Coq build system.

- **Checked:** Rust workspace tests for `trinity_rust/` and
  `games/trinity_fold/`, Pages / wasm deploy of the GOLDEN BRIDGE
  canvas, anti-numerology gate, Coq build gate, Lean scaffolding gate,
  honest counter (comment-stripped Coq statistics), live game at
  <https://t27.ai/trinity-s3ai/>.
- **Blind spots:** the gates verify build hygiene and tag hygiene, not
  physics; CI is heavy and slow; there is no single dashboard showing
  proof-debt, claim counts, and gate state side-by-side.
- **Next unlock:** CI Observatory dashboard, proof-debt counter wired
  into PRs, Claim Gate (every PR touching public docs must point to a
  ledger row), Artifact Gate for the arXiv bundle.

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

- **Checked:** five-status vocabulary
  (`verified` / `empirical_fit` / `open_conjecture` /
  `high_risk_or_falsified` / `unverified`), no Theory-of-Everything
  wording, no prize wording, the GOLDEN BRIDGE game is framed as a
  hypothesis puzzle and not as evidence.
- **Blind spots:** older `*_v44.md`, `*_v46.md`, and `IMPACT_*` files
  are not yet all linked to ledger rows; tile metadata in the game is
  not yet driven from a single source of truth.
- **Next unlock:** `claims.yaml` / `claims.json` SSOT consumed by
  README, game tile catalogue, and docs generators, so every public
  claim is traceable to exactly one ledger row.

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

- **Checked:** Coq / Rocq infrastructure (Wave 17 baseline: 1 790
  `Qed.`+`Defined.` across the canonical tree; 0 real `Admitted.`
  after comment stripping), Lean 4 scaffolding (`TrinityLean/`), 14
  refutation theorems (`*_refuted`), NGT1..NGT4 closed with `Qed.`.
- **Blind spots:** the formal layer does **not** close the Lagrangian
  derivation; Track B Clifford statements (Cl(0,6) iso, Bott 8-period)
  rest on citation-backed `Axiom`s, not in-tree proofs; the Lean side
  is red on `main` (`H4RootSystem.lean` parse error, `Snub24Z3.lean`
  Mathlib synthesis issues).
- **Next unlock:** machine-readable proof map (which `Qed.` discharges
  which claim row), "no floating theorem" rule, expanded refutation
  library, bridge theorems between Layer 3 geometry and Layer 4
  spectral / Lagrangian side.

| Aspect | Status | Pointer |
|--------|--------|---------|
| Four Coq-formal No-Go Theorems NGT1–NGT4 | **verified** (`Qed.`) | [`proofs/trinity/NoGoTheorems.v`](../proofs/trinity/NoGoTheorems.v) |
| Additional No-Go results NGT-5 (D₄/24-cell), NGT-6 (no σ-field under string/orbifold rescue), NGT-7 (F₄ 3-generation hierarchy) | **verified** at paper / analysis level (not yet Coq-formalised in `NoGoTheorems.v`) | [`paper/CHANGELOG_v1_to_v2.md`](../paper/CHANGELOG_v1_to_v2.md), [`ROADMAP.md`](../ROADMAP.md), [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md) |
| `Qed.`+`Defined.` count (comment-stripped, Wave 17) | **verified** at **1 790** across **81** `.v` files in the canonical tree (52 in `proofs/trinity/` with **1 063** `Qed.`+`Def.`) | run [`scripts/count_admitted_honest.py`](../scripts/count_admitted_honest.py); see [`HONESTY_MANIFEST.md`](../HONESTY_MANIFEST.md) |
| Real `Admitted.` count (comment-stripped, Wave 17) | **0** across the canonical tree (all surface "Admitted" strings in `proofs/trinity/` are inside historical comments) | [`scripts/count_admitted_honest.py`](../scripts/count_admitted_honest.py) JSON output |
| 14 refutation theorems (`*_refuted`) | **verified** | `proofs/trinity/` |
| Track B: Cl(p,q) universal property, Cl(0,6) ≅ M₈(R)⊕M₈(R), Bott 8-periodicity | **open_conjecture** — Wave 17 honest counter reports 0 real `Admitted.`; load-bearing statements remain as cited `Axiom`s (Lounesto 2001 Table 16.3; Wieser–Song 2022 §6; Atiyah–Bott–Shapiro 1964 Table 3; Lawson–Michelsohn 1989 Prop. I.4.1) | [`proofs/clifford_cl8/`](../proofs/clifford_cl8/) |
| Chirality analysis | **open_conjecture** for the full physical claim; NGT3 (the chirality No-Go on the 600-cell) is `Qed.` in `NoGoTheorems.v` | `derivations/chirality/ChiralityAnalysis.v` |
| Lean 4 build of `TrinityLean` | **red** on `main` as of `0832b72` — `H4RootSystem.lean` parse error and `Snub24Z3.lean` Mathlib synthesis issues; tracked as follow-up, not in scope of the review-readiness docs PR | [`.github/workflows/lean.yml`](../.github/workflows/lean.yml), [`derivations/lean_port/TrinityLean/`](../derivations/lean_port/TrinityLean/) |

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

- **Checked:** H4 root system (order 14 400, 120 roots, rank 4),
  600-cell polytope, Snub 24-cell `Z_3` tripartition as a bridge
  candidate, Dirac spectrum on the 600-cell reported numerically as
  `empirical_fit`.
- **Blind spots:** no derivation of the Standard Model from geometry
  alone; no end-to-end bridge `geometry -> spectral triple -> gauge ->
  Lagrangian`; the `a4` conversion factor is not fully reconciled
  across the three derivations.
- **Next unlock:** geometry atlas (one page per geometric fact with
  its status), `a4` reconciliation quest, explicit boundary doc
  separating pure-math facts from physics-dependent ones.

| Aspect | Status | Pointer |
|--------|--------|---------|
| H4 root system, order 14 400, 120 roots, rank 4 | **verified** | `H4Derivations.v`, [`trinity_rust/`](../trinity_rust/) |
| Reflection subgroup chain underlying gauge assignment ansatz | **verified** as mathematics, **open_conjecture** as physics | `H4Derivations.v` |
| Dirac spectrum on 600-cell (Clifford realisation) | **empirical_fit** numerically; reported with figures | [`p1_dirac_spectrum_600cell_report.txt`](../reports/p1_dirac_spectrum_600cell_report.txt), [`p1_spectrum_analysis.png`](../figures/p1_spectrum_analysis.png) |
| Cl(8) / J₃(O) / triality (Track B) | **open_conjecture** (see Layer 2) | `proofs/clifford_cl8/` |

**Next milestone.** Document, in one place, which geometric facts are
purely mathematical (so they will outlive the No-Go) and which are
physics-dependent.

---

## Layer 4 — NCG / Lagrangian

What is in scope: noncommutative-geometry spectral triple, σ-field,
spectral action, attempted derivation of the Standard Model Lagrangian.

- **Checked:** Connes-Chamseddine spectral-action benchmark as the
  comparison target; the derivation chain that the project would need
  to close is enumerated.
- **Blind spots:** the gauge structure, Higgs sector, Yukawa
  couplings, and three-generation structure are not derived; NGT2 (no
  σ-field from H4 alone) and paper-level NGT-6 (no string / orbifold
  rescue) bound what can be recovered.
- **Next unlock:** finite-algebra candidate, Dirac-operator
  construction, inner-fluctuations check, side-by-side NCG comparison
  table, and a "no derivation, no claim" gate on the Lagrangian docs.

| Aspect | Status | Pointer |
|--------|--------|---------|
| Spectral triple construction | **open_conjecture** (`Axiom` scaffolding) | `SpectralExtras.v` |
| σ-field for H4 | **high_risk_or_falsified** | NGT2 in `NoGoTheorems.v` (Coq-formal `Qed.`); reinforced by paper-level NGT-6 (no σ-field under string / orbifold rescue) — see [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md) |
| E₈ plumbing / B-matrix η convergence to −2 | **high_risk_or_falsified** — Wave 17 honesty notes state the η discrepancy does not converge to −2 and the B-matrix is a heuristic, not rigorously derived | [`paper/CHANGELOG_v1_to_v2.md`](../paper/CHANGELOG_v1_to_v2.md) |
| String / heterotic / F-theory / orbifold rescue of the SM mass hierarchy | **high_risk_or_falsified** — no known string compactification selects H4 / F4; toy Z₂ orbifold ~2× vs required ~5000× improvement on Yukawa eigenvalue ratio | [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md) §"Wave 17.2 Findings", `derivations/string_correspondence/` |
| Spectral action computation | **empirical_fit** numerically | [`spectral_action_compute.py`](../scripts/legacy/spectral_action_compute.py), [`spectral_action_results.md`](analysis/spectral_action_results.md) |
| SM Lagrangian "from H4" | **open_conjecture** with substantial fit content | [`LAGRANGIAN_HONEST_STATUS.md`](status/LAGRANGIAN_HONEST_STATUS.md), [`lagrangian_roadmap.md`](roadmaps/lagrangian_roadmap.md) |
| Yukawa coupling derivation | **empirical_fit** | [`yukawa_from_h4_derivation.md`](analysis/yukawa_from_h4_derivation.md), [`yukawa_h4_results.json`](../data/yukawa_h4_results.json) |
| RG running of gauge couplings | **verified** (numerical scheme) | [`RG_RUNNING_PROVEN.md`](analysis/RG_RUNNING_PROVEN.md), `RGRunningExtras.v` |

**Next milestone.** Either close the gap between the spectral-action
construction and the SM Lagrangian fits, or downgrade the relevant
documents from "derivation" wording to "fit" wording with a
cross-reference to the relevant No-Go theorem.

---

## Layer 5 — Numerical fits and validation

What is in scope: the 59 catalogued numerical matches, error windows,
falsifiability assessments, and risky predictions.

- **Checked:** 59 formulas matching PDG 2024 inside stated windows
  (interval-bound `Qed.` in `proofs/catalog/Catalog42_corrected.v`), reproducibility
  scripts, falsifiability protocol, honest p-value computation, RG
  running scheme.
- **Blind spots:** the `e^2` derivation, full RG closure,
  numerology / look-elsewhere risk, post-data fitting risk on any new
  numerical claim.
- **Next unlock:** fit registry tied to the claim ledger, systematic
  ablations, RG quest, pre-registered prediction lock so that no new
  numerical claim is allowed to land without a stated window.

| Aspect | Status | Pointer |
|--------|--------|---------|
| 59 formulas matching PDG 2024 within stated windows | **empirical_fit** (with `Qed.` bound checks) | [`Catalog42_corrected.v`](../proofs/catalog/Catalog42_corrected.v) |
| 11 SG-class formulas (< 0.01 % error) | **empirical_fit** | README §"Coq Proof Statistics" |
| 14 V-class formulas (0.01–0.3 % error) | **empirical_fit** | README §"Coq Proof Statistics" |
| Falsifiability protocol | **verified** as a protocol; the predictions themselves are **open_conjecture** | [`Trinity_Falsifiability_Assessment.md`](analysis/Trinity_Falsifiability_Assessment.md) |
| Risky predictions (DUNE, JUNO, LHC) | **open_conjecture** | [`RISKY_PREDICTIONS.md`](analysis/RISKY_PREDICTIONS.md) and per-experiment files |
| Honest p-value report | **verified** as a computation | [`honest_pvalue_report.txt`](../reports/honest_pvalue_report.txt) |

**Next milestone.** Maintain the SG/V-class numbers as PDG updates land.

---

## Layer 6 — GOLDEN BRIDGE game

What is in scope: the hypothesis-discovery puzzle deployed at
<https://t27.ai/trinity-s3ai/>, and its Rust workspace.

- **Checked:** Rust + wasm GOLDEN BRIDGE canvas (live on Pages),
  five-ring Cargo workspace with inward-only dependency tests, every
  tile carries a `ClaimStatus`, falsification floor (any falsified
  tile collapses the bridge), framing the game as
  "data + geometry -> bridge candidate" rather than as proof.
- **Blind spots:** the game is an educational interface, not a proof
  engine; level catalogue and claim-ledger SSOT are not yet wired into
  the game's tile data; "the game proves something" must stay an
  explicit non-claim.
- **Next unlock:** GOLDEN BRIDGE levels 1..5, each unlocked only when
  its underlying claim row reaches the required status.

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

- **Checked:** TRIOS PhD-style pipeline (paper v2, seminar talk v2,
  arXiv tarball, Zenodo deposit plan, citation metadata); all public
  documents written in English.
- **Blind spots:** drift risk between README, paper PDF, talk slides,
  and game tile text; possible non-English leakage in older artefacts;
  secrets in the tree.
- **Next unlock:** generated publication artefacts (README, paper, and
  game catalogue all driven from `claims.yaml`); strict no-Cyrillic /
  English-only gate on public docs; automated secret-scan gate.

| Aspect | Status | Pointer |
|--------|--------|---------|
| Paper draft v2 (Wave 17) — negative-result framing | **draft, review-ready per Wave 17 report** | [`paper/wave17_paper_v2.pdf`](../paper/wave17_paper_v2.pdf), [`paper/wave17_paper_v2.tex`](../paper/wave17_paper_v2.tex), [`paper/CHANGELOG_v1_to_v2.md`](../paper/CHANGELOG_v1_to_v2.md) |
| Seminar talk v2 (Wave 17) | **draft, review-ready per Wave 17 report** | [`talks/wave17_talk.pdf`](../talks/wave17_talk.pdf), [`talks/wave17_talk.tex`](../talks/wave17_talk.tex), [`talks/QANDA_PREP.md`](../talks/QANDA_PREP.md) |
| arXiv submission tarball | **prepared** | [`trinity-s3ai-arxiv.tar.gz`](../releases/trinity-s3ai-arxiv.tar.gz), [`paper/arxiv_checklist.md`](../paper/arxiv_checklist.md) |
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
  [`COQ_HONEST_STATUS.md`](status/COQ_HONEST_STATUS.md); when those
  disagree with this file, those win and this file should be updated.
- It is not a list of every formula; that is what
  [`TRACEABILITY.md`](analysis/TRACEABILITY.md) and
  [`FORMULAS.md`](../FORMULAS.md) are for.
