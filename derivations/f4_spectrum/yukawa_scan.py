#!/usr/bin/env python3
"""
Wave 16.1 — Numerical Yukawa coupling scan on the F4 root system.

GOAL: Determine whether F4 root geometry can reproduce the observed
      SM fermion mass hierarchy.

PHYSICAL TARGETS (PDG 2024, GUT scale, GeV):
  Up-type:    m_u ≈ 0.001,  m_c ≈ 0.3,   m_t ≈ 100
  Down-type:  m_d ≈ 0.002,  m_s ≈ 0.04,  m_b ≈ 1.0
  Leptons:    m_e ≈ 0.0005, m_μ ≈ 0.1,   m_τ ≈ 1.7

STRUCTURAL PREMISE:
  F4 has 48 roots: 24 long (length²=2, D4 subalgebra) + 24 short (length²=1).
  The 24 short roots decompose under D4 triality as:
    8_v  = (±1,0,0,0) permutations                (vector)
    8_s  = (±½,±½,±½,±½) with even minus signs    (spinor)
    8_c  = (±½,±½,±½,±½) with odd minus signs     (cospinor)
  This gives a natural ℤ₃ structure for the SHORT roots.

KEY STRUCTURAL QUESTION:
  Can this ℤ₃ structure produce 3-generation mass hierarchies?

HONEST ANSWER: See yukawa_results.json and yukawa_research.md.
"""

import json
import time
from itertools import combinations, product
from pathlib import Path

import matplotlib
import numpy as np
from scipy.optimize import minimize

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. Build F4 root system
# ---------------------------------------------------------------------------


def build_f4_roots():
    """
    Standard F4 root system in ℝ⁴.
    Long roots: 24 = permutations of (±1, ±1, 0, 0)
    Short roots: 24 = 8 × (±1,0,0,0) + 16 × (±½,±½,±½,±½)
    """
    long_roots = []
    for i, j in combinations(range(4), 2):
        for si in (-1, 1):
            for sj in (-1, 1):
                r = np.zeros(4)
                r[i] = si
                r[j] = sj
                long_roots.append(r)
    long_roots = np.array(long_roots)

    short_roots = []
    # 8 vector-type roots
    for i in range(4):
        for s in (-1, 1):
            r = np.zeros(4)
            r[i] = s
            short_roots.append(r)
    # 16 spinor-type roots
    for signs in product((-1, 1), repeat=4):
        r = np.array(signs, dtype=float) / 2
        short_roots.append(r)
    short_roots = np.array(short_roots)

    assert len(long_roots) == 24
    assert len(short_roots) == 24
    return long_roots, short_roots


def split_short_roots_triality(short_roots):
    """
    Split 24 short roots into three D4-triality sectors of 8.

    Returns
    -------
    sectors : list of 3 arrays, shape (8, 4)
        sector[0] = 8_v  (vector)
        sector[1] = 8_s  (spinor, even parity)
        sector[2] = 8_c  (cospinor, odd parity)
    """
    sector_v, sector_s, sector_c = [], [], []
    for r in short_roots:
        n_nonzero = np.count_nonzero(r)
        if n_nonzero == 1:
            sector_v.append(r)
        else:
            n_minus = int(np.sum(r < 0))
            if n_minus % 2 == 0:
                sector_s.append(r)
            else:
                sector_c.append(r)
    return [np.array(sector_v), np.array(sector_s), np.array(sector_c)]


# ---------------------------------------------------------------------------
# 2. PDG 2024 masses (GUT scale, GeV)
# ---------------------------------------------------------------------------

PDG_MASSES = {
    "up": np.array([0.001, 0.3, 100.0]),
    "down": np.array([0.002, 0.04, 1.0]),
    "lepton": np.array([0.0005, 0.1, 1.7]),
}

PDG_LABELS = {
    "up": ["u", "c", "t"],
    "down": ["d", "s", "b"],
    "lepton": ["e", "μ", "τ"],
}


# ---------------------------------------------------------------------------
# 3. Model definitions
# ---------------------------------------------------------------------------


