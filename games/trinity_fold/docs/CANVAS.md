# Rust canvas UI (ring 4)

The canvas UI is implemented as a fifth crate in the workspace,
[`ring4_canvas`](../crates/ring4_canvas), sitting just outside the IO ring
and just inside the orchestration crate:

```
ring0_core  <-  ring1_constraints  <-  ring2_search  <-  ring3_adapters  <-  ring4_canvas  <-  app
   types          scoring               search             IO / fixtures      UI render +       CLI
                                                                              wasm shell
```

Dependency direction is enforced by
[`crates/app/tests/ring_boundaries.rs`](../crates/app/tests/ring_boundaries.rs).
No inner ring depends on `ring4_canvas`, `wasm-bindgen`, `web-sys`,
`js-sys`, or `console_error_panic_hook` (browser-only); the test fails the
build if anyone adds such a dependency by accident.

## Why a separate ring (and why Rust, not JavaScript)

The original prototype shipped with a hand-written JavaScript mirror of the
scoring model in `web/app.js`. That has two problems:

1. **Two sources of truth.** Every score change had to be ported by hand from
   `ring1_constraints/src/scoring.rs` to `web/app.js`. The JS copy was best-
   effort and could (and did) drift.
2. **No claim-status enforcement on the UI side.** Browser code could quietly
   ignore `worst_claim` or render a tile without its claim chip.

Ring 4 fixes both by routing **all** rendering through the same Rust pipeline
that produced the original scores. The browser shell becomes pure presentation:
mouse coordinates in, render primitives out. The game state, scorer, search
moves, and benchmark logic are the *same* code paths exercised by `cargo run`.

## Module layout

| File | Purpose |
|---|---|
| `src/state.rs`   | `AppState` — owns `Board`, `Catalog`, latest `ScoreBreakdown`, view options, recipes, and the GOLDEN BRIDGE view. The only mutator is `AppState::apply(UiEvent)`. |
| `src/input.rs`   | `UiEvent`, `InputAction`, `KeyCode`. `resolve(model, action) -> Option<UiEvent>` does pure hit-testing against the latest render model. |
| `src/render.rs`  | `layout(state, viewport, theme) -> RenderModel`. Emits `RenderPrimitive`s (rect, line, circle, text) and `HitBox`es — no DOM types. Renders the GOLDEN BRIDGE deck (piers + span line + space-fold motif + integrity banner + recipe rail) above the two towers. |
| `src/bridge.rs`  | `BridgeView` — view projection over `Board` + `Catalog` + `ScoreBreakdown`. Computes pier counts, span nodes with `SpanStatus`, `BridgeIntegrity` (Empty/Sound/Provisional/Collapsed), and a `compression` ratio. Introduces no new scoring. |
| `src/recipes.rs` | Built-in `Recipe` list (named tile sets with rationale). Clicking a recipe chip emits `UiEvent::LoadRecipe(id)`. |
| `src/wasm.rs`    | Browser shell, compiled only for `target_arch = "wasm32"` and feature `wasm`. Wires DOM events to `input::resolve` and paints `RenderModel` onto a `CanvasRenderingContext2d`. |

The Rust pipeline runs:

```
DOM event  ─► InputAction ─► resolve(model) ─► UiEvent ─► AppState::apply ─► layout() ─► RenderModel ─► Canvas2D
```

Every arrow except the first and the last is pure Rust, unit-tested without
a browser.

## Building & running locally

### Native sanity checks (no browser needed)

```bash
cd games/trinity_fold
cargo test                                # full workspace, includes ring4 unit tests
cargo test -p ring4_canvas                # ring4 unit tests in isolation (19 tests)
cargo build --workspace                   # compile everything
```

### Browser build (wasm-pack)

The canvas UI runs as a WebAssembly module loaded by
[`web/canvas/index.html`](../web/canvas/index.html). Build the bundle once:

```bash
cd games/trinity_fold
wasm-pack build crates/ring4_canvas \
  --target web \
  --features wasm \
  --out-dir ../../web/canvas/pkg
```

