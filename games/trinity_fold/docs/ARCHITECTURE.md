# Architecture

Trinity Fold is organized as a five-crate Cargo **workspace** following a
ring (onion) architecture. Dependencies point strictly INWARD: each outer
ring may depend on lower-numbered rings, never the reverse. This is the
architectural pattern this project borrows from `trios-a2a`-style layered
designs (where access to that reference was unavailable at port time, the
ring vocabulary and the inward-only rule are kept as the conceptual core).

## Ring diagram

```
                ╭──────────────────────────────────────────────────────╮
                │                       app                            │
                │   crates/app  (trinity-fold CLI binary)              │
                │   ╭──────────────────────────────────────────────╮   │
                │   │                ring 3                        │   │
                │   │   ring3_adapters                             │   │
                │   │   • fixtures::default_catalog                │   │
                │   │   • io::{load_catalog, save_catalog}         │   │
                │   │   • web::{catalog_to_web_json, ...}          │   │
                │   │   ╭──────────────────────────────────────╮   │   │
                │   │   │              ring 2                  │   │   │
                │   │   │   ring2_search                       │   │   │
                │   │   │   • hill_climb (deterministic)       │   │   │
                │   │   │   • anneal    (seed-stable)          │   │   │
                │   │   │   • Lcg (self-contained RNG)         │   │   │
                │   │   │   ╭──────────────────────────────╮   │   │   │
                │   │   │   │          ring 1              │   │   │   │
                │   │   │   │   ring1_constraints          │   │   │   │
                │   │   │   │   • ScoreBreakdown           │   │   │   │
                │   │   │   │   • ScoreWeights             │   │   │   │
                │   │   │   │   • score_board(_with)       │   │   │   │
                │   │   │   │   • tower_counts             │   │   │   │
                │   │   │   │   ╭──────────────────────╮   │   │   │   │
                │   │   │   │   │       ring 0         │   │   │   │   │
                │   │   │   │   │   ring0_core         │   │   │   │   │
                │   │   │   │   │   • Node / NodeKind  │   │   │   │   │
                │   │   │   │   │   • Board / Catalog  │   │   │   │   │
                │   │   │   │   │   • ClaimStatus      │   │   │   │   │
                │   │   │   │   │   • Tower            │   │   │   │   │
                │   │   │   │   ╰──────────────────────╯   │   │   │   │
                │   │   │   ╰──────────────────────────────╯   │   │   │
                │   │   ╰──────────────────────────────────────╯   │   │
                │   ╰──────────────────────────────────────────────╯   │
                ╰──────────────────────────────────────────────────────╯
```

## Dependency rules

These are the binding invariants. They are checked at `cargo test` time by
[`crates/app/tests/ring_boundaries.rs`](../crates/app/tests/ring_boundaries.rs);
adding a forbidden edge will fail CI.

| From / to            | ring 0 | ring 1 | ring 2 | ring 3 | app |
|----------------------|:------:|:------:|:------:|:------:|:---:|
| **ring0_core**       |   —    |  NO    |  NO    |  NO    | NO  |
| **ring1_constraints**|  yes   |   —    |  NO    |  NO    | NO  |
| **ring2_search**     |  yes   |  yes   |   —    |  NO    | NO  |
| **ring3_adapters**   |  yes   |  yes   |  yes   |   —    | NO  |
| **app**              |  yes   |  yes   |  yes   |  yes   |  —  |

Additional, narrower rules enforced by the boundary tests:

- `ring0_core` may not pull in `serde_json` (it is the type layer, not the
  serialization layer) and may not use `std::fs`, `std::net`,
  `std::process`, or `std::thread::sleep` anywhere in its source.
- `ring1_constraints` and `ring2_search` may not depend on `serde_json`.
- Only `ring3_adapters` is allowed to touch the filesystem.

## Two-tower abstraction (inside ring 0)

`NodeKind::tower()` maps each tile to one of two towers:

- **Data Tower** — `Observable`, `Constraint`. Anything sourced from
  experiment, PDG/CODATA, or a No-Go theorem.
- **Geometry Tower** — `Constant`, `Field`, `Symmetry`, `Geometry`.
  Anything that lives on the math side.

The score does not multiply the two towers together (we are not actually
running an Evoformer). The towers serve two purposes:

1. **UI separation.** The web frontend renders them as two side panels so a
   player can see at a glance whether they are "all maths, no data".
2. **Triangle hints.** A `Catalog::triangles` field holds triples that
   should travel together. They contribute to `symmetry_coherence` only
   when all three tiles are on the board, mirroring (loosely) the
   triangular updates in AlphaFold's Evoformer.