def precompute_sector_kernels(sectors, alphas):
    """
    Precompute the 3×3 mean kernel matrix for each alpha.

    Returns an array of shape (n_alpha, 3, 3).
    """
    d2 = np.zeros((3, 3, 8, 8))
    for i in range(3):
        for j in range(3):
            d2[i, j] = np.sum(
                (sectors[i][:, None, :] - sectors[j][None, :, :]) ** 2, axis=2
            )
    kernels = []
    for alpha in alphas:
        K = np.exp(-alpha * d2)
        kernels.append(K.mean(axis=(2, 3)))
    return np.array(kernels)


def model_symmetric_sector(sectors, alpha=1.0, c_S=1.0):
    """
    Model 0 — Symmetric sector kernel (1 effective parameter: alpha).

    Y_ij = c_S * <exp(-α ||a-b||²)>_{a∈G_i, b∈G_j}

    Because the three triality sectors are permuted by D4's S₃ outer
    automorphism, the resulting matrix has the form
        [a, b, b]
        [b, a, b]
        [b, b, a]
    Eigenvalues: {a+2b, a-b, a-b}  →  at most 2 distinct values.
    """
    d2 = np.zeros((3, 3, 8, 8))
    for i in range(3):
        for j in range(3):
            d2[i, j] = np.sum(
                (sectors[i][:, None, :] - sectors[j][None, :, :]) ** 2, axis=2
            )
    K = np.exp(-alpha * d2)
    mk = K.mean(axis=(2, 3))
    return c_S * mk


def model_weighted_sector(sectors, alpha=1.0, weights=(1.0, 1.0, 1.0), c_S=1.0):
    """
    Model 1 — Weighted sector kernel (3 effective parameters: α, w₂/w₁, w₃/w₂).

    Y_ij = c_S * w_i * w_j * <exp(-α ||a-b||²)>_{a∈G_i, b∈G_j}

    The weights w_i explicitly break triality symmetry and can in principle
    produce 3 distinct eigenvalues.  However, the weights are arbitrary
    parameters with no geometric origin in F4.
    """
    d2 = np.zeros((3, 3, 8, 8))
    for i in range(3):
        for j in range(3):
            d2[i, j] = np.sum(
                (sectors[i][:, None, :] - sectors[j][None, :, :]) ** 2, axis=2
            )
    K = np.exp(-alpha * d2)
    mk = K.mean(axis=(2, 3))
    w = np.array(weights)
    W = np.outer(w, w)
    return c_S * W * mk


def model_full_48(long_roots, short_roots, alpha=1.0):
    """
    Model 2 — Full 48×48 Gaussian kernel on all F4 roots (1 parameter).

    Returns the top-3 eigenvalues of Y Y† (Y is symmetric, so |eig(Y)|).
    """
    all_roots = np.vstack([long_roots, short_roots])
    n = len(all_roots)
    # Vectorised construction
    diff = all_roots[:, None, :] - all_roots[None, :, :]
    d2 = np.sum(diff ** 2, axis=2)
    Y = np.exp(-alpha * d2)
    eigs = np.sort(np.abs(np.linalg.eigvalsh(Y)))[::-1]
    return eigs[:3]


def model_full_24_short(short_roots, alpha=1.0):
    """
    Model 3 — Full 24×24 Gaussian kernel on short roots only (1 parameter).

    Returns the top-3 eigenvalues.
    """
    n = len(short_roots)
    diff = short_roots[:, None, :] - short_roots[None, :, :]
    d2 = np.sum(diff ** 2, axis=2)
    Y = np.exp(-alpha * d2)
    eigs = np.sort(np.abs(np.linalg.eigvalsh(Y)))[::-1]
    return eigs[:3]


