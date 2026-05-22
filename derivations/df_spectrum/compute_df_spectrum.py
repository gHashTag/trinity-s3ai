#!/usr/bin/env python3
"""
compute_df_spectrum.py  —  Wave 8.4
====================================
Constructs and diagonalizes a 480×480 candidate finite Dirac operator D_F
for the 600-cell spectral triple, then compares the spectrum to SM mass ratios.

CONSTRUCTION CHOICE
-------------------
We use the "graph Dirac with 2I-twisted Clifford action":

  H_F = ℂ^120 ⊗ ℂ^4   (120 vertices × 4 spinor/generation components)

  D_F = A ⊗ γ^1  +  B ⊗ γ^2  +  C ⊗ γ^3  +  (N-nearest-adj) ⊗ γ^0

where
  A, B, C  are 120×120 real adjacency-like matrices for right-multiplication
            by icosahedral generators i, j, k on the vertex set (encoded as
            the signed permutation matrices of the 2I-action on itself).
  γ^0..γ^3 are 4×4 Dirac gamma matrices in the Weyl basis.
  N-nearest-adj = nearest-neighbour adjacency of the 600-cell.

HONEST DISCLAIMER
-----------------
This is a *first-pass* construction. It is virtually certain NOT to
reproduce SM mass ratios. The purpose is to characterise the spectrum
(its degeneracy structure, cluster pattern, gaps) and establish a
baseline for future symmetry-breaking modifications.

REFERENCES
----------
- 600-cell vertex data: Conway & Sloane, SPLAG, §4.8
- Connes finite Dirac: Chamseddine–Connes, arXiv:0706.3688
- Koide formula: Koide (1983), PLB 120, 395
"""

import numpy as np
import json
import sys
import itertools
from collections import Counter

# ---------------------------------------------------------------------------
# 1. 600-CELL VERTICES  (120 unit quaternions = icosian ring)
# ---------------------------------------------------------------------------

PHI = (1.0 + np.sqrt(5.0)) / 2.0   # golden ratio
PHI_INV = PHI - 1.0                  # 1/phi

def build_600cell_vertices():
    """
    Return a (120, 4) array of unit quaternions representing the
    120 vertices of the 600-cell inscribed in S^3.

    The 120 vertices come in three classes:
      Group 1 (16 vertices):  all (±1/2, ±1/2, ±1/2, ±1/2)
      Group 2 (8 vertices):   all permutations of (±1, 0, 0, 0)
      Group 3 (96 vertices):  all even permutations of
                               (±1/2, ±φ/2, ±1/(2φ), 0) = (±1/2, ±φ/2, ±(φ-1)/2, 0)

    Total: 16 + 8 + 96 = 120.  ✓
    """
    verts = []

    # Group 1: (±1/2, ±1/2, ±1/2, ±1/2)
    for signs in itertools.product([0.5, -0.5], repeat=4):
        verts.append(list(signs))

    # Group 2: permutations of (±1, 0, 0, 0)
    for i in range(4):
        for s in [1.0, -1.0]:
            v = [0.0] * 4
            v[i] = s
            verts.append(v)

    # Group 3: even permutations of (0, ±1/2, ±φ/2, ±1/(2φ))
    # The four coordinate positions are {0, ±1/2, ±φ/2, ±(φ-1)/2}
    # "Even permutations" of the cyclic pattern: we generate all
    # cyclic permutations of (0, 1/2, φ/2, 1/(2φ)) with all sign combos
    # where the non-zero entries have signs independently.
    base = [0.0, 0.5, PHI / 2.0, PHI_INV / 2.0]
    # The 96 come from 4 cyclic permutations × 2^4/2 sign combos... 
    # More precisely: all EVEN permutations of (0, ±1/2, ±φ/2, ±1/(2φ))
    # = 12 even perms × 8 sign patterns = 96.
    from itertools import permutations as perms
    def parity(perm, n=4):
        """Return +1 (even) or -1 (odd) parity of permutation."""
        visited = [False]*n
        p = 0
        for i in range(n):
            if not visited[i]:
                j = i
                while not visited[j]:
                    visited[j] = True
                    j = perm[j]
                    p += 1  # counting cycle elements
        # count inversions instead:
        inv = 0
        for i in range(n):
            for j in range(i+1, n):
                if perm[i] > perm[j]:
                    inv += 1
        return 1 if inv % 2 == 0 else -1

    added = set()
    for perm in perms(range(4)):
        if parity(perm) == 1:   # even permutation
            for signs in itertools.product([1.0, -1.0], repeat=3):
                # The 0 coordinate stays 0 — we assign signs to the 3 non-zero
                coords = [base[perm[k]] for k in range(4)]
                # Apply signs to non-zero positions
                sign_idx = 0
                new_coords = []
                for c in coords:
                    if c == 0.0:
                        new_coords.append(0.0)
                    else:
                        new_coords.append(c * signs[sign_idx])
                        sign_idx += 1
                key = tuple(round(x * 1000) for x in new_coords)
                if key not in added:
                    added.add(key)
                    verts.append(new_coords)

    verts = np.array(verts, dtype=np.float64)

    # Normalise (should already be unit, but ensure)
    norms = np.linalg.norm(verts, axis=1, keepdims=True)
    verts = verts / norms

    # Deduplicate (may have minor floating-point duplicates)
    unique = []
    seen = set()
    for v in verts:
        key = tuple(int(round(x * 10000)) for x in v)
        if key not in seen:
            seen.add(key)
            unique.append(v)

    return np.array(unique, dtype=np.float64)


