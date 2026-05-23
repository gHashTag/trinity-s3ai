#!/usr/bin/env python3
"""
============================================================================
verify_rg_running.py
============================================================================
Numerical verification of RG running from H4 GUT scale to electroweak scale.
Compares 1-loop SM RGE evolution with Trinity formula predictions.

Boundary conditions:
    Λ_H4  = 1.5 × 10^16 GeV  (H4 Coxeter group order 14400)
    α_unif = 1/25             (typical GUT unification coupling)

Trinity predictions (low-energy):
    1/α     = 36φe²/π        ≈ 137.00
    α_s     = (√5−2)/2       ≈ 0.1180
    sin²θ_W = 3φ⁻⁶π²e⁻²      ≈ 0.2233

Usage: python verify_rg_running.py
Output: rg_verification_results.json
============================================================================
"""

import numpy as np
from scipy.integrate import solve_ivp
import json
import os

# ---------------------------------------------------------------------------
# 1. H4 BOUNDARY CONDITIONS
# ---------------------------------------------------------------------------
Lambda_H4  = 1.5e16          # GeV — H4 Coxeter group unification scale
m_Z        = 91.19           # GeV — Z boson mass

alpha_unif_inv = 25.0        # 1/α_unif = 25  →  α_unif = 0.04
g_unif = np.sqrt(4 * np.pi / alpha_unif_inv)   # √(4π/25) ≈ 0.707
alpha_unif = 1.0 / alpha_unif_inv

# Unified inverse couplings at Λ_H4 (SU(5) normalization: α₁ = (5/3)α_Y)
alpha_init = np.array([alpha_unif, alpha_unif, alpha_unif])

# ---------------------------------------------------------------------------
# 2. TRINITY PREDICTIONS
# ---------------------------------------------------------------------------
phi = (1 + np.sqrt(5)) / 2  # Golden ratio φ ≈ 1.6180339887...
e   = np.e                    # Euler's number

trinity_alpha_inv   = 36 * phi * e**2 / np.pi         # 1/α ≈ 137.00
trinity_alpha       = 1.0 / trinity_alpha_inv
trinity_alpha_s     = (np.sqrt(5) - 2) / 2             # α_s ≈ 0.1180
trinity_sin2thetaW  = 3 * phi**(-6) * np.pi**2 / e**2  # sin²θ_W ≈ 0.2233

# ---------------------------------------------------------------------------
# 3. SM 1-LOOP BETA FUNCTIONS
# ---------------------------------------------------------------------------
# Coefficients as specified: b₁ = 41/12, b₂ = −19/24, b₃ = −7/8
# Convention: t = ln(Λ_H4/μ), so t increases as energy decreases.
#   dαᵢ/dt = −bᵢ · αᵢ² / (2π)
def beta(alpha, t):
    """
    SM 1-loop gauge-coupling beta functions.

    Parameters
    ----------
    alpha : array_like, shape (3,)
        Couplings [α₁, α₂, α₃] with SU(5) normalization
        (α₁ = (5/3)α_Y,  α₂ = α_W,  α₃ = α_s).
    t : float
        log(Λ_H4/μ) — increases as we run down to lower energy.

    Returns
    -------
    ndarray, shape (3,)
        [dα₁/dt, dα₂/dt, dα₃/dt]
    """
    b1, b2, b3 = 41/12, -19/24, -7/8
    return np.array([
        -b1 * alpha[0]**2 / (2 * np.pi),
        -b2 * alpha[1]**2 / (2 * np.pi),
        -b3 * alpha[2]**2 / (2 * np.pi)
    ])

# ---------------------------------------------------------------------------
# 4. SOLVE RGE: Λ_H4 → m_Z
# ---------------------------------------------------------------------------
t_final = np.log(Lambda_H4 / m_Z)   # total log-interval
t_span  = [0, t_final]

sol = solve_ivp(
    lambda t, y: beta(y, t),
    t_span,
    alpha_init,
    method='RK45',
    dense_output=True,
    max_step=0.1,
    rtol=1e-9,
    atol=1e-12
)

alpha1_mZ, alpha2_mZ, alpha3_mZ = sol.y[:, -1]

# ---------------------------------------------------------------------------
# 5. EXTRACT LOW-ENERGY PHYSICAL COUPLINGS
# ---------------------------------------------------------------------------
# SU(5) normalization: α₁ = (5/3) α_Y  →  α_Y = (3/5) α₁
alpha_Y_mZ = (3/5) * alpha1_mZ

# Electromagnetic coupling:  1/α_em = (5/3)/α₁ + 1/α₂
alpha_em_mZ = alpha_Y_mZ * alpha2_mZ / (alpha_Y_mZ + alpha2_mZ)

# Weak mixing angle: sin²θ_W = α_em / α₂
sin2thetaW_mZ = alpha_em_mZ / alpha2_mZ

# Strong coupling
alpha_s_mZ = alpha3_mZ

# Inverse couplings
alpha_em_inv_mZ = 1.0 / alpha_em_mZ
alpha_s_inv_mZ  = 1.0 / alpha_s_mZ

