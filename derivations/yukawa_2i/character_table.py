#!/usr/bin/env python3
"""
Wave 9.2: Character table of 2I (binary icosahedral group) and Clebsch-Gordan coefficients.

2I = SL(2, F_5) = Binary Icosahedral Group, |2I| = 120
9 conjugacy classes, 9 irreps with dimensions: 1, 2, 2', 3, 3', 4, 4', 5, 6
McKay correspondence: affine E_8 diagram

Character table verified (all 81 orthogonality relations satisfied):
  - ρ1(1), ρ4(3), ρ5(3'), ρ8(5), ρ9(6): real (self-dual) reps
  - ρ2(2), ρ3(2'): Galois conjugate pair (related by φ ↔ -1/φ automorphism)
  - ρ4(3), ρ5(3'): Galois conjugate pair (same automorphism)
  - ρ6(4): lifts from A5 = 2I/{±1} (central element acts as +I)
  - ρ7(4'): Sym^3 of fundamental (central element acts as -I)

References:
  - GAP: CharacterTable("2.A5")
  - Ludl (2010), arXiv:1101.2308
  - Conway & Smith, "On Quaternions and Octonions" (2003)
"""

import numpy as np
import json, os

phi = (1 + np.sqrt(5)) / 2  # golden ratio ≈ 1.618033

# ============================================================
# Conjugacy classes of 2I (ATLAS ordering for 2.A5)
# ============================================================
class_labels = ['1A', '2A', '3A', '4A', '5A', '5B', '6A', '10A', '10B']
class_sizes  = [1,    1,    20,   30,   12,   12,   20,   12,    12   ]
class_orders = [1,    2,    3,    4,    5,    5,    6,    10,    10   ]
G_order = 120
n_classes = 9

assert sum(class_sizes) == G_order

# ============================================================
# 9 Irreducible representations
# ============================================================
# Dimensions: 1, 2, 2', 3, 3', 4, 4', 5, 6
# All character values verified: Σ_c |C_c| |χ_i(c)|^2 = |G| for each i
#                                 Σ_i |χ_i(c)|^2 = |G|/|C_c| for each c

irrep_names = ['ρ1(1)', 'ρ2(2)', "ρ3(2')", 'ρ4(3)', "ρ5(3')", 'ρ6(4)', "ρ7(4')", 'ρ8(5)', 'ρ9(6)']
irrep_dims  = [1,       2,       2,         3,       3,         4,       4,         5,       6      ]

# Character values (columns = ATLAS classes 1A,2A,3A,4A,5A,5B,6A,10A,10B):
ct = np.array([
    # ρ1(1): trivial
    [1,  1,  1,  1,   1,       1,      1,   1,       1     ],
    # ρ2(2): fundamental spin-1/2 rep (Sym^1 of SU(2) restricted to 2I)
    [2, -2, -1,  0,  -phi,     1/phi,  1,   phi,    -1/phi ],
    # ρ3(2'): Galois conjugate of ρ2 (φ ↔ -1/φ swaps 5A↔5B and 10A↔10B)
    [2, -2, -1,  0,   1/phi,  -phi,   1,  -1/phi,   phi   ],
    # ρ4(3): spin-1 rep (Sym^2 of fundamental)
    [3,  3,  0, -1,   phi,    -1/phi,  0,   phi,    -1/phi ],
    # ρ5(3'): Galois conjugate of ρ4
    [3,  3,  0, -1,  -1/phi,  phi,    0,  -1/phi,   phi   ],
    # ρ6(4): 4-dim rep lifting from A5=2I/{±1} (central element → +I)
    [4,  4,  1,  0,  -1,     -1,      1,  -1,      -1     ],
    # ρ7(4'): Sym^3 of fundamental (central element → -I)
    [4, -4,  1,  0,  -1,     -1,     -1,   1,       1     ],
    # ρ8(5): spin-2 rep (Sym^4)
    [5,  5, -1,  1,   0,      0,     -1,   0,       0     ],
    # ρ9(6): spin-5/2 rep (Sym^5)
    [6, -6,  0,  0,   1,      1,      0,  -1,      -1     ],
], dtype=float)

