#!/usr/bin/env python3
"""
Wave 9.5: Three Fermion Generations from H4/600-cell + 2I

Five candidate mechanisms for exactly 3 fermion generations.
Each mechanism analysed numerically; honest verdict recorded.

Author: Trinity S3AI Wave 9.5
"""

import math
import itertools
from fractions import Fraction
from collections import Counter

PHI = (1 + math.sqrt(5)) / 2   # golden ratio

def header(title):
    bar = "=" * 72
    print("\n" + bar)
    print("  " + title)
    print(bar)

def subheader(title):
    print("\n--- " + title + " ---")

# ---------------------------------------------------------------------------
# MECHANISM A
# 2I irreducible representations in the regular representation
# ---------------------------------------------------------------------------

def mechanism_A():
    header("MECHANISM A: 2I irrep multiplicities in the regular representation")

    # 2I = SL(2,5) has exactly 9 complex irreps.
    # Their dimensions are: 1, 2, 2, 3, 3, 4, 4, 5, 6
    # Verification: 1+4+4+9+9+16+16+25+36 = 120 = |2I|
    dims_2I = [1, 2, 2, 3, 3, 4, 4, 5, 6]
    names   = ["rho_%d"%i for i in range(1, 10)]
    # conjugate pairing: (rho2,rho3) dim2, (rho5,rho6) dim3, (rho7,rho8) dim4
    # real (self-conjugate): rho1(1), rho4(3), rho9(5), -- hmm wait
    # Note: [1,2,2,3,3,4,4,5,6]:
    #   dim-1: rho1 (trivial, real)
    #   dim-2: rho2, rho3 (conjugate spinor pair)
    #   dim-3: rho4 (real), rho5, rho6 (complex conj pair) -- 3 of them
    #   dim-4: rho7, rho8 (complex conj pair)
    #   dim-5: rho9 (real)
    #   dim-6: ... but there is no 10th irrep!
    # CHECK: 1+2+2+3+3+4+4+5+6 = 30 (Coxeter number of H4)  [structural fact]
    
    ss = sum(d**2 for d in dims_2I)
    print("\n2I = SL(2,5) irreducible representations:")
    print("  Dimensions: " + str(dims_2I))
    print("  Count: " + str(len(dims_2I)))
    print("  Sum of dim^2: " + str(ss) + "  (must equal |2I|=120: " + str(ss==120) + ")")
    print("  Sum of dims:  " + str(sum(dims_2I)) + "  (Coxeter number h(H4)=30: " + str(sum(dims_2I)==30) + ")")
    
    if ss != 120:
        print("  ERROR: sum of squares wrong!")
        # This would indicate an error in the dim list.

    # In the regular representation reg(2I), each irrep rho_i appears
    # exactly dim(rho_i) times.
    print("\nMultiplicities in regular rep:")
    for name, d in zip(names, dims_2I):
        print("  " + name + " (dim " + str(d) + "): multiplicity " + str(d))

    # Spinor irreps are rho_2 and rho_3 (dim 2)
    spinor_dims = [d for d in dims_2I if d == 2]
    spinor_mults = spinor_dims  # multiplicity = dim
    print("\nSpinor (dim-2) irreps: " + str(len(spinor_dims)) + " of them, each with multiplicity 2")
    print("  -> " + str(len(spinor_dims)) + " spinor irreps x multiplicity 2 = " + str(len(spinor_dims)*2) + " copies total")
    print("  -> The two spinor irreps are complex conjugates (rho_2 <-> rho_3)")

    # Do any irreps appear with multiplicity exactly 3?
    triple_irreps = [(n, d) for n, d in zip(names, dims_2I) if d == 3]
    print("\nIrreps with multiplicity exactly 3 (i.e., dim=3 irreps):")
    for n, d in triple_irreps:
        print("  " + n + " (dim " + str(d) + ")")
    print("  Count: " + str(len(triple_irreps)))
    print("  -> These are the 3-dimensional reps, NOT chiral spinors")

    print("\nVERDICT:")
    print("  Spinor irreps (dim 2): appear TWICE in reg(2I), not three times.")
    print("  Dim-3 irreps appear 3 times each -- but these are not spinors.")
    print("  No spinor irrep has multiplicity 3 in reg(2I).")
    print("  Mechanism A FAILS to give 3 chiral fermion generations.")

    return {
        "mechanism": "A",
        "dims": dims_2I,
        "sum_sq": ss,
        "n_irreps": len(dims_2I),
        "spinor_mult": 2,
        "dim3_count": len(triple_irreps),
        "gives_3": False,
        "verdict": "FAIL: spinor irreps have multiplicity 2, not 3",
    }