## Honesty plumbing

Three places are responsible for keeping the prototype honest:

1. **`ClaimStatus`** (ring 0). Discriminant order matters; the ring 1
   scorer walks every active node and propagates the worst status into
   `ScoreBreakdown::worst_claim`.
2. **Falsification floor** (ring 1). Boards with any `HighRiskOrFalsified`
   tile are capped at total ≤ −0.25, so they cannot read as "good" no
   matter what other components score.
3. **Disclaimers** (app + web). CLI and UI both print/render the same
   disclaimer next to every reported number.

## How to add a new tile, constraint, or search strategy

The right insertion ring depends on what you are adding. Picking the wrong
ring will either (a) duplicate work, or (b) fail the boundary tests.

### New tile (constant, field, symmetry, geometry, constraint, observable)

1. Append a new `Node { ... }` to `default_catalog()` in
   [`crates/ring3_adapters/src/fixtures.rs`](../crates/ring3_adapters/src/fixtures.rs).
2. Choose a `ClaimStatus` honestly. New unsourced content defaults to
   `Unverified` (zero positive weight). Use `Verified` only if it points to
   a `Qed` proof or an authoritative reference (PDG/CODATA).
3. If the tile has a measured value, set `value`, `uncertainty`, and `unit`.
   If it makes a prediction, also set `predicted` — that drives the
   `observable_fit` term.
4. If it requires other tiles to be meaningful, list them in `requires`.
   If it falsifies a combination, use `incompatible_with` or the `no_go` tag.
5. Re-run `cargo run -p trinity_fold_app -- export fixtures/catalog.json`
   to refresh the web UI's data file.

You do NOT need to touch ring 0/1/2 to add a tile. That's the point of the
architecture.

### New scoring component

1. Add a field to `ScoreBreakdown` and `ScoreWeights` in
   [`crates/ring1_constraints/src/scoring.rs`](../crates/ring1_constraints/src/scoring.rs).
2. Compute it inside `score_board_with`, using only inputs available from
   ring 0 (`Catalog`, `Board`, `Node`, `ClaimStatus`). If you find yourself
   needing IO or randomness, you are in the wrong ring.
3. Add a sanity test in
   [`crates/app/tests/scoring.rs`](../crates/app/tests/scoring.rs).
4. Mirror the change in [`web/app.js`](../web/app.js) to keep the JS scorer
   in lockstep with the Rust source of truth.

### New search strategy

1. Add a new function (e.g. `tabu_search`) to
   [`crates/ring2_search/src/search.rs`](../crates/ring2_search/src/search.rs).
   It must take a seed parameter for reproducibility and use the local
   `Lcg` rather than introducing a new RNG dependency.
2. Re-export it from `ring2_search::lib.rs`.
3. Wire a CLI flag in [`crates/app/src/main.rs`](../crates/app/src/main.rs).
4. Add a determinism test (run twice with the same seed, expect identical
   `best_board.selected`).

### New adapter / IO format

Add a module to `ring3_adapters` (e.g. `src/csv.rs` for CSV import). Only
this ring is allowed to perform filesystem or network access.

## Running tests, CLI, and web UI

```bash
cd games/trinity_fold

# All workspace tests (10 scoring + 5 boundary):
cargo test

# Just the dependency-direction guards:
cargo test -p trinity_fold_app --test ring_boundaries

# CLI:
cargo run -p trinity_fold_app -- score "s_su2,s_u1,f_higgs"
cargo run -p trinity_fold_app -- search --anneal --seed 42 --iters 2000
cargo run -p trinity_fold_app -- export fixtures/catalog.json

# Web UI (static, no build step):
python3 -m http.server 8000  # then open http://localhost:8000/web/
```

## Source-of-truth duality

Both the Rust core and the browser UI implement scoring. The Rust core
(ring 1) is the source of truth — when in doubt, run `cargo test`. The
browser code is a strict mirror so the game can run offline from `file://`
or any static server. If you change one, change the other; the test suite
does not yet enforce parity.

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
- **No secrets, no Railway/Postgres dependency, no external services.**
  Trinity Fold runs entirely from a checkout of this repository.

## Note on `trios-a2a`

The user request asked for "ring architecture as in `trios-a2a`". At port
time, `gHashTag/trios-a2a` was not reachable via `gh`, so we could not
mirror its exact crate layout. The conceptual pattern is preserved: pure
domain types innermost, scoring next, search above that, IO at the
boundary, orchestration on top — with the inward-only dependency rule
enforced by integration tests. If the reference repo later becomes
available and uses different ring names or boundaries, the layout here
should be re-aligned.
