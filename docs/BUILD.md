# Build Instructions — Trinity S³AI

Full build matrix for Coq, Rust, and Python validators.

---

## Prerequisites

- Coq 8.20.1
- opam (OCaml package manager)
- coq-interval, coq-coquelicot (Coq libraries)
- Rust toolchain (for `trinity_rust/` and `games/trinity_fold/`)
- Python 3 + `mpmath`, `numpy`

---

## Coq Build

### Local build

```bash
# Install dependencies (first time only)
opam repo add coq-released https://coq.inria.fr/opam/released
opam install coq.8.20.1 coq-interval coq-coquelicot

# Build
cd proofs/trinity
coq_makefile -f _CoqProject -o Makefile.coq
make -f Makefile.coq -j$(nproc)
```

### Docker (zero host dependencies)

```bash
docker run -it --rm -v $(pwd):/work coqorg/coq:8.20.1-ocaml-4.14-flambda bash
cd /work/proofs/trinity
coq_makefile -f _CoqProject -o Makefile.coq
make -f Makefile.coq -j4
```

---

## Rust Build

```bash
# Trinity Rust formula catalog
cd trinity_rust
cargo test

# GOLDEN CHAIN game workspace
cd games/trinity_fold
cargo test --workspace
```

---

## Python Validators

```bash
pip install mpmath numpy

# Formula error bounds vs PDG 2024 (~10 s)
python3 scripts/validators/validate_v4.py

# Honesty gate — detects untagged φ/π/e formulas (~5 s)
python3 scripts/anti_numerology_gate.py

# Honest Coq counter — strips comments before counting (~2 s)
python3 scripts/count_admitted_honest.py
```

---

## CI Workflows

| Workflow | What it gates | File |
|----------|---------------|------|
| `ci.yml` | Anti-numerology gate, Coq build, Python validators | `.github/workflows/ci.yml` |
| `rust.yml` | Rust formatter, clippy, tests | `.github/workflows/rust.yml` |
| `pages.yml` | Builds and deploys GOLDEN CHAIN canvas to GitHub Pages | `.github/workflows/pages.yml` |
| `lean.yml` | Lean 4 (Mathlib) auxiliary proof PRs | `.github/workflows/lean.yml` |
| `release.yml` | Builds the release bundle (Coq + PDF) | `.github/workflows/release.yml` |

---

## One-liner Sceptic's Path

```bash
pip install mpmath numpy
python3 scripts/anti_numerology_gate.py      # ~5 s
python3 scripts/count_admitted_honest.py     # ~2 s
python3 scripts/validators/validate_v4.py      # ~10 s
cd games/trinity_fold && cargo test --workspace  # ~30 s
```

If any step fails, the README statistics are stale — please open an issue.
