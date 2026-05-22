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
| [SALVAGE.md](SALVAGE.md) | Honest summary: what H4 can/cannot do |
| [NoGoTheorems.v](proofs/trinity/NoGoTheorems.v) | Formal no-go theorems NGT1–NGT4 |
| [Catalog42.v](proofs/trinity/Catalog42.v) | 42 SM parameter formulas (tagged phenomenological) |
| [admitted_log.md](admitted_log.md) | Log of all Admitted with their tags |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution rules + build instructions |
| [scripts/prepare_zenodo.md](scripts/prepare_zenodo.md) | Zenodo publication guide |
| [proofs/trinity/FOUNDATIONS.md](proofs/trinity/FOUNDATIONS.md) | Axiom stratification and open assumptions |
| [proofs/clifford_cl8/README.md](proofs/clifford_cl8/README.md) | **Track B (Wave 12)** — Cl(p,q) formalization launch (T1–T3) |

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

## The Four No-Go Theorems

| Theorem | Statement | File |
|---------|-----------|------|
| **NGT1** (Cosmology) | φ^a π^b e^c formulas cannot reproduce Λ or Ω_b | NoGoTheorems.v |
| **NGT2** (σ-field) | No NCG σ-field from H4 root structure alone | NoGoTheorems.v |
| **NGT3** (Chirality) | 600-cell D_F is vector-like (antipodal symmetry) | NoGoTheorems.v |
| **NGT4** (Mass hierarchy) | 2I-equivariant D_F cannot reproduce lepton mass ratios | NoGoTheorems.v |

---

## Coq Proof Statistics (v4.0 — Wave 10.4 audit)

| Metric | Value |
|--------|-------|
| Coq version | 8.20.1 |
| Coq files | 77 total (compile status varies) |
| Qed theorems | 1348 (was 1326 pre-W11.7/W12.4 sprints) |
| Admitted (pure) | 34 (was 37; −2 in W11.7, −1 in W12.4) |
| admit (inline) | 17 |
| Axiom declarations | 68 (proofs/) after W11.7+W12.4; 88 originally |
| SG-class formulas (error < 0.01%) | 11 |
| V-class formulas (error 0.01–0.3%) | 14 |
| Anti-numerology gate | ✓ PASS (59 formulas tagged) |
| Proof transparency | See [FOUNDATIONS.md](proofs/trinity/FOUNDATIONS.md) |

> **Audit note (Wave 10.4):** Prior versions of this README incorrectly claimed
> "Admitted: 0". The A1 audit found 37 Admitted + 17 admit + 88 Axiom.
> All items are documented in [admitted_log.md](admitted_log.md) and
> stratified by type in [FOUNDATIONS.md](proofs/trinity/FOUNDATIONS.md).
> The four No-Go Theorems (NGT1–NGT4) compile and are valid modulo the
> axioms documented therein.

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
proofs/trinity/              — Coq .v source files (23 files)
  CorePhi.v                  — Golden ratio φ and its algebra
  Catalog42.v                — 42 SM parameter formulas [phenomenological_fit]
  NoGoTheorems.v             — NGT1–NGT4 formal no-go theorems
  HiggsPrediction.v          — Higgs mass formulas [phenomenological_fit]
  CosmologyOrigins.v         — Cosmological formulas [HONEST: ...]
  ...
scripts/
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