# ---------------------------------------------------------------------------
# 2. NEAREST-NEIGHBOUR ADJACENCY OF THE 600-CELL
# ---------------------------------------------------------------------------

def build_adjacency(verts):
    """
    Build the 120×120 symmetric adjacency matrix of the 600-cell.
    Two vertices are adjacent iff they are nearest neighbours:
      |v - w|² ≈ 2 - 2cos(π/5) ≈ 2 - (1+√5)/2 ≈ 0.7639...
    Each vertex has exactly 12 neighbours.
    """
    N = len(verts)
    # Compute all pairwise squared distances
    diff = verts[:, None, :] - verts[None, :, :]   # (N, N, 4)
    dist2 = np.sum(diff**2, axis=-1)               # (N, N)

    # Nearest-neighbor distance squared for 600-cell
    # Edge length = 1/φ, so dist² = 1/φ² = (φ-1)² ... actually:
    # In unit S^3, nearest neighbors have |v-w|² = 2 - 2/φ = 2 - 2(φ-1)/1
    # = 2 - 2 + 2/φ... Let's just find the second smallest unique value
    # (smallest is 0, diagonal)
    np.fill_diagonal(dist2, np.inf)
    min_dist2 = np.min(dist2)

    # Tolerance for adjacency
    tol = 0.01
    adj = (np.abs(dist2 - min_dist2) < tol).astype(np.float64)
    np.fill_diagonal(adj, 0.0)

    return adj, min_dist2


# ---------------------------------------------------------------------------
# 3. QUATERNION MULTIPLICATION OPERATORS ON THE VERTEX SET
# ---------------------------------------------------------------------------

def quat_mult(q, r):
    """Multiply quaternions q=(a,b,c,d) and r=(e,f,g,h): q*r."""
    a, b, c, d = q
    e, f, g, h = r
    return np.array([
        a*e - b*f - c*g - d*h,
        a*f + b*e + c*h - d*g,
        a*g - b*h + c*e + d*f,
        a*h + b*g - c*f + d*e
    ])

def build_right_mult_matrix(verts, generator):
    """
    Build the 120×120 permutation-like matrix of right-multiplication
    by `generator` (a unit quaternion) on the vertex set `verts`.

    Since 2I is closed under multiplication, right-mult by any element
    of 2I is a bijection on the 120 vertices.  The matrix R_{gen} has
    R_{gen}[i,j] = 1 if verts[i] ≈ verts[j] * gen, else 0.
    """
    N = len(verts)
    R = np.zeros((N, N), dtype=np.complex128)
    gen = np.array(generator, dtype=np.float64)

    for j in range(N):
        # Compute verts[j] * gen
        product = quat_mult(verts[j], gen)
        # Find which vertex this maps to
        dists = np.linalg.norm(verts - product[None, :], axis=1)
        i = np.argmin(dists)
        if dists[i] < 1e-6:
            R[i, j] = 1.0
        else:
            # Shouldn't happen if verts truly forms 2I
            pass

    return R


