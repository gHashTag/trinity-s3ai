# LEGACY DOCUMENT (historical salvage analysis)
# Current status: see RESEARCH_STATUS.md and TECH_TREE.md for canonical framing.

# SALVAGE.md — What to Keep, What to Archive

**Project:** Trinity S3AI  
**Wave:** 9.6 — Honest Meta-Analysis  
**Date:** June 2026  
**Principle:** "Do not lie!! Be honest!"

---

## Brief summary

After eight waves of formalisation, 340 machine-verified theorems and 4 obstruction theorems (BT-1–4), the project is at a point of honest reckoning. This document defines:

- **KEEP**: mathematical and methodological achievements of independent value
- **ARCHIVE**: physical claims that have been refuted or falsified
- **RENAME**: what the project should be called to reflect its real contribution

---

## Part 1: WHAT TO KEEP

### 1.1 Coq formalisation (340 Qed)

| File | Value | Reason |
|------|-------|--------|
| `CorePhi.v` | High | First-class formalisation of the golden ratio with arithmetic and inequalities |
| `SpectralExtras.v` | High | Spectral constants of the 600-cell (Qed, 0 Admitted) |
| `DiracOperator.v` | High | D = R_i satisfies the first-order condition (Qed); methodologically novel approach |
| `EtaInvariant.v` | High | η = -2 on S³/2I — necessary condition for chirality |
| `KODimension.v` | High | KO-dimension = 6 mod 8 — positive structural result |
| `QuaternionicLinearity.v` | High | 2I structure and quaternionic motivation ℍ ⊂ A_F |
| `UnimodularityAndSigma.v` | Medium | U1–U7: Qed, sigma_boundary: BT-2 reinforced |
| `RGRunningExtras.v` | High | alpha_from_H4_refuted (Qed) — exemplary boundary finding |
| `ChiralityAnalysis.v` | High | Honest analysis; BT-3 is based on this file |
| **`NoGoTheorems.v`** | **High** | **32 Qed, 0 Admitted — main contribution of Wave 9.6** |
| `SpectralTripleAxioms.v` | Medium | Structure of NCG axioms |
| `DFSpectrum.v` | High | σ = 5.62 — key number of BT-4 |
| `EtaInvariant.v` | High | Poincaré η-invariant |

**Total: ~340 machine-verified lemmas and theorems.**

### 1.2 Methodological tools

| File/approach | Value | Description |
|--------------|-------|-------------|
| `admitted_log.md` | High | Exemplary registry of honest gaps with HONEST tags |
| `cosmology_falsified_log.md` | High | Registry of 9 falsified formulas with σ-distances |
| `catalog_audit/audit_report.md` | High | Classification of 25 formulas by rigour (R/S/NF) |
| `registered_predictions.md` | Medium | Registry of falsifiable predictions |
| `full_audit.csv` | Medium | Machine-readable audit |

**Methodology:** Coq verification of numerical inequalities as a means of honest documentation of formula accuracy — this is a novel approach worthy of a separate methodological publication.

### 1.3 Physical results surviving after BT-1–4

| Result | Status | Value |
|--------|--------|-------|
| KO-dim = 6 mod 8 | ✅ SURVIVES | Structural match with NCG SM |
| 2I motivates ℍ ⊂ A_F | ✅ SURVIVES | Algebraic fact |
| η = -2 on S³/2I | ✅ SURVIVES | Necessary condition for chirality |
| D = R_i: first-order condition | ✅ SURVIVES | Exact result |
| Unimodularity via H4 → A4 → SU(5) | ✅ SURVIVES | Embedding chain |
| 25 formulas with NF/S/R tags | ✅ SURVIVES (as catalogue) | Honest numerology |
| δ_CP = 65.66° | ⏳ PENDING | DUNE 2028 will give the answer |

### 1.4 Lean port (scaffold)

`derivations/lean_port/` — beginning of Lean 4 formalisation. Keep as a basis for future work. Lean 4 is more accessible to the physics community than Coq.

---

## Part 2: WHAT TO ARCHIVE

### 2.1 Physical claims refuted or falsified

| Claim | Wave of refutation | Reason |
|-------|-------------------|--------|
| "Trinity derives the Standard Model" | Wave 9.6 (BT-1–4) | The combined force of four obstruction theorems |
| "α is computed from H4" | Wave 3 | alpha_from_H4_refuted (Qed) |
| "σ-field from H4-structure" | Wave 5.3 | sigma_boundary (BT-2) |
| "600-cell is chiral" | Wave 6 | Antipodal symmetry (BT-3) |
| "D_F reproduces the SM spectrum" | Wave 8.4 | σ = 5.62 >> 5 (BT-4) |
| Λ = φ^(-144)/2 | Wave 7/8.5 | ~118 orders of magnitude deviation |
| All Tier-3 CMB formulas | Wave 8.5 | 9 falsifications (up to 754σ) |
| "Catalogue formulas are rigorous derivations" | Wave 3 | 0/25 class R |

### 2.2 What to do with them