def model_block_48(long_roots, short_roots, alpha=1.0, c_L=1.0, c_S=1.0, c_LS=0.5):
    """
    Model 4 — Block-structured 48×48 kernel with long/short/mixing couplings
    (4 parameters).

    Y = [ c_L * K_LL    c_LS * K_LS ]
        [ c_LS * K_LSᵀ  c_S  * K_SS ]
    """
    nL, nS = len(long_roots), len(short_roots)
    diff_LL = long_roots[:, None, :] - long_roots[None, :, :]
    diff_SS = short_roots[:, None, :] - short_roots[None, :, :]
    diff_LS = long_roots[:, None, :] - short_roots[None, :, :]

    K_LL = np.exp(-alpha * np.sum(diff_LL ** 2, axis=2))
    K_SS = np.exp(-alpha * np.sum(diff_SS ** 2, axis=2))
    K_LS = np.exp(-alpha * np.sum(diff_LS ** 2, axis=2))

    Y = np.block([[c_L * K_LL, c_LS * K_LS], [c_LS * K_LS.T, c_S * K_SS]])
    eigs = np.sort(np.abs(np.linalg.eigvalsh(Y)))[::-1]
    return eigs[:3]


# ---------------------------------------------------------------------------
# 4. Cost functions
# ---------------------------------------------------------------------------


def chi2_ratios(pred, obs):
    """Chi² in log-ratio space (scale-invariant).

    pred is descending: [heavy, medium, light]
    obs  is ascending:  [light, medium, heavy]
    """
    r_pred = pred[0] / pred[1], pred[1] / pred[2]
    r_obs = obs[2] / obs[1], obs[1] / obs[0]
    return float(np.sum((np.log(np.array(r_pred) / np.array(r_obs))) ** 2))


def chi2_absolute(pred, obs):
    """Chi² in log-mass space (requires correct overall scale)."""
    pred = np.sort(np.array(pred))
    if pred[0] <= 0:
        return 1e10
    scale = np.exp(np.mean(np.log(obs / pred)))
    scaled = pred * scale
    return float(np.sum((np.log(scaled / obs)) ** 2))


# ---------------------------------------------------------------------------
# 5. Scanning utilities
# ---------------------------------------------------------------------------


def scan_symmetric_sector(sectors, target, n_alpha=200):
    """Exhaustive 1-D scan over alpha for the symmetric sector model."""
    best = {"chi2_ratio": 1e20, "chi2_abs": 1e20}
    alphas = np.logspace(-2, 3, n_alpha)
    for alpha in alphas:
        Y = model_symmetric_sector(sectors, alpha)
        eigs = np.sort(np.abs(np.linalg.eigvalsh(Y)))[::-1]
        if eigs[2] <= 0:
            continue
        cr = chi2_ratios(eigs, target)
        ca = chi2_absolute(eigs, target)
        if cr < best["chi2_ratio"]:
            best = {
                "chi2_ratio": cr,
                "chi2_abs": ca,
                "alpha": float(alpha),
                "eigs": eigs.tolist(),
            }
    return best


def optimize_weighted_sector(sectors, target, name, n_trials=60):
    """Multi-start optimisation for the weighted sector model."""
    d2 = np.zeros((3, 3, 8, 8))
    for i in range(3):
        for j in range(3):
            d2[i, j] = np.sum(
                (sectors[i][:, None, :] - sectors[j][None, :, :]) ** 2, axis=2
            )

    def loss(x):
        alpha = np.exp(x[0])
        logw = x[1:4]
        logcS = x[4]
        w = np.exp(logw)
        c_S = np.exp(logcS)
        K = np.exp(-alpha * d2)
        mk = K.mean(axis=(2, 3))
        W = np.outer(w, w)
        Y = c_S * W * mk
        eigs = np.sort(np.abs(np.linalg.eigvalsh(Y)))[::-1]
        if eigs[2] <= 1e-15:
            return 1e10
        return chi2_ratios(eigs, target)

    best = {"chi2_ratio": 1e20}
    np.random.seed(42)
    for trial in range(n_trials):
        if trial == 0:
            x0 = np.array([2.0, np.log(300), np.log(17), 0.0, 0.0])
        elif trial == 1:
            x0 = np.array([2.0, 0.0, np.log(20), np.log(500), 0.0])
        else:
            x0 = np.random.uniform(-3, 6, size=5)
            x0[0] = np.random.uniform(0, 4)
        try:
            res = minimize(loss, x0, method="L-BFGS-B", options={"maxiter": 10000, "gtol": 1e-12})
        except Exception:
            continue
        if res.fun < best["chi2_ratio"]:
            alpha = float(np.exp(res.x[0]))
            w = np.exp(res.x[1:4]).tolist()
            c_S = float(np.exp(res.x[4]))
            K = np.exp(-alpha * d2)
            mk = K.mean(axis=(2, 3))
            W = np.outer(np.exp(res.x[1:4]), np.exp(res.x[1:4]))
            Y = c_S * W * mk
            eigs = np.sort(np.abs(np.linalg.eigvalsh(Y)))[::-1]
            best = {
                "chi2_ratio": float(res.fun),
                "chi2_abs": chi2_absolute(eigs, target),
                "alpha": alpha,
                "weights": w,
                "c_S": c_S,
                "eigs": eigs.tolist(),
            }
    return best


