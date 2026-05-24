# Reviewer Guide — Trinity S3AI

A 10-minute path for an external scientific or engineering reviewer to
get oriented, run the artifacts, and judge the claims without having to
read the full repository.

This guide is intentionally short. It points to the documents that
hold the detail and tells you in what order to read them.

> **One-line framing.** Trinity S3AI is a *constructive negative
> result* on whether H4 / 600-cell geometry (and, in Wave 17, the
> broader F4 / E8 / string-correspondence neighbourhood) can support a
> noncommutative geometry (NCG) model of the Standard Model. Four
> Coq-formal Boundary Theorems (BT-1–BT-4) and additional paper-level
> Boundary results (BT-5..7, see `paper/CHANGELOG_v1_to_v2.md`) prove or
> document specific impossibilities. The remaining content is a
> catalogue of numerological coincidences, all *explicitly tagged as
> phenomenological fits*, not derivations. We make no Theory-of-
> Everything claim and no prize claim. See
> [`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md) for how each claim is
> labelled, and [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md)
> for Tracks A / B / C of the post-Wave-17 program.

---

## 1. The 10-minute path

| # | Step | Time | Action |
|---|------|------|--------|
| 1 | Read this section | 1 min | You are here. |
| 2 | Read [`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md) and the README claim table | 2 min | The claim ledger: what is verified, what is a fit, what is open, what is refuted. The README table is auto-generated from [`docs/claims.yaml`](claims.yaml). |
| 3 | Skim [`HONESTY_MANIFEST.md`](../HONESTY_MANIFEST.md) | 1 min | Ground-truth Coq statistics with comments stripped. |
| 4 | Skim the [Obstruction Theorems](../proofs/trinity/BoundaryTheorems.v) | 2 min | The four Coq-formal impossibility results BT-1–BT-4 (Qed). Additional Boundary results BT-5..7 are documented at paper level in [`paper/CHANGELOG_v1_to_v2.md`](../paper/CHANGELOG_v1_to_v2.md). |
| 5 | Open the live GOLDEN BRIDGE canvas | 1 min | <https://t27.ai/trinity-s3ai/> — a hypothesis-discovery puzzle, **not** evidence. |
| 6 | Read [`docs/TECH_TREE.md`](TECH_TREE.md) | 2 min | Layered status: infra → claim ledger → proofs → geometry → fits → game → paper. |
| 7 | Use the [Review Checklist](REVIEW_CHECKLIST.md) | 1 min | Tick off install/run/tests/no-secrets/no-hype/reproducibility. |

If you only have 3 minutes, read steps 2, 3, and 5 and stop.

---

## 2. What to read first, by reviewer profile

**Formal-methods reviewer (Coq / Lean).** Start with
[`HONESTY_MANIFEST.md`](../HONESTY_MANIFEST.md) for the honest counter
methodology, then
[`COQ_HONEST_STATUS.md`](status/COQ_HONEST_STATUS.md) for the canonical
reconciliation across older docs, then
[`proofs/trinity/BoundaryTheorems.v`](../proofs/trinity/BoundaryTheorems.v) and
[`admitted_log.md`](analysis/admitted_log.md).

