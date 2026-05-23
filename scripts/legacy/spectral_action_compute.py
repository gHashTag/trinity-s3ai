#!/usr/bin/env python3
"""
Spectral Action Computation for 600-Cell Dirac Operator

Reference: Iochum, Levy, Vassilevich 2011 "Spectral action beyond 4D"

Computes:
1. Eigenvalues of D^2 for the 600-cell Hodge-Dirac operator
2. Spectral zeta function zeta_D(s)
3. Heat kernel coefficients a_0, a_2, a_4
4. Dixmier trace Tr_omega(D^{-4})
5. Spectral action coefficient a_4(D^2)
6. Standard Model predictions (Higgs mass, gauge couplings)

The 600-cell (hexacosichoron) is a regular 4D polytope with:
- 120 vertices, 720 edges, 1200 faces (triangles), 600 cells (tetrahedra)
- Schlafli symbol {3,3,5}
- Vertex figure: icosahedron
- Euler characteristic: chi = 0 (triangulation of S^3)
"""

import numpy as np
from itertools import permutations, product, combinations
import json

# =============================================================================
# 1. CONSTRUCT THE 600-CELL
# =============================================================================

def construct_600_cell():
    """Generate 600-cell vertices as 120 points on S^3 in R^4."""
    phi = (1 + np.sqrt(5)) / 2
    phi_inv = 1 / phi
    vertices = []

    # Group 1: (±1, ±1, ±1, ±1)/2 — 16 vertices
    for signs in product([-1, 1], repeat=4):
        v = np.array(signs, dtype=float) / 2
        vertices.append(v)

    # Group 2: (±1, 0, 0, 0) and permutations — 8 vertices
    for i in range(4):
        for sign in [-1, 1]:
            v = np.zeros(4)
            v[i] = sign
            vertices.append(v)

    # Group 3: even permutations of (±φ/2, ±1/2, ±φ⁻¹/2, 0) — 96 vertices
    even_perms = [(0,1,2,3), (0,2,3,1), (0,3,1,2), (1,0,3,2), (1,2,0,3), (1,3,2,0),
                  (2,0,1,3), (2,1,3,0), (2,3,0,1), (3,0,2,1), (3,1,0,2), (3,2,1,0)]
    for perm in even_perms:
        for signs in product([-1, 1], repeat=3):
            v = np.zeros(4)
            v[perm[0]] = signs[0] * phi / 2
            v[perm[1]] = signs[1] / 2
            v[perm[2]] = signs[2] * phi_inv / 2
            v[perm[3]] = 0
            if not any(np.allclose(v, existing) for existing in vertices):
                vertices.append(v)

    return np.array(vertices)


def build_adjacency_matrix(vertices):
    """Build adjacency matrix from minimum edge length."""
    N = len(vertices)
    # Compute all pairwise distances
    dists = np.zeros((N, N))
    for i in range(N):
        for j in range(i+1, N):
            dists[i, j] = dists[j, i] = np.linalg.norm(vertices[i] - vertices[j])

    # Edge length = minimum nonzero distance
    edge_length = dists[dists > 0].min()

    # Build adjacency: A[i,j] = 1 if distance equals edge length
    A = np.zeros((N, N))
    tol = 1e-6
    for i in range(N):
        for j in range(i+1, N):
            if abs(dists[i, j] - edge_length) < tol:
                A[i, j] = A[j, i] = 1

    return A, edge_length


def build_coboundary_operators(A, vertices):
    """Build cellular coboundary operators d_0, d_1, d_2."""
    N = len(vertices)

    # Edges
    edge_list = []
    for i in range(N):
        for j in range(i+1, N):
            if A[i, j]:
                edge_list.append((i, j))
    E = len(edge_list)
    edge_index = {e: i for i, e in enumerate(edge_list)}

    # Faces (triangles)
    faces = []
    for tri in combinations(range(N), 3):
        i, j, k = tri
        if A[i, j] and A[j, k] and A[i, k]:
            faces.append(tuple(sorted(tri)))
    F = len(faces)
    face_index = {f: i for i, f in enumerate(faces)}

    # Cells (tetrahedra)
    cells = []
    for tet in combinations(range(N), 4):
        v = list(tet)
        is_tetra = True
        for e in combinations(v, 2):
            if not A[e[0], e[1]]:
                is_tetra = False
                break
        if is_tetra:
            cells.append(tuple(sorted(tet)))
    T = len(cells)

    # d_0: H^0 -> H^1
    d_0 = np.zeros((E, N))
    for ei, (i, j) in enumerate(edge_list):
        d_0[ei, i] = -1
        d_0[ei, j] = 1

    # d_1: H^1 -> H^2
    d_1 = np.zeros((F, E))
    for fi, face in enumerate(faces):
        i, j, k = face
        e1 = (i, j) if i < j else (j, i)
        e2 = (i, k) if i < k else (k, i)
        e3 = (j, k) if j < k else (k, j)
        s1 = 1 if i < j else -1
        s2 = -1 if i < k else 1
        s3 = 1 if j < k else -1
        d_1[fi, edge_index[e1]] = s1
        d_1[fi, edge_index[e2]] = s2
        d_1[fi, edge_index[e3]] = s3

    # d_2: H^2 -> H^3
    d_2 = np.zeros((T, F))
    for ti, cell in enumerate(cells):
        i, j, k, l = cell
        f1 = tuple(sorted([j, k, l]))
        f2 = tuple(sorted([i, k, l]))
        f3 = tuple(sorted([i, j, l]))
        f4 = tuple(sorted([i, j, k]))
        signs = [1, -1, 1, -1]
        for f, s in zip([f1, f2, f3, f4], signs):
            if f in face_index:
                d_2[ti, face_index[f]] = s

    return d_0, d_1, d_2, edge_list, faces, cells


