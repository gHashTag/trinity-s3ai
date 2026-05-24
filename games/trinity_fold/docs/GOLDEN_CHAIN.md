# GOLDEN CHAIN — concept and architecture

> **GOLDEN CHAIN is the user-facing product name for the game whose source
> code lives at `games/trinity_fold/`.** The Cargo workspace and crate names
> were created earlier under the working title "Trinity Fold" and are kept
> for backwards compatibility; the UI now renders the GOLDEN CHAIN concept.
>
> **GOLDEN CHAIN is a hypothesis-discovery puzzle. It is NOT a proven
> Theory of Everything, and a high "bridge strength" is not evidence for
> one.** The game inherits the honesty policy of the surrounding repository
> (see [`README.md`](../README.md), [`FOUNDATIONS.md`](../../../docs/analysis/FOUNDATIONS.md),
> and the four Boundary theorems in
> [`proofs/trinity/BoundaryTheorems.v`](../../../proofs/trinity/BoundaryTheorems.v)).

## The metaphor

GOLDEN CHAIN reframes the Trinity Fold prototype as a **structural bridge
between two shores of reality**:

| Shore / pier | What sits there | Source crate |
|---|---|---|
| **Data pier** (left) | Observational and experimental constraints — PDG observables, anomaly cancellation, unitarity bounds. Conceptually the "AlphaFold data side". | `NodeKind::Constraint` + `NodeKind::Observable` in `ring0_core` |
| **Geometry pier** (right) | Theoretical symmetries, constants, fields, geometric structures (H4 / 600-cell, Clifford algebras, NCG spectral triples). | `NodeKind::Symmetry`, `NodeKind::Geometry`, `NodeKind::Field`, `NodeKind::Constant` |
| **Bridge span** (middle) | The player's *candidate hypothesis* — a set of tiles drawn from both piers. The span only "holds" if the underlying claim statuses are strong enough and no falsified tile sits on it. | `bridge::SpanNode` projected from `Board` + `Catalog` + `ScoreBreakdown` |

The neuro-symbolic loop is:

1. Player (human intuition) selects tiles from both piers, optionally
   triggered by clicking a built-in **Recipe** chip.
2. `ring1_constraints::score_board` (the symbolic / machine side) computes a
   reproducible score with eight components and a `worst_claim` tag.
3. `ring4_canvas::bridge::BridgeView` projects that result into a bridge
   view: pier counts, span nodes coloured by claim status, an
   `integrity` verdict, a compression metric, and a falsified-tile count.
4. The canvas renders the bridge. If any tile is `HighRiskOrFalsified`, the
   deck line is drawn with a gap labelled `COLLAPSE` and `BridgeView::integrity`
   becomes `Collapsed` — the **honesty floor** has tripped.

## Claim-status visual language

| Status (ring 0) | Span colour (ring 4) | Meaning |
|---|---|---|
| `Verified` | **Gold** (`#d4af37`) — bridge gold | Backed by a `Qed` Coq proof or equivalent formal derivation. |
| `EmpiricalFit` | Steel blue | Numerical agreement with experiment within a stated tolerance. **Not** derived from first principles. |
| `OpenConjecture` | Amber | Stated but not proven; no falsifying evidence yet. |
| `HighRiskOrFalsified` | Red — **deck breaks here** | Currently contradicted by data or by an existing Boundary theorem. Triggers the honesty floor. |
| `Unverified` | Grey | Default for fresh user input. Carries no positive contribution. |

Colours are defined in `Theme` (`crates/ring4_canvas/src/render.rs`). The
`worst_claim` field of `ScoreBreakdown` is rendered next to the total in
every state of the UI — no surface area exists for hiding it.

## Honesty floor

`BridgeView::integrity` is computed from the score and span statuses:

```
Empty       — no tiles placed yet
Sound       — all cables Gold or Empirical; no falsified node; proof_debt_penalty < 0.25
Provisional — at least one Open / Unverified cable, or proof_debt_penalty >= 0.25, but no falsified node
Collapsed   — one or more falsified cables; the honesty floor has tripped
```

`Collapsed` is also what `ring1_constraints::score_board` does internally:
the total is capped at `-0.25` whenever a falsified tile is on the board.
GOLDEN CHAIN merely surfaces that cap as a visual collapse rather than
burying it in a number.

## Space-fold motif

The arcs drawn behind the bridge deck are a **visual** hint at "compressing
a high-dimensional building-block space into a small consistent set". They
are decorative: the radius depends on `BridgeView::compression`
(`span_nodes.len() / catalog.nodes.len()`), but compression does **not**
feed into the score. The arcs exist to remind the player that the goal is
"small consistent hypothesis", not "place every tile".

## Recipes

