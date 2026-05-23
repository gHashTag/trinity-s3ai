#!/usr/bin/env python3
"""
Wave 12.4 — One-loop Coleman–Weinberg-like refinement of Higgs mass
====================================================================
Attempt to reduce the tree-level discrepancy
    m_H(tree) = 132.88 GeV  →  PDG 125.10 GeV
by adding 1-loop fermion and boson contributions to the effective potential.

Physical model
--------------
Tree-level potential (from 600-cell geometry, Wave 11.5):
    V_0(φ) = -μ² φ²/2 + λ φ⁴/4,   μ² = λ v²,   v = 246 GeV
    λ = 1/φ⁴  (geometric coupling)

One-loop Coleman–Weinberg effective potential (hard-cutoff version):
    V_1(φ) = (1/64π²) Σ_i (-1)^(2s_i) n_i M_i⁴(φ)
             × [ln(M_i²(φ)/Λ²) - c_i]
where:
    s_i = spin,  n_i = degrees of freedom,
    c_i = 3/2 for fermions, 5/6 for gauge bosons,
    Λ   = UV cutoff (spectral-action scale, ~10¹⁶ GeV).

Mass functions (task convention):
    Fermions:  M_f(φ) = y_f φ
    Bosons:    M_b(φ) = g_b φ / 2

The Higgs mass is the curvature of V = V_0 + V_1 at the minimum φ = v:
    m_H² = V_0''(v) + V_1''(v) - V_1'(v)/v
         = 2λ v² + Δm_H²

After simplification (see derivation in code comments):
    Δm_H²,fermion = - (n_f y_f⁴ / 8π²) v² ln(y_f² v² / Λ²)
    Δm_H²,boson   = + (n_b g_b⁴ / 1024π²) v² [8 ln(g_b² v² / (4Λ²)) + 16/3]

Yukawa couplings from 600-cell spectrum
----------------------------------------
The 480×480 discrete Dirac operator D_F^{600} has 240 positive eigenvalues.
We treat them as Yukawa couplings up to an overall scale c:
    y_i = c · λ_i^+    (i = 1 … 240)

A natural scale is obtained by mapping the largest eigenvalue to the top Yukawa:
    c_natural = y_top / max(λ_i^+) ≈ 0.158

Important note on renormalization scale
----------------------------------------
The hard-cutoff CW formula with Λ = 10¹⁶ GeV produces logarithms of order
ln(v²/Λ²) ≈ -60.  In the Standard Model the 1-loop shift of the Higgs pole
mass is only a few GeV because the large logs are resummed via the
renormalization group (¯MS).  For a fair comparison we therefore also report
results with a "physical matching scale" μ ~ v, which replaces Λ in the log.
This is equivalent to evaluating the running couplings at the electroweak scale.

Honest controls
---------------
1. Plot m_H vs. Yukawa scale c.
2. Plot m_H vs. cutoff / matching scale.
3. Report whether 125.10 GeV is reachable without forced tuning.

References
----------
* S. Coleman, E. Weinberg, Phys. Rev. D 7 (1973) 1888.
* A. Connes, M. Marcolli, *Noncommutative Geometry, Quantum Fields
  and Motives*, AMS, 2008 (Chapter 1).
"""

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PHI = (1.0 + np.sqrt(5.0)) / 2.0          # φ  ≈ 1.6180339887
LAMBDA_HIGGS = 1.0 / PHI ** 4              # geometric coupling from 600-cell
VEV = 246.0                                # GeV
M_H_PDG = 125.10                           # GeV
M_H_PDG_ERR = 0.14                         # GeV

# Tree-level Higgs mass (must match Wave 11.5)
M2_TREE = 2.0 * LAMBDA_HIGGS * VEV ** 2
M_H_TREE = float(np.sqrt(M2_TREE))

# SM gauge couplings at electroweak scale (PDG 2024)
G2 = 0.652                                 # SU(2)_L
G1 = 0.357                                 # U(1)_Y
GZ = np.sqrt(G1**2 + G2**2)                # Z coupling

# CW degrees of freedom
N_W = 6     # 3 polarizations × 2 charge states
N_Z = 3     # 3 polarizations

# Physical top Yukawa (on-shell)
Y_TOP = 0.996


