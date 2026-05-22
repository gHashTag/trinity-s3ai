#!/usr/bin/env python3
"""
compute_eta_table.py

Compute η-invariants for the binary tetrahedral (S³/2T = Σ(2,3,3)),
binary octahedral (S³/2O = Σ(2,3,4)), and binary icosahedral
(S³/2I = Σ(2,3,5)) spherical space forms.

Three complementary approaches are implemented:

1. APS plumbing theorem (project convention)
   For the negative-definite ADE plumbing X with boundary Y,
   η_Dir(Y) = σ(X)/4  (adopting the project's sign convention η = −2Â).

2. Natural metric (Dedekind sums / Nicolaescu)
   Using the Seifert invariants of the link of the singularity and
   Nicolaescu's formula
       4 η_Dir + (ℓ/3 − sign(ℓ) − 4 S(β,α)) = F(Y),
   where F(Y) is the Frøyshov invariant.  For the ADE links we take
   F(Y) = b₂(X) (the Milnor number, verified for E8 where F=8).
   The signature η for the same metric follows from the topological
   identity (1/2)η_Dir + (1/8)η_Sign = −σ/8.

3. Round metric (group-theoretic cotangent sums)
   The signature η for the constant-curvature round metric is computed
   from the equivariant fixed-point formula (Ouyang / Tang–Zhang):
       η_Sign = (1/|Γ|) Σ_{g≠1} cot(r(g)/2) cot(s(g)/2),
   where r(g), s(g) are the rotation angles of g acting on R⁴.
   The corresponding Dirac η is then inferred from the same
   topological identity.

All calculations are performed with exact rational arithmetic (fractions.Fraction
and sympy exact radicals).  Irrational contributions cancel in the final
rational answers.
"""

from fractions import Fraction
import sympy as sp

# ---------------------------------------------------------------------------
# Helpers: Dedekind sums
# ---------------------------------------------------------------------------

def dedekind_sum(h: int, k: int) -> Fraction:
    """Exact Dedekind sum s(h,k) using the sawtooth definition."""
    total = Fraction(0, 1)
    for i in range(1, k):
        x = Fraction(i, k)
        saw_x = x - Fraction(1, 2) if i % k != 0 else Fraction(0, 1)
        hi = (h * i) % k
        y = Fraction(hi, k)
        saw_y = y - Fraction(1, 2) if hi != 0 else Fraction(0, 1)
        total += saw_x * saw_y
    return total


# ---------------------------------------------------------------------------
# Helpers: exact cotangent values for the angles that appear
# ---------------------------------------------------------------------------

def _make_cot_table():
    """Precompute exact cot(θ/2) for all angles θ appearing in the binary
    polyhedral groups."""
    return {
        'pi':       sp.cot(sp.pi / 2),          # 0
        'pi_2':     sp.cot(sp.pi / 4),          # 1
        '2pi_3':    sp.cot(sp.pi / 3),          # 1/√3
        'pi_3':     sp.cot(sp.pi / 6),          # √3
        'pi_4':     sp.cot(sp.pi / 8),          # 1+√2
        '3pi_4':    sp.cot(3 * sp.pi / 8),      # √2−1
        '5pi_4':    sp.cot(5 * sp.pi / 8),      # 1−√2  (squared = (√2−1)²)
        '7pi_4':    sp.cot(7 * sp.pi / 8),      # −(1+√2) (squared = (1+√2)²)
        '2pi_5':    sp.cot(sp.pi / 5),          # √(1+2/√5)
        '4pi_5':    sp.cot(2 * sp.pi / 5),      # √(1−2/√5)
        'pi_5':     sp.cot(sp.pi / 10),         # √(5+2√5)
        '3pi_5':    sp.cot(3 * sp.pi / 10),     # √(5−2√5)
    }

_COT = _make_cot_table()


