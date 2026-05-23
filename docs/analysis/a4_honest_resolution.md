# a4 Discrepancy — Honest Resolution

## 1. Executive Summary

The discrepancy between the Coq heat-kernel a4 and the Trinity Higgs a4 has an
**exact, closed-form conversion factor**. This factor is **not** 60 = 5!; it is
coincidentally close to 60 (within 0.59%) but differs by an irreducible
algebraic expression in the golden ratio. Claiming the factor is exactly 60
would be mathematically incorrect and, under peer review, indefensible.

---

## 2. Exact Conversion Factor

### 2.1 Statement of the two a4 values

| Source | Expression | Numerical value |
|--------|-----------|-----------------|
| Coq (heat kernel) | (5 + 6φ)/(16φ) | ≈ 0.5681356214843421 |
| Trinity (Higgs) | 8φ³ | ≈ 33.888543819998318 |

where φ = (1 + √5)/2 is the golden ratio.

### 2.2 Exact ratio

```
Factor = Trinity a4 / Coq a4
       = 8φ³ · 16φ / (5 + 6φ)
       = 128 φ⁴ / (5 + 6φ)
```

Rationalising the denominator (multiply top and bottom by the conjugate
8 − 3√5) gives three equivalent exact forms:

| Form | Expression | Decimal |
|------|-----------|---------|
| **Primary** | **(704 + 192√5) / 19** | **59.64868693052419** |
| In φ | 128 (4 + 3φ) / 19 | 59.64868693052419 |
| In √5 | 64 (11 + 3√5) / 19 | 59.64868693052419 |

### 2.3 Comparison with 60

| Quantity | Value | Difference from 60 |
|----------|-------|-------------------|
| Exact factor | 59.64868693052419 | −0.35131306947581 |
| 60 (hypothesised) | 60.0 | — |
| 5! = 120/2 | 60.0 | — |

- **Absolute difference**: 60 − factor = (436 − 192√5)/19 ≈ 0.3513
- **Relative difference**: 0.3513 / 60 ≈ **0.59%**

Coq a4 × 60 = 34.08813728906053  
Trinity a4  = 33.88854381999832  
Relative mismatch ≈ **0.59%**

### 2.4 Verdict: Is the factor exactly 60?

**No.** The exact factor is (704 + 192√5)/19, an algebraic number of degree 2
over Q. It is *not* the integer 60, not 5!, not 120/2, not any simple
combinatorial count of the 600-cell. The proximity to 60 is a numerical
coincidence, not a structural identity.

---

## 3. Physical Interpretation

### 3.1 What Coq a4 is

The Coq value a4 = (5 + 6φ)/(16φ) is the **per-vertex heat-kernel
coefficient** computed from the Seeley–DeWitt expansion of the Laplacian (or
Dirac operator squared) on the 600-cell skeleton. It arises from the small-t
asymptotics

```
Tr e^{−tΔ} ~ (4πt)^{−dim/2} Σ a_n t^n
```

and encapsulates local curvature and combinatorial data at a single vertex.

### 3.2 What Trinity a4 is

The Trinity value a4 = 8φ³ appears in the **Higgs-potential term** of the
spectral action. In Connes–Chamseddine spectral action formalism, the
quartic Higgs coupling receives contributions of the form

```
V(H) ⊃ (f4 a4 / 2π²) |H|⁴
```

where f4 is the fourth moment of the cutoff function. The Trinity value
8φ³ is the *total* a4-weighted contribution that enters the Higgs mass
formula after summing over the finite geometry with whatever normalisation
and weighting conventions Trinity uses.

### 3.3 Why the ratio is ~60 — honest assessment

**The per-vertex hypothesis does not work cleanly.**

The 600-cell has 120 vertices. If Coq a4 were simply per-vertex and Trinity
a4 were the total over all vertices, one would expect:

```
Expected total = 120 × 0.5681356... = 68.17627...
Actual Trinity = 33.88854...
```

These do not match. The ratio is not 120.

**The "60 vertices" hypothesis is post-hoc.**

The observation that 60 × 0.568 ≈ 33.89 (within 0.6%) is tempting, and the
number 60 = 120/2 appears naturally in the 600-cell (e.g. 120 vertices / 2,
or 720 edges / 12, etc.). However:

1. The exact factor is 59.65, not 60. There is no known geometric principle
   that explains why the Trinity normalisation should produce precisely
   (704 + 192√5)/19 vertices' worth of contribution.

2. The Trinity codebase does not *document* a division-by-2 or a "60-vertex"
   weighting in its a4 computation. If such a weighting exists, it is implicit
   and unexplained.

3. The 0.6% mismatch is too large to be a rounding artefact and too small to
   be an obvious bug. It is in the uncomfortable middle ground that suggests
   either (a) a missing φ-dependent correction in one of the two codes, or
   (b) genuinely different conventions that have not been reconciled.

### 3.4 Is this post-hoc?

**Yes, honestly.** The hypothesis that "the factor is 60 because the 600-cell
has 120 vertices and there is an implicit factor of 1/2" was constructed
*after* seeing the numerical proximity. It is not derived from first
principles, nor is it documented in either codebase. A referee would
immediately ask: "Where does the 1/2 come from?" and the honest answer is
"we don't know; it fits the numbers to within 0.6%."

---

## 4. Possible Origins of the Discrepancy

### Hypothesis A: Different operator definitions
The Coq computation may use the graph Laplacian Δ = d†d, while Trinity may
use the Dirac operator D (or D²) with a Clifford-module structure that
introduces a factor of 1/2 in the heat-kernel coefficients. If so, the
conversion factor should be exactly 2 (or 1/2), not ~59.65. This hypothesis
does not explain the data.