# ---------------------------------------------------------------------------
# MECHANISM B
# 600-cell decomposition into 24-cells
# ---------------------------------------------------------------------------

def _build_600cell():
    """Build the 120 vertices of the 600-cell as unit quaternions."""
    phi = PHI
    verts = set()

    def add(v):
        verts.add(tuple(round(x, 9) for x in v))

    # Type I: 8 vertices -- permutations of (+-1, 0, 0, 0)
    for i in range(4):
        for s in [1, -1]:
            v = [0.0]*4
            v[i] = float(s)
            add(v)

    # Type II: 16 vertices -- (+-1/2, +-1/2, +-1/2, +-1/2)
    for sgns in itertools.product([0.5, -0.5], repeat=4):
        add(sgns)

    # Type III: 96 vertices -- even permutations of (0, +-1/2, +-1/(2phi), +-phi/2)
    base = [0.0, 0.5, 1.0/(2*phi), phi/2.0]
    perms = list(itertools.permutations([0,1,2,3]))
    # Keep only even permutations
    def parity(p):
        n = len(p)
        vis = [False]*n
        sgn = 1
        for i in range(n):
            if not vis[i]:
                j, cyc = i, 0
                while not vis[j]:
                    vis[j] = True
                    j = p[j]
                    cyc += 1
                if cyc % 2 == 0:
                    sgn = -sgn
        return sgn

    even_perms = [p for p in perms if parity(p) == 1]
    for ep in even_perms:
        for sgns in itertools.product([1,-1], repeat=4):
            v = [sgns[k]*base[ep[k]] for k in range(4)]
            add(v)

    return list(verts)

def qmul(p, q):
    a1,b1,c1,d1 = p
    a2,b2,c2,d2 = q
    return (a1*a2-b1*b2-c1*c2-d1*d2,
            a1*b2+b1*a2+c1*d2-d1*c2,
            a1*c2-b1*d2+c1*a2+d1*b2,
            a1*d2+b1*c2-c1*b2+d1*a2)

