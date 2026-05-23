// Trinity Fold — puzzle prototype for exploring candidate unification structures.
//
// Honesty-first: this library does NOT prove a Theory of Everything. It scores
// candidate boards built from theory tiles against a fixed set of constraints
// and observables, and tags every score with a claim status.
//
// See games/trinity_fold/README.md for the full claim-status policy.

pub mod board;
pub mod claim;
pub mod fixtures;
pub mod io;
pub mod node;
pub mod scoring;
pub mod search;

pub use board::Board;
pub use claim::ClaimStatus;
pub use node::{Node, NodeKind};
pub use scoring::{ScoreBreakdown, score_board};
