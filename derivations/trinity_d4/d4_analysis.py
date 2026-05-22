#!/usr/bin/env python3
"""
Trinity-D4 Analysis (Wave 11.2)
================================
Discrete Dirac operator on the 24-cell (D4 roots) × 4-component spinors,
with binary tetrahedral group 2T, triality test, and KO-dimension signs.

Requirements: numpy
"""

import numpy as np
import itertools
# sympy и mpmath доступны в окружении, но явные вычисления проводятся
# на уровне NumPy для скорости и точности с плавающей точкой.
import sympy as sp
import mpmath as mp

np.set_printoptions(precision=4, suppress=True)

# ---------------------------------------------------------------------------
# 1. D4 root system (24-cell vertices)
# ---------------------------------------------------------------------------
def build_d4_roots():
    """Return the 24 roots of D4 as integer vectors in R^4."""
    roots = []
    for i, j in itertools.combinations(range(4), 2):
        for si in (1, -1):
            for sj in (1, -1):
                r = np.zeros(4, dtype=int)
                r[i] = si
                r[j] = sj
                roots.append(r)
    return np.array(roots)


# ---------------------------------------------------------------------------
# 2. Binary tetrahedral group 2T (24 unit Hurwitz quaternions)
# ---------------------------------------------------------------------------
def build_binary_tetrahedral_group():
    """Return the 24 elements of 2T as (w,x,y,z) 4-tuples."""
    units = []
    for s in (1, -1):
        units.append(np.array([s, 0, 0, 0], dtype=float))
        units.append(np.array([0, s, 0, 0], dtype=float))
        units.append(np.array([0, 0, s, 0], dtype=float))
        units.append(np.array([0, 0, 0, s], dtype=float))
    half = []
    for signs in itertools.product((1, -1), repeat=4):
        half.append(np.array(signs, dtype=float) / 2)
    return np.vstack([np.array(units), np.array(half)])


# ---------------------------------------------------------------------------
# 3. Gamma matrices (Euclidean Cl(4) representation)
# ---------------------------------------------------------------------------
def build_gamma_matrices():
    """Build Hermitian 4×4 gamma matrices satisfying {γ^a, γ^b} = 2δ^{ab}I."""
    s1 = np.array([[0, 1], [1, 0]], dtype=complex)
    s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s3 = np.array([[1, 0], [0, -1]], dtype=complex)
    i2 = np.eye(2, dtype=complex)
    g1 = np.kron(s1, i2)
    g2 = np.kron(s2, i2)
    g3 = np.kron(s3, s1)
    g4 = np.kron(s3, s2)
    return [g1, g2, g3, g4]


# ---------------------------------------------------------------------------
# 4. Discrete Dirac operator on C^{96}
# ---------------------------------------------------------------------------
def build_dirac_operator(roots, gammas):
    """
    Build the 96×96 Hermitian Dirac-like operator:
        D = i Σ_{<i,j>} c(r_j - r_i) ⊗ (E_{ij} - E_{ji})
    where the sum runs over nearest-neighbor edges of the 24-cell
    (⟨r_i, r_j⟩ = 1) and c(v) = Σ_a v_a γ^a.
    """
    n = len(roots)
    N = n * 4
    A = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            if i != j and np.dot(roots[i], roots[j]) == 1:
                A[i, j] = 1

    D = np.zeros((N, N), dtype=complex)
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j]:
                e = roots[j] - roots[i]
                ce = sum(e[a] * gammas[a] for a in range(4))
                D[i*4:(i+1)*4, j*4:(j+1)*4] += 1j * ce
                D[j*4:(j+1)*4, i*4:(i+1)*4] -= 1j * ce
    # Hermitian symmetrisation (numerical safety)
    D = (D + D.conj().T) / 2
    return D, A


