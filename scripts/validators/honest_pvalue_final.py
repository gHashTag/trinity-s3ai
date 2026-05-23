#!/usr/bin/env python3
"""
honest_pvalue_final.py
Honest Monte-Carlo p-value simulation for Trinity coefficient enumeration.
Computes exact search space, Monte-Carlo p-value with 95% CI, and analytical bounds.
"""

import math
import random
import sys
from itertools import combinations, product
from fractions import Fraction

# ============================================================================
# 1. EXACT SEARCH SPACE ENUMERATION
# ============================================================================

BASE = {1, 2, 7, 11, 12, 19, 20, 29, 30, 120, 240}
TARGET_SET = {1, 2, 3, 4, 8, 10, 14, 15, 18, 24, 36, 48, 92, 239, 549}
N_TARGET = len(TARGET_SET)

def enumerate_reachable():
    """
    Enumerate ALL values reachable from BASE using:
      - Binary: +, -, *, // (integer division)
      - Unary: square
    with complexity <= 3 operations.

    Complexity = number of operations in the expression tree.
    """
    # Level 0: base elements (0 operations)
    level = [set() for _ in range(4)]
    level[0] = set(BASE)

    all_reachable = set(BASE)

    # Build levels 1, 2, 3
    for c in range(1, 4):
        current = set()

        # Unary: square (complexity adds 1)
        for prev_c in range(c):
            for x in level[prev_c]:
                # square(x) has complexity prev_c + 1 = c, so prev_c = c - 1
                if prev_c == c - 1:
                    result = x * x
                    if 1 <= result <= 600:
                        current.add(result)

        # Binary operations: +, -, *, //
        # For complexity c, we need left_c + right_c + 1 = c
        # So left_c + right_c = c - 1, with left_c <= c-1, right_c <= c-1
        for left_c in range(c):
            right_c = c - 1 - left_c
            if right_c < 0 or right_c >= c:
                continue
            for a in level[left_c]:
                for b in level[right_c]:
                    # Addition
                    result = a + b
                    if 1 <= result <= 600:
                        current.add(result)

                    # Subtraction (a - b)
                    result = a - b
                    if 1 <= result <= 600:
                        current.add(result)

                    # Multiplication
                    result = a * b
                    if 1 <= result <= 600:
                        current.add(result)

                    # Integer division (a // b), b != 0
                    if b != 0:
                        result = a // b
                        if 1 <= result <= 600:
                            current.add(result)

        level[c] = current
        all_reachable.update(current)

    return all_reachable, level

print("=" * 70)
print("TRINITY V3.3 — HONEST MONTE-CARLO P-VALUE SIMULATION")
print("=" * 70)

# Enumerate
reachable, levels = enumerate_reachable()

print("\n--- SEARCH SPACE ENUMERATION ---")
print(f"Base invariants: {sorted(BASE)}")
print(f"Operations: +, -, *, //, square")
print(f"Complexity <= 3 operations")
print()
for i in range(4):
    print(f"  Level {i} (<= {i} ops): {len(levels[i])} unique values")
print(f"\n  UNION (all reachable 1-600): {len(reachable)} unique values")

reachable_sorted = sorted(reachable)
print(f"\n  Reachable values: {reachable_sorted}")

# Total generated count (including duplicates across levels)
total_generated = sum(len(levels[i]) for i in range(4))
print(f"\n  Total count (sum across levels): {total_generated}")
print(f"  Unique count: {len(reachable)}")

# Check target coverage
target_covered = TARGET_SET.issubset(reachable)
target_in_reachable = TARGET_SET.intersection(reachable)
target_missing = TARGET_SET - reachable
print(f"\n--- TARGET SET COVERAGE ---")
print(f"Target set: {sorted(TARGET_SET)}")
print(f"Target elements found in reachable: {len(target_in_reachable)} / {len(TARGET_SET)}")
print(f"Missing from reachable: {sorted(target_missing) if target_missing else 'NONE'}")
print(f"Full coverage: {target_covered}")


# ============================================================================
# 2. MONTE-CARLO SIMULATION (1,000,000 trials)
# ============================================================================

R = len(reachable)          # size of reachable set
N = 600                     # total universe
T = N_TARGET                # size of target set

def run_monte_carlo(n_trials, seed=42):
    """
    Randomly select T coefficients from the reachable set (without replacement).
    Check if they exactly match the target set.
    Returns: number of matches, elapsed time estimate.
    """
    rng = random.Random(seed)
    reachable_list = list(reachable)
    target_sorted = sorted(TARGET_SET)

    matches = 0
    for trial in range(n_trials):
        # Randomly select T elements from reachable without replacement
        selected = sorted(rng.sample(reachable_list, T))
        if selected == target_sorted:
            matches += 1

        # Progress report every 100k
        if (trial + 1) % 100000 == 0:
            print(f"    ... completed {trial + 1:,} trials, matches so far: {matches}")

    return matches

print("\n--- MONTE-CARLO SIMULATION ---")
print(f"Trials: 1,000,000")
print(f"Selection: {T} values without replacement from {R} reachable values")
print(f"Success criterion: selected set == target set")
print()

mc_matches = run_monte_carlo(1_000_000)
mc_pvalue = mc_matches / 1_000_000

# 95% CI for binomial proportion (Wilson interval)
n = 1_000_000
if mc_matches > 0:
    z = 1.96  # 95% confidence
    p = mc_pvalue
    ci_center = (p + z*z/(2*n)) / (1 + z*z/n)
    ci_width = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    ci_lower = max(0, ci_center - ci_width)
    ci_upper = ci_center + ci_width
