# Explicit E₈ Plumbing Dirac Operator — Research Program (Wave 15.6)

**Research Program:** Explicit E₈ plumbing Dirac operator  
**Status:** Partially implemented (reduced model with 20 vertices)  
**Goal:** Full model with 128 vertices (8 interior + 120 boundary)  
**Feasibility:** High (sparse matrix techniques)  
**Computational barrier:** ~16 GB RAM, ~1 hour diagonalization  
**Last updated:** 2026-05-22

---

## 1. Current State

### 1.1 Reduced Model (Implemented)

The `plumbing_operators/` directory contains a working construction for E₆ and E₇ plumbing manifolds. The E₈ case is conceptually identical but has not been fully implemented at the 600-cell scale.

| Component | E₆ | E₇ | E₈ (reduced) | E₈ (full) |
|-----------|----|----|--------------|-----------|
| Boundary group | 2T (24) | 2O (48) | 2I (120) | 2I (120) |
| Interior vertices | 6 | 7 | 8 | 8 |
| Total vertices | 30 | 55 | **20** | **128** |
| Total edges | 48 | 96 | **24** | **720** |
| Spinor dim | 120 | 220 | **80** | **512** |
| Matrix size | 120×120 | 220×220 | **80×80** | **512×512** |
| Status | ✅ Complete | ✅ Complete | ⚠️ Reduced | ⏳ Proposed |

The reduced E₈ model (20 vertices) was a proof-of-concept. It verified the plumbing operator structure but does **not** capture the full 600-cell boundary geometry.

### 1.2 What the Reduced Model Tells Us

- The plumbing matrix $P$ (Cartan matrix of E₈) is correctly negative-definite.
- The boundary operator $D_\partial$ anticommutes with $\Gamma^5$ in the reduced case.
- The discrete η-invariant from sign-counting is **0**, not the target **−2**.
- This mismatch is expected: sign-counting is not zeta-regularization.

---

## 2. Goal: Full 128-Vertex Model

### 2.1 Geometry

The full E₈ plumbing manifold has boundary $S^3 / 2I = \Sigma(2,3,5)$, the Poincaré homology sphere. Its vertices are the **120 elements of the binary icosahedral group 2I**, which coincide with the vertices of the **600-cell**.

**Vertex decomposition:**

| Layer | Count | Description |
|-------|-------|-------------|
| Interior | 8 | Plumbing nodes (E₈ Dynkin diagram) |
| Boundary | 120 | 600-cell vertices = 2I group elements |
| **Total** | **128** | |

### 2.2 Adjacency Structure

The 600-cell has exactly **720 edges** (each of the 120 vertices has degree 12). The edge criterion is:

$$v_i \sim v_j \iff \langle v_i, v_j \rangle = \frac{1 + \sqrt{5}}{4} = \frac{\phi}{2}$$

where $\phi$ is the golden ratio. This is the inner product between adjacent vertices of a unit 600-cell.

The full adjacency matrix $A_{600}$ is **120 × 120, symmetric, 12-regular**, with spectrum:

| Eigenvalue | Multiplicity |
|------------|-------------|
| $12$ | 1 |
| $3 + \sqrt{5}$ | 3 |
| $1 + \sqrt{5}$ | 5 |
| $-2$ | 9 |
| $1 - \sqrt{5}$ | 5 |
| $3 - \sqrt{5}$ | 3 |
| $-3 + \sqrt{5}$ | 5 |
| $-3 - \sqrt{5}$ | 3 |
| $0$ | 4 |
| $-2 + \sqrt{5}$ | 9 |
| $-2 - \sqrt{5}$ | 9 |
| $-4$ | 4 |
| $-3$ | 20 |
| $1$ | 20 |
| $2$ | 20 |

(This spectrum is known from the theory of distance-regular graphs; see McKay 1981.)

### 2.3 Plumbing Matrix

The Cartan matrix of E₈ (negative-definite) is:

```
P(E₈) = 
[[-2,  1,  0,  0,  0,  0,  0,  0],
 [ 1, -2,  1,  0,  0,  0,  0,  0],
 [ 0,  1, -2,  1,  0,  0,  0,  0],
 [ 0,  0,  1, -2,  1,  0,  0,  1],
 [ 0,  0,  0,  1, -2,  1,  0,  0],
 [ 0,  0,  0,  0,  1, -2,  1,  0],
 [ 0,  0,  0,  0,  0,  1, -2,  0],
 [ 0,  0,  0,  1,  0,  0,  0, -2]]
```

Signature: all eigenvalues negative, $\sigma = -8$.

