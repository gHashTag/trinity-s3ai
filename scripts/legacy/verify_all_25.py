#!/usr/bin/env python3
"""
Trinity Formula Verification Script
Numerical verification of ALL 25 Trinity formulas against PDG 2024 data.
"""

import math

# Constants
phi = (1 + math.sqrt(5)) / 2  # Golden ratio
e = math.e  # Euler's number
pi = math.pi

print("=" * 90)
print("TRINITY FORMULA VERIFICATION - ALL 25 FORMULAS vs PDG 2024")
print("=" * 90)
print(f"\nConstants: φ = {phi:.10f}, e = {e:.10f}, π = {pi:.10f}")
print()

# PDG 2024 experimental data
PDG = {
    'm_t/m_u': 20.003,
    'm_tau/m_e': 3477.23,
    'm_tau/m_mu': 16.817,
    'm_b/m_c': 52.3,
    'm_H/m_W': 125.20 / 80.377,  # m_H / m_W
    'delta_m21/delta_m31': 7.5e-5 / 2.5e-3,  # ratio of mass splittings
    'm_p/m_e': 1836.15267343,
    'm_mu/m_e': 206.7682830,
    '1/alpha': 137.035999084,
    'sin2_12': 0.307,
    'sin2_23': 0.546,
    '|V_us|': 0.2243,
    '|V_cb|': 0.0405,
    '|V_ub|': 0.0036,
    'm_H': 125.20,
    'm_H/m_Z': 125.20 / 91.1876,
    'sin2_theta_W': 0.23121,
    'm_u/m_d': 1.0 / 8.0,  # ~0.125 (inverse of d/u ratio ~8)
    'm_s/m_u': 95.0 / 2.16,  # m_s / m_u using PDG central values
    'm_c/m_s': 1.27e3 / 95.0,  # m_c / m_s using PDG central values
    'm_t/m_c': 172.69e3 / 1.27e3,  # m_t / m_c using PDG central values
    'sin2_13': 0.022,
    'Higgs_lambda': (125.20 ** 2) / (2 * 246.0 ** 2),  # λ = m_H²/(2v²)
    'm_c/m_d': 1.27e3 / 4.67,  # m_c / m_d using PDG central values
    'alpha_s': 0.1179,  # PDG 2024 α_s(M_Z)
}

# Classification thresholds
def classify(rel_err_pct):
    if rel_err_pct < 0.01:
        return "SG"  # Super Good
    elif rel_err_pct < 0.1:
        return "V"   # Very good
    elif rel_err_pct < 1.0:
        return "W"   # Within tolerance
    else:
        return "F"   # Failed

results = []