# ---------------------------------------------------------------------------
# 6. COMPARE WITH TRINITY PREDICTIONS — COMPUTE ERRORS
# ---------------------------------------------------------------------------
rg_alpha_inv   = alpha_em_inv_mZ
rg_alpha_s     = alpha_s_mZ
rg_sin2thetaW  = sin2thetaW_mZ

err_alpha_inv  = abs(rg_alpha_inv  - trinity_alpha_inv)  / trinity_alpha_inv  * 100
err_alpha_s    = abs(rg_alpha_s    - trinity_alpha_s)    / trinity_alpha_s    * 100
err_sin2thetaW = abs(rg_sin2thetaW - trinity_sin2thetaW) / trinity_sin2thetaW * 100

max_error = max(err_alpha_inv, err_alpha_s, err_sin2thetaW)
avg_error = (err_alpha_inv + err_alpha_s + err_sin2thetaW) / 3.0

# Assessment thresholds
if max_error < 1.0:
    assessment = "RG matches PRECISELY (all errors < 1%)"
elif max_error < 5.0:
    assessment = "RG is CONSISTENT (all errors < 5%)"
elif max_error < 10.0:
    assessment = "RG is APPROXIMATELY CONSISTENT (all errors < 10%)"
else:
    assessment = "RG shows SIGNIFICANT DEVIATIONS from Trinity (errors ≥ 10%)"

# ---------------------------------------------------------------------------
# 7. PRINT REPORT
# ---------------------------------------------------------------------------
separator = "=" * 70

print(separator)
print("  H4 → m_Z  RENORMALIZATION-GROUP VERIFICATION")
print("  Trinity Model vs. 1-Loop SM RGE Running")
print(separator)

print("\n--- BOUNDARY CONDITIONS (at Λ_H4) ---")
print(f"  Λ_H4    = {Lambda_H4:.2e} GeV")
print(f"  1/α_unif = {alpha_unif_inv:.0f}  →  α_unif = {alpha_unif:.6f}")
print(f"  g_unif   = {g_unif:.6f}")

print("\n--- TRINITY PREDICTIONS (at m_Z) ---")
print(f"  1/α     = {trinity_alpha_inv:>12.6f}")
print(f"  α_s     = {trinity_alpha_s:>12.6f}")
print(f"  sin²θ_W = {trinity_sin2thetaW:>12.6f}")

print("\n--- RG RUNNING RESULTS (at m_Z) ---")
print(f"  α₁(m_Z) = {alpha1_mZ:.6f}   (SU(5) normalization)")
print(f"  α₂(m_Z) = {alpha2_mZ:.6f}")
print(f"  α₃(m_Z) = {alpha3_mZ:.6f}")
print(f"  1/α_em  = {rg_alpha_inv:>12.4f}")
print(f"  α_s     = {rg_alpha_s:>12.6f}")
print(f"  sin²θ_W = {rg_sin2thetaW:>12.6f}")

print("\n--- ERRORS ---")
print(f"  α_em  error : {err_alpha_inv:>8.4f}%")
print(f"  α_s   error : {err_alpha_s:>8.4f}%")
print(f"  sin²θ_W err : {err_sin2thetaW:>8.4f}%")
print(f"  MAX  error  : {max_error:>8.4f}%")
print(f"  AVG  error  : {avg_error:>8.4f}%")

print("\n--- ASSESSMENT ---")
print(f"  {assessment}")

# ---------------------------------------------------------------------------
# 8. SAVE RESULTS TO JSON
# ---------------------------------------------------------------------------
results = {
    "metadata": {
        "script": "verify_rg_running.py",
        "description": "H4→m_Z RG running vs Trinity predictions",
        "date": "2025",
        "Lambda_H4_GeV": Lambda_H4,
        "m_Z_GeV": m_Z,
        "log_interval": float(t_final)
    },
    "boundary_conditions": {
        "alpha_unif_inv": float(alpha_unif_inv),
        "alpha_unif": float(alpha_unif),
        "g_unif": float(g_unif)
    },
    "trinity_predictions": {
        "1_over_alpha": float(trinity_alpha_inv),
        "alpha": float(trinity_alpha),
        "alpha_s": float(trinity_alpha_s),
        "sin2_theta_W": float(trinity_sin2thetaW)
    },
    "rg_running_results": {
        "alpha1_mZ_SU5_norm": float(alpha1_mZ),
        "alpha2_mZ": float(alpha2_mZ),
        "alpha3_mZ": float(alpha3_mZ),
        "alpha_em_inv_mZ": float(rg_alpha_inv),
        "alpha_em_mZ": float(alpha_em_mZ),
        "alpha_s_mZ": float(rg_alpha_s),
        "sin2_theta_W_mZ": float(rg_sin2thetaW)
    },
    "errors_percent": {
        "alpha_em_error_pct": float(err_alpha_inv),
        "alpha_s_error_pct": float(err_alpha_s),
        "sin2_theta_W_error_pct": float(err_sin2thetaW),
        "max_error_pct": float(max_error),
        "avg_error_pct": float(avg_error)
    },
    "assessment": assessment
}

output_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(output_dir, "rg_verification_results.json")

with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n--- OUTPUT ---")
print(f"  Results saved to: {output_path}")
print(separator)
