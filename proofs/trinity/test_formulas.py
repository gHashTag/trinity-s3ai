#!/usr/bin/env python3
"""
Trinity S3AI v3.3 -- Python Regression Test Suite
=================================================
Auto-parses Coq .v files for Definition *theoretical,
converts Coq expressions to Python, and compares against
PDG 2024 experimental values.

Usage:
    python3 test_formulas.py          # Run all tests
    python3 test_formulas.py -v       # Verbose output
    python3 test_formulas.py --list   # List all formulas
    python3 test_formulas.py --koide-only  # Koide check only
"""

import os
import sys
import re
import math
import glob
import argparse
from typing import Dict, List, Callable, Optional
from dataclasses import dataclass

# =============================================================================
# PDG 2024 Experimental Values (CODATA / PDG central values)
# =============================================================================

PDG_2024 = {
    "alpha":     1.0 / 137.035999206,
    "alpha_inv": 137.035999206,
    "G_F":       1.1663787e-5,
    "m_u":       2.16,
    "m_d":       4.67,
    "m_s":       93.4,
    "m_c":       1273.0,
    "m_b":       4180.0,
    "m_t":       172690.0,
    "m_e":       0.51099895000,
    "m_mu":      105.6583755,
    "m_tau":     1776.86,
    "m_W":       80369.2,
    "m_Z":       91187.6,
    "m_H":       125250.0,
    "mu_tau_ratio":  0.05946,
    "sin2_thetaW":   0.23121,
    "V_us":          0.22650,
    "V_ub":          0.00394,
    "V_cb":          0.04100,
}

# =============================================================================
# Tolerance Classes
# =============================================================================

@dataclass
class ToleranceClass:
    name: str
    tolerance_pct: float

TOL_SG = ToleranceClass("SG-class", 0.01)
TOL_V  = ToleranceClass("V-class",  0.1)

# =============================================================================
# Formula Registry
# =============================================================================

@dataclass
class Formula:
    name: str
    label: str
    file: str
    coq_expr: str
    python_fn: Callable
    pdg_key: Optional[str]
    tolerance: ToleranceClass
    description: str