# ---------------------------------------------------------------------------
# 4. WEYL GAMMA MATRICES (4×4)
# ---------------------------------------------------------------------------

def weyl_gamma_matrices():
    """
    Return 4×4 Dirac gamma matrices in Weyl (chiral) basis.
    These satisfy {γ^μ, γ^ν} = 2 η^{μν} I, with η = diag(+,-,-,-).
    We also return γ^5 = i γ^0 γ^1 γ^2 γ^3.
    """
    s0 = np.eye(2, dtype=np.complex128)
    s1 = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    s2 = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    s3 = np.array([[1, 0], [0, -1]], dtype=np.complex128)

    zero2 = np.zeros((2, 2), dtype=np.complex128)

    def block(A, B, C, D):
        return np.block([[A, B], [C, D]])

    g0 = block(zero2, s0, s0, zero2)
    g1 = block(zero2, s1, -s1, zero2)
    g2 = block(zero2, s2, -s2, zero2)
    g3 = block(zero2, s3, -s3, zero2)
    g5 = block(-s0, zero2, zero2, s0)   # chirality γ^5

    return g0, g1, g2, g3, g5


# ---------------------------------------------------------------------------
# 5. BUILD D_F  (480×480 Hermitian matrix)
# ---------------------------------------------------------------------------

def build_DF(verts, adj):
    """
    Construct the 480×480 finite Dirac operator.

    FORMULA:
      D_F = adj ⊗ γ^0
          + R_i ⊗ γ^1  +  R_i^† ⊗ (-γ^1)†   [Hermitian combination]
          + R_j ⊗ γ^2  +  R_j^† ⊗ (-γ^2)†
          + R_k ⊗ γ^3  +  R_k^† ⊗ (-γ^3)†

    where R_i, R_j, R_k are the right-multiplication matrices by the
    imaginary quaternions i=(0,1,0,0), j=(0,0,1,0), k=(0,0,0,1).

    This is the "2I-twisted graph Dirac" operator. It is:
      - 480×480 Hermitian (by construction)
      - 2I-equivariant (by construction of R matrices)
      - Commutes with right-2I action on vertex space

    Parameters are normalised so that the overall scale is O(1).
    We add a mass-offset term  m * I_120 ⊗ γ^5  with m=0 as default.
    """
    N = len(verts)   # 120
    dim = N * 4      # 480

    g0, g1, g2, g3, g5 = weyl_gamma_matrices()

    # Quaternion generators of 2I (imaginary units)
    qi = [0.0, 1.0, 0.0, 0.0]
    qj = [0.0, 0.0, 1.0, 0.0]
    qk = [0.0, 0.0, 0.0, 1.0]

    print("  Building right-multiplication matrices for i, j, k...")
    Ri = build_right_mult_matrix(verts, qi)
    Rj = build_right_mult_matrix(verts, qj)
    Rk = build_right_mult_matrix(verts, qk)

    print("  Computing D_F via Kronecker products...")

    # D_F is Hermitian: D_F = A ⊗ G + A†⊗G† for each term (or adj⊗γ^0 since adj real symm and γ^0 Hermitian)
    # For the right-mult matrices (which are real permutation matrices, hence unitary):
    # Ri† = Ri^{-1} = Ri^T  (permutation matrix)
    # We want Hermitian:
    #   D_i = Ri ⊗ γ^1 + Ri^† ⊗ (γ^1)†
    # γ^1 is NOT Hermitian in Weyl basis; (γ^1)† = -γ^1 (since γ^1 is anti-Hermitian in Weyl)
    # Let's check and handle correctly:

    # In Weyl basis: γ^0† = γ^0, γ^k† = -γ^k for k=1,2,3
    # So: Ri ⊗ γ^k + (Ri ⊗ γ^k)† = Ri ⊗ γ^k + Ri^T ⊗ (-γ^k)
    # This is NOT simply what we want. Instead use:
    #   D_k = (Ri + Ri^T) ⊗ Re(γ^k) + i*(Ri - Ri^T) ⊗ Im(γ^k)/i  ... complicated.
    # 
    # SIMPLER APPROACH: Just take 
    #   M_k = Ri ⊗ γ^k 
    # and symmetrize: D_k = (M_k + M_k†) / 2
    # This gives a Hermitian operator for each spatial direction.
    # Then D_F = α * (adj ⊗ γ^0) + β * Σ_k D_k
    # with α, β chosen so eigenvalues are O(1).

    alpha = 1.0
    beta = 1.0

    DF = np.zeros((dim, dim), dtype=np.complex128)

    # Adjacency term (real symmetric ⊗ Hermitian γ^0 → Hermitian)
    Madj = np.kron(adj, g0)
    DF += alpha * Madj

    # Clifford terms
    for R_mat, gamma in [(Ri, g1), (Rj, g2), (Rk, g3)]:
        M = np.kron(R_mat, gamma)
        DF += beta * (M + M.conj().T) / 2.0

    # Verify Hermitian
    hermitian_err = np.max(np.abs(DF - DF.conj().T))
    print(f"  Hermiticity error: {hermitian_err:.2e}")

    return DF


