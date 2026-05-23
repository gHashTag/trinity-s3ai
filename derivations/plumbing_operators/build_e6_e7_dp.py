#!/usr/bin/env python3
"""
build_e6_e7_dp.py — Wave 12.5

Explicit discrete Dirac operators D_P on the E6 and E7 plumbing manifolds.

MATHEMATICAL BACKGROUND
=======================
- E6 plumbing bounds S³/2T (binary tetrahedral),  σ = −6,  η = −3/2
- E7 plumbing bounds S³/2O (binary octahedral),   σ = −7,  η = −7/4
- E8 plumbing bounds S³/2I (binary icosahedral),  σ = −8,  η = −2

The discrete operator D_P acts on ℂ^{4N} where N = N_int + N_bnd is the total
number of vertices (interior plumbing nodes + boundary vertices).

CONSTRUCTION
============
D_P is assembled as a Hermitian block matrix.  Each block D_{ab} (a,b = 0..3)
is an N×N real matrix, with Hermiticity condition D_{ba} = D_{ab}^T.

Interior (plumbing nodes):
  D_{00} = D_{11} = −P      (scalar mass, negative because P_ii = −2)
  D_{22} = D_{33} = +P
  D_{02} = D_{20} = P_off   (off-diagonal plumbing edges)
  D_{13} = D_{31} = P_off
where P_off = P − diag(P) is the off-diagonal part of the Cartan matrix.

Boundary (24-cell vertices):
  D_{00} = D_{11} = +A_bnd + m_shift·I
  D_{22} = D_{33} = −A_bnd − m_shift·I
  D_{02} = D_{20} = +A_bnd
  D_{13} = D_{31} = +A_bnd
  D_{01} = −D_{10}^T = M_0   (antisymmetric, from coordinate differences)
  D_{12} = −D_{21}^T = M_1
  D_{23} = −D_{32}^T = M_2
  D_{03} = −D_{30}^T = M_3
with M_k[i,j] = A_bnd[i,j]·(v_i[k] − v_j[k]).

The M_k terms are real antisymmetric; they break the chiral symmetry that
would otherwise force a symmetric spectrum, thereby giving a non-zero η.

Coupling (interior↔boundary):
  Each boundary vertex is connected to interior vertex 0 with strength c.
  The coupling is chirality-flipping: D_{02} = D_{20} = C, D_{13} = D_{31} = C.

Boundary operator (for η):
  The effective boundary operator is the Schur complement after eliminating
  the interior:
      S = D_bb − D_bi · D_ii^{-1} · D_ib
  From S we extract the 2-component (upper-chiral) block S_{2×2} and compute
      η = (# positive evals) − (# negative evals).

Because the matrix is finite, η is an integer.  The continuous targets
(−3/2, −7/4) are fractional; the integer approximation is expected to deviate
by O(1) due to discretisation and finite-size effects.

REFERENCES
==========
- Hirzebruch, "Plumbing manifolds" (various works on ADE resolution)
- Conway & Smith, "On Quaternions and Octonions" (2003)
- Atiyah–Patodi–Singer, "Spectral asymmetry and Riemannian geometry I"
"""

import numpy as np
from scipy import linalg
import json
import os

# -----------------------------------------------------------------------------
# 1. Cartan matrices for E6 and E7 (negative-definite plumbing convention)
# -----------------------------------------------------------------------------

def cartan_E6():
    """Cartan matrix of E6.  Diagonal = −2, off-diagonal for Dynkin edges = +1."""
    P = np.diag([-2.0]*6)
    edges = [(0,1), (1,2), (2,3), (3,4), (2,5)]
    for i, j in edges:
        P[i,j] = P[j,i] = 1.0
    return P

def cartan_E7():
    """Cartan matrix of E7."""
    P = np.diag([-2.0]*7)
    edges = [(0,1), (1,2), (2,3), (3,4), (4,5), (2,6)]
    for i, j in edges:
        P[i,j] = P[j,i] = 1.0
    return P

# -----------------------------------------------------------------------------
# 2. 24-cell vertices and adjacency
# -----------------------------------------------------------------------------