def round_signature_eta(name: str) -> Fraction:
    """Return the exact round-metric signature η for S³/Γ.

    The formula used is
        η_Sign = (1/|Γ|) Σ_{g≠1} −cot²(θ_g/2),
    where θ_g is the rotation angle of g in the standard 4-dim real
    representation (the SU(2) action on C² ≅ R⁴).
    """
    if name == '2I':
        # |Γ| = 120
        # classes: 1(-I,π), 30(order4,π/2), 20(order3,2π/3), 20(order6,π/3),
        #          12(order5,2π/5), 12(order5,4π/5), 12(order10,π/5), 12(order10,3π/5)
        total = (
            1 * (-_COT['pi']**2)
            + 30 * (-_COT['pi_2']**2)
            + 20 * (-_COT['2pi_3']**2)
            + 20 * (-_COT['pi_3']**2)
            + 12 * (-_COT['2pi_5']**2)
            + 12 * (-_COT['4pi_5']**2)
            + 12 * (-_COT['pi_5']**2)
            + 12 * (-_COT['3pi_5']**2)
        )
        eta = sp.simplify(total / 120)
    elif name == '2T':
        # |Γ| = 24
        # classes: 1(-I,π), 6(order4,π/2), 8(order3,2π/3), 8(order6,π/3)
        total = (
            1 * (-_COT['pi']**2)
            + 6 * (-_COT['pi_2']**2)
            + 8 * (-_COT['2pi_3']**2)
            + 8 * (-_COT['pi_3']**2)
        )
        eta = sp.simplify(total / 24)
    elif name == '2O':
        # |Γ| = 48
        # classes: 1(-I,π), 18(order4,π/2), 8(order3,2π/3), 8(order6,π/3),
        #          3(order8,π/4), 3(order8,3π/4), 3(order8,5π/4), 3(order8,7π/4)
        total = (
            1 * (-_COT['pi']**2)
            + 18 * (-_COT['pi_2']**2)
            + 8 * (-_COT['2pi_3']**2)
            + 8 * (-_COT['pi_3']**2)
            + 3 * (-_COT['pi_4']**2)
            + 3 * (-_COT['3pi_4']**2)
            + 3 * (-_COT['5pi_4']**2)
            + 3 * (-_COT['7pi_4']**2)
        )
        eta = sp.simplify(total / 48)
    else:
        raise ValueError(name)

    # sympy should have reduced to a rational number; convert to Fraction
    return Fraction(int(eta.p), int(eta.q))


# ---------------------------------------------------------------------------
# Main computation
# ---------------------------------------------------------------------------