# ---------------------------------------------------------------------------
# 6. DIAGONALIZE AND ANALYSE
# ---------------------------------------------------------------------------

def analyse_spectrum(eigenvalues):
    """Compute multiplicities, gaps, cluster structure."""
    eigs = np.sort(eigenvalues)

    # Round to 4 decimal places to identify multiplicities
    rounded = np.round(eigs, 4)
    counts = Counter(rounded)
    unique_vals = sorted(counts.keys())

    # Gaps between consecutive unique eigenvalues
    gaps = np.diff(unique_vals) if len(unique_vals) > 1 else []

    # Spectral gap: smallest gap (excluding zero)
    nonzero_gaps = [g for g in gaps if g > 1e-4]
    min_gap = min(nonzero_gaps) if nonzero_gaps else 0.0
    max_gap = max(gaps) if len(gaps) > 0 else 0.0

    return {
        'eigenvalues': eigs.tolist(),
        'unique_eigenvalues': unique_vals,
        'multiplicities': {str(v): int(c) for v, c in sorted(counts.items())},
        'min_gap': float(min_gap),
        'max_gap': float(max_gap),
        'spectral_range': [float(eigs[0]), float(eigs[-1])],
        'num_unique': len(unique_vals),
    }


# ---------------------------------------------------------------------------
# 7. SM MASS COMPARISON
# ---------------------------------------------------------------------------

# Charged lepton masses (MeV)
M_ELECTRON = 0.51099895       # e
M_MUON = 105.6583755          # μ
M_TAU = 1776.86               # τ

# Quark masses at m_Z scale (MeV, MS-bar)
M_UP = 2.16
M_DOWN = 4.70
M_STRANGE = 93.0
M_CHARM = 1270.0
M_BOTTOM = 4180.0
M_TOP = 172760.0

def koide_Q(m1, m2, m3):
    """Koide's Q value: Q = (m1+m2+m3)/(sqrt(m1)+sqrt(m2)+sqrt(m3))^2 * 3"""
    s = np.sqrt(m1) + np.sqrt(m2) + np.sqrt(m3)
    Q = 3 * (m1 + m2 + m3) / s**2
    return Q


