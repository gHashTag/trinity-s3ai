// Pure input handling.
//
// Hit-testing maps cursor coordinates to a typed `UiEvent`. The wasm shell
// converts DOM mouse/keyboard events into `InputAction` values; this module
// resolves them against the current `RenderModel` (which knows tile bounds)
// and emits a `UiEvent` that `AppState::apply` can consume.

use crate::render::{HitRegion, RenderModel};

/// Logical UI events. The state machine only knows about these — never raw
/// pixel coordinates or key codes.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum UiEvent {
    ToggleTile(String),
    Focus(String),
    Hover(Option<String>),
    ClearBoard,
    ToggleBenchmark,
    RunHillClimb,
    RunAnneal { seed: u64, iters: usize },
    /// Replace the board with the tiles named by a GOLDEN BRIDGE recipe.
    LoadRecipe(String),
    /// Remove the most recently-picked tile (single-step undo).
    UndoLast,

    Tick,
}

/// Raw input from the host shell, prior to hit-testing.
#[derive(Clone, Debug)]
pub enum InputAction {
    Click { x: f32, y: f32 },
    Hover { x: f32, y: f32 },
    Key(KeyCode),
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum KeyCode {
    /// `c` — clear board.
    Clear,
    /// `h` — run a hill-climb step.
    HillClimb,
    /// `a` — run a fixed-seed anneal.
    Anneal,
    /// `b` — toggle benchmark mode.
    ToggleBenchmark,
    /// `u` — undo last pick.
    Undo,

    /// `Esc` — drop focus.
    Escape,
}

impl KeyCode {
    /// Map a DOM `KeyboardEvent.key` string to our enum. Anything else is
    /// returned as `None` so the shell can ignore it.
    pub fn from_dom_key(s: &str) -> Option<Self> {
        match s {
            "c" | "C" => Some(KeyCode::Clear),
            "h" | "H" => Some(KeyCode::HillClimb),
            "a" | "A" => Some(KeyCode::Anneal),
            "b" | "B" => Some(KeyCode::ToggleBenchmark),
            "u" | "U" => Some(KeyCode::Undo),

            "Escape" | "Esc" => Some(KeyCode::Escape),
            _ => None,
        }
    }
}

/// Resolve a raw input action into a typed event using the latest render
/// model for hit-testing. Returns `None` if the action does not map to
/// any event (e.g. click on empty background).
pub fn resolve(model: &RenderModel, action: InputAction) -> Option<UiEvent> {
    match action {
        InputAction::Click { x, y } => match hit(model, x, y) {
            Some(HitRegion::Tile(id)) => Some(UiEvent::ToggleTile(id)),
            Some(HitRegion::ButtonClear) => Some(UiEvent::ClearBoard),
            Some(HitRegion::ButtonHillClimb) => Some(UiEvent::RunHillClimb),
            Some(HitRegion::ButtonAnneal) => Some(UiEvent::RunAnneal {
                seed: 42,
                iters: 500,
            }),
            Some(HitRegion::ButtonBenchmark) => Some(UiEvent::ToggleBenchmark),
            Some(HitRegion::ButtonUndo) => Some(UiEvent::UndoLast),
            Some(HitRegion::RecipeChip(id)) => Some(UiEvent::LoadRecipe(id)),

            None => None,
        },
        InputAction::Hover { x, y } => match hit(model, x, y) {
            Some(HitRegion::Tile(id)) => Some(UiEvent::Hover(Some(id))),
            _ => Some(UiEvent::Hover(None)),
        },
        InputAction::Key(k) => Some(match k {
            KeyCode::Clear => UiEvent::ClearBoard,
            KeyCode::HillClimb => UiEvent::RunHillClimb,
            KeyCode::Anneal => UiEvent::RunAnneal {
                seed: 42,
                iters: 500,
            },
            KeyCode::ToggleBenchmark => UiEvent::ToggleBenchmark,
            KeyCode::Undo => UiEvent::UndoLast,

            KeyCode::Escape => UiEvent::Hover(None),
        }),
    }
}

fn hit(model: &RenderModel, x: f32, y: f32) -> Option<HitRegion> {
    // Iterate in reverse so visually-topmost regions win when overlapping
    // (the render model emits backgrounds first, then tiles, then buttons).
    for r in model.hit_regions.iter().rev() {
        if x >= r.x && x <= r.x + r.w && y >= r.y && y <= r.y + r.h {
            return Some(r.region.clone());
        }
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::render::{HitBox, HitRegion};

    fn model_with(regions: Vec<HitBox>) -> RenderModel {
        RenderModel {
            primitives: vec![],
            hit_regions: regions,
            viewport: crate::render::ViewportSize { width: 800.0, height: 600.0 },
        }
    }

    #[test]
    fn click_in_empty_returns_none() {
        let m = model_with(vec![]);
        assert!(resolve(&m, InputAction::Click { x: 1.0, y: 1.0 }).is_none());
    }

    #[test]
    fn click_inside_tile_returns_toggle() {
        let m = model_with(vec![HitBox {
            x: 10.0, y: 10.0, w: 50.0, h: 50.0,
            region: HitRegion::Tile("s_su2".into()),
        }]);
        assert_eq!(
            resolve(&m, InputAction::Click { x: 20.0, y: 20.0 }),
            Some(UiEvent::ToggleTile("s_su2".into()))
        );
    }

    #[test]
    fn click_outside_tile_returns_none() {
        let m = model_with(vec![HitBox {
            x: 10.0, y: 10.0, w: 50.0, h: 50.0,
            region: HitRegion::Tile("s_su2".into()),
        }]);
        assert!(resolve(&m, InputAction::Click { x: 100.0, y: 100.0 }).is_none());
    }

    #[test]
    fn topmost_region_wins() {
        let m = model_with(vec![
            HitBox { x: 0.0, y: 0.0, w: 100.0, h: 100.0, region: HitRegion::Tile("under".into()) },
            HitBox { x: 0.0, y: 0.0, w: 100.0, h: 100.0, region: HitRegion::Tile("over".into()) },
        ]);
        assert_eq!(
            resolve(&m, InputAction::Click { x: 50.0, y: 50.0 }),
            Some(UiEvent::ToggleTile("over".into()))
        );
    }

    #[test]
    fn key_clear_maps_to_clear_event() {
        let m = model_with(vec![]);
        assert_eq!(
            resolve(&m, InputAction::Key(KeyCode::Clear)),
            Some(UiEvent::ClearBoard)
        );
    }

    #[test]
    fn recipe_chip_click_resolves_to_load_recipe() {
        let m = model_with(vec![HitBox {
            x: 0.0, y: 0.0, w: 80.0, h: 26.0,
            region: HitRegion::RecipeChip("sm_core".into()),
        }]);
        assert_eq!(
            resolve(&m, InputAction::Click { x: 10.0, y: 10.0 }),
            Some(UiEvent::LoadRecipe("sm_core".into()))
        );
    }

    #[test]
    fn dom_key_parsing() {
        assert_eq!(KeyCode::from_dom_key("c"), Some(KeyCode::Clear));
        assert_eq!(KeyCode::from_dom_key("u"), Some(KeyCode::Undo));
        assert_eq!(KeyCode::from_dom_key("Escape"), Some(KeyCode::Escape));
        assert_eq!(KeyCode::from_dom_key("F12"), None);
    }

    #[test]
    fn undo_button_click_resolves_to_undo_last() {
        let m = model_with(vec![HitBox {
            x: 0.0, y: 0.0, w: 80.0, h: 40.0,
            region: HitRegion::ButtonUndo,
        }]);
        assert_eq!(
            resolve(&m, InputAction::Click { x: 10.0, y: 10.0 }),
            Some(UiEvent::UndoLast)
        );
    }

    #[test]
    fn undo_key_maps_to_undo_last() {
        let m = model_with(vec![]);
        assert_eq!(
            resolve(&m, InputAction::Key(KeyCode::Undo)),
            Some(UiEvent::UndoLast)
        );
    }

}