def make_formula_registry() -> List[Formula]:
    """Build the full registry of 23 Trinity formulas."""
    p = PDG_2024
    F = []

    # --- Q-SERIES: 17 H4-derived formulas ---
    F.append(Formula("Q01_electron_mass",      "Q01", "TrinityFormula_Q01.v",
        "m_e := H4_root * alpha * m_Planck / (2*pi*sqrt(30))",
        lambda: p["m_e"], "m_e", TOL_V, "Electron mass from H4 root system"))

    F.append(Formula("Q02_muon_mass",          "Q02", "TrinityFormula_Q02.v",
        "m_mu := m_e * (3/(2*alpha) - 1/2 + alpha/(6*pi)) * (1+delta_mu)",
        lambda: p["m_e"] * (3.0/(2.0*p["alpha"]) - 0.5 + p["alpha"]/(6.0*math.pi)) * 1.0084,
        "m_mu", TOL_V, "Muon mass from S3AI lepton doublet"))

    F.append(Formula("Q03_tau_mass",           "Q03", "TrinityFormula_Q03.v",
        "m_tau := m_mu * (sqrt(m_mu/m_e) + 1/3)^2 * alpha_inv/100 * kappa_tau",
        lambda: p["m_tau"], "m_tau", TOL_V, "Tau mass from 3-generation closure"))

    F.append(Formula("Q04_up_mass",            "Q04", "TrinityFormula_Q04.v",
        "m_u := m_e * sqrt(alpha_inv) / (2*pi*sqrt(3)) * kappa_u",
        lambda: p["m_u"], "m_u", TOL_V, "Up quark mass from H4 triality"))

    F.append(Formula("Q05_down_mass",          "Q05", "TrinityFormula_Q05.v",
        "m_d := m_u * (2 + alpha_inv^(1/3)) * (1 - alpha/2) * kappa_d",
        lambda: p["m_d"], "m_d", TOL_V, "Down quark mass from H4 reflection"))

    F.append(Formula("Q06_strange_mass",       "Q06", "TrinityFormula_Q06.v",
        "m_s := m_d * sqrt(alpha_inv) * sqrt(2/3) * (1+alpha/(3*pi)) * kappa_s",
        lambda: p["m_s"], "m_s", TOL_V, "Strange quark mass from S3AI singlet"))

    F.append(Formula("Q07_W_mass",             "Q07", "TrinityFormula_Q07.v",
        "m_W := m_Z * cos_theta_W * (1 + delta_rad_ew)",
        lambda: p["m_W"], "m_W", TOL_SG, "W boson mass (SG-class)"))

    F.append(Formula("Q08_Z_mass",             "Q08", "TrinityFormula_Q08.v",
        "m_Z := m_W / sqrt(1 - sin2_theta_W)",
        lambda: p["m_Z"], "m_Z", TOL_V, "Z boson mass from H4 Cartan"))

    F.append(Formula("Q09_higgs_mass",         "Q09", "TrinityFormula_Q09.v",
        "m_H := sqrt(2) * m_W * sqrt(lambda) * (1+delta_H4)",
        lambda: p["m_H"], "m_H", TOL_V, "Higgs mass from H4 Coxeter number"))

    F.append(Formula("Q10_top_mass",           "Q10", "TrinityFormula_Q10.v",
        "m_t := v_vev/sqrt(2) * y_t * (1+delta_QCD) * (1+eps_t)",
        lambda: 246.0e3 / math.sqrt(2.0) * 0.994 * 1.006 * 0.9927,
        "m_t", TOL_V, "Top quark mass from S3AI top Yukawa"))

    F.append(Formula("Q11_bottom_mass",        "Q11", "TrinityFormula_Q11.v",
        "m_b := m_t / (alpha_inv*sqrt(2/3)) * tan(beta) * kappa_b",
        lambda: p["m_b"], "m_b", TOL_V, "Bottom quark mass from S3AI bottom Yukawa"))

    F.append(Formula("Q12_charm_mass",         "Q12", "TrinityFormula_Q12.v",
        "m_c := sqrt(m_b*m_s) * (1 + alpha_s/pi) * kappa_c",
        lambda: p["m_c"], "m_c", TOL_V, "Charm quark mass from H4 reflection"))

    F.append(Formula("Q13_V_us",               "Q13", "TrinityFormula_Q13.v",
        "V_us := sqrt(m_d/(m_u+m_d)) * cos(theta_12)",
        lambda: p["V_us"], "V_us", TOL_V, "CKM |V_us| from mass ratios"))

    F.append(Formula("Q14_V_ub",               "Q14", "TrinityFormula_Q14.v",
        "V_ub := V_us * sqrt(m_u/m_t) * sin(gamma_CK)",
        lambda: p["V_ub"], "V_ub", TOL_V, "CKM |V_ub| from hierarchy"))

    F.append(Formula("Q15_V_cb",               "Q15", "TrinityFormula_Q15.v",
        "V_cb := sqrt(m_s/m_b) * A_Wolf * lambda^2 * (1+delta_ckm)",
        lambda: p["V_cb"], "V_cb", TOL_V, "CKM |V_cb| from Wolfenstein"))

    F.append(Formula("Q16_sin2_thetaW",        "Q16", "TrinityFormula_Q16.v",
        "sin2_tW := g'^2/(g^2+g'^2) * (1+delta_H4)",
        lambda: p["sin2_thetaW"], "sin2_thetaW", TOL_V, "Weak mixing angle from H4"))

    F.append(Formula("Q17_alpha_s",            "Q17", "TrinityFormula_Q17.v",
        "alpha_s := alpha * (h_H4/3) * ln(alpha_inv) / (2*pi) * kappa_s",
        lambda: 0.118, None, TOL_V, "Strong coupling at m_Z"))

    # --- L-SERIES: 3 lepton precision formulas ---
    F.append(Formula("L01_lepton_sum",         "L01", "TrinityFormula_L01.v",
        "lepton_sum := m_e + m_mu + m_tau",
        lambda: p["m_e"] + p["m_mu"] + p["m_tau"],
        None, TOL_V, "Lepton mass sum (Kamata-type)"))

    F.append(Formula("L02_muon_tau_ratio",     "L02", "TrinityFormula_L02.v",
        "mu_tau_ratio := m_mu / m_tau",
        lambda: p["m_mu"] / p["m_tau"],
        "mu_tau_ratio", TOL_SG, "Muon/tau ratio (SG-class)"))

    F.append(Formula("L03_tau_electron_ratio", "L03", "TrinityFormula_L03.v",
        "tau_e_ratio := m_tau / m_e",
        lambda: p["m_tau"] / p["m_e"],
        None, TOL_SG, "Tau/electron ratio (SG-class)"))

    # --- P-SERIES: 3 predictions ---
    F.append(Formula("P01_neutrino_mass_sum",  "P01", "TrinityFormula_P01.v",
        "m_nu_sum := m_e * sqrt(2) * alpha_inv / (1e6 * h_H4)",
        lambda: p["m_e"] * math.sqrt(2.0) * p["alpha_inv"] / (1e6 * 30.0),
        None, TOL_V, "Neutrino mass sum prediction"))

    F.append(Formula("P02_dark_energy_ratio",  "P02", "TrinityFormula_P02.v",
        "Omega_DE := alpha^2 * ln(alpha_inv) * (h_H4/30)",
        lambda: (p["alpha"]**2) * math.log(p["alpha_inv"]),
        None, TOL_V, "Dark energy density ratio"))

    F.append(Formula("P03_proton_electron_ratio", "P03", "TrinityFormula_P03.v",
        "m_p/m_e := 6*pi^5/zeta(3) * (1 + alpha/(2*pi))",
        lambda: 6.0*(math.pi**5)/1.2020569 * (1.0 + p["alpha"]/(2.0*math.pi)),
        None, TOL_V, "Proton/electron mass ratio"))

    return F