A `Recipe` (see `crates/ring4_canvas/src/recipes.rs`) is a named list of
catalog ids plus a short rationale. Clicking a recipe chip in the UI
emits `UiEvent::LoadRecipe(id)`, which replaces the board with the recipe's
tile set and rescore from scratch. Recipes ship with built-in starting
points (`sm_core`, `h4_geometry`, `anomaly_audit`) — none of them is a
solution to the puzzle; they are diagnostic shortcuts.

To add a recipe today, append to `builtin_recipes()`. The longer-term plan
is for `ring3_adapters` to expose a JSON loader so community contributions
do not require recompiling, but that loader is not implemented yet — see
[`EXTENDING.md`](EXTENDING.md) for the proposed API.

## Architecture: where the bridge lives

GOLDEN CHAIN does **not** introduce a new ring. The bridge is a **view**
over the existing ring 0..3 outputs:

```
ring0_core  <-  ring1_constraints  <-  ring2_search  <-  ring3_adapters  <-  ring4_canvas  <-  app
   types         scoring               search             IO / fixtures      bridge + render +  CLI
                                                                              wasm shell
```

The bridge view (`bridge::BridgeView`) only depends on `ring0_core` types
(`Board`, `Catalog`, `ClaimStatus`) and `ring1_constraints::ScoreBreakdown`.
It introduces no new scoring rules — if a future bridge metric would change
the score, it belongs in `ring1_constraints`, not here.

This invariant is enforced by `crates/app/tests/ring_boundaries.rs`:

* `ring4_canvas_depends_inward_only` — ring 4 may pull in rings 0..3 only.
* `no_inner_ring_imports_ring4` — no inner ring may pull in `ring4_canvas`,
  `wasm-bindgen`, `web-sys`, `js-sys`, or `console_error_panic_hook`.

## How to add a new bridge feature

| Want to ... | Edit |
|---|---|
| Add a new span-status colour          | `render.rs::Theme::default()` + `span_color()` |
| Add a new integrity verdict           | `bridge.rs::BridgeIntegrity` + `BridgeView::build` + `integrity_color()` |
| Add a new UI interaction              | Add a `UiEvent` variant + handle it in `AppState::apply` + render a hit region in `render.rs` |
| Add a new built-in recipe             | Append to `recipes.rs::builtin_recipes()` |
| Add a new tile or constraint          | Edit `ring0_core` (the *type*) and `ring3_adapters::fixtures` (the *fixture*); never edit ring 4 |
| Change the score                      | Edit `ring1_constraints::scoring`; never edit ring 4 |
| Change the search strategy            | Edit `ring2_search`; never edit ring 4 |

## Running

```bash
cd games/trinity_fold

# Native: run the full Rust test suite (including the bridge tests).
cargo test --workspace

# CLI score (unchanged from earlier waves).
cargo run --quiet -p trinity_fold_app -- score "s_su2,s_u1,s_su3,f_higgs,f_fermions,cn_anomaly,o_higgs_mass"

# Build the canvas UI for the browser:
wasm-pack build crates/ring4_canvas --target web --features wasm \
    --out-dir ../../web/canvas/pkg

# Serve the static host:
python3 -m http.server 8000
# then open http://localhost:8000/web/canvas/
```

## Limitations

* **No proof of physics.** GOLDEN CHAIN is a puzzle. The default catalog is
  illustrative. The score surface is shallow. No claim about reality is
  asserted by reaching any total.
* **`trios-a2a` ring pattern not cross-imported.** The task brief asked the
  ring architecture to mirror `gHashTag/trios-a2a`. That repository is not
  reachable from this environment; the architecture follows the conventions
  PR #25 already established in this repository and is consistent with the
  standard layered-ring pattern.
* **Triangle hint lines are still a stub.** `render::draw_triangles` does
  not draw the connecting yellow lines for completed Evoformer-style
  triangles yet; the constraint is still rewarded by the scorer, only the
  visual is pending.
* **wasm-pack build is not invoked here.** The sandbox does not ship
  `wasm-pack`; the wasm shell module is gated behind
  `#[cfg(all(target_arch = "wasm32", feature = "wasm"))]` so native builds
  and tests are unaffected. Build instructions are above.
* **Recipes are in-crate.** The JSON loader hook is documented but not
  wired through `ring3_adapters` yet.
* **No multiplayer / collective intelligence backend.** GOLDEN CHAIN is
  local-first.

## What is explicitly NOT claimed

* That GOLDEN CHAIN has discovered, verified, or even narrowed any candidate
  unification model.
* That a `Sound` integrity verdict means the candidate is "true". It means
  the board avoids the falsification floor and carries low proof debt
  within this illustrative catalog.
* That the built-in recipes are correct physical theories. They are
  diagnostic starting points.
* That this game is a substitute for the formal proofs in `proofs/`, the
  empirical analyses in `derivations/`, or the falsifiability assessments
  in `Trinity_Falsifiability_Assessment.md`.
