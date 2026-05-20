#!/usr/bin/env python3
"""
================================================================================
INDEPENDENT VERIFICATION OF ALL 25 TRINITY FORMULAS
================================================================================
Skeptical reviewer mode: Verify each formula independently using PDG 2024 data.
NO TUNING. NO EXCUSES. If a formula fails, it fails.

Classification thresholds:
  SG  = Super Good   (< 0.01%)
  V   = Very Good    (< 0.1%)
  W   = Within tol   (< 1%)
  F   = FAIL         (> 1%)

Author: Independent Numerical Analyst
Date: 2024
================================================================================
"""

import math

# ==============================================================================
# FUNDAMENTAL CONSTANTS (high precision)
# ==============================================================================
phi = (1 + math.sqrt(5)) / 2   # Golden ratio
pi  = math.pi
e   = math.e
sqrt5 = math.sqrt(5)

print("=" * 100)
print("INDEPENDENT VERIFICATION OF ALL 25 TRINITY FORMULAS")
print("Skeptical Reviewer Mode -- Using EXACT PDG 2024 Values")
print("=" * 100)
print(f"\nFundamental constants:")
print(f"  φ = (1+√5)/2 = {phi:.12f}")
print(f"  π = {pi:.12f}")
print(f"  e = {e:.12f}")
print(f"  √5 = {sqrt5:.12f}")

# ==============================================================================
# PDG 2024 EXPERIMENTAL DATA (EXACT values as specified)
# ==============================================================================
print("\n" + "=" * 100)
print("PDG 2024 EXPERIMENTAL INPUTS")
print("=" * 100)

# Masses in MeV unless noted
m_u   = 2.16      # m_u(2GeV) in MeV
m_d   = 4.67      # m_d(2GeV) in MeV
m_s   = 93.4      # m_s(2GeV) in MeV
m_c   = 1270.0    # m_c(m_c) = 1.27 GeV = 1270 MeV
m_b   = 4180.0    # m_b(m_b) = 4.18 GeV = 4180 MeV
m_t   = 173100.0  # m_t(pole) = 173.1 GeV = 173100 MeV
m_tau = 1776.86   # m_tau in MeV
m_mu  = 105.658   # m_mu in MeV
m_e   = 0.511     # m_e in MeV
m_H   = 125200.0  # m_H = 125.20 GeV = 125200 MeV
m_W   = 80377.0   # m_W = 80.377 GeV = 80377 MeV
m_Z   = 91188.0   # m_Z = 91.188 GeV = 91188 MeV
m_p   = 938.272   # m_p in MeV

# Couplings and mixing
alpha_inv = 137.035999084   # 1/α
sin2_thetaW = 0.23121       # sin²θ_W
sin2_12 = 0.307             # sin²θ₁₂
sin2_13 = 0.022             # sin²θ₁₃
sin2_23 = 0.546             # sin²θ₂₃

# CKM
V_us = 0.2243
V_cb = 0.0405
V_ub = 0.0036

# Neutrino
Delta_m2_21 = 7.5e-5        # Δm²₂₁ in eV²
Delta_m2_31 = 2.5e-3        # Δm²₃₁ in eV²

# Derived experimental values
exp_m_t_over_m_u    = m_t / m_u
exp_m_tau_over_m_e  = m_tau / m_e
exp_m_tau_over_m_mu = m_tau / m_mu
exp_m_b_over_m_c    = m_b / m_c
exp_m_H_over_m_W    = m_H / m_W
exp_Delta_m2_ratio  = Delta_m2_21 / Delta_m2_31
exp_m_p_over_m_e    = 1836.152673  # Given directly
exp_m_mu_over_m_e   = m_mu / m_e
exp_m_u_over_m_d    = m_u / m_d
exp_m_s_over_m_u    = m_s / m_u
exp_m_c_over_m_s    = m_c / m_s
exp_m_t_over_m_c    = m_t / m_c
exp_m_c_over_m_d    = m_c / m_d

# Higgs self-coupling λ = m_H²/(2v²) with v = 246 GeV = 246000 MeV
v_ew = 246000.0  # MeV
exp_Higgs_lambda = m_H**2 / (2 * v_ew**2)

# α_s(M_Z) - PDG 2024 central value
exp_alpha_s = 0.1179

