use crate::rng::Lcg;
use ring0_core::{Board, Catalog};
use ring1_constraints::{ScoreBreakdown, ScoreWeights, score_board_with};

/// A single mutation proposal. Kept here so search strategies can return
/// trajectories without depending on adapter-layer formatting.
#[derive(Clone, Copy, Debug)]
pub enum Move {
    Add(usize),
    Remove(usize),
    Swap(usize, usize),
}

#[derive(Clone, Debug)]
pub struct SearchReport {
    pub best_board: Board,
    pub best_score: ScoreBreakdown,
    pub iterations: usize,
    pub accepted_moves: usize,
}

/// Deterministic hill climbing. Tries each possible single-node toggle, keeps
/// the first one that improves the total score. Halts when no toggle helps.
pub fn hill_climb(
    catalog: &Catalog,
    start: Board,
    weights: &ScoreWeights,
    max_iters: usize,
) -> SearchReport {
    let mut current = start;
    let mut best_score = score_board_with(catalog, &current, weights);
    let mut iterations = 0usize;
    let mut accepted = 0usize;

    'outer: while iterations < max_iters {
        iterations += 1;
        for node in catalog.nodes.iter() {
            let mut candidate = current.clone();
            if candidate.contains(&node.id) {
                candidate.remove(&node.id);
            } else {
                candidate.insert(node.id.clone());
            }
            let s = score_board_with(catalog, &candidate, weights);
            if s.total > best_score.total + 1e-12 {
                current = candidate;
                best_score = s;
                accepted += 1;
                continue 'outer;
            }
        }
        break;
    }

    SearchReport {
        best_board: current,
        best_score,
        iterations,
        accepted_moves: accepted,
    }
}

/// Simulated annealing with a self-contained LCG. Deterministic given a
/// fixed `seed`. Temperature schedule is geometric.
pub fn anneal(
    catalog: &Catalog,
    start: Board,
    weights: &ScoreWeights,
    iters: usize,
    seed: u64,
    t0: f64,
    cooling: f64,
) -> SearchReport {
    let mut rng = Lcg::new(seed);
    let mut current = start;
    let mut current_score = score_board_with(catalog, &current, weights);
    let mut best_board = current.clone();
    let mut best_score = current_score.clone();
    let mut accepted = 0usize;

    if catalog.nodes.is_empty() {
        return SearchReport {
            best_board,
            best_score,
            iterations: 0,
            accepted_moves: 0,
        };
    }

    let mut t = t0;
    for _ in 0..iters {
        let idx = rng.next_range(catalog.nodes.len() as u64) as usize;
        let node_id = catalog.nodes[idx].id.clone();
        let mut candidate = current.clone();
        if candidate.contains(&node_id) {
            candidate.remove(&node_id);
        } else {
            candidate.insert(node_id);
        }
        let s = score_board_with(catalog, &candidate, weights);
        let delta = s.total - current_score.total;
        let accept = if delta > 0.0 {
            true
        } else {
            let r = rng.next_f64();
            r < (delta / t.max(1e-9)).exp()
        };
        if accept {
            current = candidate;
            current_score = s;
            accepted += 1;
            if current_score.total > best_score.total {
                best_board = current.clone();
                best_score = current_score.clone();
            }
        }
        t *= cooling;
    }

    SearchReport {
        best_board,
        best_score,
        iterations: iters,
        accepted_moves: accepted,
    }
}
