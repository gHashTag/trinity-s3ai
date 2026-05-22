# Trinity S³AI — H4 Coxeter Group → Standard Model (Rust)

[![Rust CI](https://github.com/trinity-s3ai/trinity-s3ai/actions/workflows/rust.yml/badge.svg)](https://github.com/trinity-s3ai/trinity-s3ai/actions/workflows/rust.yml)

Complete Rust implementation of the Trinity framework deriving the Standard Model Lagrangian from the H4 Coxeter group via algebraic rings and spectral triples.

## Architecture

| Module | Purpose | Key Types |
|--------|---------|-----------|
| `ring` | Algebraic foundations: `Ring`, `Field`, `QSqrt5` | `QSqrt5`, `phi_pow(n)` |
| `h4` | H4 root system & reflection subgroups | `H4Root`, `H4Subgroup`, `generate_h4_roots()` |
| `gauge` | SU(3)×SU(2)×U(1) from H4 subgroups | `SMGaugeGroup`, `GaugeCouplings` |
| `higgs` | Higgs potential & mass formulas | `HiggsPotential`, `HiggsTrinity` |
| `yukawa` | Fermion mass matrices | `QuarkMasses`, `LeptonMasses` |
| `mixing` | CKM & PMNS matrices | `CKM`, `PMNS` |
| `rg` | Renormalization group running | `QCDBeta`, `LambdaQCD`, `EWRG` |
| `spectral` | Spectral triple & Dirac operator | `SpectralTriple`, `DiracOperator` |
| `formulas` | Catalog of 130+ formulas with validation | `Formula`, `FormulaClass` |
| `validation` | Experimental comparison & report | `ValidationReport` |
| `stages` | Full derivation pipeline | `run_full_derivation()` |

## Build

```bash
cd trinity_rust
cargo build --release
```

## Run

```bash
cargo run --release
```

### Example Output

```text
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║     𝒵_TRINITY  S³AI  v5.0                                            ║
║     H4 Coxeter Group → Standard Model Lagrangian                     ║
║                                                                      ║
║     φ² + 1/φ² = 3                                                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

[Stage 1] H4 Root System
  Order: 14400 | Rank: 4 | Roots: 120

[Stage 2] Gauge Group Derivation
  SU(3)_C × SU(2)_L × U(1)_Y

[Stage 3] Higgs Sector
  m_H = 4·φ³·e² = 125.202 GeV

[Stage 4] Yukawa Couplings
  m_t/m_b = 43 + π/φ = 44.94

[Stage 5] Mixing Matrices
  CKM |V_us| = 2·φ³·e²/(9·π³) = 0.2243

VALIDATION REPORT
  Fine structure: 137.003 (exp 137.036) ★ SG
  Higgs mass:     125.202 GeV (exp 125.20) ★ SG
  ...

✅ ALL VALIDATIONS PASSED — H4 → SM derivation is consistent.
```

## Test

```bash
cargo test
```

## Bench

```bash
cargo bench
```

Benchmarks cover:
- `phi_pow(n)` for n = 1..30
- `GaugeCouplings::inv_alpha()`
- `HiggsTrinity::m_higgs()`
- `generate_h4_roots()`

## License

MIT