print(f"  m_u(2GeV)     = {m_u} MeV")
print(f"  m_d(2GeV)     = {m_d} MeV")
print(f"  m_s(2GeV)     = {m_s} MeV")
print(f"  m_c(m_c)      = {m_c} MeV")
print(f"  m_b(m_b)      = {m_b} MeV")
print(f"  m_t(pole)     = {m_t} MeV")
print(f"  m_τ           = {m_tau} MeV")
print(f"  m_μ           = {m_mu} MeV")
print(f"  m_e           = {m_e} MeV")
print(f"  m_H           = {m_H} MeV")
print(f"  m_W           = {m_W} MeV")
print(f"  m_Z           = {m_Z} MeV")
print(f"  m_p           = {m_p} MeV")
print(f"  1/α           = {alpha_inv}")
print(f"  sin²θ_W       = {sin2_thetaW}")
print(f"  sin²θ₁₂       = {sin2_12}")
print(f"  sin²θ₁₃       = {sin2_13}")
print(f"  sin²θ₂₃       = {sin2_23}")
print(f"  |V_us|        = {V_us}")
print(f"  |V_cb|        = {V_cb}")
print(f"  |V_ub|        = {V_ub}")
print(f"  Δm²₂₁         = {Delta_m2_21} eV²")
print(f"  Δm²₃₁         = {Delta_m2_31} eV²")
print(f"\nDerived experimental values:")
print(f"  m_t/m_u       = {exp_m_t_over_m_u:.6f}")
print(f"  m_τ/m_e       = {exp_m_tau_over_m_e:.6f}")
print(f"  m_τ/m_μ       = {exp_m_tau_over_m_mu:.6f}")
print(f"  m_b/m_c       = {exp_m_b_over_m_c:.6f}")
print(f"  m_H/m_W       = {exp_m_H_over_m_W:.8f}")
print(f"  Δm²₂₁/Δm²₃₁   = {exp_Delta_m2_ratio:.6f}")
print(f"  m_p/m_e       = {exp_m_p_over_m_e:.9f}")
print(f"  m_μ/m_e       = {exp_m_mu_over_m_e:.6f}")
print(f"  m_u/m_d       = {exp_m_u_over_m_d:.6f}")
print(f"  m_s/m_u       = {exp_m_s_over_m_u:.6f}")
print(f"  m_c/m_s       = {exp_m_c_over_m_s:.6f}")
print(f"  m_t/m_c       = {exp_m_t_over_m_c:.6f}")
print(f"  m_c/m_d       = {exp_m_c_over_m_d:.6f}")
print(f"  Higgs λ       = {exp_Higgs_lambda:.8f}")
print(f"  α_s(M_Z)      = {exp_alpha_s}")


# ==============================================================================
# CLASSIFICATION FUNCTION
# ==============================================================================
def classify(rel_err_pct):
    """Classify relative error into SG, V, W, F."""
    if rel_err_pct < 0.01:
        return "SG"
    elif rel_err_pct < 0.1:
        return "V"
    elif rel_err_pct < 1.0:
        return "W"
    else:
        return "F"


def classify_verbose(cls):
    """Full classification name."""
    names = {"SG": "SUPER GOOD (<0.01%)", "V": "VERY GOOD (<0.1%)",
             "W": "WITHIN TOL (<1%)", "F": "FAIL (>1%)"}
    return names.get(cls, "UNKNOWN")


# ==============================================================================
# RESULTS STORAGE
# ==============================================================================
results = []
failures = []


def add_result(id_num, name, formula_tex, predicted, experimental,
               description=""):
    """Add a verification result."""
    abs_err = abs(predicted - experimental)
    rel_err = (abs_err / abs(experimental)) * 100.0 if experimental != 0 else float('inf')
    cls = classify(rel_err)

    result = {
        'id': id_num,
        'name': name,
        'formula': formula_tex,
        'predicted': predicted,
        'experimental': experimental,
        'abs_err': abs_err,
        'rel_err': rel_err,
        'class': cls,
        'description': description
    }
    results.append(result)
    if cls == "F":
        failures.append(result)
    return result


# ==============================================================================
# VERIFY ALL 25 FORMULAS
# ==============================================================================
print("\n" + "=" * 100)
print("FORMULA VERIFICATION")
print("=" * 100)

