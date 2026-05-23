#!/usr/bin/env python3
"""
Wave 17.1 — Full 128-Vertex E8 Plumbing Model and η Convergence Study

MATHEMATICAL CONTENT:
  1. Build E8 Cartan matrix (8×8, negative-definite)
  2. Build 600-cell vertices (120 unit quaternions in R^4)
  3. Extract nested boundary subsets: 12, 24, 48, 120 vertices
  4. Build B-matrix (interior-boundary coupling) for each resolution
  5. Assemble D_P (4N × 4N) for each resolution
  6. Diagonalize and compute η(ε) = (n_pos(>ε) − n_neg(<−ε))/2
  7. Convergence study: does η → −2 as boundary → 120?

HONEST DISCLAIMER:
  The exact form of B is NOT derived from first principles. We use the
  geometrically motivated heuristic from Wave 16.2 with adaptive equatorial
  slice size (min(30, N_bnd)).  See the research markdown for full discussion.

OUTPUTS:
  - full_e8_results.json  (spectrum stats, η values, timing)
  - eta_convergence.png   (plot of η vs boundary vertex count)
"""

import numpy as np
from scipy import linalg
import json
import os
import time
import tracemalloc
from itertools import combinations, permutations, product
import warnings

warnings.filterwarnings("ignore")

phi = (1.0 + np.sqrt(5.0)) / 2.0

# =============================================================================
# 1. E8 Cartan matrix
# =============================================================================
def cartan_E8():
    """Cartan matrix of E8 in negative-definite plumbing convention."""
    P = np.diag([-2.0] * 8)
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (2, 7)]
    for i, j in edges:
        P[i, j] = P[j, i] = 1.0
    return P


# =============================================================================
# 2. 600-cell vertices
# =============================================================================
def _sign_of_perm(p):
    """Parity of a permutation (+1 for even, −1 for odd)."""
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                inv += 1
    return 1 if inv % 2 == 0 else -1


def build_600cell():
    """
    Build the 120 vertices of the 600-cell as unit vectors in R^4.

    Returns vertices grouped as a dict for subset extraction:
      group1: 8 vertices   — permutations of (±1, 0, 0, 0)
      group2: 16 vertices  — (±1/2, ±1/2, ±1/2, ±1/2)
      group3: 96 vertices  — even permutations of (±φ/2, ±1/2, ±1/(2φ), 0)
    """
    verts_g1, verts_g2, verts_g3 = [], [], []

    # Group 1: permutations of (±1, 0, 0, 0)
    for i in range(4):
        for s in [1, -1]:
            v = [0.0, 0.0, 0.0, 0.0]
            v[i] = float(s)
            verts_g1.append(v)

    # Group 2: (±1/2, ±1/2, ±1/2, ±1/2)
    for signs in product([-1, 1], repeat=4):
        verts_g2.append([float(s) * 0.5 for s in signs])

    # Group 3: even permutations of (±φ/2, ±1/2, ±1/(2φ), 0)
    even_perms_4 = [perm for perm in permutations(range(4))
                    if _sign_of_perm(perm) == 1]
    for signs in product([-1, 1], repeat=3):
        base = [signs[0] * phi / 2.0,
                signs[1] * 0.5,
                signs[2] * 1.0 / (2.0 * phi),
                0.0]
        for perm in even_perms_4:
            v = [base[perm[i]] for i in range(4)]
            verts_g3.append(v)

    verts_g1 = np.array(verts_g1, dtype=float)
    verts_g2 = np.array(verts_g2, dtype=float)
    verts_g3 = np.array(verts_g3, dtype=float)

    # Deduplicate each group
    def dedup(V):
        seen = set()
        out = []
        for v in V:
            key = tuple(np.round(v, 10))
            if key not in seen:
                seen.add(key)
                out.append(v)
        return np.array(out, dtype=float)

    verts_g1 = dedup(verts_g1)
    verts_g2 = dedup(verts_g2)
    verts_g3 = dedup(verts_g3)

    assert len(verts_g1) == 8, f"Group 1 must have 8 vertices, got {len(verts_g1)}"
    assert len(verts_g2) == 16, f"Group 2 must have 16 vertices, got {len(verts_g2)}"
    assert len(verts_g3) == 96, f"Group 3 must have 96 vertices, got {len(verts_g3)}"

    return {"group1": verts_g1, "group2": verts_g2, "group3": verts_g3}


