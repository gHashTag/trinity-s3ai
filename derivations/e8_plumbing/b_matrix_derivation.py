#!/usr/bin/env python3
"""
Wave 16.2 — B-matrix Derivation for E8 Plumbing / 600-Cell Boundary

MATHEMATICAL CONTENT:
  1. Build E8 Cartan matrix (8×8, negative-definite)
  2. Build 600-cell vertices (120 unit quaternions in R^4)
  3. Build 600-cell adjacency (120×120, 12-regular)
  4. Construct heuristic B matrix (8×120) coupling interior nodes to boundary
  5. Assemble full 512×512 discrete Dirac operator D_P
  6. Verify Hermiticity
  7. Compute low-lying eigenvalues
  8. Compute boundary η from C block

HONEST DISCLAIMER:
  The exact form of B is NOT derived from first principles. We construct a
  geometrically motivated HEURISTIC using 16-cell frame vectors. Each interior
  node couples to the 30 boundary vertices of an icosidodecahedral equatorial
  slice. See section "B-matrix heuristic" in the output and results JSON
  for full assumptions.

REFERENCES:
  - Conway & Smith, "On Quaternions and Octonions" (2003)
  - Explicit_plumbing_research.md (Wave 15.6)
  - build_e6_e7_dp.py (Wave 12.5) for D_P block conventions
"""

import numpy as np
from scipy import linalg
import json
import os
from itertools import combinations, permutations, product

phi = (1.0 + np.sqrt(5.0)) / 2.0

# =============================================================================
# 1. E8 Cartan matrix (negative-definite plumbing convention)
# =============================================================================
def cartan_E8():
    """
    Cartan matrix of E8 in the negative-definite plumbing convention.
    Diagonal = -2, off-diagonal = +1 for Dynkin diagram edges.
    """
    P = np.diag([-2.0] * 8)
    # Dynkin diagram edges (matrix indices):
    # 0—1—2—3—4—5—6  (main chain, mapping Bourbaki α1-α3-α4-α5-α6-α7-α8)
    #     |
    #     7            (short branch, mapping Bourbaki α2 attached to α5=index3)
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (2, 7)]
    for i, j in edges:
        P[i, j] = P[j, i] = 1.0
    return P


# =============================================================================
# 2. 600-cell vertices
# =============================================================================
def _sign_of_perm(p):
    """Parity of a permutation (+1 for even, -1 for odd)."""
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                inv += 1
    return 1 if inv % 2 == 0 else -1


def build_600cell():
    """
    Build the 120 vertices of the 600-cell as unit vectors in R^4.

    Group 1: 8 vertices   — permutations of (±1, 0, 0, 0)
    Group 2: 16 vertices  — (±1/2, ±1/2, ±1/2, ±1/2)
    Group 3: 96 vertices  — even permutations of (±φ/2, ±1/2, ±1/(2φ), 0)
    """
    verts = []

    # Group 1: permutations of (±1, 0, 0, 0)
    for i in range(4):
        for s in [1, -1]:
            v = [0.0, 0.0, 0.0, 0.0]
            v[i] = float(s)
            verts.append(v)

    # Group 2: (±1/2, ±1/2, ±1/2, ±1/2)
    for signs in product([-1, 1], repeat=4):
        verts.append([float(s) * 0.5 for s in signs])

    # Group 3: even permutations of (±φ/2, ±1/2, ±1/(2φ), 0)
    # Precompute the 12 even permutations of 4 elements
    even_perms_4 = [perm for perm in permutations(range(4))
                    if _sign_of_perm(perm) == 1]

    for signs in product([-1, 1], repeat=3):
        base = [signs[0] * phi / 2.0,
                signs[1] * 0.5,
                signs[2] * 1.0 / (2.0 * phi),
                0.0]
        for perm in even_perms_4:
            v = [base[perm[i]] for i in range(4)]
            verts.append(v)

    verts = np.array(verts, dtype=float)

    # Deduplicate (the construction is exact, but we keep this for safety)
    seen = set()
    verts_unique = []
    for v in verts:
        key = tuple(np.round(v, 10))
        if key not in seen:
            seen.add(key)
            verts_unique.append(v)

    verts = np.array(verts_unique, dtype=float)
    return verts