# ---------------------------------------------------------------------------
# 5. Triality operator σ = P ⊗ S
# ---------------------------------------------------------------------------
def build_triality_operator(roots, gammas):
    """
    Construct the outer-automorphism σ of order 3 on C^{96}.
    The vertex permutation P is induced by the orthogonal map
        O = diag(1, R)  with R the 3×3 cycle (x,y,z) → (z,x,y).
    The spin lift S satisfies S γ^a S^{-1} = γ^{O(a)} and S^3 = I.
    """
    n = len(roots)
    N = n * 4

    # Orthogonal transformation on R^4 induced by quaternion conjugation
    # q = (1+i+j+k)/2  sends i→j→k→i.
    O = np.array([[1, 0, 0, 0],
                  [0, 0, 0, 1],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0]], dtype=int)

    # Permutation of the 24 roots
    P = np.zeros(n, dtype=int)
    for i in range(n):
        v = O @ roots[i]
        for j in range(n):
            if np.array_equal(v, roots[j]):
                P[i] = j
                break

    # Solve S γ^b S^{-1} = γ^{O(b)} for b=1..4
    g1, g2, g3, g4 = gammas
    targets = [g1, g3, g4, g2]   # O: 1→1, 2→3, 3→4, 4→2

    M_eq = np.zeros((64, 16), dtype=complex)
    for idx, (g, t) in enumerate(zip(gammas, targets)):
        for r in range(4):
            for c in range(4):
                row = idx * 16 + r * 4 + c
                for k in range(4):
                    M_eq[row, r * 4 + k] += g[k, c]
                    M_eq[row, k * 4 + c] -= t[r, k]

    U, s, Vh = np.linalg.svd(M_eq)
    null_mask = s < 1e-10
    V = Vh.conj().T
    S_vec = V[:, null_mask][:, 0]
    S_mat = S_vec.reshape((4, 4))

    # Remove the overall phase so that S^3 = I (not -I or iI)
    S3 = S_mat @ S_mat @ S_mat
    phase = S3[0, 0] ** (1.0 / 3.0)
    S_mat = S_mat / phase

    # Assemble σ
    sigma = np.zeros((N, N), dtype=complex)
    for i in range(n):
        j = P[i]
        sigma[j*4:(j+1)*4, i*4:(i+1)*4] = S_mat
    return sigma