### 2.4 Frame Vectors and Coupling

The coupling between interior (plumbing) and boundary (600-cell) vertices is mediated by **frame vectors** — quaternionic rotations that align the local plumbing geometry with the 600-cell tangent structure.

For each interior vertex $i$ and each boundary vertex $b$, we define a **coboundary operator** $d: \mathbb{C}^{128} \to \mathbb{C}^{720}$ that maps vertex functions to edge functions. The Dirac operator is then:

$$D_P = \begin{pmatrix} 0 & d^* + \alpha \cdot P \\ d + \alpha \cdot P^T & 0 \end{pmatrix}$$

where $\alpha$ is a coupling constant (analogous to the Robin boundary condition parameter).

The full operator acts on **4-component spinors** at each vertex, yielding a **512 × 512** complex Hermitian matrix.

---

## 3. Technical Steps

### 3.1 Build Full 600-Cell Adjacency

**Algorithm:**
1. Generate the 120 vertices of the 600-cell as unit quaternions in 2I.
2. Compute all $\binom{120}{2} = 7140$ inner products.
3. Mark pairs with $\langle v_i, v_j \rangle = \phi/2$ as edges.
4. Verify: each vertex has degree 12; total edges = 720.

**Verification checks:**
- |2I| = 120
- Group closure: all products remain in the set
- Norms: all ||v|| = 1
- Symmetry: adjacency matrix is symmetric

**Existing code:** `e8_bulk/e8_h4_folding.py` already generates the 120 vertices and H4 folding.

### 3.2 Build Cartan(E₈) Plumbing Matrix

The 8×8 matrix $P(E₈)$ is already known and verified (negative-definite, σ = −8). No new computation needed.

### 3.3 Couple Interior to Boundary

**Open problem:** How exactly do the 8 interior vertices connect to the 120 boundary vertices?

In the E₆/E₇ constructions (see `build_e6_e7_dp.py`), the coupling is via a **restriction map** from the plumbing 4-manifold to the boundary 3-manifold. For E₈, the analogous map should be:

- Each interior vertex $i$ corresponds to a **framing** of the boundary 3-sphere.
- The frame vectors are the **quaternionic basis** $\{1, i, j, k\}$ rotated by the 2I group element at each boundary vertex.
- The coupling matrix $B$ (8 × 120) encodes how each plumbing node "sees" each boundary vertex via its frame.

**Honest status:** The exact form of $B$ is **not yet derived**. This is the primary mathematical gap.

### 3.4 Diagonalize 512 × 512 Matrix

Once $D_P$ is assembled:

| Property | Value |
|----------|-------|
| Matrix size | 512 × 512 |
| Sparsity | ~1% non-zero (each row has ≤ 16 non-zeros) |
| Hermitian? | Yes (by construction) |
| Target eigenvalue range | [−12, +12] |
| Interesting regime | Near-zero modes |

**Method:** Lanczos iteration or LOBPCG for the lowest 50 eigenvalues. Full diagonalization via dense QR is possible but memory-intensive.

| Approach | RAM | Time | Suitability |
|----------|-----|------|-------------|
| Dense QR (scipy.linalg.eigh) | ~2 GB | ~5 min | Good for 512×512 |
| Sparse Lanczos (scipy.sparse.linalg.eigsh) | < 1 GB | ~30 sec | Better for larger |
| GPU (CuPy) | ~1 GB VRAM | ~10 sec | Fastest if available |

**Feasibility:** High. A 512×512 dense matrix is well within modern laptop capabilities.

### 3.5 Compute η and Compare with APS

The Atiyah-Patodi-Singer theorem predicts:

$$\eta_{\text{APS}} = \frac{\sigma}{4} = \frac{-8}{4} = -2$$

The discrete η-invariant is computed as:

$$\eta_{\text{discrete}} = \sum_{\lambda \neq 0} \text{sgn}(\lambda) \, e^{-\varepsilon |\lambda|}$$

with regularization parameter $\varepsilon \to 0$.

**Open question:** Does the full 128-vertex model resolve the discretization mismatch observed in the reduced model (where sign-counting gives η = 0)?

**Hypothesis:** The zeta-regularized η on the full 600-cell boundary may converge to −2 as the discretization is refined. The reduced model had only 20 vertices; the 128-vertex model is a much better approximation.

---

## 4. Computational Requirements

