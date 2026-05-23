//! `trinity-verification` — exact-arithmetic Rust crate replacing the
//! earlier Python verification scripts for Wave 4 / Wave 6 of
//! trinity-s3ai.
//!
//! Per rule R1 (no Python in the verification path), every numerical
//! anchor that trinity-s3ai depends on is re-derived here from
//! integer-coefficient ring elements via `Z[phi]` and the icosian
//! ring of quaternions.
//!
//! Anchor identity (proven structurally in `ring::tests`):
//!     phi^2 + phi^(-2) = 3
//! equivalently
//!     phi^4 - 3 phi^2 + 1 = 0      (held in `Z[phi]`).

pub mod icosian;
pub mod quaternion;
pub mod ring;

pub use icosian::{build_2I, find_in_2I, snub_indices};
pub use quaternion::Quat2;
pub use ring::Phi;
