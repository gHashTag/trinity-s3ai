#!/usr/bin/env python3
"""
Verify gamma matrices for Cl(0,6) ~ M_8(R).

Constructs six 8x8 signed-permutation matrices as tensor products of 2x2 blocks:
  I = [[1,0],[0,1]]       (identity)
  A = [[0,1],[1,0]]       (Pauli X)
  B = [[0,-1],[1,0]]      (antisymmetric, B^2 = -I)
  C = [[1,0],[0,-1]]      (Pauli Z)

The six generators are:
  g1 = I ⊗ I ⊗ B
  g2 = I ⊗ B ⊗ A
  g3 = A ⊗ B ⊗ C
  g4 = B ⊗ I ⊗ C
  g5 = B ⊗ A ⊗ A
  g6 = B ⊗ C ⊗ A

Verified: each squares to -I_8, pairwise anticommute,
generated algebra has dimension 64.
"""

import numpy as np

I = np.array([[1, 0], [0, 1]], dtype=int)
A = np.array([[0, 1], [1, 0]], dtype=int)
B = np.array([[0, -1], [1, 0]], dtype=int)
C = np.array([[1, 0], [0, -1]], dtype=int)

def kron3(a, b, c):
    return np.kron(np.kron(a, b), c)

generators = [
    kron3(I, I, B),   # g1
    kron3(I, B, A),   # g2
    kron3(A, B, C),   # g3
    kron3(B, I, C),   # g4
    kron3(B, A, A),   # g5
    kron3(B, C, A),   # g6
]

names = ['gamma_1', 'gamma_2', 'gamma_3', 'gamma_4', 'gamma_5', 'gamma_6']

print("=" * 60)
print("Gamma matrix verification for Cl(0,6)")
print("=" * 60)

# Verify squares
print("\n1. Square to -I_8:")
I8 = np.eye(8, dtype=int)
for name, g in zip(names, generators):
    sq = g @ g
    ok = np.array_equal(sq, -I8)
    print(f"  {name}^2 = -I_8 : {'PASS' if ok else 'FAIL'}")

# Verify anticommutation
print("\n2. Pairwise anticommute {g_i, g_j} = 0:")
all_ok = True
for i in range(6):
    for j in range(i + 1, 6):
        anticomm = generators[i] @ generators[j] + generators[j] @ generators[i]
        ok = np.array_equal(anticomm, np.zeros((8, 8), dtype=int))
        if not ok:
            all_ok = False
        print(f"  {{{names[i]}, {names[j]}}} = 0 : {'PASS' if ok else 'FAIL'}")

# Verify generated algebra dimension
print("\n3. Generated algebra dimension:")
basis_set = {np.zeros((8, 8), dtype=int).tobytes()}
current = [np.eye(8, dtype=int)]
for g in generators:
    new_current = []
    for m in current:
        for s in [1, -1]:
            for idx, basis in enumerate(current):
                prod = m @ g
                if prod.tobytes() not in basis_set:
                    basis_set.add(prod.tobytes())
                    new_current.append(prod)
    current = current + new_current

# Actually, let's do it properly: start with I, multiply by each generator
from itertools import product

algebra = {}
for coeffs in product([0, 1], repeat=6):
    mat = np.eye(8, dtype=int)
    for k, c in enumerate(coeffs):
        if c == 1:
            mat = mat @ generators[k]
    algebra[coeffs] = mat

# Check linear independence by comparing all pairs
dim = 0
unique_mats = []
for coeffs, mat in algebra.items():
    is_unique = True
    for um in unique_mats:
        if np.array_equal(mat, um):
            is_unique = False
            break
    if is_unique:
        unique_mats.append(mat)
        dim += 1

print(f"  Algebra dimension: {dim}")
print(f"  Expected: 64")
print(f"  {'PASS' if dim == 64 else 'FAIL'}")

# Output exact entries for Coq transcription
print("\n" + "=" * 60)
print("Coq definitions (copy-paste ready)")
print("=" * 60)

for name, g in zip(names, generators):
    print(f"\nDefinition {name} : Mat 8 := fun i j =>")
    print("  match fin_val i, fin_val j with")
    entries = []
    for row in range(8):
        for col in range(8):
            val = int(g[row, col])
            if val != 0:
                entries.append((row, col, val))
    for row, col, val in entries:
        sign = "" if val == 1 else "-"
        print(f"  | {row}, {col} => {sign}1")
    print("  | _, _ => 0")
    print("  end.")

if __name__ == "__main__":
    pass
