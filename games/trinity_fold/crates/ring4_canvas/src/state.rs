// Owning game state for the canvas UI.
//
// Plain Rust: no Web APIs, no global state. Holds the catalog, current
// board, latest score breakdown, and view options (selected tile,
// benchmark mode, highlighted triangle). All transitions go through
// `AppState::apply` so the wasm shell never mutates internal fields
// directly — keeping the state machine testable in pure Rust.

use ring0_core::{Board, Catalog, ClaimStatus};
use ring1_constraints::{ScoreBreakdown, ScoreWeights, score_board};
use ring2_search::{anneal, hill_climb};

use crate::bridge::BridgeView;
use crate::input::UiEvent;
use crate::recipes::{Recipe, builtin_recipes};

#[derive(Clone, Debug)]
pub struct ViewOptions {
    pub benchmark_mode: bool,
    /// Tile the cursor is currently hovering, if any.
    pub hover_id: Option<String>,
    /// Tile that was last clicked (for inspector panel).
    pub focus_id: Option<String>,
    /// Animation tick — incremented by the wasm host once per requestAnimationFrame.
    /// Pure layout/render does not need it, but visual feedback (pulsing
    /// highlight, triangle sweep) can sample it.
    pub frame: u64,
}

impl Default for ViewOptions {
    fn default() -> Self {
        Self {
            benchmark_mode: false,
            hover_id: None,
            focus_id: None,
            frame: 0,
        }
    }
}

#[derive(Clone, Debug)]
pub struct AppState {
    pub catalog: Catalog,
    pub board: Board,
    pub holdout: Vec<String>,
    pub score: ScoreBreakdown,
    pub bridge: BridgeView,
    pub recipes: Vec<Recipe>,
    pub view: ViewOptions,
    /// Insertion-order history of tile ids that are still on the board.
    /// Empty after ClearBoard / LoadRecipe; only `ToggleTile` adds to it.
    /// Powers single-step undo from the toolbar / `u` key.
    pub pick_history: Vec<String>,
}

impl AppState {
    pub fn new(catalog: Catalog, holdout: Vec<String>) -> Self {
        let board = Board::new();
        let score = score_board(&catalog, &board);
        let bridge = BridgeView::build(&catalog, &board, &score);
        let mut recipes = builtin_recipes();
        for r in recipes.iter_mut() {
            r.rebind_to(&catalog);
        }
        Self {
            catalog,
            board,
            holdout,
            score,
            bridge,
            recipes,
            view: ViewOptions::default(),
            pick_history: Vec::new(),
        }
    }

    /// Rescore from scratch. Called after every mutation that affects the board.
    pub fn rescore(&mut self) {
        // Benchmark mode hides held-out observable values from the scorer
        // by temporarily zeroing them on a *cloned* catalog. The source
        // catalog is never mutated, so toggling the checkbox is reversible.
        if self.view.benchmark_mode && !self.holdout.is_empty() {
            let mut hidden = self.catalog.clone();
            for n in hidden.nodes.iter_mut() {
                if self.holdout.iter().any(|h| h == &n.id) {
                    n.value = None;
                }
            }
            self.score = score_board(&hidden, &self.board);
            self.score
                .notes
                .insert(0, "benchmark mode: holdout values hidden".into());
        } else {
            self.score = score_board(&self.catalog, &self.board);
        }
        // GOLDEN BRIDGE projection is derived state — rebuild whenever score
        // does. Keeps the render path free of branching on benchmark mode.
        self.bridge = BridgeView::build(&self.catalog, &self.board, &self.score);
    }

    /// Replace the board with the tiles named by a recipe. Unknown ids are
    /// ignored (they were already stripped by `Recipe::rebind_to` at startup).
    pub fn load_recipe(&mut self, recipe_id: &str) -> bool {
        let Some(recipe) = self.recipes.iter().find(|r| r.id == recipe_id) else {
            return false;
        };
        let new_board = Board::from_ids(recipe.tile_ids.clone());
        if new_board.is_empty() {
            return false;
        }
        self.board = new_board;
        self.pick_history.clear();
        self.view.focus_id = None;
        self.rescore();
        true
    }

