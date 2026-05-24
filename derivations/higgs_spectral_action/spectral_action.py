#!/usr/bin/env python3
"""
Wave 11.5 — Spectral Action on the 600-Cell Discrete Dirac Operator
====================================================================
Attempt to derive the Higgs mass structurally from the
Chamseddine–Connes spectral action on D_F^{600}, WITHOUT using
the σ-field (Wave 5.3 proved σ cannot arise from H4).

This script:
1. Builds the 120 H4 roots (project convention, circumradius = 2).
2. Constructs the 600-cell adjacency graph (12-regular, 720 edges).
3. Builds the 480×480 discrete Dirac operator D = Σ_{edges} γ·ê.
4. Diagonalizes D numerically (scipy.linalg.eigh).
5. Computes heat-kernel traces and extracts Seeley–DeWitt-like
   coefficients a_0, a_2, a_4.
6. Applies the standard Connes–Marcolli Higgs-mass formula.
7. Compares to PDG 125.10 GeV and renders a verdict.

Physical parameters
-------------------
- Cutoff scale Λ  ~ 10^16 GeV  (GUT scale, reported for context)
- VEV v           = 246 GeV
- PDG m_H         = 125.10 ± 0.14 GeV
- Golden ratio φ  = (1+√5)/2

NCG Higgs mass (tree level, no σ)
----------------------------------
  λ_Higgs = 1/φ⁴        (from geometric a_4)
  m_H     = √(2λ) · v   ≈ 132.9 GeV

Trinity claim (with empirical tuning)
--------------------------------------
  m_H = 4 φ³ e² ≈ 125.20 GeV  (0.02σ fit to PDG)

Conventions
-----------
The heat-kernel expansion for a 4-D operator is
    Tr(e^{-t D²}) ~ (a_0 + t a_2 + t² a_4) / (16 π²)
For the discrete 480-dim operator a_0 = 480.
The theoretical a_4 from proofs/trinity/SpectralAction600Cell.v is
    a_4 = (5 + 6φ)/(16φ) ≈ 0.5681356
"""

import json
import os
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

# ---------------------------------------------------------------------------
# 1.  Constants & Gamma matrices
# ---------------------------------------------------------------------------
PHI = (1.0 + np.sqrt(5.0)) / 2.0          # φ  ≈ 1.6180339887
PHI_INV = PHI - 1.0                       # 1/φ = φ−1 ≈ 0.6180339887

# PDG values
M_H_PDG = 125.10                          # GeV
M_H_PDG_ERR = 0.14                        # GeV
VEV = 246.0                               # GeV

# 4×4 Euclidean gamma matrices — realisation of Cl(4,0)
#   γ¹ = σ_x ⊗ I₂ ,  γ² = σ_y ⊗ I₂ ,  γ³ = σ_z ⊗ σ_x ,  γ⁴ = σ_z ⊗ σ_y
# They are Hermitian and satisfy {γ^a, γ^b} = 2 δ^{ab}.
I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)

GAMMA = [
    np.kron(SX, I2),
    np.kron(SY, I2),
    np.kron(SZ, SX),
    np.kron(SZ, SY),
]

# Verify Clifford algebra
for a in range(4):
    for b in range(4):
        anticomm = GAMMA[a] @ GAMMA[b] + GAMMA[b] @ GAMMA[a]
        expected = (2.0 * np.eye(4) if a == b else np.zeros((4, 4), dtype=complex))
        if not np.allclose(anticomm, expected):
            raise RuntimeError(f"Clifford algebra violation: {{{a},{b}}} != 2δ")

# Chirality matrix γ⁵ = γ¹γ²γ³γ⁴  (anticommutes with every γ^μ)
GAMMA5 = GAMMA[0] @ GAMMA[1] @ GAMMA[2] @ GAMMA[3]