# =============================================================================
# 3. 600-cell adjacency
# =============================================================================
def build_600cell_adjacency(verts):
    """
    Build adjacency matrix of the 600-cell graph.

    Two vertices are adjacent iff their Euclidean inner product equals φ/2,
    which for unit-norm vertices is the cosine of the edge angle.
    """
    n = len(verts)
    A = np.zeros((n, n), dtype=float)
    target = phi / 2.0
    tol = 1e-6
    for i in range(n):
        for j in range(i + 1, n):
            ip = np.dot(verts[i], verts[j])
            if abs(ip - target) < tol:
                A[i, j] = A[j, i] = 1.0
    return A


# =============================================================================
# 4. Heuristic B matrix
# =============================================================================
def build_B_matrix(verts, coupling=1.0):
    """
    Construct the heuristic coupling matrix B (N_int × N_bnd).

    FRAME VECTORS:
      We use the 8 vertices of the 16-cell, a regular sub-polytope of the
      600-cell:
        f_0 = (+1, 0, 0, 0)   f_4 = (-1, 0, 0, 0)
        f_1 = (0, +1, 0, 0)   f_5 = (0, -1, 0, 0)
        f_2 = (0, 0, +1, 0)   f_6 = (0, 0, -1, 0)
        f_3 = (0, 0, 0, +1)   f_7 = (0, 0, 0, -1)

    EQUATORIAL SLICES:
      For each frame f_i, the 30 boundary vertices with <f_i, v> = 0 form an
      icosidodecahedron (the equatorial slice of the 600-cell orthogonal to
      the coordinate axis).  These are selected by taking the 30 vertices with
      smallest absolute inner product.

    COUPLING:
      B[i, j] = coupling * sign(f_i)  for j in the equator of f_i
      B[i, j] = 0                      otherwise
      where sign(f_i) = ±1 is the nonzero coordinate of the frame.
      Antipodal pairs (e.g. f_0 and f_4) share the same 30-vertex equator
      but receive opposite signs.

    DOCUMENTED ASSUMPTIONS:
      1. The 16-cell vertices provide natural "frame directions" for the 8
         interior plumbing nodes.  No theorem guarantees this identification.
      2. Constant coupling on the equator is a discretization artifact; a
         continuous model would use a derivative (normal derivative) across
         the equator.
      3. Opposite signs for antipodal frames are chosen to reduce exact
         degeneracy in D_P; this is a model assumption, not a theorem.
      4. The number 30 (= vertices of an icosidodecahedron) matches the
         Coxeter number h(E8) = h(H4) = 30, which is geometrically suggestive
         but not a rigorous derivation of the coupling pattern.
    """
    N_bnd = len(verts)
    N_int = 8
    B = np.zeros((N_int, N_bnd), dtype=float)

    frames = np.array([
        [ 1,  0,  0,  0],
        [ 0,  1,  0,  0],
        [ 0,  0,  1,  0],
        [ 0,  0,  0,  1],
        [-1,  0,  0,  0],
        [ 0, -1,  0,  0],
        [ 0,  0, -1,  0],
        [ 0,  0,  0, -1],
    ], dtype=float)

    for i in range(N_int):
        f = frames[i]
        ips = verts @ f                # inner products <f, v_j> for all j
        abs_ips = np.abs(ips)
        # Select the 30 vertices closest to the equator (smallest |ip|)
        threshold = np.sort(abs_ips)[29]   # 30th smallest (0-based index 29)
        equatorial_mask = abs_ips <= threshold + 1e-9
        # Coupling sign = sign of the single nonzero coordinate
        nonzero_idx = np.argmax(np.abs(f))
        sign = float(np.sign(f[nonzero_idx]))
        B[i, equatorial_mask] = coupling * sign

    return B, frames