def get_boundary_subset(groups, N_bnd, strategy="group3_first"):
    """
    Extract a nested subset of N_bnd boundary vertices from the 600-cell groups.

    Strategies:
      "group3_first" (default):
        Group 3 is the only group with internal edges in the 600-cell graph.
        For N_bnd ≤ 96 we take the first N_bnd vertices of group 3.
        For N_bnd = 120 we take the full 600-cell (groups 1+2+3).
        This ensures every reduced model has a non-trivial boundary graph.

      "layered" (legacy):
        N_bnd ≤ 8  : group1
        N_bnd ≤ 24 : group1 + group2
        N_bnd ≤ 48 : group1 + group2 + group3
        N_bnd = 120: full
        WARNING: group1 and group2 have NO internal edges, so N_bnd ≤ 24
        yields trivial boundary graphs.
    """
    g1, g2, g3 = groups["group1"], groups["group2"], groups["group3"]

    if strategy == "group3_first":
        if N_bnd <= len(g3):
            return g3[:N_bnd]
        elif N_bnd == 120:
            return np.vstack([g1, g2, g3])
        else:
            raise ValueError(f"N_bnd={N_bnd} not supported with group3_first; use ≤96 or 120")
    elif strategy == "layered":
        if N_bnd <= len(g1):
            return g1[:N_bnd]
        elif N_bnd <= len(g1) + len(g2):
            return np.vstack([g1, g2[:N_bnd - len(g1)]])
        elif N_bnd <= len(g1) + len(g2) + len(g3):
            return np.vstack([g1, g2, g3[:N_bnd - len(g1) - len(g2)]])
        elif N_bnd == 120:
            return np.vstack([g1, g2, g3])
        else:
            raise ValueError(f"N_bnd={N_bnd} not supported; max is 120")
    else:
        raise ValueError(f"Unknown strategy: {strategy}")


# =============================================================================
# 3. Boundary adjacency (induced subgraph on subset)
# =============================================================================
def build_boundary_adjacency(verts):
    """
    Build adjacency matrix for a subset of 600-cell vertices.

    Two vertices are adjacent iff their Euclidean inner product equals φ/2
    (the edge cosine for the unit 600-cell).
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
# 4. Heuristic B matrix (adaptive equatorial slice)
# =============================================================================
def build_B_matrix(verts, coupling=1.0):
    """
    Construct heuristic coupling matrix B (N_int × N_bnd).

    FRAME VECTORS: 8 vertices of the 16-cell (subset of 600-cell).

    EQUATORIAL SLICES:
      For each frame f_i, select the n_eq vertices with smallest |<f_i, v>|.
      n_eq = min(30, N_bnd)  (adaptive: for small boundaries, use all vertices).

    COUPLING:
      B[i, j] = coupling * sign(f_i)  for j in equatorial set
      B[i, j] = 0                      otherwise
      Antipodal pairs share the same equator but receive opposite signs.
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

    n_eq = min(30, N_bnd)
    for i in range(N_int):
        f = frames[i]
        ips = verts @ f
        abs_ips = np.abs(ips)
        # Select n_eq vertices closest to the equator
        threshold = np.sort(abs_ips)[min(n_eq - 1, N_bnd - 1)]
        equatorial_mask = abs_ips <= threshold + 1e-9
        nonzero_idx = np.argmax(np.abs(f))
        sign = float(np.sign(f[nonzero_idx]))
        B[i, equatorial_mask] = coupling * sign

    return B, frames