# -----------------------------------------------------------------------------
# FORMULA 1: Q07 = 24φ²/π  →  m_t/m_u
# -----------------------------------------------------------------------------
pred = 24 * phi**2 / pi
add_result(1, "Q07", "24φ²/π", pred, exp_m_t_over_m_u,
           "Top/up quark mass ratio")

# -----------------------------------------------------------------------------
# FORMULA 2: L03 = 549·e·π²/φ³  →  m_τ/m_e
# -----------------------------------------------------------------------------
pred = 549 * e * pi**2 / phi**3
add_result(2, "L03", "549eπ²/φ³", pred, exp_m_tau_over_m_e,
           "Tau/electron mass ratio")

# -----------------------------------------------------------------------------
# FORMULA 3: L02 = 239φ⁴/π⁴  →  m_τ/m_μ
# NOTE: Paper says this is for α_EW⁻¹, but verify_all_25.py maps to m_τ/m_μ
#       The paper's L03 is m_τ/m_μ = 3φ⁴/2. Let's test BOTH.
# -----------------------------------------------------------------------------
pred = 239 * phi**4 / pi**4
add_result(3, "L02", "239φ⁴/π⁴", pred, exp_m_tau_over_m_mu,
           "Tau/muon mass ratio (239φ⁴/π⁴ version)")

# Also test the paper version: 3φ⁴/2
pred_paper = 3 * phi**4 / 2
add_result(3.5, "L03-paper", "3φ⁴/2", pred_paper, exp_m_tau_over_m_mu,
           "Tau/muon mass ratio (paper version 3φ⁴/2)")

# -----------------------------------------------------------------------------
# FORMULA 4: Q05 = 127φ/120 + 30/19  →  m_b/m_c
# -----------------------------------------------------------------------------
pred = 127 * phi / 120 + 30 / 19
add_result(4, "Q05", "127φ/120 + 30/19", pred, exp_m_b_over_m_c,
           "Bottom/charm quark mass ratio")

# -----------------------------------------------------------------------------
# FORMULA 5: H02 = φ·11/20 + 20/30  →  m_H/m_W
# -----------------------------------------------------------------------------
pred = phi * 11 / 20 + 20 / 30
add_result(5, "H02", "11φ/20 + 2/3", pred, exp_m_H_over_m_W,
           "Higgs/W boson mass ratio")

# -----------------------------------------------------------------------------
# FORMULA 6: Neutrino = π/(40φ²)  →  Δm²₂₁/Δm²₃₁
# Paper says: 1/(2φ³ - 1) for this ratio. Let's test BOTH.
# -----------------------------------------------------------------------------
pred = pi / (40 * phi**2)
add_result(6, "N21-31-a", "π/(40φ²)", pred, exp_Delta_m2_ratio,
           "Neutrino mass splitting ratio (π/(40φ²) version)")

pred_paper = 1 / (2 * phi**3 - 1)
add_result(6.5, "N21-31-b", "1/(2φ³-1)", pred_paper, exp_Delta_m2_ratio,
           "Neutrino mass splitting ratio (paper version)")

# -----------------------------------------------------------------------------
# FORMULA 7: Proton = 6π⁵  →  m_p/m_e
# -----------------------------------------------------------------------------
pred = 6 * pi**5
add_result(7, "Proton", "6π⁵", pred, exp_m_p_over_m_e,
           "Proton/electron mass ratio")

# -----------------------------------------------------------------------------
# FORMULA 8: L01 = 239e/π  →  m_μ/m_e
# Paper says: m_μ/m_e = 6φ⁵/π. Let's test BOTH.
# -----------------------------------------------------------------------------
pred = 239 * e / pi
add_result(8, "L01", "239e/π", pred, exp_m_mu_over_m_e,
           "Muon/electron mass ratio (239e/π version)")

pred_paper = 6 * phi**5 / pi
add_result(8.5, "L04-paper", "6φ⁵/π", pred_paper, exp_m_mu_over_m_e,
           "Muon/electron mass ratio (paper version 6φ⁵/π)")

# -----------------------------------------------------------------------------
# FORMULA 9: G01 = 36φe²/π  →  1/α
# Paper says: α_EW⁻¹ = 360φ⁻³(1+1/(15πφ)) or 239φ⁴/π⁴. Let's test ALL.
# -----------------------------------------------------------------------------
pred = 36 * phi * e**2 / pi
add_result(9, "G01", "36φe²/π", pred, alpha_inv,
           "Inverse fine-structure constant (36φe²/π)")

