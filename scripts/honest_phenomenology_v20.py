#!/usr/bin/env python3
"""
Trinity S3AI — Wave 20: Honest Phenomenology (Direction A)
Pre-registered Monte-Carlo p-value + sigma-ranking refresh.

Improvements over Wave 18:
- 10× more trials (500k vs 50k) for tighter p-value estimates
- Full 26-observable catalog from Catalog42.v (replaced withdrawn δ_CP)
- Added: sin²θ_13, sin²θ_23, sin²θ_W, |V_ub|, λ_Higgs
- Removed: δ_CP (withdrawn at >5σ by NuFit 6.0 + T2K+NOvA 2025)
- Updated: m_H = 125.11 GeV (PDG 2024), sin²θ_W effective
- Real PDG/FLAG/NuFit uncertainties throughout

"не врать" principle: This script reports what the data says,
even if the result is not significant.
"""

import os
import sys
import math
import json
import time
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, Callable, List

import numpy as np
import mpmath as mp

# =============================================================================
# OUTPUT
# =============================================================================
OUT_DIR = Path(__file__).parent.parent / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# CONFIGURATION
# =============================================================================
N_TRIALS = 500_000      # 10× Wave 18
SAMPLE_SIZE = 2_000     # formulas sampled per trial
SEED = 20260523         # Wave 20 date

# Search-space parameters (pre-registered)
P_MAX = 1000
Q_MAX = 100
EXP_MIN = -6
EXP_MAX = 6

PHI = mp.phi
PI = mp.pi
E = mp.e

TEMPLATE_REGISTRY = {
    'T1': 'C * phi^a * pi^b * e^c',
    'T2': 'C + phi^a * pi^b * e^c',
    'T3': 'C * phi^a / (pi^b * e^c)',
    'T4': 'C * phi^a + D * pi^b * e^c',
    'T5': '(C + phi^a) / (D + pi^b * e^c)',
}


# =============================================================================
# SEARCH SPACE CONSTRUCTION
# =============================================================================

def generate_rationals() -> List[float]:
    """Generate rational prefactors p/q with p≤P_MAX, q≤Q_MAX."""
    rationals = set()
    for p in range(1, P_MAX + 1):
        for q in range(1, Q_MAX + 1):
            val = p / q
            if val > 0 and val <= 10000:
                rationals.add(val)
    # H4 invariants
    H4_INVARIANTS = [1, 2, 7, 11, 12, 19, 20, 29, 30, 120, 240]
    for h in H4_INVARIANTS:
        rationals.add(float(h))
    return sorted(rationals)


RATIONALS = generate_rationals()
print(f"[Init] Rational prefactor space size: {len(RATIONALS)}")

EXPONENTS = list(range(EXP_MIN, EXP_MAX + 1))
print(f"[Init] Exponent choices per constant: {len(EXPONENTS)}")


# =============================================================================
# PDG 2024 + NuFit 6.0 TARGETS WITH REAL UNCERTAINTIES
# =============================================================================

@dataclass
class Target:
    name: str
    value: float
    uncertainty: float
    unit: str
    source: str
    note: str = ""