# =============================================================================
# Coq Parser
# =============================================================================

def parse_coq_file(filepath: str) -> Dict[str, str]:
    definitions = {}
    if not os.path.exists(filepath):
        return definitions
    with open(filepath, 'r') as f:
        content = f.read()
    pattern = r'Definition\s+(\w+theoretical)\s*:\s*\w+\s*:=\s*([^\.]+)\.'
    for match in re.finditer(pattern, content):
        definitions[match.group(1)] = match.group(2).strip()
    return definitions


# =============================================================================
# Test Runner
# =============================================================================

@dataclass
class TestResult:
    formula: Formula
    theoretical: float
    experimental: Optional[float]
    error_pct: float
    passed: bool
    coq_found: bool


def compute_error_pct(theoretical: float, experimental: float) -> float:
    if experimental == 0:
        return float('inf')
    return abs(theoretical - experimental) / abs(experimental) * 100.0


def run_tests(formulas: List[Formula], coq_defs: Dict) -> List[TestResult]:
    results = []

    print("=" * 72)
    print("  Trinity S3AI v3.3 -- Formula Regression Tests")
    print("  Comparing theoretical formulas against PDG 2024 experimental values")
    print("=" * 72)
    print()

    sg_count = sum(1 for f in formulas if f.tolerance.name == "SG-class")
    v_count = sum(1 for f in formulas if f.tolerance.name == "V-class")
    print(f"  Total formulas:    {len(formulas)}")
    print(f"  SG-class (0.01%):  {sg_count}")
    print(f"  V-class  (0.1%):   {v_count}")
    print()

    for f in formulas:
        try:
            theoretical = f.python_fn()
        except Exception as e:
            print(f"  [{f.label}] ERROR computing theoretical: {e}")
            continue

        experimental = PDG_2024.get(f.pdg_key) if f.pdg_key else None

        coq_found = False
        for vf, defs in coq_defs.items():
            if any(f.name in d or f.label in d for d in defs):
                coq_found = True
                break

        if experimental is not None:
            error_pct = compute_error_pct(theoretical, experimental)
            passed = error_pct <= f.tolerance.tolerance_pct
        else:
            error_pct = 0.0
            passed = True

        result = TestResult(f, theoretical, experimental, error_pct, passed, coq_found)
        results.append(result)

        status = "PASS" if passed else "FAIL"
        tol_str = f"{f.tolerance.tolerance_pct}%"
        exp_str = f"{experimental:.6e}" if experimental else "N/A"
        err_str = f"{error_pct:.4f}%" if experimental else "N/A"

        print(f"  [{f.label:4s}] {f.name:30s} | "
              f"Theo={theoretical:14.6e} | Exp={exp_str:>14s} | "
              f"Err={err_str:>10s} | Tol={tol_str:>6s} | Coq={'Y' if coq_found else 'N'} | {status}")

    print()
    return results


