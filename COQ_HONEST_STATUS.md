# Coq Formalization — Honest Status

**Status**: Canonical reconciliation of the project's Coq metrics
**Date**: 2026-05-23
**Companion**: [`LAGRANGIAN_HONEST_STATUS.md`](./LAGRANGIAN_HONEST_STATUS.md) (Wave 1), [`DELTA_CP_HONEST_STATUS.md`](./DELTA_CP_HONEST_STATUS.md) (Wave 2)
**Source of ground truth**: [`admitted_log.md`](./admitted_log.md) (the project's internal audit document) + direct count on the current commit

---

## TL;DR

The repository advertises **five mutually inconsistent sets of Coq metrics** across its public documents. The correct numbers, derived from a direct count on the current commit and cross-checked against the project's own [`admitted_log.md`](./admitted_log.md), are:

| Metric | Reality (this commit) | Most common public claim | Status of public claim |
|---|---|---|---|
| `.v` files | **79** (50 in `proofs/trinity/` + 3 in `proofs/clifford_cl8/` + 26 in `derivations/`) | "19/19", "23/23", "9/19", "25" | **inconsistent across docs** |
| `Qed.` (closed theorems) | **1325** | "326 Qed", "60+ theorems QED" | **understated** |
| `Admitted.` | **25** | "0 Admitted", "6 Admitted", "25 Admitted" | **understated** in headline; correct in `admitted_log.md` |
| `admit.` (inline) | **18** | "0 admit" | **understated** |
| `Axiom` declarations | **73** | not advertised | **understated** (often "0") |
| `Parameter` declarations | **7** | not advertised | — |
| **Total unproven obligations** | **123** | "0" or "6" or "25" | **understated by 5×–20×** |

**The most-advertised slogan "326 Qed / 0 Admitted = 100% verified" is false in both halves.** The real Qed count is **4× larger** (a positive fact that the project was underselling), and the real unproven-obligation count is **123, not 0**.

---

## 1. The five conflicting public claims

| Document | Coq files claim | Qed claim | Admitted claim | Compilation |
|---|---|---|---|---|
| `README_v46.md` (pre-Wave-3) | "9/19 (47%)" | "60+ QED" | "0 Admitted" | 47% |
| `IMPROVEMENT_PLAN.md` (pre-Wave-1) | "19/19 (100%)" | not stated | "6 Admitted" | 100% |
| `IMPACT_COMPARISON.md` (pre-Wave-1) | "19/19 to 20 .vo" | **"326 Qed"** | **"0 Admitted"** | implicit 100% |
| `CONTRIBUTING.md` | "23 files" | "326 Qed" | not stated | — |
| `scripts/prepare_zenodo.md` | "23 files" | "326 Qed" | "0 Admitted" | — |
| `RELEASE_NOTES_v1.0-wave11.md` | "25 files" | "312 Qed" | "25 Admitted" | "**4/16 = 25%**" (with explicit note that README contradicts this) |
| `derivations/physics_review/independent_review.md` | "23/23" (quoting README) | "326 Qed" (quoting README) | "0 Admitted" (quoting README) | (with critique of all three) |
| **`admitted_log.md` (canonical, project-internal)** | **53 files in proofs/** | **1351 Qed** (W12.4) | **34 Admitted + 17 admit** | (not claimed) |
| **Direct count, this commit** | **79 files total** (proofs + derivations) | **1325 Qed** | **25 Admitted + 18 admit** | (not measured here) |

The `RELEASE_NOTES_v1.0-wave11.md` already contains the most important admission, in writing:

> "**Note:** The README advertises 23/23 Coq files compiling at 100 %. The ground truth from `compilation_report.md` is **4/16 compiled** with 12 files failing due to tactic failures, syntax errors, and missing dependencies."

That note was correct. The remedy was never propagated to the README.

---

## 2. The canonical numbers (May 2026)

Direct count via `grep -h "^Qed\." | wc -l` on the current commit, across both `proofs/` (the published proof tree) and `derivations/` (parallel derivation files, many of which mirror `proofs/`):

```
.v files:    79  (50 proofs/trinity + 3 proofs/clifford_cl8 + 26 derivations)
Qed.:        1325
Admitted.:   25
admit (inline): 18
Axiom:       73
Parameter:   7
─────────────────
unproven:    123   (= 25 + 18 + 73 + 7)
```

These are the numbers that should appear in any public-facing summary. They supersede the seven inconsistent versions listed above.

### Where the 123 unproven obligations live

Per `admitted_log.md` taxonomy (with counts updated for current commit):

| Category | Count | What it is |
|---|---|---|
| `[PHYSICAL_AXIOM]` | ~5 | Genuine physics assumptions (RG boundary, mass scale, normalization) — **not closable by mathematics alone** |
| `[NUMERICAL_FIT]` | ~3 | Formula found by numerical search; no derivation exists — **GENUINE_ASSUMPTION** |
| `[MATH_TODO]` | ~6 | Mathematically provable, proof not written |
| `[LIBRARY_GAP]` | ~15 | Closable with tactic tweaks (`interval`, `field`, `lia` in Rocq 9.1.1) — **mechanical work** |
| `[REFUTED]` | ~2 | Mathematically false; flagged for refutation, not closure |
| **Track B Cl(8)** | 10 | New direction; 6 Axiom + 4 Admitted with full published citations (Wieser-Song 2022, Lounesto 2001, Atiyah-Bott-Shapiro 1964) |
| **Other (Axiom/Parameter scaffolding)** | ~82 | Existence claims for spectral triple components, gauge group assignments, NCG axioms, derivation mirror files |

The breakdown is taken from `admitted_log.md` §"Tag Summary" — **the project's own audit**. Wave 3 does not invent any of this; it surfaces what `admitted_log.md` has already documented.

---

## 3. What is actually verified in Coq

This is where Wave 3 is more positive than the existing public summary. The real Coq work is **larger** than advertised, even though the headline metric was misleading.

### Files with genuine `0 Admitted` status (verified by direct count)

The following files have no `Admitted.` declarations:

- `CorePhi.v` — φ definition, φ² = φ+1, powZ, Lucas numbers
- `H4Derivations.v` — 17 derivation theorems from H4 invariants
- `HiggsPrediction.v` — m_H = 4φ³e² bounds (m_H ≈ 125.1 GeV within 0.09% of PDG)
- `KoideOrigins.v` — 13 Qed, including the honest "Koide ≠ 2/3 in H4" theorem
- `QuarkOrigins.v` — quark mass theorem inventory, all Qed
- `QuaternionicLinearity.v` — quaternionic algebra, Hamilton product
- `RGRunningExtras.v` — 14 Qed extras for RG running
- `SpectralExtras.v` — spectral triple supplementary lemmas
- `UniquenessTheorem.v` — H4 invariant enumeration
- `UniquenessStructural.v` *(header claim; has 1 Admitted per direct count — see correction below)*

### Files with non-zero `Admitted.`

Per direct count (`grep -l "^Admitted\." proofs/`):

- `proofs/trinity/test_scratch.v` (3 Admitted)
- `proofs/trinity/UniquenessStructural.v` (1 Admitted)
- `proofs/trinity/RGRunning.v` (2 Admitted)
- `proofs/trinity/NeutrinoOrigins.v` (2 Admitted)
- `proofs/trinity/LeptonOrigins.v` (1 Admitted)
- `proofs/trinity/H4GaugeEmbedding.v` (1 Admitted)
- `proofs/trinity/GaugeOrigins.v` (1 Admitted)
- `proofs/trinity/E6vsH4.v` (4 Admitted)
- `proofs/trinity/ChiralityAnalysis.v` (1 Admitted)
- `proofs/clifford_cl8/CliffordAlgebra.v` (1 Admitted)
- `proofs/clifford_cl8/Cl8_periodicity.v` (2 Admitted)
- `proofs/clifford_cl8/Cl6_iso_M8R.v` (1 Admitted)
- Plus derivations/ mirrors

### Misleading file-level header comments

Per `admitted_log.md` §"Header-comment status":

| File | Header claim | Reality | Action |
|---|---|---|---|
| `E6vsH4.v` | "ALL theorems: QED, 0 Admitted." | **4 Admitted + admit** | Fixed in Wave 3 |
| `UniquenessStructural.v` | "0 Admitted" | **1 Admitted** per current count | Fixed in Wave 3 |
| `H4Derivations.v` | "ALL theorems: QED, 0 Admitted." | **Verified true** for this file | Unchanged |
| `CorePhi.v` | "All theorems provable with Qed (0 Admitted)" | **Verified true** | Unchanged |

---

## 4. What this means for the "Mathematical Rigor 9/10" score

[`IMPACT_COMPARISON.md`](./IMPACT_COMPARISON.md) gives the project a **9/10 on Mathematical Rigor**. The justification was "326 theorems Qed in Coq, 0 Admitted". Both halves of that justification are now corrected:

- The true Qed count is **1325**, not 326 (4× higher — argues **for** a high score)
- The true unproven-obligation count is **123**, not 0 (argues **against** a maximal score)

### Caveat: even Qed-closed lemmas are not all "physics theorems"

[`derivations/physics_review/independent_review.md`](./derivations/physics_review/independent_review.md) §3.2 makes the deeper point: many of the 1325 Qed-closed lemmas are:

1. **Trivial reflexivity** facts (e.g. `coxeter_number_factorization : 30 = 2*3*5. reflexivity. Qed.`)
2. **Numerical interval verifications** via the `interval` tactic — these verify *that a formula evaluates to a number in a given range*, not *that the formula follows from physical first principles*.
3. **Definitions stated as theorems** (e.g. `H4_order = 14400` is a definition, not a derived fact).

So `Qed.` count is a real signal of work done, but it is not directly proportional to "physics derived from first principles". This caveat is consistent with the Lagrangian honesty pass (Wave 1): **3 of 13 SM Lagrangian sectors are formally derived from first principles; the rest are phenomenological fits whose numerical agreement is verified in Coq via `interval`**.

### Revised score

A defensible score for Mathematical Rigor — preserving the strong genuine successes while accounting for the unproven obligations and the interval-tactic caveat — is in the **6–7 / 10** range, not 9/10. The strongest signals (m_H closed, gauge couplings closed, 1325 Qed, well-maintained `admitted_log.md`) are real; the weakening signals (123 obligations, blanket "0 Admitted" claims that are false, interval verification vs derivation conflation) cap the score below 9.

---

## 5. What is updated by Wave 3

| File | Change |
|---|---|
| **`COQ_HONEST_STATUS.md`** (this file) | NEW — canonical reconciliation |
| `README_v46.md` | "0 Admitted" blanket claims replaced; "60+ QED" replaced with real count; "9/19" status flagged as one-of-five inconsistent claims |
| `IMPACT_COMPARISON.md` | "326 Qed / 0 Admitted" replaced; Mathematical Rigor 9/10 revised to 6–7/10 with justification |
| `IMPROVEMENT_PLAN.md` | "19/19 compile" + "6 Admitted" replaced with link to this doc |
| `CONTRIBUTING.md` | "23 files, 326 Qed" replaced with real count |
| `scripts/prepare_zenodo.md` | "326 Qed / 0 Admitted" corrected before any Zenodo DOI is minted with these numbers |

## 6. What is NOT updated

- **`admitted_log.md`** — already honest; left unchanged. This is the canonical source.
- **`RELEASE_NOTES_v1.0-wave11.md`** — already honest; already contains the warning about README misrepresentation.
- **`peer_review_PRD.md`** — already honest; already calls the inconsistency academic dishonesty.
- **`derivations/physics_review/independent_review.md`** — already honest; already analyses the trivial-reflexivity caveat.
- **The Coq proof files themselves** — no proofs are modified, no `Admitted.` is closed by hand. Wave 3 only updates *claims about* the proofs, not the proofs.

---

## 7. Why this matters

The Lagrangian honesty pass (Wave 1) and the δ_CP honesty pass (Wave 2) both turned on a single pattern: **the project's internal audit documents already said the harder truth, but the public-facing documents kept the older overclaim**. Wave 3 is the same pattern in a third sector.

- `admitted_log.md` already said: "Previous README claimed 0 Admitted. This is INCORRECT."
- `RELEASE_NOTES_v1.0-wave11.md` already said: "README advertises 23/23 compiling at 100%. Ground truth: 4/16 compiled."
- `peer_review_PRD.md` already said: "An Admitted theorem in a paper claiming 0 Admitted is academic dishonesty."
- `independent_review.md` already said: "the v4.12 claim of 0 Admitted... many 'proofs' are trivial reflexivities".

This pass lifts those four internal admissions into a single front-page document so that they cannot be contradicted by a README slogan.

> A formalisation effort that produces 1325 Qed-closed lemmas and 123 honestly-tracked unproven obligations is **stronger** as a project than one that produces 326 Qed-closed lemmas and claims 0 admitted. The first is real work transparently documented; the second is a slogan that survives only as long as nobody counts.