TARGETS: Dict[str, Target] = {
    'L01': Target('m_mu/m_e (pole)', 206.7682830, 0.0000046, '', 'PDG 2024',
                  'Muon/electron mass ratio, pole masses'),
    'L02': Target('m_tau/m_mu (pole)', 16.8167, 0.0011, '', 'PDG 2024',
                  'Tau/muon mass ratio'),
    'L03': Target('m_tau/m_e (pole)', 3477.3, 0.2, '', 'PDG 2024',
                  'Tau/electron mass ratio'),
    'Q01': Target('m_u/m_d (@2GeV)', 0.462, 0.018, '', 'FLAG 2024',
                  'Light quark mass ratio; asymmetric uncertainty ~0.46±0.02'),
    'Q02': Target('m_s/m_u (@2GeV)', 43.24, 1.4, '', 'FLAG 2024',
                  'Strange/up mass ratio'),
    'Q03': Target('m_c/m_d', 272.0, 5.0, '', 'PDG 2024',
                  'Charm/down; cross-scheme uncertainty larger'),
    'Q04': Target('m_c/m_s', 13.633, 0.020, '', 'PDG 2024',
                  'Charm/strange'),
    'Q05': Target('m_b/m_s', 44.94, 0.10, '', 'PDG 2024',
                  'Bottom/strange'),
    'Q07': Target('m_s/m_d (@2GeV)', 20.00, 0.70, '', 'PDG 2024',
                  'Strange/down'),
    'G01': Target('1/alpha (Thomson)', 137.035999084, 0.000000021, '', 'PDG 2024',
                  'Inverse fine-structure at q²=0'),
    'G03': Target('sin²θ_W (effective)', 0.22336, 0.00010, '', 'PDG 2024',
                  'Weak mixing angle, effective sin²θ_W'),
    'N01': Target('sin²θ_12', 0.307, 0.013, '', 'PDG 2024 (NuFit)',
                  'Solar mixing angle'),
    'N03': Target('sin²θ_23', 0.546, 0.021, '', 'PDG 2024 (NuFit)',
                  'Atmospheric mixing angle'),
    'Sin13': Target('sin²θ_13', 0.0220, 0.0007, '', 'NuFit 6.0 2024',
                    'Reactor mixing angle; NH best fit'),
    'C01': Target('|V_us|', 0.22650, 0.00050, '', 'PDG 2024',
                  'CKM element'),
    'C02': Target('|V_cb|', 0.04053, 0.00072, '', 'PDG 2024',
                  'CKM element; inclusive/exclusive tension'),
    'C03': Target('|V_ub|', 0.00382, 0.00020, '', 'PDG 2024',
                  'CKM element; inclusive/exclusive tension'),
    'H01': Target('m_H', 125.11, 0.11, 'GeV', 'PDG 2024',
                  'Higgs boson mass; updated from 125.20'),
    'H02': Target('m_H/m_W', 125.11 / 80.379,
                  math.hypot(0.11/80.379, 125.11*0.012/80.379**2), '', 'Derived',
                  'Ratio of pole masses'),
    'H03': Target('m_H/m_Z', 125.11 / 91.1876,
                  math.hypot(0.11/91.1876, 125.11*0.0021/91.1876**2), '', 'Derived',
                  'Ratio of pole masses'),
    'v21': Target('Δm²_21', 7.53e-5, 0.20e-5, 'eV²', 'PDG 2024',
                  'Neutrino mass-squared difference'),
    'v31': Target('Δm²_31', 2.51e-3, 0.03e-3, 'eV²', 'PDG 2024 NH',
                  'Atmospheric neutrino difference; NH'),
    'N21': Target('Δm²_21/Δm²_31', 7.53e-5/2.51e-3,
                  7.53e-5/2.51e-3 * math.hypot(0.20/7.53, 0.03/2.51), '', 'Derived',
                  'Ratio of mass-squared differences'),
    'Pr': Target('m_p/m_e', 1836.15267343, 0.00000011, '', 'PDG 2024',
                 'Proton/electron mass ratio'),
    'Snu': Target('Σm_ν', 0.0588, 0.012, 'eV', 'Planck 2018 + BAO',
                  'Sum of neutrino masses; 95% CL upper limit ~0.12'),
    'Lambda': Target('λ_Higgs', 0.129, 0.025, '', 'ATLAS+CMS Run 2',
                     'Higgs self-coupling; κ_λ = 1.02±0.19, λ_SM≈0.129'),
}

print(f"[Init] Loaded {len(TARGETS)} observables with real uncertainties")


# =============================================================================
# TRINITY CATALOG FORMULAS (from Catalog42.v, canonical)
# =============================================================================

TRINITY_FORMULAS: Dict[str, Tuple[str, str]] = {
    'Q07':  ('24*PHI**2/PI', 'm_s/m_d (@2GeV)'),
    'L03':  ('549*E*PI**2/PHI**3', 'm_tau/m_e (pole)'),
    'L02':  ('239*PHI**4/PI**4', 'm_tau/m_mu (pole)'),
    'H02':  ('11*PHI/20 + 2/3', 'm_H/m_W'),
    'N21':  ('PI/(40*PHI**2)', 'Δm²_21/Δm²_31'),
    'Pr':   ('6*PI**5', 'm_p/m_e'),
    'Q03':  ('19*PI*E**2/PHI', 'm_c/m_d'),
    'Q04':  ('24*PI**3/E**4', 'm_c/m_s'),
    'v21':  ('(PHI*E/PI)**6 * 1e-5', 'Δm²_21'),
    'v31':  ('15*PHI**(-5)*PI**(-2)*E**(-4)', 'Δm²_31'),
    'Snu':  ('8*PHI**(-6)*PI**(-5)*E**6 * 0.1', 'Σm_ν'),
    'L01':  ('239*E/PI', 'm_mu/m_e (pole)'),
    'G01':  ('36*PHI*E**2/PI', '1/alpha (Thomson)'),
    'N01':  ('8*PI/(PHI**5 * E**2)', 'sin²θ_12'),
    'N03':  ('PI**2/18', 'sin²θ_23'),
    'Sin13':('PI**2/(25*PHI**6)', 'sin²θ_13'),
    'C01':  ('2*PHI**3*E**2/(9*PI**3)', '|V_us|'),
    'C02':  ('1/(3*PHI**2*PI)', '|V_cb|'),
    'C03':  ('1/(39*PHI**2*E)', '|V_ub|'),
    'H01':  ('4*PHI**3*E**2', 'm_H'),
    'H03':  ('4*PHI*PI/15 + 4/225', 'm_H/m_Z'),
    'G03':  ('3/(8*PHI)', 'sin²θ_W'),
    'Q01':  ('2*PHI/7', 'm_u/m_d (@2GeV)'),
    'Q02':  ('12 + PHI**3*E**2', 'm_s/m_u (@2GeV)'),
    'Q05':  ('43 + PI/PHI', 'm_b/m_s'),
    'Lambda':('mp.sqrt(PHI)/(PI**2)', 'λ_Higgs'),
}