else:
    # Rule of three for zero events
    ci_lower = 0.0
    ci_upper = 3.0 / n

print(f"\n  Monte-Carlo matches: {mc_matches} / 1,000,000")
print(f"  Empirical p-value: {mc_pvalue:.10e}")
if mc_matches > 0:
    print(f"  95% CI: [{ci_lower:.10e}, {ci_upper:.10e}]")
else:
    print(f"  95% CI (Rule of 3): [0, {ci_upper:.10e}]")

# ============================================================================
# 3. ANALYTICAL BOUNDS
# ============================================================================

print("\n--- ANALYTICAL BOUNDS ---")

# Exact combinatorial probability
# P(match) = 1 / C(R, T)  -- only ONE subset of size T matches exactly
def nCk(n, k):
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)

analytical_p = 1.0 / nCk(R, T)
print(f"  Reachable set size R = {R}")
print(f"  Target set size T = {T}")
print(f"  C({R}, {T}) = {nCk(R, T):,}")
print(f"  P(exact match | 1 family) = 1 / C({R}, {T}) = {analytical_p:.10e}")

# Full universe probability
universe_p = 1.0 / nCk(N, T)
print(f"\n  C({N}, {T}) = {nCk(N, T):,}")
print(f"  P(random T-subset of 1..{N} equals target) = {universe_p:.10e}")

# Bonferroni correction for 5 Coxeter families
N_FAMILIES = 5  # E6, E7, E8, F4, H4
bonferroni_p = N_FAMILIES * analytical_p
print(f"\n  Bonferroni x{N_FAMILIES} (families E6, E7, E8, F4, H4)")
print(f"  Conservative p-value = {N_FAMILIES} * {analytical_p:.10e} = {bonferroni_p:.10e}")

# ============================================================================
# 4. FORMATTED REPORT
# ============================================================================

report = f"""
{'='*70}
TRINITY V3.3 — HONEST P-VALUE ANALYSIS REPORT
{'='*70}

1. SEARCH SPACE ENUMERATION
   -------------------------
   Base invariants:     {sorted(BASE)}
   Operations:          +, -, *, //, square
   Complexity bound:    <= 3 operations

   Level 0 (0 ops):     {len(levels[0]):3d} values  ->  {sorted(levels[0])}
   Level 1 (1 op):      {len(levels[1]):3d} values  ->  {sorted(levels[1])}
   Level 2 (2 ops):     {len(levels[2]):3d} values  ->  {sorted(levels[2])}
   Level 3 (3 ops):     {len(levels[3]):3d} values  ->  {sorted(levels[3])}

   UNION (all reachable 1-600):  {len(reachable)} unique values

   Target set:          {sorted(TARGET_SET)}
   Target coverage:     {len(target_in_reachable)}/{len(TARGET_SET)} elements found
   Full coverage:       {'YES' if target_covered else 'NO — missing: ' + str(sorted(target_missing))}

2. MONTE-CARLO SIMULATION
   -----------------------
   Trials:              1,000,000
   Selection method:    {T} values without replacement from {R} reachable
   Matches:             {mc_matches}
   Empirical p-value:   {mc_pvalue:.10e}
   95% CI:              [{ci_lower:.10e}, {ci_upper:.10e}]

3. ANALYTICAL BOUNDS
   -----------------
   Reachable set size:  R = {R}
   Target size:         T = {T}
   C(R, T):             {nCk(R, T):,}

   P(exact match) = 1/C(R,T) = {analytical_p:.10e}
   P(universe)    = 1/C(600,{T}) = {universe_p:.10e}

   Bonferroni x{N_FAMILIES}:   {N_FAMILIES} * {analytical_p:.10e} = {bonferroni_p:.10e}

4. SUMMARY TABLE
   -------------
   +---------------------------+--------------------------+
   | Metric                    | Value                    |
   +---------------------------+--------------------------+
   | Unique reachable values   | {len(reachable):>24} |
   | Target set size           | {N_TARGET:>24} |
   | Target coverage           | {'YES' if target_covered else 'NO':>24} |
   | MC p-value (1M trials)    | {mc_pvalue:>24.10e} |
   | 95% CI lower              | {ci_lower:>24.10e} |
   | 95% CI upper              | {ci_upper:>24.10e} |
   | Analytical p-value        | {analytical_p:>24.10e} |
   | Conservative (Bonferroni) | {bonferroni_p:>24.10e} |
   +---------------------------+--------------------------+

5. INTERPRETATION
   --------------
   The probability of randomly selecting the exact Trinity target set from
   the {R} reachable values is {analytical_p:.2e}.

   After Bonferroni correction for testing {N_FAMILIES} Coxeter families
   (E6, E7, E8, F4, H4), the conservative p-value is {bonferroni_p:.2e}.

   This represents {'strong' if bonferroni_p < 0.01 else 'moderate' if bonferroni_p < 0.05 else 'no'} statistical evidence
   against the null hypothesis of random coincidence.

{'='*70}
"""

print(report)

# Save report to file
import os
report_dir = os.environ.get('TRINITY_OUTPUT_DIR', 'reports')
os.makedirs(report_dir, exist_ok=True)
report_path = os.path.join(report_dir, 'honest_pvalue_report.txt')
with open(report_path, 'w') as f:
    f.write(report)
print(f"Report saved to {report_path}")
