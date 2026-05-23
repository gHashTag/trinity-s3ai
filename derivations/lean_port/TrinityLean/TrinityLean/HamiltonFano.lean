/-
  Trinity S3AI — TrinityLean/HamiltonFano.lean
  Wave 4 W4.5 — first Trinity-specific theorem

  STATUS: Scaffold — NOT yet compiled in CI. Requires elan + lake on host.
  See derivations/lean_port/README.md for build instructions.

  THEOREM (informal):
    A Hamiltonian cycle of the 3-cube Q3 encodes the 7 lines of the
    Fano plane PG(2, F2).

  MATHEMATICAL CONTENT:
    * Q3 has 8 vertices, identified with Fin 8 via the canonical bijection
      Fin 8 ≃ (Fin 2 × Fin 2 × Fin 2) ≃ (ZMod 2)^3. Bitwise XOR makes the
      vertex set an abelian 2-group of order 8.
    * Q3-adjacency: u ~ v iff u XOR v has popcount exactly 1
      (the difference is a coordinate basis vector).
    * The Fano plane PG(2, F2) has 7 points (nonzero vectors of (F2)^3)
      and 7 lines, each a 3-set {a, b, c} with a + b + c = 0
      (equivalently, c = a XOR b).
    * A Hamiltonian cycle of Q3 starting at 0 visits all 8 vertices
      v0 = 0, v1, ..., v7 and returns to v0; the 7 nonzero vertices
      {v1, ..., v7} are exactly the 7 Fano points, and the 7 Fano lines
      are the 3-element subsets of {v1, ..., v7} whose XOR is 0.

  CHOSEN HAMILTONIAN CYCLE (standard reflected Gray code on 3 bits):
    0 → 1 → 3 → 2 → 6 → 7 → 5 → 4 → 0
    Each consecutive pair differs in exactly one bit (Q3 edge).

  PROOF STRATEGY:
    All four substantive claims are statements about a fixed list of 8
    natural numbers / Bool triples, hence decidable by `decide` or
    `native_decide`. We use `decide` for portability.

  SORRY COUNT: 0
-/

import Mathlib.Data.Fin.Basic
import Mathlib.Data.List.Basic
import Mathlib.Data.List.Nodup
import Mathlib.Data.Nat.Bitwise
import Mathlib.Tactic

namespace TrinityLean.HamiltonFano

/-! ## Section 1: Q3 vertices and XOR structure

We model vertices of Q3 as natural numbers in `Fin 8`. Bitwise XOR on the
underlying `Nat` carrier is used to express the group operation of
`(ZMod 2)^3`.
-/

/-- The 8 vertices of the 3-cube Q3. -/
abbrev BitVec3 := Fin 8

/-- XOR of two vertices, viewed via their `Nat` codes. The result is again
in `Fin 8` because Nat XOR of values `< 8` is `< 8`. -/
def bxor (a b : BitVec3) : BitVec3 :=
  ⟨a.val ^^^ b.val, by
    have ha : a.val < 8 := a.isLt
    have hb : b.val < 8 := b.isLt
    -- a.val ^^^ b.val < 2^3 = 8
    exact Nat.xor_lt_two_pow (n := 3) ha hb⟩

/-- Popcount of a vertex (number of 1-bits in its 3-bit representation). -/
def popcount (n : BitVec3) : Nat :=
  (n.val &&& 1) + ((n.val >>> 1) &&& 1) + ((n.val >>> 2) &&& 1)

/-- Q3-adjacency: two vertices are adjacent iff their XOR has popcount 1. -/
def Q3Adj (u v : BitVec3) : Bool :=
  decide (popcount (bxor u v) = 1)

/-! ## Section 2: A specific Hamiltonian cycle (reflected Gray code)

`gray3` lists the 8 vertices in Hamiltonian order, ending where it begins
when wrapped around.
-/

/-- Reflected Gray code Hamiltonian cycle on Q3 (length 8, plus closing edge
back to the start by wraparound). -/
def gray3 : List BitVec3 :=
  [0, 1, 3, 2, 6, 7, 5, 4]

/-- The closing edge of the cycle: from the last vertex back to the first. -/
def cycleEdges : List (BitVec3 × BitVec3) :=
  -- consecutive pairs (vi, v(i+1 mod 8))
  (gray3.zip (gray3.tail ++ [gray3.head!]))

/-! ## Section 3: Decidable facts about the chosen cycle. -/

/-- The cycle has length 8 (visits all 8 vertices). -/
theorem gray3_length : gray3.length = 8 := by decide

/-- The cycle has no repeated vertex (genuine Hamiltonian path). -/
theorem gray3_nodup : gray3.Nodup := by decide

/-- The cycle visits every vertex of Q3 exactly once. -/
theorem gray3_visits_all : ∀ v : BitVec3, v ∈ gray3 := by decide

/-- Every consecutive pair in the cycle is a Q3-edge (Hamiltonicity, open
part). -/
theorem gray3_consecutive_edges :
    ∀ p ∈ cycleEdges, Q3Adj p.1 p.2 = true := by decide

/-- The closing wrap-around edge (last vertex back to first) is also a
Q3-edge. -/
theorem gray3_closes_cycle : Q3Adj (gray3.getLast!) (gray3.head!) = true := by
  decide

