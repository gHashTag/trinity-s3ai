use crate::board::{Board, Catalog};
use crate::claim::ClaimStatus;
use crate::node::{NodeKind, Tower};
use serde::{Deserialize, Serialize};

/// Eight scalar components combined into one composite score.
///
/// Each component is normalized to roughly [0, 1] before combination so that
/// the final number is interpretable. Weights are tunable in `ScoreWeights`.
///
/// IMPORTANT: a high `total` does NOT mean the candidate is "true". It means
/// the board passes more of the consistency checks than alternatives. The
/// `worst_claim` field surfaces the strongest claim status across active
/// contributions, so the UI can label the result honestly.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct ScoreBreakdown {
    pub consistency: f64,
    pub dimensional_sanity: f64,
    pub observable_fit: f64,
    pub proof_debt_penalty: f64,
    pub falsification_penalty: f64,
    pub simplicity: f64,
    pub symmetry_coherence: f64,
    pub reproducibility: f64,
    pub total: f64,
    pub worst_claim: ClaimStatus,
    pub notes: Vec<String>,
}

#[derive(Clone, Debug)]
pub struct ScoreWeights {
    pub consistency: f64,
    pub dimensional_sanity: f64,
    pub observable_fit: f64,
    pub proof_debt_penalty: f64,
    pub falsification_penalty: f64,
    pub simplicity: f64,
    pub symmetry_coherence: f64,
    pub reproducibility: f64,
}

impl Default for ScoreWeights {
    fn default() -> Self {
        Self {
            consistency: 1.0,
            dimensional_sanity: 1.0,
            observable_fit: 1.5,
            proof_debt_penalty: 1.0,
            falsification_penalty: 4.0,
            simplicity: 0.5,
            symmetry_coherence: 0.75,
            reproducibility: 0.5,
        }
    }
}

pub fn score_board(catalog: &Catalog, board: &Board) -> ScoreBreakdown {
    score_board_with(catalog, board, &ScoreWeights::default())
}

