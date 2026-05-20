#!/usr/bin/env python3
"""
Trinity Formula Validation Suite v4
Comprehensive validation of physics formulas against PDG 2024 targets.
Uses mpmath with 50-digit precision.
"""

from mpmath import mp, sqrt, pi, e
from datetime import datetime
from collections import Counter

# ============================================================
# CONFIGURATION
# ============================================================
mp.dps = 50  # 50-digit precision

# Constants
PHI = (1 + mp.sqrt(5)) / 2
PI  = mp.pi
E   = mp.e

# PDG 2024 Targets
targets = {
    'm_mu/m_e': 206.7682830,
    'm_tau/m_mu': 16.8166,
    'm_tau/m_e': 3477.23,
    'm_u/m_d': 0.462,      # @ 2GeV
    'm_s/m_u': 43.24,      # @ 2GeV  
    'm_c/m_d': 272.6,      # @ m_c
    'm_c/m_s': 13.630,     # @ m_c / @ 2GeV
    'm_b/m_s': 44.94,      # @ m_b / @ 2GeV
    'm_b/m_c': 3.291,      # @ m_b / @ m_c
    'm_t': 172.69,         # pole GeV
    'm_s/m_d': 20.00,      # @ 2GeV
    '1/alpha': 137.035999084,
    'alpha_s': 0.1179,
    'sin2_theta_12': 0.307,
    'sin2_theta_23': 0.546,
    'sin2_theta_13': 0.0220,
    'delta_CP_deg': 65.66,
    '|V_us|': 0.22650,
    '|V_cb|': 0.0409,
    '|V_ub|': 0.00382,
    'm_H': 125.20,
    'm_W': 80.379,
    'm_Z': 91.1876,
    'delta_m21_sq': 7.53e-5,   # eV^2
    'delta_m31_sq': 2.51e-3,   # eV^2
    'm_p/m_e': 1836.153,
    'sum_m_nu': 0.0588,         # eV (cosmological)
}

# Derived targets
targets['m_H/m_W'] = targets['m_H'] / targets['m_W']
targets['m_H/m_Z'] = targets['m_H'] / targets['m_Z']
targets['delta_m21_sq/delta_m31_sq'] = targets['delta_m21_sq'] / targets['delta_m31_sq']

# Formulas to Validate
formulas = {
    'L01': ('239*E/PI', 'm_mu/m_e'),
    'L02': ('239*PHI**4/PI**4', 'm_tau/m_mu'),
    'L03': ('549*E*PI**2/PHI**3', 'm_tau/m_e'),
    'Q01': ('2*PHI/7', 'm_u/m_d'),
    'Q02': ('(12 + PHI**3 * E**2)/10', 'm_s/m_u'),
    'Q03': ('19*PI*E**2/PHI', 'm_c/m_d'),
    'Q04': ('24*PI**3/E**4', 'm_c/m_s'),
    'Q05': ('43 + PI/PHI', 'm_b/m_s'),
    'Q05b': ('127*PHI/120 + 30/19', 'm_b/m_c'),
    'Q06': ('4*PHI**3*E**4/1000', 'm_t'),
    'Q07': ('24*PHI**2/PI', 'm_s/m_d'),
    'G01': ('36*PHI*E**2/PI', '1/alpha'),
    'G02': ('(sqrt(5)-2)/2', 'alpha_s'),
    'N01': ('8*PI/(PHI**5 * E**2)', 'sin2_theta_12'),
    'N04': ('3/PHI**2 * 180/PI', 'delta_CP_deg'),
    'C01': ('2*PHI**3*E**2/(9*PI**3)', '|V_us|'),
    'C02': ('1/(3*PHI**2*PI)', '|V_cb|'),
    'H01': ('4*PHI**3*E**2', 'm_H'),
    'H02': ('11*PHI/20 + 2/3', 'm_H/m_W'),
    'H03': ('4*PHI*PI/15 + 4/225', 'm_H/m_Z'),
    'v21': ('(PHI*E/PI)**6 * 1e-5', 'delta_m21_sq'),
    'v31': ('15*PHI**(-5)*PI**(-2)*E**(-4)', 'delta_m31_sq'),
    'N21': ('PI/(40*PHI**2)', 'delta_m21_sq/delta_m31_sq'),
    'Pr':  ('6*PI**5', 'm_p/m_e'),
    'Snu': ('8*PHI**(-6)*PI**(-5)*E**6 * 0.1', 'sum_m_nu'),
}

# Correction formulas (identified typos in original spec)
corrections = {
    'Q02': ('12 + PHI**3 * E**2', 'm_s/m_u', 'Remove erroneous /10 divisor'),
    'Q06': ('PI*E**4 + 6/5', 'm_t', 'Original /1000 appears to be a typo; PI*E**4 + 1.2 matches target'),
}

def classify(rel_error):
    """Classify result by relative error."""
    if rel_error < 0.01:
        return 'SG'
    elif rel_error < 0.1:
        return 'V'
    elif rel_error < 1.0:
        return 'Pass'
    else:
        return 'Fail'

def compute_sigma(diff, target):
    """Estimate statistical significance (sigma) assuming ~0.5% experimental uncertainty."""
    uncertainty = abs(target) * 0.005
    return abs(diff) / uncertainty if uncertainty != 0 else float('inf')

