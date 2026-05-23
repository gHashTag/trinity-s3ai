// Trinity Fold — ring 2 (search / AI).
//
// Deterministic local search over board configurations. Two strategies:
//   * `hill_climb` — greedy single-toggle improvement; fully reproducible.
//   * `anneal`     — simulated annealing with a self-contained LCG so the
//                    same `seed` yields the same trajectory across runs.
//
// Dependency rule: ring 2 depends on ring 0 (types) and ring 1 (scoring).
// It does NOT depend on adapters (ring 3) — no I/O, no time, no UI. The
// only "randomness" is the supplied seed, kept inside this crate.

#![forbid(unsafe_code)]

pub mod rng;
pub mod search;

pub use search::{Move, SearchReport, anneal, hill_climb};