    /// Apply a typed UI event to the state. Returns true if the state
    /// changed in a way that requires re-rendering.
    pub fn apply(&mut self, ev: UiEvent) -> bool {
        match ev {
            UiEvent::ToggleTile(id) => {
                if self.catalog.by_id(&id).is_none() {
                    return false;
                }
                if self.board.contains(&id) {
                    self.board.remove(&id);
                    self.pick_history.retain(|h| h != &id);
                } else {
                    self.board.insert(id.clone());
                    self.pick_history.retain(|h| h != &id);
                    self.pick_history.push(id.clone());
                }
                self.view.focus_id = Some(id);
                self.rescore();
                true
            }
            UiEvent::ClearBoard => {
                if self.board.is_empty() {
                    return false;
                }
                self.board = Board::new();
                self.pick_history.clear();
                self.view.focus_id = None;
                self.rescore();
                true
            }
            UiEvent::UndoLast => {
                let last = loop {
                    match self.pick_history.pop() {
                        Some(id) if self.board.contains(&id) => break Some(id),
                        Some(_) => continue,
                        None => break None,
                    }
                };
                let Some(id) = last else { return false; };
                self.board.remove(&id);
                self.view.focus_id = None;
                self.rescore();
                true
            }
            UiEvent::Focus(id) => {
                if self.view.focus_id.as_deref() == Some(id.as_str()) {
                    false
                } else {
                    self.view.focus_id = Some(id);
                    true
                }
            }
            UiEvent::Hover(id) => {
                if self.view.hover_id == id {
                    false
                } else {
                    self.view.hover_id = id;
                    true
                }
            }
            UiEvent::ToggleBenchmark => {
                self.view.benchmark_mode = !self.view.benchmark_mode;
                self.rescore();
                true
            }
            UiEvent::RunHillClimb => {
                let w = ScoreWeights::default();
                let report = hill_climb(&self.catalog, self.board.clone(), &w, 64);
                self.board = report.best_board;
                self.pick_history.clear();
                self.rescore();
                true
            }
            UiEvent::RunAnneal { seed, iters } => {
                let w = ScoreWeights::default();
                let report = anneal(&self.catalog, self.board.clone(), &w, iters, seed, 1.0, 0.97);
                self.board = report.best_board;
                self.pick_history.clear();
                self.rescore();
                true
            }
            UiEvent::LoadRecipe(id) => self.load_recipe(&id),
            UiEvent::Tick => {
                self.view.frame = self.view.frame.wrapping_add(1);
                // Animations are cosmetic — do not force a full redraw every tick.
                false
            }
        }
    }