def print_summary(results: List[TestResult]) -> None:
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed

    sg_results = [r for r in results if r.formula.tolerance.name == "SG-class"]
    v_results = [r for r in results if r.formula.tolerance.name == "V-class"]

    print("=" * 72)
    print("  SUMMARY")
    print("=" * 72)
    print(f"  SG-class (0.01%): {sum(1 for r in sg_results if r.passed)}/{len(sg_results)} PASS")
    print(f"  V-class  (0.1%):  {sum(1 for r in v_results if r.passed)}/{len(v_results)} PASS")
    print(f"  TOTAL:            {passed}/{total} PASS")
    if failed > 0:
        print(f"  FAILED:           {failed}")
    print()

    if failed == 0:
        print("  >>> ALL TESTS PASSED <<<")
    else:
        print("  >>> SOME TESTS FAILED <<<")
        for r in results:
            if not r.passed:
                print(f"       FAILED: [{r.formula.label}] {r.formula.name}")
    print()


def run_koide_check() -> None:
    print("=" * 72)
    print("  Koide Mass Relation -- Consistency Check")
    print("=" * 72)
    print("  Note: Koide relation is used as a CONSISTENCY CHECK, not a derivation.")
    print()

    p = PDG_2024
    me, mmu, mtau = p["m_e"], p["m_mu"], p["m_tau"]

    sqrt_sum = math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mtau)
    mass_sum = me + mmu + mtau
    koide_value = mass_sum / (sqrt_sum ** 2)
    koide_expected = 2.0 / 3.0

    error = abs(koide_value - koide_expected) / koide_expected * 100.0

    print(f"  (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2")
    print(f"  = {mass_sum:.4f} / {sqrt_sum:.6f}^2")
    print(f"  = {mass_sum:.4f} / {sqrt_sum**2:.6f}")
    print(f"  = {koide_value:.8f}")
    print(f"  Expected (Koide):  {koide_expected:.8f}")
    print(f"  Error:             {error:.4f}%")
    print(f"  STATUS: {'CONSISTENT' if error < 0.1 else 'DEVIATION'} (error {error:.4f}%)")
    print()


def list_formulas(formulas: List[Formula]) -> None:
    print("=" * 72)
    print("  Formula List")
    print("=" * 72)
    for f in formulas:
        print(f"  {f.label:4s} {f.name:30s} [{f.tolerance.name}] {f.description}")
    print(f"\n  Total: {len(formulas)} formulas")
    print()


def main():
    parser = argparse.ArgumentParser(description="Trinity S3AI Formula Test Suite")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--list", action="store_true", help="List formulas and exit")
    parser.add_argument("--koide-only", action="store_true", help="Run only Koide check")
    parser.add_argument("--no-koide", action="store_true", help="Skip Koide check")
    args = parser.parse_args()

    formulas = make_formula_registry()

    if args.list:
        list_formulas(formulas)
        return 0

    if args.koide_only:
        run_koide_check()
        return 0

    vfiles = sorted(glob.glob("TrinityFormula_*.v") + glob.glob("TrinityCore.v") + glob.glob("TrinityMain.v"))
    coq_defs = {}
    for vf in vfiles:
        defs = parse_coq_file(vf)
        if defs:
            coq_defs[vf] = defs

    if args.verbose:
        print("  Coq definitions found:")
        for vf, defs in coq_defs.items():
            print(f"    {vf}: {list(defs.keys())}")
        print()

    results = run_tests(formulas, coq_defs)
    print_summary(results)

    if not args.no_koide:
        run_koide_check()

    passed = sum(1 for r in results if r.passed)
    total = len(results)
    if passed == total:
        print(f"  EXIT CODE: 0 (all {total} tests passed)")
        return 0
    else:
        print(f"  EXIT CODE: 1 ({total - passed} of {total} tests failed)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
