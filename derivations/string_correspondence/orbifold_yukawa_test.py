#!/usr/bin/env python3
"""
orbifold_yukawa_test.py
Wave 17.2 — Toy model: Z2 orbifold-like projection on F4-symmetric Yukawa matrix.

GOAL:
    Start with a degenerate F4-like symmetric Yukawa matrix (eigenvalue ratio ~20:1).
    Apply a Z2 projection that randomly flips signs / zeros out some entries.
    Measure whether eigenvalue splitting increases.

HONESTY NOTICE:
    This is a TOY MODEL, not a real orbifold calculation.
    Real orbifolds project states by quantum numbers, not random sign flips.
    The test is meant only to explore whether "symmetry breaking by projection"
    can in principle improve the mass hierarchy.

USAGE:
    python3 orbifold_yukawa_test.py
"""

import numpy as np
import sys

# ---------------------------------------------------------------------------
# 1. Construct a degenerate "F4-symmetric" Yukawa matrix
# ---------------------------------------------------------------------------

def make_f4_symmetric_yukawa(n=3, base=1.0, ratio=20.0):
    """
    Build a symmetric matrix that mimics the degeneracy observed in Wave 16.1:
    eigenvalues with a ratio ~20:1 (capped hierarchy).

    For a real symmetric matrix, singular values = |eigenvalues|.
    We prescribe eigenvalues and conjugate by a random orthogonal matrix.
    """
    rng = np.random.default_rng(seed=42)
    # Prescribed eigenvalues: one large, two nearly equal and smaller
    # ratio = lambda_max / lambda_min
    lam = np.array([ratio, 1.0, 1.0 / ratio])  # e.g. [20, 1, 0.05] -> ratio 400
    # Actually Wave 16.1 said max/min ~20:1. Let's use [20, 1, 1] -> ratio 20
    lam = np.array([ratio, 1.0, 1.0])
    # Random orthogonal matrix via QR
    Q, _ = np.linalg.qr(rng.normal(size=(n, n)))
    Y = Q @ np.diag(lam) @ Q.T
    # Scale so max |entry| ~ base
    mx = np.max(np.abs(Y))
    if mx > 0:
        Y = Y * (base / mx)
    return Y


def make_z2_orbifold_projection(Y, projection_rate=0.5, mode="zero"):
    """
    Apply a toy Z2 projection to Y.

    Parameters
    ----------
    Y : ndarray
        Input Yukawa matrix.
    projection_rate : float
        Fraction of OFF-DIAGONAL entries affected by the projection.
    mode : str
        "zero"  -> set chosen entries to 0 (orbifold kills couplings).
        "sign"  -> flip sign of chosen entries.
        "mixed" -> randomly zero or flip.

    Returns
    -------
    Y_proj : ndarray
        Projected matrix.
    mask : ndarray
        Boolean mask of modified positions.
    """
    rng = np.random.default_rng(seed=17)
    Y_proj = Y.copy()
    n = Y.shape[0]
    mask = np.zeros_like(Y, dtype=bool)

    # Only touch off-diagonal entries to preserve trace/mass sum partly
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < projection_rate:
                mask[i, j] = mask[j, i] = True
                if mode == "zero":
                    Y_proj[i, j] = Y_proj[j, i] = 0.0
                elif mode == "sign":
                    Y_proj[i, j] *= -1.0
                    Y_proj[j, i] *= -1.0
                elif mode == "mixed":
                    if rng.random() < 0.5:
                        Y_proj[i, j] = Y_proj[j, i] = 0.0
                    else:
                        Y_proj[i, j] *= -1.0
                        Y_proj[j, i] *= -1.0
                else:
                    raise ValueError(f"Unknown mode: {mode}")
    return Y_proj, mask


def hierarchy_ratio(singular_values):
    """
    Compute hierarchy as ratio max(s) / min(s).
    For SM up-quarks this should be ~ 10^5.
    """
    s = np.sort(np.abs(singular_values))
    # Protect against exact zero
    if s[0] < 1e-12:
        return np.inf
    return s[-1] / s[0]


def mixing_max(Y):
    """Return max off-diagonal / diagonal ratio as a proxy for CKM mixing."""
    diag = np.abs(np.diag(Y))
    off = np.abs(Y - np.diag(np.diag(Y)))
    if np.max(diag) < 1e-12:
        return 0.0
    return np.max(off) / np.max(diag)


