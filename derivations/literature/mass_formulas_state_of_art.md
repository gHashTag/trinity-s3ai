# Standard Model Fermion Mass Formulas: State of Theory in 2026

> Analytical review for the trinity-s3ai project  
> Compiled: June 2026  
> Source status: real arXiv preprints and peer-reviewed journals

---

## Contents

1. [Koide Formula: History and Current Status](#1-koide-formula)
2. [Non-Numerological Approaches to Mass Matrices](#2-non-numerological-approaches)
3. [Works 2022–2026: Yukawa Hierarchies from F-Theory, Landscape, and AI/ML](#3-works-2022-2026)
4. ["Derivation" vs "Fitting": Falsifiability Criteria](#4-derivation-vs-fitting)
5. [Coxeter Group H₄ and the 600-Cell: Precedents](#5-h4-group-and-600-cell)
6. [10–15 Practical Lessons for trinity-s3ai](#6-lessons-for-trinity-s3ai)
7. [List of Sources](#7-list-of-sources)

---

## 1. Koide Formula

### 1.1 Original Works (1981–1983)

Yoshio Koide proposed an empirical formula in 1981–1982 in the context of a **preon model** — hypothetical substructures of leptons and quarks. The formula arose as a byproduct of an attempt to relate the Cabibbo angle to charged lepton masses:

\[
Q = \frac{m_e + m_\mu + m_\tau}{(\sqrt{m_e} + \sqrt{m_\mu} + \sqrt{m_\tau})^2} = \frac{2}{3}
\]

In the original formulation ([Koide 1982](https://arxiv.org/abs/hep-ph/0505220)) the mass of the i-th lepton was assumed proportional to \((z_0 + z_i)^2\), where the parameters \(z_i\) satisfied two symmetry conditions: \(\sum z_i = 0\) and \(\frac{1}{3}\sum z_i^2 = z_0^2\). From these conditions the formula Q = 2/3 follows as a geometric identity.

**Important:** In 1981, when the formula was proposed, the tau lepton mass had not yet been precisely measured (the value given was \(1783 \pm 4\) MeV). The prediction of the formula was \(m_\tau = 1776.97\) MeV — this was a genuine prediction, later confirmed.

### 1.2 Precision with Modern PDG 2024 Values

From PDG 2024 data (cited in [arXiv:2510.01312](https://arxiv.org/abs/2510.01312)):

| Particle | Mass (MeV/c²) |
|---------|---------------|
| \(m_e\) | 0.51099895000(15) |
| \(m_\mu\) | 105.6583755(23) |
| \(m_\tau\) | 1776.93(09) |

Computed value: **Q = 0.66666446(508)**

Relative deviation from 2/3: **9.3 ppm** (parts per million).

According to [arXiv:2605.09651](https://arxiv.org/abs/2605.09651) (May 2026), the formula holds with precision **9.3 ppm** using PDG 2024 pole masses. Assuming Q = 2/3 exactly gives a prediction for the tau lepton mass: **\(m_\tau^{\rm pred} = 1776.969\) MeV**, whereas the measured value is \(1776.93 \pm 0.09\) MeV.

**Conclusion:** The Koide formula holds to 5-digit precision (∼ 10⁻⁵) and remains within experimental error.

### 1.3 Theoretical Explanations

#### Sumino Model (2009)
Y. Sumino proposed an explanation through a **family gauge symmetry U(3)**, which forces pole masses to exactly satisfy the Koide formula by suppressing QED corrections. The model is discussed in [arXiv:0812.2090](https://arxiv.org/abs/0812.2090) ("Family Gauge Symmetry and Koide's Mass Formula", Phys.Lett.B 2009). Key mechanism: the gauge symmetry unifies SU(2)_L at a scale of 10²–10³ TeV and forbids radiative corrections that violate the relation.

#### Foot's Geometric Interpretation (1994)
Robert Foot reformulated the formula as a **geometric condition**: the angle between the vector \((\sqrt{m_e}, \sqrt{m_\mu}, \sqrt{m_\tau})\) and the symmetry axis (1,1,1) is exactly 45°:

\[
\cos^2\theta = \frac{1}{3Q} \Rightarrow \theta = 45.000° \pm 0.001°
\]

This observation ([hep-ph/9402242](https://arxiv.org/abs/hep-ph/9402242)) raises the question: why does the mass vector lie exactly "halfway" between the limiting configurations?

#### Brannen's Phase Parameterization (2006)
Carl Brannen discovered a trigonometric expression uniting the three masses through **two parameters** (scale M₀ and phase δ):

\[
\sqrt{m_n} = M_0\left[1 + \sqrt{2}\cos\left(\delta + \frac{2\pi}{3}n\right)\right], \quad n = 1,2,3
\]

For charged leptons: \(M_0 = 313.8\) MeV, \(\delta_e = 0.222\). This allows a "chain" prediction of quark masses (see 1.4).

#### Koide's Higgs Potential
Koide himself (later works, 2005–2020) showed that the formula can be "embedded" in a model with a Higgs field carrying U(3) charge \(\Phi^{a\bar{b}}\):

\[
V(\Phi) = \left[2[\mathrm{tr}(\Phi)]^2 - 3\,\mathrm{tr}(\Phi^2)\right]^2
\]

The minimum of this potential is achieved precisely when the Koide formula holds. This model predicts the existence of new scalar particles beyond the standard Higgs.

### 1.4 Extensions to Quarks

#### Triplet (c, b, t) — Rodejohann and Zhang (2011)
Rodejohann and Zhang ([arXiv:hep-ph/0602134](https://arxiv.org/abs/hep-ph/0602134)) established that the **triplet (charm, bottom, top)** satisfies an analogue of the Koide formula with high precision when using masses in the \(\overline{\mathrm{MS}}\) scheme. This became the starting point for the search for "chains."

#### Rivero's "Waterfall" Chain (2013)
Alejandro Rivero ([arXiv:1111.0062](https://arxiv.org/abs/1111.0062), Scribd 2013) constructed a **sequential chain** of Koide triplets with alternating isospin:

\[
(c,b,t) \to (s,c,b) \to (u,s,c) \to (d,u,s)
\]

Key results:
- The chain **predicts the top quark mass: 173.264 GeV** (using only the masses of the electron and muon as input!), which is close to the measured value ~173.5 GeV
- The new triplet (s, c, b) was discovered for the first time in this work
- The alternating charge scheme resembles the structure of the S₄ cube

#### Status of Triplets for (u,c,t) and (d,s,b)
For "single-color" triplets the results are ambiguous:
- (c, b, t): **works**, Q ≈ 0.669 (∼ 2/3)
- (s, c, b): **works**, Q ≈ 0.675
- (u, c, t): Q ≈ 0.89 — **poor**
- (d, s, b): Q ≈ 0.74 — **moderate**
- (d, s, b) in inverse form (\(1/m_i\)): **works** near 100 TeV renormalization scale

**Diagnosis:** Extension to light quarks is problematic due to uncertainties in their masses and sensitivity to QCD corrections. The formula clearly works better for **pole masses** than for running masses.

---

## 2. Non-Numerological Approaches

### 2.1 Texture Zeros (Fritzsch Matrices)

Harald Fritzsch (1977–2002) proposed a systematic approach: restrict Yukawa matrices by a zero-element condition, which reduces the number of parameters and makes the model predictive.

**Original 6-zero Fritzsch ansatz:**
\[
M_f = \begin{pmatrix} 0 & A_f & 0 \\ A_f^* & 0 & B_f \\ 0 & B_f^* & C_f \end{pmatrix}
\]

**Problem:** The original ansatz is **excluded** by modern data — it predicts too large \(|V_{cb}|\) and too small \(|V_{ub}/V_{cb}|\).

**Modified 4-zero ansatz** (Fritzsch, Xing, 2002; [arXiv:hep-ph/0212195](https://arxiv.org/abs/hep-ph/0212195)) with an added (2,2) element is still **compatible with data**. A full review of texture zeros is given in [arXiv:2305.00069](https://arxiv.org/abs/2305.00069) (2023), where it is shown that the modified asymmetry in the (2,3) and (3,2) elements arising from SU(3)_H horizontal symmetry works.

**Value of the approach:** Texture zeros are an example of **structural constraints** (not fitting): zeros in the Yukawa matrix may be a consequence of horizontal symmetries or the geometry of brane placement in string models.

### 2.2 Froggatt–Nielsen Mechanism (FN)

**Classical formulation (1979):** An additional U(1)_X horizontal symmetry ("flavon") is introduced. Standard Model fields carry charges \(q_i\) under U(1)_X. After spontaneous breaking of this symmetry (via VEV of the "flavon" \(\langle\phi\rangle / M \equiv \epsilon \sim 0.2\)), Yukawa matrix elements acquire power suppressions:

\[
Y_{ij} \sim \epsilon^{|q_i + q_j|}
\]

This explains the **Yukawa hierarchy** without fine-tuning: only a moderate hierarchy in charges is needed.

**Modern state (2024–2025):**

- Ibe, Shirai, Watanabe ([arXiv:2412.19484](https://arxiv.org/abs/2412.19484), accepted in JHEP 2025): **Comprehensive Bayesian systematic analysis** of the entire FN charge space (|q_i| ≤ 10, quark + lepton sector). ~100 viable configurations found. Unexpected conclusion: **negative FN charges** and large intergenerational charge differences are allowed, contrary to usual assumptions. Different configurations give different proton decay predictions — experimentally testable.

- Constantin et al. ([arXiv:2410.17704](https://arxiv.org/abs/2410.17704)): FN models inspired by heterotic string compactification on Calabi–Yau; genetic algorithms for charge search. Reproduce observed mass hierarchies and mixing angles.

- RL agents for finding FN models ([arXiv:2510.25495](https://arxiv.org/abs/2510.25495), 2025): review of RL applications to the flavor problem. The agent finds acceptable models in 93–95% of episodes.

**Main limitation:** The FN mechanism explains **orders of magnitude** of the hierarchy but not exact numerical values: order-one coefficients (\(\mathcal{O}(1)\)) remain free parameters.

### 2.3 Modular Forms and Finite Groups (Feruglio 2017+)

**Breakthrough idea (2017):** Feruglio ([arXiv:1706.08749](https://arxiv.org/abs/1706.08749)) proposed replacing ordinary flavor symmetries with **modular invariance**: Yukawa couplings are modular forms of level N, transforming under finite groups \(\Gamma_N\). The only source of symmetry breaking is the vacuum expectation of a single complex modulus \(\tau\).

| Level N | Finite group |
|-----------|-------------|
| 2 | S₃ |
| 3 | A₄ |
| 4 | S₄ |
| 5 | A₅ |

**Key results by 2026:**

- A₄ models for neutrinos ([arXiv:1808.03012](https://arxiv.org/abs/1808.03012), 2018): predictions for \(\sin^2\theta_{23} > 0.54\), \(\delta_{CP} = \pm(50°\text{–}180°)\), \(m_{ee} \approx 22\) meV — testable in 0νββ experiments.

- S₄'-models for **quarks and leptons simultaneously** ([arXiv:2302.11183](https://arxiv.org/abs/2302.11183), 2023): the first explicit example explaining hierarchies in both sectors via S₄'-modular symmetry near the fixed point \(\tau \sim i\infty\).

- FN + modular symmetries ([JHEP 2021, 07:068](https://ui.adsabs.harvard.edu/abs/2021JHEP...07..068K/abstract)): combining the FN mechanism with modular groups — scaling of Yukawa matrices from FN at reasonable modular parameters.

- Review of modular symmetry aspects ([arXiv:2405.00870](https://arxiv.org/abs/2405.00870), 2024): systematics of predictions in different groups.

**Merits:** The number of free parameters is radically reduced — in the simplest A₄ models a single parameter (\(\tau\)) determines the entire lepton structure.

**Limitations:** The choice of level N and specific group remains unmotivated; strong dependence of predictions on the VEV of the modulus.

### 2.4 Anarchy in the Neutrino Sector

Hall, Murayama, and Weiner ([hep-ph/9911341](https://arxiv.org/abs/hep-ph/9911341), 2000, Phys.Rev.Lett. 84, 2572) proposed **neutrino anarchy**: if all elements of the neutrino and right-handed neutrino Yukawa matrices are random order-one numbers from the string landscape, then large mixing angles are reproduced naturally (unlike quarks).

**Mechanism:** The distribution of mixing angles for random matrices is determined by the Haar measure on U(3) or SO(3), which independently of the weight function predicts large values of \(\theta_{12}, \theta_{23}, \theta_{13}\).

**Status 2024:** The discovery of non-zero \(\theta_{13}\) (Daya Bay, 2012) was initially perceived as confirmation of anarchy. However, the fine neutrino mass hierarchy (moderate normal ordering) requires additional assumptions. A modification with Wishart matrices ([arXiv:1412.4061](https://arxiv.org/abs/1412.4061)) allows a quasi-degenerate spectrum to be realized.

---

## 3. Works 2022–2026: Yukawa Hierarchies from Geometry and AI

### 3.1 F-Theory

F-theory is a 12-dimensional construction reducing to a 4D effective theory. Yukawa couplings arise from topological intersections of 7-branes.

**Key mechanisms:**
- Localization of fermion wave functions at brane intersections
- T-branes (nontrivial vevs of auxiliary fields) break E₈ to SU(5)
- Only one generation gets mass at the classical level; the others through non-perturbative effects

**Hierarchies in global models:** Leontaris and Ross ([arXiv:1009.6000](https://arxiv.org/abs/1009.6000)); Maraniello et al. ([arXiv:1906.10119](https://arxiv.org/abs/1906.10119), 2019) showed that global F-theoretic compactifications generate Yukawa hierarchies of order \(\mathcal{O}(10^5)\) from geometry without instanton corrections.

**2025 work:** Sabir et al. ([arXiv:2407.19458](https://arxiv.org/abs/2407.19458), Phys.Rev.D 111, L071702, 2025): in a supersymmetric Pati–Salam landscape on a T⁶/(Z₂×Z₂)-orientifold IIA, **only two models** were found that exactly reproduce all SM fermion masses and mixings, including a prediction of Dirac neutrino masses \((50.6, 10.6, 6.2) \pm 0.1\) meV — the first precise prediction from string theory.

### 3.2 String Landscape and Statistics

The landscape problem: number of vacua \(\sim 10^{500}\). Nevertheless, the statistical distribution of Yukawa constants is not arbitrary:

- Heterotic standard models: a limited class with reproducible quark masses and CKM (review: [Annual Reviews, 2024](https://www.annualreviews.org/content/journals/10.1146/annurev-nucl-102622-012235))
- Two competing mechanisms: **point localization** (F-theory) vs **volume integrals** (heterotic)

### 3.3 AI and Machine Learning in Search for Yukawa Patterns

#### "Truth and Beauty" in SU(5) (2024)
Work [arXiv:2411.06718](https://arxiv.org/abs/2411.06718) (December 2024) applied ML to compare extensions of minimal SU(5): via the \(\overline{45}\) Higgs representation or via the 24 representation. Optimization of the loss functional (determinant ratio of mass matrices) showed that the **24-Higgs approach requires smaller deviations** from the minimal model.

#### ALBERT Agent (2026)
Alexander et al. ([arXiv:2603.28935](https://arxiv.org/abs/2603.28935), March 2026): a neuro-symbolic RL agent trained exclusively on LEP data **without direct evidence of the top quark** rediscovers the Standard Model and predicts the top mass: **178.9 ± 5.0 GeV**. The key difference from previous work: a formal grammar excludes LLM "hallucinations."

#### Review of RL for Flavor Physics (2025)
Yarnetti and Meloni ([arXiv:2510.25495](https://arxiv.org/abs/2510.25495), October 2025): systematic review of RL approaches to FN models. RL agent:
- Finds 4630 unique viable solutions for one U(1) symmetry
- 57,807 solutions for two U(1)
- Reproduces previously proposed models from the literature

#### RL for SM Phenomenology in SU(5) (2024, SMEFT)
Froggatt–Nielsen meets SMEFT ([arXiv:2402.16940](https://arxiv.org/abs/2402.16940), 2024): matching FN theories onto SMEFT operators opens a path to collider testing.

---

## 4. "Derivation" vs "Fitting": Falsifiability Criteria

### 4.1 Fundamental Difference

| Criterion | Fitting | Derivation |
|-----------|---------|------------|
| Number of free parameters | ≥ number of predicted quantities | < number of predicted quantities |
| New predictions | None | Yes (before the experiment) |
| Falsifiability | Weak | Strong |
| Structural motivation | Absent | Present (symmetry, geometry) |

### 4.2 Scale for Evaluating Mass Formulas

**Purely numerological level (0/5):**  
Formula with number of parameters ≥ number of data. Example: fitting 9 fermion masses with 9 free parameters of the Yukawa matrix.

**Phenomenological level (1/5):**  
Formula with number of parameters < number of data, but without theoretical motivation. Example: the original Koide formula — 1 constraint on 3 masses, 2 parameters determine 3 numbers. However, Q = 2/3 lacks a theoretical explanation.

**Structural level (2/5):**  
Constraints follow from symmetry (texture zeros), but the symmetry itself is not derived. Example: 4-zero Fritzsch ansatz.

**Mechanistic level (3/5):**  
Hierarchies follow from a specific mechanism (FN, seesaw), but mechanism parameters are fitted. Example: Bayesian FN [arXiv:2412.19484].

**Geometric level (4/5):**  
Couplings are derived from compactification geometry (F-theory, modular forms) without order-one free parameters. Example: [arXiv:2407.19458] — neutrino mass prediction.

**Fundamental level (5/5):**  
A single geometric object generates the entire spectrum without free parameters. Not yet explicitly achieved (claimed in [Zenodo:19592588], but not verified by the community).

### 4.3 Criteria for Evaluating Predictivity

By Popper–Lakatos, a good theory of fermion masses must:
1. **Predict before the experiment** — the Koide formula (1982) correctly predicted \(m_\tau\) before precise measurements
2. **Forbid configurations** — complete Yukawa freedom forbids nothing
3. **Explain accidental coincidences** — why Q = 2/3, not 0.7?
4. **Reproduce everything, not just a part** — a model giving lepton masses but not quark masses is incomplete

---

## 5. Coxeter Group H₄ and the 600-Cell: Precedents

### 5.1 Context: What Are the 600-Cell and H₄?

The 600-cell (hexacosichoron) is a regular four-dimensional polytope with 120 vertices, 720 edges, 1200 faces, and 600 tetrahedral cells. Its symmetry group is the Coxeter group **H₄** of order 14,400. It is related to the scandal of simple roots, the golden ratio, and the icosahedral group H₃.

### 5.2 Prior Work with 4D Polytope Geometry

#### Feng's theory (2017)
In [TSIJOURNAL](https://www.tsijournals.com/articles/b-fengs-theory-the-prediction-of-mass-spectrum-of-elementary-particles-and-the-confidence-of-at-least-4d-spacetime-part-13505.html) (2017) Feng uses the **16-cell** (one of 6 regular 4D polytopes) as a basis for the mass spectrum. The mass scale is computed through the angle of projection 4D → 3D. The formula gives results within a few percent of experimental values — but with a free parameter \(\delta\).

#### Connection of the 600-Cell to Elementary Particles (Chaos, Solitons & Fractals, 2007)
El Naschie ([doi:10.1016/S0960-0779(06)00569-8](https://www.sciencedirect.com/science/article/abs/pii/S0960077906005698)): estimation of the number of elementary particles through the topology of the 120-cell and 600-cell — a purely numerological attempt, unrelated to masses.

#### Lisi E₈ Theory (2007)
Lisi ([arXiv:0711.0770](https://arxiv.org/abs/0711.0770)) placed all SM particles in the E₈ structure. Criticism by Distler and Garibaldi (2009, Commun.Math.Phys.) proved that **it is impossible to embed all three generations in E₈** without mirror fermions. No mass scaling from E₈.

#### Connes's Construction (1996–2019): Spectral Triplet for the SM
**Alain Connes** and collaborators showed ([Noncommutative Geometry and the Standard Model, Connes & Chamseddine, 2007](https://ncatlab.org/nlab/show/spectral+triple)) that SM+gravity arises from a spectral triplet \((A_F, H_F, D_F)\), where \(A_F = \mathbb{C} \oplus \mathbb{H} \oplus M_3(\mathbb{C})\). In this approach the finite algebra is **set axiomatically**, not derived from polytope geometry.

#### Visualization of H₄ in ToE Projects (2024)
Website theoryofeverything.org ([publication September 2024](http://theoryofeverything.org/theToE/2024/09/17/the-h4-600-cell-in-all-its-beauty/)): visualization of the 600-cell with 1200 unit edges, 2400 faces; discussion of H₄→E₈ projections, golden ratio in distances. No mass computation.

### 5.3 trinity-s3ai Work (April 2026) — First Analysis

Preprint ([Zenodo:19592588](https://zenodo.org/records/19592588), April 2026) — **the first attempt in the world literature** to derive the SM fermion mass spectrum from the spectral triplet of the H₄ group on the 600-cell:

**Architecture:** Hilbert space \(H_F = \ell^2(V) \otimes \mathbb{C}^4\), dim = 480 (120 vertices × 4). Real structure operators J and parity γ.

**Algebra derivation:** The representation of H₄ on 120 vertices decomposes into irreducible representations of dimensions {1, 4, 5, 10, 16, 20, 30, 34}. The commutant of H₄ in End(H_F): ⊕ M₂(ℂ); introducing J and γ reduces to:
\[A_F = \mathbb{C} \oplus \mathbb{H} \oplus M_3(\mathbb{C})\]

**Three generations via the 53-cycle:** The positive spectrum of D_F has **53 distinct eigenvalues** of multiplicity 2. A spectral automorphism U of order 53 (U⁵³ = I) gives three orbits under the H₄ action: of sizes 22, 8, 1 — interpreted as three generations.

**Mass formula:**
\[m_k = m_0 \cdot \exp\!\left(\beta_k \cdot \csc\!\left(\frac{\pi \alpha_k}{53}\right)\right), \quad \alpha_1 = 22,\; \alpha_2 = 8,\; \alpha_3 = 1\]

At \(m_0 = m_e = 0.511\) MeV: \(m_\mu = 104.2\) MeV (exp.: 105.7), \(m_\tau = 1748\) MeV (exp.: 1776).

**Accuracy estimate:** The prediction for \(m_\mu\) is off by **~1.4%**, \(m_\tau\) by **~1.6%**. This is significantly better than random, but does not reach Koide precision (9.3 ppm).

**Status in the literature:** The work is posted on Zenodo (unreviewed preprint, April 2026). At the time of writing this review it is **not cited** in peer-reviewed journals. Claims of "zero free parameters" require independent verification — in particular, the choice of \(\beta_k\) and the exponential function requires justification.

**What is new compared to Connes:** Connes set \(A_F\) axiomatically; trinity-s3ai derives \(A_F\) from H₄ representations. This is a **geometric origin** of the algebra — a real contribution, if the mathematics is correct.

---

## 6. Lessons for trinity-s3ai

### Lesson 1: Precision Is Not Proof, but a Necessary Condition

The Koide formula holds with 9.3 ppm precision. The prediction of \(m_\tau\) from the 600-cell is off by 1.6% = **170,000 ppm**. The gap is five orders of magnitude. Until the precision is matched, it is premature to speak of "competing" with the Koide formula.

**Action:** Improve the mass formula. Consider QCD corrections, renormalization group running from the Planck scale to the electroweak scale.

### Lesson 2: "Zero Parameters" Requires a Strict Definition

In the claim "no free parameters" lies a subtlety: the choice of Hilbert space dimension, the form of the Dirac operator, and the exponential function in the mass formula are also parametric choices. Independent verification is needed that all these choices are uniquely dictated by H₄ geometry.

**Action:** Provide a complete uniqueness theorem with explicit lemma steps, verifiable by computer.

### Lesson 3: The 53-Cycle Is a Strong Structural Feature Requiring Explanation

The primality of 53 and its role as the order of the spectral automorphism is a non-trivial mathematical statement. The orbit split (22, 8, 1) resembles the split 31 = 22 + 8 + 1 in the representation theory of A_4 (but does not coincide). It is necessary to exclude the possibility that 53 is a random artifact of the Hilbert space dimension.

**Action:** Independently verify the D_F spectrum numerically. Publish the diagonalization source code.

### Lesson 4: Compare Explicitly with Connes

The Connes–Chamseddine approach is well known to the community. The trinity-s3ai work must **explicitly explain what is new**: not just "we also use a spectral triplet," but "we derive the algebra A_F from H₄, whereas Connes postulates it." This is real progress — it needs to be emphasized.

**Action:** Dedicate a separate section to comparison with Connes-Chamseddine (2006/2019) and explanation of why H₄ derives what they take axiomatically.

### Lesson 5: The Koide Formula Is a "Checkpoint," Not a Competitor

The Koide formula is a test that any successful theory of lepton masses must satisfy. If the H₄ theory gives \(m_\mu/m_e \approx 204\) instead of 206.77 — this is not "close," it is a systematic error.

**Action:** Check whether the model predicts Q = 2/3 as an exact relation or as an approximation. If not, understand why.

### Lesson 6: Quarks Are Harder Than Leptons — Do Not Bypass

All successful lepton mass models (Koide, A₄, FN) encounter difficulties when moving to quarks due to QCD corrections, uncertainties in light quarks, and scale dependence. Rivero's "waterfall" chain is the best numerological example of extension to quarks, but even it requires special conditions (isospin alternation).

**Action:** Calculate quark mass predictions in the H₄ model. Compare with PDG 2024 at the M_Z scale and in pole masses.

### Lesson 7: Neutrinos — a Predictive Window

Neutrino masses are bounded from above (Planck + DESI: \(\sum m_\nu < 0.06\) eV at 95% CL) and from below (oscillations). The absolute scale is not measured. The H₄ model predicts \(E_0 = hf_0 = 0.053\) eV as the neutrino scale. This is **testable** in KATRIN, Project 8.

**Action:** Compute full neutrino mass predictions and the PMNS matrix. Compare with NuFIT 6.0 (2024).

### Lesson 8: "Structural" vs "Accidental" Coincidence

The number 53 in the 600-cell spectrum may turn out to be a random coincidence of 53 eigenvalues with no deep meaning. Check: compute the spectrum of analogous spectral triplets on other 4D polytopes (120-cell, 24-cell, 16-cell) — if "generations" are found there too, an explanation is needed.

**Action:** Conduct a comparative analysis of spectra for all regular 4D polytopes.

### Lesson 9: Publication in a Peer-Reviewed Journal Is a Critical Step

A Zenodo preprint is a good start, but without peer review claims of "full SM derivation" will remain outside scientific discourse. Target journals: **Physical Review D** (phenomenology), **Journal of High Energy Physics** (theory), **Communications in Mathematical Physics** (rigorous mathematics).

**Action:** Focus on **one concrete result** (for example, derivation of algebra A_F from H₄), and present it as a standalone article with full proofs.

### Lesson 10: Falsifiability — Through Predictions, Not Fitting

The best way to stand out is to predict **unobserved numbers** before they are measured. Candidates:
- Exact sum of neutrino masses (within 0.05–0.12 eV)
- δ_CP (CP phase in the PMNS matrix) — not yet precisely measured
- Mass of the lightest neutrino

**Action:** Publish specific numerical predictions with indication of experimental tests.

### Lesson 11: Comparison with Modular Models Is Inevitable

Modular A₄/S₄ models (Feruglio 2017+) are the closest competitors in spirit: one parameter (τ) determines the structure. It is necessary to explain why H₄ is better (or different) at explaining the data.

**Action:** Compute correlations of H₄ model predictions (e.g., θ₂₃ vs δ_CP) and compare with predictions of the best S₄ models.

### Lesson 12: Mechanism, Not Just Result

The FN mechanism is valuable not for the formula but for the **mechanism** — exponential suppression from the power of the vacuum expectation. Similarly, the "53-cycle" in H₄ needs a dynamic explanation: why a spectral automorphism, not another symmetry? What is the physical meaning of multiplicity 2?

**Action:** Interpret U₅₃ in terms of physics (what charge of operators does it correspond to? Is it related to a discrete generation symmetry?)

### Lesson 13: Advantage of H₄ — No Mirror Fermions?

Criticism of Lisi (E₈ theory): Distler–Garibaldi proved that E₈ inevitably produces mirror fermions. If H₄ (via the 53-cycle) **avoids** this problem, this is a crucial advantage. It is necessary to explicitly show the chirality of particles in the model.

**Action:** Prove (or refute) the absence of mirror generations in the H₄ spectral triplet.

### Lesson 14: Scale f₀ = 12.8 THz — a Testable Prediction

The vacuum frequency 12.8 THz (E₀ = 0.053 eV) is a faint infrared signal. It coincides with the neutrino mass scale. If E₀ is interpreted as the minimal neutrino mass, then \(m_{\nu,\min} = 0.053\) eV — this is tested by KATRIN (current upper bound ~0.45 eV) and Future Circular Collider.

**Action:** Make this prediction explicit and testable; add an "Experimental Tests" section.

### Lesson 15: Do Not Overestimate the Zenodo Result (April 2026)

Claims like "full SM derivation," "proof of the Yang–Mills hypothesis," and "uniqueness of H₄" in a single preprint are a red flag for reviewers. The history of physics knows examples of ambitious programs (Lisi E₈, Connes NCG, superstrings 1986) where each step required years of verification.

**Action:** Break the program into **autonomous verifiable statements**. Publish each separately with full proofs.

---

## 7. List of Sources

### Koide Formula and Extensions

1. **Koide, Y. (1982)**: Original article (1981–1982) — historical reference via Rivero–Gsponer review [arXiv:hep-ph/0505220](https://arxiv.org/abs/hep-ph/0505220).

2. **Rivero, A., Gsponer, A. (2005)**. "The strange formula of Dr. Koide". [arXiv:hep-ph/0505220](https://arxiv.org/abs/hep-ph/0505220).

3. **Foot, R. (1994)**. "A note on Koide's lepton mass relation". [arXiv:hep-ph/9402242](https://arxiv.org/abs/hep-ph/9402242).

4. **Sumino, Y. (2009)**. "Family Gauge Symmetry and Koide's Mass Formula". Phys.Lett.B. [arXiv:0812.2090](https://arxiv.org/abs/0812.2090).

5. **Rodejohann, W., Zhang, H. (2006)**. "On the Koide-like Relations for Running Masses". [arXiv:hep-ph/0602134](https://arxiv.org/abs/hep-ph/0602134).

6. **Rivero, A. (2013)**. "Koide equations for quark mass triplets". [Academia.edu](https://www.academia.edu/33514663/Koide_equations_for_quark_mass_triplets); "Koide and the mass of the proton". [arXiv:1111.0062](https://arxiv.org/abs/1111.0062).

7. **Liang, Sun (2021)**. "Modified Koide formula from flavor nonets". Nucl.Phys.B 972. [arXiv:2007.05878](https://arxiv.org/abs/2007.05878).

8. **Minimization theorem for Koide ratio (2026)**. [arXiv:2605.09651](https://arxiv.org/abs/2605.09651).

9. **Updated Running Parameters 2024 PDG**. [arXiv:2510.01312](https://arxiv.org/abs/2510.01312).

### Texture Zeros and Fritzsch

10. **Fritzsch, H., Xing, Z.-Z. (2002)**. "Four-Zero Texture of Hermitian Quark Mass Matrices". [arXiv:hep-ph/0212195](https://arxiv.org/abs/hep-ph/0212195).

11. **Modified Fritzsch ansatz (2023)**. [arXiv:2305.00069](https://arxiv.org/abs/2305.00069).

12. **CKM mixings, five texture zeros (2021)**. Phys.Rev.D 104, 075009. [doi:10.1103/PhysRevD.104.075009](https://link.aps.org/doi/10.1103/PhysRevD.104.075009).

### Froggatt–Nielsen Mechanism

13. **Ibe, Shirai, Watanabe (2024)**. "Comprehensive Bayesian Exploration of Froggatt-Nielsen Mechanism". [arXiv:2412.19484](https://arxiv.org/abs/2412.19484). JHEP 2025.

14. **Constantin, Fraser-Taliente et al. (2024)**. "Fermion Masses and Mixing in String-Inspired Models". [arXiv:2410.17704](https://arxiv.org/abs/2410.17704).

15. **Mapping FN solutions (2025)**. Phys.Rev.D 111, 015042. [doi:10.1103/PhysRevD.111.015042](https://link.aps.org/doi/10.1103/PhysRevD.111.015042).

16. **Froggatt–Nielsen meets SMEFT (2024)**. [arXiv:2402.16940](https://arxiv.org/abs/2402.16940).

### Modular Symmetries

17. **Feruglio, F. (2017)**. "Are neutrino masses modular forms?" [arXiv:1706.08749](https://arxiv.org/abs/1706.08749). (Key work, birth of the field.)

18. **Novichkov et al. (2018)**. "Modular A₄ invariance and neutrino mixing". [arXiv:1808.03012](https://arxiv.org/abs/1808.03012).

19. **S₄'-models for quarks and leptons (2023)**. [arXiv:2302.11183](https://arxiv.org/abs/2302.11183).

20. **Aspects of Modular Flavor Symmetries (2024)**. [arXiv:2405.00870](https://arxiv.org/abs/2405.00870).

21. **FN + Modular origin of mass hierarchy (2021)**. JHEP. [NASA ADS](https://ui.adsabs.harvard.edu/abs/2021JHEP...07..068K/abstract).

### Neutrino Anarchy

22. **Hall, Murayama, Weiner (2000)**. "Neutrino Mass Anarchy". Phys.Rev.Lett. 84, 2572. [arXiv:hep-ph/9911341](https://arxiv.org/abs/hep-ph/9911341).

23. **Jeong, Kitajima, Takahashi (2015)**. "Degenerate spectrum in neutrino mass anarchy with Wishart matrices". [arXiv:1412.4061](https://arxiv.org/abs/1412.4061).

24. **Neutrino Mixing Anarchy: Alive and Kicking (2012)**. [arXiv:1204.1249](https://arxiv.org/abs/1204.1249).

### F-Theory and Landscape

25. **Leontaris, Ross (2010)**. "Yukawa couplings and fermion mass structure in F-theory GUTs". [arXiv:1009.6000](https://arxiv.org/abs/1009.6000).

26. **Yukawa hierarchies at E₈ point in F-theory (2015)**. [arXiv:1503.02683](https://arxiv.org/abs/1503.02683).

27. **Global F-theory Yukawa hierarchies (2019)**. [arXiv:1906.10119](https://arxiv.org/abs/1906.10119).

28. **Sabir et al. (2025)**. "Fermion masses and mixings in string theory with Dirac neutrinos". Phys.Rev.D 111, L071702. [arXiv:2407.19458](https://arxiv.org/abs/2407.19458).

29. **Standard Model from String Theory (2024)**. Annual Reviews Nucl.Part.Sci. [doi:10.1146/annurev-nucl-102622-012235](https://www.annualreviews.org/content/journals/10.1146/annurev-nucl-102622-012235).

### AI / ML in Particle Physics

30. **ML for SU(5) GUT (2024)**. "Truth, beauty, and goodness in grand unification". [arXiv:2411.06718](https://arxiv.org/abs/2411.06718).

31. **ALBERT — autonomous discovery of particle theories (2026)**. [arXiv:2603.28935](https://arxiv.org/abs/2603.28935).

32. **RL for flavor physics (2025)**. [arXiv:2510.25495](https://arxiv.org/abs/2510.25495).

### H₄ / 600-Cell / Connes

33. **Connes, A., Chamseddine, A. (2007+)**. SM spectral triplet. [nLab: spectral triple](https://ncatlab.org/nlab/show/spectral+triple).

34. **trinity-s3ai (2026)**. "600-Cell Spectral Triple Series". [Zenodo:19592588](https://zenodo.org/records/19592588). (Preprint, unreviewed.)

35. **Lisi, A.G. (2007)**. "An Exceptionally Simple Theory of Everything". [arXiv:0711.0770](https://arxiv.org/abs/0711.0770).

36. **Distler, Garibaldi (2009)**. "There is no 'Theory of Everything' inside E₈". Commun.Math.Phys.

37. **Theory of Everything H₄ visualization (2024)**. [theoryofeverything.org](http://theoryofeverything.org/theToE/2024/09/17/the-h4-600-cell-in-all-its-beauty/).

---

*Review compiled using arXiv, Zenodo, PDG 2024, Wikipedia (Koide formula) and refereed publications. All links checked for accessibility. Opinions on the status of the trinity-s3ai work are based on analysis of the publicly available preprint and do not constitute a formal review.*
