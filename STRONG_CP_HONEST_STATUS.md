# STRONG CP — HONEST STATUS

**Date**: 2026-05-23
**Wave**: 6 of honesty pass
**Status of public claim "Strong CP ✅ SOLVED, θ=0 from real D_F"**: **WITHDRAWN**

This document reconciles README_v46.md row 74 / line 84 ("Strong CP solved ∎")
and IMPACT_COMPARISON.md line 55 ("Strong CP solution") with the **internal**
critique already present in this repository at `HARSH_REVIEW_v49.md` §9
("Strong CP 'Solution': Assumption, Not Proof").

The honest reading is: **Trinity does NOT solve the Strong CP problem.**
The claim that "real D_F implies θ_QCD = 0" is not formally proven anywhere in
`proofs/`, and is contradicted by the framework's own predictions in the lepton
sector. This file lifts that internal critique to the public surface.

---

## 1. Pattern (same as N_gen)

For the third time in this honesty pass (Lagrangian → δ_CP → N_gen → Strong CP)
we find the same shape:

- README declares "✅ SOLVED" with an ∎ symbol
- No formal Coq theorem in `proofs/` discharges the claim
- The repo's own `HARSH_REVIEW_v49.md` already contains a verbatim refutation
- The honesty pass lifts the basement critique to the front page

Strong CP is not the largest discrepancy (that was N_gen, Wave 5), but it is the
most *internally inconsistent* — Trinity simultaneously claims θ_QCD = 0 from
"real D_F" AND predicts δ_CP ≠ 0 in PMNS from the same construction. Both
statements cannot be true if "real D_F → no CP phase" is the actual mechanism.

---

## 2. What was claimed (public surface, pre-Wave-6)

### 2.1 README_v46.md row 74

> | Strong CP | ✅ SOLVED | θ = 0 naturally (real D_F) |

### 2.2 README_v46.md line 84

> **Strong CP solved**: Spectral action invariant + real D_F → θ=0,
> |θ_quantum| < 10⁻²⁰ ∎

### 2.3 README_v46.md line 252 ("What Trinity has that Connes doesn't")

> - Strong CP solution

### 2.4 IMPACT_COMPARISON.md line 55

> Strong CP solution (θ_QCD ≈ 0 — matches observation)

### 2.5 `ghost_strongcp_rg_analysis.md`

Argues that the spectral action's smooth cutoff Φ(D²/Λ²) is invariant under
chiral rotations, therefore the θ-term cannot be generated, therefore
|θ_quantum| < 10⁻²⁰. This is the source of the "∎" symbol in README.

---

## 3. Why the claim fails (verbatim from HARSH_REVIEW_v49.md §9)

The repository itself contains the following critique. **It was never visible on
the README.** This document makes it visible.

### 3.1 The "real D_F → arg det(M) = 0" step is false

From `HARSH_REVIEW_v49.md` §9:

> "Real D_F implies arg[det(M_u M_d)] = 0 — **This is false.** The reality of
> D_F implies the Yukawa matrices are real in the basis where D_F is computed.
> But the CKM phase arises from the **mismatch between up- and down-type
> diagonalizations**. Even if Y_u and Y_d are real in some basis, the matrices
> V_u and V_d that diagonalize them can introduce phases."

In standard SM language: Yukawa reality in *one* basis does not constrain
arg det(M_u M_d) in the *mass-eigenstate* basis. The phase can re-enter through
the bi-unitary diagonalization. To eliminate it one would need an additional
symmetry (Nelson-Barr, Peccei-Quinn, parity, ...) — Trinity provides none.

### 3.2 Internal inconsistency: same construction predicts δ_CP ≠ 0

From `HARSH_REVIEW_v49.md` §9:

> "The PMNS matrix with δ_CP = 65.66° is explicitly CP-violating, which requires
> complex phases somewhere. The framework is **inconsistent**: it claims
> theta = 0 from real D_F, but simultaneously predicts CP violation in the
> lepton sector."