def eval_formula(expr: str) -> float:
    """Safely evaluate a Trinity formula expression."""
    ns = {'PHI': PHI, 'PI': PI, 'E': E, 'mp': mp, 'sqrt': mp.sqrt}
    return float(eval(expr, {"__builtins__": {}}, ns))


def compute_trinity_errors() -> Dict[str, dict]:
    """Compute Trinity catalog errors against PDG targets."""
    results = {}
    for fid, (expr, _) in TRINITY_FORMULAS.items():
        target = TARGETS[fid]
        computed = eval_formula(expr)
        diff = computed - target.value
        rel_err = abs(diff) / abs(target.value) * 100
        sigma = abs(diff) / target.uncertainty if target.uncertainty > 0 else float('inf')

        results[fid] = {
            'formula': expr,
            'target_value': target.value,
            'target_unc': target.uncertainty,
            'computed': computed,
            'abs_diff': abs(diff),
            'rel_error_percent': rel_err,
            'sigma_distance': sigma,
        }
    return results


# =============================================================================
# RANDOM FORMULA GENERATORS (PRE-REGISTERED TEMPLATES)
# =============================================================================

def random_formula_T1(rng: random.Random) -> Tuple[str, Callable]:
    C = rng.choice(RATIONALS)
    a, b, c = rng.choice(EXPONENTS), rng.choice(EXPONENTS), rng.choice(EXPONENTS)
    expr = f"{C} * PHI**{a} * PI**{b} * E**{c}"
    def fn():
        return C * (PHI ** a) * (PI ** b) * (E ** c)
    return expr, fn


def random_formula_T2(rng: random.Random) -> Tuple[str, Callable]:
    C = rng.choice(RATIONALS)
    a, b, c = rng.choice(EXPONENTS), rng.choice(EXPONENTS), rng.choice(EXPONENTS)
    expr = f"{C} + PHI**{a} * PI**{b} * E**{c}"
    def fn():
        return C + (PHI ** a) * (PI ** b) * (E ** c)
    return expr, fn


def random_formula_T3(rng: random.Random) -> Tuple[str, Callable]:
    C = rng.choice(RATIONALS)
    a, b, c = rng.choice(EXPONENTS), rng.choice(EXPONENTS), rng.choice(EXPONENTS)
    expr = f"{C} * PHI**{a} / (PI**{b} * E**{c})"
    def fn():
        return C * (PHI ** a) / ((PI ** b) * (E ** c))
    return expr, fn


def random_formula_T4(rng: random.Random) -> Tuple[str, Callable]:
    C = rng.choice(RATIONALS)
    D = rng.choice(RATIONALS)
    a, b, c = rng.choice(EXPONENTS), rng.choice(EXPONENTS), rng.choice(EXPONENTS)
    expr = f"{C} * PHI**{a} + {D} * PI**{b} * E**{c}"
    def fn():
        return C * (PHI ** a) + D * (PI ** b) * (E ** c)
    return expr, fn


def random_formula_T5(rng: random.Random) -> Tuple[str, Callable]:
    C = rng.choice(RATIONALS)
    D = rng.choice(RATIONALS)
    a, b, c = rng.choice(EXPONENTS), rng.choice(EXPONENTS), rng.choice(EXPONENTS)
    expr = f"({C} + PHI**{a}) / ({D} + PI**{b} * E**{c})"
    def fn():
        denom = D + (PI ** b) * (E ** c)
        if denom == 0:
            return float('inf')
        return (C + (PHI ** a)) / denom
    return expr, fn


TEMPLATE_GENERATORS = [
    random_formula_T1,
    random_formula_T2,
    random_formula_T3,
    random_formula_T4,
    random_formula_T5,
]


def random_formula(rng: random.Random) -> Tuple[str, Callable]:
    gen = rng.choice(TEMPLATE_GENERATORS)
    return gen(rng)


# =============================================================================
# MONTE-CARLO SIMULATION (vectorized)
# =============================================================================

PHI_F = float(PHI)
PI_F = float(PI)
E_F = float(E)

RATIONALS_ARR = np.array(RATIONALS, dtype=np.float64)
EXPONENTS_ARR = np.array(EXPONENTS, dtype=np.int32)

_OBS_IDS = list(TARGETS.keys())
_TARGET_VALUES = np.array([TARGETS[fid].value for fid in _OBS_IDS], dtype=np.float64)
_TARGET_UNCS = np.array([TARGETS[fid].uncertainty for fid in _OBS_IDS], dtype=np.float64)
_N_OBS = len(_OBS_IDS)