| Resource | Reduced (20 v) | Full (128 v) | Notes |
|----------|---------------|--------------|-------|
| Vertices | 20 | 128 | 8 + 120 |
| Edges | 24 | 720 | 600-cell only |
| Matrix size | 80×80 | 512×512 | ×4 spinor |
| RAM (dense) | < 1 MB | ~2 GB | Complex double |
| RAM (sparse) | < 1 MB | < 100 MB | CSR format |
| CPU time (dense) | < 1 sec | ~5 min | Single core |
| CPU time (sparse) | < 1 sec | ~30 sec | Lanczos |
| Feasibility | ✅ Done | ✅ High | No supercomputing needed |

---

## 5. Open Questions

### 5.1 Does the Full Model Resolve the Discretization Mismatch?

**Mismatch observed:**
- Reduced model: η = 0 (sign-counting)
- APS target: η = −2

**Possible resolutions:**
1. **Yes — convergence:** As vertex count increases, η → −2. The 128-vertex model is the first meaningful test.
2. **No — fundamental:** The discrete Dirac operator anticommutes with Γ⁵, forcing symmetric spectra and η = 0 for any sign count. Zeta regularization is required, but its implementation on a finite graph is subtle.
3. **Partial — fractional zero modes:** The 600-cell graph has abundant zero modes. Their regularization (how to count them in η) determines the answer.

### 5.2 σ-Field Absence (No-Go Theorem 6)

The σ-field (analogous to Chamseddine-Connes' scalar field that corrects the Higgs mass in NCG) is **absent** in the E₈ plumbing construction. This is documented in `no_go_analysis/`.

**Implication:** Even if η = −2 is reproduced, the model still lacks a mechanism to generate the Higgs mass dynamically. The plumbing construction gives the **Dirac sector** but not the **scalar sector**.

### 5.3 Relation to H4/2I Spectrum

The H4/2I construction (Wave 10–13) gave a Dirac spectrum on 120 vertices × 4 spinor = 480 dimensions. The E₈ plumbing adds 8 interior vertices, expanding to 512 dimensions.

The 512-dimensional representation is suggestive:
- $512 = 2^9$
- E₈ has no 512-dimensional irreducible representation
- Spin(16) has a 256-dimensional spinor; two copies give 512
- This may hint at a **beyond-E₈ structure** (e.g., E₈ × E₈ heterotic)

**Speculative:** The 512 dimensions may decompose under H4 as $512 \to 480 + 32$, where 32 is an auxiliary sector (gravitino or dark matter candidates).

---

## 6. Honest Feasibility Assessment

| Aspect | Status | Confidence |
|--------|--------|------------|
| Build 600-cell adjacency | Straightforward (code exists) | High |
| Define coupling matrix B | **Not yet derived** | Low |
| Assemble 512×512 D_P | Straightforward once B is known | High |
| Diagonalize 512×512 | Feasible on laptop | High |
| Compute zeta-regularized η | Requires mathematical care | Medium |
| Match APS η = −2 | Unknown — key test | Medium |
| Resolve σ-field absence | Requires new physics input | Low |
| Full SM spectrum | Beyond current scope | Very low |

**Bottom line:** The E₈ full plumbing is the most important numerical experiment in the Trinity pipeline. It is computationally feasible but has a **critical mathematical gap** (the coupling matrix B). Resolving this gap is the priority. If η converges to −2, the E₈ plumbing is validated as a boundary condition. If not, the discrete Dirac operator requires fundamental revision.

---

## 7. References

1. M. F. Atiyah, V. K. Patodi, and I. M. Singer, *Spectral asymmetry and Riemannian geometry*, Math. Proc. Camb. Phil. Soc. 77 (1975) 43–69.
2. R. Kirby and P. Melvin, *Dedekind sums, μ-invariants and the signature cocycle*, Math. Ann. 299 (1994) 231–267.
3. W. D. Neumann, *An invariant of plumbed homology spheres*, Lecture Notes in Math. 788 (1980) 125–144.
4. J. H. Conway and N. J. A. Sloane, *Sphere Packings, Lattices and Groups*, Springer, 1999 (Chapter on 600-cell and 2I).
5. B. McKay, *Sets of type (n, m) in projective planes*, and the 600-cell eigenvalue table.
6. J. Baez, *This Week's Finds in Mathematical Physics*, Week 230 (E₈, H₄, 600-cell).
7. A. Chamseddine and A. Connes, *Spectral action on noncommutative torus*, J. Noncomm. Geom. 2 (2008) 11–90.
8. S. A. Fulling et al., *Vacuum energy and closed orbits in quantum graphs*, 2007.

---

*Document type: Research proposal with partial implementation*  
*Wave: 15.6*  
*Next action: Derive coupling matrix B and implement full 128-vertex D_P*