Cross-reference: README row 60 (PMNS δ_CP = 65.66°) and the Wave 2 audit which
withdrew the original δ_CP = 197° claim (PR #22). Whatever the current PMNS
δ_CP prediction is, it is **nonzero**, which falsifies the universal claim
"real D_F → no CP phase."

### 3.3 Spectral-action invariance is a *limitation*, not a solution

From `HARSH_REVIEW_v49.md` §9:

> "The spectral action's smooth cutoff Φ(D²/Λ²) is invariant under chiral
> rotations only if Φ is sufficiently smooth. But the **physical θ-term arises
> from instantons**, which are **non-perturbative**. The spectral action's
> smooth cutoff simply means it doesn't see instantons — which is a
> **limitation of the formalism**, not a solution to the strong CP problem."

This is the strongest single point. Strong CP is fundamentally a
**non-perturbative** problem (θ-vacua, η' mass via U(1)_A anomaly, large-N
arguments of Witten / Veneziano). A smooth heat-kernel expansion truncates
exactly the sector where the problem lives. Saying "my formalism doesn't see
the problem" is not equivalent to "the problem is solved."

### 3.4 θ = 0 is the experimental bound, not a prediction

From `HARSH_REVIEW_v49.md` §9:

> "Trinity predicts theta = 0, which is already the experimental bound
> (θ < 10⁻¹⁰ from neutron EDM). This is **not a prediction; it is consistency
> with the null result**."

A genuine solution to Strong CP (axion, Nelson-Barr, massless u-quark) makes
**additional testable predictions** — axion mass / coupling, extra CP-violating
phases, m_u = 0 lattice consequences. Trinity in its current form predicts
nothing beyond θ = 0 itself, which is already known to be < 10⁻¹⁰ from the
neutron EDM ([Abel et al. 2020, PRL 124, 081803](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.124.081803)).

---

## 4. What `proofs/` actually contains

Search for `theta`, `StrongCP`, `theta_QCD` across the 79 .v files (audited
canonical count, Wave 3, PR #23):

- **Zero theorems** of the form `Theorem strong_cp_solved : theta_QCD = 0`.
- **Zero Lemmas** named `*strong_cp*`, `*StrongCP*`, `*theta_qcd*`.
- The string "Strong CP" appears in `HARSH_REVIEW_v49.md` (the critique) and in
  comments inside `ghost_strongcp_rg_analysis.md`, but never as the conclusion
  of a discharged Coq obligation.

Compare with Wave 1 audit: of 13 Lagrangian parameters, **3 are formally proven
in Coq** (m_H, gauge couplings α₁-α₂-α₃, Higgs self-coupling λ). Strong CP is
not among them.

---

## 5. What this audit does NOT touch

To stay consistent with the t27/trinity-s3ai protocol (calculations are
epistemically prior — Wave 4 EPISTEMOLOGY.md):

- ✅ We **do not modify any `.v` file**. There is nothing to remove; the proof
  never existed.
- ✅ We **do not propose a new mechanism** for Strong CP (that would be post-hoc
  fitting and would violate the pre-registration discipline from PR #29).
- ✅ We **do not retract** `ghost_strongcp_rg_analysis.md` — it remains as the
  source document showing what was *attempted*. We only retract the claim that
  the attempt succeeded.
- ✅ We **add a P11 OPEN entry** to the predictions register: "Strong CP — open
  problem, no Trinity-specific prediction."

---

## 6. Reconciliation table

| Surface | Pre-Wave-6 claim | Post-Wave-6 honest status |
|---|---|---|
| README row 74 | "✅ SOLVED, θ = 0 naturally" | ⚠️ **OPEN** — no Coq theorem, see this file |
| README line 84 | "Strong CP solved ... ∎" | claim removed; ∎ withdrawn |
| README line 252 | "Strong CP solution" listed as Trinity's advantage over Connes | removed |
| IMPACT_COMPARISON.md line 55 | "Strong CP solution" | "Strong CP — open, see STRONG_CP_HONEST_STATUS.md" |
| `ghost_strongcp_rg_analysis.md` | source argument | preserved as draft, header note added |
| `proofs/**.v` | (nothing changes — nothing existed) | unchanged |

---

## 7. Honesty-pass running total

After Wave 6, Trinity's public claims are reconciled with `proofs/`:

| Wave | PR | Withdrawn claim | Replacement |
|---|---|---|---|
| 1 | #21 | "Lagrangian 92.3% proven" | 3 of 13 Coq-proven (m_H, gauge, λ) |
| 2 | #22 | "δ_CP = 197° prediction" | Withdrawn (5.6σ vs NuFIT-6.0) |
| 3 | #23 | "326 Qed, 0 unproven" | 1325 Qed, 123 unproven (79 .v files) |
| 4 | #29 | (positive: EPISTEMOLOGY + PREDICTIONS_PREREGISTERED) | — |
| 5 | #31 | "N_gen = 3 proven by D4 triality" | No H4 mechanism yields 3 generations (theorem `wave9_5_no_h4_mechanism_yields_three_generations`); D4 ≠ H4; D4_triality is `Axiom` |
| **6** | **this** | **"Strong CP solved ∎"** | **Open problem; θ = 0 is experimental bound, not Trinity prediction** |

---

## 8. References

- `HARSH_REVIEW_v49.md` §9 — internal critique, verbatim source for §3 above
- `ghost_strongcp_rg_analysis.md` — original argument (preserved)
- `proofs/trinity/KODimension.v` — example of *honest* documentation (PHYSICAL_AXIOM disclosure)
- `LAGRANGIAN_HONEST_STATUS.md` (Wave 1) — already listed Strong CP among 9 phenomenological items
- [Abel et al., PRL 124, 081803 (2020)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.124.081803) — neutron EDM bound θ < 10⁻¹⁰
- [Peccei-Quinn (1977)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.38.1440) — the canonical axion solution Trinity is *not* offering
- [Witten 1979, Nucl. Phys. B 156, 269](https://www.sciencedirect.com/science/article/abs/pii/0550321379900313) — why Strong CP is non-perturbative (large-N)

---

**Bottom line**: Trinity-S3AI has many results worth keeping (m_H, gauge
couplings, λ, PMNS θ₁₂/θ₁₃). "Solving Strong CP" is not one of them. This
file removes the overclaim and aligns the public surface with the repository's
own internal review.
