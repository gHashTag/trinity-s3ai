# GOLDEN CHAIN (crate folder: `games/trinity_fold/`)

A hypothesis-discovery puzzle for exploring candidate unification structures,
inspired by FoldIt, AlphaFold, and CASP. **GOLDEN CHAIN** is the user-facing
product name; the Cargo workspace and crate names remain `trinity_fold*` for
backwards compatibility with PRs #24 / #25. The Rust canvas UI in
`crates/ring4_canvas` renders the GOLDEN CHAIN concept.

> **GOLDEN CHAIN is not a Theory of Everything, and a high "bridge strength"
> is not evidence for one.** It is a hypothesis-discovery and
> constraint-checking environment whose only deliverable is a tagged
> breakdown of how a candidate fares against a small, illustrative,
> human-curated set of consistency rules and observables.

## The bridge metaphor

GOLDEN CHAIN reframes the puzzle as **building a structural bridge between
two shores of reality**:

* **Data pier** (left) — observational and experimental constraints
  (`NodeKind::Constraint`, `NodeKind::Observable`).
* **Geometry pier** (right) — symmetries, constants, fields, geometric
  structures (`NodeKind::Symmetry`, `NodeKind::Geometry`, `NodeKind::Field`,
  `NodeKind::Constant`).
* **Bridge span** — the player's candidate hypothesis. Each selected tile
  becomes a span node; the span only holds if its claim status is strong
  enough and no falsified tile sits on the board.

If any tile is `HighRiskOrFalsified`, the deck breaks and `BridgeView::integrity`
becomes `Collapsed` — the honesty floor has tripped, regardless of how many
other tiles agree with experiment. Full concept docs are in
[`docs/GOLDEN_CHAIN.md`](docs/GOLDEN_CHAIN.md).

## Why this exists

The Trinity S3AI repository is a active boundary-mapping research program on H4/600-cell
NCG models of the Standard Model (see [`RESEARCH_STATUS.md`](../../README.md) and the
four Boundary Theorems (BT-1–BT-4) in
[`proofs/trinity/BoundaryTheorems.v`](../../proofs/trinity/BoundaryTheorems.v)).
This game inherits that culture:

- It treats **falsification** and **proof debt** as first-class score
  components, not afterthoughts.
- Every tile carries a `ClaimStatus` (`verified`, `empirical_fit`,
  `open_conjecture`, `high_risk_or_falsified`, `unverified`).
- The composite score is normalized and accompanied by the **worst** claim
  status surfaced across all active tiles, so a player cannot accidentally
  read a number as stronger than its underlying claims.

The metaphor (and only the metaphor) borrows from three sources:

| Source | Borrowed idea |
|---|---|
| **FoldIt** | Drag tiles on a board, see a live score breakdown, submit a candidate. |
| **AlphaFold (Evoformer)** | Two-tower split: *Data Tower* (observational/experimental constraints) and *Geometry Tower* (symmetry, geometry, fields, constants), plus Evoformer-style **triangles** that should travel together. |
| **CASP** | A held-out *benchmark* mode that hides selected observable values until after a player submits. |

No actual physics theorem is asserted by the prototype. Tiles whose claim
status is `open_conjecture` or stronger may carry citations into the rest
of the repository (or to PDG/CODATA), but those references describe what
the tile **is**, not what it **proves**.

## Claim-status policy

This taxonomy mirrors the honesty tags used in the Coq sources
(`[PHYSICAL_AXIOM]`, `[NUMERICAL_FIT]`, `[phenomenological_fit]`,
`[MATH_TODO]`, `[LIBRARY_GAP]`) and the
[`anti_numerology_gate.py`](../../scripts/anti_numerology_gate.py) checker.

| Status | Meaning | Score weight (positive contributions) |
|---|---|---|
| `verified` | Backed by a `Qed` Coq proof or equivalent formal derivation. | 1.00 |
| `empirical_fit` | Numerical agreement with experiment within a stated tolerance. **Not** derived from first principles. | 0.40 |
| `open_conjecture` | Stated but not proven; no falsifying evidence yet. | 0.15 |
| `high_risk_or_falsified` | Currently contradicted by data or by an existing Boundary theorem. | 0 (and triggers the falsification penalty) |
| `unverified` | Default for fresh user input. | 0 |

A board that contains **any** `high_risk_or_falsified` tile has its total
score floored at `-0.25`, regardless of other contributions. This is the
honesty floor.

## Architecture: ring crates