# =============================================================================
# 5. Full discrete Dirac operator D_P (Hermitian, 4N × 4N)
# =============================================================================
def build_dp_operator(P, A_bnd, verts_bnd, B, mass_shift=0.0):
    """
    Build Hermitian D_P on the E8 plumbing manifold with 600-cell boundary.

    Block structure (4 spinor components × N vertices):
      D_P = [ D_00  D_01  D_02  D_03 ]
            [ D_10  D_11  D_12  D_13 ]
            [ D_20  D_21  D_22  D_23 ]
            [ D_30  D_31  D_32  D_33 ]
    where each D_ab is N×N, N = N_int + N_bnd = 128.
    """
    N_int = P.shape[0]
    N_bnd = A_bnd.shape[0]
    N = N_int + N_bnd
    P_off = P - np.diag(np.diag(P))

    # Initialise 4×4 block structure
    blocks = [[np.zeros((N, N), dtype=float) for _ in range(4)] for _ in range(4)]

    # --- Interior blocks (plumbing / Cartan matrix) ---
    for a in (0, 1):
        blocks[a][a][:N_int, :N_int] = -P
    for a in (2, 3):
        blocks[a][a][:N_int, :N_int] = P
    for (a, b) in [(0, 2), (2, 0), (1, 3), (3, 1)]:
        blocks[a][b][:N_int, :N_int] = P_off

    # --- Boundary blocks (600-cell adjacency + antisymmetric terms) ---
    A = A_bnd + mass_shift * np.eye(N_bnd)
    for a in (0, 1):
        blocks[a][a][N_int:, N_int:] = A
    for a in (2, 3):
        blocks[a][a][N_int:, N_int:] = -A
    for (a, b) in [(0, 2), (2, 0), (1, 3), (3, 1)]:
        blocks[a][b][N_int:, N_int:] = A_bnd

    # Antisymmetric directional matrices M_k[i,j] = A_bnd[i,j] * (v_i[k] - v_j[k])
    M = []
    for k in range(4):
        M_k = np.zeros((N_bnd, N_bnd), dtype=float)
        for i in range(N_bnd):
            for j in range(i + 1, N_bnd):
                if A_bnd[i, j] > 0.5:
                    val = verts_bnd[i, k] - verts_bnd[j, k]
                    M_k[i, j] = val
                    M_k[j, i] = -val
        M.append(M_k)

    # Place M_k in antisymmetric spinor positions
    blocks[0][1][N_int:, N_int:] = M[0]
    blocks[1][0][N_int:, N_int:] = -M[0]
    blocks[1][2][N_int:, N_int:] = M[1]
    blocks[2][1][N_int:, N_int:] = -M[1]
    blocks[2][3][N_int:, N_int:] = M[2]
    blocks[3][2][N_int:, N_int:] = -M[2]
    blocks[0][3][N_int:, N_int:] = M[3]
    blocks[3][0][N_int:, N_int:] = -M[3]

    # --- Coupling blocks (interior ↔ boundary) ---
    # B is N_int × N_bnd scalar coupling, placed in chirality-flipping blocks
    for (a, b) in [(0, 2), (2, 0), (1, 3), (3, 1)]:
        blocks[a][b][:N_int, N_int:] = B
        blocks[b][a][N_int:, :N_int] = B.T

    # Assemble full 512×512 matrix
    D_P = np.block(blocks)
    return D_P


# =============================================================================
# 6. Boundary block extraction and η computation
# =============================================================================
def extract_boundary_block(D_P, N_int, N_bnd):
    """
    Extract the true boundary-boundary block D_bb from D_P.

    D_P is a (4N × 4N) matrix where N = N_int + N_bnd.
    The boundary vertices occupy the LAST N_bnd positions within each
    spinor component.  They are NOT contiguous across spinor blocks.
    """
    N = N_int + N_bnd
    # Row (and col) indices of boundary vertices in each spinor block
    idx = np.concatenate([
        np.arange(a * N + N_int, a * N + N) for a in range(4)
    ])
    return D_P[np.ix_(idx, idx)]


def extract_2comp(S):
    """Extract the upper 2-component block (spin 0,1) from 4-component S."""
    N = S.shape[0] // 4
    return S[:2 * N, :2 * N]


def compute_eta(H, tol=1e-10):
    """
    Spectral asymmetry (sign-counting):
      η = n_pos − n_neg   (excluding zeros).
    """
    ev = np.linalg.eigvalsh(H)
    n_pos = int(np.sum(ev > tol))
    n_neg = int(np.sum(ev < -tol))
    n_zero = len(ev) - n_pos - n_neg
    return float(n_pos - n_neg), n_pos, n_neg, n_zero, ev


def compute_eta_zeta_softcutoff(ev, eps=0.1):
    """
    Soft-cutoff regularization:
      η_reg(ε) = Σ sign(λ) exp(−ε|λ|).
    For a finite matrix this tends to the sign-count as ε→0.
    """
    return float(np.sum(np.sign(ev) * np.exp(-eps * np.abs(ev))))


