import TrinityLean.KODimension
import TrinityLean.QuaternionicLinearity
import TrinityLean.H4RootSystem

/-!
# TrinityLean — Lean 4 Port of Trinity S³AI Structures

This package contains basic formalisations of the algebraic structures
underlying the Trinity S³AI framework:

* `TrinityLean.KODimension` — KO-dimension signs for real spectral triples
* `TrinityLean.QuaternionicLinearity` — quaternionic structure and norm theory
* `TrinityLean.H4RootSystem` — Wave 4 W4.1: H₄ as the anchor for a
  mathlib4 `RootSystem` instance. The Coxeter matrix is re-exported
  from mathlib, cardinality facts (4 simples, 120 roots, Coxeter
  number 30, Weyl order 14400) are recorded, and the full `RootSystem`
  witness is staked out as the target of the follow-up PR.
-/