# ---------------------------------------------------------------------------
# 6. Real structure J = (I⊗C) ∘ complex conjugation
# ---------------------------------------------------------------------------
def build_real_structure():
    """Charge-conjugation matrix C for the chosen gamma representation."""
    C = np.array([[0,  0,  0,  1],
                  [0,  0,  1,  0],
                  [0, -1,  0,  0],
                  [-1, 0,  0,  0]], dtype=complex)
    return C


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("   Trinity-D₄ Analysis  (Wave 11.2)")
    print("=" * 70)

    # --- Section 1: D4 roots ------------------------------------------------
    roots = build_d4_roots()
    print("\n[1] D4 ROOT SYSTEM")
    print(f"    Number of roots : {len(roots)}")
    norms = np.sum(roots ** 2, axis=1)
    print(f"    All <α,α> = 2  : {np.all(norms == 2)}")

    # --- Section 2: Binary tetrahedral group --------------------------------
    t2 = build_binary_tetrahedral_group()
    print("\n[2] BINARY TETRAHEDRAL GROUP 2T")
    print(f"    Order            : {len(t2)}")
    t2_norms = np.sum(t2 ** 2, axis=1)
    print(f"    All ||q||² = 1  : {np.allclose(t2_norms, 1)}")

    # --- Section 3: 24-cell adjacency & Dirac operator ----------------------
    gammas = build_gamma_matrices()
    D, A = build_dirac_operator(roots, gammas)
    print("\n[3] 24-CELL & DISCRETE DIRAC OPERATOR")
    print(f"    Vertex degree    : {np.unique(np.sum(A, axis=1))[0]} (expected 8)")
    print(f"    D shape          : {D.shape}")
    print(f"    D is Hermitian   : {np.allclose(D, D.conj().T)}")

    # Spectrum
    eigvals, eigvecs = np.linalg.eigh(D)
    tol = 1e-6
    spec = []
    i = 0
    while i < len(eigvals):
        j = i
        while j < len(eigvals) and abs(eigvals[j] - eigvals[i]) < tol:
            j += 1
        spec.append((eigvals[i], j - i, eigvecs[:, i:j]))
        i = j

    print("\n    Spectrum (eigenvalues & multiplicities):")
    for val, mult, _ in spec:
        print(f"        λ = {val:+.8f}   mult = {mult}")

    # Exact values: D² has eigenvalues 8 (mult 64) and 32 (mult 32)
    d2_eig = np.linalg.eigvalsh(D @ D)
    print("\n    D² eigenvalues:")
    for val in [8.0, 32.0]:
        mult = int(np.sum(np.abs(d2_eig - val) < tol))
        print(f"        λ² = {val:.0f}   mult = {mult}")
    print("    => Exact Dirac eigenvalues: ±2√2 (mult 32) and ±4√2 (mult 16)")

    # --- Section 4: Triality ------------------------------------------------
    sigma = build_triality_operator(roots, gammas)
    print("\n[4] TRIALITY OPERATOR σ")
    print(f"    σ³ = I           : {np.allclose(sigma @ sigma @ sigma, np.eye(96))}")
    print(f"    [σ, D] = 0       : {np.allclose(sigma @ D, D @ sigma)}")

    omega = np.exp(2j * np.pi / 3)
    all_orbits_ok = True
    print("\n    Decomposition of D-eigenspaces under σ:")
    for val, mult, space in spec:
        sigma_space = space.conj().T @ sigma @ space
        w = np.linalg.eigvals(sigma_space)
        phases = np.angle(w) % (2 * np.pi)
        k = np.rint(phases / (2 * np.pi / 3)) % 3
        c1 = int(np.sum(k == 0))
        cw = int(np.sum(k == 1))
        cw2 = int(np.sum(k == 2))
        ok = (mult % 3 == 0) and (c1 == mult // 3) and (cw == mult // 3) and (cw2 == mult // 3)
        status = "PASS" if ok else "FAIL"
        print(f"        λ={val:+.4f} dim={mult:2d}  1:{c1} ω:{cw} ω²:{cw2}  {status}")
        if not ok:
            all_orbits_ok = False
    print(f"\n    All eigenspaces are pure size-3 orbits : {all_orbits_ok}")

    # --- Section 5: KO-dimension signs --------------------------------------
    Cmat = build_real_structure()
    M = np.kron(np.eye(24), Cmat)
    G5 = gammas[0] @ gammas[1] @ gammas[2] @ gammas[3]
    Gamma = np.kron(np.eye(24), G5)

    # Use a random vector to test anti-linear relations
    v = np.random.randn(96) + 1j * np.random.randn(96)
    Jv = M @ np.conj(v)
    J2v = M @ np.conj(Jv)

    j2_is_minus = np.allclose(J2v, -v)
    j2_is_plus = np.allclose(J2v, v)
    j2_sign = -1 if j2_is_minus else (+1 if j2_is_plus else None)

    DJv = D @ Jv
    JDv = M @ np.conj(D @ v)
    jd_comm = np.allclose(DJv, JDv)
    jd_anticomm = np.allclose(DJv, -JDv)
    eps_prime = +1 if jd_comm else (-1 if jd_anticomm else None)

    GJv = Gamma @ Jv
    JGv = M @ np.conj(Gamma @ v)
    jg_comm = np.allclose(GJv, JGv)
    jg_anticomm = np.allclose(GJv, -JGv)
    eps_double_prime = +1 if jg_comm else (-1 if jg_anticomm else None)

    print("\n[5] KO-DIMENSION SIGNS")
    print(f"    J²  = {j2_sign}  (expected ±1)")
    print(f"    JD = DJ  ? {jd_comm}")
    print(f"    JD = –DJ ? {jd_anticomm}")
    print(f"    ε'  = {eps_prime}")
    print(f"    JΓ = ΓJ  ? {jg_comm}")
    print(f"    JΓ = –ΓJ ? {jg_anticomm}")
    print(f"    ε'' = {eps_double_prime}")

    ko_table = {
        (+1, +1, +1): 0,
        (+1, -1, -1): 1,
        (-1, -1, +1): 2,
        (-1, +1, -1): 3,
        (-1, -1, -1): 4,
        (-1, +1, +1): 5,
        (+1, +1, -1): 6,
        (+1, -1, +1): 7,
    }
    ko_dim = ko_table.get((j2_sign, eps_prime, eps_double_prime), "unknown")
    print(f"\n    KO-dimension  = {ko_dim}  (mod 8)")
    sm_like = (ko_dim == 6)
    print(f"    SM-like (KO-dim 6) ? {sm_like}")

    # --- Final summary ------------------------------------------------------
    print("\n" + "=" * 70)
    print("   SUMMARY")
    print("=" * 70)
    print(f"   • D4 roots            : 24 vectors, all ⟨α,α⟩ = 2  ✓")
    print(f"   • 2T order            : 24 elements, all |q| = 1    ✓")
    print(f"   • 24-cell degree      : 8 nearest neighbours        ✓")
    print(f"   • D spectrum          : ±2√2 (mult 32), ±4√2 (mult 16)")
    print(f"   • Vector-like ?       : Yes (symmetric ±λ)")
    print(f"   • Triality orbits     : {all_orbits_ok} (eigenspace dims 16,32 not divisible by 3)")
    print(f"   • KO-dimension signs  : (J²,ε',ε'') = ({j2_sign},{eps_prime},{eps_double_prime})")
    print(f"   • KO-dimension        : {ko_dim} mod 8  (SM requires 6)")
    print(f"   • Verdict             : D₄ does NOT produce 3 generations automatically.")
    print("=" * 70)


if __name__ == "__main__":
    main()