The codebase is organized as six inward-pointing rings (Cargo workspace
crates), inspired by the layered "ring" / onion architecture pattern. Each
outer ring may only depend on lower-numbered rings; the inverse is forbidden
and **enforced by integration tests** in
[`crates/app/tests/ring_boundaries.rs`](crates/app/tests/ring_boundaries.rs).

```
+----------------------------------------------------------------+
|  app  (orchestration, CLI)            crates/app                |
|   +----------------------------------------------------------+ |
|   |  ring3_adapters  (IO, fixtures, web export)              | |
|   |   +----------------------------------------------------+ | |
|   |   |  ring2_search  (hill-climb, annealing, LCG RNG)    | | |
|   |   |   +----------------------------------------------+ | | |
|   |   |   |  ring1_constraints  (scoring, weights)       | | | |
|   |   |   |   +----------------------------------------+ | | | |
|   |   |   |   |  ring0_core  (Node, Board, Catalog,    | | | | |
|   |   |   |   |               ClaimStatus — pure types)| | | | |
|   |   |   |   +----------------------------------------+ | | | |
|   |   |   +----------------------------------------------+ | | |
|   |   +----------------------------------------------------+ | |
|   +----------------------------------------------------------+ |
+----------------------------------------------------------------+
```

| Ring | Crate | Allowed to depend on | What lives here |
|---|---|---|---|
| 0 | `ring0_core` | std only | `Node`, `NodeKind`, `Board`, `Catalog`, `ClaimStatus`. No IO, no RNG, no UI. |
| 1 | `ring1_constraints` | ring 0 | `ScoreBreakdown`, `score_board*`, `tower_counts`. Pure functions. |
| 2 | `ring2_search` | ring 0, ring 1 | `hill_climb`, `anneal`, self-contained LCG. Deterministic given seeds. |
| 3 | `ring3_adapters` | ring 0–2 | `fixtures::default_catalog`, JSON load/save, web JSON export. Sole IO boundary. |
| 4 | `ring4_canvas` | ring 0–3 | Rust canvas UI: pure `RenderModel` + input handling, GOLDEN CHAIN view (`bridge::BridgeView`), built-in `recipes`, plus wasm-bindgen browser shell (`Canvas2D`). See [`docs/CANVAS.md`](docs/CANVAS.md) and [`docs/GOLDEN_CHAIN.md`](docs/GOLDEN_CHAIN.md). |

| app | `trinity_fold_app` | all rings | CLI parsing + presentation only. No domain logic. |

Why this matters: every score is reproducible from ring 0+1 alone, so
auditors can rebuild the constraint surface without running any IO. See
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the dependency rules and
how to add a new tile, constraint, or search strategy.

## Scoring model

The scorer (Rust source of truth:
[`crates/ring1_constraints/src/scoring.rs`](crates/ring1_constraints/src/scoring.rs);
JS mirror: [`web/app.js`](web/app.js)) reports an eight-component breakdown,
combined with default weights into a single normalized total. Full
specification: [`docs/SCORING.md`](docs/SCORING.md).

| Component | What it measures |
|---|---|
| `consistency` | Fraction of `requires` satisfied minus `incompatible_with` violations. |
| `dimensional_sanity` | Whether the sum of dimensional signatures over the board is zero. |
| `observable_fit` | For observables that have both a measured `value` and a player-supplied `predicted`, a smooth `1/(1 + z²)` reward weighted by claim status. |
| `proof_debt_penalty` | Climbs with `open_conjecture`/`unverified` tiles and with the `proof_debt` tag. |
| `falsification_penalty` | Heaviest term. Climbs with `high_risk_or_falsified` tiles or `no_go`/`falsified` tags. |
| `simplicity` | Peaks around 10 tiles (rewards compression, penalizes both trivial and bloated boards). |
| `symmetry_coherence` | Rewards boards that contain at least one Symmetry and one Geometry tile, plus completed *Evoformer-style triangles*. |
| `reproducibility` | Fraction of tiles carrying a citation (PDG entry, Coq theorem name, arXiv id, etc.). |

## What is explicitly **not** claimed

- That the catalog encodes a complete or correct picture of physics.
  The default catalog is illustrative.
- That a high `total` score implies a unification claim, a falsification of
  the Standard Model, or any positive scientific result. It does not.
- That the local-search engine (`hill_climb` / `anneal`) "discovers" a
  formula. It only navigates a fixed score surface over a fixed tile set.
- That tiles marked `verified` are verified by this game. They inherit
  their status from the rest of the Trinity S3AI repository or from the
  PDG/CODATA reference cited; the game just propagates the tag.

## Running the prototype

### Rust CLI