pub fn score_board_with(
    catalog: &Catalog,
    board: &Board,
    w: &ScoreWeights,
) -> ScoreBreakdown {
    let mut br = ScoreBreakdown::default();
    br.worst_claim = ClaimStatus::Verified;

    // Empty board -> zero score, but not negative. Avoids spurious wins.
    if board.is_empty() {
        br.notes.push("empty board".into());
        return br;
    }

    let n = board.len() as f64;

    // 1. Consistency: every `requires` satisfied, no `incompatible_with` pair.
    let (cons_ok, cons_bad) = consistency_counts(catalog, board);
    let cons_total = cons_ok + cons_bad;
    br.consistency = if cons_total == 0 {
        1.0
    } else {
        cons_ok as f64 / cons_total as f64
    };
    if cons_bad > 0 {
        br.notes.push(format!(
            "{} unmet `requires`/`incompatible_with` checks",
            cons_bad
        ));
    }

    // 2. Dimensional sanity: the running dimension signature of all selected
    // nodes is empty (each base dimension sums to zero).
    let sig = catalog.dimensional_signature(board);
    br.dimensional_sanity = if sig.is_empty() {
        1.0
    } else {
        // Soft penalty: 1 / (1 + total absolute dimensional imbalance).
        let imbalance: i32 = sig.values().map(|v| v.abs()).sum();
        1.0 / (1.0 + imbalance as f64)
    };
    if !sig.is_empty() {
        br.notes
            .push(format!("dimensional imbalance: {:?}", sig));
    }

    // 3. Observable fit: for each Observable node with both `value` and
    // `predicted`, compute |pred - obs| / sigma and shrink to [0, 1].
    let mut fit_acc = 0.0;
    let mut fit_n = 0usize;
    for id in board.ids() {
        let Some(node) = catalog.by_id(id) else {
            continue;
        };
        if node.kind != NodeKind::Observable {
            continue;
        }
        let (Some(obs), Some(pred)) = (node.value, node.predicted) else {
            continue;
        };
        let sigma = node
            .uncertainty
            .filter(|s| *s > 0.0)
            .unwrap_or((obs.abs() * 1e-3).max(1e-12));
        let z = ((pred - obs) / sigma).abs();
        // Smooth: 1 / (1 + z^2). z=1 sigma -> 0.5; z=3 -> 0.1.
        let contrib = 1.0 / (1.0 + z * z);
        // Weight by the observable's own claim status — an unverified node
        // can't claim a perfect fit.
        fit_acc += contrib * node.claim.positive_weight();
        fit_n += 1;
        update_worst(&mut br.worst_claim, node.claim);
    }
    br.observable_fit = if fit_n == 0 { 0.0 } else { fit_acc / fit_n as f64 };

    // 4. Proof debt: count nodes tagged "proof_debt" or with claim
    // OpenConjecture / Unverified. Returned as a penalty in [0, 1].
    let mut debt = 0.0;
    for id in board.ids() {
        let Some(node) = catalog.by_id(id) else {
            continue;
        };
        let claim_cost = match node.claim {
            ClaimStatus::Verified => 0.0,
            ClaimStatus::EmpiricalFit => 0.2,
            ClaimStatus::OpenConjecture => 0.5,
            ClaimStatus::Unverified => 0.7,
            ClaimStatus::HighRiskOrFalsified => 0.0, // handled below
        };
        let tag_cost = if node.has_tag("proof_debt") { 0.3 } else { 0.0 };
        debt += claim_cost + tag_cost;
        update_worst(&mut br.worst_claim, node.claim);
    }
    br.proof_debt_penalty = (debt / n).min(1.0);

    // 5. Falsification: any node with HighRiskOrFalsified or tag
    // "falsified" / "no_go" triggers a heavy penalty. This is intentionally
    // the harshest term — boards must avoid known-broken structures.
    let mut falsified = 0usize;
    for id in board.ids() {
        let Some(node) = catalog.by_id(id) else {
            continue;
        };
        if node.claim == ClaimStatus::HighRiskOrFalsified
            || node.has_tag("falsified")
            || node.has_tag("no_go")
        {
            falsified += 1;
            update_worst(&mut br.worst_claim, ClaimStatus::HighRiskOrFalsified);
        }
    }
    br.falsification_penalty = (falsified as f64 / n).min(1.0);

    // 6. Simplicity / compression: shorter boards score higher, but only
    // after a small "useful complexity" floor — too few tiles can't cover
    // enough constraints. Peak around 8-12 tiles.
    let target = 10.0_f64;
    let dev = (n - target).abs();
    br.simplicity = (1.0 / (1.0 + 0.05 * dev * dev)).clamp(0.0, 1.0);

    // 7. Symmetry coherence: did the player place at least one Symmetry and
    // one Geometry tile, and do they share a triangle with a Constraint?
    let has_sym = board
        .ids()
        .any(|id| catalog.by_id(id).map_or(false, |n| n.kind == NodeKind::Symmetry));
    let has_geo = board
        .ids()
        .any(|id| catalog.by_id(id).map_or(false, |n| n.kind == NodeKind::Geometry));
    let triangle_hits = catalog
        .triangles
        .iter()
        .filter(|tri| tri.iter().all(|id| board.contains(id)))
        .count();
    let triangle_score = if catalog.triangles.is_empty() {
        0.5
    } else {
        (triangle_hits as f64 / catalog.triangles.len() as f64).clamp(0.0, 1.0)
    };
    br.symmetry_coherence = match (has_sym, has_geo) {
        (true, true) => 0.5 + 0.5 * triangle_score,
        (true, false) | (false, true) => 0.25 * triangle_score,
        (false, false) => 0.0,
    };

    // 8. Reproducibility: fraction of nodes that carry a citation. Reflects
    // CASP-style traceability — every score component must be auditable.
    let cited = board
        .ids()
        .filter(|id| {
            catalog
                .by_id(id)
                .map_or(false, |n| n.citation.as_ref().is_some_and(|c| !c.is_empty()))
        })
        .count();
    br.reproducibility = cited as f64 / n;

    // Compose. Positive terms add; penalty terms subtract.
    let raw = w.consistency * br.consistency
        + w.dimensional_sanity * br.dimensional_sanity
        + w.observable_fit * br.observable_fit
        + w.simplicity * br.simplicity
        + w.symmetry_coherence * br.symmetry_coherence
        + w.reproducibility * br.reproducibility
        - w.proof_debt_penalty * br.proof_debt_penalty
        - w.falsification_penalty * br.falsification_penalty;

    let max_positive = w.consistency
        + w.dimensional_sanity
        + w.observable_fit
        + w.simplicity
        + w.symmetry_coherence
        + w.reproducibility;
    br.total = if max_positive > 0.0 {
        raw / max_positive
    } else {
        0.0
    };

    // Honesty floor: if any node on the board is falsified, the total is
    // capped so the candidate cannot ever read as "good".
    if falsified > 0 {
        br.total = br.total.min(-0.25);
        br.notes
            .push(format!("{} falsified node(s) on board — total capped", falsified));
    }

    br
}

fn consistency_counts(catalog: &Catalog, board: &Board) -> (usize, usize) {
    let mut ok = 0usize;
    let mut bad = 0usize;
    for id in board.ids() {
        let Some(node) = catalog.by_id(id) else {
            continue;
        };
        for req in &node.requires {
            if board.contains(req) {
                ok += 1;
            } else {
                bad += 1;
            }
        }
        for inc in &node.incompatible_with {
            if board.contains(inc) {
                bad += 1;
            }
        }
    }
    (ok, bad)
}

fn update_worst(worst: &mut ClaimStatus, c: ClaimStatus) {
    if c > *worst {
        *worst = c;
    }
}

/// Tower coverage helper used by the UI: how many tiles sit in each tower.
/// Exposed here so the CLI report can include it without duplicating logic.
pub fn tower_counts(catalog: &Catalog, board: &Board) -> (usize, usize) {
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