**DO NOT** delete — this is the scientific history of the project. **Move** them with appropriate tags:

```
Status: ARCHIVED — superseded by BT-[1-4] (Wave 9.6)
```

Keep them in the repository as documentary evidence of **exactly how** the boundary findings were obtained.

---

## Part 3: RENAMING AND REBRANDING

### 3.1 Current name (inaccurate)

> "Trinity-s3ai: Framework for H4/600-cell Standard Model Unification"

This name is inaccurate: the formalisation **did not achieve** SM unification. The claim is misleading.

### 3.2 Proposed new name

> **"Trinity-s3ai: A formal exploration of H4/600-cell symmetry in the context of Noncommutative Geometry, with active boundary-mapping research programs"**

**Why this is better:**

1. **Honest:** the word "exploration" accurately describes what was done.
2. **Valuable:** "active boundary-mapping research programs" — a format accepted in serious journals.
3. **Accurate:** "H4/600-cell symmetry" — the real object of study.
4. **Not disappointing:** the reader knows what to expect.

### 3.3 Alternative titles for the paper

- *«H4 and the 600-cell: Four Obstruction Theorems for NCG-based Standard Model Unification»*
- *«Machine-Verified Obstruction Theorems in Speculative Unified Physics: The Trinity-s3ai Framework»*
- *«What H4 Cannot Do: A Coq-Formalized Audit of the 600-Cell Approach to Standard Model Unification»*

---

## Part 4: VALUE AS A METHODOLOGICAL CONTRIBUTION

Regardless of physical content, Trinity-s3ai demonstrates:

### 4.1 Machine verification of boundary findings

This is a **novel methodological approach**: using Coq to document not only positive but also boundary findings in speculative physics. Example from `NoGoTheorems.v`:

```coq
Theorem alpha_from_H4_refuted :
  ~ (Rabs (alpha_inv_mZ_code - trinity_alpha_inv_x) / trinity_alpha_inv_x < 1/100).
Proof. ... Qed.
```

This is a **rigorous refutation** — stronger than "this does not work for numerical reasons".

### 4.2 Honest registry of gaps

`admitted_log.md` is an example of how `Admitted` should be documented:

```
(* HONEST Admitted SM3: The H4 spectral decomposition does not produce
   the SM gauge group without additional input. *)
Admitted.
```

This contrasts with the practice of hiding `Admitted` or using them without explanation.

### 4.3 Systematic falsification

`cosmology_falsified_log.md` with its table of σ-distances — a methodological model for future work in *phenomenological numerology* with honest auditing.

---

## Part 5: CONCRETE ACTION PLAN

### Step 1: Immediate (Week 1)

- [x] Create `no_go_theorems.md` — formulation of BT-1–4 (done)
- [x] Create `NoGoTheorems.v` — 32 Qed, 0 Admitted (done)
- [x] Update README.md: add a warning that the project has reached active boundary-mapping research programs
- [ ] Add `Status: ARCHIVED` tag to falsified claims

### Step 2: Short-term (Month 1)

- [ ] Write arXiv preprint (~20 pages) with BT-1–4 and their proofs
- [ ] Submit to arXiv hep-th or math-ph
- [ ] Update CITATION.bib with an accurate project description

### Step 3: Medium-term (Quarter)

- [ ] Submit to Foundations of Physics or SHPMP (with emphasis on methodology)
- [ ] Continue developing the Lean 4 port (broader audience)
- [ ] If DUNE 2028 falsifies δ_CP: document as a predicted falsification

### Step 4: Long-term (possible open questions)

If the project continues — only through honest **new** hypotheses:

1. **Mechanism for breaking antipodal symmetry**: what extension of the construction could break the symmetry v ↦ -v? (F-theory over the 600-cell?)
2. **η-invariant as physical chirality**: APS boundary conditions for the Dirac operator on S³/2I with a compactification zone — a theoretically possible path.
3. **Richer algebra**: what if A_F is not ℂ ⊕ ℍ ⊕ M₃(ℂ), but a richer structure motivated by H4?

All three — open questions, not claims.

---

## Final summary

| Category | Count | Action |
|----------|-------|--------|
| Qed (machine-verified) | **340** | KEEP |
| Admitted (honest gaps) | **7** | KEEP with tags |
| Boundary theorems | **4** (BT-1–4) | PUBLISH |
| Falsified CMB formulas | **9** | ARCHIVE with tags |
| Surviving physical results | **6** | KEEP |
| Refuted claims | **8** | ARCHIVE |
| Formulas in honest catalogue | **25 (0R+8S+17NF)** | KEEP |

---

**Conclusion:**

The Trinity-s3ai project conducted eight waves of honest formalisation. The result is not a "theory of everything", but a **active boundary-mapping research program**: H4/600-cell in its current formulation is insufficient to derive the SM. This is a scientific contribution. It should be published as such.

*"An honest boundary theorem is worth more than a failed positive claim."*

---

*Wave 9.6 — June 2026. Trinity-s3ai: an honest reckoning.*