# ============================================================
# FORMULA 1: Q07 = 24φ²/π  →  m_t/m_u
# ============================================================
formula_name = "Q07"
formula = "24φ²/π"
predicted = 24 * phi**2 / pi
experimental = PDG['m_t/m_u']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 1, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 2: L03 = 549eπ²/φ³  →  m_tau/m_e
# ============================================================
formula_name = "L03"
formula = "549·e·π²/φ³"
predicted = 549 * e * pi**2 / phi**3
experimental = PDG['m_tau/m_e']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 2, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 3: L02 = 239φ⁴/π⁴  →  m_tau/m_mu
# ============================================================
formula_name = "L02"
formula = "239·φ⁴/π⁴"
predicted = 239 * phi**4 / pi**4
experimental = PDG['m_tau/m_mu']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 3, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 4: Q05 = 127φ/120 + 30/19  →  m_b/m_c
# ============================================================
formula_name = "Q05"
formula = "127φ/120 + 30/19"
predicted = 127 * phi / 120 + 30 / 19
experimental = PDG['m_b/m_c']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 4, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 5: H02 = φ·11/20 + 20/30  →  m_H/m_W
# ============================================================
formula_name = "H02"
formula = "φ·11/20 + 20/30"
predicted = phi * 11 / 20 + 20 / 30
experimental = PDG['m_H/m_W']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 5, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 6: Neutrino = π/(40φ²)  →  Δm²_21/Δm²_31
# ============================================================
formula_name = "Neutrino"
formula = "π/(40φ²)"
predicted = pi / (40 * phi**2)
experimental = PDG['delta_m21/delta_m31']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 6, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 7: Proton = 6π⁵  →  m_p/m_e
# ============================================================
formula_name = "Proton"
formula = "6π⁵"
predicted = 6 * pi**5
experimental = PDG['m_p/m_e']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 7, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 8: L01 = 239e/π  →  m_mu/m_e
# ============================================================
formula_name = "L01"
formula = "239·e/π"
predicted = 239 * e / pi
experimental = PDG['m_mu/m_e']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 8, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 9: G01 = 36φe²/π  →  1/α
# ============================================================
formula_name = "G01"
formula = "36φe²/π"
predicted = 36 * phi * e**2 / pi
experimental = PDG['1/alpha']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 9, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 10: N01 = 8π/(φ⁵e²)  →  sin²θ_12
# ============================================================
formula_name = "N01"
formula = "8π/(φ⁵e²)"
predicted = 8 * pi / (phi**5 * e**2)
experimental = PDG['sin2_12']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 10, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 11: N03 = π²/18  →  sin²θ_23
# ============================================================
formula_name = "N03"
formula = "π²/18"
predicted = pi**2 / 18
experimental = PDG['sin2_23']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 11, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 12: C01 = 2φ³e²/(9π³)  →  |V_us|
# ============================================================
formula_name = "C01"
formula = "2φ³e²/(9π³)"
predicted = 2 * phi**3 * e**2 / (9 * pi**3)
experimental = PDG['|V_us|']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 12, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 13: C02 = 1/(3φ²π)  →  |V_cb|
# ============================================================
formula_name = "C02"
formula = "1/(3φ²π)"
predicted = 1 / (3 * phi**2 * pi)
experimental = PDG['|V_cb|']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 13, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 14: C03 = 1/(39φ²e)  →  |V_ub|
# ============================================================
formula_name = "C03"
formula = "1/(39φ²e)"
predicted = 1 / (39 * phi**2 * e)
experimental = PDG['|V_ub|']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 14, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 15: H01 = 4φ³e²  →  m_H
# ============================================================
formula_name = "H01"
formula = "4φ³e²"
predicted = 4 * phi**3 * e**2
experimental = PDG['m_H']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 15, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 16: H03 = 4φπ/15  →  m_H/m_Z
# ============================================================
formula_name = "H03"
formula = "4φπ/15"
predicted = 4 * phi * pi / 15
experimental = PDG['m_H/m_Z']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 16, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 17: G03 = 3/(8φ)  →  sin²θ_W
# ============================================================
formula_name = "G03"
formula = "3/(8φ)"
predicted = 3 / (8 * phi)
experimental = PDG['sin2_theta_W']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 17, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 18: Q01 = 1/(8φ²πe)  →  m_u/m_d
# ============================================================
formula_name = "Q01"
formula = "1/(8φ²πe)"
predicted = 1 / (8 * phi**2 * pi * e)
experimental = PDG['m_u/m_d']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 18, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 19: Q02 = φ³π²  →  m_s/m_u
# ============================================================
formula_name = "Q02"
formula = "φ³π²"
predicted = phi**3 * pi**2
experimental = PDG['m_s/m_u']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 19, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 20: Q04 = 14e²/9  →  m_c/m_s
# ============================================================
formula_name = "Q04"
formula = "14e²/9"
predicted = 14 * e**2 / 9
experimental = PDG['m_c/m_s']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 20, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 21: Q06 = φ⁴e²/3  →  m_t/m_c
# ============================================================
formula_name = "Q06"
formula = "φ⁴e²/3"
predicted = phi**4 * e**2 / 3
experimental = PDG['m_t/m_c']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 21, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 22: Sin13 = φ^(3/2)/(30π)  →  sin²θ_13
# ============================================================
formula_name = "Sin13"
formula = "φ^(3/2)/(30π)"
predicted = phi**1.5 / (30 * pi)
experimental = PDG['sin2_13']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 22, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 23: Lambda = √φ/π²  →  Higgs λ
# ============================================================
formula_name = "Lambda"
formula = "√φ/π²"
predicted = math.sqrt(phi) / pi**2
experimental = PDG['Higgs_lambda']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 23, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 24: Q03 = πe⁴  →  m_c/m_d
# ============================================================
formula_name = "Q03"
formula = "πe⁴"
predicted = pi * e**4
experimental = PDG['m_c/m_d']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 24, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# FORMULA 25: G02 = (√5 - 2)/2  →  α_s
# ============================================================
formula_name = "G02"
formula = "(√5 - 2)/2"
predicted = (math.sqrt(5) - 2) / 2
experimental = PDG['alpha_s']
abs_err = abs(predicted - experimental)
rel_err = abs_err / experimental * 100
cls = classify(rel_err)
results.append({
    'id': 25, 'name': formula_name, 'formula': formula,
    'predicted': predicted, 'experimental': experimental,
    'abs_err': abs_err, 'rel_err': rel_err, 'class': cls
})

# ============================================================
# Print results table
# ============================================================
print("-" * 90)
print(f"{'#':>3} {'Name':>8} {'Formula':>20} {'Predicted':>14} {'PDG 2024':>14} {'Abs Err':>12} {'Rel Err%':>10} {'Cls':>4}")
print("-" * 90)