**Physics / phenomenology reviewer.** Start with
[`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md), then
[`Trinity_Falsifiability_Assessment.md`](analysis/Trinity_Falsifiability_Assessment.md),
[`RISKY_PREDICTIONS.md`](analysis/RISKY_PREDICTIONS.md), and
[`TRACEABILITY.md`](analysis/TRACEABILITY.md) for formula → script → figure
chains.

**Software / open-source reviewer.** Start with the root
[`README.md`](../README.md), then this guide, then
[`SECURITY.md`](../SECURITY.md), [`CONTRIBUTING.md`](../CONTRIBUTING.md),
and the CI workflows under
[`.github/workflows/`](../.github/workflows/).

**Engineering / Rust reviewer.** Start with
[`trinity_rust/README.md`](../trinity_rust/README.md) and
[`games/trinity_fold/README.md`](../games/trinity_fold/README.md), then
look at the ring-boundary integration tests in
`games/trinity_fold/crates/app/tests/ring_boundaries.rs`.

---

## 3. Commands a reviewer can run

All commands are read-only from the repository's perspective: they build,
test, or validate; they do not push, deploy, or modify external state.
None of them require any secret or token.

### 3.1 Anti-numerology gate (fastest sanity check, ~5 s)

```bash
python3 scripts/anti_numerology_gate.py
```

**Expected:** exit code `0`, summary line ending in `VERDICT: PASS`.
This is the same gate that runs as the first CI job. It flags any
multi-atom φ/π/e formula that is not honesty-tagged.

### 3.2 Honest Coq counter (~2 s)

```bash
python3 scripts/count_admitted_honest.py
```

**Expected:** a table of per-directory counts plus a JSON block.
Reviewers should compare its numbers with anything quoted in the README
or the paper. The script strips Coq comments before counting, which is
why naive `grep -c "Admitted"` gives a much larger number.

### 3.3 Formula error bounds (~10 s, needs `mpmath` + `numpy`)

```bash
pip install mpmath numpy
python3 scripts/validators/validate_v4.py
```

**Expected:** a list of formulas with their numeric error vs PDG values.
These are *fits*, not derivations; the script verifies the error claims.

### 3.4 GOLDEN BRIDGE prototype (~30 s, needs Rust toolchain)

```bash
cd games/trinity_fold
cargo test --workspace
```

**Expected:** all tests pass, including the ring-boundary tests that
enforce the inward-only dependency direction
(`ring0_core` ← `ring1_constraints` ← `ring2_search` ← `ring3_adapters` ← `app`).

The live deployed canvas — built from `ring4_canvas` and published by
the [`pages.yml`](../.github/workflows/pages.yml) workflow — is at:

> **<https://t27.ai/trinity-s3ai/>**

The game **does not prove** any Theory-of-Everything claim. It is a
hypothesis-discovery puzzle with a `ClaimStatus` on every tile and a
falsification floor; a high score is not evidence. See
[`games/trinity_fold/docs/GOLDEN_BRIDGE.md`](../games/trinity_fold/docs/GOLDEN_BRIDGE.md)
for the full honesty policy.

### 3.5 Full Coq proofs (~10 min, requires Coq 8.20.1 + libraries)

This is the slow path and is **not** required for a first-pass review.
Use the published CI logs unless you have reason to recheck locally.

```bash
opam repo add coq-released https://coq.inria.fr/opam/released
opam install coq.8.20.1 coq-interval coq-coquelicot
cd proofs/trinity
coq_makefile -f _CoqProject -o Makefile.coq
make -f Makefile.coq -j$(nproc)
```

Or use the published Coq Docker image as documented in
[`CONTRIBUTING.md`](../CONTRIBUTING.md#5-build-instructions-coq-8201).

---

## 4. CI and continuous evidence

| Workflow | What it gates | File |
|----------|---------------|------|
| `ci.yml` | Anti-numerology gate, then Coq build, then Python validators | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) |
| `rust.yml` | Rust formatter, clippy, tests for `trinity_rust/` and the game workspace | [`.github/workflows/rust.yml`](../.github/workflows/rust.yml) |
| `pages.yml` | Builds and deploys the GOLDEN BRIDGE canvas to GitHub Pages | [`.github/workflows/pages.yml`](../.github/workflows/pages.yml) |
| `lean.yml` | Lean 4 (Mathlib) auxiliary proof PRs | [`.github/workflows/lean.yml`](../.github/workflows/lean.yml) |
| `release.yml` | Builds the release bundle (Coq + PDF) | [`.github/workflows/release.yml`](../.github/workflows/release.yml) |

The status of the most recent runs is reflected by the badges at the
top of the [root README](../README.md).

> **Known state at the Wave 17 baseline (commit `0832b72`).**
> The `CI` (Anti-Numerology Gate + Coq build + Python validators) and
> `pages.yml` workflows are green. The `lean.yml` Lean 4 build is
> currently **red** on `main` due to pre-existing issues in
> `TrinityLean/H4RootSystem.lean` (parse error) and
> `TrinityLean/Snub24Z3.lean` (Mathlib `maxRecDepth` / synthesis
> issues). These are out of scope for the present review-readiness PR
> (which is docs-only and does not touch Lean) and are tracked as
> follow-up work in [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md).
> Reviewers should evaluate the Coq side and the docs / claim ledger
> independently of this Lean breakage.

---

## 5. How to judge the claims

This is the part reviewers ask about most. Use the rules below; the
ledger in [`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md) labels every
public-facing claim against them.