# =============================================================================
# 5. Full discrete Dirac operator D_P
# =============================================================================
def build_dp_operator(P, A_bnd, verts_bnd, B, mass_shift=0.0):
    """
    Build Hermitian D_P on the E8 plumbing manifold.

    Block structure (4 spinor components × N vertices):
      D_P = [ D_00  D_01  D_02  D_03 ]
            [ D_10  D_11  D_12  D_13 ]
            [ D_20  D_21  D_22  D_23 ]
            [ D_30  D_31  D_32  D_33 ]
    where each D_ab is N×N, N = N_int + N_bnd.
    """
    N_int = P.shape[0]
    N_bnd = A_bnd.shape[0]
    N = N_int + N_bnd
    P_off = P - np.diag(np.diag(P))

    blocks = [[np.zeros((N, N), dtype=float) for _ in range(4)] for _ in range(4)]

    # --- Interior blocks ---
    for a in (0, 1):
        blocks[a][a][:N_int, :N_int] = -P
    for a in (2, 3):
        blocks[a][a][:N_int, :N_int] = P
    for (a, b) in [(0, 2), (2, 0), (1, 3), (3, 1)]:
        blocks[a][b][:N_int, :N_int] = P_off

    # --- Boundary blocks ---
    A = A_bnd + mass_shift * np.eye(N_bnd)
    for a in (0, 1):
        blocks[a][a][N_int:, N_int:] = A
    for a in (2, 3):
        blocks[a][a][N_int:, N_int:] = -A
    for (a, b) in [(0, 2), (2, 0), (1, 3), (3, 1)]:
        blocks[a][b][N_int:, N_int:] = A_bnd

    # Antisymmetric directional matrices M_k
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

    blocks[0][1][N_int:, N_int:] = M[0]
    blocks[1][0][N_int:, N_int:] = -M[0]
    blocks[1][2][N_int:, N_int:] = M[1]
    blocks[2][1][N_int:, N_int:] = -M[1]
    blocks[2][3][N_int:, N_int:] = M[2]
    blocks[3][2][N_int:, N_int:] = -M[2]
    blocks[0][3][N_int:, N_int:] = M[3]
    blocks[3][0][N_int:, N_int:] = -M[3]

    # --- Coupling blocks ---
    for (a, b) in [(0, 2), (2, 0), (1, 3), (3, 1)]:
        blocks[a][b][:N_int, N_int:] = B
        blocks[b][a][N_int:, :N_int] = B.T

    D_P = np.block(blocks)
    return D_P


# =============================================================================
# 6. Boundary block extraction and η computation
# =============================================================================
def extract_boundary_block(D_P, N_int, N_bnd):
    """Extract boundary-boundary block from D_P."""
    N = N_int + N_bnd
    idx = np.concatenate([
        np.arange(a * N + N_int, a * N + N) for a in range(4)
    ])
    return D_P[np.ix_(idx, idx)]


def extract_2comp(S):
    """Extract upper 2-component block from 4-component boundary operator."""
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


def compute_eta_half(H, tol=1e-10):
    """
    η with division by 2 (chiral convention):
      η_half = (n_pos − n_neg) / 2.
    """
    ev = np.linalg.eigvalsh(H)
    n_pos = int(np.sum(ev > tol))
    n_neg = int(np.sum(ev < -tol))
    n_zero = len(ev) - n_pos - n_neg
    return float(n_pos - n_neg) / 2.0, n_pos, n_neg, n_zero, ev


def compute_eta_epsilon(ev, eps=0.1):
    """
    η(ε) = (n_pos(>ε) − n_neg(<−ε)) / 2.
    """
    n_pos = int(np.sum(ev > eps))
    n_neg = int(np.sum(ev < -eps))
    return float(n_pos - n_neg) / 2.0


def compute_eta_zeta_softcutoff(ev, eps=0.1):
    """Soft-cutoff regularization: η_reg(ε) = Σ sign(λ) exp(−ε|λ|)."""
    return float(np.sum(np.sign(ev) * np.exp(-eps * np.abs(ev))))


