# Trinity Fold

A puzzle prototype for exploring candidate unification structures, inspired
by FoldIt, AlphaFold, and CASP.

> **Trinity Fold is not a Theory of Everything, and a high score in the
> game is not evidence for one.** It is a hypothesis-discovery and
> constraint-checking environment whose only deliverable is a tagged
> breakdown of how a candidate fares against a small, illustrative,
> human-curated set of consistency rules and observables.

## Why this exists

The Trinity S3AI repository is a constructive negative result on H4/600-cell
NCG models of the Standard Model (see [`SALVAGE.md`](../../README.md) and the
four No-Go Theorems in
[`proofs/trinity/NoGoTheorems.v`](../../proofs/trinity/NoGoTheorems.v)).
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
| `high_risk_or_falsified` | Currently contradicted by data or by an existing No-Go theorem. | 0 (and triggers the falsification penalty) |
| `unverified` | Default for fresh user input. | 0 |

A board that contains **any** `high_risk_or_falsified` tile has its total
score floored at `-0.25`, regardless of other contributions. This is the
honesty floor.

## Scoring model

The scorer (Rust source of truth:
[`src/scoring.rs`](src/scoring.rs); JS mirror:
[`web/app.js`](web/app.js)) reports an eight-component breakdown,
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
cargo run --quiet -- score "s_su2,s_u1,s_su3,f_higgs,f_fermions,cn_anomaly,o_higgs_mass"

# Run the deterministic hill climber from an empty board:
cargo run --quiet -- search

# Reproducible simulated annealing:
cargo run --quiet -- search --anneal --seed 42 --iters 2000

# Export the catalog (used by the web UI):
cargo run --quiet -- export fixtures/catalog.json

# Benchmark mode: hides held-out observables before scoring.
cargo run --quiet -- benchmark "s_su2,s_u1,f_higgs,o_higgs_mass"
```

### Web UI

The browser UI is dependency-free static HTML/CSS/JS. It mirrors the Rust
scoring rules and re-uses the same `fixtures/catalog.json`.

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
├── Cargo.toml
├── README.md            (this file)
├── docs/
│   ├── ARCHITECTURE.md
│   ├── SCORING.md
│   ├── BENCHMARK.md
│   └── EXTENDING.md
├── fixtures/
│   └── catalog.json     (illustrative tiles, exported from src/fixtures.rs)
├── src/
│   ├── board.rs
│   ├── claim.rs
│   ├── fixtures.rs
│   ├── io.rs
│   ├── lib.rs
│   ├── main.rs
│   ├── node.rs
│   ├── scoring.rs
│   └── search.rs
├── tests/
│   └── scoring.rs
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