# ---------------------------------------------------------------------------
# 2.  H4 root system (matches proofs/trinity/SpectralAction600Cell.v
#     and trinity_rust/src/h4.rs)
# ---------------------------------------------------------------------------
def build_h4_roots() -> np.ndarray:
    """
    Return the 120 H4 roots as 4-vectors of norm 2.

    Types
    -----
    1. (±2, 0, 0, 0) and permutations                → 8 roots
    2. (±1, ±1, ±1, ±1)                              → 16 roots
    3. Even permutations of (±φ, ±1, ±1/φ, 0)        → 96 roots
    """
    roots = []

    # Type 1
    for i in range(4):
        for s in (+2.0, -2.0):
            v = np.zeros(4)
            v[i] = s
            roots.append(v)

    # Type 2
    for s1 in (+1.0, -1.0):
        for s2 in (+1.0, -1.0):
            for s3 in (+1.0, -1.0):
                for s4 in (+1.0, -1.0):
                    roots.append(np.array([s1, s2, s3, s4]))

    # Type 3 — even permutations (the 12 even elements of S₄)
    even_perms = [
        [0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0],
        [2, 0, 1, 3], [1, 2, 0, 3], [3, 0, 2, 1], [1, 3, 2, 0],
        [2, 1, 3, 0], [3, 1, 0, 2], [0, 3, 1, 2], [0, 2, 3, 1],
    ]
    base_vals = [PHI, 1.0, PHI_INV, 0.0]

    for s_phi in (+1.0, -1.0):
        for s1 in (+1.0, -1.0):
            for s_inv in (+1.0, -1.0):
                base = [s_phi * base_vals[0],
                        s1 * base_vals[1],
                        s_inv * base_vals[2],
                        base_vals[3]]
                for perm in even_perms:
                    v = np.array([base[perm[0]], base[perm[1]],
                                  base[perm[2]], base[perm[3]]])
                    roots.append(v)

    roots_arr = np.array(roots, dtype=float)
    assert roots_arr.shape == (120, 4), f"Expected (120,4), got {roots_arr.shape}"

    # Uniqueness check
    for i in range(120):
        for j in range(i + 1, 120):
            if np.linalg.norm(roots_arr[i] - roots_arr[j]) < 1e-9:
                raise RuntimeError(f"Duplicate H4 roots: {i} and {j}")

    # Norm check (all should be exactly 2 for this convention)
    norms = np.linalg.norm(roots_arr, axis=1)
    if not np.allclose(norms, 2.0):
        raise RuntimeError(f"H4 root norms not all 2: min={norms.min()}, max={norms.max()}")

    return roots_arr


# ---------------------------------------------------------------------------
# 3.  600-cell adjacency (minimal-distance graph on H4 roots)
# ---------------------------------------------------------------------------
def build_adjacency(roots: np.ndarray, tol: float = 1e-6) -> np.ndarray:
    """
    Return the 120×120 adjacency matrix of the 600-cell skeleton.
    Two vertices are adjacent when their Euclidean distance equals the
    edge length of the 600-cell (2/φ for circumradius 2).
    """
    n = roots.shape[0]
    dists = np.zeros((n, n), dtype=float)
    for i in range(n):
        diff = roots - roots[i]          # (n,4)
        dists[i] = np.linalg.norm(diff, axis=1)

    # Minimal non-zero distance = edge length
    nonzero = dists[dists > tol]
    edge_len = float(np.min(nonzero))
    expected_edge = 2.0 / PHI
    if abs(edge_len - expected_edge) > 1e-3:
        raise RuntimeError(
            f"Edge length mismatch: found {edge_len}, expected {expected_edge}"
        )

    A = (np.abs(dists - edge_len) < tol).astype(float)
    np.fill_diagonal(A, 0.0)

    degrees = A.sum(axis=1)
    if not np.allclose(degrees, 12.0):
        raise RuntimeError(
            f"600-cell not 12-regular: unique degrees = {np.unique(degrees)}"
        )

    n_edges = int(A.sum() / 2)
    if n_edges != 720:
        raise RuntimeError(f"Expected 720 edges, got {n_edges}")

    return A


