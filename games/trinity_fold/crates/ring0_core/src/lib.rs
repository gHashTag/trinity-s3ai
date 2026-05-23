// Trinity Fold — ring 0 (domain core).
//
// This crate is the innermost ring. It defines pure value types: the puzzle
// `Node`, the `Board`, the `Catalog` of available tiles, and the `ClaimStatus`
// taxonomy. It has NO dependency on:
//   * I/O (no fs, no network, no JSON)
//   * UI (no printing, no formatting helpers beyond Debug)
//   * Randomness (no RNG, no clock)
//   * Scoring / search (those live in ring1 / ring2)
//
// Dependency rule: ring0 depends on nothing in the project. Anything that
// would require pulling in fs, net, time, or randomness belongs in a higher
// ring. Keeping ring0 narrow is what makes the architecture auditable.

#![forbid(unsafe_code)]

pub mod board;
pub mod claim;
pub mod node;

pub use board::{Board, Catalog};
pub use claim::ClaimStatus;
pub use node::{Node, NodeKind, Tower};