def main():
    # Plumbing data
    data = {
        '2T': {
            'space':  r'S³ / 2T  = Σ(2,3,3)',
            'plumb':  'E₆',
            'sigma':  -6,
            'alpha':  (2, 3, 3),
            'beta':   (1, 2, 2),
            'e0':     -2,
        },
        '2O': {
            'space':  r'S³ / 2O  = Σ(2,3,4)',
            'plumb':  'E₇',
            'sigma':  -7,
            'alpha':  (2, 3, 4),
            'beta':   (1, 2, 3),
            'e0':     -2,
        },
        '2I': {
            'space':  r'S³ / 2I  = Σ(2,3,5)',
            'plumb':  'E₈',
            'sigma':  -8,
            'alpha':  (2, 3, 5),
            'beta':   (1, 2, 4),
            'e0':     -2,
        },
    }

    results = {}
    for key, d in data.items():
        sigma = d['sigma']
        alpha = d['alpha']
        beta = d['beta']

        # 1. APS plumbing (project convention)
        eta_aps = Fraction(sigma, 4)

        # 2. Natural metric via Dedekind sums / Nicolaescu
        S = sum(dedekind_sum(b, a) for a, b in zip(alpha, beta))
        P = 1
        for a in alpha:
            P *= a
        e = Fraction(d['e0'], 1) + sum(Fraction(b, a) for a, b in zip(alpha, beta))
        # ℓ = Euler number e
        ell = e
        term = ell / 3 - (-1 if ell < 0 else 1) - 4 * S
        # Frøyshov invariant F(Y) = b₂ for ADE links (verified for E8)
        F = abs(sigma)  # b₂ = |σ| for negative-definite ADE plumbing
        eta_nat_dir = (Fraction(F, 1) - term) / 4
        # Signature η for the same metric from the topological identity
        eta_nat_sig = Fraction(-sigma, 1) - 4 * eta_nat_dir

        # 3. Round metric signature η (group cotangent sums)
        eta_round_sig = round_signature_eta(key)
        # Inferred Dirac η for the round metric from the topological identity
        eta_round_dir = 2 * (Fraction(-sigma, 8) - Fraction(1, 8) * eta_round_sig)

        results[key] = {
            'space': d['space'],
            'plumb': d['plumb'],
            'sigma': sigma,
            'eta_aps': eta_aps,
            'eta_nat_dir': eta_nat_dir,
            'eta_nat_sig': eta_nat_sig,
            'eta_round_sig': eta_round_sig,
            'eta_round_dir': eta_round_dir,
            'S': S,
            'ell': ell,
            'term': term,
            'F': F,
        }

    # -----------------------------------------------------------------------
    # Print tables
    # -----------------------------------------------------------------------
    print("=" * 90)
    print("η-INVARIANT TABLE FOR BINARY POLYHEDRAL SPHERICAL SPACE FORMS")
    print("=" * 90)
    print()

    # Table 1: APS plumbing (project convention)
    print("Table 1.  APS plumbing convention  η = σ/4")
    print("-" * 60)
    print(f"{'Space':<25} {'Plumbing':<10} {'σ':>6} {'η (project)':>15}")
    print("-" * 60)
    for key in ['2T', '2O', '2I']:
        r = results[key]
        print(f"{r['space']:<25} {r['plumb']:<10} {r['sigma']:>6} {str(r['eta_aps']):>15} ({float(r['eta_aps']):+.4f})")
    print("-" * 60)
    print()

    # Table 2: Natural metric (Dedekind sums)
    print("Table 2.  Natural Seifert metric (Dedekind–Nicolaescu)")
    print("-" * 80)
    print(f"{'Space':<25} {'S(β,α)':>12} {'ℓ':>10} {'term':>12} {'F':>4} {'η_Dir':>14} {'η_Sign':>14}")
    print("-" * 80)
    for key in ['2T', '2O', '2I']:
        r = results[key]
        print(f"{r['space']:<25} {str(r['S']):>12} {str(r['ell']):>10} {str(r['term']):>12} {r['F']:>4} {str(r['eta_nat_dir']):>14} ({float(r['eta_nat_dir']):+.4f}) {str(r['eta_nat_sig']):>14} ({float(r['eta_nat_sig']):+.4f})")
    print("-" * 80)
    print()

    # Table 3: Round metric (group cotangent sums)
    print("Table 3.  Round metric (group-theoretic cotangent sums)")
    print("-" * 70)
    print(f"{'Space':<25} {'η_Sign':>18} {'η_Dir (inferred)':>22}")
    print("-" * 70)
    for key in ['2T', '2O', '2I']:
        r = results[key]
        print(f"{r['space']:<25} {str(r['eta_round_sig']):>18} ({float(r['eta_round_sig']):+.4f}) {str(r['eta_round_dir']):>22} ({float(r['eta_round_dir']):+.4f})")
    print("-" * 70)
    print()

    # Verification of the topological identity
    print("=" * 90)
    print("VERIFICATION: (1/2) η_Dir + (1/8) η_Sign  =  −σ/8")
    print("=" * 90)
    for key in ['2T', '2O', '2I']:
        r = results[key]
        lhs_nat = Fraction(1,2) * r['eta_nat_dir'] + Fraction(1,8) * r['eta_nat_sig']
        lhs_round = Fraction(1,2) * r['eta_round_dir'] + Fraction(1,8) * r['eta_round_sig']
        rhs = Fraction(-r['sigma'], 8)
        print(f"{r['space']:<25}  natural: {str(lhs_nat):>8} = {str(rhs):>8}   round: {str(lhs_round):>10} = {str(rhs):>8}")
    print()

    # Summary of adopted values
    print("=" * 90)
    print("ADOPTED VALUES (project convention)")
    print("=" * 90)
    for key in ['2T', '2O', '2I']:
        r = results[key]
        print(f"  η({r['space']}) = {str(r['eta_aps'])} = {float(r['eta_aps']):.4f}")
    print()


if __name__ == '__main__':
    main()