# ---------------------------------------------------------------------------
# 4.  Discrete Dirac operator  (480 × 480)
# ---------------------------------------------------------------------------
def build_dirac_operator(roots: np.ndarray, A: np.ndarray) -> np.ndarray:
    """
    Construct D = Σ_{i~j} γ·ê_{ij}  as a 480×480 Hermitian matrix.

    For each undirected edge (i,j) with i<j:
        ê = (v_j − v_i) / |v_j − v_i|
        block_{ij} = Σ_{μ=1}^{4} ê_μ γ^μ   (4×4)
    The matrix is Hermitian because each γ^μ is Hermitian and the
    (j,i) block receives the same 4×4 matrix.
    """
    n = roots.shape[0]          # 120
    N = 4 * n                   # 480
    D = np.zeros((N, N), dtype=complex)

    edge_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] > 0.5:
                e_vec = roots[j] - roots[i]
                e_len = np.linalg.norm(e_vec)
                e_hat = e_vec / e_len

                # γ·ê  (4×4 Hermitian, squares to I)
                gamma_e = sum(e_hat[mu] * GAMMA[mu] for mu in range(4))

                D[4 * i:4 * i + 4, 4 * j:4 * j + 4] = gamma_e
                D[4 * j:4 * j + 4, 4 * i:4 * i + 4] = gamma_e
                edge_count += 1

    assert edge_count == 720, f"Expected 720 edges, inserted {edge_count}"
    return D


# ---------------------------------------------------------------------------
# 5.  Spectral analysis
# ---------------------------------------------------------------------------
def analyze_spectrum(D: np.ndarray):
    """Diagonalize D, verify chiral symmetry, return sorted real eigenvalues."""
    if not np.allclose(D, D.conj().T):
        raise RuntimeError("D is not Hermitian")

    # Verify anticommutation with γ⁵ = I_{120} ⊗ γ⁵_{4×4}
    gamma5_full = np.kron(np.eye(120), GAMMA5)
    anticomm = D @ gamma5_full + gamma5_full @ D
    chiral_ok = np.allclose(anticomm, 0)
    if not chiral_ok:
        max_violation = np.max(np.abs(anticomm))
        print(f"WARNING: chiral-symmetry max violation = {max_violation:.2e}")

    print("Diagonalizing 480×480 Dirac operator …")
    eigvals = eigh(D, eigvals_only=True)
    eigvals = np.sort(eigvals)

    n_zero = np.sum(np.abs(eigvals) < 1e-8)
    n_pos = np.sum(eigvals > 1e-8)
    n_neg = np.sum(eigvals < -1e-8)

    print(f"  Zero modes        : {n_zero}")
    print(f"  Positive eigenvals: {n_pos}")
    print(f"  Negative eigenvals: {n_neg}")
    print(f"  Eigenvalue range  : [{eigvals[0]:.6f}, {eigvals[-1]:.6f}]")

    # Verify ± pairing
    pos = eigvals[eigvals > 1e-8]
    neg = eigvals[eigvals < -1e-8]
    if len(pos) != len(neg):
        raise RuntimeError("Chiral eigenvalue pairing broken")
    if len(pos) > 0 and not np.allclose(pos, -neg[::-1], atol=1e-6):
        raise RuntimeError("Eigenvalue mirror symmetry broken")

    return eigvals, chiral_ok


# ---------------------------------------------------------------------------
# 6.  Heat-kernel & spectral-action coefficients
# ---------------------------------------------------------------------------
def heat_kernel_traces(eigvals: np.ndarray, t_values: np.ndarray) -> np.ndarray:
    """Compute  Tr(exp(−t D²))  for each t."""
    sq = eigvals ** 2
    return np.array([np.sum(np.exp(-t * sq)) for t in t_values])