def batch_evaluate(templates_and_batches: List[Tuple[int, int]], rng: random.Random) -> Tuple[np.ndarray, np.ndarray]:
    all_vals = []

    for tidx, bsize in templates_and_batches:
        if bsize == 0:
            continue
        C_idx = rng.choices(range(len(RATIONALS_ARR)), k=bsize)
        C = RATIONALS_ARR[np.array(C_idx)]
        a = np.array(rng.choices(EXPONENTS_ARR, k=bsize), dtype=np.float64)
        b = np.array(rng.choices(EXPONENTS_ARR, k=bsize), dtype=np.float64)
        c = np.array(rng.choices(EXPONENTS_ARR, k=bsize), dtype=np.float64)

        if tidx == 0:  # T1
            vals = C * (PHI_F ** a) * (PI_F ** b) * (E_F ** c)
        elif tidx == 1:  # T2
            vals = C + (PHI_F ** a) * (PI_F ** b) * (E_F ** c)
        elif tidx == 2:  # T3
            denom = (PI_F ** b) * (E_F ** c)
            denom[denom == 0] = np.inf
            vals = C * (PHI_F ** a) / denom
        elif tidx == 3:  # T4
            D_idx = rng.choices(range(len(RATIONALS_ARR)), k=bsize)
            D = RATIONALS_ARR[np.array(D_idx)]
            vals = C * (PHI_F ** a) + D * (PI_F ** b) * (E_F ** c)
        elif tidx == 4:  # T5
            D_idx = rng.choices(range(len(RATIONALS_ARR)), k=bsize)
            D = RATIONALS_ARR[np.array(D_idx)]
            denom = D + (PI_F ** b) * (E_F ** c)
            denom[denom == 0] = np.inf
            vals = (C + (PHI_F ** a)) / denom
        else:
            vals = np.full(bsize, np.nan)

        all_vals.append(vals)

    if not all_vals:
        return np.empty((0, _N_OBS)), np.empty((0, _N_OBS))

    vals = np.concatenate(all_vals)
    valid = np.isfinite(vals)
    vals = vals[valid]

    if len(vals) == 0:
        return np.empty((0, _N_OBS)), np.empty((0, _N_OBS))

    diffs = np.abs(vals[:, None] - _TARGET_VALUES[None, :])
    rel_errors = diffs / np.abs(_TARGET_VALUES[None, :]) * 100
    sigmas = diffs / _TARGET_UNCS[None, :]

    return rel_errors, sigmas


