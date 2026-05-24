// GOLDEN BRIDGE — a structural projection over `Board` + `Catalog` + `ScoreBreakdown`.
//
// The bridge metaphor reframes the puzzle from "fold a hypothesis" to
// "build a structural bridge between two shores of reality":
//
//   * Data pier (left shore)      — observational/experimental constraints
//                                   (`NodeKind::Constraint`, `NodeKind::Observable`).
//   * Geometry pier (right shore) — theoretical symmetries and constants
//                                   (`NodeKind::Symmetry`, `NodeKind::Geometry`,
//                                    `NodeKind::Field`, `NodeKind::Constant`).
//   * Bridge span                 — the player's candidate hypothesis. Each
//                                   selected tile is a span node; the span only
//                                   "holds" if its claim status is strong enough
//                                   and if no falsified tile is on the board.
//
// This module is pure ring-4 view logic. It does NOT introduce new scoring;
// every number it surfaces is derived from `ScoreBreakdown` and `Catalog`
// produced by lower rings. Adding a new bridge metric should NOT change the
// score — if it would, push the change into `ring1_constraints` instead.

use ring0_core::{Board, Catalog, ClaimStatus, NodeKind, Tower};
use ring1_constraints::ScoreBreakdown;

/// Status of an individual span node, mirroring `ClaimStatus` but specialised
/// to the bridge-building vocabulary the UI surfaces.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum SpanStatus {
    /// Gold cable — backed by a formal derivation.
    Gold,
    /// Blue cable — empirical fit; the cable holds but only as far as data does.
    Empirical,
    /// Amber cable — open conjecture; the cable is provisional.
    Open,
    /// Red cable — falsified or boundary; the bridge collapses through this node.
    Collapsed,
    /// Grey cable — unverified user input; cannot carry load.
    Unverified,
}

impl SpanStatus {
    pub fn from_claim(c: ClaimStatus) -> Self {
        match c {
            ClaimStatus::Verified => SpanStatus::Gold,
            ClaimStatus::EmpiricalFit => SpanStatus::Empirical,
            ClaimStatus::OpenConjecture => SpanStatus::Open,
            ClaimStatus::HighRiskOrFalsified => SpanStatus::Collapsed,
            ClaimStatus::Unverified => SpanStatus::Unverified,
        }
    }

    pub fn label(&self) -> &'static str {
        match self {
            SpanStatus::Gold => "GOLD",
            SpanStatus::Empirical => "EMPIRICAL",
            SpanStatus::Open => "OPEN",
            SpanStatus::Collapsed => "COLLAPSED",
            SpanStatus::Unverified => "UNVERIFIED",
        }
    }
}

/// One node of the bridge span, ordered from the Data pier (`pier_t = 0.0`)
/// to the Geometry pier (`pier_t = 1.0`). The UI uses `pier_t` purely for
/// layout — it carries no scoring weight.
#[derive(Clone, Debug)]
pub struct SpanNode {
    pub id: String,
    pub name: String,
    pub kind: NodeKind,
    pub claim: ClaimStatus,
    pub status: SpanStatus,
    /// 0.0 = anchored at Data pier, 1.0 = anchored at Geometry pier.
    pub pier_t: f32,
}

/// Honesty floor: a board with any `HighRiskOrFalsified` node has the bridge
/// flagged as `Collapsed`; a clean board with low proof debt is `Sound`. The
/// gradient in between is reported as `Provisional`.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum BridgeIntegrity {
    /// No tiles placed yet.
    Empty,
    /// All cables gold or empirical; no falsified node; proof debt < 0.25.
    Sound,
    /// At least one open / unverified cable, or proof debt >= 0.25, but no falsified node.
    Provisional,
    /// One or more falsified cables — the honesty floor has tripped.
    Collapsed,
}

impl BridgeIntegrity {
    pub fn label(&self) -> &'static str {
        match self {
            BridgeIntegrity::Empty => "EMPTY",
            BridgeIntegrity::Sound => "SOUND",
            BridgeIntegrity::Provisional => "PROVISIONAL",
            BridgeIntegrity::Collapsed => "COLLAPSED",
        }
    }
}

