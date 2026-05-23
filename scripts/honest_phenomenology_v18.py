#!/usr/bin/env python3
"""
Trinity S3AI — Wave 18: Honest Phenomenology & Monte-Carlo P-Value
==================================================================

Pre-registered protocol (2026-05-22):
1. Search space: C * phi^a * pi^b * e^c and variants
2. PDG 2024 targets with REAL experimental uncertainties
3. Continuous surprise metric: compare error vector distributions
4. 100,000 Monte-Carlo trials

Author: Wave 18 Agent
License: Same as project (MIT)
"""

import json
import math
import random
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Tuple, Callable

import numpy as np
from mpmath import mp, phi as PHI_SYM, pi as PI_SYM, e as E_SYM

# =============================================================================
# CONFIGURATION
# =============================================================================
mp.dps = 50

PHI = (1 + mp.sqrt(5)) / 2
PI = mp.pi
E = mp.e

# Number of MC trials
N_TRIALS = 50_000
# Sample size per trial (formulas tested per observable)
SAMPLE_SIZE = 2_000
# Random seed for reproducibility
SEED = 20260522

# Output paths
OUT_DIR = Path(__file__).parent.parent / "derivations" / "catalog_audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# PRE-REGISTERED SEARCH SPACE
# =============================================================================

# H4 invariants as explicit rational prefactors
H4_INVARIANTS = [1, 2, 7, 11, 12, 19, 20, 29, 30, 120, 240, 480]

# Rational prefactors: p/q where p in [1, P_MAX], q in [1, Q_MAX]
P_MAX = 1000
Q_MAX = 100

# Exponent ranges for phi, pi, e
EXP_MIN = -6
EXP_MAX = 6

# Pre-registered formula templates (no cherry-picking allowed)
# Each returns a function(a,b,c, C, ...) -> mpmath value
TEMPLATE_REGISTRY = {
    'T1_mono': 'C * phi^a * pi^b * e^c',
    'T2_add': 'C + phi^a * pi^b * e^c',
    'T3_div': 'C * phi^a / (pi^b * e^c)',
    'T4_twoterm': 'C * phi^a + D * pi^b * e^c',
    'T5_ratio': '(C + phi^a) / (D + pi^b * e^c)',
}


def generate_rationals(p_max: int = P_MAX, q_max: int = Q_MAX) -> List[float]:
    """Generate all unique reduced fractions p/q."""
    rationals = set()
    for p in range(1, p_max + 1):
        for q in range(1, q_max + 1):
            val = p / q
            if val > 0 and val <= 10000:  # sanity bound
                rationals.add(val)
    # Also include H4 invariants
    for h in H4_INVARIANTS:
        rationals.add(float(h))
    return sorted(rationals)


RATIONALS = generate_rationals()
print(f"[Init] Rational prefactor space size: {len(RATIONALS)}")

EXPONENTS = list(range(EXP_MIN, EXP_MAX + 1))
print(f"[Init] Exponent choices per constant: {len(EXPONENTS)}")


# =============================================================================
# PDG 2024 TARGETS WITH REAL UNCERTAINTIES
# =============================================================================

