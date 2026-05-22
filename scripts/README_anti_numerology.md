# Anti-Numerology Gate

**File**: `scripts/anti_numerology_gate.py`  
**CI job**: `anti_numerology_check` in `.github/workflows/ci.yml`  
**Wave**: 10.5

---

## Purpose

The anti-numerology gate is a **heuristic CI-level safety net** that automatically detects Definition statements in `.v` files that combine multiple transcendental constants (φ, π, e, √n) without an approved honesty tag.

Its purpose is to prevent silent regression: someone adds a new `phi^a · pi^b · e^c = X` formula without the required `[phenomenological_fit]` annotation, and it silently enters the codebase as if it were a first-principles derivation.

**This tool is explicitly heuristic, not formal.** It will not catch every case, and it can produce false positives. It is a safety net, not a proof of honesty.

---

## How It Works

### Detection heuristic

The script:

1. Parses all `Definition name := rhs` statements in `proofs/trinity/*.v`
2. Checks the RHS for ≥2 distinct "atom types" from: `phi`, `PI`, `exp 1`, `exp`, `sqrt`, `powZ`, `pow_pos`
3. For each such Definition, looks in a ±12-line window for an approved honesty tag
4. Also checks for file-level header tags (first 30 lines) covering an entire file
5. Also checks if a section-block header explicitly declares the block as phenomenological
6. Flags any formula with ≥2 atoms and no approved tag

### Approved honesty tags

Any one of these (case-insensitive) satisfies the check:

| Tag | Meaning |
|-----|---------|
| `[phenomenological_fit]` | Formula is a fit to data, not derived |
| `[NUMERICAL_FIT]` | Value from numerical computation (Python, Mathematica) |
| `[HONEST: ...]` | Explicit honest acknowledgement with reason |
| `[NCG_AXIOM]` | Axiom from noncommutative geometry framework |
| `[PHYSICAL_AXIOM]` | Input from experiment (PDG value) |
| `[MATH_TODO]` | Mathematical gap to be filled later |
| `[LIBRARY_GAP]` | Coq library limitation, not a conceptual gap |

### Structural whitelist

Definitions on the structural whitelist are always PASS:

- Pure math constants: `phi`, `powZ`, `e_const`, `euler_e`, `e_coq`
- H4 group invariants: `H4_order`, `h_H4`, `d1`, `d2`, `d3`, `d4`
- PDG measurements: `m_e_PDG`, `alpha_inv_PDG`, etc.
- Geometric quantities: `vol_S3_phi`, `scalar_curvature`

---

## Test Results on Current Main HEAD

Run: `python3 scripts/anti_numerology_gate.py`

```
PASS      :   59  (multi-atom formulas with approved tag)
FLAG      :    0  (multi-atom formulas MISSING tag)
WHITELIST :   83  (structural/PDG definitions, exempt)
TOTAL defs:  142

VERDICT: ✓ PASS
```

All 59 multi-atom numerological formulas on current main are properly tagged with at least one approved honesty tag.

---

## CI Integration

The gate is the **first job** in `.github/workflows/ci.yml`:

```yaml
anti_numerology_check:
  runs-on: ubuntu-latest
  continue-on-error: false   # HARD gate — blocks build job
```

The Coq build job has `needs: anti_numerology_check` so it cannot run until the gate passes.

### Per-commit override

If you need to merge a commit that temporarily fails the gate (e.g., while adding tags to a new formula), include `[skip-numerology-check]` in your commit message:

```
git commit -m "WIP: add new Higgs formula [skip-numerology-check]"
```

This downgrades all FLAG results to warnings and exits with code 0. **Do not use this routinely** — it defeats the purpose of the gate.

---

## Adding a New Formula

When you add a new `Definition` involving φ, π, or e:

### If it's a phenomenological fit:
```coq
(* [phenomenological_fit] This is a numerical fit to PDG data, not a    *)
(* derivation from H4 geometry. Error: 0.05%. See Catalog42.v.          *)
Definition my_new_formula : R := phi^3 * exp 1 / PI.
```

### If it's from NCG theory:
```coq
(* [NCG_AXIOM] This follows from the spectral action S = Tr f(D/Lambda)  *)
(* evaluated on the 600-cell; the pi factors arise from the heat kernel. *)
Definition spectral_coeff : R := 2 * PI * PI * phi^3.
```

### If it has a mathematical gap:
```coq
(* [MATH_TODO] The derivation from H4 boundary conditions is outlined     *)
(* in yukawa_h4_appendix.txt but not yet formalized in Coq.               *)
Definition y_top_formula : R := phi^5 * exp 1 / (3 * PI).
```

---

## Known Limitations

1. **No semantic understanding**: the gate cannot distinguish a numerologically plausible formula from a derivation that happens to involve φ and π for good mathematical reasons.

2. **Regex-based parsing**: The Coq parser is regex-based and will miss some multi-line definitions or definitions inside module/section scopes.

3. **False negatives**: A formula with only 1 atom type (e.g., `phi^17`) will not be flagged, even if it's pure numerology. The threshold of ≥2 atom types is chosen to minimize false positives.

4. **File-level tags**: A `[phenomenological_fit]` tag in the file header passes ALL definitions in that file. If a file mixes legitimate derivations with fits, use per-definition tags instead.

---

## Usage

```bash
# Standard (run from repo root):
python3 scripts/anti_numerology_gate.py

# Verbose (show PASS and WHITELIST details):
python3 scripts/anti_numerology_gate.py --verbose

# Custom directory:
python3 scripts/anti_numerology_gate.py --dir path/to/other/proofs

# Strict mode (ignores [skip-numerology-check] override):
python3 scripts/anti_numerology_gate.py --strict
```

Exit codes:
- `0` — all formulas pass
- `1` — one or more formulas flagged (no override active)
- `2` — directory not found

---

*Wave 10.5 — Trinity S3AI anti-numerology infrastructure*