def run_monte_carlo(n_trials: int = N_TRIALS, sample_size: int = SAMPLE_SIZE) -> dict:
    rng = random.Random(SEED)

    obs_ids = _OBS_IDS
    n_obs = _N_OBS

    trinity_errors = compute_trinity_errors()
    trinity_rel_errs = np.array([trinity_errors[fid]['rel_error_percent'] for fid in obs_ids])
    trinity_sigmas = np.array([trinity_errors[fid]['sigma_distance'] for fid in obs_ids])

    print(f"\n[MC] Starting {n_trials:,} trials, {sample_size:,} formulas per trial")
    print(f"[MC] Observables: {n_obs}")
    print(f"[MC] Search space estimate: {len(RATIONALS)} × {len(EXPONENTS)}³ × {len(TEMPLATE_GENERATORS)} ≈ {len(RATIONALS) * len(EXPONENTS)**3 * len(TEMPLATE_GENERATORS):.2e}")

    trial_best_rel_errors = np.zeros((n_trials, n_obs), dtype=np.float64)
    trial_best_sigmas = np.zeros((n_trials, n_obs), dtype=np.float64)
    trial_mean_rel_errors = np.zeros(n_trials, dtype=np.float64)
    trial_mean_sigmas = np.zeros(n_trials, dtype=np.float64)
    trial_hit_counts_1pct = np.zeros(n_trials, dtype=np.int32)
    trial_hit_counts_01pct = np.zeros(n_trials, dtype=np.int32)
    trial_hit_counts_sg = np.zeros(n_trials, dtype=np.int32)  # < 0.01%

    n_templates = len(TEMPLATE_GENERATORS)
    base_per_template = sample_size // n_templates
    remainder = sample_size % n_templates

    start_time = time.time()

    for trial in range(n_trials):
        batches = []
        for t in range(n_templates):
            bsize = base_per_template + (1 if t < remainder else 0)
            batches.append((t, bsize))

        rel_errors, sigmas = batch_evaluate(batches, rng)

        if rel_errors.shape[0] == 0:
            trial_best_rel_errors[trial] = np.inf
            trial_best_sigmas[trial] = np.inf
            trial_mean_rel_errors[trial] = np.inf
            trial_mean_sigmas[trial] = np.inf
            continue

        best_rel = np.min(rel_errors, axis=0)
        best_sigma = np.min(sigmas, axis=0)

        trial_best_rel_errors[trial] = best_rel
        trial_best_sigmas[trial] = best_sigma
        trial_mean_rel_errors[trial] = np.mean(best_rel)
        trial_mean_sigmas[trial] = np.mean(best_sigma)
        trial_hit_counts_1pct[trial] = np.sum(best_rel < 1.0)
        trial_hit_counts_01pct[trial] = np.sum(best_rel < 0.1)
        trial_hit_counts_sg[trial] = np.sum(best_rel < 0.01)

        if (trial + 1) % 5000 == 0:
            elapsed = time.time() - start_time
            print(f"  ... trial {trial + 1:,} / {n_trials:,} ({elapsed:.1f}s, {trial/elapsed:.1f} trials/s)", flush=True)

    elapsed = time.time() - start_time
    print(f"\n[MC] Completed in {elapsed:.1f}s ({n_trials/elapsed:.1f} trials/s)", flush=True)

    trinity_mean_rel = np.mean(trinity_rel_errs)
    trinity_mean_sigma = np.mean(trinity_sigmas)
    trinity_hits_1pct = np.sum(trinity_rel_errs < 1.0)
    trinity_hits_01pct = np.sum(trinity_rel_errs < 0.1)
    trinity_hits_sg = np.sum(trinity_rel_errs < 0.01)

    p_mean_rel = np.mean(trial_mean_rel_errors <= trinity_mean_rel)
    p_mean_sigma = np.mean(trial_mean_sigmas <= trinity_mean_sigma)
    p_hits_1pct = np.mean(trial_hit_counts_1pct >= trinity_hits_1pct)
    p_hits_01pct = np.mean(trial_hit_counts_01pct >= trinity_hits_01pct)
    p_hits_sg = np.mean(trial_hit_counts_sg >= trinity_hits_sg)

    per_obs_p_rel = {}
    per_obs_p_sigma = {}
    for i, fid in enumerate(obs_ids):
        p_rel = np.mean(trial_best_rel_errors[:, i] <= trinity_rel_errs[i])
        p_sigma = np.mean(trial_best_sigmas[:, i] <= trinity_sigmas[i])
        per_obs_p_rel[fid] = float(p_rel)
        per_obs_p_sigma[fid] = float(p_sigma)

    results = {
        'protocol': {
            'n_trials': n_trials,
            'sample_size': sample_size,
            'seed': SEED,
            'search_space_rationals': len(RATIONALS),
            'search_space_exponents': len(EXPONENTS),
            'search_space_templates': len(TEMPLATE_GENERATORS),
            'templates': TEMPLATE_REGISTRY,
        },
        'trinity': {
            'mean_rel_error_percent': float(trinity_mean_rel),
            'mean_sigma_distance': float(trinity_mean_sigma),
            'hits_1pct': int(trinity_hits_1pct),
            'hits_01pct': int(trinity_hits_01pct),
            'hits_sg': int(trinity_hits_sg),
            'per_observable': {
                fid: {
                    'rel_error_percent': float(trinity_rel_errs[i]),
                    'sigma_distance': float(trinity_sigmas[i]),
                }
                for i, fid in enumerate(obs_ids)
            },
        },
        'monte_carlo': {
            'mean_rel_error_percent': {
                'median': float(np.median(trial_mean_rel_errors)),
                'mean': float(np.mean(trial_mean_rel_errors)),
                'std': float(np.std(trial_mean_rel_errors)),
                'min': float(np.min(trial_mean_rel_errors)),
                'max': float(np.max(trial_mean_rel_errors)),
                'p_value_trinity_le_random': float(p_mean_rel),
            },
            'mean_sigma_distance': {
                'median': float(np.median(trial_mean_sigmas)),
                'mean': float(np.mean(trial_mean_sigmas)),
                'std': float(np.std(trial_mean_sigmas)),
                'min': float(np.min(trial_mean_sigmas)),
                'max': float(np.max(trial_mean_sigmas)),
                'p_value_trinity_le_random': float(p_mean_sigma),
            },
            'hits_1pct': {
                'median': int(np.median(trial_hit_counts_1pct)),
                'mean': float(np.mean(trial_hit_counts_1pct)),
                'std': float(np.std(trial_hit_counts_1pct)),
                'min': int(np.min(trial_hit_counts_1pct)),
                'max': int(np.max(trial_hit_counts_1pct)),
                'p_value_trinity_ge_random': float(p_hits_1pct),
            },
            'hits_01pct': {
                'median': int(np.median(trial_hit_counts_01pct)),
                'mean': float(np.mean(trial_hit_counts_01pct)),
                'std': float(np.std(trial_hit_counts_01pct)),
                'min': int(np.min(trial_hit_counts_01pct)),
                'max': int(np.max(trial_hit_counts_01pct)),
                'p_value_trinity_ge_random': float(p_hits_01pct),
            },
            'hits_sg': {
                'median': int(np.median(trial_hit_counts_sg)),
                'mean': float(np.mean(trial_hit_counts_sg)),
                'std': float(np.std(trial_hit_counts_sg)),
                'min': int(np.min(trial_hit_counts_sg)),
                'max': int(np.max(trial_hit_counts_sg)),
                'p_value_trinity_ge_random': float(p_hits_sg),
            },
            'per_observable_p_rel': per_obs_p_rel,
            'per_observable_p_sigma': per_obs_p_sigma,
        },
    }

    return results


