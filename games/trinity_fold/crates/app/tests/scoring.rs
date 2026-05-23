// Integration tests at the app boundary. These exercise the full ring stack
// (ring0 types via ring3 fixtures, ring1 scoring, ring2 search) and verify
// that the public API the CLI relies on still behaves correctly.

use ring0_core::{Board, ClaimStatus};
use ring1_constraints::{ScoreWeights, score_board, score_board_with};
use ring2_search::{anneal, hill_climb};
use ring3_adapters::default_catalog;

#[test]
fn empty_board_scores_zero_total_and_keeps_worst_claim_pristine() {
    let cat = default_catalog();
    let b = Board::new();
    let r = score_board(&cat, &b);
    assert_eq!(r.total, 0.0);
    assert_eq!(r.worst_claim, ClaimStatus::Verified);
}

#[test]
fn unknown_ids_are_ignored_and_do_not_panic() {
    let cat = default_catalog();
    let b = Board::from_ids(["does_not_exist", "also_missing"]);
    let r = score_board(&cat, &b);
    assert!(r.total <= 0.5);
}

#[test]
fn falsified_node_caps_total_negative() {
    let cat = default_catalog();
    let b = Board::from_ids(["s_h4", "g_600cell", "cn_ngt3_chirality"]);
    let r = score_board(&cat, &b);
    assert!(
        r.total <= -0.25 + 1e-9,
        "falsification floor not enforced: total={}",
        r.total
    );
    assert_eq!(r.worst_claim, ClaimStatus::HighRiskOrFalsified);
}

#[test]
fn unmet_requires_lowers_consistency() {
    let cat = default_catalog();
    let b = Board::from_ids(["f_higgs"]);
    let r = score_board(&cat, &b);
    assert!(r.consistency < 0.5, "consistency too high: {}", r.consistency);
}

#[test]
fn full_ew_triangle_satisfies_consistency_and_triangle() {
    let cat = default_catalog();
    let b = Board::from_ids([
        "s_su2",
        "s_u1",
        "s_su3",
        "f_higgs",
        "f_fermions",
        "cn_anomaly",
        "o_higgs_mass",
    ]);
    let r = score_board(&cat, &b);
    assert!(r.consistency >= 0.99);
    assert!(r.symmetry_coherence > 0.0);
}

#[test]
fn citation_lift_reproducibility() {
    let cat = default_catalog();
    let b = Board::from_ids(["c_c", "c_hbar", "s_lorentz", "cn_unitarity"]);
    let r = score_board(&cat, &b);
    assert!(r.reproducibility >= 0.99, "reproducibility={}", r.reproducibility);
}

#[test]
fn hill_climb_is_deterministic() {
    let cat = default_catalog();
    let w = ScoreWeights::default();
    let a = hill_climb(&cat, Board::new(), &w, 200);
    let b = hill_climb(&cat, Board::new(), &w, 200);
    assert_eq!(a.best_board.selected, b.best_board.selected);
    assert!((a.best_score.total - b.best_score.total).abs() < 1e-12);
}

#[test]
fn anneal_is_deterministic_for_fixed_seed() {
    let cat = default_catalog();
    let w = ScoreWeights::default();
    let a = anneal(&cat, Board::new(), &w, 500, 42, 0.25, 0.999);
    let b = anneal(&cat, Board::new(), &w, 500, 42, 0.25, 0.999);
    assert_eq!(a.best_board.selected, b.best_board.selected);
}

#[test]
fn hill_climb_never_lands_on_falsified_only_board() {
    let cat = default_catalog();
    let w = ScoreWeights::default();
    let report = hill_climb(&cat, Board::new(), &w, 500);
    let no_go = report.best_board.contains("cn_ngt3_chirality")
        || report.best_board.contains("cn_ngt1_cosmology");
    assert!(
        !no_go || report.best_score.total <= 0.0,
        "search picked a known-falsified board with positive score"
    );
}

#[test]
fn observable_fit_rewards_close_predictions() {
    let mut cat = default_catalog();
    for n in cat.nodes.iter_mut() {
        if n.id == "o_higgs_mass" {
            n.predicted = Some(125.21);
        }
    }
    let b = Board::from_ids(["s_su2", "s_u1", "f_higgs", "o_higgs_mass"]);
    let r = score_board_with(&cat, &b, &ScoreWeights::default());
    assert!(r.observable_fit > 0.0, "observable_fit was zero");
}