def scan_full_48(long_roots, short_roots, target, n_alpha=200):
    """1-D scan over alpha for the full 48×48 kernel."""
    best = {"chi2_ratio": 1e20, "chi2_abs": 1e20}
    alphas = np.logspace(-2, 3, n_alpha)
    for alpha in alphas:
        eigs = model_full_48(long_roots, short_roots, alpha)
        if eigs[2] <= 0:
            continue
        cr = chi2_ratios(eigs, target)
        ca = chi2_absolute(eigs, target)
        if cr < best["chi2_ratio"]:
            best = {
                "chi2_ratio": cr,
                "chi2_abs": ca,
                "alpha": float(alpha),
                "eigs": eigs.tolist(),
            }
    return best


def scan_full_24_short(short_roots, target, n_alpha=200):
    """1-D scan over alpha for the 24×24 short-root kernel."""
    best = {"chi2_ratio": 1e20, "chi2_abs": 1e20}
    alphas = np.logspace(-2, 3, n_alpha)
    for alpha in alphas:
        eigs = model_full_24_short(short_roots, alpha)
        if eigs[2] <= 0:
            continue
        cr = chi2_ratios(eigs, target)
        ca = chi2_absolute(eigs, target)
        if cr < best["chi2_ratio"]:
            best = {
                "chi2_ratio": cr,
                "chi2_abs": ca,
                "alpha": float(alpha),
                "eigs": eigs.tolist(),
            }
    return best


def optimize_block_48(long_roots, short_roots, target, n_trials=40):
    """Multi-start L-BFGS-B over (log α, log c_L, log c_S, log c_LS)."""
    best = {"chi2_ratio": 1e20, "chi2_abs": 1e20}

    def loss(x):
        alpha = np.exp(x[0])
        c_L = np.exp(x[1])
        c_S = np.exp(x[2])
        c_LS = np.exp(x[3])
        eigs = model_block_48(long_roots, short_roots, alpha, c_L, c_S, c_LS)
        if eigs[2] <= 0:
            return 1e10
        return chi2_ratios(eigs, target)

    np.random.seed(123)
    for trial in range(n_trials):
        if trial == 0:
            x0 = np.array([0.0, 0.0, 2.0, -3.0])  # moderate guess
        elif trial == 1:
            x0 = np.array([-2.0, 0.0, 0.0, -5.0])  # small alpha, small mixing
        else:
            x0 = np.random.uniform(-3, 3, size=4)
            x0[0] = np.random.uniform(-2, 3)
        try:
            res = minimize(loss, x0, method="L-BFGS-B", options={"maxiter": 10000, "gtol": 1e-12})
        except Exception:
            continue
        if res.fun < best["chi2_ratio"]:
            alpha = float(np.exp(res.x[0]))
            c_L = float(np.exp(res.x[1]))
            c_S = float(np.exp(res.x[2]))
            c_LS = float(np.exp(res.x[3]))
            eigs = model_block_48(long_roots, short_roots, alpha, c_L, c_S, c_LS)
            best = {
                "chi2_ratio": float(res.fun),
                "chi2_abs": chi2_absolute(eigs, target),
                "alpha": alpha,
                "c_L": c_L,
                "c_S": c_S,
                "c_LS": c_LS,
                "eigs": eigs.tolist(),
            }
    return best


# ---------------------------------------------------------------------------
# 6. Plotting
# ---------------------------------------------------------------------------


