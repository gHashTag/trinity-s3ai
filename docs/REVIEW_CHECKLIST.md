# Review Checklist — Trinity S3AI

A short, mechanical checklist a reviewer (or a contributor preparing a
release) can run through to confirm review-readiness. Each item is
either a single command, a single file to open, or a single yes/no
question. Nothing on this list requires secrets or external access.

Pair this checklist with [`docs/REVIEW_GUIDE.md`](REVIEW_GUIDE.md)
(the narrative path) and [`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md)
(the rule book).

---

## A. Install and run

- [ ] `python3 --version` reports 3.10 or later.
- [ ] `python3 scripts/anti_numerology_gate.py` exits 0; last line ends with `VERDICT: PASS`.
- [ ] `python3 scripts/count_admitted_honest.py` runs to completion and prints a per-directory table plus a JSON block.
- [ ] `pip install mpmath numpy` succeeds; `python3 scripts/validators/validate_v4.py` runs without unhandled exceptions.
- [ ] (If Rust is available) `cd games/trinity_fold && cargo test --workspace` is green.
- [ ] (If Coq is available) `cd proofs/trinity && coq_makefile -f _CoqProject -o Makefile.coq && make -f Makefile.coq -j$(nproc)` is green. This step is slow and is **not** required for a first-pass review; the CI logs are the canonical evidence.

## B. Tests and CI

- [ ] The `CI` badge in the root README is green on `main`.
- [ ] The `Anti-Numerology Gate` badge is `PASS`.
- [ ] [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) gates Coq build on the anti-numerology job (correct order).
- [ ] [`.github/workflows/pages.yml`](../.github/workflows/pages.yml) deploys `games/trinity_fold/web/canvas`; the canvas is live at <https://t27.ai/trinity-s3ai/>.
- [ ] `python3 scripts/check_markdown_links.py --check --all` exits 0 — no broken internal markdown links and no broken `github.com/gHashTag/trinity-s3ai/blob/...` paths. External HTTP links are intentionally not fetched.

## C. Proof debt

- [ ] [`HONESTY_MANIFEST.md`](../HONESTY_MANIFEST.md) reports the same `Admitted.` count as `python3 scripts/count_admitted_honest.py` does locally.
- [ ] As of Wave 17 (`0832b72`), the comment-stripped real `Admitted.` count is **0** across the canonical Coq tree. Any future `Admitted.` introduced in a PR has either a published citation or an `[OPEN_PROBLEM]` label per [`admitted_log.md`](analysis/admitted_log.md).
- [ ] The Wave 17 honest counter table (run `python3 scripts/count_admitted_honest.py`) shows the load-bearing line **`proofs/trinity/` → 52 files, 1063 `Qed.`+`Def.`, 0 `Admitted.`, 50 `Axiom`s, 11 refutations**, matching the README and paper claims.
- [ ] [`docs/TECH_TREE.md`](TECH_TREE.md) Layer 2 lists the same set of open obligations and notes that NGT-5..7 are paper-level (not yet Coq-formal).
- [ ] No `Admitted.` in Coq code outside the locations enumerated in `HONESTY_MANIFEST.md` §2.
- [ ] The Lean 4 build (`.github/workflows/lean.yml`) is known to be red on `main` as of `0832b72` due to pre-existing issues in `TrinityLean/H4RootSystem.lean` and `TrinityLean/Snub24Z3.lean`; this is tracked as follow-up and is independent of the Coq side.

## D. Claim ledger

- [ ] [`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md) §4 ("headline claims, classified") matches what the README and the paper actually say.
- [ ] No document in the repository claims a Theory of Everything.
- [ ] No document in the repository claims prize-level recognition as a fact. (Historical hype documents, if retained, are clearly framed as historical.)
- [ ] Every multi-atom φ/π/e formula in Coq code is followed by an approved honesty tag, as enforced by `scripts/anti_numerology_gate.py`.
- [ ] [`docs/claims.yaml`](claims.yaml) is the single source of truth for the public claim table and the GOLDEN BRIDGE generated card data; `python3 scripts/generate_claims.py --check` exits 0 (no stale artefacts).

## E. No secrets, no leaks

- [ ] `git grep -niE "(api[_-]?key|password|secret|access[_-]?token)\s*[:=]"` returns nothing that is a real credential. CI permission strings such as `id-token: write` are expected and not secrets.
- [ ] No `.env`, `.envrc`, `id_rsa`, or database connection string is committed.
- [ ] No `S3` bucket name, JWT, or webhook URL appears in tracked files.
- [ ] [`SECURITY.md`](../SECURITY.md) is present and gives a contact path for vulnerability reports.

## F. Public docs are English-only