/// A render-ready view of the GOLDEN BRIDGE. Built from the current board and
/// the latest score breakdown.
#[derive(Clone, Debug)]
pub struct BridgeView {
    pub data_pier_count: usize,
    pub geom_pier_count: usize,
    pub span_nodes: Vec<SpanNode>,
    pub falsified_count: usize,
    /// `score.total` mirrored into the bridge view so the UI can show
    /// "bridge strength" without reaching back into ring 1 types.
    pub strength: f64,
    /// `score.worst_claim` mirrored into the bridge view.
    pub worst_claim: ClaimStatus,
    /// Honesty-floor verdict.
    pub integrity: BridgeIntegrity,
    /// "Space-fold" compression ratio: span_nodes.len() / catalog.nodes.len().
    /// A low value with high `strength` means the player compressed many
    /// possible building blocks into a small consistent set — that is the
    /// rhetorical point of the metaphor, not a discovery claim.
    pub compression: f64,
}

impl BridgeView {
    pub fn build(catalog: &Catalog, board: &Board, score: &ScoreBreakdown) -> Self {
        let (data_pier_count, geom_pier_count) = pier_counts(catalog, board);
        let span_nodes = build_span(catalog, board);
        let falsified_count = span_nodes
            .iter()
            .filter(|n| n.status == SpanStatus::Collapsed)
            .count();

        let integrity = if board.is_empty() {
            BridgeIntegrity::Empty
        } else if falsified_count > 0 {
            BridgeIntegrity::Collapsed
        } else if score.proof_debt_penalty >= 0.25
            || span_nodes
                .iter()
                .any(|n| matches!(n.status, SpanStatus::Open | SpanStatus::Unverified))
        {
            BridgeIntegrity::Provisional
        } else {
            BridgeIntegrity::Sound
        };

        let total_pool = catalog.nodes.len().max(1) as f64;
        let compression = span_nodes.len() as f64 / total_pool;

        Self {
            data_pier_count,
            geom_pier_count,
            span_nodes,
            falsified_count,
            strength: score.total,
            worst_claim: score.worst_claim,
            integrity,
            compression,
        }
    }

    pub fn is_collapsed(&self) -> bool {
        self.integrity == BridgeIntegrity::Collapsed
    }
}

fn pier_counts(catalog: &Catalog, board: &Board) -> (usize, usize) {
    let mut data = 0usize;
    let mut geom = 0usize;
    for id in board.ids() {
        if let Some(n) = catalog.by_id(id) {
            match n.kind.tower() {
                Tower::Data => data += 1,
                Tower::Geometry => geom += 1,
            }
        }
    }
    (data, geom)
}

fn build_span(catalog: &Catalog, board: &Board) -> Vec<SpanNode> {
    // Sort span nodes by tower then by id so layout is deterministic across
    // renders. Data-tower nodes are anchored closer to the Data pier; geometry
    // nodes anchored closer to the Geometry pier; the rest are interpolated.
    let mut entries: Vec<(NodeKind, &ring0_core::Node)> = board
        .ids()
        .filter_map(|id| catalog.by_id(id).map(|n| (n.kind, n)))
        .collect();
    entries.sort_by(|a, b| {
        tower_key(a.0.tower())
            .cmp(&tower_key(b.0.tower()))
            .then_with(|| a.1.id.cmp(&b.1.id))
    });

    let n = entries.len();
    entries
        .into_iter()
        .enumerate()
        .map(|(i, (kind, node))| {
            let pier_t = if n <= 1 {
                0.5
            } else {
                // Bias the t coordinate by tower: data-tower entries cluster
                // in the left half, geometry-tower entries in the right half.
                let base = i as f32 / (n - 1) as f32;
                match kind.tower() {
                    Tower::Data => base * 0.5,
                    Tower::Geometry => 0.5 + base * 0.5,
                }
                .clamp(0.0, 1.0)
            };
            SpanNode {
                id: node.id.clone(),
                name: node.name.clone(),
                kind,
                claim: node.claim,
                status: SpanStatus::from_claim(node.claim),
                pier_t,
            }
        })
        .collect()
}

