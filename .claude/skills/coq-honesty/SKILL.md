---
name: coq-honesty
description: Coq proof editing rules for Trinity S3AI — honesty tags, Admitted conventions, and proof structure
trigger:
  paths:
    - "proofs/**/*.v"
    - "derivations/**/*.v"
---

# Coq Honesty Rules

## Adding or Editing Coq Proofs

### Honesty Tags (mandatory)
Every theorem that relies on a multi-atom `phi/π/e` formula or an unproven assumption must carry a tag:

| Tag | Meaning | When to use |
|-----|---------|-------------|
| `[phenomenological_fit]` | Numerical coincidence with SM parameter | Formula matches PDG value but lacks physical derivation |
| `[NUMERICAL_FIT]` | Explicit numerical fit (legacy) | Same as above, older notation |
| `[PHYSICAL_AXIOM]` | Physically motivated assumption | Step needs physics justification, not just math |
| `[MATH_TODO]` | Mathematical gap | Proof step is blocked by missing lemma |
| `[LIBRARY_GAP]` | Missing Coq library | Blocked by unformalized external result |
| `[OPEN_PROBLEM]` | Honestly open | Deliberately left open with citation |

### Admitted Convention
- **Never** leave `Admitted.` without a tag in committed code.
- If a theorem is genuinely open, tag it with `[OPEN_PROBLEM]` and add a citation or cross-reference to `docs/analysis/admitted_log.md`.
- If a theorem is blocked by a missing lemma, tag it with `[MATH_TODO]` or `[LIBRARY_GAP]` and name the blocker.
- `proofs/trinity/` targets **0 real Admitted** — every `Qed.` must be a real proof.
- `proofs/clifford_cl8/` allows load-bearing Axioms **only with citations** (e.g., Lounesto 2001, Atiyah-Bott-Shapiro 1964).

### Running the Honest Counter
After editing Coq files, run:
```bash
python3 scripts/count_admitted_honest.py
```
This strips all comments and strings before counting, so historical `Admitted` mentions in comments do not affect the tally.

### Claim Status Mapping
| Coq Artifact | Claim Status |
|--------------|--------------|
| `Qed.` on a theorem | `verified` |
| `Qed.` on a `refuted` theorem | `verified` (impossibility result) |
| `Admitted.` with `[phenomenological_fit]` tag | `empirical_fit` |
| `Admitted.` with `[OPEN_PROBLEM]` tag | `open_conjecture` |
| `Axiom` / `Parameter` with citation | `verified` (axiomatic base) |
| `Axiom` / `Parameter` without citation | `unverified` — add citation or tag |

### Boundary Theorems
BT-1 through BT-4 are **impossibility results** (proven in `proofs/trinity/BoundaryTheorems.v`). They prove that *certain direct constructions* fail. When citing them:
- Do not call them "dead ends" — they are guideposts.
- Always reference the specific BT number and the obstruction it proves.

### Limits of Formal Proof (honest scope)
- Coq `Qed.` on a mathematical theorem **does not** guarantee correctness of a generated implementation (RTL, C, etc.).
- Formal proofs and implementation are orthogonal layers: proofs verify the *spec*, implementation must be verified separately (functional sweep, simulation, testing).
- Example: 84 Coq proofs of φ-mathematics did not catch systematic RTL bugs in GF multipliers (out-of-bounds product width, wrong normalization bit).
- Rule of thumb: if there is a code generator or handwritten implementation, add a **functional verification layer** (sweep against exact reference) in addition to formal proofs.