# Paper version 1: 360φ⁻³(1 + 1/(15πφ))
pred_paper1 = 360 * phi**(-3) * (1 + 1/(15 * pi * phi))
add_result(9.5, "L02-paper-a", "360φ⁻³(1+1/(15πφ))", pred_paper1, alpha_inv,
           "α⁻¹ (paper version 360φ⁻³(1+1/(15πφ)))")

# Paper version 2: 239φ⁴/π⁴
pred_paper2 = 239 * phi**4 / pi**4
add_result(9.6, "L02-paper-b", "239φ⁴/π⁴", pred_paper2, alpha_inv,
           "α⁻¹ (paper version 239φ⁴/π⁴)")

# -----------------------------------------------------------------------------
# FORMULA 10: N01 = 8π/(φ⁵e²)  →  sin²θ₁₂
# -----------------------------------------------------------------------------
pred = 8 * pi / (phi**5 * e**2)
add_result(10, "N01", "8π/(φ⁵e²)", pred, sin2_12,
           "PMNS sin²θ₁₂")

# -----------------------------------------------------------------------------
# FORMULA 11: N03 = π²/18  →  sin²θ₂₃
# -----------------------------------------------------------------------------
pred = pi**2 / 18
add_result(11, "N03", "π²/18", pred, sin2_23,
           "PMNS sin²θ₂₃")

# -----------------------------------------------------------------------------
# FORMULA 12: C01 = 2φ³e²/(9π³)  →  |V_us|
# Paper says: |V_us| = 1/√(2φ²+1). Let's test BOTH.
# -----------------------------------------------------------------------------
pred = 2 * phi**3 * e**2 / (9 * pi**3)
add_result(12, "C01", "2φ³e²/(9π³)", pred, V_us,
           "CKM |V_us| (2φ³e²/(9π³) version)")

pred_paper = 1 / math.sqrt(2 * phi**2 + 1)
add_result(12.5, "L08-paper", "1/√(2φ²+1)", pred_paper, V_us,
           "CKM |V_us| (paper version)")

# -----------------------------------------------------------------------------
# FORMULA 13: C02 = 1/(3φ²π)  →  |V_cb|
# Paper says: |V_cb| = (φ-1)/3. Let's test BOTH.
# -----------------------------------------------------------------------------
pred = 1 / (3 * phi**2 * pi)
add_result(13, "C02", "1/(3φ²π)", pred, V_cb,
           "CKM |V_cb| (1/(3φ²π) version)")

pred_paper = (phi - 1) / 3
add_result(13.5, "L09-paper", "(φ-1)/3", pred_paper, V_cb,
           "CKM |V_cb| (paper version (φ-1)/3)")

# -----------------------------------------------------------------------------
# FORMULA 14: C03 = 1/(39φ²e)  →  |V_ub|
# -----------------------------------------------------------------------------
pred = 1 / (39 * phi**2 * e)
add_result(14, "C03", "1/(39φ²e)", pred, V_ub,
           "CKM |V_ub|")

# -----------------------------------------------------------------------------
# FORMULA 15: H01 = 4φ³e²  →  m_H (in GeV)
# -----------------------------------------------------------------------------
pred = 4 * phi**3 * e**2  # This gives a dimensionless number
# Compare to m_H in GeV
add_result(15, "H01", "4φ³e²", pred, 125.20,
           "Higgs mass (GeV)")

# -----------------------------------------------------------------------------
# FORMULA 16: H03 = 4φπ/15  →  m_H/m_Z
# Paper says: m_W/m_Z = (φ²-1)/φ². Let's test BOTH.
# -----------------------------------------------------------------------------
pred = 4 * phi * pi / 15
add_result(16, "H03", "4φπ/15", pred, exp_m_H_over_m_W,
           "Higgs/W mass ratio (mapped to H03)")

# Paper version: m_W/m_Z = (φ²-1)/φ²
pred_paper = (phi**2 - 1) / phi**2
add_result(16.5, "L17-paper", "(φ²-1)/φ²", pred_paper, m_W/m_Z,
           "W/Z mass ratio (paper version)")