### Hypothesis B: Different spectral-action normalisations
In the spectral action, the cutoff function f enters via its moments f0, f2,
f4. Different choices of f (sharp cutoff vs. Gaussian vs. characteristic
function) change the numerical prefactors. However, these prefactors are
usually rational numbers, not algebraic numbers involving √5. It is unlikely
that normalisation alone explains the φ-dependent mismatch.

### Hypothesis C: Missing H4-invariant curvature terms
The 600-cell is a maximally symmetric discrete analogue of S³ with H4
icosahedral symmetry. The a4 coefficient on such a space can receive
contributions from higher-order curvature invariants (analogous to the
Euler term and the |Riemann|² term in the continuum). If the Coq and Trinity
computations include different subsets of these invariants, the discrepancy
could be structural rather than a simple multiplicative factor.

### Hypothesis D: One of the values is simply wrong
The most uncomfortable but most likely explanation: either the Coq a4 or the
Trinity a4 (or both) contains an algebraic error. The fact that the ratio is
close to but not exactly a nice number (60) is the hallmark of two
independent calculations that are *almost* consistent but diverge in a
subtle way.

**Evidence for Hypothesis D:**
- If Coq a4 were off by a factor of (704 + 192√5)/(19 × 60) ≈ 0.9941, the two
  would agree perfectly. This correction factor is not a simple rational
  number, suggesting a subtle algebraic slip.
- The Trinity value 8φ³ = 16 + 8√5 is a very simple algebraic integer. The
  Coq value (5 + 6φ)/(16φ) = 7/32 + 5√5/32 is also simple. The ratio of two
  simple expressions being *almost* 60 but not quite is suspicious.

---

## 5. Recommended Actions

### Immediate: Document the exact factor
Do not hide the discrepancy. In the Trinity codebase and any papers, state
clearly:

> "The conversion between the Coq per-vertex heat-kernel a4 and the Trinity
> spectral-action a4 is given by the exact algebraic factor
> (704 + 192√5)/19 ≈ 59.65, not the integer 60. The origin of this factor
> is under investigation."

### Short-term: Reconcile conventions
1. **Audit the Coq normalisation**: Check whether the Coq a4 is per-vertex
   or total, and whether it includes any volume or symmetry factors.
2. **Audit the Trinity normalisation**: Trace how 8φ³ is derived. Is it from
   a direct computation of the spectral action, or is it an empirical fit?
3. **Compare intermediate steps**: Both codes compute a chain of quantities
   (eigenvalues, multiplicities, heat-kernel traces). Compare at each step
   to localise the divergence.

### Medium-term: Verify algebraically
Use a computer algebra system (SageMath, Mathematica, or SymPy) to compute
the a4 coefficient from scratch for the 600-cell graph Laplacian, following
the standard heat-kernel expansion formula:

```
a4 = (1/360) ∫ (5R² − 2R_{ij}R^{ij} + 2R_{ijkl}R^{ijkl}) dV
```

(adapted to the discrete setting). Check whether this matches Coq or Trinity.

### Long-term: Decide on a convention
There are two defensible paths:

**Path 1: Unify on the Coq convention.**
- Adopt the Coq per-vertex a4 as the canonical value.
- Modify the Trinity Higgs potential to use the correctly converted total a4.
- This may shift the Higgs mass prediction by ~0.6%.

**Path 2: Unify on the Trinity convention.**
- Accept Trinity's a4 = 8φ³ as the operational definition.
- Document that this value is derived from spectral-action principles and
  may differ from the raw heat-kernel coefficient by a factor of
  (704 + 192√5)/19.

**Recommendation:** Choose Path 1. The Coq value has a formal proof, giving
it higher epistemic status. The Trinity value should be shown to follow from
the Coq value via a well-defined chain of physical reasoning. Until that
chain is established, 8φ³ should be treated as a phenomenological ansatz,
not a theorem.

---

## 6. What Peer Reviewers Would Say

A referee for a journal like *Communications in Mathematical Physics* or
*Journal of High Energy Physics* would likely raise the following points:

1. **"The factor 60 is not derived; it is numerically fitted."** A 0.6%
   agreement does not constitute a derivation. Show the exact conversion or
   explain the discrepancy.

2. **"Which a4 is the physical one?"** The spectral action and the heat-kernel
   expansion are related but not identical. Clarify the mapping between them.

3. **"Where is the formal proof?"** If Coq proves one value and Trinity asserts
   another, the burden of reconciliation falls on the Trinity side unless a
   physical argument overrides the formal proof.

4. **"What happens at higher orders?"** If a4 is mismatched, what about a6,
   a8, and the running of couplings? The discrepancy may propagate.

---

## 7. Conclusion

The honest resolution is:

| Question | Answer |
|----------|--------|
| Exact conversion factor? | **(704 + 192√5)/19 ≈ 59.6487** |
| Is it exactly 60 = 5!? | **No.** |
| Is the "60 vertices" interpretation valid? | **No.** It is post-hoc numerology. |
| Is the discrepancy a bug or a convention? | **Unknown.** Requires auditing both codes. |
| Recommended fix? | **Document the exact factor; reconcile conventions; favour the Coq-proven value.** |

The 0.59% mismatch is small enough to be tempting, large enough to be
meaningful, and uncomfortable enough to demand resolution before any
publication claims precision for the Higgs mass derivation.