def extract_coefficients_fits(eigvals: np.ndarray):
    """
    Extract Seeley–DeWitt-like coefficients from the discrete spectrum.

    For a 4-D operator the continuous expansion is
        Tr(e^{-t D²}) = (a_0 + a_2 t + a_4 t² + …) / (16 π²)

    Because our D is a finite matrix, the expansion is only a
    short-t Taylor series:
        Tr(e^{-t D²}) = N − t Σ λ² + t² Σ λ⁴/2 − …
    We fit in an intermediate window where the t² term dominates over
    higher powers but the series has not yet saturated to N.
    """
    N = len(eigvals)          # 480
    lam2 = eigvals ** 2
    lam4 = lam2 ** 2
    sum_lam2 = float(np.sum(lam2))
    sum_lam4 = float(np.sum(lam4))

    # Exact Taylor coefficients of the discrete heat kernel
    #   K(t) = Σ e^{-t λ²} = N − t·S₂ + t²·S₄/2 − t³·S₆/6 + …
    c0 = float(N)
    c1 = -sum_lam2
    c2 = sum_lam4 / 2.0

    # Convert to the "standard" convention where K(t) = (a_0 + a_2 t + a_4 t²)/(16π²)
    # Hence a_k = 16π² · c_k
    fac = 16.0 * np.pi ** 2
    a0_fit = fac * c0
    a2_fit = fac * c1
    a4_fit = fac * c2

    # Also do a direct numerical fit in a window 1e-4 < t < 5e-3
    t_window = np.logspace(-4, np.log10(5e-3), 30)
    K = heat_kernel_traces(eigvals, t_window)
    # Fit  K(t) = A + B t + C t²
    X = np.vstack([np.ones_like(t_window), t_window, t_window ** 2]).T
    A_mat, B_mat, C_mat = np.linalg.lstsq(X, K, rcond=None)[0]
    a0_num = fac * A_mat
    a2_num = fac * B_mat
    a4_num = fac * C_mat

    return {
        "a0_taylor": a0_fit,
        "a2_taylor": a2_fit,
        "a4_taylor": a4_fit,
        "a0_numerical": a0_num,
        "a2_numerical": a2_num,
        "a4_numerical": a4_num,
        "sum_lambda2": sum_lam2,
        "sum_lambda4": sum_lam4,
    }


# ---------------------------------------------------------------------------
# 7.  Spectral action  S(Λ) = Tr(f(D/Λ))
# ---------------------------------------------------------------------------
def spectral_action(eigvals: np.ndarray, Lambda: float,
                    cutoff: str = "gaussian") -> float:
    """
    Compute Tr(f(D/Λ)) with a smooth cutoff.

    cutoff = "gaussian"   →  f(x) = exp(−x²)
    cutoff = "exp"        →  f(x) = exp(−|x|)
    """
    if cutoff == "gaussian":
        return float(np.sum(np.exp(-(eigvals / Lambda) ** 2)))
    elif cutoff == "exp":
        return float(np.sum(np.exp(-np.abs(eigvals / Lambda))))
    else:
        raise ValueError(f"Unknown cutoff: {cutoff}")


def spectral_action_expansion(a0: float, a2: float, a4: float,
                               Lambda: float,
                               f0: float = 1.0, f2: float = 1.0, f4: float = 1.0) -> tuple:
    """
    The standard asymptotic expansion (Connes–Chamseddine 1996):
        S_Λ[D] ≈ f_4 Λ⁴ a_0 + f_2 Λ² a_2 + f_0 a_4
    Returns (term4, term2, term0, total).
    """
    term4 = f4 * Lambda ** 4 * a0
    term2 = f2 * Lambda ** 2 * a2
    term0 = f0 * a4
    return term4, term2, term0, term4 + term2 + term0


# ---------------------------------------------------------------------------
# 8.  Higgs mass from NCG formulas
# ---------------------------------------------------------------------------
def higgs_mass_prediction():
    """
    Standard tree-level NCG prediction (no σ-field).

    From the spectral action on A = C ⊕ H ⊕ M₃(C):
        g_unified² = 4/φ⁴
        λ_Higgs    = g_unified² / 4 = 1/φ⁴
        m_H        = √(2λ) · v
    """
    g_unified_sq = 4.0 / PHI ** 4
    lambda_higgs = 1.0 / PHI ** 4
    m_higgs = np.sqrt(2.0 * lambda_higgs) * VEV
    return {
        "g_unified_sq": float(g_unified_sq),
        "lambda_higgs": float(lambda_higgs),
        "m_higgs_GeV": float(m_higgs),
    }


def trinity_empirical_prediction():
    """The project's retrospective fit formula (requires σ-field)."""
    m_higgs = 4.0 * PHI ** 3 * np.e ** 2
    return float(m_higgs)