    /// Convenience used by the wasm shell to fetch the score's worst claim
    /// for the status badge.
    pub fn worst_claim(&self) -> ClaimStatus {
        self.score.worst_claim
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use ring3_adapters::{benchmark_holdout_ids, default_catalog};

    fn fresh() -> AppState {
        AppState::new(default_catalog(), benchmark_holdout_ids().iter().map(|s| s.to_string()).collect())
    }

    #[test]
    fn empty_board_scores_zero() {
        let s = fresh();
        assert!(s.board.is_empty());
        assert_eq!(s.score.total, 0.0);
    }

    #[test]
    fn toggle_tile_adds_and_removes() {
        let mut s = fresh();
        let id = s.catalog.nodes[0].id.clone();
        assert!(s.apply(UiEvent::ToggleTile(id.clone())));
        assert!(s.board.contains(&id));
        assert!(s.apply(UiEvent::ToggleTile(id.clone())));
        assert!(!s.board.contains(&id));
    }

    #[test]
    fn toggle_unknown_tile_is_noop() {
        let mut s = fresh();
        assert!(!s.apply(UiEvent::ToggleTile("definitely_not_a_real_id".into())));
        assert!(s.board.is_empty());
    }

    #[test]
    fn clear_resets_board() {
        let mut s = fresh();
        let id = s.catalog.nodes[0].id.clone();
        s.apply(UiEvent::ToggleTile(id));
        s.apply(UiEvent::ClearBoard);
        assert!(s.board.is_empty());
        assert_eq!(s.score.total, 0.0);
    }

    #[test]
    fn benchmark_toggle_changes_scoring_path() {
        let mut s = fresh();
        // Place all holdout observables, all of which carry value + predicted.
        for id in s.holdout.clone() {
            s.apply(UiEvent::ToggleTile(id));
        }
        let normal = s.score.observable_fit;
        s.apply(UiEvent::ToggleBenchmark);
        let benchmark = s.score.observable_fit;
        assert!(s.view.benchmark_mode);
        // Hiding the value strictly removes observable-fit contributions.
        assert!(
            benchmark <= normal + 1e-9,
            "benchmark fit ({}) should be <= normal fit ({})",
            benchmark,
            normal
        );
    }

    #[test]
    fn hill_climb_is_deterministic() {
        let mut a = fresh();
        let mut b = fresh();
        a.apply(UiEvent::RunHillClimb);
        b.apply(UiEvent::RunHillClimb);
        assert_eq!(a.board.ids().collect::<Vec<_>>(), b.board.ids().collect::<Vec<_>>());
        assert_eq!(a.score.total, b.score.total);
    }

    #[test]
    fn bridge_view_tracks_board() {
        let mut s = fresh();
        assert_eq!(s.bridge.span_nodes.len(), 0);
        let id = s.catalog.nodes[0].id.clone();
        s.apply(UiEvent::ToggleTile(id));
        assert_eq!(s.bridge.span_nodes.len(), 1);
        s.apply(UiEvent::ClearBoard);
        assert_eq!(s.bridge.span_nodes.len(), 0);
    }

    #[test]
    fn load_recipe_replaces_board() {
        let mut s = fresh();
        // Pre-populate the board with one unrelated tile.
        let other = s.catalog.nodes[0].id.clone();
        s.apply(UiEvent::ToggleTile(other.clone()));
        let recipe_id = s.recipes.first().expect("a builtin recipe").id.clone();
        let changed = s.apply(UiEvent::LoadRecipe(recipe_id.clone()));
        assert!(changed);
        // The pre-existing tile should be gone, replaced by recipe tiles.
        let recipe = s.recipes.iter().find(|r| r.id == recipe_id).unwrap();
        for id in &recipe.tile_ids {
            assert!(s.board.contains(id), "recipe tile `{}` should be on board", id);
        }
    }

    #[test]
    fn load_unknown_recipe_is_noop() {
        let mut s = fresh();
        assert!(!s.apply(UiEvent::LoadRecipe("definitely_not_a_recipe".into())));
        assert!(s.board.is_empty());
    }

    #[test]
    fn undo_last_removes_most_recent_pick() {
        let mut s = fresh();
        let a = s.catalog.nodes[0].id.clone();
        let b = s.catalog.nodes[1].id.clone();
        s.apply(UiEvent::ToggleTile(a.clone()));
        s.apply(UiEvent::ToggleTile(b.clone()));
        assert!(s.board.contains(&a) && s.board.contains(&b));
        assert!(s.apply(UiEvent::UndoLast));
        assert!(s.board.contains(&a), "first pick should survive undo");
        assert!(!s.board.contains(&b), "second pick should be removed by undo");
    }

    #[test]
    fn undo_last_on_empty_board_is_noop() {
        let mut s = fresh();
        assert!(!s.apply(UiEvent::UndoLast));
    }

    #[test]
    fn load_recipe_clears_undo_history() {
        let mut s = fresh();
        let a = s.catalog.nodes[0].id.clone();
        s.apply(UiEvent::ToggleTile(a));
        let recipe_id = s.recipes.first().expect("a builtin recipe").id.clone();
        s.apply(UiEvent::LoadRecipe(recipe_id));
        // After a recipe replaces the board, undo must not resurrect the
        // pre-recipe pick — that would surprise the player.
        assert!(s.pick_history.is_empty());
        assert!(!s.apply(UiEvent::UndoLast));
    }

    #[test]
    fn anneal_with_same_seed_is_deterministic() {
        let mut a = fresh();
        let mut b = fresh();
        a.apply(UiEvent::RunAnneal { seed: 42, iters: 200 });
        b.apply(UiEvent::RunAnneal { seed: 42, iters: 200 });
        assert_eq!(a.board.ids().collect::<Vec<_>>(), b.board.ids().collect::<Vec<_>>());
    }
}
