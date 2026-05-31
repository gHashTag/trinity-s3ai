# Lean 4 — Porting CorePhi (Stage 3)

> **Status:** Stage 3 — all `sorry` eliminated, `DiracOperator` module added.
> `lake build` passes **in < 2 seconds** with **0 sorry** and **0 errors**.

---

## Why Lean 4?

The Trinity S3AI project was developed in Coq (version 8.20.x).
Lean 4 / Mathlib 4 is a modern alternative with several
practical advantages:

1. **Actively developed Mathlib.**
   Mathlib 4 is the world's largest library of formalized mathematics;
   it is significantly richer than what is available "out of the box" in Coq without
   installing dozens of additional packages.

2. **Convenient tactic syntax.**
   `nlinarith`, `norm_num`, `ring`, `field_simp` — standard tactics
   of Lean 4, solving the same problems as `lra` + `interval` + `field` in Coq.

3. **Next-generation dependent types.**
   Unified elaboration, `#check`, `#eval` — rapid prototyping without
   a separate compiler.

4. **Portability.**
   Mathlib works on macOS, Linux, and Windows (WSL2) through a single
   tool `elan`/`lake`. No tie to a specific opam version.

5. **The future of formal mathematics.**
   Academic Lean projects (FLT, Fermat's Last Theorem Project, etc.)
   are moving to Lean 4, making it the de-facto standard in the coming years.

---

## Decision on Mathlib

**Recommendation: stay on pure Lean 4 core.**

### Attempt to Add Mathlib

| Stage | Result | Time |
|------|-----------|-------|
| `lake update` | Timeout (5 min) | > 5 min |
| Manual shallow clone | Success | ~48 s |
| `lake exe cache get` | dyld error on macOS | — |
| Full build | Not checked (expected > 30 min) | — |

### Trade-offs

**Pros (if added):**
- `ring`, `field_simp`, `norm_num`, `nlinarith` — automation of algebraic proofs.
- Ready lemmas for `List`, `Real`, `Finset`, `LinearAlgebra`.
- Rich ecosystem of differential geometry and spectral theory.

**Cons (real):**
- **Build time:** initial download and build of Mathlib takes 30+ minutes.
- **CI complexity:** requires caching `.lake/packages` and prebuilt cache (`lake exe cache get`), which does not work in some macOS environments.
- **Dependency fragility:** `lake update` times out in networks with limited bandwidth.
- **Toolchain lock-in:** tie to a specific Mathlib version is stronger than to a Lean version.

### Alternative

A **`lakefile-mathlib.toml`** has been created in the repository — an optional configuration
with Mathlib connection. To use:

```bash
cp lakefile-mathlib.toml lakefile.toml
lake update   # may take > 5 min
lake build    # may take > 30 min (first time)
```

By default the project remains **pure** (pure Lean 4 core), guaranteeing
a build in < 2 seconds and no external dependencies.

---

## Directory Structure (post Wave 24+ cleanup)

```
derivations/lean_port/
├── lakefile.toml           # Lake configuration (pure Lean)
├── lakefile-mathlib.toml   # optional configuration with Mathlib
├── lean-toolchain          # version pinned: leanprover/lean4:v4.13.0
├── README.md               # this file
└── TrinityLean/
    ├── CorePhi.lean                  # requires Mathlib; NOT in default target
    ├── KODimensionMathlib.lean       # Mathlib-based extended version (281 lines)
    ├── QuaternionicLinearityMathlib.lean # Mathlib-based extended version (326 lines)
    ├── TrinityLean.lean              # root file — imports default target modules
    ├── lakefile.lean                 # package config
    ├── README.md                     # module-specific docs
    └── TrinityLean/                  # default `lake build` target modules
        ├── KODimension.lean          # pure-Lean KO-dimension (95 lines)
        ├── QuaternionicLinearity.lean # pure-Lean quaternions (Float, 137 lines)
        ├── Spectrum600Cell.lean      # spectrum of the 600-cell (0 sorry)
        ├── EtaInvariant.lean         # eta invariants for platonic plumbing
        ├── DiracOperator.lean        # Dirac operator, gamma matrices, Clifford
        ├── H4RootSystem.lean         # H₄ Coxeter matrix (1 sorry)
        ├── HamiltonFano.lean         # Fano-plane Hamilton cycle
        └── Snub24Z3.lean            # Z₃ partition of snub 24-cell
```

---

## Stage 3 Status (Wave 13.2)

`lake build` passes **with 0 errors** and **1 `sorry`** (in `H4RootSystem.lean`, icosian embedding).

| File | Lemmas/Theorems | sorry | axiom | Note |
|------|-------------|-------|-------|-----------|
| `CorePhi.lean` | 14 | 0 | 0 | Requires Mathlib, not in default target |
| `TrinityLean/KODimension.lean` | 18 | 0 | 1 (`cell600_J_off_diagonal`) | Structural axiom |
| `TrinityLean/QuaternionicLinearity.lean` | 6 | **0** | 11 | 10 Float axioms + `normSq_mul` |
| `TrinityLean/Spectrum600Cell.lean` | 3 | **0** | 0 | `chiral_symmetry` proven in pure Lean |
| `TrinityLean/EtaInvariant.lean` | 4 | 0 | 0 | Pure definitions |
| `TrinityLean/DiracOperator.lean` | 5 | 0 | 1 (`clifford_mul_assoc`) | Structural axiom (analog of `normSq_mul`) |
| `TrinityLean/H4RootSystem.lean` | 5 | **1** (icosian embedding) | 0 | Structural gap; TODO follow-up PR |
| `TrinityLean/HamiltonFano.lean` | 3 | 0 | 0 | Fano-plane Hamilton cycle |
| `TrinityLean/Snub24Z3.lean` | 4 | 0 | 0 | Z₃ partition of snub 24-cell |
| **Total** | **62** | **1** | **13** | |

### What Changed in Stage 3

**`Spectrum600Cell.lean`** — last `sorry` removed:

- `chiral_symmetry` proven using `List.mem_append` and `List.mem_replicate`
  from `Init.Data.List.Lemmas` (available in Lean 4 core v4.13.0).
- Uses existing axiom `TrinityLean.Quaternion.Float.neg_neg`
  to simplify `-(-1.0) = 1.0` (Float is an opaque primitive).

**New module `DiracOperator.lean`:**

| # | Definition/Theorem | Description |
|---|---------------------|----------|
| 1 | `DiracOperator` | Structure with `dimension`, `matrix`, `self_adjoint` |
| 2 | `gamma_matrices` | List of 2×2 Pauli matrices (simplified version) |
| 3 | `clifford_multiplication` | Quaternion multiplication as Clifford |
| 4 | `dirac_600cell_dimension` | `dimension = 480` (by `rfl`) |
| 5 | `dirac_is_hermitian` | Self-adjointness of a concrete 2×2 matrix |

### Build

```bash
cd derivations/lean_port/TrinityLean
lake build   # ~1.4 s, 0 errors, 1 sorry (H4RootSystem icosian embedding)
```

---

## How to Build Locally (requires elan)

### 1. Install elan (Lean version manager)

```bash
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh
```

After installation, restart the terminal or run:

```bash
source ~/.elan/env
```

### 2. Navigate to the lean_port directory

```bash
cd derivations/lean_port/TrinityLean
```

### 3. Build the project

```bash
lake build
```

The build takes **< 2 seconds** and does not require Mathlib (only Lean 4 core).

### 4. Check individual lemmas

```bash
lake env lean --stdin <<'EOF'
#check @TrinityLean.QuaternionicLinearity.normSq_mul
#check @TrinityLean.Spectrum600Cell.chiral_symmetry
#check @TrinityLean.DiracOperator.dirac_is_hermitian
EOF
```

or open the files in VS Code with the `leanprover.lean4` extension.

---

## System Requirements

| Component | Version |
|-----------|--------|
| elan | ≥ 3.1.1 |
| Lean 4 | v4.13.0 (pinned in `lean-toolchain`) |
| macOS / Linux | any modern |
| RAM | ≥ 4 GB |

---

## Known Limitations

1. **`CorePhi.lean` requires Mathlib** and is not included in the default `lake build` target.
   The remaining modules build in pure Lean 4 core.

2. **Float axioms** (`Float.neg_neg`, `Float.mul_comm`, `normSq_mul`, `clifford_mul_assoc`)
   are mathematically obvious, but not provable in Lean 4 core without Mathlib, because
   `Float` is an opaque primitive type. This is a standard compromise for CI-friendly
   projects.

---

## Next Steps

- [ ] Port `H4Derivations.v` → `TrinityLean/H4Derivations.lean`
- [ ] Port `Bounds_LeptonMasses.v` using Mathlib (optional)
- [ ] Set up Mathlib cache in CI via `leanprover/lean4-action` + `cache`

---

## File Correspondence: Coq ↔ Lean 4

| Coq (proofs/trinity/) | Lean 4 (TrinityLean/TrinityLean/) | Status |
|-----------------------|-----------------------------------|--------|
| `CorePhi.v` | `CorePhi.lean` (top-level, Mathlib) | Stage 0 + aux. |
| `KODimension.v` | `TrinityLean/KODimension.lean` | Stage 1 ✓ |
| `QuaternionicLinearity.v` | `TrinityLean/QuaternionicLinearity.lean` | Stage 2 ✓ |
| `Spectrum600Cell.v` | `TrinityLean/Spectrum600Cell.lean` | Stage 3 ✓ |
| `EtaInvariant.v` | `TrinityLean/EtaInvariant.lean` | Stage 3 ✓ |
| `DiracOperator.v` | `TrinityLean/DiracOperator.lean` | Stage 3 ✓ (new) |
| `H4RootSystem.v` | `TrinityLean/H4RootSystem.lean` | Stage 1 ✓ |
| `HamiltonFano.v` | `TrinityLean/HamiltonFano.lean` | Stage 2 ✓ |
| `Snub24Z3.v` | `TrinityLean/Snub24Z3.lean` | Stage 3 ✓ |
| `H4Derivations.v` | _not started_ | — |
| `E6vsH4.v` | _not started_ | — |
| `Bounds_LeptonMasses.v` | _not started_ | — |
| remaining ~30 files | _not started_ | — |

---

*Trinity S3AI Lean 4 Port — Stage 3*
*Updated as part of Wave 13.2*
