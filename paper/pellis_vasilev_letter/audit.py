#!/usr/bin/env python3
"""
Independent 50-digit numerical audit for the Vasilev-Pellis-Olsen short paper
"A Constrained Symbolic Search for phi-Structured Physical Constants".

Every relative deviation printed in the paper's tables is recomputed here from
scratch with mpmath at dps=50 against the central (measured/CODATA/PDG) value.

This script is an AUDIT, not a derivation. A small relative deviation is NOT
evidence of physical structure: see the look-elsewhere caveat at the bottom and
the anti-circularity note on delta_CP.

Run:  python3 audit.py
Requires: mpmath (pip install mpmath)
"""
from mpmath import mp, mpf, sqrt, pi, e, power

mp.dps = 50  # 50 significant digits

phi = (1 + sqrt(5)) / 2  # golden ratio


def reldev(formula, target):
    """Relative deviation |formula - target| / |target|, at dps=50."""
    return abs(formula - target) / abs(target)


def show(label, formula, target, note=""):
    d = reldev(formula, target)
    print(f"{label:<28} value={mp.nstr(formula, 15):<20} "
          f"target={mp.nstr(target, 15):<20} reldev={mp.nstr(d, 4):<12} {note}")
    return d


print("=" * 100)
print("Vasilev-Pellis-Olsen audit  |  mpmath dps =", mp.dps)
print("=" * 100)

# --- alpha^-1 (fine-structure constant inverse) ---------------------------
# Central value: CODATA / PDG  alpha^-1 = 137.035999177(21)
alpha_inv = mpf("137.035999177")

# Pellis anchor (Strand III): 360 phi^-2 - 2 phi^-3 + (3 phi)^-5
anchor = 360 * phi**-2 - 2 * phi**-3 + power(3 * phi, -5)
show("alpha^-1 Pellis anchor", anchor, alpha_inv, "(3-term)")

# Monotone error chain of the anchor (term by term):
t1 = 360 * phi**-2
t2 = t1 - 2 * phi**-3
show("  term1: 360 phi^-2", t1, alpha_inv, "(golden angle in deg)")
show("  +term2", t2, alpha_inv)
show("  +term3 (full)", anchor, alpha_inv)

# Compact single-formula fit (Vasilev grammar): 36 pi^-1 phi e^2
compact = 36 * pi**-1 * phi * e**2
show("alpha^-1 compact fit", compact, alpha_inv, "(36 pi^-1 phi e^2)")

# --- alpha_s(m_Z) strong coupling -----------------------------------------
# Central value: PDG alpha_s(m_Z) = 0.11800(9)
alpha_s = mpf("0.11800")
alpha_phi = mpf("0.5") * phi**-3  # = 1/2 (sqrt5 - 2)
show("alpha_s ~ alpha_phi", alpha_phi, alpha_s, "(1/2 phi^-3)")

# --- mu = m_p/m_e leading Fibonacci-Lucas term ----------------------------
# Central value mu = 1836.15267343(11). Leading term is schematic only.
mu = mpf("1836.15267343")
mu_lead = phi**16 / sqrt(5)  # Binet: F_16 ~ phi^16 / sqrt5
show("mu leading phi^16/sqrt5", mu_lead, mu, "(schematic, large dev expected)")
print("  identity check phi^16/sqrt5 ~ F_16 = 987:",
      mp.nstr(mu_lead, 8), "(F_8*L_8 = 21*47 = 987)")

# --- delta_CP (PMNS CP phase) -- ANTI-CIRCULARITY CASE --------------------
# The formula 8 pi^3 / (9 e^2). The paper's table once listed target 3.73 rad,
# which is the formula's OWN output -> circular. The REAL measured value is
# ~197 deg = ~3.44 rad (PDG 2024). We audit against the MEASURED value.
delta_formula = 8 * pi**3 / (9 * e**2)
delta_measured = mpf("3.44")  # ~197 deg, PDG 2024 central
print("-" * 100)
print("delta_CP ANTI-CIRCULARITY check:")
print("  formula 8 pi^3/(9 e^2) =", mp.nstr(delta_formula, 8), "rad =",
      mp.nstr(delta_formula * 180 / pi, 6), "deg")
print("  vs MEASURED ~3.44 rad (197 deg): reldev =",
      mp.nstr(reldev(delta_formula, delta_measured), 4),
      "  <-- the honest ~8% gap; the 3.73-rad self-match is circular and RETRACTED")

# --- hypothesis-class cardinality |S(C)| ~ (2/3) C^4 ----------------------
print("-" * 100)
print("Hypothesis-class cardinality (signed exponent lattice):")
for C, expected in [(3, 129), (4, 321), (10, 8361)]:
    approx = mpf(2) / 3 * C**4
    print(f"  |S({C})| reported = {expected:<6} (2/3)C^4 approx = {mp.nstr(approx,6)}")

print("=" * 100)
print("CAVEAT: A small relative deviation is NOT a proof of structure. With")
print("|S(C)| candidate expressions and the look-elsewhere effect (15 of 128,400")
print("phi-forms with ||theta||_1<=4, n<=400 land within 3e-4 of alpha^-1), finding")
print("SOME phi-form near a target is expected, not surprising. This audit only")
print("confirms the arithmetic of each printed deviation, nothing more.")
print("=" * 100)