# ============================================================
# Verification
# ============================================================
def ip(a, b):
    return sum(class_sizes[c]*a[c]*b[c] for c in range(n_classes)) / G_order

print("="*80)
print("CHARACTER TABLE OF 2I = SL(2,F₅)  |2I| = 120")
print("McKay correspondence: affine E₈ diagram")
print("="*80)

# Burnside
burnside = sum(d**2 for d in irrep_dims)
print(f"\nBurnside: Σ dim² = {'+'.join(str(d**2) for d in irrep_dims)} = {burnside} = |2I| {'✓' if burnside==G_order else '✗'}")

# Row orthogonality
row_ok = True
for i in range(9):
    v = ip(ct[i], ct[i])
    ok = abs(v-1.0) < 1e-10
    if not ok: row_ok = False
print(f"Row orthogonality (⟨χᵢ,χᵢ⟩=1, ⟨χᵢ,χⱼ⟩=0): {'✓ all correct' if row_ok else '✗'}")

cross_ok = True
for i in range(9):
    for j in range(i+1, 9):
        v = ip(ct[i], ct[j])
        if abs(v) > 1e-10:
            cross_ok = False
            print(f"  ⟨ρ{i+1},ρ{j+1}⟩ = {v:.6f} ✗")
print(f"Cross orthogonality: {'✓ all correct' if cross_ok else '✗'}")

# Column orthogonality
col_ok = True
for c in range(n_classes):
    v = sum(ct[i,c]**2 for i in range(9))
    exp = G_order / class_sizes[c]
    if abs(v - exp) > 1e-8:
        col_ok = False
        print(f"  Col {class_labels[c]}: {v:.4f} ≠ {exp:.4f} ✗")
print(f"Column orthogonality (Σᵢ|χᵢ(c)|²=|G|/|Cᵢ|): {'✓ all correct' if col_ok else '✗'}")

# Print table
print(f"\n{'Irrep':<12}", end="")
for lbl, sz in zip(class_labels, class_sizes):
    print(f"  {lbl}[{sz}]".rjust(12), end="")
print()
print("-"*112)
for i in range(9):
    print(f"{irrep_names[i]:<12}", end="")
    for c in range(n_classes):
        print(f"  {ct[i,c]:+.4f}".rjust(12), end="")
    print()

# ============================================================
# Clebsch-Gordan decompositions
# ============================================================
def cg_decompose(i, j):
    chi_prod = ct[i] * ct[j]
    return [round(ip(chi_prod, ct[k])) for k in range(9)]

def format_cg(mults):
    parts = [f"{m}·{irrep_names[k]}" if m > 1 else irrep_names[k]
             for k, m in enumerate(mults) if m > 0]
    return " ⊕ ".join(parts) if parts else "0"

print(f"\n{'='*80}")
print("CLEBSCH-GORDAN DECOMPOSITIONS")
print("="*80)

key_pairs = [
    (1,1), (1,2), (2,2),    # 2⊗2, 2⊗2', 2'⊗2'
    (1,3), (1,4), (2,3),    # 2⊗3, 2⊗3', 2'⊗3
    (3,3), (3,4), (4,4),    # 3⊗3, 3⊗3', 3'⊗3'
    (5,5), (5,6), (6,6),    # 4⊗4, 4⊗4', 4'⊗4'
    (7,7), (1,7), (3,5),    # 5⊗5, 2⊗5, 3⊗4
    (3,7), (7,5),           # 3⊗5, 5⊗4
]

cg_table = {}
all_cg_ok = True
for i, j in key_pairs:
    mults = cg_decompose(i, j)
    d_out = sum(mults[k]*irrep_dims[k] for k in range(9))
    d_exp = irrep_dims[i]*irrep_dims[j]
    ok = d_out == d_exp
    if not ok: all_cg_ok = False
    label = f"{irrep_names[i]}⊗{irrep_names[j]}"
    cg_table[label] = mults
    print(f"  {label:<30} = {format_cg(mults)}")
    print(f"    dim: {irrep_dims[i]}×{irrep_dims[j]}={d_exp} vs {d_out} {'✓' if ok else '✗'}")

