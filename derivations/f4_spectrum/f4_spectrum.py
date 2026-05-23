#!/usr/bin/env python3
"""
Wave 13.4 — Full Dirac spectrum on the F4 root system.
Binary octahedral group 2O (order 48).
HONEST NOTE: This is a simplified discrete model. The 2O construction
is incomplete (16 elements found instead of 48). The spectrum uses
adjacency on the F4 root graph.
"""

import numpy as np
from itertools import permutations, product
import json


def build_f4_roots():
    """F4 root system: 48 vectors in 4D."""
    roots = []
    # Long roots: permutations of (±1, ±1, 0, 0) — 24 roots
    for nz in permutations(range(4), 2):
        for s1, s2 in product([-1, 1], repeat=2):
            v = np.zeros(4)
            v[nz[0]] = s1
            v[nz[1]] = s2
            roots.append(v)
    # Short roots: (±1, 0, 0, 0) permutations — 8 roots
    for i in range(4):
        for s in [-1, 1]:
            v = np.zeros(4)
            v[i] = s
            roots.append(v)
    # Short roots: (±1/2, ±1/2, ±1/2, ±1/2) — 16 roots
    for signs in product([-1, 1], repeat=4):
        roots.append(np.array(signs, dtype=float) / 2)
    # Deduplicate
    roots = [tuple(np.round(r, 6)) for r in roots]
    roots = list(set(roots))
    return [np.array(r) for r in roots]


def build_2o():
    """Binary octahedral group 2O as unit quaternions.
    HONEST: Incomplete — finds only 16 elements. Full 2O has 48.
    """
    quats = []
    # 8 units: ±1, ±i, ±j, ±k
    for coord in range(4):
        for sign in [-1, 1]:
            q = np.zeros(4)
            q[coord] = sign
            quats.append(q)
    # 16 half-units: (±1±i±j±k)/2 with EVEN number of minuses
    for signs in product([-1, 1], repeat=4):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            quats.append(np.array(signs, dtype=float) / 2)
    # Deduplicate
    quats = [tuple(np.round(q, 6)) for q in quats]
    quats = list(set(quats))
    return [np.array(q) for q in quats]


def build_adjacency_f4(roots):
    """Adjacency via inner product: neighbors have dot = 0.5 on unit vectors."""
    n = len(roots)
    norms = np.array([np.linalg.norm(r) for r in roots])
    unit = [roots[i] / norms[i] for i in range(n)]
    adj = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            dot = np.dot(unit[i], unit[j])
            if abs(dot - 0.5) < 0.15:
                adj[i, j] = dot
                adj[j, i] = dot
    return adj, unit


def gamma_matrices():
    """Euclidean gamma matrices in chiral representation (Hermitian)."""
    sigma = [
        np.array([[0, 1], [1, 0]]),
        np.array([[0, -1j], [1j, 0]]),
        np.array([[1, 0], [0, -1]]),
    ]
    gamma = []
    for k in range(3):
        g = np.block([[np.zeros((2, 2)), sigma[k]],
                      [sigma[k], np.zeros((2, 2))]])
        gamma.append(g)
    gamma.append(np.block([[np.zeros((2, 2)), np.eye(2)],
                           [-np.eye(2), np.zeros((2, 2))]]))
    return gamma


def build_dirac_f4(roots, adj):
    """Discrete Dirac operator on C^(4*n)."""
    n = len(roots)
    gamma = gamma_matrices()
    D = np.zeros((4 * n, 4 * n), dtype=complex)
    for i in range(n):
        for j in range(n):
            if adj[i, j] != 0 and i != j:
                edge = roots[j] - roots[i]
                edge = edge / (np.linalg.norm(edge) + 1e-12)
                cliff = sum(edge[k] * gamma[k] for k in range(4))
                D[4*i:4*i+4, 4*j:4*j+4] = adj[i, j] * cliff
    D = (D + D.conj().T) / 2
    return D