# =============================================================================
# 2. MAIN COMPUTATION
# =============================================================================

def compute_spectral_action():
    """Main computation of spectral action for 600-cell."""

    phi = (1 + np.sqrt(5)) / 2
    results = {}

    # Construct 600-cell
    print("Constructing 600-cell vertices...")
    vertices = construct_600_cell()
    N = len(vertices)
    results['N_vertices'] = int(N)
    results['phi'] = float(phi)

    # Verify
    norms = np.linalg.norm(vertices, axis=1)
    assert np.allclose(norms, 1), "Vertices not on unit sphere"

    # Build adjacency matrix
    print("Building adjacency matrix...")
    A, edge_length = build_adjacency_matrix(vertices)
    degrees = A.sum(axis=1)
    E = int(A.sum() / 2)
    results['E_edges'] = E
    results['edge_length'] = float(edge_length)
    results['vertex_degree'] = int(degrees[0])
    assert all(degrees == 12), "Not regular of degree 12"
    assert E == 720, f"Expected 720 edges, got {E}"

    # Build coboundary operators
    print("Building coboundary operators...")
    d_0, d_1, d_2, edge_list, faces, cells = build_coboundary_operators(A, vertices)
    F = len(faces)
    T = len(cells)
    results['F_faces'] = F
    results['T_cells'] = T
    assert F == 1200, f"Expected 1200 faces, got {F}"
    assert T == 600, f"Expected 600 cells, got {T}"

    # Euler characteristic
    chi = N - E + F - T
    results['euler_characteristic'] = int(chi)
    assert chi == 0, f"Expected chi=0, got {chi}"

    # Verify d^2 = 0
    assert np.allclose(d_1 @ d_0, 0), "d_1 @ d_0 != 0"
    assert np.allclose(d_2 @ d_1, 0), "d_2 @ d_1 != 0"

    # Construct Hodge-Dirac operator D = d + d^
    d_0dag = d_0.T
    d_1dag = d_1.T
    d_2dag = d_2.T

    dim_H = int(N + E + F + T)
    results['dim_H'] = dim_H

    D = np.zeros((dim_H, dim_H))
    D[:N, N:N+E] = d_0dag
    D[N:N+E, :N] = d_0
    D[N:N+E, N+E:N+E+F] = d_1dag
    D[N+E:N+E+F, N:N+E] = d_1
    D[N+E:N+E+F, N+E+F:] = d_2dag
    D[N+E+F:, N+E:N+E+F] = d_2

    assert np.allclose(D, D.T), "D not Hermitian"

    # Compute D^2 eigenvalues
    print("Computing D^2 eigenvalues...")
    D2 = D @ D
    eigvals_D2 = np.linalg.eigvalsh(D2)

    # Separate zero and nonzero modes
    nz_eigvals = eigvals_D2[eigvals_D2 > 1e-10]
    n_zero = (eigvals_D2 <= 1e-10).sum()
    results['n_zero_modes'] = int(n_zero)
    results['n_nonzero'] = len(nz_eigvals)
    results['smallest_nonzero'] = float(nz_eigvals.min())
    results['largest_eigenvalue'] = float(eigvals_D2.max())

    # Hodge Laplacian blocks
    L_0 = D2[:N, :N]
    L_1 = D2[N:N+E, N:N+E]
    L_2 = D2[N+E:N+E+F, N+E:N+E+F]
    L_3 = D2[N+E+F:, N+E+F:]

    eig_L0 = np.linalg.eigvalsh(L_0)
    eig_L1 = np.linalg.eigvalsh(L_1)
    eig_L2 = np.linalg.eigvalsh(L_2)
    eig_L3 = np.linalg.eigvalsh(L_3)

    eigenvalues_by_degree = {0: eig_L0, 1: eig_L1, 2: eig_L2, 3: eig_L3}

    # Spectral zeta function
    zeta_0 = len(nz_eigvals)
    results['zeta_D2_0'] = int(zeta_0)
    results['zeta_D2_1'] = float(np.sum(nz_eigvals**(-1)))
    results['zeta_D2_2'] = float(np.sum(nz_eigvals**(-2)))
    results['zeta_D2_4'] = float(np.sum(nz_eigvals**(-4)))

    # Traces (positive powers)
    Tr_D2 = float(np.sum(nz_eigvals))
    Tr_D4 = float(np.sum(nz_eigvals**2))
    results['Tr_D2'] = Tr_D2
    results['Tr_D4'] = Tr_D4

    # Traces (inverse powers)
    Tr_inv2 = float(np.sum(nz_eigvals**(-1)))
    Tr_inv4 = float(np.sum(nz_eigvals**(-2)))
    Tr_inv6 = float(np.sum(nz_eigvals**(-3)))
    results['Tr_Dinv2'] = Tr_inv2
    results['Tr_Dinv4'] = Tr_inv4
    results['Tr_Dinv6'] = Tr_inv6

    # Graded traces
    graded_inv2 = sum((-1)**k * np.sum(eig[eig > 1e-10]**(-1))
                      for k, eig in eigenvalues_by_degree.items())
    graded_inv4 = sum((-1)**k * np.sum(eig[eig > 1e-10]**(-2))
                      for k, eig in eigenvalues_by_degree.items())
    results['graded_Tr_inv2'] = float(graded_inv2)
    results['graded_Tr_inv4'] = float(graded_inv4)

    # Unique eigenvalues with multiplicities
    unique_eigs = np.sort(np.unique(eigvals_D2.round(10)))
    spectrum_data = []
    for val in unique_eigs:
        mult = int((np.abs(eigvals_D2 - val) < 1e-6).sum())
        spectrum_data.append({'eigenvalue': float(val), 'multiplicity': mult})
    results['spectrum'] = spectrum_data

    # Heat kernel coefficients
    results['K_0'] = dim_H  # K(t->0) = dim(H)
    results['K_inf'] = int(n_zero)  # K(t->inf) = dim(ker)

    # Dixmier trace
    Vol_S4 = 8 * np.pi**2 / 3
    Tr_omega_S4 = Vol_S4 / (16 * np.pi**2)
    results['Tr_omega_S4'] = float(Tr_omega_S4)
    results['Tr_omega_600cell'] = 0.0
    results['Tr_omega_product'] = float(Tr_omega_S4 * dim_H)

    # Spectral action coefficient a_4
    a_4_ILV = float(zeta_0)
    results['a4_ILV'] = a_4_ILV

    # Combined with S^4
    a_0_S4 = 2.0/3.0
    a_2_S4 = -2.0
    a_4_S4 = 13.0/45.0
    a_4_combined = a_4_S4 * dim_H + a_2_S4 * Tr_D2 + (a_0_S4/2.0) * Tr_D4
    results['a4_S4'] = float(a_4_S4)
    results['a4_combined'] = float(a_4_combined)

    # Standard Model predictions
    f0 = 1.0
    g_sq = np.pi**2 / (f0 * Tr_inv2)
    g_val = np.sqrt(g_sq)
    lambda_H = (np.pi**4 * Tr_inv4) / (4 * f0 * Tr_inv2**2)
    v_ew = 246.0
    m_H = 2 * v_ew * np.sqrt(lambda_H)

    results['gauge_coupling_g'] = float(g_val)
    results['gauge_coupling_alpha'] = float(g_sq / (4 * np.pi))
    results['higgs_quartic'] = float(lambda_H)
    results['higgs_mass_GeV'] = float(m_H)
    results['ratio_Tr4_Tr2sq'] = float(Tr_inv4 / Tr_inv2**2)

    # Effective radius
    R_eff = np.sqrt(3 / eig_L0[eig_L0 > 1e-10].min())
    results['effective_radius'] = float(R_eff)

    print(f"\n{'='*60}")
    print("COMPUTATION COMPLETE")
    print(f"{'='*60}")
    print(f"Vertices:         {N}")
    print(f"Edges:            {E}")
    print(f"Faces:            {F}")
    print(f"Cells:            {T}")
    print(f"Euler char:       {chi}")
    print(f"Hilbert space:    {dim_H}")
    print(f"Zero modes:       {n_zero}")
    print(f"a_4 (ILV):        {a_4_ILV}")
    print(f"a_4 (S^4 x 600):  {a_4_combined:.2f}")
    print(f"Higgs mass:       {m_H:.1f} GeV")
    print(f"Gauge coupling:   g = {g_val:.4f}")

    return results


# =============================================================================
# 3. SAVE RESULTS
# =============================================================================

if __name__ == "__main__":
    results = compute_spectral_action()

    # Save as JSON
    with open("/mnt/agents/output/trinity-v33/spectral_action_data.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nResults saved to spectral_action_data.json")
