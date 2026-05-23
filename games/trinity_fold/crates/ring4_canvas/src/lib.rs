// Trinity Fold — ring 4 (canvas UI).
//
// This is the Rust-first UI ring. It depends inward on ring 0..3 and exposes:
//
//   * `state::AppState`   — owning game state (Board + Catalog + last score).
//   * `render::RenderModel` — pure data describing what to draw on a 2D canvas
//                              (rectangles, lines, circles, text). No Web APIs.
//   * `input` — pure hit-testing: maps a click `(x, y)` or key code to a typed
//               `UiEvent`, which is applied to the state by `AppState::apply`.
//   * `wasm` (feature `wasm`, target `wasm32`) — wasm-bindgen entry point that
//               wires an `HtmlCanvasElement` and its `CanvasRenderingContext2d`
//               to the render model, plus mouse/keyboard dispatch.
//
// Dependency rule: ring 4 may depend on rings 0..3. Nothing in rings 0..3 may
// depend on ring 4. Enforced by `crates/app/tests/ring_boundaries.rs`.
//
// Honesty: this ring renders the existing score breakdown; it does not invent
// new scoring rules. A high score on screen is **not** evidence for any
// physics claim. The `worst_claim` badge is always rendered alongside the
// total.

#![forbid(unsafe_code)]

pub mod bridge;
pub mod input;
pub mod recipes;
pub mod render;
pub mod state;

#[cfg(all(target_arch = "wasm32", feature = "wasm"))]
pub mod wasm;

pub use bridge::{BridgeIntegrity, BridgeView, SpanNode, SpanStatus};
pub use input::{InputAction, KeyCode, UiEvent};
pub use recipes::{Recipe, builtin_recipes};
pub use render::{Color, RenderModel, RenderPrimitive, Theme, ViewportSize, layout};
pub use state::{AppState, ViewOptions};

/// Product / concept name surfaced in the UI header. The crate folder
/// remains `trinity_fold` for historical reasons (the workspace was created
/// before the rename); user-facing copy refers to it as **GOLDEN BRIDGE**.
pub const PRODUCT_NAME: &str = "GOLDEN BRIDGE";
pub const PRODUCT_TAGLINE: &str =
    "Build a structural bridge between data and geometry — without collapsing it.";