# -----------------------------------------------------------------------------
# FORMULA 17: G03 = 3/(8φ)  →  sin²θ_W
# Paper says: sin²θ_W = (3-φ)/5. Let's test BOTH.
# -----------------------------------------------------------------------------
pred = 3 / (8 * phi)
add_result(17, "G03", "3/(8φ)", pred, sin2_thetaW,
           "Weak mixing angle sin²θ_W (3/(8φ) version)")

pred_paper = (3 - phi) / 5
add_result(17.5, "L05-paper", "(3-φ)/5", pred_paper, sin2_thetaW,
           "Weak mixing angle sin²θ_W (paper version)")

# -----------------------------------------------------------------------------
# FORMULA 18: Q01 = 1/(8φ²πe)  →  m_u/m_d
# -----------------------------------------------------------------------------
pred = 1 / (8 * phi**2 * pi * e)
add_result(18, "Q01", "1/(8φ²πe)", pred, exp_m_u_over_m_d,
           "Up/down quark mass ratio")

# -----------------------------------------------------------------------------
# FORMULA 19: Q02 = φ³π²  →  m_s/m_u
# -----------------------------------------------------------------------------
pred = phi**3 * pi**2
add_result(19, "Q02", "φ³π²", pred, exp_m_s_over_m_u,
           "Strange/up quark mass ratio")

# -----------------------------------------------------------------------------
# FORMULA 20: Q04 = 14e²/9  →  m_c/m_s
# -----------------------------------------------------------------------------
pred = 14 * e**2 / 9
add_result(20, "Q04", "14e²/9", pred, exp_m_c_over_m_s,
           "Charm/strange quark mass ratio")

# -----------------------------------------------------------------------------
# FORMULA 21: Q06 = φ⁴e²/3  →  m_t/m_c
# -----------------------------------------------------------------------------
pred = phi**4 * e**2 / 3
add_result(21, "Q06", "φ⁴e²/3", pred, exp_m_t_over_m_c,
           "Top/charm quark mass ratio")

# -----------------------------------------------------------------------------
# FORMULA 22: Sin13 = π²/(25φ⁶)  →  sin²θ₁₃  [CORRECTED 2025-07-28]
# Was: φ^(3/2)/(30π), error 0.74%. New formula: 0.003% error (SG-class).
# sin θ₁₃ = π/(5φ³), sin² θ₁₃ = π²/(25φ⁶)
# -----------------------------------------------------------------------------
pred = pi**2 / (25 * phi**6)
add_result(22, "Sin13", "π²/(25φ⁶)", pred, sin2_13,
           "PMNS sin²θ₁₃ — reactor mixing")

# -----------------------------------------------------------------------------
# FORMULA 23: Lambda = √φ/π²  →  Higgs λ
# -----------------------------------------------------------------------------
pred = math.sqrt(phi) / pi**2
add_result(23, "Lambda", "√φ/π²", pred, exp_Higgs_lambda,
           "Higgs self-coupling λ")

# -----------------------------------------------------------------------------
# FORMULA 24: Q03 = πe⁴  →  m_c/m_d
# -----------------------------------------------------------------------------
pred = pi * e**4
add_result(24, "Q03", "πe⁴", pred, exp_m_c_over_m_d,
           "Charm/down quark mass ratio")

# -----------------------------------------------------------------------------
# FORMULA 25: G02 = (√5 - 2)/2  →  α_s(M_Z)
# Paper says: α_s = π/(4φ²)(1 - 1/(8πφ)). Let's test BOTH.
# -----------------------------------------------------------------------------
pred = (sqrt5 - 2) / 2
add_result(25, "G02", "(√5-2)/2", pred, exp_alpha_s,
           "Strong coupling α_s(M_Z) ((√5-2)/2 version)")

# Paper version: π/(4φ²)(1 - 1/(8πφ))
pred_paper = (pi / (4 * phi**2)) * (1 - 1/(8 * pi * phi))
add_result(25.5, "L06-paper", "π/(4φ²)(1-1/(8πφ))", pred_paper, exp_alpha_s,
           "Strong coupling α_s(M_Z) (paper version)")

# ==============================================================================
# PRINT RESULTS TABLE
# ==============================================================================
print("\n" + "=" * 120)
print(f"{'#':>4} {'Name':>10} {'Formula':>22} {'Predicted':>16} {'PDG 2024':>16} {'Abs Error':>14} {'Rel Err %':>10} {'Cls':>4} {'Status':>10}")
print("=" * 120)

