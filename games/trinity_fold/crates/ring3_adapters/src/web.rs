// Serialization helpers for the static web UI.
//
// The web UI is a no-build, static HTML+JS page; it consumes whatever JSON
// this module produces. Keeping the projection here means the inner rings
// never grow knowledge of "what the front-end wants to see".

use ring0_core::{Board, Catalog};
use ring1_constraints::ScoreBreakdown;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ScoreView {
    pub board: Vec<String>,
    pub score: ScoreBreakdown,
}

pub fn catalog_to_web_json(catalog: &Catalog) -> Result<String, String> {
    serde_json::to_string_pretty(catalog).map_err(|e| e.to_string())
}

pub fn score_to_web_json(board: &Board, score: &ScoreBreakdown) -> Result<String, String> {
    let view = ScoreView {
        board: board.ids().cloned().collect(),
        score: score.clone(),
    };
    serde_json::to_string_pretty(&view).map_err(|e| e.to_string())
}
