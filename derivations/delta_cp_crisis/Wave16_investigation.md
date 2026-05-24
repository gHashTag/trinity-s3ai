# Wave 16 Investigation: The δ_CP Crisis

**Date:** 2026-05-23  
**Mandate:** Search for alternative δ_CP formulas from the H4/Coxeter/φ formalism that agree with modern experimental data (NuFit 6.0–6.1, T2K 2025, JUNO 2025).  
**Principle:** «Do not lie» — do not invent derivations.

---

## 1. Current Trinity Formula and Its Derivation

### 1.1 Definition

In `proofs/trinity/MixingOrigins.v` (line 51):

```coq
Definition delta_CP_formula : R := 3 / (phi * phi).
```

In `proofs/trinity/Predictions.v` (line 35):

```coq
Definition delta_CP_pred : R := 3 / phi^2.
```

In `proofs/trinity/Bounds_Mixing.v` (line 46):

```coq
Definition N04_formula_rad : R := 3 / (phi * phi).
```

### 1.2 Numerical Value

| Quantity | Value |
|----------|-------|
| `3 / φ²` (rad) | 1.145898… |
| `3 / φ²` (deg) | **65.6551°** |

### 1.3 Honest Derivation Status

**There is NO first-principles derivation of δ_CP = 3/φ² from H4 group theory.**

The `MixingOrigins.v` file is explicitly tagged `[phenomenological_fit]` and contains the following honest annotation (line 14–15):

> "formulas in this file are empirical fits of phi/pi/e combinations to PDG values. NOT first-principles derivations."

The theorem `delta_CP_acute` (line 169) only proves that 0 < 3/φ² < π/2 — a trivial numerical bound. The theorem `CKM_gamma_equals_delta_CP` (line 322) is Admitted with the comment:

> "The claim that both PMNS delta_CP and CKM gamma equal 3/phi^2 is either: (a) a remarkable H4 geometric coincidence, or (b) an accidental numerical fit with 2 free parameters. We CANNOT distinguish (a) from (b) without a group-theoretic derivation."

### 1.4 Historical Evolution

The δ_CP "prediction" has changed **three times** in the project's history, each time retro-fitted to shifting experimental central values:

| Version | Formula | Value | Status |
|---------|---------|-------|--------|
| v3.3 | `arcsin(8/φπ)` | ~90.2° | Excluded |
| v3.4 | `e/2` | ~77.87° | Excluded at 7.7σ |
| v3.5+ | `3/φ²` | **65.66°** | Current |

The `delta_cp_analysis.md` document confirms that the 3/φ² formula was selected from a brute-force search of **72,600 combinations** of the form `a · φ^b · π^c · e^d`. The best numerical fit was actually `4·φ⁻²·π⁻²·e² = 65.5385°` (0.02σ), but `3/φ² = 65.6551°` (0.10σ) was chosen for "elegance."

---

## 2. The Crisis: Modern Experimental Data

The `Bounds_Mixing.v` file cites an **outdated** experimental value:

```coq
Definition delta_CP_experimental_center : R := 65.5.  (* PDG 2024 combined T2K+NOvA+Daya Bay *)
Definition delta_CP_experimental_uncertainty : R := 4.
```

This ±4° uncertainty is now completely superseded. Modern global fits (2024–2025) give:

| Experiment | δ_CP best fit | 1σ uncertainty | Distance from 65.66° |
|------------|---------------|----------------|----------------------|
| NuFit 6.0 (NO, without SK) | **~177°** | ±20° | **5.6σ** |
| NuFit 6.0 (NO, with SK) | **~212°** | ±26° / −41° | **~4–6σ** |
| NuFit 6.1 + JUNO | **~212°** | (tighter) | **~5–6σ** |
| T2K 2025 + NOvA (Nature Oct 2025) | **~270°** (IO preferred) | ±~20° | **~10σ** |

The project's own documents acknowledge this crisis:
- `README_v46.md`: "δ_CP = 65.66° vs ~177° — 5.6σ tension. DUNE 2028 decides. No theoretical fix available without breaking other predictions"
- `LAGRANGIAN_HONEST_STATUS.md`: "δ_CP = 65.66° prediction is excluded by NuFIT-6.0"
- `DUNE_RISKY_PREDICTION.md`: "Trinity's prediction of 65.66 degrees is in the opposite quadrant from the current best fit"

---

## 3. Phase Convention Check