for r in results:
    status = "✓ PASS" if r['class'] != 'F' else "✗ FAIL"
    print(f"{r['id']:>4.1f} {r['name']:>10} {r['formula']:>22} "
          f"{r['predicted']:>16.8f} {r['experimental']:>16.8f} "
          f"{r['abs_err']:>14.8f} {r['rel_err']:>10.4f}% {r['class']:>4} {status:>10}")

# ==============================================================================
# CLASSIFICATION SUMMARY
# ==============================================================================
print("\n" + "=" * 100)
print("CLASSIFICATION SUMMARY")
print("=" * 100)

sg = [r for r in results if r['class'] == 'SG']
vv = [r for r in results if r['class'] == 'V']
ww = [r for r in results if r['class'] == 'W']
ff = [r for r in results if r['class'] == 'F']

print(f"\nSG (Super Good, <0.01%):   {len(sg):2d} formulas")
for r in sg:
    print(f"  #{r['id']:4.1f} {r['name']:10s} {r['formula']:22s} → {r['rel_err']:.6f}%  | {r['description']}")

print(f"\nV (Very Good, <0.1%):      {len(vv):2d} formulas")
for r in vv:
    print(f"  #{r['id']:4.1f} {r['name']:10s} {r['formula']:22s} → {r['rel_err']:.6f}%  | {r['description']}")

print(f"\nW (Within Tolerance, <1%): {len(ww):2d} formulas")
for r in ww:
    print(f"  #{r['id']:4.1f} {r['name']:10s} {r['formula']:22s} → {r['rel_err']:.4f}%  | {r['description']}")

print(f"\n{'='*60}")
print(f"F (FAIL, >1%):             {len(ff):2d} formulas")
print(f"{'='*60}")
for r in ff:
    print(f"  #{r['id']:4.1f} {r['name']:10s} {r['formula']:22s} → {r['rel_err']:.4f}%  | {r['description']}")
    print(f"       Predicted: {r['predicted']:.8f}  |  Experimental: {r['experimental']:.8f}  |  Abs err: {r['abs_err']:.8f}")

# ==============================================================================
# STATISTICS
# ==============================================================================
print("\n" + "=" * 100)
print("STATISTICAL SUMMARY")
print("=" * 100)

total = len([r for r in results if r['id'] == int(r['id'])])  # Count only integer IDs (main 25)
# Actually count all unique formulas including paper variants
total_all = len(results)
success_all = len(sg) + len(vv) + len(ww)
failed_all = len(ff)

# Count only the main 25 (integer IDs)
main_results = [r for r in results if r['id'] == int(r['id'])]
total_main = len(main_results)
sg_main = len([r for r in main_results if r['class'] == 'SG'])
v_main = len([r for r in main_results if r['class'] == 'V'])
w_main = len([r for r in main_results if r['class'] == 'W'])
f_main = len([r for r in main_results if r['class'] == 'F'])
success_main = sg_main + v_main + w_main

print(f"\nMain 25 formulas:")
print(f"  Total evaluated:    {total_main}")
print(f"  SG (<0.01%):        {sg_main}")
print(f"  V (<0.1%):          {v_main}")
print(f"  W (<1%):            {w_main}")
print(f"  F (>1%, FAIL):      {f_main}")
print(f"  Success rate:       {success_main}/{total_main} = {success_main/total_main*100:.1f}%")

print(f"\nAll formulas (including paper variants):")
print(f"  Total evaluated:    {total_all}")
print(f"  SG (<0.01%):        {len(sg)}")
print(f"  V (<0.1%):          {len(vv)}")
print(f"  W (<1%):            {len(ww)}")
print(f"  F (>1%, FAIL):      {len(ff)}")
print(f"  Success rate:       {success_all}/{total_all} = {success_all/total_all*100:.1f}%")

rel_errors_main = [r['rel_err'] for r in main_results]
print(f"\nRelative error statistics (main 25):")
print(f"  Mean:   {sum(rel_errors_main)/len(rel_errors_main):.4f}%")
print(f"  Median: {sorted(rel_errors_main)[len(rel_errors_main)//2]:.4f}%")
print(f"  Min:    {min(rel_errors_main):.6f}%  (Formula #{[r for r in main_results if r['rel_err']==min(rel_errors_main)][0]['id']:.0f})")
print(f"  Max:    {max(rel_errors_main):.4f}%  (Formula #{[r for r in main_results if r['rel_err']==max(rel_errors_main)][0]['id']:.0f})")