1. **A "Qed" in Coq is a proof, not a physical claim.** A theorem
   `m_H_in_interval` proves that a *numeric expression* lies in a
   *numeric interval*; it does not prove that the expression is
   physically derived from H4. Check the surrounding comments and the
   `[phenomenological_fit]` or `[NUMERICAL_FIT]` tag.
2. **An `Admitted` is a gap.** As of Wave 17 the honest, comment-
   stripped count produced by `scripts/count_admitted_honest.py` is
   **0 real `Admitted.`** across the canonical Coq tree (see
   [`HONESTY_MANIFEST.md`](../HONESTY_MANIFEST.md) and the script's
   table). All historical occurrences of "Admitted" in `proofs/trinity/`
   are inside comments. Any new `Admitted.` introduced in a PR must
   have a citation or `[OPEN_PROBLEM]` label in
   [`admitted_log.md`](analysis/admitted_log.md).
3. **Empirical fit ≠ derivation.** Any formula combining ≥2 of {φ, π, e,
   √n} that matches a PDG value is, by repository policy, a
   phenomenological fit unless explicitly proved otherwise. The
   anti-numerology gate enforces this for new code.
4. **A Boundary theorem is a negative claim with a formal proof.** The
   four Coq-formal Boundary theorems BT-1–BT-4 in
   [`proofs/trinity/BoundaryTheorems.v`](../proofs/trinity/BoundaryTheorems.v)
   close with `Qed.` and rule out specific constructions
   (cosmology ansatz; σ-field from H4; chirality on the 600-cell;
   mass hierarchy from 2I-equivariant D_F). They are not omnibus
   impossibility claims for "any H4-based theory"; read the
   statement. Additional Wave 11–17 Boundary results — BT-5 (D₄/24-cell),
   BT-6 (no σ-field under string/orbifold rescue), BT-7 (F₄
   3-generation hierarchy) — are documented at paper / analysis
   level (see [`paper/CHANGELOG_v1_to_v2.md`](../paper/CHANGELOG_v1_to_v2.md)
   and [`ROADMAP.md`](../ROADMAP.md)).
5. **The GOLDEN BRIDGE game is not evidence.** A high "bridge strength"
   says nothing about the underlying physics. If any tile is
   `HighRiskOrFalsified`, the bridge collapses by design.
6. **No prize claims.** This project takes no position on prize-level
   recognition. External validation, if it ever happens, is a long-term
   community process. Any document that frames a result as
   "Nobel-worthy" or similar is a documentation bug; please file an
   issue.

---

## 6. Known blind spots

These are the failure modes a reviewer should look for, listed here so
they are easy to find rather than hidden in long appendices.

- **Numerical fits dressed as derivations.** The repository contains
  many `Definition`s of the form `phi^a * pi^b * exp 1 / N`. They are
  required to be tagged, but tagging is a social commitment, not a
  proof; the anti-numerology gate is the mechanical check.
- **Inconsistent older counts.**
  [`COQ_HONEST_STATUS.md`](status/COQ_HONEST_STATUS.md) catalogues five
  mutually inconsistent sets of Coq metrics across older documents. The
  canonical numbers are produced by
  `scripts/count_admitted_honest.py`; treat anything else as historical.