def mechanism_B():
    header("MECHANISM B: Decomposition of 600-cell into 24-cells")

    V = _build_600cell()
    print("\nVertices built: " + str(len(V)) + "  (expected 120)")

    # Check norms
    max_norm_err = max(abs(math.sqrt(sum(x**2 for x in v))-1.0) for v in V)
    print("Max |norm-1|: " + str(round(max_norm_err, 10)) + "  (should be ~0)")

    # Verify adjacency structure
    edge_sq = 2.0 - PHI   # ~0.38197
    V_set = set(V)

    degrees = {}
    for v in V:
        deg = 0
        for w in V:
            if w == v:
                continue
            d2 = sum((v[k]-w[k])**2 for k in range(4))
            if abs(d2 - edge_sq) < 1e-6:
                deg += 1
        degrees[v] = deg

    deg_vals = list(degrees.values())
    print("Vertex degrees: min=" + str(min(deg_vals)) + " max=" + str(max(deg_vals)) + "  (all should be 12)")
    n_edges = sum(deg_vals) // 2
    print("Number of edges: " + str(n_edges) + "  (expected 720)")

    subheader("Binary tetrahedral group 2T (order 24) = one 24-cell")

    # 2T elements: 8 from {+-1, +-i, +-j, +-k} + 16 from 1/2(+-1+-i+-j+-k)
    two_T = set()
    for i in range(4):
        for s in [1,-1]:
            v = [0.0]*4; v[i]=float(s)
            two_T.add(tuple(round(x,9) for x in v))
    for sgns in itertools.product([0.5,-0.5], repeat=4):
        two_T.add(tuple(round(x,9) for x in sgns))
    print("2T elements: " + str(len(two_T)) + "  (expected 24)")

    two_T_in_V = two_T.issubset(V_set)
    print("2T subset of 600-cell: " + str(two_T_in_V))

    subheader("Coset decomposition 2I / 2T -> 5 disjoint 24-cells")

    def coset_of(rep):
        c = set()
        for h in two_T:
            prod = tuple(round(x,9) for x in qmul(rep, h))
            if prod in V_set:
                c.add(prod)
            else:
                neg = tuple(-x for x in prod)
                rneg = tuple(round(x,9) for x in neg)
                if rneg in V_set:
                    c.add(rneg)
        return frozenset(c)

    covered = set(two_T)
    cosets = [frozenset(two_T)]

    for v in sorted(V):
        if v not in covered and len(cosets) < 5:
            c = coset_of(v)
            if len(c) == 24 and c.issubset(V_set):
                inter = c & covered
                if len(inter) == 0:
                    cosets.append(c)
                    covered.update(c)

    print("Disjoint 24-cells found: " + str(len(cosets)) + "  (expected 5)")
    total = sum(len(c) for c in cosets)
    print("Total vertices covered: " + str(total) + "  (expected 120)")
    print("Sizes: " + str(sorted(len(c) for c in cosets)))

    print("\n120 = 5 x 24  (the natural factorisation is 5, not 3)")
    print("For 3 generations we would need 120 = 3 x 40.")
    print("But 40 is NOT the size of any canonical polytope substructure.")
    print("The 24-cell decomposition gives 5 sectors, not 3.")
    print("A 3+2 split of the 5 cosets is possible but requires an EXTERNAL principle.")

    print("\nVERDICT:")
    print("  600-cell decomposes into 5 (not 3) disjoint 24-cells.")
    print("  The natural count from this geometry is 5, not 3.")
    print("  Mechanism B DOES NOT automatically give 3 generations.")

    return {
        "mechanism": "B",
        "n_24cells": 5,
        "factorisation": "120 = 5 x 24",
        "gives_3": False,
        "verdict": "FAIL: natural decomposition gives 5 sectors, not 3",
    }

# ---------------------------------------------------------------------------
# MECHANISM C
# Factorisation 120 = 2^3 * 3 * 5
# ---------------------------------------------------------------------------

def mechanism_C():
    header("MECHANISM C: Factorisation 120 = 2^3 * 3 * 5 and the factor 3")

    def factorize(n):
        f = {}
        d = 2
        while d*d <= n:
            while n % d == 0:
                f[d] = f.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            f[n] = f.get(n, 0) + 1
        return f

    fac = factorize(120)
    print("\n120 = " + " * ".join(str(p)+"^"+str(e) if e>1 else str(p) for p,e in sorted(fac.items())))
    print("Factor 3 is present: True")

    print("\nNormal subgroups of 2I = SL(2,5) and their indices:")
    # 2I has a rich normal subgroup structure:
    # Z(2I) = Z_2 (center = {+1, -1}), and 2I / Z_2 = A5 (simple)
    # Subgroups of 2I: {1} C Z_2 C Q_8 (Sylow 2) is NOT normal...
    # Actually normal subgroups of SL(2,5):
    #   {I}, <-I> = Z_2, SL(2,5) itself.
    # A5 = SL(2,5)/{+-I} is simple, so the only normal subgroups of SL(2,5)
    # are {I}, {+-I}, and SL(2,5).
    # (Reference: SL(2,5) is "perfect" i.e. [G,G]=G, so its normal subgroups
    #  are just its central extension structure.)
    normal_subs = [
        ("{1}", 1, 120),
        ("Z_2 = {+/-I}", 2, 60),
        ("2I itself", 120, 1),
    ]
    for name, order, index in normal_subs:
        f = factorize(index)
        fstr = " * ".join(str(p)+"^"+str(e) if e>1 else str(p) for p,e in sorted(f.items())) if f else "1"
        print("  N = " + name + " (order " + str(order) + "): index = " + str(index) + " = " + fstr)

    print("\n2I has no normal subgroup of index 3.")
    print("  (The quotient 2I/N has order 3 only if |N| = 40, but no such N exists.)")
    print("  2I modulo its center gives A5, which is simple (no Z_3 quotient).")

    print("\nArithmetic fact: 120 = 3 * 40.")
    print("Group-theoretic fact: no canonical partition of 2I into 3 blocks of 40.")
    print("The factor 3 in 120=2^3*3*5 does not correspond to any normal subgroup.")

    print("\nVERDICT:")
    print("  120 = 2^3*3*5 contains the factor 3, but 2I has no Z_3 quotient.")
    print("  There is no group-theoretic partition into 3 blocks of size 40.")
    print("  Mechanism C is pure arithmetic -- not a derivation of 3 generations.")
    print("  FAIL.")

    return {
        "mechanism": "C",
        "factorisation": fac,
        "factor_3": True,
        "has_index_3_normal_subgroup": False,
        "gives_3": False,
        "verdict": "FAIL: arithmetic coincidence, no Z_3 quotient of 2I",
    }

