// Deterministic local search over board configurations.
//
// Two strategies are provided:
//   * `hill_climb`  — greedy improvement; useful for tests and reproducible runs.
//   * `anneal`      — simulated annealing with a pure LCG random source so
//                     the same `seed` yields the same trajectory.
//
// No external RNG crate is used to keep the dependency surface small and
// avoid pulling crates that would change the audit story.

use crate::board::{Board, Catalog};
use crate::scoring::{ScoreBreakdown, ScoreWeights, score_board_with};

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
        for (i, node) in catalog.nodes.iter().enumerate() {
            let _ = i;
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

// Tiny LCG. Not cryptographic; we only need reproducible exploration.
struct Lcg {
    state: u64,
}

impl Lcg {
    fn new(seed: u64) -> Self {
        Self {
            state: seed.wrapping_add(0x9E3779B97F4A7C15),
        }
    }
    fn next_u64(&mut self) -> u64 {
        self.state = self
            .state
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        self.state
    }
    fn next_f64(&mut self) -> f64 {
        // 53-bit mantissa.
        (self.next_u64() >> 11) as f64 / (1u64 << 53) as f64
    }
    fn next_range(&mut self, n: u64) -> u64 {
        if n == 0 {
            return 0;
        }
        self.next_u64() % n
    }
}
