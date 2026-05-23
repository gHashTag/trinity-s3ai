# Trinity S3AI — H4 Coxeter Group / Standard Model Unification

[![CI](https://github.com/gHashTag/trinity-s3ai/actions/workflows/ci.yml/badge.svg)](https://github.com/gHashTag/trinity-s3ai/actions/workflows/ci.yml)
[![Anti-Numerology Gate](https://img.shields.io/badge/anti--numerology-PASS-brightgreen)](https://github.com/gHashTag/trinity-s3ai/actions/workflows/ci.yml)
[![Coq](https://img.shields.io/badge/Coq-8.20.1-blue)](https://coq.inria.fr)
[![DOI](https://img.shields.io/badge/DOI-pending%20Zenodo-lightgrey)](scripts/prepare_zenodo.md)

---


## English

### Status

> **This is a constructive negative result. See [SALVAGE.md](SALVAGE.md).**

This repository contains formal Coq proofs investigating whether the H4 Coxeter group geometry (and its associated 600-cell polytope) can serve as the basis for a noncommutative geometry model of the Standard Model of particle physics.

**The answer is NO** — four formal No-Go Theorems prove specific structural impossibilities.

What is preserved (the "salvage") is a catalog of 59 numerological coincidences between H4 invariants and PDG 2024 measurements, all formally verified as interval bounds in Coq and explicitly tagged as phenomenological fits.

### Quick Links

| Resource | Description |
|----------|-------------|
| [docs/REVIEW_GUIDE.md](docs/REVIEW_GUIDE.md) | **For reviewers:** 10-minute path with commands and expected outputs |
| [docs/CLAIM_STATUS.md](docs/CLAIM_STATUS.md) | Claim-status rule book (verified / empirical fit / open / refuted) |
| [docs/TECH_TREE.md](docs/TECH_TREE.md) | Layered status of the whole stack (infra → proofs → fits → game → paper) |
| [docs/REVIEW_CHECKLIST.md](docs/REVIEW_CHECKLIST.md) | Mechanical review-readiness checklist |
| [SALVAGE.md](SALVAGE.md) | Honest summary: what H4 can/cannot do |
| [ROADMAP_WAVE17_PLUS.md](ROADMAP_WAVE17_PLUS.md) | **Post-Wave-17 program**: Tracks A (honest phenomenology), B (Cl(8) / J3(O)), C (negative-result paper) |
| [paper/CHANGELOG_v1_to_v2.md](paper/CHANGELOG_v1_to_v2.md) | Wave 17 paper v2 changelog — new No-Go NGT-7, updated counters, E8-plumbing / string-correspondence honesty notes |
| [SECURITY.md](SECURITY.md) | Security policy and reporting path |
| [HONESTY_MANIFEST.md](HONESTY_MANIFEST.md) | **Ground-truth statistics** (comments stripped) |
| [NoGoTheorems.v](proofs/trinity/NoGoTheorems.v) | Formal no-go theorems NGT1–NGT4 |
| [Catalog42.v](proofs/trinity/Catalog42.v) | 42 SM parameter formulas (tagged phenomenological) |
| [admitted_log.md](admitted_log.md) | Log of all Admitted with their tags |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution rules + build instructions |
| [scripts/prepare_zenodo.md](scripts/prepare_zenodo.md) | Zenodo publication guide |
| [proofs/trinity/FOUNDATIONS.md](proofs/trinity/FOUNDATIONS.md) | Axiom stratification and open assumptions |
| [proofs/clifford_cl8/README.md](proofs/clifford_cl8/README.md) | **Track B (Wave 12)** — Cl(p,q) formalization launch (T1–T3) |
| [GOLDEN BRIDGE (live)](https://t27.ai/trinity-s3ai/) | Live hypothesis-discovery puzzle (not evidence; see game README) |

> **For external reviewers:** start with
> [`docs/REVIEW_GUIDE.md`](docs/REVIEW_GUIDE.md). It lists what to read,
> what commands to run, and how to judge each kind of claim against
> [`docs/CLAIM_STATUS.md`](docs/CLAIM_STATUS.md). The live GOLDEN BRIDGE
> canvas is at <https://t27.ai/trinity-s3ai/>; CI status is shown by the
> badges at the top of this file. Known blind spots and proof debt are
> tracked in [`docs/TECH_TREE.md`](docs/TECH_TREE.md). **No Theory-of-
> Everything claim and no prize claim is made.**

---

## Track B — Cl(p,q) formalization (Wave 12 launch)

Following the no-go results on the H4/600-cell side, Wave 12 launches a
parallel **Track B** investigating Cl(8) / J3(O) / triality as an
alternative basis for the three-generations question (per
`outputs/B_program_T1_T12.md`).

The new directory [`proofs/clifford_cl8/`](proofs/clifford_cl8/) introduces:

- **T1** — definition of Cl(p,q) via universal property
  (`CliffordAlgebra.v`) — *mostly Qed*
- **T2** — statement of Cl(0,6) ≅ M_8(R) ⊕ M_8(R) (`Cl6_iso_M8R.v`) —
  *stated, Admitted with citation* (Lounesto 2001 Table 16.3, Wieser-Song
  2022 §6, arXiv:2110.03551)
- **T3** — statement of Bott 8-periodicity Cl(n+8) ≅ Cl(n) ⊗ Cl(8)
  (`Cl8_periodicity.v`) — *stated, Admitted with citation*
  (Atiyah-Bott-Shapiro 1964 Table 3, Lawson-Michelsohn 1989 Prop. I.4.1)

Track B is intentionally decoupled from the H4 core (no `Trinity` imports);
its Admitted set is logged separately as `TRACK_B_CLIFFORD` in
[admitted_log.md](admitted_log.md). The launch PR provides the scaffolding
and statement-level theorems; T4–T12 and the Admitted discharges are
follow-up work.

---

## Trinity Fold — hypothesis-discovery puzzle prototype

[`games/trinity_fold/`](games/trinity_fold/) is a small, opt-in puzzle
prototype inspired by FoldIt, AlphaFold's Evoformer two-tower split, and
CASP-style held-out benchmarking. It scores candidate boards built from
theory tiles (constants, symmetries, geometry blocks, fields, constraints,
observables) against a fixed catalog and surfaces the **worst** claim
status across all active tiles. **It does not prove or test any Theory of
Everything claim.** Every tile carries a `ClaimStatus`
(`verified` / `empirical_fit` / `open_conjecture` /
`high_risk_or_falsified` / `unverified`), and boards containing
falsified tiles are floored at a negative total. See
[`games/trinity_fold/README.md`](games/trinity_fold/README.md) for the
honesty policy and scoring spec.

The prototype is fully decoupled from the Coq proofs and from the
`anti_numerology_check` CI gate; it lives in its own Rust **Cargo
workspace** (five ring crates: `ring0_core` ← `ring1_constraints` ←
`ring2_search` ← `ring3_adapters` ← `app`) so a broken game build never
blocks proof work and so each layer can be audited independently. The
inward-only dependency direction is enforced by integration tests in
`games/trinity_fold/crates/app/tests/ring_boundaries.rs`.

---

## The Four No-Go Theorems

| Theorem | Statement | File |
|---------|-----------|------|
| **NGT1** (Cosmology) | φ^a π^b e^c formulas cannot reproduce Λ or Ω_b | NoGoTheorems.v |
| **NGT2** (σ-field) | No NCG σ-field from H4 root structure alone | NoGoTheorems.v |
| **NGT3** (Chirality) | 600-cell D_F is vector-like (antipodal symmetry) | NoGoTheorems.v |
| **NGT4** (Mass hierarchy) | 2I-equivariant D_F cannot reproduce lepton mass ratios | NoGoTheorems.v |

---

## Coq Proof Statistics (Wave 15.1 — Honest Audit)

| Metric | Value |
|--------|-------|
| Coq version | 8.20.1 |
| Coq `.v` files (proofs + derivations) | **79** |
| `Qed.` theorems | **1 762** |
| Real `Admitted.` (outside comments/strings) | **5** |
| `Axiom` + `Conjecture` + `Parameter` | **85** |
| Refutation theorems | **14** |
| SG-class formulas (error < 0.01 %) | 11 |
| V-class formulas (error 0.01–0.3 %) | 14 |
| Anti-numerology gate | ✓ PASS (59 formulas tagged) |
| Honest-count script | [`scripts/count_admitted_honest.py`](scripts/count_admitted_honest.py) |

> **Audit note (Wave 15.1):** Prior counts mixed comment text with real proof
> obligations. A naive `grep -c "Admitted"` finds **77** matches in
> `proofs/trinity/`, but **all 77 are inside historical comments** (tags,
> TODOs, cross-references). The honest parser strips comments and strings
> before counting.  The result: `proofs/trinity/` has **0** real `Admitted.`,
> `proofs/clifford_cl8/` has **4**, and `derivations/chirality/` has **1**.
> Full methodology and commitment are in [HONESTY_MANIFEST.md](HONESTY_MANIFEST.md).
> All 5 open gaps are documented with citations or `[OPEN_PROBLEM]` labels.

---

## Build Instructions

### Prerequisites

- Coq 8.20.1
- opam (OCaml package manager)
- coq-interval, coq-coquelicot (Coq libraries)

### Local build

```bash
# Install dependencies (first time only)
opam repo add coq-released https://coq.inria.fr/opam/released
opam install coq.8.20.1 coq-interval coq-coquelicot

# Build
cd proofs/trinity
coq_makefile -f _CoqProject -o Makefile.coq
make -f Makefile.coq -j$(nproc)
```

### Docker

```bash
docker run -it --rm -v $(pwd):/work coqorg/coq:8.20.1-ocaml-4.14-flambda bash
cd /work/proofs/trinity
coq_makefile -f _CoqProject -o Makefile.coq
make -f Makefile.coq -j4
```

### Python validators

```bash
pip install mpmath numpy
python3 validate_v4.py                        # formula error bounds
python3 scripts/anti_numerology_gate.py       # honesty check
```

---

## Repository Structure

```
proofs/trinity/              — Coq .v source files (50 files)
  CorePhi.v                  — Golden ratio φ and its algebra
  Catalog42.v                — 42 SM parameter formulas [phenomenological_fit]
  NoGoTheorems.v             — NGT1–NGT4 formal no-go theorems
  HiggsPrediction.v          — Higgs mass formulas [phenomenological_fit]
  CosmologyOrigins.v         — Cosmological formulas [HONEST: ...]
  ...
scripts/
  count_admitted_honest.py   — Honest parser: strips comments before counting
  anti_numerology_gate.py    — CI gate: detect untagged φ/π/e formulas
  README_anti_numerology.md  — Gate documentation
  prepare_zenodo.md          — Zenodo publication guide
.github/
  workflows/ci.yml           — CI: anti_numerology_check → build
  workflows/release.yml      — Release: coq bundle + PDF
  PULL_REQUEST_TEMPLATE.md   — Enforces "verified/open" PR section
SALVAGE.md                   — Honest summary of results
CITATION.cff                 — Citation metadata (Zenodo)
CONTRIBUTING.md              — Contribution rules (Russian + English)
```

---

## Honesty Statement

The 59 formulas in `Catalog42.v` and related files match Standard Model parameters to <0.01% precision using combinations of φ, π, and e. **This is a catalog of numerical coincidences, not a physical theory.** The No-Go theorems prove that these coincidences cannot be elevated to a consistent NCG model of the Standard Model.

Every formula is tagged with `[phenomenological_fit]` and is automatically checked by the anti-numerology CI gate (`scripts/anti_numerology_gate.py`). Any new formula without an approved honesty tag will be rejected by CI.

---

## Citation

See [CITATION.cff](CITATION.cff) for citation metadata.

After Zenodo deposit, the DOI badge above will be updated. For now, cite the GitHub repository:

```bibtex
@software{trinity_s3ai_2026,
  title  = {Trinity-s3ai: A Constructive Negative Result on H4-Based Standard Model Unification},
  author = {[Author Name]},
  year   = {2026},
  url    = {https://github.com/gHashTag/trinity-s3ai},
  note   = {Version v1.0-wave10}
}
```

Also see [CITATION.bib](CITATION.bib) for formatted references.

---

## Wave History

| Wave | Key addition |
|------|-------------|
| 1–3 | Initial φ/π/e formula catalog |
| 4.1 | Honesty tags: `[phenomenological_fit]`, `[NUMERICAL_FIT]` added |
| 5–8 | NCG derivations, spectral action |
| 9.6 | NGT1–NGT4 no-go theorems formalized |
| 10.5 | Anti-numerology CI gate; CITATION.cff; CONTRIBUTING.md |
| 15.1 | Honest counting system: comments stripped before statistics |