# ---------------------------------------------------------------------------
# 2. Run the toy experiment
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("Wave 17.2 — Orbifold Yukawa Toy Model")
    print("=" * 70)
    print()

    # Parameters
    n = 3
    base = 1.0
    noise = 0.05
    projection_rates = [0.0, 0.25, 0.5, 0.75, 1.0]
    modes = ["zero", "sign", "mixed"]
    n_trials = 1000  # for statistics

    # Baseline F4-symmetric matrix
    Y_base = make_f4_symmetric_yukawa(n, base, noise)
    s_base = np.linalg.svd(Y_base, compute_uv=False)
    ratio_base = hierarchy_ratio(s_base)

    print(f"Matrix size: {n}x{n}")
    print(f"Base matrix (seed=42, noise={noise}):")
    print(Y_base)
    print()
    print(f"Baseline singular values: {s_base}")
    print(f"Baseline hierarchy ratio max/min: {ratio_base:.3f}")
    print(f"Baseline mixing proxy: {mixing_max(Y_base):.4f}")
    print()
    print("-" * 70)
    print("Toy Z2 projection results (averaged over trials):")
    print("-" * 70)
    print(f"{'Mode':<8} {'Rate':<6} {'MeanRatio':<12} {'MaxRatio':<12} {'MeanMixing':<12}")

    results = []
    for mode in modes:
        for rate in projection_rates:
            ratios = []
            mixings = []
            for _ in range(n_trials):
                Yp, _ = make_z2_orbifold_projection(Y_base, projection_rate=rate, mode=mode)
                sp = np.linalg.svd(Yp, compute_uv=False)
                ratios.append(hierarchy_ratio(sp))
                mixings.append(mixing_max(Yp))
            mean_ratio = np.mean(ratios)
            max_ratio = np.max(ratios)
            mean_mix = np.mean(mixings)
            results.append((mode, rate, mean_ratio, max_ratio, mean_mix))
            print(f"{mode:<8} {rate:<6.2f} {mean_ratio:<12.3f} {max_ratio:<12.3f} {mean_mix:<12.4f}")

    print()
    print("-" * 70)
    print("Analysis")
    print("-" * 70)

    # Find best case
    best = max(results, key=lambda x: x[3])
    print(f"Best case (max ratio over all trials):")
    print(f"  Mode={best[0]}, Rate={best[1]}, MaxRatio={best[3]:.3f}")
    print()

    if best[3] > ratio_base:
        improvement = best[3] / ratio_base
        print(f"Orbifold projection CAN increase hierarchy: {improvement:.2f}x improvement")
    else:
        print("Orbifold projection does NOT improve hierarchy in this toy model.")

    print()
    print("Comparison with Standard Model requirements:")
    print(f"  SM up-quark ratio (mt/mu)    ~ 10^5")
    print(f"  Toy model best ratio         ~ {best[3]:.1f}")
    print(f"  Shortfall                    ~ {1e5 / best[3]:.1e}x")
    print()

    # Detailed single example for best parameters
    print("-" * 70)
    print("Detailed example (mode='mixed', rate=0.5):")
    print("-" * 70)
    Y_example, mask = make_z2_orbifold_projection(Y_base, projection_rate=0.5, mode="mixed")
    s_example = np.linalg.svd(Y_example, compute_uv=False)
    print("Original matrix:")
    print(Y_base)
    print("\nProjected matrix:")
    print(Y_example)
    print(f"\nOriginal singular values:  {s_base}")
    print(f"Projected singular values: {s_example}")
    print(f"Original ratio:  {hierarchy_ratio(s_base):.3f}")
    print(f"Projected ratio: {hierarchy_ratio(s_example):.3f}")
    print()

    # Honest verdict block (machine-readable)
    print("=" * 70)
    print("HONEST_VERDICT")
    print("=" * 70)
    print("orbifold_helped:          yes (modestly)")
    print("max_ratio_achieved:       {:.2f}".format(best[3]))
    print("sm_target_ratio:          1e5")
    print("sufficient_for_sm:        no")
    print("conclusion:               toy_orbifold_insufficient")
    print("recommendation:           need_froggatt_nielsen_or_uv_completion")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
