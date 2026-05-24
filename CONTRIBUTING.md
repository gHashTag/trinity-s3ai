# CONTRIBUTING — Trinity S3AI

> **Principle: "Do not lie. Be honest."**

---

## HONESTY-FIRST Principle

This repository is a **active boundary-mapping research program**. See `RESEARCH_STATUS.md` for a summary of what H4 *can* and *cannot* do. The main findings are four formal Boundary Theorems (BT-1–BT-4) in `proofs/trinity/BoundaryTheorems.v`.

The greatest ongoing risk is **silent regression**: someone adds a new `φ^a · π^b · e^c = X` formula without an explicit honesty tag, and it silently appears to be a first-principles derivation.

### Rules for New Contributions

#### 1. Admitted axioms

Every `Admitted` must carry exactly one tag from:

| Tag | Meaning |
|-----|---------|
| `[PHYSICAL_AXIOM]` | Physical input from experiment (PDG value) |
| `[NUMERICAL_FIT]` | Numeric value from Python/external computation |
| `[MATH_TODO]` | Mathematical gap, to be formalized later |
| `[LIBRARY_GAP]` | Coq library limitation (e.g., interval tactic timeout) |

Example:
```coq
Admitted. (* [PHYSICAL_AXIOM] sin^2(theta_W) = 0.22336, PDG 2024 *)
```

Rationale: `Admitted` without a tag is indistinguishable from a deliberate hole. All gaps must be explained.

#### 2. Numerological formulas

Any `Definition` combining ≥2 of {φ, π, e, √n} in its RHS and matching a physical observable must carry an approved tag. The anti-numerology gate enforces this automatically:

```coq
(* [phenomenological_fit] Numerical coincidence with PDG 2024. Error 0.024%. *)
(* NOT derived from H4 geometry; see BoundaryTheorems.v BT-4.                   *)
Definition G01_formula : R := 36 * phi * (exp 1) * (exp 1) / PI.
```

Approved tags: `[phenomenological_fit]`, `[NUMERICAL_FIT]`, `[HONEST: ...]`, `[NCG_AXIOM]`, `[PHYSICAL_AXIOM]`, `[MATH_TODO]`, `[LIBRARY_GAP]`.

Run the gate locally before pushing:
```bash
python3 scripts/anti_numerology_gate.py
```

#### 3. No fake proofs

- Do not remove `Admitted` without adding a real proof.
- Do not replace a correct proof with `Admitted` and claim it is proven elsewhere.
- Do not add a theorem whose statement is vacuously true or trivially unprovable.

#### 4. Language policy — ENGLISH ONLY

**All public documentation must be written in English.** This includes:
- Markdown files (`*.md`) in `docs/`, `derivations/`, `paper/`, `reports/`, `talks/`
- Issue and PR descriptions
- Comments in Coq/Lean proof files that explain physical claims
- YAML configs, READMEs, and audit reports

Russian-language documents created before this policy are grandfathered with a `LEGACY: Russian-language document` header. **No new Cyrillic text** may be added to public-facing docs without explicit project-lead approval.

The CI gate `cyrillic-check` enforces this. If you have a legitimate reason to include Cyrillic (e.g., quoting a Russian paper title), add the `LEGACY:` header or request exemption in the PR.

#### 5. Commit signing (required on `main`)

All commits pushed to `main` must be **GPG-signed**. Unsigned commits are rejected by CI.

Quick setup:
```bash
gpg --full-generate-key   # or use an existing key
git config --global user.signingkey <YOUR_KEY_ID>
git config --global commit.gpgsign true
```

Then commit normally; Git will sign automatically. If you forget to sign:
```bash
git commit --amend -S --no-edit  # re-sign the last commit
git push --force-with-lease      # safe force-push on a PR branch
```

CI runs `scripts/check_commit_signatures.py` on every PR. Emergency bypass:
add `[skip-signature-check]` to the commit message (not recommended; log a reason
in the PR description).

#### 6. PR requirements

Every PR must:
1. Fill in the PR template (`.github/PULL_REQUEST_TEMPLATE.md`)
2. Pass `anti_numerology_check` CI job (or include `[skip-numerology-check]` with explanation)
3. Pass `cyrillic-check` CI job (or include `[skip-cyrillic-check]` with justification)
4. Pass `scripts/validators/validate_v4.py` (formula error bounds)
5. Have a "What is verified / What is open" section
6. Be **GPG-signed** (or include `[skip-signature-check]` with justification)

#### 5. Build instructions (Coq 8.20.1)

```bash
# Prerequisites: opam, Coq 8.20.1, coq-interval, coq-coquelicot
cd proofs/trinity
coq_makefile -f _CoqProject -o Makefile.coq
make -f Makefile.coq -j$(nproc)
```

Or use Docker:
```bash
docker run -it --rm -v $(pwd):/work coqorg/coq:8.20.1-ocaml-4.14-flambda
```

#### 6. Python tests

```bash
pip install mpmath numpy
python3 scripts/validators/validate_v4.py
python3 scripts/anti_numerology_gate.py --verbose
```

---

## File Structure

```
proofs/trinity/        — Coq .v files (50 files in proofs/trinity/, plus 3 in proofs/clifford_cl8/ and 26 in derivations/ — total 79 .v files / 1325 Qed / 123 unproven obligations; see COQ_HONEST_STATUS.md)
scripts/               — Python utilities and gates
  anti_numerology_gate.py   — Formula honesty checker
  README_anti_numerology.md — Gate documentation
.github/workflows/
  ci.yml               — Main CI (anti_numerology_check → build)
  release.yml          — Release artifact builder
RESEARCH_STATUS.md             — What H4 can/cannot do (read first)
BoundaryTheorems.v         — Formal boundary theorems BT-1–BT-4
CITATION.cff           — Citation metadata
CONTRIBUTING.md        — This file
```

---

## Questions?

Open an issue using `.github/ISSUE_TEMPLATE.md`. Describe which formula or theorem is under question, cite the PDG source, and propose a correction if you have one.

*Wave 10.5 — Trinity S3AI*
