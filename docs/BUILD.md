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

## Hardware Build (FPGA / RTL)

```bash
# GF16 RTL synthesis (Yosys + nextpnr, openXC7 toolchain)
cd docs/hardware/rtl

# Synthesize GF16 multiplier
yosys -p "read_verilog gf16_mul.v; synth_xilinx -flatten -abc9 -arch xc7 -top gf16_mul; write_json gf16_mul.json"

# Run testbench with Icarus Verilog
iverilog -o gf16_mul_tb.vvp gf16_mul_tb.v gf16_mul.v
vvp gf16_mul_tb.vvp

# Full dot4 unit
cd build/
yosys -p "read_verilog ../gf16_dot4.v ../gf16_mul.v ../gf16_add.v; synth_xilinx -flatten -abc9 -arch xc7 -top gf16_dot4; write_json gf16_dot4.json"
```

**Requirements:**
- Yosys 0.40+
- nextpnr-xilinx (openXC7)
- Icarus Verilog 12.0+
- GTKWave (optional, for VCD inspection)

**FPGA target:** Xilinx Artix-7 XC7A100T (QMTech board).  
**Performance:** 323 MHz combinational, 35/35 tests pass.

See `docs/hardware/rtl/build/` for pre-generated synthesis reports.

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
