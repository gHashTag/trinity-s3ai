# SALVAGE — What H4 *can* and *cannot* do

This file is the short, plain-English summary the
[`README.md`](README.md) and several other documents link to. It is
intentionally a single page; the deep audits live elsewhere and are
linked below.

---

## In one paragraph

Trinity S3AI started as an investigation of whether the H4 Coxeter
group (and the 600-cell polytope) could underlie a noncommutative
geometry (NCG) model of the Standard Model of particle physics.
**The answer is: no, not as originally hoped.** Four formal No-Go
Theorems in Coq prove specific structural impossibilities. What is
preserved — the "salvage" — is a catalogue of 59 numerical coincidences
between H4 invariants and PDG 2024 measurements, every one tagged as a
*phenomenological fit*, never as a derivation. This repository is a
constructive negative result, and is honest about it.

---

## What H4 *cannot* do (proven in Coq)

The four No-Go Theorems in
[`proofs/trinity/NoGoTheorems.v`](proofs/trinity/NoGoTheorems.v):

| | Statement | What it rules out |
|---|-----------|-------------------|
| **NGT1** | φ^a · π^b · e^c formulas cannot reproduce Λ or Ω_b | Cosmological constant / baryon fraction from this ansatz |
| **NGT2** | No NCG σ-field from H4 root structure alone | A core NCG ingredient cannot be built from H4 |
| **NGT3** | 600-cell D_F is vector-like (antipodal symmetry) | Chiral fermions in the obvious construction |
| **NGT4** | 2I-equivariant D_F cannot reproduce lepton mass ratios | Lepton mass hierarchy in the obvious construction |

These are formal Coq theorems with closing `Qed.`s. They are negative
claims; they do not say "no H4-based theory of anything is possible",
they say "*these specific constructions fail*".

## What H4 *can* do (and what it means)

- **59 numerical matches.** Combinations of φ, π, e and small
  integers reproduce many SM observables (masses, couplings, mixing
  angles) within stated error windows. **These are fits, not
  derivations.** Every such formula is tagged `[phenomenological_fit]`
  or `[NUMERICAL_FIT]`, and the
  [anti-numerology gate](scripts/anti_numerology_gate.py) enforces the
  tagging on every PR. See [`Catalog42_corrected.v`](Catalog42_corrected.v).
- **A large body of real Coq mathematics.** 1 762 `Qed.` theorems
  across 79 `.v` files (count with comments stripped — see
  [`HONESTY_MANIFEST.md`](HONESTY_MANIFEST.md)). Most of these are
  bound checks and structural lemmas; the No-Go theorems are the
  load-bearing physical content.
- **A falsification protocol.** Risky predictions for DUNE, JUNO and
  LHC are listed in [`RISKY_PREDICTIONS.md`](RISKY_PREDICTIONS.md) with
  criteria that would falsify them. The protocol is in
  [`Trinity_Falsifiability_Assessment.md`](Trinity_Falsifiability_Assessment.md).
- **A hypothesis-discovery puzzle, GOLDEN BRIDGE.** Live at
  <https://t27.ai/trinity-s3ai/>. The game scores candidate boards
  against a small curated rule set, surfaces the worst claim status,
  and floors the score if any tile is falsified. It does not prove or
  test any Theory-of-Everything claim, and a high score is not
  evidence. See
  [`games/trinity_fold/README.md`](games/trinity_fold/README.md).

## What this repository does *not* claim

- **No Theory of Everything.** This is the no-overclaim rule of
  [`docs/CLAIM_STATUS.md`](docs/CLAIM_STATUS.md). Any document that
  reads otherwise is a documentation bug; please file an issue.
- **No prize-level recognition.** External validation, if it ever
  happens, is a long-term community process that this repository takes
  no position on.
- **No equivalence between numeric fit and physical derivation.**
  Catalogued fits are catalogued fits.

---

## Where to read next

| For… | Read |
|------|------|
| A 10-minute reviewer path | [`docs/REVIEW_GUIDE.md`](docs/REVIEW_GUIDE.md) |
| The claim-status rule book | [`docs/CLAIM_STATUS.md`](docs/CLAIM_STATUS.md) |
| A layered status of the whole stack | [`docs/TECH_TREE.md`](docs/TECH_TREE.md) |
| A mechanical review checklist | [`docs/REVIEW_CHECKLIST.md`](docs/REVIEW_CHECKLIST.md) |
| Honest Coq statistics | [`HONESTY_MANIFEST.md`](HONESTY_MANIFEST.md) |
| The reconciliation of older metric claims | [`COQ_HONEST_STATUS.md`](COQ_HONEST_STATUS.md) |
| The traceability of figures to scripts | [`TRACEABILITY.md`](TRACEABILITY.md) |
