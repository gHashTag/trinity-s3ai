use serde::{Deserialize, Serialize};

/// Claim status for any node, observable, score component, or board summary.
///
/// Mirrors the honesty taxonomy used elsewhere in the repository
/// (CONTRIBUTING.md, anti_numerology_gate.py, admitted_log.md).
///
/// Order is significant: lower discriminants are stronger claims.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ClaimStatus {
    /// Backed by a Qed Coq proof or equivalent formal derivation.
    #[default]
    Verified,
    /// Numerical agreement with experiment within a stated tolerance,
    /// not derived from first principles. Equivalent to `[NUMERICAL_FIT]`
    /// or `[phenomenological_fit]` tags in the Coq sources.
    EmpiricalFit,
    /// Stated but not proven; no falsifying evidence yet.
    OpenConjecture,
    /// Currently contradicted by data or by an existing No-Go theorem.
    HighRiskOrFalsified,
    /// Default for fresh user input. Must be promoted before it counts
    /// toward a non-trivial score contribution.
    Unverified,
}

impl ClaimStatus {
    pub fn label(&self) -> &'static str {
        match self {
            ClaimStatus::Verified => "VERIFIED",
            ClaimStatus::EmpiricalFit => "EMPIRICAL_FIT",
            ClaimStatus::OpenConjecture => "OPEN_CONJECTURE",
            ClaimStatus::HighRiskOrFalsified => "HIGH_RISK_OR_FALSIFIED",
            ClaimStatus::Unverified => "UNVERIFIED",
        }
    }

    /// Weight applied to a positive score contribution depending on the
    /// strength of the underlying claim. Used by `scoring::score_board`.
    ///
    /// Intentionally conservative: an `Unverified` contribution is worth
    /// zero, and a `HighRiskOrFalsified` contribution carries a penalty
    /// (handled separately in the scorer, not via this weight).
    pub fn positive_weight(&self) -> f64 {
        match self {
            ClaimStatus::Verified => 1.0,
            ClaimStatus::EmpiricalFit => 0.4,
            ClaimStatus::OpenConjecture => 0.15,
            ClaimStatus::HighRiskOrFalsified => 0.0,
            ClaimStatus::Unverified => 0.0,
        }
    }
}
