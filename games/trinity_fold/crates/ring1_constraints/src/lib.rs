// Trinity Fold — ring 1 (constraints / scoring).
//
// This crate scores a `Board` against a fixed `Catalog` along eight axes:
// consistency, dimensional sanity, observable fit, proof-debt penalty,
// falsification penalty, simplicity, symmetry coherence, reproducibility.
//
// Dependency rule: ring 1 depends only on ring 0. It performs no I/O, no
// randomness, no UI. Every function is pure: same inputs => same outputs.
//
// Honesty contract: a high `total` is NOT evidence the underlying physics is
// "true" — it only means the board passes more checks than alternatives in
// the current catalog. The `worst_claim` field surfaces the strongest claim
// status across active contributions so the UI can label results honestly.

#![forbid(unsafe_code)]

pub mod scoring;

pub use scoring::{
    ScoreBreakdown, ScoreWeights, score_board, score_board_with, tower_counts,
};