def load_eigenvalues(path: Path) -> np.ndarray:
    """Load the 480 eigenvalues saved by Wave 11.5."""
    ev = np.load(path)
    assert ev.shape == (480,), f"Expected 480 eigenvalues, got {ev.shape}"
    return ev


def fermion_loop_delta_m2(y: np.ndarray, n_dof: float, Lambda: float, v: float = VEV) -> float:
    """
    1-loop Higgs-mass² shift from fermions (hard-cutoff CW).

    Derivation:
        V_1,f(φ) = - (n_dof / 64π²) y⁴ φ⁴ [ln(y² φ²/Λ²) - 3/2]
        V_1,f'(φ)  = - (n_dof / 64π²) y⁴ φ³ [4 ln(...) - 6 + 2]
        V_1,f''(φ) = - (n_dof / 64π²) y⁴ φ² [12 ln(...) - 18 + 8 + 8]
                     = - (n_dof / 64π²) y⁴ φ² [12 ln(...) - 2]
        (the extra +8 comes from d/dφ of the 2/φ factor inside the derivative)

        Wait, let's do it carefully:
        L(φ) = ln(y² φ² / Λ²) - 3/2
        V_1 = A φ⁴ L,   A = - n_dof y⁴ / (64π²)
        V_1' = A [4φ³ L + φ⁴ L'] = A φ³ [4L + φ L']
        L' = 2/φ
        V_1' = A φ³ [4L + 2]
        V_1'' = A [3φ²(4L+2) + φ³ (4L' + 0)]
              = A φ² [12L + 6 + 4φ(2/φ)]
              = A φ² [12L + 6 + 8]
              = A φ² [12L + 14]

        Δm² = V_1''(v) - V_1'(v)/v
             = A v² [12L(v) + 14 - 4L(v) - 2]
             = A v² [8L(v) + 12]
             = A v² [8(ln(y²v²/Λ²) - 3/2) + 12]
             = A v² [8 ln(y²v²/Λ²)]
             = - (n_dof y⁴ / 8π²) v² ln(y²v²/Λ²)

    For an array of Yukawas the contributions add linearly.
    """
    if len(y) == 0 or n_dof == 0:
        return 0.0

    arg = (y ** 2 * v ** 2) / (Lambda ** 2)
    arg = np.maximum(arg, 1e-300)
    log_terms = np.log(arg)

    delta_m2 = - (n_dof / (8.0 * np.pi ** 2)) * v ** 2 * np.sum(y ** 4 * log_terms)
    return float(delta_m2)


def boson_loop_delta_m2(g: float, n_dof: float, Lambda: float, v: float = VEV) -> float:
    """
    1-loop Higgs-mass² shift from a gauge boson (hard-cutoff CW).

    Derivation (same pattern as fermions, c = 5/6):
        V_1,b(φ) = + (n_dof / 64π²) (g⁴/16) φ⁴ [ln(g² φ²/(4Λ²)) - 5/6]
        A_b = n_dof g⁴ / (1024 π²)
        Δm² = A_b v² [8 ln(g²v²/(4Λ²)) + 16/3]
    """
    arg = (g ** 2 * v ** 2) / (4.0 * Lambda ** 2)
    arg = max(arg, 1e-300)
    log_term = np.log(arg)
    delta_m2 = (n_dof * g ** 4 / (1024.0 * np.pi ** 2)) * v ** 2 * (8.0 * log_term + 16.0 / 3.0)
    return float(delta_m2)