In the PDG-standard PMNS parameterization, δ_CP is defined in `[0, 2π)`. There is **no convention** under which 65.66° maps to ~180°, ~212°, or ~270°:

| Operation | Result | Matches experiment? |
|-----------|--------|---------------------|
| `3/φ²` | 65.66° | ❌ No |
| `π − 3/φ²` | 114.34° | ❌ No |
| `π + 3/φ²` | 245.66° | ❌ No (diff 33° from 212°, 24° from 270°) |
| `2π − 3/φ²` | 294.34° | ❌ No (diff 24° from 270°) |
| `π/2 + 3/φ²` | 155.66° | ❌ No |
| `3π/2 − 3/φ²` | 204.34° | ❌ No (diff 8° from 212°, closest but no derivation) |

The only mapping that comes within ~10° of any experimental value is `3π/2 − 3/φ² ≈ 204.34°` (7.7° from 212°), but this has **no geometric motivation** in H4 theory and was never proposed in any project document.

---

## 4. Systematic Search for Alternative Formulas

### 4.1 Search Strategy

We tested **>7,000 closed-form expressions** built from the H4/Coxeter/φ invariants:
- Constants: φ, 1/φ, φ², φ³, π, e, and their powers
- H4 structural numbers: h=30, degrees {2,12,20,30}, |H4|=14400, |2I|=120
- Operations: +, −, ×, ÷, sqrt, arcsin, arccos, arctan, ln
- Integer coefficients: 1–20

Targets:
- **180°** — CP-conserving, NuFit 6.0 NO (without SK)
- **212°** — NuFit 6.1 with JUNO
- **270°** — ~−90°, NuFit 6.0 IO / T2K 2025

### 4.2 Results: Closest Numerical Accidents

#### Target: 180°

| Rank | Formula | Value | Δ from 180° | H4 Derivation? |
|------|---------|-------|-------------|----------------|
| 1 | `e² − φ³` | 181.185° | +1.185° | **None** |
| 2 | `3·e/φ²` | 178.469° | −1.531° | **None** |
| 3 | `π/2 + φ` | 182.707° | +2.707° | **None** |
| 4 | `π²/(2φ)` | 174.745° | −5.255° | **None** |
| 5 | `e·π/φ²` | 186.892° | +6.892° | **None** |

**Verdict:** No formula from the H4 invariants lands within 1° of 180°. The closest accidental hit (`e² − φ³`) has no Coxeter geometric meaning.

#### Target: 212°

| Rank | Formula | Value | Δ from 212° | H4 Derivation? |
|------|---------|-------|-------------|----------------|
| 1 | `e²/2` | 211.681° | −0.319° | **None** |
| 2 | `2π − φ²` | 209.998° | −2.002° | **None** |
| 3 | `π + 1/φ` | 215.411° | +3.411° | **None** |
| 4 | `π²/φ²` | 215.997° | +3.997° | **None** |
| 5 | `3π/φ²` | 206.262° | −5.738° | **None** |

**Verdict:** `e²/2` is remarkably close (0.3°), but it is a pure numerological accident — Euler's number squared has no known connection to H4 Coxeter geometry. `π²/φ²` (4° away) and `3π/φ²` (5.7° away) involve the project's constants but have never been derived from group theory.

#### Target: 270°

| Rank | Formula | Value | Δ from 270° | H4 Derivation? |
|------|---------|-------|-------------|----------------|
| 1 | `2π − φ` | 267.294° | −2.707° | **None** |
| 2 | `π + φ` | 272.707° | +2.707° | **None** |
| 3 | `e² − φ²` | 273.359° | +3.359° | **None** |
| 4 | `√π · φ²` | 265.872° | −4.128° | **None** |
| 5 | `ln(120)` | 274.303° | +4.303° | **None** |

**Verdict:** `2π − φ` and `π + φ` are symmetrically placed ±2.7° from 270°, but again these are numerological accidents with no H4 derivation. Trivially, `3π/2 = 270°` exactly, but this is just a right angle — it has no special connection to the 600-cell or H4 invariants.

### 4.3 Notable Misses

Several formulas mentioned in `IMPROVEMENT_PLAN.md` were checked:

| Claimed in IMPROVEMENT_PLAN | Actual value | Δ from target | Assessment |
|-----------------------------|--------------|---------------|------------|
| `π − 3/φ² ≈ 171.6°` | 114.34° | — | **Computational error in plan** (subtracted degrees from radians or similar) |
| `π + φ ≈ 176.2°` | 272.71° | — | **Computational error in plan** |