# =============================================================================
# REPORT GENERATION
# =============================================================================

def sigma_grade(sigma: float) -> str:
    if sigma < 0.1:
        return "SG (<0.1σ)"
    elif sigma < 1.0:
        return "V (0.1–1.0σ)"
    elif sigma < 3.0:
        return "Pass (1–3σ)"
    elif sigma < 5.0:
        return "Marginal (3–5σ)"
    else:
        return "Fail (>5σ)"


def generate_report(results: dict) -> str:
    lines = []
    lines.append("# Trinity S³AI — Wave 20 Honest Phenomenology Report")
    lines.append("")
    lines.append("**Date:** 2026-05-23  ")
    lines.append("**Protocol:** Pre-registered Monte-Carlo p-value (Direction A)  ")
    lines.append("**Trials:** {:,}  ".format(results['protocol']['n_trials']))
    lines.append("**Sample size:** {:,} formulas per trial  ".format(results['protocol']['sample_size']))
    lines.append("**Wave:** 20 (honest refresh of Wave 18)  ")
    lines.append("")

    lines.append("## 1. Pre-Registered Protocol")
    lines.append("")
    lines.append("### Search Space")
    lines.append(f"- Rational prefactors: {results['protocol']['search_space_rationals']:,} values (p/q, p≤{P_MAX}, q≤{Q_MAX})")
    lines.append(f"- Exponents: a,b,c ∈ {{{EXP_MIN},...,{EXP_MAX}}} ({results['protocol']['search_space_exponents']} choices each)")
    lines.append(f"- Templates: {results['protocol']['search_space_templates']}")
    for tid, tdesc in results['protocol']['templates'].items():
        lines.append(f"  - `{tid}`: `{tdesc}`")
    lines.append("")

    lines.append("### Catalog Changes from Wave 18")
    lines.append("- **Removed:** δ_CP (N04) — withdrawn at >5σ by NuFit 6.0 + T2K+NOvA 2025")
    lines.append("- **Added:** sin²θ_13 (Sin13), sin²θ_23 (N03), sin²θ_W (G03), |V_ub| (C03), λ_Higgs (Lambda)")
    lines.append("- **Updated:** m_H = 125.11±0.11 GeV (PDG 2024)")
    lines.append(f"- **Total observables:** {len(TARGETS)}")
    lines.append("")

    lines.append("### PDG Targets")
    lines.append(f"- {len(TARGETS)} observables with real experimental uncertainties")
    lines.append("- Sources: PDG 2024, FLAG 2024, NuFit 6.0, Planck 2018+BAO, ATLAS+CMS Run 2")
    lines.append("")

    lines.append("## 2. Trinity Catalog Performance")
    lines.append("")
    lines.append("| Observable | Formula (excerpt) | Target | Computed | Rel.Error | σ-distance | Grade |")
    lines.append("|------------|-------------------|--------|----------|-----------|------------|-------|")

    trinity = results['trinity']['per_observable']
    for fid in TARGETS.keys():
        if fid not in trinity:
            continue
        t = trinity[fid]
        expr_short = TRINITY_FORMULAS[fid][0][:35]
        target = TARGETS[fid]
        computed = eval_formula(TRINITY_FORMULAS[fid][0])
        grade = sigma_grade(t['sigma_distance'])
        lines.append(f"| {fid} | `{expr_short}` | {target.value:.4g} | {computed:.4g} | {t['rel_error_percent']:.4f}% | {t['sigma_distance']:.2f}σ | {grade} |")

    lines.append("")
    lines.append("**Summary:**")
    lines.append(f"- Mean relative error: {results['trinity']['mean_rel_error_percent']:.4f}%")
    lines.append(f"- Mean σ-distance: {results['trinity']['mean_sigma_distance']:.2f}σ")
    lines.append(f"- SG-class (<0.01%): {results['trinity']['hits_sg']}/{len(TARGETS)}")
    lines.append(f"- V-class (<0.1%): {results['trinity']['hits_01pct']}/{len(TARGETS)}")
    lines.append(f"- <1.0% error: {results['trinity']['hits_1pct']}/{len(TARGETS)}")
    lines.append("")

    lines.append("## 3. Monte-Carlo Results")
    lines.append("")
    lines.append("### Distribution of Best Random Errors")
    mc = results['monte_carlo']
    lines.append("| Metric | Trinity | Random (median) | Random (mean±std) | p-value |")
    lines.append("|--------|---------|-----------------|-------------------|---------|")
    lines.append(f"| Mean rel.error (%) | {results['trinity']['mean_rel_error_percent']:.4f} | {mc['mean_rel_error_percent']['median']:.4f} | {mc['mean_rel_error_percent']['mean']:.4f}±{mc['mean_rel_error_percent']['std']:.4f} | {mc['mean_rel_error_percent']['p_value_trinity_le_random']:.4f} |")
    lines.append(f"| Mean σ-distance | {results['trinity']['mean_sigma_distance']:.2f} | {mc['mean_sigma_distance']['median']:.2f} | {mc['mean_sigma_distance']['mean']:.2f}±{mc['mean_sigma_distance']['std']:.2f} | {mc['mean_sigma_distance']['p_value_trinity_le_random']:.4f} |")
    lines.append(f"| SG hits (<0.01%) | {results['trinity']['hits_sg']} | {mc['hits_sg']['median']} | {mc['hits_sg']['mean']:.1f}±{mc['hits_sg']['std']:.1f} | {mc['hits_sg']['p_value_trinity_ge_random']:.4f} |")
    lines.append(f"| V hits (<0.1%) | {results['trinity']['hits_01pct']} | {mc['hits_01pct']['median']} | {mc['hits_01pct']['mean']:.1f}±{mc['hits_01pct']['std']:.1f} | {mc['hits_01pct']['p_value_trinity_ge_random']:.4f} |")
    lines.append(f"| Hits <1.0% | {results['trinity']['hits_1pct']} | {mc['hits_1pct']['median']} | {mc['hits_1pct']['mean']:.1f}±{mc['hits_1pct']['std']:.1f} | {mc['hits_1pct']['p_value_trinity_ge_random']:.4f} |")
    lines.append("")

    lines.append("### Per-Observable P-Values")
    lines.append("P(observable | Trinity error ≤ random best error)")
    lines.append("")
    lines.append("| Observable | p-value (rel.error) | p-value (σ-distance) | Interpretation |")
    lines.append("|------------|---------------------|----------------------|----------------|")
    for fid in TARGETS.keys():
        p_rel = mc['per_observable_p_rel'].get(fid, 0)
        p_sig = mc['per_observable_p_sigma'].get(fid, 0)
        if p_rel < 0.001:
            interp = "Highly significant"
        elif p_rel < 0.01:
            interp = "Significant"
        elif p_rel < 0.05:
            interp = "Suggestive"
        else:
            interp = "Not significant"
        lines.append(f"| {fid} | {p_rel:.4f} | {p_sig:.4f} | {interp} |")
    lines.append("")

    lines.append("## 4. Sigma-Ranking (Wave 20 Refresh)")
    lines.append("")
    lines.append("Ranked by σ-distance (smallest = best agreement with experiment):")
    lines.append("")
    lines.append("| Rank | Observable | σ-distance | Grade | Note |")
    lines.append("|------|------------|------------|-------|------|")

    sorted_obs = sorted(
        [(fid, trinity[fid]['sigma_distance']) for fid in TARGETS.keys() if fid in trinity],
        key=lambda x: x[1]
    )
    for rank, (fid, sigma) in enumerate(sorted_obs, 1):
        grade = sigma_grade(sigma)
        note = ""
        if sigma > 1000:
            note = "Ultra-precision trap"
        elif sigma > 100:
            note = "Precise measurement"
        elif sigma < 0.1:
            note = "SG-class"
        lines.append(f"| {rank} | {fid} | {sigma:.3f}σ | {grade} | {note} |")

    lines.append("")

    lines.append("## 5. Interpretation")
    lines.append("")
    p_mean_rel = mc['mean_rel_error_percent']['p_value_trinity_le_random']
    p_mean_sig = mc['mean_sigma_distance']['p_value_trinity_le_random']
    p_hits_sg = mc['hits_sg']['p_value_trinity_ge_random']
    p_hits_01 = mc['hits_01pct']['p_value_trinity_ge_random']

    if p_mean_rel < 0.001 and p_hits_sg < 0.001:
        verdict = (
            "The Trinity catalog achieves highly significant improvement over random sampling "
            f"(mean error p = {p_mean_rel:.4f}, SG hits p = {p_hits_sg:.4f}). "
            "This suggests the catalog is not a trivial random coincidence."
        )
    elif p_mean_rel < 0.01 and (p_hits_sg < 0.01 or p_hits_01 < 0.01):
        verdict = (
            "The Trinity catalog shows statistically significant improvement over random sampling "
            f"(mean error p = {p_mean_rel:.4f}, SG/V hits p = {p_hits_sg:.4f}/{p_hits_01:.4f}). "
            "The result is significant but not overwhelming."
        )
    elif p_mean_rel < 0.05 or p_hits_01 < 0.05:
        verdict = (
            "The Trinity catalog shows marginal significance against random coincidence "
            f"(mean error p = {p_mean_rel:.4f}, V hits p = {p_hits_01:.4f}). "
            "The result is suggestive but not conclusive."
        )
    else:
        verdict = (
            "The Trinity catalog does NOT show statistically significant improvement "
            f"over random sampling (mean error p = {p_mean_rel:.4f}). "
            "The observed precision is consistent with searching a large enough space. "
            "This is an honest negative result — the formulas are phenomenological fits, "
            "not first-principles derivations."
        )

    lines.append(verdict)
    lines.append("")

    lines.append("## 6. Comparison with Wave 18")
    lines.append("")
    lines.append("| Metric | Wave 18 | Wave 20 | Change |")
    lines.append("|--------|---------|---------|--------|")
    lines.append(f"| Trials | 50,000 | {results['protocol']['n_trials']:,} | 10× |")
    lines.append(f"| Observables | 25 | {len(TARGETS)} | +1 (replaced δ_CP with sin²θ_13, sin²θ_23, sin²θ_W, |V_ub|, λ) |")
    lines.append("| SG-class formulas | 11 | {} | see table |".format(results['trinity']['hits_sg']))
    lines.append("")

    lines.append("## 7. Limitations")
    lines.append("")
    lines.append("1. **Search space size**: The chosen space (~10⁸ formulas) may not match the actual space searched. If true space was larger, p-value is conservative. If smaller, anti-conservative.")
    lines.append("2. **Template choice**: Five pre-registered templates. Original search may have used additional forms (logs, square roots, nested expressions).")
    lines.append("3. **Multiple testing**: No explicit Bonferroni correction on aggregate p-values; per-observable p-values are uncorrected.")
    lines.append("4. **Cosmological limits**: Σm_ν and λ_Higgs have large asymmetric/non-Gaussian uncertainties; σ-distance is less meaningful for these.")
    lines.append("5. **Mass scheme mixing**: Different renormalization schemes (pole, MSbar @ 2GeV, @ m_q) are treated as dimensionless ratios; scheme-dependence is a systematic.")
    lines.append("")
    lines.append("---")
    lines.append("*Report generated by Wave 20 honest phenomenology protocol.*")
    lines.append("*Principle: не врать — we report what the data says, even when it's not significant.*")

    return "\n".join(lines)


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("TRINITY S³AI — WAVE 20: HONEST PHENOMENOLOGY (DIRECTION A)")
    print("=" * 70)
    print(f"Protocol: Pre-registered Monte-Carlo p-value")
    print(f"Trials: {N_TRIALS:,} | Sample: {SAMPLE_SIZE:,} | Seed: {SEED}")
    print("")

    print("[1/4] Computing Trinity catalog errors...")
    trinity_errors = compute_trinity_errors()
    print(f"       Mean rel.error: {np.mean([v['rel_error_percent'] for v in trinity_errors.values()]):.4f}%")
    print(f"       Mean σ-distance: {np.mean([v['sigma_distance'] for v in trinity_errors.values()]):.2f}")

    print("\n[2/4] Running Monte-Carlo simulation...")
    mc_results = run_monte_carlo()

    print("\n[3/4] Saving results...")
    json_path = OUT_DIR / "wave20_mc_results.json"
    with open(json_path, 'w') as f:
        json.dump(mc_results, f, indent=2)
    print(f"       JSON: {json_path}")

    print("\n[4/4] Generating report...")
    report = generate_report(mc_results)
    report_path = OUT_DIR / "honest_pvalue_report_v20.md"
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"       Report: {report_path}")

    print("\n" + "=" * 70)
    print("WAVE 20 COMPLETE")
    print("=" * 70)
    p_rel = mc_results['monte_carlo']['mean_rel_error_percent']['p_value_trinity_le_random']
    p_sig = mc_results['monte_carlo']['mean_sigma_distance']['p_value_trinity_le_random']
    p_hits_sg = mc_results['monte_carlo']['hits_sg']['p_value_trinity_ge_random']
    p_hits_01 = mc_results['monte_carlo']['hits_01pct']['p_value_trinity_ge_random']
    print(f"P(Trinity mean error ≤ random): {p_rel:.4f}")
    print(f"P(Trinity mean σ ≤ random):     {p_sig:.4f}")
    print(f"P(Trinity SG hits ≥ random):    {p_hits_sg:.4f}")
    print(f"P(Trinity V hits ≥ random):     {p_hits_01:.4f}")
    print("")
    if p_rel < 0.001:
        print("VERDICT: Highly significant (p < 0.001)")
    elif p_rel < 0.01:
        print("VERDICT: Statistically significant (p < 0.01)")
    elif p_rel < 0.05:
        print("VERDICT: Marginally significant (p < 0.05)")
    else:
        print("VERDICT: NOT significant — consistent with random search")
    print("=" * 70)


if __name__ == '__main__':
    main()