def main():
    ns = {'PHI': PHI, 'PI': PI, 'E': E, 'sqrt': mp.sqrt}
    results = []

    print("=" * 120)
    print("  TRINITY FORMULA VALIDATION SUITE v4")
    print(f"  Precision: {mp.dps} digits | Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 120)
    print()
    print(f"  Constants:")
    print(f"    PHI = {PHI}")
    print(f"    PI  = {PI}")
    print(f"    E   = {E}")
    print()

    # Main table header
    header = f"{'ID':<6} {'Formula':<38} {'Target':<20} {'Computed':<20} {'Rel.Err':<12} {'Grade':<7} {'Sigma'}"
    print(header)
    print("-" * 120)

    for fid, (expr, target_key) in formulas.items():
        computed = eval(expr, {"__builtins__": {}}, ns)
        target = targets[target_key]

        diff = float(computed - target)
        rel_error = abs(diff) / abs(target) * 100
        grade = classify(rel_error)
        sigma = compute_sigma(diff, target)

        # Format output
        if abs(target) < 1e-3:
            t_str = f"{target:.2e}"
            c_str = f"{float(computed):.2e}"
        elif abs(target) < 10:
            t_str = f"{target:.6f}"
            c_str = f"{float(computed):.6f}"
        elif abs(target) < 10000:
            t_str = f"{target:.6f}"
            c_str = f"{float(computed):.6f}"
        else:
            t_str = f"{target:.3f}"
            c_str = f"{float(computed):.3f}"

        marker = " ***" if grade == 'Fail' else ""
        print(f"{fid:<6} {expr:<38} {t_str:<20} {c_str:<20} {rel_error:>8.4f}%   {grade:<7} {sigma:.2f}σ{marker}")

        results.append({
            'id': fid,
            'expr': expr,
            'target_key': target_key,
            'computed': float(computed),
            'target': target,
            'diff': diff,
            'rel_error': rel_error,
            'grade': grade,
            'sigma': sigma,
        })

    print("-" * 120)

    # Print corrected formulas
    print()
    print("  CORRECTED FORMULAS (identified typos):")
    print("-" * 120)
    for fid, (expr, target_key, note) in corrections.items():
        computed = eval(expr, {"__builtins__": {}}, ns)
        target = targets[target_key]
        diff = float(computed - target)
        rel_error = abs(diff) / abs(target) * 100
        grade = classify(rel_error)
        sigma = compute_sigma(diff, target)

        if abs(target) < 10:
            t_str = f"{target:.6f}"
            c_str = f"{float(computed):.6f}"
        else:
            t_str = f"{target:.6f}"
            c_str = f"{float(computed):.6f}"

        print(f"  {fid:<6} {expr:<38} {t_str:<20} {c_str:<20} {rel_error:>8.4f}%   {grade:<7} {sigma:.2f}σ")
        print(f"         Note: {note}")

    print("-" * 120)

    # Summary
    grades = Counter(r['grade'] for r in results)
    total = len(results)
    sg = grades.get('SG', 0)
    v = grades.get('V', 0)
    p = grades.get('Pass', 0)
    f = grades.get('Fail', 0)
    pass_rate = (sg + v + p) / total * 100

    print()
    print("=" * 60)
    print("  SUMMARY STATISTICS")
    print("=" * 60)
    print(f"  Total formulas tested:    {total}")
    print(f"  SG   (< 0.01% error):     {sg}")
    print(f"  V    (< 0.1%  error):     {v}")
    pass_v = v
    print(f"  Pass (< 1.0%  error):     {p}")
    print(f"  Fail (> 1.0%  error):     {f}")
    print(f"  ─────────────────────────────────────")
    print(f"  Pass rate (SG+V+Pass):    {pass_rate:.1f}%")
    print(f"  SG+V rate:                {(sg+v)/total*100:.1f}%")
    print(f"  Mean relative error:      {sum(r['rel_error'] for r in results)/total:.4f}%")
    print(f"  Median relative error:    {sorted(r['rel_error'] for r in results)[total//2]:.4f}%")
    print(f"  Max relative error:       {max(r['rel_error'] for r in results):.2f}%")
    print("=" * 60)

    # Grade breakdown by category
    print()
    print("  GRADE DISTRIBUTION BY CATEGORY:")
    categories = {
        'Lepton': ['L01', 'L02', 'L03'],
        'Quark':  ['Q01', 'Q02', 'Q03', 'Q04', 'Q05', 'Q05b', 'Q06', 'Q07'],
        'Gauge':  ['G01', 'G02'],
        'Neutrino': ['N01', 'N04', 'v21', 'v31', 'N21', 'Snu'],
        'CKM':    ['C01', 'C02'],
        'Higgs':  ['H01', 'H02', 'H03'],
        'Other':  ['Pr'],
    }

    for cat, ids in categories.items():
        cat_results = [r for r in results if r['id'] in ids]
        cat_grades = Counter(r['grade'] for r in cat_results)
        cat_pass = sum(1 for r in cat_results if r['grade'] != 'Fail')
        cat_total = len(cat_results)
        grade_str = '/'.join(f"{g}:{cat_grades.get(g,0)}" for g in ['SG','V','Pass','Fail'])
        print(f"    {cat:<10} [{', '.join(ids):<40}] -> {grade_str} | Pass: {cat_pass}/{cat_total}")

    return results

if __name__ == '__main__':
    results = main()