- [ ] [`README.md`](../README.md), [`docs/REVIEW_GUIDE.md`](REVIEW_GUIDE.md), [`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md), [`docs/TECH_TREE.md`](TECH_TREE.md), [`docs/REVIEW_CHECKLIST.md`](REVIEW_CHECKLIST.md), [`SECURITY.md`](../SECURITY.md), [`HONESTY_MANIFEST.md`](../HONESTY_MANIFEST.md), and [`SALVAGE.md`](../SALVAGE.md) contain no non-English prose.
- [ ] [`ROADMAP.md`](../ROADMAP.md), [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md), [`CONTRIBUTING.md`](../CONTRIBUTING.md), [`FORMULAS.md`](../FORMULAS.md), and [`derivations/formulas_cleanup/PROPOSAL.md`](../derivations/formulas_cleanup/PROPOSAL.md) are English-only. New top-level public docs default to English-only.
- [ ] Run the scan: `bash scripts/check_english_only.sh` exits 0. The script scans top-level public docs (README/SECURITY/HONESTY_MANIFEST/SALVAGE/FORMULAS/ROADMAP*/CONTRIBUTING, all of `docs/`, `.github/`, and `scripts/*.md`) and reports any Cyrillic. Deeper research notes under `derivations/` are out of scope (private research analyses; tracked as a follow-up).

## G. No hype

- [ ] No README or paper text describes any result as a Theory of Everything, "unification achieved", "Nobel-level", or equivalent.
- [ ] The word "derived" is used only where there is an actual derivation (not just a numeric match) — or qualified with "fit" / "ansatz" wording.
- [ ] The GOLDEN BRIDGE game is described as a hypothesis-discovery puzzle, not as evidence.
- [ ] Risky predictions are labelled as such and listed in [`RISKY_PREDICTIONS.md`](analysis/RISKY_PREDICTIONS.md) with falsification criteria.

## H. Reproducibility

- [ ] Every figure in the paper / repository has a script that regenerates it (see [`TRACEABILITY.md`](analysis/TRACEABILITY.md)).
- [ ] Every formula in `Catalog42.v` and friends has a stated error bound that `scripts/validators/validate_v4.py` can reproduce.
- [ ] Versions are pinned: Coq 8.20.1, Lean 4 v4.13.0, Rust edition 2024, Python 3.12 in CI.
- [ ] Build instructions in [`README.md`](../README.md) §"Build Instructions" and [`CONTRIBUTING.md`](../CONTRIBUTING.md) match what CI actually runs.

## I. Pages deploy and live game

- [ ] <https://t27.ai/trinity-s3ai/> loads.
- [ ] The page renders either the wasm canvas or the inline SVG fallback (the workflow guarantees the page is never blank).
- [ ] The live canvas links back to the repository.

## J1. Wave 17 honest-negative-result discipline

- [ ] The README and `SALVAGE.md` describe the project as a *constructive negative result*, not as a successful unification.
- [ ] The four Coq-formal No-Go theorems NGT1–NGT4 in [`proofs/trinity/NoGoTheorems.v`](../proofs/trinity/NoGoTheorems.v) close with `Qed.` and are listed in [`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md) §4.
- [ ] The additional Wave 11–17 No-Go results NGT-5 (D₄/24-cell), NGT-6 (no σ-field under string/orbifold rescue) and NGT-7 (F₄ 3-generation hierarchy) are documented at paper / analysis level in [`paper/CHANGELOG_v1_to_v2.md`](../paper/CHANGELOG_v1_to_v2.md), [`ROADMAP.md`](../ROADMAP.md) and [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md), and are flagged as *not yet Coq-formalised* in [`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md) and [`docs/TECH_TREE.md`](TECH_TREE.md).
- [ ] The E₈-plumbing η-convergence claim and the string / heterotic / orbifold rescue claim are both classified as **high_risk_or_falsified** in [`docs/CLAIM_STATUS.md`](CLAIM_STATUS.md) §4, consistent with the Wave 17 honesty notes in [`paper/CHANGELOG_v1_to_v2.md`](../paper/CHANGELOG_v1_to_v2.md) and the findings in [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md).
- [ ] The post-Wave-17 program is published as Tracks A (honest phenomenology), B (Cl(8) / J₃(𝕆)) and C (negative-result paper) in [`ROADMAP_WAVE17_PLUS.md`](../ROADMAP_WAVE17_PLUS.md); no track claims a Theory of Everything or prize-level recognition.

## J. Known blind spots are visible

- [ ] [`docs/REVIEW_GUIDE.md`](REVIEW_GUIDE.md) §6 enumerates the known blind spots.
- [ ] [`docs/TECH_TREE.md`](TECH_TREE.md) Layer 4 flags the Lagrangian gap.
- [ ] [`COQ_HONEST_STATUS.md`](status/COQ_HONEST_STATUS.md) documents the older inconsistent metric claims.
- [ ] [`REMAINING_PROBLEMS.md`](status/REMAINING_PROBLEMS.md) is up to date with the layers above.

---

## Sign-off

A reviewer who has ticked every box above can fairly say:

> *Trinity S3AI is review-ready as a constructive negative result: the
> proofs that exist are real, the fits that exist are tagged, the
> impossibilities that are claimed are formal, and no Theory-of-
> Everything claim is made.*

That is the standard the project holds itself to. It is **not** a
statement that the open conjectures are correct, nor that the risky
predictions will survive contact with data; those are external matters
that this repository deliberately does not pre-judge.