# =============================================================================
# 7. Run single model
# =============================================================================
def run_model(N_bnd, P, groups, coupling=1.0, mass_shift=0.0, subset_strategy="group3_first"):
    """
    Build and diagonalize D_P for a given boundary size N_bnd.
    Returns a dict with all results.
    """
    N_int = 8
    print(f"\n  --- Model: N_bnd = {N_bnd}, N_total = {N_int + N_bnd} ---")

    # Memory tracking
    tracemalloc.start()
    t0 = time.perf_counter()

    # Build boundary
    verts_bnd = get_boundary_subset(groups, N_bnd, strategy=subset_strategy)
    A_bnd = build_boundary_adjacency(verts_bnd)
    degrees = A_bnd.sum(axis=1)
    print(f"    Boundary degree range: [{degrees.min():.0f}, {degrees.max():.0f}]")
    print(f"    Boundary edges: {int(A_bnd.sum() / 2)}")

    # Build B matrix
    B, frames = build_B_matrix(verts_bnd, coupling=coupling)
    nonzero_per_row = np.sum(np.abs(B) > 1e-12, axis=1)
    print(f"    B nonzeros per row: {nonzero_per_row.tolist()}")

    # Build D_P
    D_P = build_dp_operator(P, A_bnd, verts_bnd, B, mass_shift=mass_shift)
    herm_err = np.max(np.abs(D_P - D_P.T.conj()))
    print(f"    D_P shape: {D_P.shape}, Hermitian error: {herm_err:.2e}")

    # Diagonalize
    ev_dp = np.linalg.eigvalsh(D_P)
    t1 = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"    D_P spectrum: [{ev_dp.min():.4f}, {ev_dp.max():.4f}]")
    near_zero = int(np.sum(np.abs(ev_dp) < 0.1))
    print(f"    Near-zero modes (|λ|<0.1): {near_zero}")
    print(f"    Diagonalization time: {t1 - t0:.3f}s")
    print(f"    Peak RAM: {peak / (1024**2):.2f} MB")

    # Boundary η
    S = extract_boundary_block(D_P, N_int, N_bnd)
    H2 = extract_2comp(S)

    eta_int, n_pos, n_neg, n_zero, ev_bnd = compute_eta(H2)
    eta_half, _, _, _, _ = compute_eta_half(H2)

    print(f"    Boundary η (integer): {eta_int}")
    print(f"    Boundary η / 2:       {eta_half}")
    print(f"    (#pos, #neg, #zero):  ({n_pos}, {n_neg}, {n_zero})")
    print(f"    Boundary eval range:  [{ev_bnd.min():.4f}, {ev_bnd.max():.4f}]")

    # η(ε) for various cutoffs
    eta_eps = {}
    for eps in [0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005]:
        eta_eps[f"eps_{eps}"] = compute_eta_epsilon(ev_bnd, eps=eps)

    # Soft-cutoff
    eta_reg = {}
    for eps in [0.5, 0.2, 0.1, 0.05, 0.02, 0.01]:
        eta_reg[f"eps_{eps}"] = compute_eta_zeta_softcutoff(ev_bnd, eps=eps)

    return {
        "N_int": N_int,
        "N_bnd": N_bnd,
        "N_total": N_int + N_bnd,
        "D_P_shape": list(D_P.shape),
        "hermitian_error": float(herm_err),
        "hermitian": bool(herm_err < 1e-12),
        "spectrum_min": float(ev_dp.min()),
        "spectrum_max": float(ev_dp.max()),
        "near_zero_modes": near_zero,
        "diag_time_sec": float(t1 - t0),
        "peak_ram_mb": float(peak / (1024 ** 2)),
        "boundary_degrees": {
            "min": float(degrees.min()),
            "max": float(degrees.max()),
            "mean": float(degrees.mean()),
        },
        "boundary_edges": int(A_bnd.sum() / 2),
        "B_nonzeros_per_row": [int(x) for x in nonzero_per_row],
        "B_total_nonzeros": int(np.sum(nonzero_per_row)),
        "eta_integer": float(eta_int),
        "eta_half": float(eta_half),
        "eta_target_APS": -2.0,
        "n_positive": n_pos,
        "n_negative": n_neg,
        "n_zero": n_zero,
        "boundary_eval_min": float(ev_bnd.min()),
        "boundary_eval_max": float(ev_bnd.max()),
        "eta_epsilon": eta_eps,
        "eta_reg_soft": eta_reg,
    }