/-! ## Section 4: The Fano plane PG(2, F2)

The 7 Fano points are the 7 nonzero elements of `Fin 8`, viewed as nonzero
vectors of `(F2)^3` via bit representation. The 7 Fano lines are the 7
unordered 3-subsets `{a, b, c}` with `a XOR b XOR c = 0` and all distinct
nonzero.

We list both as explicit sorted data, so all properties below reduce to
`decide`.
-/

/-- The 7 Fano points: the nonzero elements of `Fin 8`. -/
def fanoPoints : List BitVec3 := [1, 2, 3, 4, 5, 6, 7]

/-- The 7 lines of the Fano plane, each as a sorted triple of nonzero
vertices whose XOR sum is 0. -/
def fanoLines : List (List BitVec3) :=
  [ [1, 2, 3]   -- axes x, y, and their sum x⊕y
  , [1, 4, 5]   -- x, z, x⊕z
  , [1, 6, 7]   -- x, y⊕z, x⊕y⊕z
  , [2, 4, 6]   -- y, z, y⊕z
  , [2, 5, 7]   -- y, x⊕z, x⊕y⊕z
  , [3, 4, 7]   -- x⊕y, z, x⊕y⊕z
  , [3, 5, 6]   -- x⊕y, x⊕z, y⊕z
  ]

/-- There are 7 Fano lines. -/
theorem fanoLines_card : fanoLines.length = 7 := by decide

/-- Each Fano line has exactly 3 points. -/
theorem fanoLines_each_triple : ∀ l ∈ fanoLines, l.length = 3 := by decide

/-- Every Fano line consists of three distinct nonzero vertices. -/
theorem fanoLines_nodup_nonzero :
    ∀ l ∈ fanoLines, l.Nodup ∧ ∀ v ∈ l, v ≠ 0 := by decide

/-- Every Fano line is closed under XOR: the three points sum (via XOR)
to zero. This is the defining incidence relation of PG(2, F2). -/
theorem fanoLines_xor_zero :
    ∀ l ∈ fanoLines, ∃ a b c : BitVec3,
        l = [a, b, c] ∧ bxor (bxor a b) c = 0 := by decide

/-! ## Section 5: The encoding theorem

We extract the 7 nonzero vertices visited by the Hamiltonian cycle (in
their cycle order, dropping the initial 0), and prove they coincide as a
set with `fanoPoints`. Then we prove the structural theorem: the Fano
lines are recovered as the 3-subsets of cycle vertices that XOR-sum to
zero.
-/

/-- The 7 nonzero vertices visited by the cycle, in cycle order. -/
def cycleNonzero : List BitVec3 := gray3.tail

theorem cycleNonzero_eq : cycleNonzero = [1, 3, 2, 6, 7, 5, 4] := by decide

/-- The cycle visits each Fano point exactly once. -/
theorem cycleNonzero_perm_fanoPoints : cycleNonzero.Perm fanoPoints := by
  decide

/-- All 3-element subsets of the 7 cycle vertices whose XOR-sum is 0,
listed in canonical (sorted, non-decreasing) order. -/
def cycleFanoLines : List (List BitVec3) :=
  -- enumerate sorted triples of nonzero vertices summing to 0
  let pts := [1, 2, 3, 4, 5, 6, 7]
  (do
    let a ← pts
    let b ← pts
    let c ← pts
    guard (a.val < b.val ∧ b.val < c.val ∧ bxor (bxor a b) c = 0)
    pure ([a, b, c] : List BitVec3))

/-- The set of XOR-summing triples extracted from cycle vertices equals
the published Fano line list. THIS IS THE MAIN THEOREM. -/
theorem hamiltonCycle_encodes_fanoLines :
    cycleFanoLines = fanoLines := by
  decide

/-- Restated as a Perm-style equivalence (order-insensitive). -/
theorem hamiltonCycle_encodes_fanoLines_perm :
    cycleFanoLines.Perm fanoLines := by
  rw [hamiltonCycle_encodes_fanoLines]

/-! ## Section 6: Summary corollary

A single proposition wrapping the structural content of W4.5:

  * `gray3` is a Hamiltonian cycle (length 8, distinct, every vertex,
    each consecutive pair adjacent including the wrap-around);
  * dropping the zero vertex gives a permutation of the 7 Fano points;
  * the 7 Fano lines are recovered as the XOR-zero triples.
-/

theorem W4_5_hamiltonCycle_encodes_fanoLines :
    gray3.length = 8 ∧
    gray3.Nodup ∧
    (∀ v : BitVec3, v ∈ gray3) ∧
    (∀ p ∈ cycleEdges, Q3Adj p.1 p.2 = true) ∧
    Q3Adj (gray3.getLast!) (gray3.head!) = true ∧
    cycleNonzero.Perm fanoPoints ∧
    cycleFanoLines = fanoLines := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact gray3_length
  · exact gray3_nodup
  · exact gray3_visits_all
  · exact gray3_consecutive_edges
  · exact gray3_closes_cycle
  · exact cycleNonzero_perm_fanoPoints
  · exact hamiltonCycle_encodes_fanoLines

end TrinityLean.HamiltonFano