def compute_m_h(
    yukawas: np.ndarray,
    Lambda: float,
    include_bosons: bool = False,
    n_dof_per_fermion: float = 1.0,
    v: float = VEV,
) -> dict:
    """
    Compute tree-level and 1-loop Higgs mass.

    Parameters
    ----------
    yukawas : array of Yukawa couplings
    Lambda : cutoff / matching scale (GeV)
    include_bosons : whether to include W and Z loops
    n_dof_per_fermion : degrees of freedom per eigenvalue in CW sum
    v : Higgs VEV

    Returns dict with tree and 1-loop masses, plus the individual shifts.
    """
    m2_tree = 2.0 * LAMBDA_HIGGS * v ** 2

    # Fermion contribution (sum over all provided Yukawas)
    delta_m2_f = fermion_loop_delta_m2(yukawas, n_dof=n_dof_per_fermion, Lambda=Lambda, v=v)

    delta_m2_b = 0.0
    if include_bosons:
        delta_m2_w = boson_loop_delta_m2(G2, N_W, Lambda, v)
        delta_m2_z = boson_loop_delta_m2(GZ, N_Z, Lambda, v)
        delta_m2_b = delta_m2_w + delta_m2_z

    delta_m2_total = delta_m2_f + delta_m2_b
    m2_total = m2_tree + delta_m2_total

    if m2_total < 0:
        m_h_total = float("nan")
    else:
        m_h_total = float(np.sqrt(m2_total))

    m2_f_only = m2_tree + delta_m2_f
    m_h_f_only = float(np.sqrt(max(m2_f_only, 0.0))) if m2_f_only >= 0 else float("nan")

    return {
        "m_H_tree_GeV": float(np.sqrt(m2_tree)),
        "m_H_1loop_fermions_only_GeV": m_h_f_only,
        "m_H_1loop_total_GeV": m_h_total,
        "delta_m2_fermions_GeV2": float(delta_m2_f),
        "delta_m2_bosons_GeV2": float(delta_m2_b),
        "delta_m2_total_GeV2": float(delta_m2_total),
    }


def sigma_distance(m_h: float, pdg: float = M_H_PDG, err: float = M_H_PDG_ERR) -> float:
    return abs(m_h - pdg) / err


def scan_yukawa_scale(ev_pos: np.ndarray, Lambda: float, n_dof: float = 1.0):
    """Scan c and return (c_values, m_H_fermions, m_H_total)."""
    c_vals = np.linspace(0.0, 0.5, 800)
    m_h_f = []
    m_h_tot = []
    for c in c_vals:
        y = c * ev_pos
        res = compute_m_h(y, Lambda=Lambda, include_bosons=True, n_dof_per_fermion=n_dof)
        m_h_f.append(res["m_H_1loop_fermions_only_GeV"])
        m_h_tot.append(res["m_H_1loop_total_GeV"])
    return c_vals, np.array(m_h_f), np.array(m_h_tot)


def scan_scale(ev_pos: np.ndarray, c: float, n_dof: float = 1.0):
    """Scan the cutoff / matching scale and return (Lambda, m_H_f, m_H_tot)."""
    log_Lambda = np.linspace(1, 19, 600)
    Lambda_vals = 10.0 ** log_Lambda
    y = c * ev_pos
    m_h_f = []
    m_h_tot = []
    for Lam in Lambda_vals:
        res = compute_m_h(y, Lambda=Lam, include_bosons=True, n_dof_per_fermion=n_dof)
        m_h_f.append(res["m_H_1loop_fermions_only_GeV"])
        m_h_tot.append(res["m_H_1loop_total_GeV"])
    return Lambda_vals, np.array(m_h_f), np.array(m_h_tot)


