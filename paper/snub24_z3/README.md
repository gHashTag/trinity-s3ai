# Z₃ tripartition of the snub 24-cell as a flavour structure

Standalone LaTeX paper for the Trinity S³AI project.

## Title
"Z₃ tripartition of the snub 24-cell as a flavour structure"

## Target journal
Journal of Mathematical Physics (J. Math. Phys.) or arXiv math.GR

## Files

| File | Description |
|------|-------------|
| `snub24_z3.tex` | Main LaTeX source (amsart, ~14 pages) |
| `snub24_z3.bib` | BibTeX bibliography (25 entries) |
| `Makefile` | Build automation |
| `README.md` | This file |

## Build instructions

```bash
make
```

This runs the standard `pdflatex → bibtex → pdflatex → pdflatex` chain.

To clean auxiliary files:
```bash
make clean
```

To remove the PDF as well:
```bash
make distclean
```

## Paper structure

1. **Introduction** — Three-generation problem, geometric origins programmes, statement of the combinatorial theorem.
2. **The snub 24-cell as 4 cosets of 2T in 2I** — Quaternionic realisation, coset decomposition theorem.
3. **The Z₃ subgroup and its action** — Explicit generator g = (−1/2, 1/2, 1/2, 1/2), proof of freeness.
4. **The canonical 3-partition** — Theorem: 96 = 32 + 32 + 32, formal verification in Coq and Lean 4.
5. **Connection to representation theory of 2I** — Character table, anti-numerology discussion.
6. **Physical speculation** (explicitly labeled) — Relation to Wilson's Pati–Salam embedding, honest assessment of open problems.
7. **Open problems** — Spectral triples, E₈ connection, S³/2I geometry, orbifolds, triality.
8. **References** — 25 real, verified citations.

## Critical principles

- All text is in English.
- The paper does **not** claim a complete solution to the three-generation problem.
- The paper does **not** claim Nobel-grade results.
- One explicitly labeled speculative section (§6).
- Principle: «ne vrat'» — do not lie.

## Formal verification

The main theorem has been independently formalised in:
- **Coq**: `derivations/alt_crystallography/Snub24CellZ3.v` (commit `d883275`)
- **Lean 4**: `Trinity/H4RootSystem/Snub24Z3.lean` (commit `916bc6e`)

Repository: https://github.com/gHashTag/trinity-s3ai
