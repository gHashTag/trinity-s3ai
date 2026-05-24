# RESEARCH_STATUS — Boundary Map of the H4 → SM Exploration

This file is the short, plain-English summary that [`README.md`](README.md)
and several other documents link to. It maps what is **open**, what is
**obstructed**, and what is **under active exploration**. The deep audits
live elsewhere and are linked below.

---

## In one paragraph

Trinity S³AI is an active boundary-mapping research program that **tests the single hypothesis** that H4 Coxeter group geometry encodes the parameters of the Standard Model of particle physics. We explore H4 invariants, 600-cell geometry, E8 embeddings, Clifford algebras Cl(8), and φ/π/e phenomenological coincidences — formalizing what works, rigorously mapping obstruction boundaries (BT-1–BT-7), and redirecting toward new ansätze when specific constructions fail. The project commits to one hypothesis while transparently documenting where it succeeds and where it hits boundaries.

**Boundary theorems (BT-1–BT-4)** mark specific obstruction points: they
prove that *certain direct constructions* from H4 geometry do not reproduce
the SM. These are **guideposts**, not dead ends — they narrow the search
space and direct ongoing work toward Tracks A, B, and C.

The project maintains a living catalog of 59 numerical coincidences between
H4 invariants and PDG 2024 measurements, all formally verified in Coq and
tagged by epistemic status. Whether these coincidences are deep or
accidental is itself an open research question. The ultimate goal is to
find a rigorous bridge from discrete geometry to fundamental physics — or
to map the full boundary of why such a bridge is difficult.

---

## Known Obstructions (proven in Coq)

The four Coq-formal obstruction theorems in
[`proofs/trinity/BoundaryTheorems.v`](proofs/trinity/BoundaryTheorems.v):

| | Statement | What it bounds |
|---|-----------|----------------|
| **BT-1** | φ^a · π^b · e^c formulas cannot reproduce Λ or Ω_b | Cosmological constant / baryon fraction from this ansatz |
| **BT-2** | No NCG σ-field from H4 root structure alone | A core NCG ingredient in the obvious H4 construction |
| **BT-3** | 600-cell D_F is vector-like (antipodal symmetry) | Chiral fermions in the obvious construction |
| **BT-4** | 2I-equivariant D_F cannot reproduce lepton mass ratios | Lepton mass hierarchy in the obvious construction |

These are formal Coq theorems with closing `Qed.`s. They are **boundary**
claims: they do not say "no H4-based theory of anything is possible", they
say "*these specific constructions hit a wall*". Future waves may find
detours, alternative algebras, or entirely different geometric starting
points.

Three further Wave 11–17 boundary results are documented at paper /
analysis level — **BT-5** (D₄/24-cell does not yield 3 generations,
Wave 11), **BT-6** (no σ-field under string / orbifold rescue,
Wave 14–17.2) and **BT-7** (F₄ cannot produce the SM 3-generation
hierarchy, Wave 16) — see
[`paper/CHANGELOG_v1_to_v2.md`](paper/CHANGELOG_v1_to_v2.md),
[`ROADMAP.md`](ROADMAP.md) §"Boundary theorems" and
[`ROADMAP_WAVE17_PLUS.md`](ROADMAP_WAVE17_PLUS.md). These are honestly
flagged as *not yet Coq-formalised in `proofs/trinity/BoundaryTheorems.v`*
and are tracked for promotion to `Qed.` in future waves.

## What the project delivers now

- **59 numerical matches.** Combinations of φ, π, e and small
  integers reproduce many SM observables (masses, couplings, mixing
  angles) within stated error windows. **These are fits, not
  derivations.** Every such formula is tagged `[phenomenological_fit]`
  or `[NUMERICAL_FIT]`, and the
  [anti-numerology gate](scripts/anti_numerology_gate.py) enforces the
  tagging on every PR. See [`Catalog42_corrected.v`](proofs/catalog/Catalog42_corrected.v).
- **A growing body of real Coq mathematics.** As of Wave 17 the
  comment-stripped honest counter
  ([`scripts/count_admitted_honest.py`](scripts/count_admitted_honest.py))
  reports **1 790 `Qed.`+`Defined.`** across **81** `.v` files in the
  canonical tree, with **1 063** of those in `proofs/trinity/`
  (52 files), and **0** real `Admitted.` anywhere in the canonical
  tree. Most of these are bound checks and structural lemmas; the
  obstruction theorems are the load-bearing physical content. See
  [`HONESTY_MANIFEST.md`](HONESTY_MANIFEST.md) for the reconciliation
  with older inconsistent metric documents.
- **A falsification protocol.** Risky predictions for DUNE, JUNO and
  LHC are listed in [`RISKY_PREDICTIONS.md`](docs/analysis/RISKY_PREDICTIONS.md) with
  criteria that would falsify them. The protocol is in
  [`Trinity_Falsifiability_Assessment.md`](docs/analysis/Trinity_Falsifiability_Assessment.md).
- **A hypothesis-discovery puzzle, GOLDEN BRIDGE.** Live at
  <https://t27.ai/trinity-s3ai/>. The game scores candidate boards
  against a small curated rule set, surfaces the worst claim status,
  and floors the score if any tile is falsified. It does not prove or
  test any Theory-of-Everything claim, and a high score is not
  evidence. See
  [`games/trinity_fold/README.md`](games/trinity_fold/README.md).

## Research Directions Within the H4 → SM Program

The project explores the H4 → SM hypothesis through several interconnected approaches:

| Direction | Status | What we are learning |
|-----------|--------|---------------------|
| **Direct NCG construction** (H4 root system → spectral triple) | 🔄 Obstructed at BT-2, BT-3, BT-4 | The obvious construction fails; we map exactly where and why |
| **600-cell phenomenology** (φ/π/e coincidence catalog) | 🔄 59 matches; statistical audit ongoing | Whether these coincidences are deep or accidental is an open research question |
| **Cl(8) / triality** (spinor algebra, three generations) | 🔄 Active (T1 ✅, T2–T12 🔄) | Alternative algebraic route that may bypass H4-specific obstructions |
| **E8 plumbing / string correspondence** | 🔄 Partial (η discrepancy documented) | Testing whether exceptional-group embeddings rescue the construction |
| **Neutrino sector predictions** | 🔄 Open (δ_CP withdrawn; θ₁₂, θ₁₃ match) | Pre-registered predictions to be adjudicated by DUNE, JUNO, KATRIN |
| **Cosmology ansatz** | ❌ Obstructed (BT-1; >300σ) | Honest closure: this sub-ansatz does not work |

> **The research continues.** The H4 → SM hypothesis is alive and under active investigation. Obstructions on specific constructions are data, not defeats. Every boundary theorem tells us where *not* to build — which is as valuable as knowing where to build next.
