# Extending the catalog

The fastest way to add a tile is to edit
[`crates/ring3_adapters/src/fixtures.rs`](../crates/ring3_adapters/src/fixtures.rs)
and re-export the catalog. Tiles live in ring 3 (the adapter ring) because
they are data, not behaviour — you never need to touch the inner rings to
add a new tile.

```bash
cd games/trinity_fold
cargo run --quiet -p trinity_fold_app -- export fixtures/catalog.json
```

Every tile is a `Node`:

```rust
let mut n = node(
    "my_id",                           // stable id, snake_case
    NodeKind::Constraint,              // Constant | Field | Symmetry | Geometry | Constraint | Observable
    "Human-readable name",
    "What this is. One sentence.",
    ClaimStatus::OpenConjecture,       // REQUIRED — see policy below
);
n.requires           = vec!["other_id".into()];
n.incompatible_with  = vec!["bad_id".into()];
n.dimension          = dim(&[("mass", 1)]);   // optional, used by dimensional_sanity
n.value              = Some(125.20);          // Observables: measured value
n.uncertainty        = Some(0.11);            // Observables: 1σ
n.unit               = Some("GeV".into());
n.tags.push("proof_debt".into());             // optional behavioural tags
n.citation           = Some("PDG 2024".into());
```

## Claim-status policy

You **must** pick one of:

| Status | Use when |
|---|---|
| `Verified` | A Qed Coq proof (or equivalent formal derivation) exists. |
| `EmpiricalFit` | The number matches experiment within a stated tolerance but is not derived. |
| `OpenConjecture` | The statement is on the table but not proven; no known falsifier. |
| `HighRiskOrFalsified` | A Boundary theorem or experimental result rules it out. |
| `Unverified` | Placeholder. Will contribute 0 to positive components. |

This mirrors the Coq honesty tags in
[`CONTRIBUTING.md`](../../../CONTRIBUTING.md) (`[NUMERICAL_FIT]`,
`[phenomenological_fit]`, `[MATH_TODO]`, etc.) and is checked at runtime
by the scorer.

## Recognized tags

| Tag | Effect |
|---|---|
| `proof_debt` | Adds 0.3 to that node's contribution to `proof_debt_penalty`. |
| `falsified` | Treated as `HighRiskOrFalsified` for the falsification term. |
| `boundary` | Same as `falsified`. Use for Boundary theorem statements. |
| `compression` | Currently informational; reserved for a future term that rewards reuse of a small set of primitives. |

Unknown tags are silently ignored.

## Adding a triangle

`Catalog::triangles` is a list of 3-tuples of ids. A triangle contributes
to `symmetry_coherence` only when all three tiles are on the board. Use
this for non-obvious co-dependencies (e.g. "if you want BT-3, you must
have placed s_h4 and g_600cell").

## After editing

```bash
cargo test                                                          # all 15 tests (10 scoring + 5 boundary)
cargo run --quiet -p trinity_fold_app -- export fixtures/catalog.json  # refresh web UI data
```

For adding new scoring components or new search strategies, see the
"How to add ..." section in [`ARCHITECTURE.md`](ARCHITECTURE.md). The
relevant ring is different from the tile-extension flow:

- new scoring component → ring 1 (`crates/ring1_constraints`)
- new search strategy → ring 2 (`crates/ring2_search`)
- new IO format → ring 3 (`crates/ring3_adapters`)
- new CLI subcommand → app (`crates/app`)

The web UI consumes `fixtures/catalog.json` directly — there is no build
step.
