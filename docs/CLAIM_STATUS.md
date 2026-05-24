# Claim Status Ledger — Trinity S3AI

This document tells a reviewer, in one place, **what each kind of
public-facing claim means in this repository** and **how to tell which
status a given statement has**. It is the discipline that holds the
rest of the documentation together.

It is intentionally short. The deep audits live in
[`HONESTY_MANIFEST.md`](../HONESTY_MANIFEST.md),
[`COQ_HONEST_STATUS.md`](status/COQ_HONEST_STATUS.md), and
[`admitted_log.md`](analysis/admitted_log.md). This file is the rule book.

---

## 1. The five statuses

Every claim in this repository — every formula, every theorem, every
numeric match, every prediction — is in exactly one of these states.
The same vocabulary is used by the GOLDEN CHAIN puzzle's
`ClaimStatus` enum.

| Status | Meaning | Where it appears in code |
|--------|---------|--------------------------|
| **verified** | Formally proven in Coq (`Qed.`) or in Lean. The statement is mathematical; no claim about physical reality follows automatically. | `Qed.` in `proofs/trinity/*.v` |
| **empirical_fit** | A numeric expression that matches a measured value within a stated error. Not derived from H4 geometry. Tagged `[phenomenological_fit]` or `[NUMERICAL_FIT]`. | Tagged `Definition`s in `Catalog42.v` etc. |
| **open_conjecture** | Stated but not proven; tagged `[MATH_TODO]`, `[LIBRARY_GAP]`, or `[OPEN_PROBLEM]`. | `Admitted.` with tag |
| **high_risk_or_falsified** | Refuted, or so far from data that we list it as falsified. Theorem names end in `_refuted`. | 14 refutation theorems in `proofs/trinity/` |
| **unverified** | The default for anything that has not yet been classified. New content should not stay here. | — |

A claim must never drift upward (e.g., from `empirical_fit` to
`verified`) without a real Coq or Lean proof of the *physical*
derivation, not just of the numeric bound.

---

## 2. The no-overclaim rule

This is the single rule that the rest of the policy is built on.

> **A numeric coincidence is not a derivation.**
> **A Coq `Qed.` on an interval bound is not a physical derivation.**
> **A high score in GOLDEN CHAIN is not evidence.**
> **No statement in this repository constitutes a Theory of Everything.**
> **No statement claims prize-level recognition.**

Concretely:

- Any formula of the form `phi^a * pi^b * exp 1 / N` that matches a PDG
  observable is **empirical_fit**, regardless of how small the error is.
- Theorems like `m_H_in_interval` are **verified** as statements
  about numbers, and at the same time the *underlying physical claim*
  they suggest (that `4 φ³ e²` is the Higgs mass for a structural
  reason) is **open_conjecture** or **high_risk_or_falsified**, ruled
  out for H4 by the Boundary theorems where applicable.
- Documents that describe past hype around prize-level claims are
  retained for transparency but tagged as historical; the canonical
  position of the project is that *no such claim is made*.

If a reviewer finds wording that violates this rule, please file an
issue per [`docs/REVIEW_GUIDE.md`](REVIEW_GUIDE.md) §7.

---

## 3. Derivation vs. fit — how to tell them apart

When reading a Coq file or a markdown derivation, use these checks:

1. **Find the formula's `Definition`.** If it is wrapped in or directly
   preceded by `(* [phenomenological_fit] … *)` or
   `(* [NUMERICAL_FIT] … *)`, it is a fit. End of story.
2. **Find the surrounding theorem.** A theorem
   `name_in_interval : R_lo < formula < R_hi` is a *bound check*. It
   does not establish a derivation; it certifies that the numerical
   value lies in a window.
3. **Find the path to H4.** A real derivation will pass through
   `H4Root`, `H4Subgroup`, a reflection-subgroup chain, an NCG
   spectral triple, or a Clifford algebra. If the right-hand side is a
   bare combination of φ, π, e and small integers with no such path,
   it is a fit.
4. **Look for the corresponding Boundary Theorem.** Where a Boundary theorem applies
   (chirality, lepton mass hierarchy, σ-field, Λ), the matching fit
   *cannot* be a derivation by construction; it is at best a
   phenomenological coincidence within an H4-style ansatz.

The same rule applies to numeric scripts: a `*.py` file that produces a
small error against PDG does not establish derivation; it establishes
that a fit exists.

---

## 4. The headline claims, classified

This table is what most reviewers want to skim. It is the canonical
status for the project's most-referenced statements as of Wave 17.

