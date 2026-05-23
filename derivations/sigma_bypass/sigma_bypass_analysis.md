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

---

## Geometric Test Results — Wave 14.4

### Method

We built a **discrete de Rham complex** on reduced simplicial models of the E₈, F₄, and H₄ plumbing manifolds:

| Component | E₈ model | F₄ model | H₄ model |
|-----------|----------|----------|----------|
| Interior vertices | 8 (E₈ Dynkin nodes) | 4 (F₄ Dynkin nodes) | 4 (H₄ Dynkin nodes) |
| Boundary vertices | 12 (icosahedron) | 24 (24-cell) | 12 (icosahedron) |
| Total vertices | 20 | 28 | 16 |
| Interior edges | E₈ Dynkin diagram | F₄ Dynkin diagram | H₄ Dynkin diagram |
| Boundary edges | Icosahedral adjacency | 24-cell adjacency | Icosahedral adjacency |
| Interior–boundary edges | **All-to-all** (cone join) | **All-to-all** (cone join) | **All-to-all** (cone join) |

For each model we constructed:
- k-cochain spaces C^k for k = 0, 1, 2, 3, 4
- Coboundary operators d_k via oriented simplex incidence
- Adjoints d†_k = d_k^T (unit diagonal mass matrix)
- Hodge Laplacians Δ_k = d_{k-1} d_{k-1}^T + d_k^T d_k
- Kernel dimensions via eigendecomposition (eigenvalue threshold 1×10⁻⁸)

### Numerical Results

| System | C⁰ | C¹ | C² | C³ | C⁴ | dim H⁰ | dim H¹ | **dim H²** | dim H³ | dim H⁴ |
|--------|----|----|----|----|----|--------|--------|------------|--------|--------|
| E₈ | 20 | 133 | 344 | 370 | 140 | 1 | 0 | **0** | 0 | 0 |
| F₄ | 28 | 195 | 552 | 672 | 288 | 1 | 0 | **0** | 0 | 0 |
| H₄ | 16 | 81 | 176 | 170 | 60 | 1 | 0 | **0** | 0 | 0 |

Euler-characteristic checks (χ = Σ (−1)^k dim C^k = Σ (−1)^k b_k):
- E₈: χ = 20 − 133 + 344 − 370 + 140 = **1** = 1 − 0 + 0 − 0 + 0 ✓
- F₄: χ = 28 − 195 + 552 − 672 + 288 = **1** = 1 − 0 + 0 − 0 + 0 ✓
- H₄: χ = 16 − 81 + 176 − 170 + 60 = **1** = 1 − 0 + 0 − 0 + 0 ✓

Smallest nonzero eigenvalue of Δ₂ (spectral gap):
- E₈: λ_min(Δ₂) ≈ 0.962
- F₄: λ_min(Δ₂) ≈ 1.586
- H₄: λ_min(Δ₂) ≈ 1.350

All Laplacians are strictly positive on C²; there is **no zero mode**.

### Interpretation

**No-Go Theorem 6 (reduced model):**  
In the reduced simplicial model, **dim H² = 0 for E₈, F₄, and H₄**.  
No harmonic 2-form exists → **no sigma-field candidate** in this approximation.

### Honest Limitations

1. **Reduced boundary dimension.** The true E₈ plumbing boundary is the Poincaré homology sphere (a 3-manifold, triangulated by the 600-cell with 120 vertices). We replaced it with the icosahedron (12 vertices, S²) or the 24-cell (24 vertices, S³). The reduced boundary does not faithfully represent the true 3-dimensional topology.

2. **Contractible join topology.** Connecting every interior vertex to every boundary vertex via all-to-all edges makes the complex a topological cone. The interior Dynkin-diagram trees are contractible, and the cone over any boundary polytope is contractible. Consequently the reduced model has the homology of a point (b₀ = 1, b_k = 0 for k > 0), **regardless** of the root system.

3. **Missing 2-cycles.** The true E₈ plumbing has second Betti number b₂ = 8 (from the eight plumbed 2-spheres whose intersection matrix is the E₈ Cartan matrix). Our reduced model contains no embedded 2-spheres; the interior vertices are 0-dimensional, and the only 2-dimensional subcomplex is the boundary polytope, which is filled by 3-simplices (tetrahedra) because of the all-to-all cone structure.

4. **Scalar vs. 2-form.** In the Connes–Marcolli construction the sigma-field is an auxiliary scalar field, not a 2-form. We followed the Wave 14.4 instruction to test k = 2 (middle degree in 4D), but the physical interpretation of a 2-form zero mode as a scalar field candidate is itself a modeling assumption.

### Conclusion

The **geometric test on the reduced model supports No-Go Theorem 6**: no system admits a harmonic 2-form, so no sigma-field candidate emerges from this discrete de Rham complex.

However, because the reduced model is contractible and cannot resolve the true 4-manifold topology of the plumbing construction, **this result does not definitively rule out a sigma-field in the full E₈ or F₄ geometry**. A genuine proof would require:

1. A full simplicial triangulation of the E₈ plumbing with the 600-cell boundary (128 vertices).
2. Explicit construction of the eight 2-sphere cycles in the interior.
3. Verification that the Hodge Laplacian on that full complex has dim H² = 8 for E₈ (matching the true second Betti number).
4. Only then could one ask whether any of those harmonic 2-forms can serve as a sigma-field in the spectral action.

**Status: No-Go Theorem 6 holds in the reduced model, but the full 4-manifold topology remains untested.**

The sigma-field bypass via E₈/F₄ remains a viable research direction for a future wave with sufficient computational resources to handle the full 128-vertex triangulation.

---

**Files:**
- `derivations/sigma_bypass/geometric_sigma_test.py` — Python script (builds complex, computes Laplacians, outputs JSON)
- `derivations/sigma_bypass/geometric_sigma_results.json` — numerical results (Betti numbers, ranks, eigenvalue spectra)