# ---------------------------------------------------------------------------
# 9.  Main driver
# ---------------------------------------------------------------------------
def main():
    out_dir = Path("/Users/playra/trinity-s3ai/derivations/higgs_spectral_action")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Wave 11.5 — Spectral Action on 600-Cell Dirac Operator")
    print("Structural Higgs-mass derivation WITHOUT σ-field")
    print("=" * 70)

    # --- Geometry ----------------------------------------------------------
    print("\n[1] Building H4 root system (120 vertices, circumradius = 2) …")
    roots = build_h4_roots()
    print(f"    OK: {roots.shape[0]} vertices, norm = {np.linalg.norm(roots[0]):.1f}")

    print("\n[2] Building 600-cell adjacency (edge length = 2/φ) …")
    A = build_adjacency(roots)
    print(f"    OK: 12-regular, 720 edges")

    # --- Dirac operator ----------------------------------------------------
    print("\n[3] Building 480×480 discrete Dirac operator …")
    D = build_dirac_operator(roots, A)
    print(f"    Matrix shape: {D.shape}")
    print(f"    Hermitian     : {np.allclose(D, D.conj().T)}")

    # --- Spectrum ----------------------------------------------------------
    print("\n[4] Computing spectrum …")
    eigvals, chiral_ok = analyze_spectrum(D)
    np.save(out_dir / "eigenvalues.npy", eigvals)

    # Save spectrum summary
    spectrum_summary = {
        "n_total": int(len(eigvals)),
        "n_zero": int(np.sum(np.abs(eigvals) < 1e-8)),
        "n_positive": int(np.sum(eigvals > 1e-8)),
        "min_positive": float(eigvals[eigvals > 1e-8].min()) if np.any(eigvals > 1e-8) else None,
        "max_abs": float(np.max(np.abs(eigvals))),
        "mean_abs": float(np.mean(np.abs(eigvals))),
        "median_abs": float(np.median(np.abs(eigvals))),
    }

    # --- Heat kernel -------------------------------------------------------
    print("\n[5] Heat-kernel analysis …")
    coeffs = extract_coefficients_fits(eigvals)
    a4_theory = (5.0 + 6.0 * PHI) / (16.0 * PHI)

    print(f"    a_0 (Taylor)    = {coeffs['a0_taylor']:.6f}")
    print(f"    a_0 (numerical) = {coeffs['a0_numerical']:.6f}")
    print(f"    a_2 (Taylor)    = {coeffs['a2_taylor']:.6f}")
    print(f"    a_4 (Taylor)    = {coeffs['a4_taylor']:.6f}")
    print(f"    a_4 (numerical) = {coeffs['a4_numerical']:.6f}")
    print(f"    a_4 (theory)    = {a4_theory:.10f}")

    # Note: the Taylor a_4 is huge because it counts λ⁴ for a discrete matrix.
    # The "theoretical" a_4 from the Coq proof assumes a continuous 4-D
    # manifold and is orders of magnitude smaller.  We report both honestly.

    # --- Spectral action at GUT scale --------------------------------------
    print("\n[6] Spectral action at Λ = 10¹⁶ GeV …")
    Lambda_GeV = 1e16
    # Rescale eigenvalues to physical units.  The dimensionless spectrum has
    # typical magnitude ~3.5.  We set the physical scale so that the
    # largest |λ| corresponds to Λ_GUT.
    scale_factor = Lambda_GeV / np.max(np.abs(eigvals))
    eigvals_physical = eigvals * scale_factor

    S_gauss = spectral_action(eigvals_physical, Lambda_GeV, cutoff="gaussian")
    S_exp = spectral_action(eigvals_physical, Lambda_GeV, cutoff="exp")
    print(f"    S_gaussian(Λ) = {S_gauss:.6e}")
    print(f"    S_exp(Λ)      = {S_exp:.6e}")

    # --- Higgs mass predictions --------------------------------------------
    print("\n[7] Higgs mass predictions …")
    pred = higgs_mass_prediction()
    m_h_nocorr = pred["m_higgs_GeV"]
    m_h_trinity = trinity_empirical_prediction()

    diff_nocorr = abs(m_h_nocorr - M_H_PDG)
    sigma_nocorr = diff_nocorr / M_H_PDG_ERR

    diff_trinity = abs(m_h_trinity - M_H_PDG)
    sigma_trinity = diff_trinity / M_H_PDG_ERR

    print(f"    λ_Higgs (geometric) = {pred['lambda_higgs']:.10f}")
    print(f"    g_unified²          = {pred['g_unified_sq']:.10f}")
    print(f"    m_H (no σ, tree)    = {m_h_nocorr:.4f} GeV")
    print(f"    m_H (Trinity fit)   = {m_h_trinity:.4f} GeV")
    print(f"    PDG m_H             = {M_H_PDG:.2f} ± {M_H_PDG_ERR:.2f} GeV")
    print(f"    Δ(no σ)             = {diff_nocorr:.4f} GeV  ({sigma_nocorr:.1f}σ)")
    print(f"    Δ(Trinity)          = {diff_trinity:.4f} GeV  ({sigma_trinity:.2f}σ)")

    # --- Best-fit Λ (honest check: does tuning Λ save the prediction?) -----
    print("\n[8] Checking Λ-dependence (honest control) …")
    # In pure geometric NCG, m_H at tree level does NOT depend on Λ.
    # The coupling λ is fixed by the algebra/geometry, not by the cutoff.
    # We demonstrate this explicitly.
    lambdas_test = np.logspace(15, 17, 5)
    print("    Λ [GeV]        |  m_H predicted [GeV]")
    print("    ---------------|----------------------")
    for Lam in lambdas_test:
        # Tree-level formula has no Λ dependence
        print(f"    {Lam:.3e}    |  {m_h_nocorr:.4f}   (constant)")
    print("    → Tree-level m_H is Λ-independent.  Tuning Λ cannot fix the discrepancy.")

    # --- Verdict -----------------------------------------------------------
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    if sigma_nocorr < 2.0:
        verdict = (
            "POSITIVE: The 600-cell spectral action without σ-field "
            "reproduces the observed Higgs mass within 2σ."
        )
    elif sigma_nocorr < 5.0:
        verdict = (
            "MARGINAL: The prediction is off by a few σ; "
            "higher-order or RG effects might bridge the gap, "
            "but no structural mechanism is identified."
        )
    else:
        verdict = (
            "NEGATIVE: The 600-cell spectral action WITHOUT σ-field "
            "fails to predict the correct Higgs mass. "
            f"The structural prediction m_H = {m_h_nocorr:.2f} GeV "
            f"deviates by {sigma_nocorr:.1f}σ from PDG. "
            "The σ-field correction (Connes–Marcolli) is unavailable in H4 "
            "per Wave 5.3.  This is another boundary result for the pure geometric programme."
        )

    print(verdict)
    print("=" * 70)

    # --- Save all results --------------------------------------------------
    results = {
        "spectrum_summary": spectrum_summary,
        "heat_kernel": coeffs,
        "a4_theory": float(a4_theory),
        "spectral_action_GUT": {
            "Lambda_GeV": Lambda_GeV,
            "S_gaussian": float(S_gauss),
            "S_exp": float(S_exp),
        },
        "higgs_prediction": {
            "g_unified_sq": pred["g_unified_sq"],
            "lambda_higgs": pred["lambda_higgs"],
            "m_higgs_no_sigma_GeV": m_h_nocorr,
            "m_higgs_trinity_GeV": m_h_trinity,
            "m_higgs_pdg_GeV": M_H_PDG,
            "m_higgs_pdg_err_GeV": M_H_PDG_ERR,
            "diff_no_sigma_GeV": diff_nocorr,
            "sigma_no_sigma": sigma_nocorr,
            "diff_trinity_GeV": diff_trinity,
            "sigma_trinity": sigma_trinity,
        },
        "verdict": verdict,
        "chiral_symmetry_ok": chiral_ok,
    }

    with open(out_dir / "spectral_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to:\n  {out_dir / 'spectral_results.json'}\n  {out_dir / 'eigenvalues.npy'}")
    return results


if __name__ == "__main__":
    main()
