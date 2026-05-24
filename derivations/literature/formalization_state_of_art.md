# State of Physics Formalization in Proof Assistants (2026)
## Review for the trinity-s3ai project (Coq/Rocq 9.1 + coq-interval)

*Compiled: July 2026*

---

## Introduction

This review covers the current state of formalization of mathematics and physics in
proof assistants — primarily Coq/Rocq and Lean 4 — as applied to the tasks of the
trinity-s3ai project: numerical fitting of physical constants, proofs using
coq-interval, and honest separation of mathematical theorems from physical hypotheses.

---

## 1. Real Analysis in Coq/Rocq: Current State (2025–2026)

### 1.1 Coq Standard Library

The Coq standard library contains an axiomatic formalization of real
numbers (not constructive). It provides the basics: limit of a sequence, derivative
via `derivable`, Riemann integral. A serious drawback is the use of dependent
types for limits and derivatives, which makes reasoning cumbersome.

**Reference:** [Coquelicot: A User-Friendly Library of Real Analysis for Coq](https://guillaume.melquiond.fr/doc/14-mcs.pdf)

### 1.2 Coquelicot (version 3.x)

A conservative extension of the standard library. Key improvements:
- Total functions instead of dependent types for limits, derivatives, integrals.
- Extended limits: `R_bar = R ∪ {-∞, +∞}`.
- Partial derivatives and parametric integrals.
- Automation of differentiability proofs.
- Support for multidimensional functions.

Compatible with Coq 8.5–9.x. Used by coq-interval as a dependency.

**Example:** In Coquelicot, Bessel functions and the one-dimensional wave equation are formalized.

**Limitations:** No differential forms, manifolds, or Lie groups.

**Reference:** [http://coquelicot.saclay.inria.fr](http://coquelicot.saclay.inria.fr)

### 1.3 MathComp Analysis (version 1.9.0, February 2025)

A real analysis library based on Mathematical Components (MathComp 2.5.0, October 2025).
Distinguished by:
- Classical mathematics (LEM, axiom of choice).
- Filters instead of ε-δ for limits (following Isabelle/HOL).
- Tight integration with the MathComp algebraic structure hierarchy.
- Active development (44 releases by 2025).

Contains: measures, Lebesgue integrals, topology, normed spaces,
foundations of probability theory. Supports Rocq 9.1+.

**Reference:** [https://github.com/math-comp/analysis](https://github.com/math-comp/analysis)

### 1.4 Differential Forms in Coq/Rocq

**Status (2026): absent in the Coq/Rocq ecosystem.**

There is no library for differential forms on manifolds in Coq. Exterior algebras
over rings exist in MathComp (`Algebra/`), but exterior calculus on manifolds is
an open problem.

### 1.5 Manifolds and Lie Groups in Coq

Coq/Rocq lacks a full-fledged library of smooth manifolds, de Rham maps,
or Lie groups. This is a significant gap compared to Lean 4.

---

## 2. Lean 4 / Mathlib: Differential Geometry, Lie Theory, Representation Theory

### 2.1 Smooth Manifolds (Mathlib)

Lean 4 Mathlib contains the most advanced formalization of
differential geometry among proof assistants today:

- **Smooth manifolds with corners** — manifolds with corners are included in the definition,
  which avoids duplicating code for manifolds with boundary.
- **`MDifferentiableAt I I' f x`** — differentiability of maps between manifolds.
- **`mfderiv I I' f x`** — Fréchet derivative on a manifold (as a continuous linear
  map between tangent spaces).
- **`tangentMap I I' f`** — derivative as a map between tangent bundles.
- Integration with `fderiv` (Fréchet derivative in vector spaces).

**Reference:** [Mathlib.Geometry.Manifold.MFDeriv.Defs](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Geometry/Manifold/MFDeriv/Defs.html)

### 2.2 Differential Forms in Lean 4 (Mathlib)

Starting from 2024, Mathlib acquired a formalization of the exterior derivative:

```
Mathlib.Analysis.Calculus.DifferentialForm.Basic
```

The exterior derivative `extDeriv` is defined for differential n-forms on normed
spaces. `d ∘ d = 0` is proven. Compatibility with pullback is supported.

**Reference:** [Exterior derivative of a differential form](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/Calculus/DifferentialForm/Basic.html)

**Limitation:** Forms on normed spaces, not on arbitrary manifolds
(work in progress, 2025–2026).

### 2.3 Lie Algebras and Modules (Mathlib)

Lean 4 Mathlib contains an extensive theory of Lie algebras:

- `Mathlib.Algebra.Lie.Basic` — Lie rings, Lie algebras over commutative rings,
  Lie modules, morphisms, Lie bracket, Jacobi identity.
- Johan Commelin (May 2024) proved a number of important structural properties of Lie algebras.
- Work on `solvable` and `nilpotent` Lie algebras, classification of low-dimensional
  solvable Lie algebras (May 2025, [arXiv:2505.19975](https://arxiv.org/html/2505.19975v1)).
- Vertex algebras (`Mathlib.Algebra.Vertex`): Scott Carnahan, January 2025
  ([Lean Together 2025 talk](https://www.youtube.com/watch?v=bmqEmc1nkkU)) — work
  toward affine Lie algebras in Mathlib.

### 2.4 Representation Theory (Mathlib)

Module `Mathlib.RepresentationTheory`:
- `Basic`, `Action`, `Character`, `FDRep`, `Irreducible`, `Maschke`, `Semisimple`,
  `Tannaka`, `Induced`, `Coinduced`, etc.
- Maschke's theorem, characters, semisimple representations, Tannaka's theorem.

**Reference:** [Mathlib module list](https://leanprover-community.github.io/mathlib4_docs/Mathlib)

### 2.5 Should trinity-s3ai Migrate to Lean 4?

**Arguments in favor of migration:**
- Mathlib contains differential forms, manifolds, Lie groups — none of which exist in Coq.
- The AI tools ecosystem (Lean Copilot, DeepSeek-Prover-V2, Goedel-Prover-V2,
  AlphaProof) is primarily aimed at Lean 4.
- Active community, >210,000 theorems by 2025.
- PhysLib/HepLean for physics — actively developed in Lean 4.

**Arguments against (for trinity-s3ai):**
- coq-interval is a unique Coq tool without a direct analogue in Lean 4 of comparable
  maturity (LeanCert exists but is less mature).
- Existing Rocq 9.1 code requires significant effort to migrate.
- Gappa and Flocq are mature tools for numerical proofs in Coq.
- If the main task is numerical certificates (coq-interval), staying in Rocq is reasonable.

**Recommendation:** Use Rocq for numerical proofs (coq-interval), but
closely monitor Lean 4 / Mathlib for future migration of geometric parts.

---

## 3. Existing Projects for Formalizing Physics

### 3.1 Special Relativity (Coq)

A formalization of special relativity based on the axiomatic system
SpecRel (Andréka–Madarász–Németi–Székely) was carried out in Coq
([arXiv, Harvard](https://dash.harvard.edu/bitstreams/4160f812-a67d-42c4-9261-c159ade7cd86/download)).
Axioms: bodies, photons, observation predicate `W`. Sufficiency for
deriving the main results of special relativity is shown.

**General Relativity:** No complete formalization of GR in Coq/Rocq. Berghofer
(from Graz) works on principles of gauge field theory, but not on formalization
of Einstein's equations in a proof assistant.

### 3.2 Quantum Mechanics and Quantum Computing

- **Lean 4 (Physlib/HepLean, Tooby-Smith):** Wick's theorem is formally verified
  ([physlib.io](https://physlib.io)). An error was found in a paper on 2HDM (2006),
  confirmed by the authors — the first major non-trivial case of error detection
  in a physics paper through formalization
  ([arXiv:2603.08139](https://arxiv.org/abs/2603.08139), March 2026).
- **Lean 4 (QFT):** Free scalar QFT in 4D Euclidean space is formalized
  (Glimm–Jaffe / Osterwalder–Schrader axioms). Project mrdouglasny/OSforGFF
  ([arXiv:2603.15770](https://arxiv.org/html/2603.15770v1), 2026). Initially three
  axioms were `sorry`, later all were proven or removed.
- **Lean 4 (LeanForPhysics / Lean4PHYS):** The first benchmark for physics problems
  in Lean 4 (200 problems from textbooks). PhysLib contains foundations of mechanics, quantum
  physics ([ICLR 2026](https://openreview.net/forum?id=wQ2jyFz18H)).
- **Lean 4 (chemistry):** [Formalizing chemical physics using the Lean theorem prover](https://pubs.rsc.org/en/content/articlehtml/2024/dd/d3dd00077j)
  — formalization of chemical physics, RSC 2024.
- **MerLean:** Auto-formalization of quantum circuits in Lean 4
  ([arXiv:2602.16554](https://arxiv.org/html/2602.16554v1), 2026).

### 3.3 Standard Model Lagrangian: Formalized?

**No complete formalization exists.** No project formalizes the full SM Lagrangian
(with couplings, chiral fermions, Higgs mechanism) in a proof assistant.

HepLean/Physlib (Lean 4) is the closest project. It contains sectors:
quantum chromodynamics, Higgs mechanism, electroweak interaction — partially.
The work on 2HDM revealed an error in the literature, confirming the value of formalization.

### 3.4 Spectral Action / Connes's NCG

**Status: early stage.**

- Christoph Stephan (Potsdam), talk February 2026
  ([agenda.infn.it/event/49101](https://agenda.infn.it/event/49101/)):
  project to formalize NCG in Lean 4, long-term goal — Connes's reconstruction theorem.
  Project is at an **early stage**.
- The Lean community has already laid foundations (Lie groups, operator algebras).
- No completed formalizations of the spectral action or the Connes–Lott Lagrangian exist.

---

## 4. CoqInterval / coq-interval: Capabilities and Limitations

### 4.1 What coq-interval Can Do

The `interval` tactic proves goals of the form `c1 ≤ e ≤ c2` for expressions containing:

| Constants | `PI`, numeric literals |
|-----------|------------------------|
| Arithmetic | `+`, `-`, `*`, `/`, `pow` |
| Elementary functions | `sqrt`, `exp`, `ln`, `cos`, `sin`, `tan`, `atan` |
| Floating-point arithmetic | `Flocq` operators `Zfloor`, `Zceil`, `ZnearestE`, `round` |

**For π:** coq-interval knows `PI` as a constant and can prove strict
bounds, for example:
```coq
Goal 3141592 / 1000000 < PI < 3141593 / 1000000.
Proof. interval. Qed.
```

**For e:** via `exp 1`. Similarly, arbitrarily tight bounds can be proven.

**Integrals:** the `integral` tactic for `RInt` with constant bounds and
well-behaved integrand. Improper integrals via `RInt_gen`.

**Performance (2024):** A fast binary64 implementation of exp was integrated,
providing ×20 speedup compared to the previous version
([ITP 2024, LIPIcs.ITP.2024.14](https://drops.dagstuhl.de/storage/00lipics/lipics-vol309-itp2024/LIPIcs.ITP.2024.14/LIPIcs.ITP.2024.14.pdf)).

**Reference:** [coqinterval.gitlabpages.inria.fr](https://coqinterval.gitlabpages.inria.fr)

### 4.2 Limitations of coq-interval

| Limitation | Description |
|------------|-------------|
| Sine/cosine domain | Argument must be in `[-2π, 2π]`; outside this domain — trivial bounds `[-1,1]` |
| Tangent argument | Only `(-π/2, π/2)` |
| Powers | `pow` and `powerRZ` require a numeric exponent |
| Variables | Variables are only allowed through hypotheses of the form `c1 ≤ t ≤ c2` |
| Compound expressions | For large nesting depth, computations may be slow |
| Maximum depth | Default 15 for `interval`, 5 for `interval_intro` |
| Integrals | Up to 100 subdivisions by default (`i_fuel`) |
| No symbolic computation | Cannot reason about the **structure** of expressions, only numerical evaluation |
| No multidimensional interpolation | Does not support integrals over two or more variables |

### 4.3 Transcendental Numbers: What Is and Is Not Possible

**Possible:** prove `|π - 3.14159265358979| < 10⁻¹⁵` and similar inequalities.
**Not possible:** prove the transcendence of π or e (this requires the Lindemann–Weierstrass theory,
which exists neither in Coq nor in MathComp Analysis).
**Possible:** use π as a constant in expressions and obtain strict numerical bounds.

---

## 5. Best Practices for Formalizing Physical Statements

### 5.1 Separation of Mathematics and Physics

The key principle is to explicitly distinguish three levels:

```
Level 1: Mathematical theorem (proven)
Level 2: Physical hypothesis (stated, not proven)
Level 3: Numerical agreement (certified by coq-interval)
```

**Recommended schema in Rocq:**

```coq
(** PHYSICAL HYPOTHESIS: m_e/m_p mass ratio is taken from experiment.
    Source: CODATA 2022. Value confirmed experimentally to precision
    ~3×10⁻¹¹. Status: [PHYSICAL_INPUT]. *)
Hypothesis mass_ratio_experimental :
  1836183 / 1000000 <= m_e_over_m_p <= 1836184 / 1000000.

(** MATHEMATICAL THEOREM: from hypothesis mass_ratio_experimental follows... *)
Theorem bound_on_alpha :
  mass_ratio_experimental ->
  0 <= alpha - alpha_predicted <= 1/1000.
Proof. interval. Qed.
```

### 5.2 Taxonomy of `Admitted`

It is recommended to tag each `Admitted` with one of the following tags in the docstring:

| Tag | Meaning |
|-----|---------|
| `[PHYSICAL_AXIOM]` | Physical hypothesis about nature, not a mathematical theorem |
| `[NUMERICAL_FIT]` | Result of numerical fitting; coq-interval can check bounds |
| `[MATH_TODO]` | Mathematically true, but not formally proven |
| `[OPEN_PROBLEM]` | Open mathematical problem |
| `[LIBRARY_GAP]` | True, but the needed lemma is missing from the library |

**Example:**

```coq
(** The spectral action is minimal at the concurrence point for the given parameters.
    STATUS: [NUMERICAL_FIT] Verification by the interval method is available,
    but a formal proof of minimality requires [LIBRARY_GAP]
    — variational calculus is not formalized in Rocq. *)
Admitted.
```

### 5.3 Honest Formulation of Numerical Agreement

Instead of `"prediction matches experiment"`, use:

```coq
(** Numerical agreement: |M_predicted - M_observed| / M_observed ≤ ε.
    [NUMERICAL_FIT] ε = 1.2×10⁻⁵, source: PDG 2024 mass table.
    Mathematical theorem: Theorem numerical_agreement below.
    Physical interpretation: NOT a consequence of the theorem;
    depends on physical assumptions marked as [PHYSICAL_AXIOM]. *)
Theorem numerical_agreement :
  Rabs (M_predicted - M_observed) / M_observed <= 12 / 1000000.
Proof. interval. Qed.
```

### 5.4 Lessons from the OSforGFF Project (QFT in Lean 4, 2026)

From the paper [arXiv:2603.15770](https://arxiv.org/html/2603.15770v1):

1. Start with `sorry` stubs, replace gradually.
2. Key definitions must be correct from the beginning — an error in a definition
   rewrites the entire project.
3. Maintain `axioms.md` — a living list of all `Admitted`/`sorry` with explanations.
4. Break long proofs into lemmas, not monoliths.
5. Cross-check auxiliary lemmas with multiple tools.

---

## 6. AI-Assisted Theorem Proving (2024–2026)

### 6.1 Overview of Key Systems

| System | Platform | Result (2025–2026) |
|--------|----------|----------------------|
| **AlphaProof** (Google DeepMind) | Lean 4 | Silver medal IMO 2024; [Nature 2025](https://www.nature.com/articles/s41586-025-09833-y) |
| **DeepSeek-Prover-V2-671B** | Lean 4 | 88.9% on MiniF2F; 49/658 Putnam; [arXiv:2504.21801](https://arxiv.org/abs/2504.21801) |
| **Goedel-Prover-V2-32B** | Lean 4 | 90.4% on MiniF2F; 86/644 Putnam; [OpenReview 2026](https://openreview.net/forum?id=j4C0nALrgK) |
| **Lean Copilot** | Lean 4 | Reduces manual input to 2.08 steps; [arXiv:2404.12534](https://arxiv.org/abs/2404.12534) |
| **Claude Opus 4.6 + rocq-mcp** | **Rocq** | 10/12 Putnam 2025 problems in Rocq; [arXiv:2603.20405](https://arxiv.org/html/2603.20405v1) |

### 6.2 Specifics for Coq/Rocq

Important result: Claude Opus 4.6 with `rocq-mcp` tools solved 10/12
Putnam 2025 problems in **Rocq** (not Lean), demonstrating that AI assistance works
for Rocq too, despite less attention compared to Lean 4.

Key tools:
- `rocq-mcp` — a set of MCP tools for Claude in Rocq.
- AI is used for tactic generation, lemma search, filling `sorry`.

### 6.3 Applicability to trinity-s3ai

**How AI can close `Admitted` in trinity-s3ai:**

1. **Trivial algebraic lemmas** — Claude/GPT-5/Gemini fill them via
   `ring`, `lra`, `field_simplify`.
2. **Numerical inequalities** — coq-interval is often sufficient; AI can formulate
   the correct call `interval with (i_prec 200)`.
3. **Library gaps** — AI finds analogues in MathComp/Coquelicot.
4. **Complex `Admitted`** — AI proposes a proof sketch, human
   verifies the plan.

**Not suitable:** AI cannot "prove" physical axioms — only mathematical
consequences from them.

### 6.4 ProofNet and Formalization of Physics

ProofNet is a benchmark based on textbooks (Spivak, Rudin, etc.) for formalization.
Goedel-Prover achieves 15% on ProofNet (Pass@32). This means: ~15% of standard
lemmas from physics/mathematics textbooks are already automatically provable.

---

## 7. Similar Projects: Computational Physics + Coq

### 7.1 Wave Equation (Boldo, Lelay, Melquiond)

**Project:** Formal proof of correctness of a C program solving the acoustic
wave equation ([HAL:hal-00649240](https://inria.hal.science/hal-00649240/document)).

**Method:** Coq + Gappa + SMT solvers. Chain:
- Continuous PDE solution → discretization scheme → C program.
- At each level, formal error bounds.

**Lesson for trinity-s3ai:** Separation of "mathematical convergence theorem" and
"numerical error estimate" — an exemplary case.

**Reference:** [Formal Proof of a Wave Equation Resolution Scheme](https://guillaume.melquiond.fr/doc/10-itp.pdf)

### 7.2 Formally Verified Definite Integrals

**Paper:** [Formally Verified Approximations of Definite Integrals](https://inria.hal.science/hal-01630143v2/document)
(Boldo, Martin-Dorel, Melquiond).

Method: antiderivatives from RPA (strict polynomial approximations) + adaptive
subdivision. Example:
```coq
Goal Rabs (RInt (fun x => atan (sqrt (x*x + 2)) / ...) 0 1 - 5/96*PI*PI) <= 1/1000.
Proof. integral. Qed.
```

**Lesson:** coq-interval `integral` can certify complex integrals of physically
significant functions.

### 7.3 Taylor Models and ODEs in Coq (ITP 2024)

**Paper:** [A Coq Formalization of Taylor Models for ODE Solving](https://drops.dagstuhl.de/storage/00lipics/lipics-vol309-itp2024/LIPIcs.ITP.2024.30/LIPIcs.ITP.2024.30.pdf)
(Park, Thies, Kyoto 2024).

Method: exact real arithmetic (cAERN library), formal verification of
ODE solver. Strict guarantee: the solution can be approximated to arbitrary precision.

### 7.4 LeanBET: Surface Area in Physics (2026)

**Paper:** [LeanBET: Formally-verified surface area calculations in Lean](https://arxiv.org/html/2605.16169v1)
(2026) — formal verification of surface area calculations in adsorption physics.

**Key pattern:** Separation of `computation` (floating-point arithmetic) and
`specification` (over real numbers) + soundness proof.

### 7.5 Trusting Computations (PDE, Coq)

**Paper:** [Trusting computations: a mechanized proof from PDE](https://www.sciencedirect.com/science/article/pii/S0898122114002636)
— mechanized proof of convergence of a numerical scheme for PDE.

---

## 8. Ten to Fifteen Practical Lessons for trinity-s3ai

### Lesson 1: Strictly separate the three levels in every `.v` file

```
/* MATHEMATICAL THEOREM */ — formally proven
/* PHYSICAL HYPOTHESIS */    — [PHYSICAL_AXIOM], explicitly documented
/* NUMERICAL CERTIFICATE */   — [NUMERICAL_FIT], checked by coq-interval
```

**Tool:** A special comment header in every `Section`.

---

### Lesson 2: Maintain a living `admitted_log.md`

The file must contain for each `Admitted`:
- Theorem name.
- Status tag (see taxonomy above).
- Estimated proof difficulty.
- Required library dependencies.
- Date added.

Analogous to `axioms.md` from the OSforGFF project.

---

### Lesson 3: Use `Hypothesis` instead of `Axiom` for physical inputs

```coq
(* CORRECT: physical hypothesis as a section parameter *)
Section S3AIBounds.
  Hypothesis alpha_exp_bound :
    7297352 / 1000000000 <= alpha <= 7297353 / 1000000000.

  Theorem predicted_mass_bound :
    alpha_exp_bound ->
    Rabs (M_pred - M_obs) <= epsilon.
  Proof. ... Qed.
End S3AIBounds.

(* INCORRECT: physical data as a global Axiom *)
Axiom alpha_is_exactly : alpha = 7297352569 / 1000000000000.
```

`Hypothesis` (in a section) is more honest: it is clear that the theorem is conditional.

---

### Lesson 4: Apply coq-interval for strict numerical certificates

coq-interval can prove:
- Values of π, e, sqrt(2) to arbitrary precision.
- Compound expressions of elementary functions.
- Proper and improper integrals.

**For trinity-s3ai:** Instead of `Admitted (* number is close to observation *)`, write:

```coq
Lemma spectral_action_bound :
  Rabs (spectral_action_approx - 91.19) <= 0.01.
Proof.
  unfold spectral_action_approx.
  (* after unfolding definition: *)
  interval with (i_prec 200).
Qed.
```

---

### Lesson 5: Document what exactly coq-interval certifies

coq-interval proves a **mathematical inequality**, but not:
- That the model correctly describes nature.
- That the input parameters are correct.
- That the numerical match is not coincidental.

Add an explicit phrase in `(** ... *)`:
```
This certificate confirms: for the given parameter values
|computed - expected| ≤ ε. Physical interpretation depends
on the hypotheses [PHYSICAL_AXIOM] above.
```

---

### Lesson 6: For geometric parts, consider a parallel Lean 4 file

If trinity-s3ai includes differential forms, manifolds, Lie groups:
- No such libraries exist in Rocq → the entire geometric layer remains `Admitted`.
- Consider: maintaining a parallel Lean 4 file with geometry (Mathlib),
  Rocq — for numerical certificates (coq-interval).
- Connection: human-readable statements as a "bridge" between the two systems.

---

### Lesson 7: Use Claude Opus + rocq-mcp to close `Admitted`

Result ([arXiv:2603.20405](https://arxiv.org/html/2603.20405v1)):
Claude Opus 4.6 + rocq-mcp closed 10/12 olympiad problems in Rocq.

**Protocol for trinity-s3ai:**
1. For each `[MATH_TODO]` or `[LIBRARY_GAP]` — run Claude Opus + rocq-mcp.
2. Sandboxing: verify that the proof does not redefine the problem statement.
3. Whitelist of standard axioms: do not allow nonstandard `Axiom`.

---

### Lesson 8: PhysLib (Lean 4) as a benchmark for project structure

PhysLib / HepLean ([physlib.io](https://physlib.io)) — an exemplary case:
- Explicit separation of `Definitions`, `Theorems`, `Calculations`.
- Physical units formalized separately.
- Every result is tied to a source.
- Open source, community-managed.

For trinity-s3ai: adopt the structure (file `units.v`, file `physical_axioms.v`,
file `mathematical_results.v`, file `numerical_certificates.v`).

---

### Lesson 9: Error detection is the most valuable result of formalization

Tooby-Smith (2026) found an error in a cited paper on 2HDM through formalization.
This is the first non-trivial case in physics.

**For trinity-s3ai:** Formalization is valuable in itself as a checking tool:
even if not all `Admitted` are closed, explicit recording of conditions reveals hidden assumptions.

---

### Lesson 10: NCG and spectral action — an open field

The Stephan project (Lean 4, 2026) is at an early stage. The Connes–Lott
Lagrangian is nowhere formalized. For trinity-s3ai:
- One can **pioneer** formalization in Rocq (with `Admitted` for geometric parts).
- Alternative: wait for results from Stephan (Lean 4).

---

### Lesson 11: Flocq + Gappa for floating-point arithmetic verification

If trinity-s3ai involves floating-point computations:
- **Flocq** ([flocq.gitlabpages.inria.fr](https://flocq.gitlabpages.inria.fr)) —
  formal IEEE 754 library in Rocq.
- **Gappa** — automated rounding error checking.
- Combined use of Flocq + Gappa + coq-interval covers the entire stack:
  from algorithm to formal proof.

---

### Lesson 12: Decompose complex `Admitted` by "backward chaining"

Pattern from OSforGFF:
```
Main theorem T
├── Auxiliary lemma L1 [initially: Admitted]
│   ├── L1.1 [proven by coq-interval]
│   └── L1.2 [LIBRARY_GAP — needs Stokes in Rocq]
└── Auxiliary lemma L2 [proven by ring/lra]
```
First prove T, assuming L1 is true. Then work on L1.

---

### Lesson 13: Specify the minimal set of axioms in every `.v` file

```coq
(** This file uses the following nonstandard assumptions:
    - classical (excluded middle) from Coq.Logic.Classical
    - functional_extensionality
    - Physical axioms: see Section PhysicalInputs
    Mathematical theorems do not require [PHYSICAL_AXIOM] for correctness;
    they state: "IF the axioms are true, THEN..." *)
```

The command `Print Assumptions theorem_name` in Rocq prints the full list.

---

### Lesson 14: Monitor MathComp Analysis for future integration

MathComp Analysis 1.9.0 (February 2025) is actively developed. Expected:
- Lebesgue integrals, L^p spaces.
- Probability theory (Affeldt et al., ITP 2025).
- Possibly, in 2026–2027: differential forms in Rocq via MathComp.

---

### Lesson 15: Auto-formalization is a tool to accelerate coding

DeepSeek-Prover-V2 and Goedel-Prover-V2 already automatically formalize problem
statements from natural language into Lean 4. For Rocq: Claude + rocq-mcp.

**Practice for trinity-s3ai:**
- Write the physical statement in natural language (LaTeX).
- Use an AI auto-formalizer for the first draft `.v`.
- Human checks: what exactly is stated, whether all dependencies are correct.

---

## 9. Tool Recommendations

| Task | Tool |
|------|------|
| Numerical inequalities with π, exp, sqrt | `coq-interval` (tactic `interval`) |
| Integrals | `coq-interval` (tactic `integral`) |
| Floating-point arithmetic | `Flocq` + `Gappa` |
| Real analysis | `Coquelicot` + `MathComp Analysis` |
| Algebraic identities | `ring`, `field`, `lra` |
| Differential geometry | Lean 4 Mathlib (not yet available in Rocq) |
| AI assistance (Rocq) | `Claude Opus 4.6` + `rocq-mcp` |
| AI assistance (Lean 4) | `Lean Copilot`, `DeepSeek-Prover-V2`, `Goedel-Prover-V2` |
| Lie theory / Representations | Lean 4 Mathlib (not available in Rocq) |
| Quantum systems | PhysLib / HepLean (Lean 4) |
| NCG / Spectral action | Early stage (Stephan, Lean 4, 2026) |

---

## 10. Conclusion

**State of the field (2026):**

1. **Rocq/Coq** — mature for numerical certificates (coq-interval), analysis
   (Coquelicot + MathComp Analysis), floating-point arithmetic (Flocq/Gappa). Gap:
   differential forms, manifolds, Lie groups.

2. **Lean 4 / Mathlib** — leader in mathematical depth (manifolds, forms,
   Lie groups, representation theory, >210,000 theorems). Leader in AI tools.
   PhysLib/HepLean — the first serious physics libraries.

3. **Formalization of physics** — developing rapidly. QFT (Osterwalder–Schrader) —
   2026. Error in 2HDM found via Lean — 2026. NCG — early stage.

4. **AI assistance** — has reached a level allowing tens of `sorry`
   to be closed automatically. For Rocq: Claude + rocq-mcp. For Lean 4: full stack of tools.

5. **SM Lagrangian and spectral action** — nowhere fully formalized.
   trinity-s3ai can be a pioneer.

---

## References (Key)

1. [Coquelicot: A User-Friendly Library of Real Analysis for Coq](https://guillaume.melquiond.fr/doc/14-mcs.pdf) — Boldo, Lelay, Melquiond
2. [MathComp Analysis GitHub (v1.9.0, 2025)](https://github.com/math-comp/analysis)
3. [CoqInterval Documentation](https://coqinterval.gitlabpages.inria.fr)
4. [Lean 4 Mathlib: MFDeriv](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Geometry/Manifold/MFDeriv/Defs.html)
5. [Lean 4 Mathlib: Exterior Derivative](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/Calculus/DifferentialForm/Basic.html)
6. [Lean 4 Mathlib: LieAlgebra.Basic](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/Lie/Basic.html)
7. [Formalization of QFT in Lean 4 (arXiv:2603.15770, 2026)](https://arxiv.org/html/2603.15770v1)
8. [Formalizing 2HDM stability in Lean — error found (arXiv:2603.08139, 2026)](https://arxiv.org/abs/2603.08139)
9. [PhysLib — Lean 4 physics library](https://physlib.io)
10. [LeanForPhysics / Lean4PHYS (ICLR 2026)](https://openreview.net/forum?id=wQ2jyFz18H)
11. [Lean Copilot (arXiv:2404.12534)](https://arxiv.org/abs/2404.12534)
12. [Goedel-Prover-V2 (OpenReview 2026)](https://openreview.net/forum?id=j4C0nALrgK)
13. [DeepSeek-Prover-V2 (arXiv:2504.21801)](https://arxiv.org/abs/2504.21801)
14. [AlphaProof — Nature 2025](https://www.nature.com/articles/s41586-025-09833-y)
15. [Claude Opus 4.6 + rocq-mcp: 10/12 Putnam 2025 (arXiv:2603.20405)](https://arxiv.org/html/2603.20405v1)
16. [Formalizing NCG in Lean 4 (Stephan, INFN 2026)](https://agenda.infn.it/event/49101/)
17. [Formally Verified Approximations of Definite Integrals (HAL)](https://inria.hal.science/hal-01630143v2/document)
18. [Coq formal proof of wave equation (Boldo et al.)](https://guillaume.melquiond.fr/doc/10-itp.pdf)
19. [Taylor Models and ODEs in Coq, ITP 2024](https://drops.dagstuhl.de/storage/00lipics/lipics-vol309-itp2024/LIPIcs.ITP.2024.30/LIPIcs.ITP.2024.30.pdf)
20. [LeanBET: formally-verified surface area (arXiv:2605.16169, 2026)](https://arxiv.org/html/2605.16169v1)
21. [Flocq: Floats for Coq](https://flocq.gitlabpages.inria.fr)
22. [Formalizing low-dimensional solvable Lie algebras (arXiv:2505.19975, 2025)](https://arxiv.org/html/2505.19975v1)
23. [ITP 2024: Fast exp for CoqInterval](https://drops.dagstuhl.de/storage/00lipics/lipics-vol309-itp2024/LIPIcs.ITP.2024.14/LIPIcs.ITP.2024.14.pdf)
24. [Formalizing concentration inequalities in Rocq, ITP 2025](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2025.21)
25. [Special Relativity formalization in Coq (Harvard)](https://dash.harvard.edu/bitstreams/4160f812-a67d-42c4-9261-c159ade7cd86/download)