# ---------------------------------------------------------------------------
# MECHANISM D
# Coxeter arithmetic of H4
# ---------------------------------------------------------------------------

def mechanism_D():
    header("MECHANISM D: Coxeter-number arithmetic of H4")

    rank = 4
    h = 30          # Coxeter number h(H4) = 30 = 2*3*5
    exponents = [1, 11, 19, 29]   # Coxeter exponents of H4
    order = 14400   # |W(H4)| = 120^2

    print("\nH4 data:")
    print("  Rank: " + str(rank))
    print("  Coxeter number h = " + str(h) + " = 2*3*5")
    print("  Exponents: " + str(exponents))
    print("  |W(H4)| = " + str(order))
    print("  n_positive_roots = h*r/2 = " + str(h*rank//2) + "  (expected 60)")
    print("  n_roots = h*r = " + str(h*rank) + "  (expected 120)")
    print("  Product of (m_i+1) = " + str(math.prod(m+1 for m in exponents)) + "  (= |W(H4)|? " + str(math.prod(m+1 for m in exponents)==order) + ")")

    # Sum of exponents
    print("  Sum of exponents = " + str(sum(exponents)) + "  (= r*h/2 = " + str(rank*h//2) + "? " + str(sum(exponents)==rank*h//2) + ")")

    # Non-trivial exponents (those > 1)
    non_triv = [e for e in exponents if e != 1]
    print("\nNon-trivial exponents (> 1): " + str(non_triv))
    print("Count: " + str(len(non_triv)) + "  (= rank - 1 = " + str(rank-1) + ")")

    print("\nCan any Coxeter arithmetic give 3?")
    print("  h mod rank = " + str(h % rank) + "   (not 3)")
    print("  h / 10 = " + str(h // 10) + "   (= 3; trivially 30 = 10*3)")
    print("  rank - 1 = " + str(rank-1) + "   (= 3; any rank-4 group has this)")
    print("  # exponents in range (1,30) = " + str(len([e for e in exponents if 1 < e < 30])) + "  (= 3)")
    print("  # exponents > 10 = " + str(len([e for e in exponents if e > 10])) + "  (= 3)")

    print("\nKey observation:")
    print("  H4 has 4 exponents: {1, 11, 19, 29}.")
    print("  Removing the trivial exponent 1 leaves 3 non-trivial ones.")
    print("  BUT this is rank arithmetic: ANY rank-4 group has rank-1 = 3")
    print("  non-trivial exponents.")
    print("  This does not DERIVE 3 generations -- it only notes rank(H4) = 4.")

    print("\nComparison with E8 exponents {1,7,11,13,17,19,23,29}:")
    e8_exp = [1,7,11,13,17,19,23,29]
    h4_in_e8 = [e for e in exponents if e in e8_exp]
    print("  H4 exponents contained in E8: " + str(h4_in_e8))
    print("  E8 exponents NOT in H4: " + str([e for e in e8_exp if e not in exponents]))
    # The paper's Sector B argument uses {11,17,23,29} which is NOT H4 exponents
    sector_B = [11, 17, 23, 29]
    in_H4 = [e for e in sector_B if e in exponents]
    print("  E8 'Sector B' = " + str(sector_B) + " -- only " + str(in_H4) + " are H4 exponents.")
    print("  The AP {11,17,23} with common difference 6 is E8 data, not H4.")

    print("\nVERDICT:")
    print("  rank(H4)-1 = 3 gives 3 non-trivial exponents, but this is")
    print("  rank arithmetic, not a physical derivation.")
    print("  The existing three-generations-proof.md confuses H4 and E8 exponents.")
    print("  Mechanism D: WEAK (arithmetic coincidence, not a derivation).")

    return {
        "mechanism": "D",
        "rank": rank,
        "h": h,
        "exponents": exponents,
        "non_trivial_count": len(non_triv),
        "gives_3_via_rank_minus_1": True,
        "verdict": "WEAK: rank(H4)-1=3 is arithmetic; not a physical generation mechanism",
        "gives_3": False,
        "note": "Rank arithmetic only. Any rank-4 group has rank-1=3 non-trivial exponents.",
    }

# ---------------------------------------------------------------------------
# MECHANISM E
# Gauge anomaly cancellation for 2I-symmetric theories
# ---------------------------------------------------------------------------

def mechanism_E():
    header("MECHANISM E: Gauge anomaly cancellation for 2I-symmetric theories")

    print("\n--- Standard Model anomaly review ---")
    print("SM anomaly conditions per generation (using hypercharges Y):")
    # One SM generation: Q_L(3,2,1/6), u_R(3,1,2/3), d_R(3,1,-1/3), L_L(1,2,-1/2), e_R(1,1,-1)
    matter = [
        ("Q_L", 3, 2, Fraction(1,6)),
        ("u_R", 3, 1, Fraction(2,3)),
        ("d_R", 3, 1, Fraction(-1,3)),
        ("L_L", 1, 2, Fraction(-1,2)),
        ("e_R", 1, 1, Fraction(-1,1)),
    ]
    for name, su3, su2, Y in matter:
        print("  " + name + ": ("+str(su3)+","+str(su2)+","+str(Y)+")")

    U1c = sum(su3*su2*Y**3 for _,su3,su2,Y in matter)
    SU3U1 = sum(su2*Y for _,su3,su2,Y in matter if su3 > 1)
    SU2U1 = sum(su3*Y for _,su3,su2,Y in matter if su2 > 1)
    gravU1 = sum(su3*su2*Y for _,su3,su2,Y in matter)

    print("\nAnomalies per generation:")
    print("  [U(1)]^3 = " + str(U1c))
    print("  [SU(3)]^2 [U(1)] = " + str(SU3U1))
    print("  [SU(2)]^2 [U(1)] = " + str(SU2U1))
    print("  [Grav]^2 [U(1)] = " + str(gravU1))

    per_gen_zero = (U1c == 0 and SU3U1 == 0 and SU2U1 == 0 and gravU1 == 0)
    print("\nAll anomalies zero per generation: " + str(per_gen_zero))
    print("=> Anomaly cancellation holds for ANY N_gen >= 1.")
    print("=> N_gen is NOT fixed by SM anomaly cancellation.")

    print("\n--- 2I as a generation/flavour symmetry ---")
    print("If 2I acts as a generation symmetry (not gauge symmetry),")
    print("matter fields transform as (SM rep) x (2I rep).")
    print("The 2I irreps relevant to generation structure:")
    print("  dim 3 irreps: rho_4 (real), rho_5, rho_6 (complex conj pair)")
    print("  If generation space = rho_4 (dim 3, real): 3 copies automatically.")
    print("  This is the ONLY natural way to get exactly 3 from 2I.")

    print("\nIs this forced by anomaly cancellation?  NO.")
    print("  Anomaly cancellation is generation-blind (per-gen contributions cancel).")
    print("  Choosing rho_4 as generation space is a MODEL CHOICE.")
    print("  Why rho_4 and not rho_9 (dim 5) or rho_7 (dim 4)?")
    print("  There is no dynamical reason within this framework.")

    print("\nComparison: standard flavour model approach")
    print("  Many flavour models use finite groups (A4, S3, Z_3, ...) as generation")
    print("  symmetries, choosing the 3-dimensional rep by hand.")
    print("  Using 2I would be unusual (order 120 >> typical flavour group order).")
    print("  2I contains A5 and A4 as subgroups -- perhaps A4 is more natural?")
    print("  A4 has a 3-dimensional real irrep (the fundamental) and order 12.")

    print("\nVERDICT:")
    print("  Anomaly cancellation does NOT determine N_gen in the SM.")
    print("  The 3-dim irrep rho_4 of 2I CAN give 3 copies if chosen as gen space.")
    print("  But this is a model-building CHOICE, not an anomaly derivation.")
    print("  Mechanism E FAILS as an anomaly argument.")
    print("  Partial: 2I as flavour group with rho_4 gives 3, but it's circular.")

    return {
        "mechanism": "E",
        "sm_anomaly_per_gen_zero": True,
        "anomaly_determines_N_gen": False,
        "2I_has_3dim_irrep": True,
        "gives_3_via_flavour": True,
        "gives_3": False,   # False because it's a choice, not a derivation
        "verdict": "FAIL as anomaly argument; partial as flavour-symmetry choice",
        "note": "Anomaly cancellation is generation-blind. Choosing 2I's dim-3 irrep "
                "as generation space gives 3 but is a model-building assumption.",
    }

# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------

def summary(results):
    header("SUMMARY: Wave 9.5 -- Do any mechanisms give 3 fermion generations?")

    print("\nMechanism | Gives 3? | Verdict")
    print("-" * 72)
    for r in results:
        gives = "YES (partial)" if r.get("gives_3_via_flavour") else ("NO" if not r["gives_3"] else "YES")
        print("  " + r["mechanism"] + "         | " + gives.ljust(12) + " | " + r["verdict"][:60])

    any_yes = any(r["gives_3"] for r in results)
    print("\nAny mechanism gives 3 FROM FIRST PRINCIPLES? " + str(any_yes))

    if not any_yes:
        print("""
NEGATIVE RESULT (honest assessment):

None of the five mechanisms DERIVES exactly 3 fermion generations
from the H4/600-cell + 2I geometry alone, without additional assumptions.

Best near-misses:
  A: dim-3 irreps of 2I appear 3 times in reg(2I), but are not spinors.
  D: rank(H4)-1 = 3 is an arithmetic fact but not a physical derivation.
  E: 2I's dim-3 irrep rho_4 could host 3 generations as a FLAVOUR CHOICE.
  B: Natural structure gives 5 sectors (24-cells), not 3.
  C: 120=2^3*3*5 contains 3 but there is no Z_3 normal subgroup of 2I.

Most promising partial path:
  Using 2I as a generation/flavour symmetry with the 3-dim irrep rho_4
  as the generation-space representation gives 3 automatically.
  This is theoretically consistent but requires choosing rho_4 by hand.
  A deeper principle selecting rho_4 (not rho_7 or rho_9) is absent.

This constitutes a NEGATIVE RESULT for H4-based automatic 3-generation
derivation. The count 3 does not emerge naturally from the combinatorics
of the 600-cell, the group theory of 2I, or the Coxeter arithmetic of H4.
""")

def main():
    print("Wave 9.5: Search for 3 fermion generations from H4/600-cell + 2I")
    print("=" * 72)

    results = []
    results.append(mechanism_A())
    results.append(mechanism_B())
    results.append(mechanism_C())
    results.append(mechanism_D())
    results.append(mechanism_E())
    summary(results)

    return results

if __name__ == "__main__":
    main()