# ============================================================
# Regular representation structure
# ============================================================
print(f"\n{'='*80}")
print("REGULAR REPRESENTATION: ℓ²(2I) ≅ ⊕ᵢ (dim ρᵢ)·ρᵢ")
print("="*80)
total = 0
for i in range(9):
    d = irrep_dims[i]
    total += d*d
    print(f"  {irrep_names[i]}: multiplicity {d}, dim contribution {d}² = {d*d}")
print(f"  Total: {' + '.join(str(d**2) for d in irrep_dims)} = {total} = |2I| {'✓' if total==G_order else '✗'}")

print("""
SCHUR'S LEMMA (THE KEY THEOREM):
  Any 2I-equivariant linear map T: ℓ²(2I)→ℓ²(2I) decomposes as:
    T = ⊕ᵢ (Tᵢ ⊗ Id_{dim ρᵢ})
  where Tᵢ is a (dim ρᵢ)×(dim ρᵢ) matrix acting on the multiplicity space.

  For D_F BUILT purely from 2I-equivariant structure:
    D_F|_{isotypic(ρᵢ)} = λᵢ · Id_{(dim ρᵢ)²}
  All (dim ρᵢ)² eigenvalues within each isotypic block are EQUAL.
  
  CONCLUSION: A purely 2I-equivariant D_F has only 9 distinct eigenvalues
  (one per irrep), with multiplicities dim²(ρᵢ). This matches Wave 8.4 findings.
  Mass hierarchies CANNOT emerge without explicit symmetry breaking.
""")

# ============================================================
# Physical implications for 3-generation structure
# ============================================================
print("="*80)
print("3-GENERATION STRUCTURE FROM 2I IRREPS")
print("="*80)
print("""
Three 3-dim irreps: NONE — 2I has only TWO 3-dim irreps: ρ4(3) and ρ5(3').
Two 2-dim irreps: ρ2(2) and ρ3(2') — gives at most 2 "generation-like" multiplicities.

From ρ4(3)⊗ρ4(3) = ρ1(1) ⊕ ρ4(3) ⊕ ρ8(5):
  → 3×3=9 dimensional product, contains a 3-dim component.
  → If we identify ρ4(3) with "lepton doublet space", 
    the Clebsch-Gordan decomposition of Y = (Higgs ⊗ ρ4)·ψ gives:
    allowed Yukawa from singlet (1), triplet (3), quintet (5) Higgs.

The 3 generations in NCG/SM come from a SEPARATE generation index (not from 2I alone).
The 2I symmetry organizes FLAVOR, not generation number.
Without an external 3-dimensional generation space, 2I cannot produce 3 mass eigenvalues.
""")

# ============================================================
# Save results
# ============================================================
results = {
    "group": "2I = SL(2,F5) = Binary Icosahedral Group",
    "order": G_order,
    "n_classes": n_classes,
    "n_irreps": 9,
    "class_sizes": class_sizes,
    "class_orders": class_orders,
    "class_labels": class_labels,
    "irrep_dims": irrep_dims,
    "irrep_names": irrep_names,
    "burnside_sum": burnside,
    "burnside_ok": bool(burnside == G_order),
    "row_orthogonality_ok": bool(row_ok and cross_ok),
    "col_orthogonality_ok": bool(col_ok),
    "cg_ok": bool(all_cg_ok),
    "character_table": ct.tolist(),
    "phi": float(phi),
    "cg_decompositions": {k: v for k, v in cg_table.items()},
    "physics_conclusion": (
        "2I has 9 irreps: 1,2,2',3,3',4,4',5,6. Burnside: 120=|2I|. "
        "Schur's lemma: purely 2I-equivariant D_F is scalar on each isotypic block. "
        "Mass hierarchies require explicit 2I-symmetry breaking via Yukawa/Higgs. "
        "2I has no 3-copies of any single irrep — cannot naturally give 3 generations."
    )
}

out_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(out_dir, 'character_table_results.json'), 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nSaved → character_table_results.json")
print(f"All orthogonality verified: row={row_ok and cross_ok}, col={col_ok}, CG_dims={all_cg_ok}")