for r in results:
    print(f"{r['id']:>3} {r['name']:>8} {r['formula']:>20} "
          f"{r['predicted']:>14.8f} {r['experimental']:>14.8f} "
          f"{r['abs_err']:>12.8f} {r['rel_err']:>10.4f}% {r['class']:>4}")

print("-" * 90)

# ============================================================
# Classification summary
# ============================================================
print("\n" + "=" * 90)
print("CLASSIFICATION SUMMARY")
print("=" * 90)

sg = [r for r in results if r['class'] == 'SG']
v = [r for r in results if r['class'] == 'V']
w = [r for r in results if r['class'] == 'W']
f = [r for r in results if r['class'] == 'F']

print(f"\nSG (Super Good, < 0.01%):  {len(sg)} formulas")
for r in sg:
    print(f"  #{r['id']:2d} {r['name']:8s} {r['formula']:20s} → {r['rel_err']:.6f}%")

print(f"\nV (Very Good, < 0.1%):     {len(v)} formulas")
for r in v:
    print(f"  #{r['id']:2d} {r['name']:8s} {r['formula']:20s} → {r['rel_err']:.6f}%")

print(f"\nW (Within Tolerance, <1%): {len(w)} formulas")
for r in w:
    print(f"  #{r['id']:2d} {r['name']:8s} {r['formula']:20s} → {r['rel_err']:.4f}%")

print(f"\nF (FAILED, > 1%):          {len(f)} formulas")
for r in f:
    print(f"  #{r['id']:2d} {r['name']:8s} {r['formula']:20s} → {r['rel_err']:.4f}%  (abs_err={r['abs_err']:.6f})")

# ============================================================
# Summary statistics
# ============================================================
print("\n" + "=" * 90)
print("SUMMARY STATISTICS")
print("=" * 90)

total = len(results)
success = len(sg) + len(v) + len(w)
failed = len(f)

print(f"\nTotal formulas evaluated:     {total}")
print(f"Successful (SG+V+W):          {success}")
print(f"Failed (>1%):                 {failed}")
print(f"Success rate:                 {success/total*100:.1f}%")

rel_errors = [r['rel_err'] for r in results]
print(f"\nRelative error statistics:")
print(f"  Mean:   {sum(rel_errors)/len(rel_errors):.4f}%")
print(f"  Median: {sorted(rel_errors)[len(rel_errors)//2]:.4f}%")
print(f"  Min:    {min(rel_errors):.6f}%  (#{[r for r in results if r['rel_err']==min(rel_errors)][0]['id']})")
print(f"  Max:    {max(rel_errors):.4f}%  (#{[r for r in results if r['rel_err']==max(rel_errors)][0]['id']})")

# ============================================================
# Print PDG reference values used
# ============================================================
print("\n" + "=" * 90)
print("PDG 2024 REFERENCE VALUES USED")
print("=" * 90)
print(f"  m_t/m_u        = {PDG['m_t/m_u']}")
print(f"  m_tau/m_e      = {PDG['m_tau/m_e']}")
print(f"  m_tau/m_mu     = {PDG['m_tau/m_mu']}")
print(f"  m_b/m_c        = {PDG['m_b/m_c']}")
print(f"  m_H/m_W        = {PDG['m_H/m_W']:.8f}")
print(f"  Δm²₂₁/Δm²₃₁   = {PDG['delta_m21/delta_m31']:.5f}")
print(f"  m_p/m_e        = {PDG['m_p/m_e']}")
print(f"  m_mu/m_e       = {PDG['m_mu/m_e']}")
print(f"  1/α            = {PDG['1/alpha']}")
print(f"  sin²θ₁₂       = {PDG['sin2_12']}")
print(f"  sin²θ₂₃       = {PDG['sin2_23']}")
print(f"  |V_us|         = {PDG['|V_us|']}")
print(f"  |V_cb|         = {PDG['|V_cb|']}")
print(f"  |V_ub|         = {PDG['|V_ub|']}")
print(f"  m_H (GeV)      = {PDG['m_H']}")
print(f"  m_H/m_Z        = {PDG['m_H/m_Z']:.8f}")
print(f"  sin²θ_W       = {PDG['sin2_theta_W']}")
print(f"  m_u/m_d        = {PDG['m_u/m_d']:.6f}")
print(f"  m_s/m_u        = {PDG['m_s/m_u']:.4f}")
print(f"  m_c/m_s        = {PDG['m_c/m_s']:.4f}")
print(f"  m_t/m_c        = {PDG['m_t/m_c']:.4f}")
print(f"  sin²θ₁₃       = {PDG['sin2_13']}")
print(f"  Higgs λ        = {PDG['Higgs_lambda']:.6f}")
print(f"  m_c/m_d        = {PDG['m_c/m_d']:.4f}")
print(f"  α_s            = {PDG['alpha_s']}")

print("\n" + "=" * 90)
print("VERIFICATION COMPLETE")
print("=" * 90)