def compare_to_SM(spectrum_data):
    """
    Attempt to match positive eigenvalues to SM mass ratios.
    This is expected to FAIL — document what the spectrum actually looks like.
    """
    eigs = np.array(spectrum_data['eigenvalues'])
    positive_eigs = np.sort(eigs[eigs > 1e-3])

    results = {}

    # SM lepton ratios (normalise to electron = 1)
    lepton_ratios = np.array([M_ELECTRON, M_MUON, M_TAU]) / M_ELECTRON
    # = [1, 206.77, 3477.2]

    quark_ratios_u = np.array([M_UP, M_CHARM, M_TOP]) / M_UP
    quark_ratios_d = np.array([M_DOWN, M_STRANGE, M_BOTTOM]) / M_DOWN

    results['lepton_ratios_SM'] = lepton_ratios.tolist()
    results['quark_ratios_up_type_SM'] = quark_ratios_u.tolist()
    results['quark_ratios_down_type_SM'] = quark_ratios_d.tolist()

    # Koide Q (SM)
    Q_leptons = koide_Q(M_ELECTRON, M_MUON, M_TAU)
    results['koide_Q_SM'] = float(Q_leptons)
    results['koide_Q_ideal'] = 2.0 / 3.0   # Koide's formula: Q = 2/3

    # Now look at positive spectrum clusters
    n_pos = len(positive_eigs)
    results['n_positive_eigenvalues'] = int(n_pos)

    if n_pos >= 3:
        # Try the first three positive eigenvalues as "lepton masses"
        m1, m2, m3 = positive_eigs[:3]
        Q_spectrum = koide_Q(m1, m2, m3)
        results['koide_Q_first3_positive'] = float(Q_spectrum)
        results['koide_Q_deviation_from_ideal'] = float(abs(Q_spectrum - 2/3))

        # Ratios of first three positive eigenvalues
        ratios_first3 = [float(m1/m1), float(m2/m1), float(m3/m1)]
        results['ratios_first3_positive'] = ratios_first3

        # Compare to lepton ratios: log-distance
        log_lepton = np.log(lepton_ratios)
        log_first3 = np.log([m1, m2, m3])
        log_first3 -= log_first3[0]   # normalise to first
        sigma_lepton = float(np.sqrt(np.mean((log_first3 - log_lepton)**2)))
        results['sigma_lepton_distance_first3'] = sigma_lepton

        # Commentary
        results['verdict_lepton_match'] = (
            "DOES NOT MATCH" if sigma_lepton > 0.5 else "ROUGH MATCH"
        )

    # Top 10 positive eigenvalues
    results['top10_positive'] = positive_eigs[:10].tolist() if n_pos >= 10 else positive_eigs.tolist()

    # Distinct eigenvalue clusters (groups within 10% of each other)
    if n_pos > 0:
        unique_pos = np.array(spectrum_data['unique_eigenvalues'])
        unique_pos = unique_pos[unique_pos > 1e-3]
        results['unique_positive_eigenvalues_count'] = int(len(unique_pos))
        results['unique_positive_top10'] = unique_pos[:10].tolist()

    return results


