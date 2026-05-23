# Architecture

Trinity Fold is intentionally small. It is a single Rust crate plus a static
web frontend. There is no server, no database, no telemetry.

## Module map

```
src/
├── claim.rs       ClaimStatus enum + positive-score weighting per claim
├── node.rs        Node struct, NodeKind, Tower (Data | Geometry)
├── board.rs       Board (set of node ids) + Catalog (pool + Evoformer triangles)
├── scoring.rs     8-component breakdown, weight defaults, total composition
├── search.rs      hill_climb + simulated annealing with a self-contained LCG
├── fixtures.rs    Default illustrative catalog + benchmark hold-out ids
├── io.rs          JSON load/save for the catalog
├── lib.rs         re-exports
└── main.rs        CLI subcommands: score, benchmark, search, export, help
```

## Two-tower abstraction

`NodeKind::tower()` maps each tile to one of two towers:

- **Data Tower** — `Observable`, `Constraint`. Anything sourced from
  experiment, PDG/CODATA, or a No-Go theorem.
- **Geometry Tower** — `Constant`, `Field`, `Symmetry`, `Geometry`.
  Anything that lives on the math side.

The score does not multiply the two towers together (we are not actually
running an Evoformer). The towers serve two purposes:

1. **UI separation.** The web frontend renders them as two side panels so a
   player can see at a glance whether they are "all maths, no data" or vice
   versa.
2. **Triangle hints.** A `Catalog::triangles` field holds triples that
   should travel together. They contribute to `symmetry_coherence` only
   when all three tiles are on the board, mirroring (loosely) the
   triangular updates in AlphaFold's Evoformer.

## Honesty plumbing

Three places are responsible for keeping the prototype honest:

1. **`ClaimStatus`.** Discriminant order matters; the scorer walks every
   active node and propagates the worst status into
   `ScoreBreakdown::worst_claim`.
2. **Falsification floor.** Boards with any `HighRiskOrFalsified` tile are
   capped at total ≤ −0.25, so they cannot read as "good" no matter what.
3. **Disclaimers.** CLI and UI both print/render the same disclaimer next
   to every reported number.

## Source-of-truth duality

Both the Rust core and the browser UI implement scoring. The Rust core is
the source of truth — when in doubt, run `cargo test`. The browser code is
a strict mirror so the game can run offline from `file://` or any static
server. If you change one, change the other; the test suite does not yet
enforce parity.

## What is intentionally absent

- **No probability claims.** The score is a normalized weighted sum, not a
  posterior. It is not interpretable as P(theory).
- **No machine learning model.** The "AI/search component" is a local
  search over a fixed catalog. No external data, no training run, no
  embeddings.
- **No persistence.** Boards live in memory; the CLI is stateless across
  invocations.
- **No network.** The web UI does one `fetch()` to load the static
  catalog. Nothing else.