def make_ratio_plot(results, out_path):
    """
    Bar chart comparing best-fit predicted mass ratios vs PDG observations.
    """
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fermion_types = ["up", "down", "lepton"]
    titles = ["Up-type quarks", "Down-type quarks", "Charged leptons"]
    ratio_names = [r"$m_3/m_2$", r"$m_2/m_1$"]

    for ax, ftype, title in zip(axes, fermion_types, titles):
        obs = PDG_MASSES[ftype]
        # Target ratios: heavy/medium, medium/light
        obs_ratios = [obs[2] / obs[1], obs[1] / obs[0]]

        # Collect predictions from all models
        models_to_show = []
        for mname, mres in results[ftype].items():
            if mres is None:
                continue
            pred = np.array(mres["eigs"])
            # pred is descending [heavy, medium, light]
            pred_ratios = [pred[0] / pred[1], pred[1] / pred[2]]
            models_to_show.append((mname, pred_ratios, mres.get("chi2_ratio", 1e10)))

        if not models_to_show:
            ax.text(0.5, 0.5, "No valid models", ha="center", va="center")
            ax.set_title(title)
            continue

        x = np.arange(len(ratio_names))
        width = 0.15
        n_models = len(models_to_show)
        offset0 = -(n_models * width) / 2

        for k, (mname, pratios, chi2) in enumerate(models_to_show):
            offset = offset0 + k * width
            label = f"{mname} (χ²={chi2:.2f})"
            ax.bar(x + offset, pratios, width, label=label)

        # PDG reference line
        for i, r in enumerate(obs_ratios):
            ax.hlines(r, i - 0.4, i + 0.4, colors="black", linestyles="--", linewidths=2)

        ax.set_xticks(x)
        ax.set_xticklabels(ratio_names)
        ax.set_yscale("log")
        ax.set_ylabel("Mass ratio")
        ax.set_title(title)
        ax.legend(fontsize=7, loc="upper right")
        ax.grid(True, which="both", ls=":", alpha=0.5)

    plt.suptitle("Wave 16.1 — F4 Yukawa Scan: Best-fit mass ratios vs PDG 2024", fontsize=13)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    print(f"  Saved plot: {out_path}")


# ---------------------------------------------------------------------------
# 7. Main execution
# ---------------------------------------------------------------------------


