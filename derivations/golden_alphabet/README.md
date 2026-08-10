# The golden weight alphabet, machine-checked

Three results about the weight alphabet `{-φ, 0, +φ}` used by a multiplier-free
ternary datapath. Unlike the physics derivations elsewhere in this repository,
these are arithmetic facts with no modelling assumptions: the kernel checks them
and there is nothing left to dispute.

## What is proved

| theorem | statement |
|---|---|
| `phi_quadratic` | `φ·φ = φ + 1` |
| `phi_unique` | any `r > 1` with `r·r = r + 1` **is** `φ` — the base is forced, not chosen |
| `mulphi_correct` | on integer pairs `(a,b) ≡ a + bφ`, multiplying by `φ` is `(a,b) → (b, a+b)`: the Fibonacci step, **one integer addition, no shift** |
| `addp_correct`, `negp_correct` | addition and negation are componentwise |
| **`dot_exact`** | **the entire linear path — any fan-in, any weight pattern — computed in integer pairs equals the real-valued result exactly** |
| `phi_pow_fib` | `φ^(k+1) = F_(k+1)·φ + F_k`, so the gain of `k` stacked layers is a pair of integers and depth needs no multiplier |

`dot_exact` is the one that matters. Everywhere else number formats are compared
by the size of their rounding error. Here there is no rounding error to compare:
the multiply-free path is not merely cheap, it is **exact**. Rounding enters such
a network only at the nonlinearity, where no format avoids it.

Why the base cannot be anything else: closure needs `r² = pr + q` with integer
`p, q`, so that `Z[r]` is a ring. Any `p > 1` adds a shift alongside the
addition — `1+√2` satisfies `r² = 2r + 1` and pays that shift, while `√2` has
`r² = 2` and loses the scale out of the lattice. The `p = q = 1` case is `φ`,
and it is the minimum rather than one acceptable option among several.

**Scope.** This is arithmetic in a lattice. It covers the linear algebra that
dominates a network's work and its DSP cost. It says nothing about control flow,
branching or addressing, which are not lattice problems.

## Reproduce

```
docker run --rm -v "$PWD":/w -w /w coqorg/coq:8.20.1 coqc GoldenAlphabet.v
docker run --rm -v "$PWD":/w -w /w coqorg/coq:8.20.1 coqchk -silent -o GoldenAlphabet
```

Verified on `coqorg/coq:8.20.1`, matching this repository's CI. `coqc` exits 0;
`coqchk` reports no type-in-type, no unsafe fixpoints and no assumed positivity.
The file contains zero `Admitted` and zero `Axiom`.

**Negative control**, run before trusting the green: changing `phi_unique`'s
conclusion from `r = phi` to `r = phi + 1` makes compilation **fail** with exit
1. A proof checker that accepts a false statement would be measuring nothing, so
this check is part of the procedure rather than a courtesy.