(If `wasm-pack` is unavailable, install it via
`cargo install wasm-pack` or follow https://rustwasm.github.io/wasm-pack/.)

Then serve the directory and open the page:

```bash
python3 -m http.server 8000
# http://localhost:8000/games/trinity_fold/web/canvas/
```

The page detects a missing bundle and shows a fallback notice with the same
build command, so a fresh checkout never silently breaks. The fallback also
embeds a static SVG snapshot of the GOLDEN BRIDGE layout so the preview is
visually meaningful even without the wasm bundle.

### Static SVG fallback

To regenerate the snapshot used by the fallback panel:

```bash
cd games/trinity_fold
cargo run -p ring4_canvas --example snapshot_svg -- \
  web/canvas/snapshot.svg
```

The snapshot is produced by calling the same
`ring4_canvas::render::layout` function the wasm shell consumes, so the
fallback cannot drift from the live UI without a corresponding change in
ring 4. It is intentionally a static picture of the initial state (empty
board, default catalog, benchmark off) and is clearly labelled as
non-interactive in the page.

### Legacy JS UI

The original static HTML page in `web/index.html` is still present and
unchanged. It re-uses `fixtures/catalog.json` and mirrors a subset of the
Rust scorer. It is kept for environments where building wasm is not an
option — but it is no longer the source of truth, and the README has been
updated to point at the canvas UI first.

## How input flows

```
        HtmlCanvasElement.click ────► MouseEvent { x, y }
                                            │
                                            ▼
                              InputAction::Click { x, y }
                                            │
                                  resolve(&model, action)
                                            │
                                            ▼
                              UiEvent::ToggleTile("s_su2")
                                            │
                                  state.apply(event)
                                            │
                                            ▼
                             layout(&state, viewport, theme)
                                            │
                                  paint(&ctx, &model)
```

The hit-test is *purely* a function of the latest render model and the
cursor coordinates. There is no shadow state in JavaScript — the JS layer
holds no game data at all.

## Adding a new UI interaction

1. Add a variant to `UiEvent` in `ring4_canvas/src/input.rs`.
2. Teach `AppState::apply` to handle it in `ring4_canvas/src/state.rs` and
   return `true` if it changed something visible.
3. If it is triggered by a click on a region: extend `HitRegion` and emit a
   `HitBox` for it from `render::layout`.
4. If it is triggered by a key: extend `KeyCode` and its `from_dom_key`
   mapping. The wasm shell will route the key automatically; no JS edits.
5. Cover the event with a unit test under `#[cfg(test)]` in `state.rs` or
   `input.rs`. Hit-test tests should use `model_with(vec![...])` so they
   don't depend on the full catalog layout.

## Testing surface

Ring 4 ships 38 unit tests, all native (no browser):

- `state::tests` — apply/toggle/clear/benchmark/hill-climb/anneal determinism,
  unknown-id handling, GOLDEN BRIDGE view tracking, recipe loading.
- `render::tests` — hit-region coverage of the catalog, toolbar buttons,
  worst-claim text, GOLDEN BRIDGE branding, integrity label, collapse
  warning, recipe-chip hits, colour CSS formatting, truncation.
- `input::tests` — pure hit-testing, including topmost-wins overlap and
  recipe-chip → `LoadRecipe` resolution.
- `bridge::tests` — pier partitioning, falsified-tile collapse,
  provisional-vs-sound integrity, compression bounds, tower ordering.
- `recipes::tests` — built-in recipes are non-empty and rebind cleanly
  against the default catalog.

The GOLDEN BRIDGE concept (piers, span, honesty floor, recipes, space-fold
motif) is documented separately in
[`GOLDEN_BRIDGE.md`](GOLDEN_BRIDGE.md).

The boundary test
[`ring_boundaries::no_inner_ring_imports_ring4`](../crates/app/tests/ring_boundaries.rs)
asserts that no lower ring takes a dependency on ring 4 or on browser-only
crates. Adding `web-sys` to (say) `ring0_core` fails the test.

## Limitations of this PR

- **The wasm bundle is not built in CI here**, because the sandbox does not
  ship `wasm-pack` and the toolchain prerequisites (`rustup target add
  wasm32-unknown-unknown`). All Rust code that wasm-pack would compile is
  exercised by the native unit tests; the wasm-only `src/wasm.rs` module is
  gated by `#[cfg(all(target_arch = "wasm32", feature = "wasm"))]` so it
  does not affect native builds. Validation in a real browser is the
  reviewer's first manual step.
- **Triangle hint lines are not drawn yet.** `render::draw_triangles` is a
  stub. Implementing it requires carrying tile centroids out of the tower
  layout pass and joining them by Evoformer triplet. The score panel still
  reflects triangle completion via `symmetry_coherence` and the scorer's
  notes.
- **No drag-and-drop.** Tiles toggle on click, by design — the underlying
  `Board` is a set, not a 2D layout. Adding drag would require introducing
  free positions to `ring0_core`, which I declined to do without a separate
  discussion.
- **`gHashTag/trios-a2a`** (which the prompt asked me to inspect for prior
  ring work) is not publicly reachable from this environment — `gh repo
  view` returns `Could not resolve to a Repository`. The architecture here
  follows the conventions already established in this repository by PR #25,
  with ring 4 added at the same indentation level as the others.