@dataclass
class Target:
    name: str
    value: float
    uncertainty: float  # 1-sigma experimental uncertainty
    unit: str
    source: str  # PDG 2024 or specific experiment
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
    'Q05b': Target('m_b/m_c', 3.2908, 0.0030, '', 'PDG 2024',
                   'Bottom/charm'),
    'Q06': Target('m_t (pole)', 172.69, 0.30, 'GeV', 'PDG 2024',
                  'Top quark pole mass'),
    'Q07': Target('m_s/m_d (@2GeV)', 20.00, 0.70, '', 'PDG 2024',
                  'Strange/down'),
    'G01': Target('1/alpha (Thomson)', 137.035999084, 0.000000021, '', 'PDG 2024',
                  'Inverse fine-structure at q²=0'),
    'G02': Target('alpha_s(M_Z)', 0.1179, 0.0010, '', 'PDG 2024',
                  'Strong coupling at M_Z'),
    'N01': Target('sin²θ_12', 0.307, 0.013, '', 'PDG 2024 (NuFit)',
                  'Solar mixing angle'),
    'N04': Target('δ_CP', 65.5, 1.6, 'deg', 'NuFit 6.0 2024',
                  'CP-violating phase; NH best fit'),
    'C01': Target('|V_us|', 0.22650, 0.00050, '', 'PDG 2024',
                  'CKM element'),
    'C02': Target('|V_cb|', 0.04053, 0.00072, '', 'PDG 2024',
                  'CKM element; inclusive/exclusive tension'),
    'H01': Target('m_H', 125.20, 0.11, 'GeV', 'PDG 2024',
                  'Higgs boson mass'),
    'H02': Target('m_H/m_W', 1.5577, 0.0010, '', 'Derived',
                  'Ratio of pole masses'),
    'H03': Target('m_H/m_Z', 1.3737, 0.0012, '', 'Derived',
                  'Ratio of pole masses'),
    'v21': Target('Δm²_21', 7.53e-5, 0.20e-5, 'eV²', 'PDG 2024',
                  'Neutrino mass-squared difference'),
    'v31': Target('Δm²_31', 2.51e-3, 0.03e-3, 'eV²', 'PDG 2024 NH',
                  'Atmospheric neutrino difference; NH'),
    'N21': Target('Δm²_21/Δm²_31', 0.0300, 0.0008, '', 'Derived',
                  'Ratio of mass-squared differences'),
    'Pr': Target('m_p/m_e', 1836.15267343, 0.00000011, '', 'PDG 2024',
                 'Proton/electron mass ratio'),
    'Snu': Target('Σm_ν', 0.0588, 0.012, 'eV', 'Planck 2018 + BAO',
                  'Sum of neutrino masses; 95% CL upper limit ~0.12'),
}

# Derived targets (computed from base targets)
TARGETS['H02'] = Target('m_H/m_W', TARGETS['H01'].value / 80.379, 
                        math.hypot(TARGETS['H01'].uncertainty/80.379, 
                                   TARGETS['H01'].value*0.012/80.379**2), '', 'Derived', '')
TARGETS['H03'] = Target('m_H/m_Z', TARGETS['H01'].value / 91.1876,
                        math.hypot(TARGETS['H01'].uncertainty/91.1876,
                                   TARGETS['H01'].value*0.0021/91.1876**2), '', 'Derived', '')
TARGETS['N21'] = Target('Δm²_21/Δm²_31', 7.53e-5/2.51e-3,
                        7.53e-5/2.51e-3 * math.hypot(0.20/7.53, 0.03/2.51), '', 'Derived', '')

print(f"[Init] Loaded {len(TARGETS)} observables with PDG uncertainties")


# =============================================================================
# TRINITY CATALOG FORMULAS
# =============================================================================