# =============================================================================
# 8. Main: convergence study
# =============================================================================
def main():
    print("=" * 70)
    print("Wave 17.1: Full 128-Vertex E8 Plumbing Model — η Convergence Study")
    print("=" * 70)

    # E8 Cartan
    P = cartan_E8()
    evP = np.linalg.eigvalsh(P)
    sigma = int(np.sum(evP > 1e-10) - np.sum(evP < -1e-10))
    print(f"\n[E8 Cartan matrix]")
    print(f"    Eigenvalues: {np.round(evP, 4)}")
    print(f"    σ(P) = {sigma}  (target: −8)")
    assert sigma == -8, "E8 Cartan matrix signature must be −8"

    # 600-cell vertex groups
    groups = build_600cell()
    print(f"\n[600-cell vertex groups]")
    print(f"    Group 1: {len(groups['group1'])} vertices")
    print(f"    Group 2: {len(groups['group2'])} vertices")
    print(f"    Group 3: {len(groups['group3'])} vertices")
    print(f"    Total:   {sum(len(g) for g in groups.values())} vertices")

    # Run convergence study at multiple resolutions
    # Using group3_first strategy: group 3 has 96 vertices with internal edges.
    boundary_sizes = [12, 24, 32, 48, 64, 96, 120]
    all_results = []

    print("\n" + "=" * 70)
    print("CONVERGENCE STUDY")
    print("=" * 70)

    for N_bnd in boundary_sizes:
        try:
            res = run_model(N_bnd, P, groups, coupling=1.0, mass_shift=0.0)
            all_results.append(res)
        except Exception as e:
            print(f"    ERROR at N_bnd={N_bnd}: {e}")

    # Also run with different coupling constants for the full model
    print("\n" + "=" * 70)
    print("COUPLING SENSITIVITY (full model, N_bnd=120)")
    print("=" * 70)
    coupling_study = []
    for c in [0.5, 1.0, 2.0, 5.0]:
        res = run_model(120, P, groups, coupling=c, mass_shift=0.0)
        res["coupling"] = c
        coupling_study.append(res)

    # Also run with mass shift for the full model
    print("\n" + "=" * 70)
    print("MASS-SHIFT SENSITIVITY (full model, N_bnd=120)")
    print("=" * 70)
    mass_study = []
    for m in [0.0, 0.1, 0.5, 1.0]:
        res = run_model(120, P, groups, coupling=1.0, mass_shift=m)
        res["mass_shift"] = m
        mass_study.append(res)

    # =============================================================================
    # Save JSON
    # =============================================================================
    out_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)

    output = {
        "wave": "17.1",
        "date": "2026-05-22",
        "description": "Full 128-vertex E8 plumbing model and eta convergence study",
        "E8_cartan": {
            "eigenvalues": [float(x) for x in evP],
            "sigma": sigma,
            "sigma_target": -8,
        },
        "convergence_study": all_results,
        "coupling_sensitivity": coupling_study,
        "mass_shift_sensitivity": mass_study,
    }

    out_path = os.path.join(out_dir, "full_e8_results.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n[Results saved to {out_path}]")

    # =============================================================================
    # Plot
    # =============================================================================
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # Plot 1: η_half vs N_bnd
        ax = axes[0, 0]
        Ns = [r["N_bnd"] for r in all_results]
        etas = [r["eta_half"] for r in all_results]
        ax.plot(Ns, etas, "o-", color="steelblue", linewidth=2, markersize=8)
        ax.axhline(-2.0, color="crimson", linestyle="--", linewidth=2, label="APS target η = −2")
        ax.set_xlabel("Number of boundary vertices", fontsize=11)
        ax.set_ylabel(r"$\eta = (n_+ - n_-) / 2$", fontsize=11)
        ax.set_title("η vs Boundary Resolution", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Plot 2: η_epsilon for various cutoffs (full model)
        ax = axes[0, 1]
        full_res = [r for r in all_results if r["N_bnd"] == 120][0]
        eps_vals = []
        eta_eps_vals = []
        for key, val in sorted(full_res["eta_epsilon"].items(), key=lambda x: float(x[0].split("_")[1])):
            eps_vals.append(float(key.split("_")[1]))
            eta_eps_vals.append(val)
        ax.plot(eps_vals, eta_eps_vals, "s-", color="darkgreen", linewidth=2, markersize=8)
        ax.axhline(-2.0, color="crimson", linestyle="--", linewidth=2, label="APS target η = −2")
        ax.set_xlabel(r"Cutoff $\varepsilon$", fontsize=11)
        ax.set_ylabel(r"$\eta(\varepsilon)$", fontsize=11)
        ax.set_title(r"Cutoff Dependence of $\eta$ (Full Model, $N_{bnd}=120$)", fontsize=12)
        ax.set_xscale("log")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Plot 3: soft-cutoff η_reg vs epsilon
        ax = axes[1, 0]
        reg_vals = []
        for key, val in sorted(full_res["eta_reg_soft"].items(), key=lambda x: float(x[0].split("_")[1])):
            reg_vals.append(val)
        ax.plot(eps_vals[:len(reg_vals)], reg_vals, "^-", color="purple", linewidth=2, markersize=8)
        ax.axhline(-2.0, color="crimson", linestyle="--", linewidth=2, label="APS target η = −2")
        ax.set_xlabel(r"Regularization $\varepsilon$", fontsize=11)
        ax.set_ylabel(r"$\eta_{\mathrm{reg}}(\varepsilon)$", fontsize=11)
        ax.set_title(r"Soft-Cutoff $\eta_{\mathrm{reg}}$ (Full Model)", fontsize=12)
        ax.set_xscale("log")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Plot 4: spectrum histogram (full model)
        ax = axes[1, 1]
        full_res = [r for r in all_results if r["N_bnd"] == 120][0]
        # We didn't save the full spectrum in JSON to save space, but we can recompute or skip.
        # Instead, show coupling sensitivity bar chart.
        couplings = [c["coupling"] for c in coupling_study]
        eta_couplings = [c["eta_half"] for c in coupling_study]
        ax.bar([str(c) for c in couplings], eta_couplings, color="coral", edgecolor="black")
        ax.axhline(-2.0, color="crimson", linestyle="--", linewidth=2, label="APS target η = −2")
        ax.set_xlabel("Coupling constant", fontsize=11)
        ax.set_ylabel(r"$\eta$", fontsize=11)
        ax.set_title(r"$\eta$ vs Coupling Constant (Full Model)", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        plot_path = os.path.join(out_dir, "eta_convergence.png")
        plt.savefig(plot_path, dpi=150)
        print(f"[Plot saved to {plot_path}]")
    except ImportError:
        print("[matplotlib not available; skipping plot]")

    # =============================================================================
    # Text summary
    # =============================================================================
    print("\n" + "=" * 70)
    print("SUMMARY TABLE")
    print("=" * 70)
    print(f"{'N_bnd':>6} {'N_total':>8} {'D_P dim':>10} {'η_int':>8} {'η/2':>8} {'target':>8} {'time(s)':>10} {'RAM(MB)':>10}")
    print("-" * 70)
    for r in all_results:
        print(f"{r['N_bnd']:>6} {r['N_total']:>8} {r['D_P_shape'][0]:>10} "
              f"{r['eta_integer']:>8.1f} {r['eta_half']:>8.2f} {-2.0:>8.1f} "
              f"{r['diag_time_sec']:>10.3f} {r['peak_ram_mb']:>10.2f}")
    print("-" * 70)

    print("\n" + "=" * 70)
    print("CONVERGENCE VERDICT")
    print("=" * 70)
    full_eta = [r["eta_half"] for r in all_results if r["N_bnd"] == 120]
    if full_eta:
        print(f"  Full model (120 boundary vertices): η = {full_eta[0]:.2f}")
        print(f"  APS target:                         η = −2.00")
        print(f"  Discrepancy:                        |η − η_APS| = {abs(full_eta[0] - (-2)):.2f}")
        if abs(full_eta[0] - (-2)) < 1.0:
            print("  → η is within O(1) of the APS target. Convergence plausible.")
        else:
            print("  → η is NOT close to the APS target. Convergence FAILED.")
            print("    Possible reasons:")
            print("    1. The B-matrix heuristic does not capture the correct plumbing topology.")
            print("    2. Sign-counting on a finite graph cannot reproduce a fractional η.")
            print("    3. The M_k antisymmetric terms are too small relative to adjacency eigenvalues.")
            print("    4. A mass shift or coupling rescaling might be needed (phenomenological).")
    print("=" * 70)


if __name__ == "__main__":
    main()