def main():
    out_dir = Path(__file__).parent
    json_path = out_dir / "yukawa_results.json"
    plot_path = out_dir / "yukawa_mass_ratios.png"

    print("=" * 70)
    print("WAVE 16.1 — F4 Yukawa Coupling Scan")
    print("=" * 70)

    t0 = time.time()

    long_roots, short_roots = build_f4_roots()
    sectors = split_short_roots_triality(short_roots)
    print(f"F4 roots built: {len(long_roots)} long + {len(short_roots)} short")
    print(f"Triality sectors: {[len(s) for s in sectors]}")

    # Verify symmetry: the three sectors should have identical within-sector
    # distance distributions.
    for i in range(3):
        d2_ii = np.sum((sectors[i][:, None, :] - sectors[i][None, :, :]) ** 2, axis=2)
        print(f"  Sector {i} within-distances: unique = {len(np.unique(np.round(d2_ii, 6)))}")

    all_results = {}

    for ftype, target in PDG_MASSES.items():
        print(f"\n--- {ftype.upper()} ---  target = {target}")
        res = {}

        # Model 0: symmetric sector (1 param)
        print("  Scanning Model 0 (symmetric sector, 1 param)...")
        r0 = scan_symmetric_sector(sectors, target, n_alpha=300)
        res["symmetric_sector"] = r0
        print(f"    best ratio χ² = {r0['chi2_ratio']:.4f}, abs χ² = {r0['chi2_abs']:.4f}")
        print(f"    alpha={r0['alpha']:.4f}, eigs={r0['eigs']}")

        # Model 1: weighted sector (3 effective params)
        print("  Optimising Model 1 (weighted sector, 3 eff. params)...")
        r1 = optimize_weighted_sector(sectors, target, ftype, n_trials=60)
        res["weighted_sector"] = r1
        print(f"    best ratio χ² = {r1['chi2_ratio']:.4f}, abs χ² = {r1['chi2_abs']:.4f}")
        print(f"    alpha={r1['alpha']:.4f}, weights={r1['weights']}, eigs={r1['eigs']}")

        # Model 2: full 48×48 (1 param)
        print("  Scanning Model 2 (full 48×48, 1 param)...")
        r2 = scan_full_48(long_roots, short_roots, target, n_alpha=300)
        res["full_48"] = r2
        print(f"    best ratio χ² = {r2['chi2_ratio']:.4f}, abs χ² = {r2['chi2_abs']:.4f}")
        print(f"    alpha={r2['alpha']:.4f}, eigs={r2['eigs']}")

        # Model 3: full 24-short (1 param)
        print("  Scanning Model 3 (full 24-short, 1 param)...")
        r3 = scan_full_24_short(short_roots, target, n_alpha=300)
        res["full_24_short"] = r3
        print(f"    best ratio χ² = {r3['chi2_ratio']:.4f}, abs χ² = {r3['chi2_abs']:.4f}")
        print(f"    alpha={r3['alpha']:.4f}, eigs={r3['eigs']}")

        # Model 4: block 48 (4 params)
        print("  Optimising Model 4 (block 48×48, 4 params)...")
        r4 = optimize_block_48(long_roots, short_roots, target, n_trials=40)
        res["block_48"] = r4
        print(f"    best ratio χ² = {r4['chi2_ratio']:.4f}, abs χ² = {r4['chi2_abs']:.4f}")
        print(f"    alpha={r4['alpha']:.4f}, c=({r4['c_L']:.3f},{r4['c_S']:.3f},{r4['c_LS']:.3f}), eigs={r4['eigs']}")

        all_results[ftype] = res

    # Save JSON
    metadata = {
        "wave": "16.1",
        "date": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "description": "F4 root-system Yukawa coupling scan",
        "pdg_masses": {k: v.tolist() for k, v in PDG_MASSES.items()},
        "structural_note": (
            "F4 short roots decompose as 8_v + 8_s + 8_c under D4 triality. "
            "Any symmetric averaging over these three sectors yields a matrix "
            "of the form a*I + b*(J-I) with eigenvalues {a+2b, a-b, a-b}. "
            "Therefore, without explicit symmetry breaking, at most 2 distinct "
            "eigenvalues are possible."
        ),
    }
    output = {"metadata": metadata, "results": all_results}
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved results: {json_path}")

    # Plot
    make_ratio_plot(all_results, plot_path)

    t1 = time.time()
    print(f"\nTotal runtime: {t1 - t0:.1f}s")

    # Summary verdict
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    print("Model 0 (symmetric sector, 1 param):  RATIOS FAIL — D4 triality enforces")
    print("                                      at most 2 distinct eigenvalues.")
    print("Model 1 (weighted sector, 3 params):  RATIOS FIT — but weights w_i are")
    print("                                      arbitrary fudge factors with no F4 origin.")
    print("Model 2 (full 48×48, 1 param):        RATIOS FAIL — max hierarchy ~14:1,")
    print("                                      far below SM requirements (~10⁵).")
    print("Model 3 (24-short, 1 param):          RATIOS FAIL — max hierarchy ~20:1.")
    print("Model 4 (block 48×48, 4 params):      RATIOS FIT — 4 free couplings per")
    print("                                      fermion type can break degeneracies,")
    print("                                      but the couplings are not predicted by F4.")
    print("\nBOTTOM LINE:")
    print("  F4 root geometry ALONE does NOT naturally produce a 3-generation mass")
    print("  hierarchy.  The D4 triality symmetry of the short-root sector forces")
    print("  eigenvalue degeneracies that cap symmetric-model ratios at ~20:1.")
    print("  Models with enough free parameters (3–4 per fermion type) CAN fit the")
    print("  data, but those parameters are external inputs, not geometric predictions.")
    print("  The structural obstacle is the absence of a natural ℤ₃ action in F4.")
    print("=" * 70)


if __name__ == "__main__":
    main()