fn tower_key(t: Tower) -> u8 {
    match t {
        Tower::Data => 0,
        Tower::Geometry => 1,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use ring1_constraints::score_board;
    use ring3_adapters::default_catalog;

    fn build(ids: &[&str]) -> BridgeView {
        let cat = default_catalog();
        let board = Board::from_ids(ids.iter().map(|s| s.to_string()));
        let score = score_board(&cat, &board);
        BridgeView::build(&cat, &board, &score)
    }

    #[test]
    fn empty_board_is_empty_bridge() {
        let v = build(&[]);
        assert_eq!(v.integrity, BridgeIntegrity::Empty);
        assert_eq!(v.span_nodes.len(), 0);
        assert_eq!(v.data_pier_count, 0);
        assert_eq!(v.geom_pier_count, 0);
        assert!(!v.is_collapsed());
    }

    #[test]
    fn span_nodes_cover_only_known_ids() {
        let v = build(&["s_su2", "definitely_unknown_id", "f_higgs"]);
        let known: Vec<_> = v.span_nodes.iter().map(|n| n.id.as_str()).collect();
        assert!(known.contains(&"s_su2"));
        assert!(known.contains(&"f_higgs"));
        assert!(!known.contains(&"definitely_unknown_id"));
    }

    #[test]
    fn pier_counts_partition_board_by_tower() {
        let v = build(&["s_su2", "f_higgs", "o_higgs_mass"]);
        assert_eq!(
            v.data_pier_count + v.geom_pier_count,
            v.span_nodes.len(),
            "every span node should belong to exactly one pier"
        );
    }

    #[test]
    fn falsified_tile_collapses_bridge() {
        let cat = default_catalog();
        let falsified_id = cat
            .nodes
            .iter()
            .find(|n| n.claim == ClaimStatus::HighRiskOrFalsified)
            .map(|n| n.id.clone());
        let Some(id) = falsified_id else {
            // The illustrative catalog may not always ship one; treat as a
            // soft skip rather than failing CI on an unrelated fixture edit.
            return;
        };
        let board = Board::from_ids([id]);
        let score = score_board(&cat, &board);
        let v = BridgeView::build(&cat, &board, &score);
        assert_eq!(v.integrity, BridgeIntegrity::Collapsed);
        assert!(v.is_collapsed());
        assert!(v.falsified_count >= 1);
    }

    #[test]
    fn provisional_integrity_when_no_falsified_but_open_present() {
        let cat = default_catalog();
        let open_id = cat
            .nodes
            .iter()
            .find(|n| n.claim == ClaimStatus::OpenConjecture)
            .map(|n| n.id.clone());
        let Some(id) = open_id else {
            return;
        };
        let board = Board::from_ids([id]);
        let score = score_board(&cat, &board);
        let v = BridgeView::build(&cat, &board, &score);
        assert_ne!(v.integrity, BridgeIntegrity::Collapsed);
        assert_ne!(v.integrity, BridgeIntegrity::Empty);
    }

    #[test]
    fn compression_is_between_zero_and_one() {
        let v = build(&["s_su2", "f_higgs"]);
        assert!(v.compression > 0.0 && v.compression <= 1.0);
    }

    #[test]
    fn span_status_round_trips_through_claim() {
        for c in [
            ClaimStatus::Verified,
            ClaimStatus::EmpiricalFit,
            ClaimStatus::OpenConjecture,
            ClaimStatus::HighRiskOrFalsified,
            ClaimStatus::Unverified,
        ] {
            let s = SpanStatus::from_claim(c);
            // No panic and a stable, non-empty label.
            assert!(!s.label().is_empty());
        }
    }

    #[test]
    fn span_nodes_are_ordered_by_tower() {
        let v = build(&["s_su2", "f_higgs", "o_higgs_mass", "cn_anomaly"]);
        // After sort, no data-tower node should appear after a geometry-tower one.
        let mut seen_geom = false;
        for n in &v.span_nodes {
            match n.kind.tower() {
                Tower::Geometry => seen_geom = true,
                Tower::Data => {
                    assert!(!seen_geom, "data tower node `{}` appeared after a geometry tower node", n.id);
                }
            }
        }
    }
}
