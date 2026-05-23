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

use crate::input::UiEvent;

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
    pub view: ViewOptions,
}

impl AppState {
    pub fn new(catalog: Catalog, holdout: Vec<String>) -> Self {
        let board = Board::new();
        let score = score_board(&catalog, &board);
        Self {
            catalog,
            board,
            holdout,
            score,
            view: ViewOptions::default(),
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
                } else {
                    self.board.insert(id.clone());
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
                self.rescore();
                true
            }
            UiEvent::RunAnneal { seed, iters } => {
                let w = ScoreWeights::default();
                let report = anneal(&self.catalog, self.board.clone(), &w, iters, seed, 1.0, 0.97);
                self.board = report.best_board;
                self.rescore();
                true
            }
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
    fn anneal_with_same_seed_is_deterministic() {
        let mut a = fresh();
        let mut b = fresh();
        a.apply(UiEvent::RunAnneal { seed: 42, iters: 200 });
        b.apply(UiEvent::RunAnneal { seed: 42, iters: 200 });
        assert_eq!(a.board.ids().collect::<Vec<_>>(), b.board.ids().collect::<Vec<_>>());
    }
}
