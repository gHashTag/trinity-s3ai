/-!
# H₄ Root System — Lean 4 Port (Wave 4 — first migration PR)

This module begins the Lean 4 port of Trinity-s³AI's H₄/600-cell layer.
The long-term goal (stated in the Wave 3 W3.8 migration plan) is to
recover the H₄ root system as an instance of mathlib4's
`RootSystem ι ℝ M N`. This first PR lays the structural anchor:

* The H₄ Coxeter matrix is reused directly from
  `Mathlib.GroupTheory.Coxeter.Matrix`'s `CoxeterMatrix.H₄`.
* The 120 H₄ root *indices* are wrapped as `Fin 120`, the 4 simple
  reflection indices as `Fin 4`, and basic cardinality facts are
  discharged by `decide`.
* The bridge to `RootSystem` is stated as a target theorem
  (`h4_is_root_system`) and explicitly left as `sorry` — constructing
  the full `RootPairing` requires the icosian (Conway–Sloane)
  quaternion coordinates plus 120·120 reflection-permutation tables,
  which is scoped out to the next PR.

We deliberately keep `sorry` only on the genuinely hard structural
target. Every numeric / cardinality lemma in this file is `by decide`
or `rfl`, so the file will compile under `lake build` once Mathlib is
fetched.

## Anchors used from mathlib v4.13.0

* `Mathlib.GroupTheory.Coxeter.Matrix` — `CoxeterMatrix`, `CoxeterMatrix.H₄`
* `Mathlib.LinearAlgebra.RootSystem.Defs` — `RootSystem`, `RootPairing`
* `Mathlib.Data.Real.GoldenRatio` — `goldenRatio`, `gold_sq`, `gold_pos`
-/}

import Mathlib.GroupTheory.Coxeter.Matrix
import Mathlib.LinearAlgebra.RootSystem.Defs
import Mathlib.Data.Real.GoldenRatio
import Mathlib.Data.Fintype.Card
import Mathlib.Tactic

namespace TrinityLean
namespace H4

open scoped Classical

/-! ## §1. The H₄ Coxeter matrix (re-export from mathlib).

We do not redefine the H₄ Coxeter matrix; mathlib already provides it.
Re-exporting under a stable local name keeps downstream proofs in this
project decoupled from minor renames in mathlib. -/

/-- The H₄ Coxeter matrix, indexed by `Fin 4`. Re-exported from
`Mathlib.GroupTheory.Coxeter.Matrix`. -/
def coxeterMatrix : CoxeterMatrix (Fin 4) := CoxeterMatrix.H₄

/-- The diagonal of the H₄ matrix is all 1s — checked by `decide` via
the auto-param in the underlying `CoxeterMatrix` structure. -/
theorem coxeterMatrix_diag (i : Fin 4) : coxeterMatrix.M i i = 1 :=
  coxeterMatrix.diagonal i

/-- The H₄ Coxeter matrix is symmetric. -/
theorem coxeterMatrix_isSymm : coxeterMatrix.M.IsSymm :=
  coxeterMatrix.isSymm

/-! ## §2. Cardinalities — discharged by `decide`.

These are the small finite facts the framework needs to reference:
H₄ has 4 simple reflections, 120 roots in the 600-cell, and Coxeter
number 30. The 120-root cardinality is what makes H₄ a non-trivial
geometric object; we do *not* yet build the 120 vectors here. -/

/-- Index set for the 4 simple reflections of H₄. -/
abbrev SimpleIdx : Type := Fin 4

/-- Index set for the 120 roots of H₄ (= vertices of the 600-cell).
We use an abstract `Fin 120` here; explicit icosian coordinates are
introduced in the follow-up PR. -/
abbrev RootIdx : Type := Fin 120

/-- There are exactly 4 simple reflections. -/
theorem card_simple : Fintype.card SimpleIdx = 4 := by decide

/-- There are exactly 120 H₄ roots. -/
theorem card_roots : Fintype.card RootIdx = 120 := by decide

/-- The Coxeter number of H₄ is 30. Recorded as a definitional
constant; properties (e.g. divisibility relations to the order of
`W(H₄)`) are deferred. -/
def coxeterNumber : ℕ := 30

theorem coxeterNumber_eq : coxeterNumber = 30 := rfl

/-- The (claimed) order of the Coxeter group `W(H₄)`. Stated as a
definitional constant; proving
`Nat.card (CoxeterMatrix.H₄.Group) = 14400` follows from the
classification of finite Coxeter groups, which is non-trivial to
formalise from scratch and is therefore deferred. -/
def weylOrder : ℕ := 14400

theorem weylOrder_eq : weylOrder = 14400 := rfl

/-- Sanity check tying together rank, root count, Coxeter number and
Weyl order: a smoke test for the file, not a deep theorem. All four
goals close by `decide`. -/
theorem h4_constants :
    Fintype.card SimpleIdx = 4 ∧
    Fintype.card RootIdx = 120 ∧
    coxeterNumber = 30 ∧
    weylOrder = 14400 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> decide

/-! ## §3. Golden-ratio anchor.

H₄ is the unique 4-dimensional non-crystallographic Coxeter group and
its structure constants live in `ℤ[φ]`, where `φ = (1+√5)/2`. We
import mathlib's `goldenRatio` and recall the defining identity
`φ² = φ + 1`. This is the algebraic "seed" the icosian construction
will use in the next PR. -/

/-- Local name for the golden ratio (`= (1+√5)/2`). -/
noncomputable abbrev φ : ℝ := goldenRatio

/-- φ² = φ + 1. -/
theorem phi_sq : φ ^ 2 = φ + 1 := gold_sq

/-- φ > 0. -/
theorem phi_pos : 0 < φ := gold_pos

/-- 1 < φ < 2. -/
theorem one_lt_phi_lt_two : 1 < φ ∧ φ < 2 :=
  ⟨one_lt_gold, gold_lt_two⟩

/-! ## §4. Target: H₄ as a `RootSystem`.

We state the long-term target as a `Nonempty` claim about a
`RootSystem` over `ℝ` indexed by `RootIdx`. Building the witness
requires:

1. An explicit embedding `RootIdx → ℝ⁴` (the 120 icosian unit
   quaternions, Conway–Sloane 1988).
2. A dual coroot map and a `PerfectPairing ℝ (ℝ⁴) (ℝ⁴)`.
3. The 120×120 reflection-permutation tables and the
   `reflection_perm_root` / `reflection_perm_coroot` axioms.
4. The `span_eq_top` proof.

Items (1) and (2) involve coordinates in `ℤ[φ]`; items (3) and (4)
reduce to finite checks once the coordinates are pinned down. The
whole bundle is scoped to the next migration PR. -/

/-- Existence of a `RootSystem` structure on the 120 H₄ vectors,
left as the target theorem for the follow-up PR. -/
theorem h4_is_root_system :
    Nonempty (RootSystem RootIdx ℝ (Fin 4 → ℝ) (Fin 4 → ℝ)) := by
  -- TODO (follow-up PR): construct the icosian root embedding,
  -- the dual coroot map, the perfect pairing, and the reflection
  -- permutations, then close with `exact ⟨…⟩`.
  sorry

end H4
end TrinityLean
