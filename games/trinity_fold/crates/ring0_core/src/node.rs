use crate::claim::ClaimStatus;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

/// What category a tile represents on the puzzle board.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum NodeKind {
    /// A dimensionful or dimensionless physical constant (G, hbar, alpha, ...).
    Constant,
    /// A field appearing in a Lagrangian (Higgs, fermion, gauge, gravity).
    Field,
    /// A symmetry group or generator (SU(3), Lorentz, conformal, ...).
    Symmetry,
    /// A geometric/algebraic building block (H4 root system, 600-cell,
    /// Clifford algebra Cl(p,q), F4 spectrum, NCG spectral triple, ...).
    Geometry,
    /// An algebraic or differential constraint the candidate must respect
    /// (dimensional sanity, anomaly cancellation, unitarity, ...).
    Constraint,
    /// An experimental observable used to score fit (PDG quantity, etc.).
    Observable,
}

impl NodeKind {
    pub fn label(&self) -> &'static str {
        match self {
            NodeKind::Constant => "constant",
            NodeKind::Field => "field",
            NodeKind::Symmetry => "symmetry",
            NodeKind::Geometry => "geometry",
            NodeKind::Constraint => "constraint",
            NodeKind::Observable => "observable",
        }
    }

    /// Which of the two AlphaFold-style towers a node sits in.
    /// The Data Tower holds empirical constraints and observables.
    /// The Geometry Tower holds symmetry, geometry, fields, constants.
    pub fn tower(&self) -> Tower {
        match self {
            NodeKind::Constraint | NodeKind::Observable => Tower::Data,
            NodeKind::Constant | NodeKind::Field | NodeKind::Symmetry | NodeKind::Geometry => {
                Tower::Geometry
            }
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Tower {
    Data,
    Geometry,
}

/// A single tile in the puzzle.
///
/// `requires` lists ids of other nodes that must be present on the board for
/// this one to count (e.g. a Higgs-mass observable requires a Higgs field).
/// `incompatible_with` lists ids that, if both present, falsify the board
/// (e.g. an H4-only chirality claim is incompatible with NGT3).
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Node {
    pub id: String,
    pub kind: NodeKind,
    pub name: String,
    pub description: String,
    pub claim: ClaimStatus,
    /// Dimensional signature, e.g. `{"mass": 1, "length": -1}`. Empty for
    /// dimensionless quantities. Only used by the dimensional sanity check.
    #[serde(default)]
    pub dimension: BTreeMap<String, i32>,
    /// Numerical value of an observable in `unit`. Optional; only used by
    /// the empirical-fit term in the scorer.
    #[serde(default)]
    pub value: Option<f64>,
    #[serde(default)]
    pub uncertainty: Option<f64>,
    #[serde(default)]
    pub unit: Option<String>,
    /// Predicted value supplied by the player ("if you place these tiles,
    /// the candidate predicts this number"). Optional.
    #[serde(default)]
    pub predicted: Option<f64>,
    #[serde(default)]
    pub requires: Vec<String>,
    #[serde(default)]
    pub incompatible_with: Vec<String>,
    /// Free-form tags. The presence of `proof_debt` increases the proof-debt
    /// penalty; `compression` rewards simplicity. The set of meaningful tags
    /// is documented in `docs/SCORING.md`.
    #[serde(default)]
    pub tags: Vec<String>,
    /// Optional citation: PDG entry, arXiv id, Coq theorem name, etc.
    #[serde(default)]
    pub citation: Option<String>,
}

impl Node {
    pub fn has_tag(&self, tag: &str) -> bool {
        self.tags.iter().any(|t| t == tag)
    }
}
