# Ancillary files for arXiv submission

This directory contains the machine-verified proofs referenced in the paper
"Z_3 tripartition of the snub 24-cell as a flavour structure".

## Files

### Snub24CellZ3.v (Coq)
- **Language:** Coq 8.18+ (depends on Trinity.CorePhi, Trinity.QuaternionicLinearity)
- **Content:** Formalises the binary icosahedral group 2I, the binary tetrahedral
  subgroup 2T, the order-3 generator g = (-1/2, 1/2, 1/2, 1/2), and the free
  Z_3 action on the 96 snub vertices. Proves the canonical tripartition
  96 = 32 + 32 + 32 via orbit-stabiliser arithmetic.
- **Status:** Arithmetic and structural theorems are complete (Qed). Heavy
  group-theoretic lemmas (subgroup structure, freeness proof) are stated as
  structural placeholders with honest comments documenting the gap.
- **Repository:** https://github.com/gHashTag/trinity-s3ai (commit d883275)

### Snub24Z3.lean (Lean 4)
- **Language:** Lean 4 / mathlib4
- **Content:** Independent formalisation using Fin 32 x Fin 3 as a labelled model
  of the snub 24-cell with Z_3 action. Proves freeness, the three partition sets
  G_0, G_1, G_2, their cardinalities (32 each), pairwise disjointness, union =
  whole set, and cyclic permutation by the generator. All theorems are closed by
  `decide` with 0 sorries and 0 axioms.
- **Status:** Complete. The labelled model is isomorphic to the quaternionic
  model verified numerically in the companion Python script.
- **Repository:** https://github.com/gHashTag/trinity-s3ai (commit 916bc6e)

## How to check

### Coq
```bash
coqtop -l Snub24CellZ3.v
```
(Requires the Trinity S^3AI Coq library installed.)

### Lean 4
```bash
cd TrinityLean
lake build
```
(Requires elan and mathlib4. See derivations/lean_port/README.md in the repo.)

## License

These files are released under the same license as the Trinity S^3AI project
(see the main repository LICENSE file).