- **Track B (Cl(8))** is a parallel exploration. As of Wave 17 the
  Coq-formal status reported by `count_admitted_honest.py` is 0 real
  `Admitted.` in `proofs/clifford_cl8/`, but the substantive Cl(0,6)
  and Bott-8 theorems are stated as `Axiom` with published citations
  (Lounesto 2001, Wieser–Song 2022, Atiyah–Bott–Shapiro 1964,
  Lawson–Michelsohn 1989). Reviewers should treat these as
  *citation-backed assumptions*, not yet as in-tree proofs.
- **Chirality.** `derivations/chirality/ChiralityAnalysis.v` is the
  reference for the chirality Boundary Theorem (BT-3); the comment-stripped
  honest counter reports 0 real `Admitted.` there in Wave 17.
- **E8 plumbing.** The Wave 17 paper / changelog report that the
  E8-plumbing η discrepancy does **not** converge to −2 and that the
  underlying B-matrix is a heuristic, not a rigorous derivation
  (see [`paper/CHANGELOG_v1_to_v2.md`](../paper/CHANGELOG_v1_to_v2.md)
  "Honesty Notes"). Treat E8 plumbing as **open_conjecture /
  high_risk** until that gap closes.
- **String / orbifold rescue.** Wave 17.2 found that no known string
  compactification predicts H4 / F4 and that toy Z₂ orbifold projection
  improves the Yukawa eigenvalue ratio by ~2×, far short of the ~5000×
  required for the SM hierarchy (see
  [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md) §"Wave 17.2
  Findings"). Treat the string-correspondence layer as
  **high_risk_or_falsified** for the original mass-hierarchy aim.
- **Lagrangian derivations** are work-in-progress; see
  [`LAGRANGIAN_HONEST_STATUS.md`](status/LAGRANGIAN_HONEST_STATUS.md) for
  what is and is not derived.

---

## 7. Wave 17 outcome and next steps

The Wave 17 outcome, in one paragraph: H4, F4 and the immediate E8 /
heterotic / orbifold neighbourhood **do not** rescue the mass-hierarchy
program. The E8-plumbing η discrepancy does not converge to −2; the
string correspondence is too weak to predict H4 or F4; an orbifold Z₂
projection improves the Yukawa eigenvalue ratio by ~2× against a
required ~5000×. See
[`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md) for the detailed
findings.

The post-Wave-17 program has three tracks, none of which claims a
Theory of Everything:

- **Track A — Honest phenomenology.** Treat the catalogued formulas as
  a statistically tested fit, compute an honest p-value, publish a
  data paper.
- **Track B — Cl(8) / J₃(𝕆) / triality.** Continue the parallel
  exploration in `proofs/clifford_cl8/`; the Wave 17 honest counter
  reports 0 real `Admitted.`, with the load-bearing isomorphisms
  retained as cited `Axiom`s. Replace these with in-tree proofs over
  the next waves.
- **Track C — Boundary-result publication.** Submit the Coq-formal
  BT-1–BT-4 plus the paper-level BT-5..7 as a boundary-result paper.
  arXiv submission (`trinity-s3ai-arxiv.tar.gz`) and Zenodo deposit
  (`scripts/prepare_zenodo.md`) are prepared; the seminar talk v2 is
  in [`talks/wave17_talk.tex`](../talks/wave17_talk.tex).

Reviewers can therefore judge the present state as: *boundary-mapping research program,
formally backed in the four BT-1–BT-4 theorems, with the further
Wave 17 negative findings documented but not yet Coq-formalised*. No
claim is upgraded above its honest status, and no Theory-of-Everything
or prize-level claim is made.

---

## 8. If you find a problem

Open a GitHub issue using
[`.github/ISSUE_TEMPLATE.md`](../.github/ISSUE_TEMPLATE.md). Please
include the file path, the line number, and the PDG (or other primary)
source you are comparing to. Corrections to formulas, tags, or
statistics are welcome; cosmetic edits that reduce visible `Admitted`
counts without closing gaps are explicitly out of scope per
[`CONTRIBUTING.md`](../CONTRIBUTING.md).