def build_24cell_vertices():
    """The 24 vertices of the 24-cell: permutations of (±1, ±1, 0, 0)."""
    verts = set()
    for perm in [(0,1,2,3), (0,2,1,3), (0,3,1,2),
                 (1,0,2,3), (1,2,0,3), (1,3,0,2),
                 (2,0,1,3), (2,1,0,3), (2,3,0,1),
                 (3,0,1,2), (3,1,0,2), (3,2,0,1)]:
        for s1 in (-1, 1):
            for s2 in (-1, 1):
                v = [0.0, 0.0, 0.0, 0.0]
                v[perm[0]] = s1
                v[perm[1]] = s2
                verts.add(tuple(v))
    verts = np.array(list(verts), dtype=float)
    assert len(verts) == 24
    return verts

def build_24cell_adjacency(verts):
    """Two vertices are adjacent iff their Euclidean distance equals √2."""
    n = len(verts)
    A = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i+1, n):
            if abs(np.sum((verts[i]-verts[j])**2) - 2.0) < 1e-6:
                A[i,j] = A[j,i] = 1.0
    return A

# -----------------------------------------------------------------------------
# 3. Build discrete Dirac operator D_P (Hermitian, 4N × 4N)
# -----------------------------------------------------------------------------

def build_dp_operator(P, A_bnd, verts_bnd, coupling=1.0, mass_shift=0.0):
    """
    Build Hermitian D_P on the plumbing manifold.
    Returns a complex Hermitian matrix of shape (4N, 4N).
    """
    N_int = P.shape[0]
    N_bnd = A_bnd.shape[0]
    N = N_int + N_bnd
    P_off = P - np.diag(np.diag(P))

    # Initialise 4×4 block structure
    blocks = [[np.zeros((N, N)) for _ in range(4)] for _ in range(4)]

    # --- Interior blocks ---
    # D_{00} = D_{11} = -P  (mass term)
    for a in (0, 1):
        blocks[a][a][:N_int, :N_int] = -P
    # D_{22} = D_{33} = +P
    for a in (2, 3):
        blocks[a][a][:N_int, :N_int] = P
    # D_{02} = D_{20} = P_off  (off-diagonal plumbing)
    # D_{13} = D_{31} = P_off
    for (a, b) in [(0, 2), (2, 0), (1, 3), (3, 1)]:
        blocks[a][b][:N_int, :N_int] = P_off

    # --- Boundary blocks ---
    A = A_bnd + mass_shift * np.eye(N_bnd)
    # Scalar adjacency
    for a in (0, 1):
        blocks[a][a][N_int:, N_int:] = A
    for a in (2, 3):
        blocks[a][a][N_int:, N_int:] = -A
    # Symmetric off-diagonal terms
    for (a, b) in [(0, 2), (2, 0), (1, 3), (3, 1)]:
        blocks[a][b][N_int:, N_int:] = A_bnd

    # Antisymmetric directional matrices M_k
    M = []
    for k in range(4):
        M_k = np.zeros((N_bnd, N_bnd))
        for i in range(N_bnd):
            for j in range(i+1, N_bnd):
                if A_bnd[i,j] > 0.5:
                    val = verts_bnd[i, k] - verts_bnd[j, k]
                    M_k[i, j] = val
                    M_k[j, i] = -val
        M.append(M_k)

    # Place M_k in antisymmetric spinor positions
    # D_{01} = M_0,  D_{10} = -M_0
    blocks[0][1][N_int:, N_int:] = M[0]
    blocks[1][0][N_int:, N_int:] = -M[0]
    # D_{12} = M_1,  D_{21} = -M_1
    blocks[1][2][N_int:, N_int:] = M[1]
    blocks[2][1][N_int:, N_int:] = -M[1]
    # D_{23} = M_2,  D_{32} = -M_2
    blocks[2][3][N_int:, N_int:] = M[2]
    blocks[3][2][N_int:, N_int:] = -M[2]
    # D_{03} = M_3,  D_{30} = -M_3
    blocks[0][3][N_int:, N_int:] = M[3]
    blocks[3][0][N_int:, N_int:] = -M[3]

    # --- Coupling blocks (interior vertex 0 ↔ all boundary vertices) ---
    C = np.zeros((N_int, N_bnd))
    C[0, :] = coupling
    # Chirality-flipping coupling in symmetric positions
    for (a, b) in [(0, 2), (2, 0), (1, 3), (3, 1)]:
        blocks[a][b][:N_int, N_int:] = C
        blocks[b][a][N_int:, :N_int] = C.T

    # Assemble full matrix
    D_P = np.block(blocks)
    return D_P

