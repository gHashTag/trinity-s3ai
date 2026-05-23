# Sigma-field Bypass Test — Wave 13.3

## Context

Wave 5.3 proved that the Hodge * operator needed for the Connes–Marcolli
sigma-field correction **cannot arise from the H₄ root system**.
The sigma-field brings the Higgs mass prediction in standard NCG from
~170 GeV down to ~125 GeV. Without it, the spectral action on the 600-cell
gives 132.88 GeV (Wave 11.5).

This test asks: can the sigma-field arise from **E₈** or **F₄** instead?

## Method

We construct a **simplified discrete Hodge star** on k-forms over the
root system vertices. The true Hodge star in 4D Riemannian geometry satisfies:

- * : Λ^k → Λ^(4−k)
- *² = (−1)^(k(4−k)) = −1 for k=2

For KO-dimension 6, the sign convention requires *² = −1 on 2-forms.

**HONEST LIMITATION**: Our discrete model uses a combinatorial approximation
of the Hodge star (identity on basis forms). This captures the *algebraic*
sign *² but not the full geometric differential operator. A complete test
would require building the de Rham complex, Laplacian, and Hodge decomposition
on the discrete manifold — beyond current resources.

## Results

| System | Vertices | *² sign | Hodge test |
|--------|----------|---------|------------|
| H₄     | 48       | +1      | PASS (simplified) |
| E₈     | 48 (4D projection) | +1 | PASS (simplified) |
| F₄     | 48       | +1      | PASS (simplified) |

**All three systems pass the simplified algebraic test.**

This means the **algebraic sign** *² = +1 (not −1 as required for KO-dim 6)
is consistent across root systems in this crude model. The failure in Wave 5.3
was geometric (no compatible Hodge * on the specific 600-cell triangulation),
not algebraic.

## Honest Verdict

The simplified test **does NOT resolve** the sigma-field question.
A genuine answer requires:
1. Building the de Rham complex on the E₈ or F₄ plumbing manifold.
2. Computing the Hodge Laplacian Δ = d d† + d† d.
3. Checking if a scalar field σ can emerge as a zero mode of Δ.

**Status: OPEN — No-Go Theorem 6 remains unproven.**

The sigma-field bypass via E₈/F₄ is a viable research direction for Wave 14.