The plan's arithmetic appears to have mixed radian and degree values in places.

---

## 5. Structural Obstacles to Any Fix

### 5.1 The Formula Is Hard-Coded in Multiple Files

`3/φ²` appears in at least **6 separate files**:

| File | Line | Context |
|------|------|---------|
| `proofs/trinity/MixingOrigins.v` | 51 | `delta_CP_formula` |
| `proofs/trinity/Predictions.v` | 35 | `delta_CP_pred` |
| `proofs/trinity/Bounds_Mixing.v` | 46 | `N04_formula_rad` |
| `Catalog42_corrected.v` | 199 | `delta_CP_pred` (DUNE 2030) |
| `trinity_rust/src/mixing.rs` | 118 | `delta_cp()` function |
| `delta_cp_analysis.md` | 54 | Historical justification |

### 5.2 The CKM γ Angle Is Locked to the Same Value

`MixingOrigins.v` (line 322) explicitly identifies CKM γ with δ_CP:

> "Trinity identifies gamma = 3/phi^2 = 65.66 degrees"

Changing δ_CP without also changing γ would break the project's claimed "quark-lepton unification." PDG 2024 gives γ = 65.9° ± 3.4°, so 65.66° **does** match the quark sector well. The problem is that the lepton sector (PMNS δ_CP) no longer agrees with this value.

### 5.3 The 3/φ² Formula Is Embedded in the Jarlskog Computation

`DUNE_RISKY_PREDICTION.md` and `delta_cp_analysis.md` compute the leptonic Jarlskog invariant using sin(65.66°). Any change to δ_CP would change |J_Trinity| and potentially destroy the agreement with experiment in that observable as well.

### 5.4 The Experimental Data The Formula Was Fitted to Is Now Obsolete

The `Bounds_Mixing.v` theorem `N04_within_experimental_range` (line 82) proves:

```coq
Rabs (N04_formula_deg - 65.5) < 4
```

This relied on PDG 2024's combined T2K+NOvA+Daya Bay fit (65.5° ± 4°). That central value has **shifted by more than 110°** in subsequent global analyses. The project's Coq proof is therefore formally proving agreement with an experimental value that the physics community no longer considers valid.

---

## 6. Conclusion

### 6.1 Is There a Fix?

**No.**

After exhaustive search:
- **No H4-derived formula** evaluates to ~180°, ~212°, or ~270°.
- The closest **numerical accidents** (`e²/2 ≈ 211.7°`, `π + 1/φ ≈ 215.4°`, `2π − φ ≈ 267.3°`) are within 0.3°–5° of experimental values, but **none have any geometric derivation** from the 600-cell, H4 root system, or Coxeter invariants.
- **No phase convention** maps 65.66° to the experimentally favored region.
- The project itself has already stated in `README_v46.md`: "No theoretical fix available without breaking other predictions."

### 6.2 Honest Assessment

The δ_CP = 3/φ² = 65.66° formula is:
1. A **phenomenological fit** to outdated data (PDG 2024 T2K+NOvA+Daya Bay, 65.5° ± 4°).
2. **Excluded at >5σ** by modern global fits (NuFit 6.0–6.1, JUNO 2025).
3. **Deeply embedded** in the project's CKM-PMNS structure (linked to γ angle, Jarlskog invariant).
4. **Not derivable** from H4 group theory — admitted as conjectural in the Coq sources.

### 6.3 Recommendation

| Option | Action | Scientific Integrity |
|--------|--------|---------------------|
| A | **Retract the δ_CP prediction** and state clearly that the PMNS sector prediction is WITHDRAWN (>5σ excluded by current data) | ✅ High — follows «do not lie» |
| B | Wait for DUNE 2028 and maintain the pre-registered 65.66° as a falsifiable claim | ✅ Acceptable — if honestly framed as "already disfavored" |
| C | Invent a new post-hoc formula (e.g., `e²/2`) and claim it was "hidden in H4" | ❌ Unacceptable — would be the 4th retro-fit |

**Recommended action:** The project should update `Bounds_Mixing.v` to acknowledge that the 65.5° ± 4° experimental bound is obsolete, and add an explicit HONEST comment that the δ_CP prediction is in **>5σ crisis** with modern data. If DUNE 2028 confirms ~180°–212°, the PMNS sector prediction should be formally retracted.

---

*Investigation completed. No alternative formula found. No fake derivations invented.*
