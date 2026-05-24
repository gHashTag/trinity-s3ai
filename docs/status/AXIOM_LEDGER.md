# Axiom Ledger — Trinity S³AI (Wave 20 Honesty Refresh)

**Companion to:** `COQ_HONEST_STATUS.md`, `TAUTOLOGY_AUDIT.md`  
**Purpose:** Catalog every `Axiom`, `Parameter`, and `Conjecture` in the Coq codebase with honest assessment of load-bearing status and proof priority.

---

## Honesty Statement

The project advertises "0 real `Admitted.` in proofs/trinity/" as an achievement. This is technically true but **strategically incomplete**. There are **82 Axioms + 8 Parameters** (90 total unproven obligations) that serve the same epistemic function as `Admitted.` — they assert conclusions without proof. The difference is cosmetic: `Admitted.` appears in proof scripts; `Axiom` appears in declarations. Both leave a logical gap.

This ledger is the project's commitment to **not hiding gaps behind syntax**.

---

## Ledger by Category

### 1. Physical Conclusions Asserted as Axioms (CRITICAL — must prove or withdraw)

These Axioms assert exactly the physical conclusions the project claims to have derived.

| # | Axiom | File | What it asserts | Why it's a gap |
|---|-------|------|-----------------|----------------|
| 1 | `Trinity_matches_experiment` | `HiggsPotentialCorrected.v` | `Rabs(m_H_Trinity - m_H_measured) < 0.25` | The "proof" that Higgs potential matches experiment is this Axiom. Circular. |
| 2 | `H01_spectral_key_identity` | `HiggsOrigins.v` | `Tr_D2 * 480 / Tr_D4 = 4 * phi^3` | Central claim linking H4 geometry to Higgs mass. Asserted, not derived. |
| 3 | `gap_approx_6percent` | `HiggsPotentialCorrected.v` | `220/246 < gap_factor < 235/246` | Assumes the 6% gap exists. |
| 4 | `APS_E8_plumbing` | `EtaDFBridge.v` | `eta_continuous = -2` | Assumes APS index theorem result for E8 plumbing. |
| 5 | `sigma_no_go` | `UnimodularityAndSigma.v` | `True` | **Zero logical content.** Tagged `SIGMA_NO_GO_STRUCTURAL` but proves nothing. |
| 6 | `sigma_no_dynamical_field` | `UnimodularityAndSigma.v` | `True` | **Zero logical content.** |
| 7 | `DF_max_eigenvalue_numerical` | `DFSpectrum.v` | Numerical spectrum bound | Hard-codes Python diagonalization result. |

### 2. Open Mathematical Problems (HONEST — labeled MATH_TODO)

These are honest placeholders for genuine unsolved problems in NCG / spectral triples.

| # | Axiom | File | Open Problem |
|---|-------|------|--------------|
| 8 | `axiom_first_order_MATH_TODO` | `SpectralTripleAxioms.v` | First-order condition for 600-cell spectral triple |
| 9 | `axiom_orientation_hochschild` | `SpectralTripleAxioms.v` | Hochschild orientation cycle for H4 geometry |
| 10 | `axiom_poincare_nondegeneracy` | `SpectralTripleAxioms.v` | Poincaré duality for finite H4 spectral triple |
| 11 | `axiom4_commutator_vanishing` | `SpectralTripleAxioms.v` | `[a, [D, b]] = 0` for H4 Dirac operator |
| 12 | `cell600_J_off_diagonal_KO6` | `SpectralTripleAxioms.v` | KO-dimension 6 structure for 600-cell |
| 13 | `axiom7_KK_theory_poincare` | `Axiom7Poincare.v` | Full K-theoretic Poincaré duality |
| 14 | `full_KK_poincare_duality` | `Axiom7Poincare.v` | Complete KK-theory duality for H4 bundle |
| 15 | `topological_K_theory_2I` | `Axiom7Poincare.v` | K-theory of binary icosahedral group |

### 3. Structural / Geometric Assumptions (CITED_MATH — reasonable but unproven)

These assume standard mathematical results that the project cites but does not formalize.

| # | Axiom | File | Cited Result |
|---|-------|------|--------------|
| 16 | `eta_S3_2T_admitted` | `AltCrystallography.v` | η-invariant for S³/2T (binary tetrahedral) |
| 17 | `eta_S3_2O_admitted` | `AltCrystallography.v` | η-invariant for S³/2O (binary octahedral) |
| 18 | `discrete_DP_exists_structurally` | `E8Bulk.v` | Existence of discrete Dirac operator with certain properties |
| 19 | `chirality_mechanism_unknown` | `ChiralityAnalysis.v` | Acknowledges chirality mechanism is not understood |
| 20 | `sm_cubic_anomaly_zero_per_gen` | `ThreeGenerations.v` | SM cubic anomaly cancellation per generation |

### 4. Parameters (Free variables, not claims)

| # | Parameter | File | Role |
|---|-----------|------|------|
| 21–28 | Various `Parameter : R` | `HiggsPotentialCorrected.v`, `SpectralTripleAxioms.v` | Placeholder real variables for bounds |

---

## Tally

| Category | Count | Risk Level |
|----------|-------|------------|
| Physical conclusions as Axioms | 7 | **CRITICAL** |
| Honest MATH_TODO placeholders | 8 | High (but honest) |
| CITED_MATH assumptions | 5 | Medium |
| Parameters | 8 | Low |
| **Total unproven obligations** | **28** | — |

**Note:** The remaining ~57 Axioms are duplicates across `proofs/trinity/` and `derivations/` mirrors. The unique count is approximately **28**.

---

## Comparison with Admitted Count

| Metric | Count | Notes |
|--------|-------|-------|
| Real `Admitted.` (entire repo) | 4 | All in `proofs/clifford_cl8/` |
| Real `Admitted.` (`proofs/trinity/`) | **0** | True, but misleading |
| Axiom + Parameter (entire repo) | **90** | Same epistemic function |
| Axiom + Parameter (`proofs/trinity/`) | **~57** | The real gap count |
| Unique unproven obligations | **~28** | After deduplication |

---

## Wave 20 Recommendation

**Stop advertising "0 Admitted" as a strength.** Replace with: "0 Admitted in proofs/trinity/; 28 unique unproven obligations catalogued in AXIOM_LEDGER.md, 7 of which are physical conclusions asserted without proof."

This is weaker copy but stronger science.
