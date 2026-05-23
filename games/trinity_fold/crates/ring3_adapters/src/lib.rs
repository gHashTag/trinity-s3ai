// Trinity Fold — ring 3 (adapters / interfaces).
//
// This crate adapts the inner rings to the outside world:
//   * `io`       — JSON load/save for the catalog.
//   * `fixtures` — the built-in illustrative catalog and CASP-style holdout.
//   * `web`      — serializes catalog + score reports for the static web UI.
//
// Dependency rule: ring 3 depends inward on ring 0..2. It is the FIRST ring
// allowed to touch the filesystem or perform serialization. Application
// orchestration (CLI parsing, scenario loading, benchmark runs) lives one
// ring further out, in the `app` crate.

#![forbid(unsafe_code)]

pub mod fixtures;
pub mod io;
pub mod web;

pub use fixtures::{benchmark_holdout_ids, default_catalog};
pub use io::{load_catalog, save_catalog};
pub use web::{ScoreView, catalog_to_web_json, score_to_web_json};