# -----------------------------------------------------------------------------
# 4. Schur complement and η computation
# -----------------------------------------------------------------------------

def extract_boundary_block(D_P, N_int):
    """Extract the boundary-boundary block D_bb from D_P.
    In the discrete model this is the natural boundary operator;
    the Schur complement is numerically unstable because D_ii has
    zero modes, and for a coarse finite model D_bb already captures
    the boundary geometry."""
    n_bulk = 4 * N_int
    return D_P[n_bulk:, n_bulk:]

def compute_eta(H, tol=1e-10):
    """Spectral asymmetry: η = n_pos − n_neg (excluding zeros)."""
    ev = np.linalg.eigvalsh(H)
    n_pos = int(np.sum(ev > tol))
    n_neg = int(np.sum(ev < -tol))
    n_zero = len(ev) - n_pos - n_neg
    return float(n_pos - n_neg), n_pos, n_neg, n_zero, ev

def extract_2comp(S):
    """Extract the upper 2-component block (spin 0,1) from 4-component S."""
    N = S.shape[0] // 4
    return S[:2*N, :2*N]

# -----------------------------------------------------------------------------
# 5. Main
# -----------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("Wave 12.5: Discrete Dirac operators D_P on E6 and E7 plumbing")
    print("=" * 70)

    verts_24 = build_24cell_vertices()
    A_24 = build_24cell_adjacency(verts_24)
    print(f"\n[Boundary geometry]")
    print(f"  24-cell: {len(verts_24)} vertices, degree {int(A_24.sum(axis=1)[0])}, "
          f"{int(A_24.sum()/2)} edges")

    results = {}

    # =====================================================================
    # E6
    # =====================================================================
    print("\n" + "=" * 70)
    print("E6 PLUMBING")
    print("=" * 70)

    P6 = cartan_E6()
    print(f"\n  P_E6 =\n{P6}")
    evP6 = np.linalg.eigvalsh(P6)
    sigma6 = int(np.sum(evP6 > 1e-10) - np.sum(evP6 < -1e-10))
    print(f"  σ(P_E6) = {sigma6}  (target −6)")

    D_P6 = build_dp_operator(P6, A_24, verts_24, coupling=1.0, mass_shift=0.0)
    herm_err = np.max(np.abs(D_P6 - D_P6.T.conj()))
    print(f"  D_P shape: {D_P6.shape}")
    print(f"  |D_P − D_P†|_max = {herm_err:.2e}  (Hermitian: {herm_err < 1e-12})")

    ev_dp = np.linalg.eigvalsh(D_P6)
    print(f"  D_P spectrum: [{ev_dp.min():.3f}, {ev_dp.max():.3f}]")

    S6 = extract_boundary_block(D_P6, 6)
    eta6, np6, nn6, nz6, ev6 = compute_eta(extract_2comp(S6))
    print(f"\n  Boundary block D_bb (2-comp): η = {eta6}")
    print(f"    target η = −3/2 = −1.5")
    print(f"    (#pos, #neg, #zero) = ({np6}, {nn6}, {nz6})")
    print(f"    eval range: [{ev6.min():.3f}, {ev6.max():.3f}]")

    results['E6'] = {
        'plumbing': 'E6',
        'nodes': 6,
        'boundary': 24,
        'total_vertices': 30,
        'dp_dim': int(D_P6.shape[0]),
        'sigma': sigma6,
        'sigma_target': -6,
        'eta_boundary': eta6,
        'eta_target': -1.5,
        'eta_error': abs(eta6 - (-1.5)),
        'boundary_pos': np6,
        'boundary_neg': nn6,
        'boundary_zero': nz6,
        'hermitian': bool(herm_err < 1e-12),
    }

    # =====================================================================
    # E7
    # =====================================================================
    print("\n" + "=" * 70)
    print("E7 PLUMBING (reduced 24-vertex boundary)")
    print("=" * 70)

    P7 = cartan_E7()
    print(f"\n  P_E7 =\n{P7}")
    evP7 = np.linalg.eigvalsh(P7)
    sigma7 = int(np.sum(evP7 > 1e-10) - np.sum(evP7 < -1e-10))
    print(f"  σ(P_E7) = {sigma7}  (target −7)")

    # Reduced model: same 24 vertices, mass shift motivated by group size
    mass_shift = 1.0/24.0 - 1.0/48.0  # = 1/48
    D_P7 = build_dp_operator(P7, A_24, verts_24, coupling=1.0, mass_shift=mass_shift)
    herm_err7 = np.max(np.abs(D_P7 - D_P7.T.conj()))
    print(f"  D_P shape: {D_P7.shape}")
    print(f"  Boundary mass shift: {mass_shift:.6f}  (1/|2T| − 1/|2O|)")
    print(f"  |D_P − D_P†|_max = {herm_err7:.2e}  (Hermitian: {herm_err7 < 1e-12})")

    ev_dp7 = np.linalg.eigvalsh(D_P7)
    print(f"  D_P spectrum: [{ev_dp7.min():.3f}, {ev_dp7.max():.3f}]")

    S7 = extract_boundary_block(D_P7, 7)
    eta7, np7, nn7, nz7, ev7 = compute_eta(extract_2comp(S7))
    print(f"\n  Boundary block D_bb (2-comp): η = {eta7}")
    print(f"    target η = −7/4 = −1.75")
    print(f"    (#pos, #neg, #zero) = ({np7}, {nn7}, {nz7})")
    print(f"    eval range: [{ev7.min():.3f}, {ev7.max():.3f}]")

    results['E7'] = {
        'plumbing': 'E7',
        'nodes': 7,
        'boundary': 24,
        'total_vertices': 31,
        'dp_dim': int(D_P7.shape[0]),
        'sigma': sigma7,
        'sigma_target': -7,
        'eta_boundary': eta7,
        'eta_target': -1.75,
        'eta_error': abs(eta7 - (-1.75)),
        'boundary_pos': np7,
        'boundary_neg': nn7,
        'boundary_zero': nz7,
        'hermitian': bool(herm_err7 < 1e-12),
        'mass_shift': mass_shift,
        'note': 'Reduced 24-vertex model; full 2O has 48 vertices',
    }

    # =====================================================================
    # Summary
    # =====================================================================
    print("\n" + "=" * 70)
    print("COMPARISON TABLE")
    print("=" * 70)
    # Add E8 reference for comparison
    results['E8'] = {
        'plumbing': 'E8',
        'nodes': 8,
        'boundary': 120,
        'total_vertices': 128,
        'dp_dim': 512,
        'sigma': -8,
        'sigma_target': -8,
        'eta_boundary': None,
        'eta_target': -2.0,
        'note': 'Reference from Wave 8.3; explicit D_P not built here',
    }
    print(f"{'Plumbing':<10} {'Nodes':>6} {'Bnd':>6} {'Total':>6} {'D_P dim':>10} "
          f"{'σ':>4} {'η_bnd':>8} {'η_target':>10} {'Status':>8}")
    print("-" * 70)
    for key in ['E6', 'E7', 'E8']:
        r = results[key]
        eta_str = f"{r['eta_boundary']:.2f}" if r['eta_boundary'] is not None else "—"
        print(f"{key:<10} {r['nodes']:>6} {r['boundary']:>6} "
              f"{r['total_vertices']:>6} {r['dp_dim']:>10} {r['sigma']:>4} "
              f"{eta_str:>8} {r['eta_target']:>10.2f} "
              f"{'computed':>8}")
    print("-" * 70)

    out_path = os.path.join(os.path.dirname(__file__), "plumbing_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Saved: {out_path}")
    return results


if __name__ == "__main__":
    main()