```bash
cd games/trinity_fold

# Score a hand-picked board:
cargo run --quiet -p trinity_fold_app -- score "s_su2,s_u1,s_su3,f_higgs,f_fermions,cn_anomaly,o_higgs_mass"

# Run the deterministic hill climber from an empty board:
cargo run --quiet -p trinity_fold_app -- search

# Reproducible simulated annealing:
cargo run --quiet -p trinity_fold_app -- search --anneal --seed 42 --iters 2000

# Export the catalog (used by the web UI):
cargo run --quiet -p trinity_fold_app -- export fixtures/catalog.json

# Benchmark mode: hides held-out observables before scoring.
cargo run --quiet -p trinity_fold_app -- benchmark "s_su2,s_u1,f_higgs,o_higgs_mass"
```

### Web UI (Rust canvas, recommended)

The canvas UI is implemented in Rust (`ring4_canvas`) and runs in the
browser as WebAssembly via Canvas2D. Build it once:

```bash
cd games/trinity_fold
wasm-pack build crates/ring4_canvas --target web --features wasm \
  --out-dir ../../web/canvas/pkg
python3 -m http.server 8000
# then open http://localhost:8000/games/trinity_fold/web/canvas/
```

The game state, layout, and hit-testing all live in Rust; JavaScript only
forwards DOM events into the wasm module. See
[`docs/CANVAS.md`](docs/CANVAS.md) for the full architecture, how to add a
new UI interaction, and limitations.

### Legacy static UI

The original dependency-free static HTML/CSS/JS page is kept for
environments where building wasm is not an option. It mirrors a subset of
the Rust scoring rules and is no longer the source of truth.

```bash
cd games/trinity_fold
python3 -m http.server 8000
# then open http://localhost:8000/web/
```

Use the `Benchmark mode` checkbox to hide the held-out observable values
listed in [`docs/BENCHMARK.md`](docs/BENCHMARK.md). Click any tile to add or
remove it from the board. The score panel updates live and surfaces the
worst claim status across active tiles.

## Adding nodes and constraints

See [`docs/EXTENDING.md`](docs/EXTENDING.md). In short: every new tile must
specify a `ClaimStatus`. The build will pass without one (the field has a
default of `Unverified`), but any contribution it makes to a positive score
component will be weighted at zero — by design.

## Tests

```bash
cd games/trinity_fold
cargo test
```

Tests cover empty boards, unmet `requires`, the falsification floor,
deterministic search, and observable-fit reward. They are intentionally
sanity-level checks, not a guarantee that scoring rules match any external
specification.

## Layout

```
games/trinity_fold/
├── Cargo.toml                      (virtual workspace manifest)
├── README.md                       (this file)
├── docs/
│   ├── ARCHITECTURE.md             (ring rules, dependency direction, how-to-extend)
│   ├── SCORING.md
│   ├── BENCHMARK.md
│   └── EXTENDING.md
├── crates/
│   ├── ring0_core/                 (domain types — Node, Board, Catalog, ClaimStatus)
│   │   └── src/{lib,board,claim,node}.rs
│   ├── ring1_constraints/          (scoring; depends on ring0)
│   │   └── src/{lib,scoring}.rs
│   ├── ring2_search/               (hill-climb, anneal, LCG; depends on ring0+1)
│   │   └── src/{lib,search,rng}.rs
│   ├── ring3_adapters/             (fixtures, JSON IO, web export; depends on ring0–2)
│   │   └── src/{lib,fixtures,io,web}.rs
│   └── app/                        (CLI binary `trinity-fold`; composes all rings)
│       ├── src/main.rs
│       └── tests/
│           ├── scoring.rs          (end-to-end scoring + search tests)
│           └── ring_boundaries.rs  (dependency-direction guard tests)
├── fixtures/
│   └── catalog.json                (illustrative tiles, exported from ring3 fixtures)
└── web/
    ├── app.js
    ├── index.html
    └── style.css
```

## Limitations

- The default catalog is small (~25 nodes). The score surface is
  correspondingly shallow; do not over-interpret search trajectories.
- The dimensional sanity check only sums per-base-dimension exponents over
  selected nodes; it does not parse Lagrangian densities.
- The benchmark mode hides observable *values*, not nodes — players still
  see the observable exists. A more rigorous CASP analogue would require
  splitting catalog versions.
- No multiplayer / collective-intelligence backend. Trinity Fold is a
  local-first prototype.
- No Coq integration: a `verified` tag in the catalog asserts that
  Trinity S3AI considers the cited object verified, not that this game
  verified it.

## License

MIT (consistent with `trinity_rust/Cargo.toml`).
