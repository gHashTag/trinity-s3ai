# Trinity S³AI — H4 Coxeter / Standard Model Boundary Mapping

[![CI](https://github.com/gHashTag/trinity-s3ai/actions/workflows/ci.yml/badge.svg)](https://github.com/gHashTag/trinity-s3ai/actions/workflows/ci.yml)
[![Anti-Numerology Gate](https://img.shields.io/badge/anti--numerology-PASS-brightgreen)](https://github.com/gHashTag/trinity-s3ai/actions/workflows/ci.yml)
[![Coq](https://img.shields.io/badge/Coq-8.20.1-blue)](https://coq.inria.fr)
[![Active Research](https://img.shields.io/badge/active--research-blue)](docs/TECH_TREE.md)
[![DOI](https://img.shields.io/badge/DOI-pending%20Zenodo-lightgrey)](scripts/prepare_zenodo.md)

> [!CAUTION]
> **No Theory-of-Everything claim is made.**
> This repository documents an *active boundary-mapping research program* —
> we prove what H4 geometry **cannot** reproduce, narrowing the search space.

---

## 🎯 Start here based on who you are

| Role | Start here | Time | What you'll learn |
|------|-----------|------|-------------------|
| **Physicist / Reviewer** | [`docs/REVIEW_GUIDE.md`](docs/REVIEW_GUIDE.md) | 10 min | Honest path with commands and expected outputs |
| **Formal methods researcher** | [`proofs/trinity/BoundaryTheorems.v`](proofs/trinity/BoundaryTheorems.v) | 5 min | BT-1..BT-4 Qed, 0 real Admitted in `proofs/trinity/` |
| **Curious visitor** | [🌉 GOLDEN CHAIN live](https://t27.ai/trinity-s3ai/) | 2 min | Interactive hypothesis-discovery puzzle |
| **Contributor** | [`CONTRIBUTING.md`](CONTRIBUTING.md) + [`good first issue`](https://github.com/gHashTag/trinity-s3ai/issues) | 15 min | Build instructions, phi-loop protocol |

---

We maintain a catalog of **59 numerically verified formulas** between H4 Coxeter
invariants and PDG 2024 measurements, plus **4 formal boundary theorems**
proving obstructions. Whether the coincidences are deep or accidental is itself
an open research question — tracked via a 7-layer verification stack and a
living claim ledger.

---

## 📊 Living Status

| Layer | Status | Key Metric | Details |
|-------|--------|------------|---------|
| L0 Infrastructure | ✅ | [Live demo](https://t27.ai/trinity-s3ai/) | Rust + Coq CI, anti-numerology gate |
| L1 Claim Ledger | ✅ | SSOT `claims.yaml` | 5-status vocabulary enforced |
| L2 Formal Proofs | ✅ | **0 real Admitted** | `proofs/trinity/` only; Track B has 4 cited Axioms |
| L3 Geometry | ⚠️ | `a₄` factor unresolved | 3 derivations don't converge |
| L4 NCG / Lagrangian | 🔴 | BT-2, BT-6 bound recovery | No σ-field from H4; no string rescue |
| L5 Numerical Fits | ⚠️ | 59 formulas, 1 withdrawn | δ_CP withdrawn; sin²θ_W = 84σ genuine failure |
| L6 GOLDEN CHAIN | ✅ | Rust + wasm deployed | 5-ring Cargo workspace |
| L7 Publication | 🔄 | Paper v2 in prep | arXiv + Zenodo pipeline |

---

## 🏗️ Verification Stack

```mermaid
flowchart BT
    L7[📄 L7 Publication<br/>paper v2 / arXiv / Zenodo] --> L6
    L6[🎮 L6 GOLDEN CHAIN<br/>hypothesis puzzle] --> L5
    L5[📐 L5 Numerical Fits<br/>59 formulas, p-values] --> L4
    L4[🔬 L4 NCG / Lagrangian<br/>spectral action] --> L3
    L3[📐 L3 Geometry<br/>H4 / 600-cell / Cl(8)] --> L2
    L2[✅ L2 Formal Proofs<br/>Coq / Lean, BT-1..BT-4] --> L1
    L1[📋 L1 Claim Ledger<br/>5-status SSOT] --> L0
    L0[⚙️ L0 Infrastructure<br/>CI, honest counter, Pages]

    style L2 fill:#90EE90,stroke:#333
    style L5 fill:#FFD700,stroke:#333
    style L4 fill:#FF6B6B,stroke:#333
    style L3 fill:#FFD700,stroke:#333
```

---

## 🏆 Boundary Results (formally verified)

| Theorem | Statement | Status |
|---------|-----------|--------|
| **BT-1** | φᵃ πᵇ eᶜ formulas cannot reproduce Λ or Ω_b | ✅ Qed |
| **BT-2** | No NCG σ-field from H4 root structure alone | ✅ Qed |
| **BT-3** | 600-cell D_F is vector-like (antipodal symmetry) | ✅ Qed |
| **BT-4** | 2I-equivariant D_F cannot reproduce lepton mass ratios | ✅ Qed |

**Coq Stats (Wave 23):** 1,762 Qed · 0 real Admitted (`proofs/trinity/`) · 14 refutation theorems  
**Honest p-value:** p = 0.077 (mean error, not significant) · p < 0.0001 (SG-hit density, significant)

> *"Not a proof is also a proof."* — We share what we tried to prove and could not,
> because knowing the boundary is as valuable as knowing the path.

---

## 🚀 Quick Start

```bash
# Docker (zero dependencies)
docker run -it --rm -v $(pwd):/work coqorg/coq:8.20.1 bash -c \
  "cd /work/proofs/trinity && coq_makefile -f _CoqProject -o Makefile.coq && make -f Makefile.coq -j$(nproc)"

# Validators
pip install mpmath numpy
python3 scripts/validators/validate_v4.py
python3 scripts/anti_numerology_gate.py
python3 scripts/count_admitted_honest.py
```

Full build matrix: [`docs/BUILD.md`](docs/BUILD.md) · Contributing: [`CONTRIBUTING.md`](CONTRIBUTING.md)

---

## 📚 Citation

```bibtex
@software{trinity_s3ai_2026,
  title  = {Trinity-s3ai: Active Boundary-Mapping Research Program},
  author = {Dmitrii Vasilev},
  year   = {2026},
  url    = {https://github.com/gHashTag/trinity-s3ai},
  note   = {v1.0-wave23}
}
```

See [`CITATION.cff`](CITATION.cff) for metadata. Zenodo DOI badge pending deposit.

---

<details>
<summary>🔍 Full Claim Ledger (auto-generated from <code>claims.yaml</code>)</summary>

<!-- CLAIMS_TABLE:START -->

_Generated from [`docs/claims.yaml`](docs/claims.yaml) by [`scripts/generate_claims.py`](scripts/generate_claims.py). Do not edit this block by hand._

| Claim | Layer | Status | Evidence | Blocking gap |
|-------|-------|--------|----------|--------------|
| GOLDEN CHAIN live canvas deployed on GitHub Pages (Rust + wasm) | L0 | `verified` | .github/workflows/pages.yml; live at https://t27.ai/trinity-s3ai/ | — |
| Wave 17 honest counter reports 0 real `Admitted.` in proofs/trinity/ | L2 | `verified` | scripts/count_admitted_honest.py output; HONESTY_MANIFEST.md | Holds only for proofs/trinity/. Track B (proofs/clifford_cl8/) retains load-bearing Axioms with citations; the Lagrangian derivation is not closed. |
| BT-1–BT-4: four formal Boundary theorems closed with `Qed.` | L2 | `verified` | proofs/trinity/BoundaryTheorems.v (BT1, BT2, BT3, BT4 all Qed) | — |
| E8 plumbing: eta discrepancy does NOT converge to -2 | L4 | `high_risk_or_falsified` | paper/CHANGELOG_v1_to_v2.md (Honesty Notes); Wave 17 audit | — |
| No known string / heterotic / F-theory / orbifold compactification rescues the SM hierarchy from H4 or F4 | L4 | `high_risk_or_falsified` | ROADMAP_WAVE17_PLUS.md (Wave 17.2 Findings) | — |
| `a4` conversion factor not fully reconciled across three derivations | L3 | `open_conjecture` | docs/analysis/a4_conversion_factor_analysis.md; docs/analysis/a4_honest_resolution.md | Produce a single derivation that all three (analytic, spectral, fit) paths agree on, or document why they cannot agree and downgrade the relevant fits. |
| `m_H = 4 phi^3 e^2 ~ 125.1 GeV` is the Higgs mass | L5 | `empirical_fit` | proofs/trinity/HiggsPrediction.v (interval bound); docs/analysis/higgs_potential_proven.md | Derive m_H from H4 / NCG structure rather than from a (phi, e) monomial. Any such derivation must pass the anti-numerology gate and avoid the BT2 sigma-field boundary. |
| GOLDEN CHAIN puzzle is a hardware-verified proof chain, not evidence | L6 | `verified` | games/trinity_fold/README.md; ring0_core::ClaimStatus enum | — |
| No Theory-of-Everything claim and no prize claim is made | L1 | `verified` | docs/CLAIM_STATUS.md §2; README.md preamble | — |

<!-- CLAIMS_TABLE:END -->

To update: edit `docs/claims.yaml`, run `python3 scripts/generate_claims.py`,
commit both the YAML and the regenerated artefacts. CI runs the same
script with `--check` and fails if anything is stale.

</details>

<details>
<summary>🌊 Wave History</summary>

| Wave | Key addition |
|------|-------------|
| 1–3 | Initial φ/π/e formula catalog |
| 4.1 | Honesty tags: `[phenomenological_fit]`, `[NUMERICAL_FIT]` added |
| 5–8 | NCG derivations, spectral action |
| 9.6 | BT-1–BT-4 boundary theorems formalized |
| 10.5 | Anti-numerology CI gate; CITATION.cff; CONTRIBUTING.md |
| 12 | Track B launch: Cl(p,q) formalization (T1–T3) |
| 15.1 | Honest counting system: comments stripped before statistics |
| 17 | Formal retraction of δ_CP = 65.66° (5.6σ excluded); 0 real `Admitted.` in proofs/trinity/ |
| 18 | Merge of honesty-pass PRs #21–#23 (Lagrangian status, δ_CP withdrawal, Coq audit) |
| 19 | Merge of honesty-pass PRs #29, #31, #32 (calculation-primacy, N_gen=3 withdrawn, Strong CP withdrawn); all old PRs merged |
| 20 | Honest phenomenology refresh: 500k-trial p-value, σ-ranking updated (26 obs, δ_CP withdrawn, sin²θ_13/23/W + \|V_ub\| + λ added) |
| 23 | README redesign: lean structure, audience selector, Mermaid tech tree, collapsible ledger |

</details>

---

## 🔗 Quick Links

| Resource | Description |
|----------|-------------|
| [`docs/REVIEW_GUIDE.md`](docs/REVIEW_GUIDE.md) | **For reviewers:** 10-minute path with commands and expected outputs |
| [`docs/REPOSITORY_MAP.md`](docs/REPOSITORY_MAP.md) | Where every kind of artifact lives |
| [`docs/CLAIM_STATUS.md`](docs/CLAIM_STATUS.md) | Claim-status rule book (5 canonical statuses) |
| [`docs/TECH_TREE.md`](docs/TECH_TREE.md) | Layered status of the whole stack |
| [`RESEARCH_STATUS.md`](RESEARCH_STATUS.md) | Boundary map: open, obstructed, or under exploration |
| [`HONESTY_MANIFEST.md`](HONESTY_MANIFEST.md) | **Ground-truth statistics** (comments stripped) |
| [`ROADMAP_WAVE17_PLUS.md`](ROADMAP_WAVE17_PLUS.md) | Tracks A, B, C of active research |
| [`paper/CHANGELOG_v1_to_v2.md`](paper/CHANGELOG_v1_to_v2.md) | Paper v2 changelog — new boundary notes |
| [`SECURITY.md`](SECURITY.md) | Security policy and reporting path |
| [`docs/BUILD.md`](docs/BUILD.md) | Full build matrix (Coq, Rust, Python) |