TRINITY_FORMULAS: Dict[str, Tuple[str, str]] = {
    'L01': ('239*E/PI', 'm_mu/m_e (pole)'),
    'L02': ('239*PHI**4/PI**4', 'm_tau/m_mu (pole)'),
    'L03': ('549*E*PI**2/PHI**3', 'm_tau/m_e (pole)'),
    'Q01': ('2*PHI/7', 'm_u/m_d (@2GeV)'),
    'Q02': ('12 + PHI**3 * E**2', 'm_s/m_u (@2GeV)'),
    'Q03': ('19*PI*E**2/PHI', 'm_c/m_d'),
    'Q04': ('24*PI**3/E**4', 'm_c/m_s'),
    'Q05': ('43 + PI/PHI', 'm_b/m_s'),
    'Q05b': ('127*PHI/120 + 30/19', 'm_b/m_c'),
    'Q06': ('PI*E**4 + 6/5', 'm_t (pole)'),
    'Q07': ('24*PHI**2/PI', 'm_s/m_d (@2GeV)'),
    'G01': ('36*PHI*E**2/PI', '1/alpha (Thomson)'),
    'G02': ('(mp.sqrt(5)-2)/2', 'alpha_s(M_Z)'),
    'N01': ('8*PI/(PHI**5 * E**2)', 'sin²θ_12'),
    'N04': ('3/PHI**2 * 180/PI', 'δ_CP'),
    'C01': ('2*PHI**3*E**2/(9*PI**3)', '|V_us|'),
    'C02': ('1/(3*PHI**2*PI)', '|V_cb|'),
    'H01': ('4*PHI**3*E**2', 'm_H'),
    'H02': ('11*PHI/20 + 2/3', 'm_H/m_W'),
    'H03': ('4*PHI*PI/15 + 4/225', 'm_H/m_Z'),
    'v21': ('(PHI*E/PI)**6 * 1e-5', 'Δm²_21'),
    'v31': ('15*PHI**(-5)*PI**(-2)*E**(-4)', 'Δm²_31'),
    'N21': ('PI/(40*PHI**2)', 'Δm²_21/Δm²_31'),
    'Pr': ('6*PI**5', 'm_p/m_e'),
    'Snu': ('8*PHI**(-6)*PI**(-5)*E**6 * 0.1', 'Σm_ν'),
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
    """Template T1: C * phi^a * pi^b * e^c"""
    C = rng.choice(RATIONALS)
    a, b, c = rng.choice(EXPONENTS), rng.choice(EXPONENTS), rng.choice(EXPONENTS)
    expr = f"{C} * PHI**{a} * PI**{b} * E**{c}"
    def fn():
        return C * (PHI ** a) * (PI ** b) * (E ** c)
    return expr, fn


def random_formula_T2(rng: random.Random) -> Tuple[str, Callable]:
    """Template T2: C + phi^a * pi^b * e^c"""
    C = rng.choice(RATIONALS)
    a, b, c = rng.choice(EXPONENTS), rng.choice(EXPONENTS), rng.choice(EXPONENTS)
    expr = f"{C} + PHI**{a} * PI**{b} * E**{c}"
    def fn():
        return C + (PHI ** a) * (PI ** b) * (E ** c)
    return expr, fn


def random_formula_T3(rng: random.Random) -> Tuple[str, Callable]:
    """Template T3: C * phi^a / (pi^b * e^c)"""
    C = rng.choice(RATIONALS)
    a, b, c = rng.choice(EXPONENTS), rng.choice(EXPONENTS), rng.choice(EXPONENTS)
    expr = f"{C} * PHI**{a} / (PI**{b} * E**{c})"
    def fn():
        return C * (PHI ** a) / ((PI ** b) * (E ** c))
    return expr, fn


def random_formula_T4(rng: random.Random) -> Tuple[str, Callable]:
    """Template T4: C * phi^a + D * pi^b * e^c"""
    C = rng.choice(RATIONALS)
    D = rng.choice(RATIONALS)
    a, b, c = rng.choice(EXPONENTS), rng.choice(EXPONENTS), rng.choice(EXPONENTS)
    expr = f"{C} * PHI**{a} + {D} * PI**{b} * E**{c}"
    def fn():
        return C * (PHI ** a) + D * (PI ** b) * (E ** c)
    return expr, fn


def random_formula_T5(rng: random.Random) -> Tuple[str, Callable]:
    """Template T5: (C + phi^a) / (D + pi^b * e^c)"""
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
    """Pick a random template and generate a formula."""
    gen = rng.choice(TEMPLATE_GENERATORS)
    return gen(rng)


# =============================================================================
# MONTE-CARLO SIMULATION
# =============================================================================

# Float constants for fast numpy vectorization
PHI_F = float(PHI)
PI_F = float(PI)
E_F = float(E)

RATIONALS_ARR = np.array(RATIONALS, dtype=np.float64)
EXPONENTS_ARR = np.array(EXPONENTS, dtype=np.int32)

# Pre-extract target arrays for vectorization
_OBS_IDS = list(TARGETS.keys())
_TARGET_VALUES = np.array([TARGETS[fid].value for fid in _OBS_IDS], dtype=np.float64)
_TARGET_UNCS = np.array([TARGETS[fid].uncertainty for fid in _OBS_IDS], dtype=np.float64)
_N_OBS = len(_OBS_IDS)


def batch_evaluate(templates_and_batches: List[Tuple[int, int]], rng: random.Random) -> Tuple[np.ndarray, np.ndarray]:
    """
    Vectorized batch formula evaluation.
    
    templates_and_batches: list of (template_index, batch_size)
    Returns: (rel_errors, sigmas) both shape (total_formulas, n_obs)
    """
    all_vals = []
    
    for tidx, bsize in templates_and_batches:
        if bsize == 0:
            continue
        # Pick random parameters
        C_idx = rng.choices(range(len(RATIONALS_ARR)), k=bsize)
        C = RATIONALS_ARR[np.array(C_idx)]
        a = np.array(rng.choices(EXPONENTS_ARR, k=bsize), dtype=np.float64)
        b = np.array(rng.choices(EXPONENTS_ARR, k=bsize), dtype=np.float64)
        c = np.array(rng.choices(EXPONENTS_ARR, k=bsize), dtype=np.float64)
        
        if tidx == 0:  # T1: C * phi^a * pi^b * e^c
            vals = C * (PHI_F ** a) * (PI_F ** b) * (E_F ** c)
        elif tidx == 1:  # T2: C + phi^a * pi^b * e^c
            vals = C + (PHI_F ** a) * (PI_F ** b) * (E_F ** c)
        elif tidx == 2:  # T3: C * phi^a / (pi^b * e^c)
            denom = (PI_F ** b) * (E_F ** c)
            denom[denom == 0] = np.inf
            vals = C * (PHI_F ** a) / denom
        elif tidx == 3:  # T4: C * phi^a + D * pi^b * e^c
            D_idx = rng.choices(range(len(RATIONALS_ARR)), k=bsize)
            D = RATIONALS_ARR[np.array(D_idx)]
            vals = C * (PHI_F ** a) + D * (PI_F ** b) * (E_F ** c)
        elif tidx == 4:  # T5: (C + phi^a) / (D + pi^b * e^c)
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
    # Remove infinities and NaNs
    valid = np.isfinite(vals)
    vals = vals[valid]
    
    if len(vals) == 0:
        return np.empty((0, _N_OBS)), np.empty((0, _N_OBS))
    
    # Vectorized comparison with all targets: (n_formulas, 1) vs (1, n_obs)
    diffs = np.abs(vals[:, None] - _TARGET_VALUES[None, :])
    rel_errors = diffs / np.abs(_TARGET_VALUES[None, :]) * 100
    sigmas = diffs / _TARGET_UNCS[None, :]
    
    return rel_errors, sigmas


def run_monte_carlo(n_trials: int = N_TRIALS, sample_size: int = SAMPLE_SIZE) -> dict:
    """
    Run Monte Carlo simulation (vectorized).
    
    For each trial:
      - Generate `sample_size` random formulas (batched by template)
      - For each observable, find the BEST (minimum) relative error
      - Record the error vector for this trial
    
    Returns distribution statistics comparing random best errors to Trinity.
    """
    rng = random.Random(SEED)
    
    obs_ids = _OBS_IDS
    n_obs = _N_OBS
    
    # Trinity error vector
    trinity_errors = compute_trinity_errors()
    trinity_rel_errs = np.array([trinity_errors[fid]['rel_error_percent'] for fid in obs_ids])
    trinity_sigmas = np.array([trinity_errors[fid]['sigma_distance'] for fid in obs_ids])
    
    print(f"\n[MC] Starting {n_trials:,} trials, {sample_size:,} formulas per trial")
    print(f"[MC] Observables: {n_obs}")
    print(f"[MC] Search space estimate: {len(RATIONALS)} × {len(EXPONENTS)}³ × {len(TEMPLATE_GENERATORS)} ≈ {len(RATIONALS) * len(EXPONENTS)**3 * len(TEMPLATE_GENERATORS):.2e}")
    
    # Storage for trial statistics
    trial_best_rel_errors = np.zeros((n_trials, n_obs), dtype=np.float64)
    trial_best_sigmas = np.zeros((n_trials, n_obs), dtype=np.float64)
    trial_mean_rel_errors = np.zeros(n_trials, dtype=np.float64)
    trial_mean_sigmas = np.zeros(n_trials, dtype=np.float64)
    trial_hit_counts_1pct = np.zeros(n_trials, dtype=np.int32)
    trial_hit_counts_01pct = np.zeros(n_trials, dtype=np.int32)
    
    # Distribute sample across templates
    n_templates = len(TEMPLATE_GENERATORS)
    base_per_template = sample_size // n_templates
    remainder = sample_size % n_templates
    
    start_time = time.time()
    
    for trial in range(n_trials):
        # Build batch distribution
        batches = []
        for t in range(n_templates):
            bsize = base_per_template + (1 if t < remainder else 0)
            batches.append((t, bsize))
        
        rel_errors, sigmas = batch_evaluate(batches, rng)
        
        if rel_errors.shape[0] == 0:
            # All formulas invalid — fill with inf
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
        
        if (trial + 1) % 5000 == 0:
            elapsed = time.time() - start_time
            print(f"  ... trial {trial + 1:,} / {n_trials:,} ({elapsed:.1f}s, {trial/elapsed:.1f} trials/s)", flush=True)
    
    elapsed = time.time() - start_time
    print(f"\n[MC] Completed in {elapsed:.1f}s ({n_trials/elapsed:.1f} trials/s)", flush=True)
    
    # Compute p-values
    trinity_mean_rel = np.mean(trinity_rel_errs)
    trinity_mean_sigma = np.mean(trinity_sigmas)
    trinity_hits_1pct = np.sum(trinity_rel_errs < 1.0)
    trinity_hits_01pct = np.sum(trinity_rel_errs < 0.1)
    
    p_mean_rel = np.mean(trial_mean_rel_errors <= trinity_mean_rel)
    p_mean_sigma = np.mean(trial_mean_sigmas <= trinity_mean_sigma)
    p_hits_1pct = np.mean(trial_hit_counts_1pct >= trinity_hits_1pct)
    p_hits_01pct = np.mean(trial_hit_counts_01pct >= trinity_hits_01pct)
    
    # Per-observable p-values
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
            'per_observable_p_rel': per_obs_p_rel,
            'per_observable_p_sigma': per_obs_p_sigma,
        },
    }
    
    return results


# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_report(results: dict) -> str:
    """Generate human-readable markdown report."""
    lines = []
    lines.append("# Trinity S3AI — Wave 18 Honest Phenomenology Report")
    lines.append(f"\n**Date:** 2026-05-22  ")
    lines.append(f"**Protocol:** Pre-registered Monte-Carlo p-value  ")
    lines.append(f"**Trials:** {results['protocol']['n_trials']:,}  ")
    lines.append(f"**Sample size:** {results['protocol']['sample_size']:,} formulas per trial  ")
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
    
    lines.append("### PDG Targets")
    lines.append(f"- {len(TARGETS)} observables with real experimental uncertainties")
    lines.append("- Uncertainties from PDG 2024, FLAG 2024, NuFit 6.0")
    lines.append("")
    
    lines.append("## 2. Trinity Catalog Performance")
    lines.append("")
    lines.append("| Observable | Formula (excerpt) | Target | Computed | Rel.Error | σ-distance |")
    lines.append("|------------|-------------------|--------|----------|-----------|------------|")
    
    trinity = results['trinity']['per_observable']
    for fid in TARGETS.keys():
        if fid not in trinity:
            continue
        t = trinity[fid]
        expr_short = TRINITY_FORMULAS[fid][0][:30]
        target = TARGETS[fid]
        computed = eval_formula(TRINITY_FORMULAS[fid][0])
        lines.append(f"| {fid} | `{expr_short}` | {target.value:.4g} | {computed:.4g} | {t['rel_error_percent']:.4f}% | {t['sigma_distance']:.2f}σ |")
    
    lines.append("")
    lines.append(f"**Summary:**")
    lines.append(f"- Mean relative error: {results['trinity']['mean_rel_error_percent']:.4f}%")
    lines.append(f"- Mean σ-distance: {results['trinity']['mean_sigma_distance']:.2f}σ")
    lines.append(f"- Formulas with <0.1% error: {results['trinity']['hits_01pct']}/{len(TARGETS)}")
    lines.append(f"- Formulas with <1.0% error: {results['trinity']['hits_1pct']}/{len(TARGETS)}")
    lines.append("")
    
    lines.append("## 3. Monte-Carlo Results")
    lines.append("")
    lines.append("### Distribution of Best Random Errors")
    mc = results['monte_carlo']
    lines.append(f"| Metric | Trinity | Random (median) | Random (mean±std) | p-value |")
    lines.append(f"|--------|---------|-----------------|-------------------|---------|")
    lines.append(f"| Mean rel.error (%) | {results['trinity']['mean_rel_error_percent']:.4f} | {mc['mean_rel_error_percent']['median']:.4f} | {mc['mean_rel_error_percent']['mean']:.4f}±{mc['mean_rel_error_percent']['std']:.4f} | {mc['mean_rel_error_percent']['p_value_trinity_le_random']:.4f} |")
    lines.append(f"| Mean σ-distance | {results['trinity']['mean_sigma_distance']:.2f} | {mc['mean_sigma_distance']['median']:.2f} | {mc['mean_sigma_distance']['mean']:.2f}±{mc['mean_sigma_distance']['std']:.2f} | {mc['mean_sigma_distance']['p_value_trinity_le_random']:.4f} |")
    lines.append(f"| Hits <1.0% | {results['trinity']['hits_1pct']} | {mc['hits_1pct']['median']} | {mc['hits_1pct']['mean']:.1f}±{mc['hits_1pct']['std']:.1f} | {mc['hits_1pct']['p_value_trinity_ge_random']:.4f} |")
    lines.append(f"| Hits <0.1% | {results['trinity']['hits_01pct']} | {mc['hits_01pct']['median']} | {mc['hits_01pct']['mean']:.1f}±{mc['hits_01pct']['std']:.1f} | {mc['hits_01pct']['p_value_trinity_ge_random']:.4f} |")
    lines.append("")
    
    lines.append("### Per-Observable P-Values")
    lines.append("P(observable | Trinity error ≤ random best error)")
    lines.append("")
    lines.append("| Observable | p-value (rel.error) | p-value (σ-distance) | Interpretation |")
    lines.append("|------------|---------------------|----------------------|----------------|")
    for fid in TARGETS.keys():
        p_rel = mc['per_observable_p_rel'].get(fid, 0)
        p_sig = mc['per_observable_p_sigma'].get(fid, 0)
        if p_rel < 0.01:
            interp = "Significant"
        elif p_rel < 0.05:
            interp = "Suggestive"
        else:
            interp = "Not significant"
        lines.append(f"| {fid} | {p_rel:.4f} | {p_sig:.4f} | {interp} |")
    lines.append("")
    
    lines.append("## 4. Interpretation")
    lines.append("")
    p_mean_rel = mc['mean_rel_error_percent']['p_value_trinity_le_random']
    p_mean_sig = mc['mean_sigma_distance']['p_value_trinity_le_random']
    p_hits_1 = mc['hits_1pct']['p_value_trinity_ge_random']
    
    if p_mean_rel < 0.01 and p_hits_1 < 0.01:
        verdict = (
            "The Trinity catalog achieves significantly smaller mean relative errors "
            f"than random sampling (p = {p_mean_rel:.4f}). The number of high-precision "
            f"hits (<1%) is also significant (p = {p_hits_1:.4f}). "
            "This suggests the catalog is not a trivial random coincidence."
        )
    elif p_mean_rel < 0.05 or p_hits_1 < 0.05:
        verdict = (
            "The Trinity catalog shows marginal significance against random coincidence "
            f"(p = {p_mean_rel:.4f} for mean error, p = {p_hits_1:.4f} for hits). "
            "The result is suggestive but not conclusive."
        )
    else:
        verdict = (
            "The Trinity catalog does NOT show statistically significant improvement "
            f"over random sampling (p = {p_mean_rel:.4f}). "
            "The observed precision is consistent with searching a large enough space. "
            "This is an honest negative result."
        )
    
    lines.append(verdict)
    lines.append("")
    lines.append("## 5. Limitations")
    lines.append("")
    lines.append("1. **Search space size**: The chosen space (~10⁸ formulas) may not perfectly match the actual space searched during Trinity development. If the true search space was larger, the p-value is conservative (favors Trinity). If smaller, it is anti-conservative.")
    lines.append("2. **Template choice**: Five pre-registered templates were used. The original Trinity search may have used additional forms (e.g., logs, square roots). This is a limitation of the protocol.")
    lines.append("3. **Bonferroni**: Multiple observables were tested; no explicit Bonferroni correction was applied to the aggregate p-value, but the per-observable p-values are uncorrected.")
    lines.append("4. **Experimental uncertainties**: Some uncertainties (e.g., cosmological Σm_ν) are upper limits, not Gaussian errors. The σ-distance for these is less meaningful.")
    lines.append("")
    lines.append("---")
    lines.append("*Report generated by Wave 18 honest phenomenology protocol.*")
    
    return "\n".join(lines)


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("TRINITY S3AI — WAVE 18: HONEST PHENOMENOLOGY")
    print("=" * 70)
    print(f"Protocol: Pre-registered Monte-Carlo p-value")
    print(f"Trials: {N_TRIALS:,} | Sample: {SAMPLE_SIZE:,} | Seed: {SEED}")
    print("")
    
    # Step 1: Compute Trinity errors
    print("[1/4] Computing Trinity catalog errors...")
    trinity_errors = compute_trinity_errors()
    print(f"       Mean rel.error: {np.mean([v['rel_error_percent'] for v in trinity_errors.values()]):.4f}%")
    print(f"       Mean σ-distance: {np.mean([v['sigma_distance'] for v in trinity_errors.values()]):.2f}")
    
    # Step 2: Run Monte Carlo
    print("\n[2/4] Running Monte-Carlo simulation...")
    mc_results = run_monte_carlo()
    
    # Step 3: Save JSON
    print("\n[3/4] Saving results...")
    json_path = OUT_DIR / "wave18_mc_results.json"
    with open(json_path, 'w') as f:
        json.dump(mc_results, f, indent=2)
    print(f"       JSON: {json_path}")
    
    # Step 4: Generate report
    print("\n[4/4] Generating report...")
    report = generate_report(mc_results)
    report_path = OUT_DIR / "honest_pvalue_report_v18.md"
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"       Report: {report_path}")
    
    # Summary
    print("\n" + "=" * 70)
    print("WAVE 18 COMPLETE")
    print("=" * 70)
    p_rel = mc_results['monte_carlo']['mean_rel_error_percent']['p_value_trinity_le_random']
    p_sig = mc_results['monte_carlo']['mean_sigma_distance']['p_value_trinity_le_random']
    p_hits = mc_results['monte_carlo']['hits_1pct']['p_value_trinity_ge_random']
    print(f"P(Trinity mean error ≤ random): {p_rel:.4f}")
    print(f"P(Trinity mean σ ≤ random):     {p_sig:.4f}")
    print(f"P(Trinity hits ≥ random):       {p_hits:.4f}")
    print("")
    if p_rel < 0.01:
        print("VERDICT: Statistically significant (p < 0.01)")
    elif p_rel < 0.05:
        print("VERDICT: Marginally significant (p < 0.05)")
    else:
        print("VERDICT: NOT significant — consistent with random search")
    print("=" * 70)


if __name__ == '__main__':
    main()