| Claim | Status | Pointer |
|-------|--------|---------|
| H4 / 600-cell cannot produce a consistent NCG model of the SM (four Coq-formal impossibilities BT-1–BT-4) | **verified** | [`proofs/trinity/BoundaryTheorems.v`](../proofs/trinity/BoundaryTheorems.v) (BT-1–BT-4, all `Qed.`) |
| Additional Wave 11–17 Boundary results: BT-5 (D₄/24-cell), BT-6 (no σ-field under string/orbifold rescue), BT-7 (F₄ cannot produce 3-generation hierarchy) | **verified** (at paper / analysis level — not yet Coq-formalised in `proofs/trinity/BoundaryTheorems.v`) | [`ROADMAP.md`](../ROADMAP.md) §"Boundary theorems", [`paper/CHANGELOG_v1_to_v2.md`](../paper/CHANGELOG_v1_to_v2.md), [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md) |
| 59 numerical matches between H4 invariants and PDG 2024 observables, within stated error windows | **verified** (bound check) + **empirical_fit** (physical reading) | [`Catalog42.v`](../proofs/catalog/Catalog42_corrected.v) |
| `m_H = 4 φ³ e² ≈ 125.1 GeV` is the Higgs mass | **empirical_fit** | `HiggsPrediction.v`, [`higgs_potential_proven.md`](analysis/higgs_potential_proven.md) |
| Koide relation in H4 | **high_risk_or_falsified** | `KoideOrigins.v` (the "Koide ≠ 2/3 in H4" theorem is `Qed.`) |
| H4 chirality fully derived | **open_conjecture** | `derivations/chirality/ChiralityAnalysis.v`; chirality Boundary Theorem is BT-3 (`Qed.`) |
| Cl(0,6) ≅ M₈(R) ⊕ M₈(R); Bott 8-periodicity | **open_conjecture** | `proofs/clifford_cl8/` — Wave 17 honest counter reports 0 real `Admitted.`; load-bearing statements retained as `Axiom` with published citations (Lounesto 2001, Wieser–Song 2022, Atiyah–Bott–Shapiro 1964, Lawson–Michelsohn 1989) |
| Standard Model Lagrangian "derived from H4" | **open_conjecture** with substantial empirical-fit content | [`LAGRANGIAN_HONEST_STATUS.md`](status/LAGRANGIAN_HONEST_STATUS.md) |
| RG running of gauge couplings | **verified** (as a numerical scheme) | `RGRunningExtras.v`, [`RG_RUNNING_PROVEN.md`](analysis/RG_RUNNING_PROVEN.md) |
| E₈ plumbing η discrepancy converges to −2 | **high_risk_or_falsified** — Wave 17 reports the η discrepancy does **not** converge to −2 and that the underlying B-matrix is a heuristic, not a rigorous derivation | [`paper/CHANGELOG_v1_to_v2.md`](../paper/CHANGELOG_v1_to_v2.md) "Honesty Notes" |
| String / heterotic / F-theory / orbifold compactification predicts H4 or F4 and rescues the SM mass hierarchy | **high_risk_or_falsified** — no known string compactification selects H4 or F4; toy Z₂ orbifold improves Yukawa eigenvalue ratio ~2× against required ~5000× | [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md) §"Wave 17.2 Findings" |
| DUNE / JUNO / LHC predictions for δ_CP | **withdrawn** — post-hoc fit excluded at >5σ by NuFIT-6.0 + T2K+NOvA 2025; anti-post-hoc rule enforced | [`DELTA_CP_HONEST_STATUS.md`](DELTA_CP_HONEST_STATUS.md) |
| DUNE / JUNO / LHC predictions for mass ordering, Λ_NP | **risky_prediction** under the project's own typology — treat as **open_conjecture** until data lands | [`RISKY_PREDICTIONS.md`](analysis/RISKY_PREDICTIONS.md), [`DUNE_RISKY_PREDICTION.md`](experiments/DUNE_RISKY_PREDICTION.md) |
| Theory of Everything | **not claimed** | — |
| Nobel-level / prize-worthy claim | **not claimed** | — |

If a public document in this repository contradicts this table, **this
table is the canonical version** and the other document should be
updated. Please file an issue if you find a contradiction.

---

## 4a. Machine-readable ledger

The table in §4 is a human view of the SSOT at
[`docs/claims.yaml`](claims.yaml). The same YAML drives:

- the **README claim table** between `<!-- CLAIMS_TABLE:START -->` /
  `<!-- CLAIMS_TABLE:END -->` markers in [`README.md`](../README.md);
- the **GOLDEN CHAIN generated card data** at
  [`games/trinity_fold/fixtures/generated_claim_cards.json`](../games/trinity_fold/fixtures/generated_claim_cards.json),
  embedded into the wasm build at compile time via `ring3_adapters::embedded_claim_deck`.

To update a claim:

1. Edit `docs/claims.yaml` (one row per claim, see the header comment in
   that file for the schema).
2. Run `python3 scripts/generate_claims.py` to regenerate README + game
   card data.
3. Commit the YAML and both regenerated artefacts in the same PR.

CI runs `python3 scripts/generate_claims.py --check` and fails if the
generated artefacts are stale.

> **No promotion without evidence.** Upgrading a status from
> `empirical_fit` to `verified` (or from `open_conjecture` to
> `verified`) must reference a *physical* derivation, not just a Coq
> interval bound. See §2.

---

## 5. The mechanical checks that back this up

| Check | What it enforces | Command |
|-------|------------------|---------|
| Anti-numerology gate | Every multi-atom φ/π/e formula is tagged | `python3 scripts/anti_numerology_gate.py` |
| Honest counter | Comment-stripped Coq statistics | `python3 scripts/count_admitted_honest.py` |
| Formula bounds | Error windows match what the docs claim | `python3 scripts/validators/validate_v4.py` |
| Coq build | Every advertised `Qed.` actually closes | `cd proofs/trinity && make -f Makefile.coq` |
| GOLDEN CHAIN tests | Ring boundaries hold; falsified tiles floor the score | `cargo test --workspace` in `games/trinity_fold/` |
| Public-docs language | English-only public docs (CONTRIBUTING is bilingual by design) | manual / reviewer check |
| Claim ledger SSOT | YAML parses, statuses/layers/kinds valid, README block and game card JSON match `docs/claims.yaml` | `python3 scripts/generate_claims.py --check` |

If any of these stops working on `main`, the corresponding claim status
is no longer trustworthy and should be downgraded to
`open_conjecture` until the check is restored.