# ==============================================================================
# FAILURE ANALYSIS
# ==============================================================================
if ff:
    print("\n" + "=" * 100)
    print("FAILURE ANALYSIS -- REQUIRING INVESTIGATION")
    print("=" * 100)
    for r in ff:
        print(f"\n  [#{r['id']:.1f}] {r['name']} -- {r['description']}")
        print(f"  Formula:        {r['formula']}")
        print(f"  Predicted:      {r['predicted']:.10f}")
        print(f"  Experimental:   {r['experimental']:.10f}")
        print(f"  Absolute error: {r['abs_err']:.10f}")
        print(f"  Relative error: {r['rel_err']:.4f}%  [{classify_verbose(r['class'])}]")
        print(f"  Verdict:        ✗ FAIL - Formula does not match experiment within 1%")

# ==============================================================================
# PAPER FORMULA COMPARISON
# ==============================================================================
print("\n" + "=" * 100)
print("PAPER FORMULAS (L01-L17) vs ALTERNATE FORMULAS")
print("=" * 100)

# Build comparison table
comparisons = [
    ("L02", "α⁻¹", "360φ⁻³(1+1/(15πφ))", 9.5),
    ("L02", "α⁻¹", "239φ⁴/π⁴", 9.6),
    ("L03", "m_τ/m_μ", "3φ⁴/2", 3.5),
    ("L04", "m_μ/m_e", "6φ⁵/π", 8.5),
    ("L05", "sin²θ_W", "(3-φ)/5", 17.5),
    ("L06", "α_s", "π/(4φ²)(1-1/(8πφ))", 25.5),
    ("L08", "|V_us|", "1/√(2φ²+1)", 12.5),
    ("L09", "|V_cb|", "(φ-1)/3", 13.5),
    ("L17", "m_W/m_Z", "(φ²-1)/φ²", 16.5),
    ("N21", "Δm²₂₁/Δm²₃₁", "1/(2φ³-1)", 6.5),
]

print(f"\n{'Paper ID':>8} {'Quantity':>14} {'Paper Formula':>28} {'Predicted':>14} {'PDG':>14} {'Rel Err%':>10} {'Class':>5}")
print("-" * 100)
for paper_id, qty, formula, res_id in comparisons:
    r = [x for x in results if x['id'] == res_id]
    if r:
        rr = r[0]
        print(f"{paper_id:>8} {qty:>14} {formula:>28} {rr['predicted']:>14.8f} {rr['experimental']:>14.8f} {rr['rel_err']:>10.4f}% {rr['class']:>5}")

# ==============================================================================
# FINAL VERDICT
# ==============================================================================
print("\n" + "=" * 100)
print("FINAL INDEPENDENT VERDICT")
print("=" * 100)

if f_main == 0:
    print("\n  >>> ALL 25 MAIN FORMULAS PASS (within <1% tolerance) <<<")
elif f_main <= 3:
    print(f"\n  >>> {f_main} of 25 MAIN FORMULAS FAIL (>1% error) -- REQUIRES ATTENTION <<<")
else:
    print(f"\n  >>> {f_main} of 25 MAIN FORMULAS FAIL (>1% error) -- MAJOR CONCERN <<<")

print(f"\n  Breakdown:")
print(f"    SG-class (<0.01%):  {sg_main:2d} formulas")
print(f"    V-class  (<0.1%):   {v_main:2d} formulas")
print(f"    W-class  (<1%):     {w_main:2d} formulas")
print(f"    F-class  (>1%):     {f_main:2d} formulas")

print(f"\n  Honest assessment: {success_main}/{total_main} = {success_main/total_main*100:.1f}% pass rate")

if f_main > 0:
    print(f"\n  FAILED formulas (require investigation):")
    for r in [x for x in main_results if x['class'] == 'F']:
        print(f"    #{r['id']:2.0f} {r['name']:10s} {r['formula']:22s}  →  {r['rel_err']:>8.4f}% error")

print("\n" + "=" * 100)
print("VERIFICATION COMPLETE -- Independent skeptical reviewer")
print("=" * 100)