# =============================================================================
# 7. Main
# =============================================================================
def main():
    print("=" * 70)
    print("Wave 16.2: B-matrix Derivation for E8 Plumbing / 600-Cell")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # E8 Cartan matrix
    # -------------------------------------------------------------------------
    P = cartan_E8()
    print("\n[1] E8 Cartan matrix")
    print(f"    Shape: {P.shape}")
    evP = np.linalg.eigvalsh(P)
    print(f"    Eigenvalues: {np.round(evP, 4)}")
    sigma = int(np.sum(evP > 1e-10) - np.sum(evP < -1e-10))
    print(f"    σ(P) = {sigma}  (target: −8)")
    assert sigma == -8, "E8 Cartan matrix signature must be −8"

    # -------------------------------------------------------------------------
    # 600-cell vertices
    # -------------------------------------------------------------------------
    verts = build_600cell()
    print(f"\n[2] 600-cell vertices")
    print(f"    Count: {len(verts)}  (target: 120)")
    assert len(verts) == 120, "600-cell must have exactly 120 vertices"
    norms_sq = np.array([np.dot(v, v) for v in verts])
    print(f"    Norm² range: [{norms_sq.min():.10f}, {norms_sq.max():.10f}]")
    assert np.allclose(norms_sq, 1.0, atol=1e-8), "All 600-cell vertices must be unit norm"

    # -------------------------------------------------------------------------
    # 600-cell adjacency
    # -------------------------------------------------------------------------
    A = build_600cell_adjacency(verts)
    print(f"\n[3] 600-cell adjacency")
    degrees = A.sum(axis=1)
    print(f"    Degree range: [{degrees.min():.0f}, {degrees.max():.0f}]  (target: 12)")
    print(f"    Total edges: {int(A.sum() / 2)}  (target: 720)")
    assert np.allclose(degrees, 12.0, atol=1e-8), "600-cell must be 12-regular"
    assert int(A.sum() / 2) == 720, "600-cell must have exactly 720 edges"

    # -------------------------------------------------------------------------
    # Heuristic B matrix
    # -------------------------------------------------------------------------
    B, frames = build_B_matrix(verts, coupling=1.0)
    print(f"\n[4] Heuristic B matrix")
    print(f"    Shape: {B.shape}")
    nonzero_per_row = np.sum(np.abs(B) > 1e-12, axis=1)
    print(f"    Nonzeros per row: {[int(x) for x in nonzero_per_row]}")
    print(f"    Total nonzeros: {int(np.sum(nonzero_per_row))}  (target: 240 = 8×30)")
    sparsity = 1.0 - np.sum(np.abs(B) > 1e-12) / B.size
    print(f"    Sparsity: {sparsity:.4f}  ({sparsity*100:.1f}% zeros)")

    # Verify equatorial count is exactly 30 for each frame
    for i in range(8):
        assert nonzero_per_row[i] == 30, f"Frame {i} must have exactly 30 equatorial vertices"

    # -------------------------------------------------------------------------
    # Full D_P operator
    # -------------------------------------------------------------------------
    D_P = build_dp_operator(P, A, verts, B, mass_shift=0.0)
    print(f"\n[5] Full D_P operator")
    print(f"    Shape: {D_P.shape}")
    herm_err = np.max(np.abs(D_P - D_P.T.conj()))
    print(f"    |D_P − D_P†|_max = {herm_err:.2e}")
    print(f"    Hermitian: {'YES ✓' if herm_err < 1e-12 else 'NO ✗'}")
    assert herm_err < 1e-12, "D_P must be Hermitian"

    # -------------------------------------------------------------------------
    # Eigenvalues of D_P
    # -------------------------------------------------------------------------
    print(f"\n[6] Diagonalizing 512×512 D_P...")
    ev_dp = np.linalg.eigvalsh(D_P)
    print(f"    Spectrum: [{ev_dp.min():.4f}, {ev_dp.max():.4f}]")
    near_zero = np.sum(np.abs(ev_dp) < 0.1)
    print(f"    Near-zero modes (|λ| < 0.1): {near_zero}")
    print(f"    First 10 eigenvalues (sorted): {np.round(np.sort(np.abs(ev_dp))[:10], 6)}")

    # -------------------------------------------------------------------------
    # Boundary η from D_bb (2-component restriction)
    # -------------------------------------------------------------------------
    S = extract_boundary_block(D_P, 8, 120)
    eta, n_pos, n_neg, n_zero, ev_bnd = compute_eta(extract_2comp(S))
    print(f"\n[7] Boundary η (sign-counting, 2-component block)")
    print(f"    η = {eta}")
    print(f"    Target η = −2  (APS: σ/4 = −8/4 = −2)")
    print(f"    (#positive, #negative, #zero) = ({n_pos}, {n_neg}, {n_zero})")
    print(f"    Boundary eval range: [{ev_bnd.min():.4f}, {ev_bnd.max():.4f}]")

    # -------------------------------------------------------------------------
    # Zeta-regularized η estimates (soft cutoff)
    # -------------------------------------------------------------------------
    print(f"\n[8] Zeta-regularized η estimates (soft cutoff)")
    for eps in [0.2, 0.1, 0.05, 0.02, 0.01]:
        eta_reg = compute_eta_zeta_softcutoff(ev_bnd, eps=eps)
        print(f"    η_reg(ε={eps:5.2f}) = {eta_reg:8.4f}")

    # -------------------------------------------------------------------------
    # Save results
    # -------------------------------------------------------------------------
    results = {
        "wave": "16.2",
        "B_matrix": {
            "dimensions": list(B.shape),
            "sparsity": float(sparsity),
            "nonzeros_per_row": [int(x) for x in nonzero_per_row],
            "total_nonzeros": int(np.sum(nonzero_per_row)),
            "frame_vectors": frames.tolist(),
            "coupling_type": "constant_on_equator_with_alternating_signs",
            "assumptions": [
                "Frame vectors are the 8 vertices of the 16-cell (subset of 600-cell).",
                "Each interior node couples to exactly 30 boundary vertices forming an icosidodecahedral equatorial slice.",
                "Antipodal frame pairs (0,4), (1,5), (2,6), (3,7) share the same equator but receive opposite coupling signs.",
                "Constant coupling on the equator is a discretization artifact; a continuous model would use a normal derivative across the equator.",
                "The number 30 (= vertices of an icosidodecahedron) coincides with the Coxeter number h(E8)=h(H4)=30; this is suggestive but not a rigorous derivation.",
                "THIS IS A HEURISTIC. The exact B matrix has NOT been derived from first principles."
            ]
        },
        "D_P": {
            "shape": list(D_P.shape),
            "hermitian_error": float(herm_err),
            "hermitian": bool(herm_err < 1e-12),
            "spectrum_min": float(ev_dp.min()),
            "spectrum_max": float(ev_dp.max()),
            "near_zero_modes": int(near_zero)
        },
        "boundary_eta": {
            "eta_sign_count": float(eta),
            "eta_target": -2.0,
            "n_positive": int(n_pos),
            "n_negative": int(n_neg),
            "n_zero": int(n_zero),
            "boundary_eval_min": float(ev_bnd.min()),
            "boundary_eval_max": float(ev_bnd.max()),
            "eta_reg_eps_0.20": float(compute_eta_zeta_softcutoff(ev_bnd, eps=0.20)),
            "eta_reg_eps_0.10": float(compute_eta_zeta_softcutoff(ev_bnd, eps=0.10)),
            "eta_reg_eps_0.05": float(compute_eta_zeta_softcutoff(ev_bnd, eps=0.05)),
            "eta_reg_eps_0.02": float(compute_eta_zeta_softcutoff(ev_bnd, eps=0.02)),
            "eta_reg_eps_0.01": float(compute_eta_zeta_softcutoff(ev_bnd, eps=0.01)),
        },
        "verdict": {
            "B_rigorously_derived": False,
            "B_geometrically_motivated": True,
            "eta_sign_count_matches_APS": abs(eta - (-2)) < 0.5,
            "eta_sign_count": float(eta),
            "eta_target": -2.0,
            "note": (
                "Heuristic B produces an integer sign-counting eta. "
                "The continuous APS target is −2. Agreement within O(1) is expected for a finite discretization. "
                "A full derivation of B from the plumbing geometry remains an open problem."
            )
        }
    }

    out_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "b_matrix_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[9] Results saved to {out_path}")

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  B dimensions:           {B.shape}")
    print(f"  B sparsity:             {sparsity:.4f} ({sparsity*100:.1f}% zeros)")
    print(f"  D_P Hermitian error:    {herm_err:.2e}")
    print(f"  D_P spectrum:           [{ev_dp.min():.4f}, {ev_dp.max():.4f}]")
    print(f"  Boundary η (sign):      {eta}")
    print(f"  APS target η:           −2")
    print(f"  Verdict:                B is HEURISTIC (not rigorously derived)")
    print(f"  Frame vectors:          16-cell vertices")
    print(f"  Coupling:               30 equatorial vertices per interior node")
    print("=" * 70)


if __name__ == "__main__":
    main()