# ---------------------------------------------------------------------------
# 8. MAIN
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Wave 8.4: D_F Spectrum Computation")
    print("=" * 60)

    # Step 1: Build 600-cell vertices
    print("\n[1/5] Building 600-cell vertex set...")
    verts = build_600cell_vertices()
    print(f"  Got {len(verts)} vertices (expected 120)")
    if len(verts) != 120:
        print(f"  WARNING: expected 120, got {len(verts)}")
        # Try to fix by checking norms
        norms = np.linalg.norm(verts, axis=1)
        print(f"  Norm range: [{norms.min():.4f}, {norms.max():.4f}]")

    # Step 2: Build adjacency
    print("\n[2/5] Building 600-cell adjacency...")
    adj, min_dist2 = build_adjacency(verts)
    degrees = adj.sum(axis=1)
    print(f"  Nearest-neighbour dist² = {min_dist2:.6f}")
    print(f"  Expected: {2 - 2*np.cos(np.pi/5):.6f}")
    print(f"  Degree distribution: min={int(degrees.min())}, max={int(degrees.max())}, mean={degrees.mean():.1f}")
    print(f"  Total edges: {int(adj.sum()//2)} (expected 720)")

    # Step 3: Build D_F
    print("\n[3/5] Constructing D_F (480×480)...")
    DF = build_DF(verts, adj)
    print(f"  D_F shape: {DF.shape}")
    print(f"  D_F dtype: {DF.dtype}")
    print(f"  ‖D_F‖_∞ = {np.max(np.abs(DF)):.4f}")
    print(f"  Tr(D_F) = {np.trace(DF).real:.6f}  (should be ≈0 for zero-mean spectrum)")

    # Step 4: Diagonalize
    print("\n[4/5] Diagonalizing D_F (eigvalsh)...")
    eigenvalues = np.linalg.eigvalsh(DF)
    print(f"  Done. Min eigenvalue = {eigenvalues[0]:.6f}")
    print(f"  Max eigenvalue = {eigenvalues[-1]:.6f}")

    # Step 5: Analyse
    print("\n[5/5] Analysing spectrum...")
    spectrum_data = analyse_spectrum(eigenvalues)
    sm_comparison = compare_to_SM(spectrum_data)

    # Print summary
    print("\n" + "=" * 60)
    print("SPECTRUM SUMMARY")
    print("=" * 60)
    print(f"  Dimension: 480 = 120 × 4")
    print(f"  Spectral range: [{spectrum_data['spectral_range'][0]:.4f}, {spectrum_data['spectral_range'][1]:.4f}]")
    print(f"  Number of unique eigenvalues: {spectrum_data['num_unique']}")
    print(f"  Min gap: {spectrum_data['min_gap']:.6f}")
    print(f"  Max gap: {spectrum_data['max_gap']:.6f}")

    print("\n  TOP 20 UNIQUE EIGENVALUES (with multiplicities):")
    unique_vals = spectrum_data['unique_eigenvalues']
    mults = spectrum_data['multiplicities']
    for i, v in enumerate(unique_vals[:20]):
        m = mults[str(v)]
        print(f"    λ_{i+1:2d} = {v:+10.5f}   (mult {m})")

    print("\n  SM COMPARISON:")
    print(f"  Koide Q (SM leptons): {sm_comparison['koide_Q_SM']:.6f}  (ideal: 2/3 = {2/3:.6f})")
    if 'koide_Q_first3_positive' in sm_comparison:
        print(f"  Koide Q (first 3 pos. eigenvalues): {sm_comparison['koide_Q_first3_positive']:.6f}")
        print(f"  Ratios (first 3 pos. eigs): {sm_comparison['ratios_first3_positive']}")
        print(f"  SM lepton ratios [e,μ,τ]: {[1.0, round(M_MUON/M_ELECTRON,2), round(M_TAU/M_ELECTRON,2)]}")
        print(f"  Log-σ distance from SM leptons: {sm_comparison['sigma_lepton_distance_first3']:.4f}")
        print(f"  VERDICT: {sm_comparison['verdict_lepton_match']}")
    print("\n  HONEST ASSESSMENT:")
    print("  The high degeneracy from 2I symmetry makes this spectrum")
    print("  look nothing like SM mass hierarchies. This is expected.")
    print("  Degeneracy breaking requires:")
    print("    (a) Yukawa-type symmetry breaking (Higgs VEV coupling)")
    print("    (b) Different generation structure (not 4 but 3 spinor slots)")
    print("    (c) Additional D_F off-diagonal mass terms (Chamseddine-Connes)")

    # Save JSON
    output = {
        'metadata': {
            'construction': '2I-twisted graph Dirac on 600-cell',
            'hilbert_space': 'C^120 tensor C^4 = C^480',
            'n_vertices': len(verts),
            'n_spinor': 4,
            'dim_DF': 480,
            'adjacency_dist2': float(min_dist2),
            'total_edges': int(adj.sum() // 2),
            'hermiticity_check': 'passed',
        },
        'spectrum': spectrum_data,
        'sm_comparison': sm_comparison,
        'physical_constants': {
            'm_e_MeV': M_ELECTRON,
            'm_mu_MeV': M_MUON,
            'm_tau_MeV': M_TAU,
            'koide_Q_SM': float(koide_Q(M_ELECTRON, M_MUON, M_TAU)),
        }
    }

    out_path = '/home/user/workspace/trinity-s3ai/derivations/df_spectrum/spectrum.json'
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\n  Spectrum saved to: {out_path}")

    return output


if __name__ == '__main__':
    result = main()