def main():
    out_dir = Path("/Users/playra/trinity-s3ai/derivations/higgs_spectral_action")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Wave 12.4 — One-loop Coleman–Weinberg refinement")
    print("=" * 70)

    # -----------------------------------------------------------------------
    # Load spectrum
    # -----------------------------------------------------------------------
    ev_path = out_dir / "eigenvalues.npy"
    eigenvalues = load_eigenvalues(ev_path)
    ev_pos = np.sort(eigenvalues[eigenvalues > 1e-8])
    print(f"\n[1] Spectrum loaded")
    print(f"    Positive eigenvalues : {len(ev_pos)}")
    print(f"    Range [min, max]     : [{ev_pos.min():.4f}, {ev_pos.max():.4f}]")

    # -----------------------------------------------------------------------
    # Tree level
    # -----------------------------------------------------------------------
    print(f"\n[2] Tree-level prediction")
    print(f"    λ_Higgs = 1/φ⁴       = {LAMBDA_HIGGS:.10f}")
    print(f"    m_H (tree)           = {M_H_TREE:.4f} GeV")
    print(f"    PDG m_H              = {M_H_PDG:.2f} ± {M_H_PDG_ERR:.2f} GeV")
    print(f"    Δ(tree)              = {abs(M_H_TREE - M_H_PDG):.4f} GeV  ({sigma_distance(M_H_TREE):.1f}σ)")

    # -----------------------------------------------------------------------
    # Natural Yukawa scale
    # -----------------------------------------------------------------------
    c_natural = Y_TOP / ev_pos.max()
    y_natural = c_natural * ev_pos
    print(f"\n[3] Natural Yukawa scale")
    print(f"    c_natural = y_top / λ_max = {c_natural:.6f}")
    print(f"    Yukawa range : [{y_natural.min():.6f}, {y_natural.max():.4f}]")
    print(f"    Mean Yukawa  : {y_natural.mean():.6f}")
    print(f"    Sum y_i⁴     : {np.sum(y_natural**4):.4f}")
    print(f"    (SM top only: 3 y_t⁴ ≈ {3 * Y_TOP**4:.4f})")

    # -----------------------------------------------------------------------
    # 1-loop with GUT-scale cutoff (hard-cutoff CW)
    # -----------------------------------------------------------------------
    Lambda_GUT = 1e16
    print(f"\n[4] Hard-cutoff CW at Λ = {Lambda_GUT:.0e} GeV")
    res_gut = compute_m_h(y_natural, Lambda=Lambda_GUT, include_bosons=True, n_dof_per_fermion=1.0)
    print(f"    m_H (fermions only)   = {res_gut['m_H_1loop_fermions_only_GeV']:.4f} GeV")
    print(f"    m_H (fermions+bosons) = {res_gut['m_H_1loop_total_GeV']:.4f} GeV")
    print(f"    → Unphysically large because ln(v²/Λ²) ≈ {np.log(VEV**2 / Lambda_GUT**2):.1f}")

    # -----------------------------------------------------------------------
    # 1-loop with physical matching scale μ = v
    # -----------------------------------------------------------------------
    mu_phys = VEV
    print(f"\n[5] Physical matching scale μ = {mu_phys:.0f} GeV (¯MS-like)")
    res_phys = compute_m_h(y_natural, Lambda=mu_phys, include_bosons=True, n_dof_per_fermion=1.0)
    sigma_f = sigma_distance(res_phys["m_H_1loop_fermions_only_GeV"])
    sigma_fb = sigma_distance(res_phys["m_H_1loop_total_GeV"])
    print(f"    m_H (fermions only)   = {res_phys['m_H_1loop_fermions_only_GeV']:.4f} GeV  ({sigma_f:.1f}σ)")
    print(f"    m_H (fermions+bosons) = {res_phys['m_H_1loop_total_GeV']:.4f} GeV  ({sigma_fb:.1f}σ)")
    print(f"    Δm² fermions          = {res_phys['delta_m2_fermions_GeV2']:.4e} GeV²")
    print(f"    Δm² bosons            = {res_phys['delta_m2_bosons_GeV2']:.4e} GeV²")

    # -----------------------------------------------------------------------
    # Scan Yukawa scale
    # -----------------------------------------------------------------------
    print(f"\n[6] Scanning Yukawa scale c …")
    c_vals, mH_f, mH_tot = scan_yukawa_scale(ev_pos, Lambda=mu_phys, n_dof=1.0)

    # Find best-fit c
    valid = np.isfinite(mH_tot)
    if np.any(valid):
        idx_best = np.nanargmin(np.abs(mH_tot[valid] - M_H_PDG))
        c_best = c_vals[valid][idx_best]
        mH_best = mH_tot[valid][idx_best]
    else:
        c_best = 0.0
        mH_best = M_H_TREE

    print(f"    Best fit (scan) : c = {c_best:.4f}, m_H = {mH_best:.4f} GeV")
    print(f"    Natural c       : {c_natural:.4f}")
    if abs(c_natural - c_best) / max(c_best, 1e-10) < 0.5:
        print("    → Natural scale is within ~50% of best-fit scale.")
    else:
        print("    → Natural scale is FAR from best-fit scale.")

    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axhline(M_H_PDG, color="green", linestyle="--", linewidth=1.5, label=f"PDG {M_H_PDG} GeV")
    ax.axhline(M_H_PDG + 2 * M_H_PDG_ERR, color="green", linestyle=":", alpha=0.5)
    ax.axhline(M_H_PDG - 2 * M_H_PDG_ERR, color="green", linestyle=":", alpha=0.5)
    ax.axhline(M_H_TREE, color="black", linestyle="-.", alpha=0.6, label=f"Tree level {M_H_TREE:.1f} GeV")
    ax.plot(c_vals, mH_f, color="blue", label="Fermions only", alpha=0.8)
    ax.plot(c_vals, mH_tot, color="red", label="Fermions + bosons", alpha=0.8)
    ax.axvline(c_natural, color="gray", linestyle="-.", alpha=0.6, label=f"Natural c = {c_natural:.3f}")
    ax.set_xlabel("Yukawa scale factor c")
    ax.set_ylabel(r"$m_H$ [GeV]")
    ax.set_title("1-loop Higgs mass vs. Yukawa scale (μ = 246 GeV)")
    ax.set_xlim([0, c_vals.max()])
    ax.set_ylim([50, 250])
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_dir / "oneloop_mh_vs_yukawa_scale.png", dpi=200)
    plt.close(fig)
    print(f"    Plot saved: {out_dir / 'oneloop_mh_vs_yukawa_scale.png'}")

    # -----------------------------------------------------------------------
    # Scan cutoff / matching scale
    # -----------------------------------------------------------------------
    print(f"\n[7] Scanning matching scale Λ …")
    Lambda_vals, mH_L_f, mH_L_tot = scan_scale(ev_pos, c=c_natural, n_dof=1.0)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axhline(M_H_PDG, color="green", linestyle="--", linewidth=1.5, label=f"PDG {M_H_PDG} GeV")
    ax.axhline(M_H_PDG + 2 * M_H_PDG_ERR, color="green", linestyle=":", alpha=0.5)
    ax.axhline(M_H_PDG - 2 * M_H_PDG_ERR, color="green", linestyle=":", alpha=0.5)
    ax.axhline(M_H_TREE, color="black", linestyle="-.", alpha=0.6, label=f"Tree level {M_H_TREE:.1f} GeV")
    ax.plot(Lambda_vals, mH_L_f, color="blue", label="Fermions only", alpha=0.8)
    ax.plot(Lambda_vals, mH_L_tot, color="red", label="Fermions + bosons", alpha=0.8)
    ax.set_xscale("log")
    ax.set_xlabel(r"Matching scale $\Lambda$ / $\mu$ [GeV]")
    ax.set_ylabel(r"$m_H$ [GeV]")
    ax.set_title("1-loop Higgs mass vs. matching scale (natural Yukawa scale)")
    ax.set_ylim([50, 250])
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_dir / "oneloop_mh_vs_cutoff.png", dpi=200)
    plt.close(fig)
    print(f"    Plot saved: {out_dir / 'oneloop_mh_vs_cutoff.png'}")

    # -----------------------------------------------------------------------
    # What if we use the SM-style degrees of freedom?
    # -----------------------------------------------------------------------
    print(f"\n[8] Sanity check: SM-like degrees of freedom")
    # In the SM CW potential the top contributes with n_dof = 12 (3 colours × 4 Dirac components).
    # If we rescale our 240 eigenvalues to represent 120 Dirac fermions (n_dof = 4 each),
    # the total would be n_dof = 480 — far too large.  Instead we show what happens if we
    # pretend the 240 eigenvalues are 240 Weyl fermions (n_dof = 2 each, total = 480).
    # This is still too large, but we report it for completeness.
    res_w = compute_m_h(y_natural, Lambda=mu_phys, include_bosons=True, n_dof_per_fermion=2.0)
    print(f"    n_dof = 2 per eigenvalue (Weyl): m_H = {res_w['m_H_1loop_total_GeV']:.4f} GeV")

    # Another sanity check: use ONLY the largest eigenvalue as the top
    y_top_only = np.array([y_natural.max()])
    res_top = compute_m_h(y_top_only, Lambda=mu_phys, include_bosons=True, n_dof_per_fermion=12.0)
    print(f"    Top only (n_dof=12, y={y_natural.max():.3f}): m_H = {res_top['m_H_1loop_total_GeV']:.4f} GeV")

    # -----------------------------------------------------------------------
    # Verdict
    # -----------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    best_mh = res_phys["m_H_1loop_total_GeV"]
    best_sigma = sigma_fb

    print(f"Tree level:              m_H = {M_H_TREE:.4f} GeV  ({sigma_distance(M_H_TREE):.1f}σ)")
    print(f"1-loop (hard Λ=10¹⁶):    m_H = {res_gut['m_H_1loop_total_GeV']:.4f} GeV  (unphysical)")
    print(f"1-loop (μ=v, fermions):  m_H = {res_phys['m_H_1loop_fermions_only_GeV']:.4f} GeV  ({sigma_f:.1f}σ)")
    print(f"1-loop (μ=v, ferm+bos):  m_H = {res_phys['m_H_1loop_total_GeV']:.4f} GeV  ({sigma_fb:.1f}σ)")
    print(f"Best-fit scan:           m_H = {mH_best:.4f} GeV  ({sigma_distance(mH_best):.1f}σ)")
    print(f"SM top-only mimic:       m_H = {res_top['m_H_1loop_total_GeV']:.4f} GeV")

    if best_sigma < 2.0:
        verdict = (
            "MARGINAL: 1-loop corrections bring m_H within 2σ of PDG. "
            "However, this relies on a specific choice of matching scale and Yukawa mapping."
        )
    elif best_sigma < 5.0:
        verdict = (
            "WEAK: 1-loop corrections reduce the discrepancy somewhat, "
            "but the prediction remains several σ away from PDG. "
            "No clear structural mechanism is identified."
        )
    else:
        verdict = (
            "NEGATIVE.  The 600-cell Dirac spectrum does not naturally mimic "
            "the SM 1-loop correction to the Higgs mass.\n\n"
            "Key findings:\n"
            f"  1. Hard-cutoff CW with Λ = 10¹⁶ GeV gives m_H ≈ {res_gut['m_H_1loop_total_GeV']:.0f} GeV — "
            "unphysically large because the 600-cell contains ~240 eigenvalues with O(1) "
            "Yukawas, whereas the SM has only one heavy fermion (top).\n"
            f"  2. Using a physical matching scale μ = v gives m_H ≈ {best_mh:.1f} GeV — "
            f"still {best_sigma:.1f}σ from PDG.\n"
            f"  3. The best-fit Yukawa scale c ≈ {c_best:.3f} is ~{(c_best/c_natural - 1)*100:.0f}% from the natural scale "
            f"c ≈ {c_natural:.3f} (which maps the largest eigenvalue to the top Yukawa).\n"
            "  4. The σ-field mechanism (Connes–Marcolli) remains the only known way "
            "to reach 125 GeV in NCG, and Wave 5.3 proved it unavailable in H₄."
        )
    print(verdict)
    print("=" * 70)

    # -----------------------------------------------------------------------
    # Save results
    # -----------------------------------------------------------------------
    results = {
        "wave": "12.4",
        "tree_level": {
            "lambda_higgs": float(LAMBDA_HIGGS),
            "m_H_GeV": M_H_TREE,
            "sigma_pdg": float(sigma_distance(M_H_TREE)),
        },
        "natural_scale": {
            "c": float(c_natural),
            "y_max": float(y_natural.max()),
            "y_mean": float(y_natural.mean()),
            "sum_y4": float(np.sum(y_natural**4)),
        },
        "hard_cutoff_GUT": {
            "Lambda_GeV": Lambda_GUT,
            "m_H_fermions_only_GeV": res_gut["m_H_1loop_fermions_only_GeV"],
            "m_H_total_GeV": res_gut["m_H_1loop_total_GeV"],
        },
        "physical_matching_scale": {
            "mu_GeV": mu_phys,
            "m_H_fermions_only_GeV": res_phys["m_H_1loop_fermions_only_GeV"],
            "m_H_total_GeV": res_phys["m_H_1loop_total_GeV"],
            "delta_m2_fermions_GeV2": res_phys["delta_m2_fermions_GeV2"],
            "delta_m2_bosons_GeV2": res_phys["delta_m2_bosons_GeV2"],
            "sigma_pdg": float(sigma_fb),
        },
        "best_fit_scan": {
            "c_best": float(c_best),
            "m_H_best_GeV": float(mH_best),
            "sigma_pdg_best": float(sigma_distance(mH_best)),
        },
        "sm_top_only_mimic": {
            "m_H_GeV": res_top["m_H_1loop_total_GeV"],
        },
        "verdict": verdict,
    }

    with open(out_dir / "oneloop_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {out_dir / 'oneloop_results.json'}")

    return results


if __name__ == "__main__":
    main()