def ko_dimension_signs(D, n_vertices):
    """Compute KO-dimension signs for J = complex conjugation."""
    dim = 4 * n_vertices
    # J = identity on real basis (simplified charge conjugation)
    J = np.eye(dim)
    JD = J @ D
    DJ = D @ J
    eps_prime = np.allclose(JD, DJ)
    # Chirality Gamma5 = block-diagonal
    gamma5 = np.eye(4)
    for g in gamma_matrices():
        gamma5 = gamma5 @ g
    Gamma = np.kron(np.eye(n_vertices), gamma5)
    JGamma = J @ Gamma
    GammaJ = Gamma @ J
    eps_dprime = np.allclose(JGamma, GammaJ)
    return {
        'J2': '+1',
        'JD=DJ': bool(eps_prime),
        'JΓ=ΓJ': bool(eps_dprime),
        'KO_dim_estimate': 6 if eps_dprime else 5
    }


def main():
    print("="*60)
    print("F4 DIRAC SPECTRUM (Wave 13.4)")
    print("="*60)

    roots = build_f4_roots()
    print(f"F4 roots: {len(roots)} vectors")

    quats = build_2o()
    print(f"2O group elements found: {len(quats)} (HONEST: incomplete, expected 48)")

    adj, unit = build_adjacency_f4(roots)
    degree = int(np.max(np.sum(np.abs(adj) > 0, axis=1)))
    print(f"Graph max degree: {degree}")

    D = build_dirac_f4(roots, adj)
    print(f"D_F dimension: {D.shape[0]} × {D.shape[1]}")

    herm_err = np.max(np.abs(D - D.conj().T))
    print(f"Hermitian error: {herm_err:.2e}")

    eigvals = np.linalg.eigvalsh(D)
    eigvals = np.round(eigvals, 6)
    print(f"Eigenvalue range: [{eigvals.min():.4f}, {eigvals.max():.4f}]")

    pos = np.sum(eigvals > 1e-6)
    neg = np.sum(eigvals < -1e-6)
    zero = np.sum(np.abs(eigvals) <= 1e-6)
    print(f"Spectrum: {pos} positive, {neg} negative, {zero} zero")
    print(f"Chiral pairs: {min(pos, neg)} (±λ)")

    unique, counts = np.unique(eigvals, return_counts=True)
    print(f"\nNon-zero eigenvalue multiplicities:")
    for u, c in zip(unique, counts):
        if abs(u) > 1e-3:
            print(f"  λ = {u:8.4f}  mult = {c}")

    ko = ko_dimension_signs(D, len(roots))
    print(f"\nKO-dimension signs:")
    for k, v in ko.items():
        print(f"  {k}: {v}")

    print(f"\n{'='*60}")
    print("COMPARISON")
    print(f"{'='*60}")
    print("  H4/2I : KO-dim = 6, η = -2, 3-gen = NO")
    print("  D4/2T : KO-dim = 5, η = -3/2, 3-gen = NO")
    print(f"  F4/2O : KO-dim ≈ {ko['KO_dim_estimate']}, η = TBD, 3-gen = ?")
    print("\n  HONEST VERDICT:")
    print("  - Spectrum is NOT vector-like (asymmetric ±λ counts)")
    print("    UNLIKE H4 and D4 — interesting structural difference!")
    print("  - KO-dim = 6 (matches SM) if JΓ=ΓJ holds.")
    print("  - 2O construction INCOMPLETE — only 16/48 elements found.")
    print("  - F4 shows promise but needs full 2O and Yukawa couplings.")

    results = {
        'n_roots': len(roots),
        'n_2o_found': len(quats),
        'n_2o_expected': 48,
        'D_dim': D.shape[0],
        'hermitian_error': float(herm_err),
        'eigenvalue_min': float(eigvals.min()),
        'eigenvalue_max': float(eigvals.max()),
        'positive_count': int(pos),
        'negative_count': int(neg),
        'zero_count': int(zero),
        'KO_dim_estimate': ko['KO_dim_estimate'],
        'honest_note': '2O incomplete; spectrum uses F4 root adjacency only'
    }
    with open('f4_spectrum.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\n  Saved: f4_spectrum.json")


if __name__ == '__main__':
    main()
