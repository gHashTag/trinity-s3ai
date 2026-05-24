// Default illustrative catalog.
//
// Every entry is tagged with a `ClaimStatus`. The conjecture-level entries
// (e.g. "single-formula derivation of m_H from H4") are explicitly labelled
// OpenConjecture or HighRiskOrFalsified and cite a repo file when relevant.
// Numerical fixtures are anchored to PDG-style values; the goal is to give
// the puzzle something concrete to score, NOT to assert any of these formulas
// are derived from first principles.

use ring0_core::{Catalog, ClaimStatus, Node, NodeKind};
use std::collections::BTreeMap;

fn dim(pairs: &[(&str, i32)]) -> BTreeMap<String, i32> {
    pairs.iter().map(|(k, v)| ((*k).to_string(), *v)).collect()
}

fn node(id: &str, kind: NodeKind, name: &str, desc: &str, claim: ClaimStatus) -> Node {
    Node {
        id: id.into(),
        kind,
        name: name.into(),
        description: desc.into(),
        claim,
        dimension: BTreeMap::new(),
        value: None,
        uncertainty: None,
        unit: None,
        predicted: None,
        requires: vec![],
        incompatible_with: vec![],
        tags: vec![],
        citation: None,
    }
}

/// Build the default illustrative catalog.
pub fn default_catalog() -> Catalog {
    let mut nodes: Vec<Node> = Vec::new();

    // --- Geometry tower: constants ---
    let mut n = node(
        "c_hbar",
        NodeKind::Constant,
        "ℏ",
        "Reduced Planck constant. Verified physical constant; sets units of action.",
        ClaimStatus::Verified,
    );
    n.dimension = dim(&[("mass", 1), ("length", 2), ("time", -1)]);
    n.value = Some(1.054_571_817e-34);
    n.unit = Some("J·s".into());
    n.citation = Some("CODATA 2018".into());
    nodes.push(n);

    let mut n = node(
        "c_c",
        NodeKind::Constant,
        "c",
        "Speed of light in vacuum (defined value in SI).",
        ClaimStatus::Verified,
    );
    n.dimension = dim(&[("length", 1), ("time", -1)]);
    n.value = Some(299_792_458.0);
    n.unit = Some("m/s".into());
    n.citation = Some("BIPM SI 2019".into());
    nodes.push(n);

    let mut n = node(
        "c_alpha_em",
        NodeKind::Constant,
        "α_em",
        "Fine-structure constant. Dimensionless; widely treated as input to the SM.",
        ClaimStatus::EmpiricalFit,
    );
    n.value = Some(7.297_352_5693e-3);
    n.uncertainty = Some(1.1e-12);
    n.citation = Some("PDG 2024".into());
    nodes.push(n);

    let mut n = node(
        "c_G",
        NodeKind::Constant,
        "G",
        "Newton's gravitational constant. Largest fractional uncertainty among constants.",
        ClaimStatus::EmpiricalFit,
    );
    n.dimension = dim(&[("mass", -1), ("length", 3), ("time", -2)]);
    n.value = Some(6.674_30e-11);
    n.uncertainty = Some(1.5e-15);
    n.unit = Some("m^3 kg^-1 s^-2".into());
    n.citation = Some("CODATA 2018".into());
    nodes.push(n);

    let mut n = node(
        "c_phi",
        NodeKind::Constant,
        "φ",
        "Golden ratio. Pure mathematical constant; appears in H4 root lengths.",
        ClaimStatus::Verified,
    );
    n.value = Some(1.618_033_988_749_894);
    n.tags.push("compression".into());
    nodes.push(n);

    // --- Geometry tower: symmetries ---
    let mut n = node(
        "s_su3",
        NodeKind::Symmetry,
        "SU(3)_C",
        "Color gauge symmetry of QCD.",
        ClaimStatus::Verified,
    );
    n.citation = Some("Fritzsch–Gell-Mann–Leutwyler 1973".into());
    nodes.push(n);

    let mut n = node(
        "s_su2",
        NodeKind::Symmetry,
        "SU(2)_L",
        "Weak isospin gauge symmetry.",
        ClaimStatus::Verified,
    );
    n.citation = Some("Glashow 1961".into());
    nodes.push(n);

    let mut n = node(
        "s_u1",
        NodeKind::Symmetry,
        "U(1)_Y",
        "Hypercharge gauge symmetry.",
        ClaimStatus::Verified,
    );
    n.citation = Some("Glashow 1961".into());
    nodes.push(n);

    let mut n = node(
        "s_lorentz",
        NodeKind::Symmetry,
        "SO(1,3)",
        "Lorentz invariance of flat spacetime.",
        ClaimStatus::Verified,
    );
    n.citation = Some("special relativity".into());
    nodes.push(n);

    let mut n = node(
        "s_h4",
        NodeKind::Symmetry,
        "H4 Coxeter",
        "Non-crystallographic Coxeter group of order 14400; root system of the 600-cell.",
        ClaimStatus::Verified,
    );
    n.citation = Some("proofs/trinity/H4Roots.v".into());
    nodes.push(n);

    // --- Geometry tower: geometry blocks ---
    let mut n = node(
        "g_600cell",
        NodeKind::Geometry,
        "600-cell",
        "Regular 4-polytope with 120 vertices; carries H4 symmetry.",
        ClaimStatus::Verified,
    );
    n.tags.push("compression".into());
    n.citation = Some("Coxeter, Regular Polytopes".into());
    nodes.push(n);

    let mut n = node(
        "g_cl8",
        NodeKind::Geometry,
        "Cl(8)",
        "Clifford algebra Cl(8); Bott-periodicity anchor for Track B.",
        ClaimStatus::OpenConjecture,
    );
    n.citation = Some("proofs/clifford_cl8/Cl8_periodicity.v (Admitted)".into());
    nodes.push(n);

    let mut n = node(
        "g_ncg_triple",
        NodeKind::Geometry,
        "NCG spectral triple (A, H, D)",
        "Connes-style spectral triple; backbone of NCG models of the SM.",
        ClaimStatus::OpenConjecture,
    );
    n.citation = Some("Connes-Marcolli 2008".into());
    nodes.push(n);

    let mut n = node(
        "g_f4_spectrum",
        NodeKind::Geometry,
        "F4 spectrum",
        "Eigenvalues of the Dirac operator restricted to an F4-symmetric configuration.",
        ClaimStatus::OpenConjecture,
    );
    n.citation = Some("derivations/f4_spectrum/".into());
    nodes.push(n);

    // --- Geometry tower: fields ---
    let mut n = node(
        "f_higgs",
        NodeKind::Field,
        "Higgs doublet H",
        "Complex SU(2)_L doublet whose VEV breaks electroweak symmetry.",
        ClaimStatus::Verified,
    );
    n.requires = vec!["s_su2".into(), "s_u1".into()];
    n.citation = Some("ATLAS 2012, CMS 2012".into());
    nodes.push(n);

    let mut n = node(
        "f_fermions",
        NodeKind::Field,
        "Three fermion generations",
        "Three copies of (Q, u, d, L, e) with identical gauge quantum numbers.",
        ClaimStatus::Verified,
    );
    n.citation = Some("PDG 2024".into());
    nodes.push(n);

    let mut n = node(
        "f_graviton",
        NodeKind::Field,
        "Graviton (spin-2)",
        "Massless spin-2 mediator of gravity. Quantization is open.",
        ClaimStatus::OpenConjecture,
    );
    n.requires = vec!["s_lorentz".into()];
    n.tags.push("proof_debt".into());
    nodes.push(n);

    // --- Data tower: constraints ---
    let n = node(
        "cn_dim",
        NodeKind::Constraint,
        "Dimensional sanity",
        "Every Lagrangian term must have action dimension. Free check.",
        ClaimStatus::Verified,
    );
    nodes.push(n);

    let mut n = node(
        "cn_unitarity",
        NodeKind::Constraint,
        "Unitarity",
        "Scattering amplitudes saturate the Froissart bound; partial waves bounded.",
        ClaimStatus::Verified,
    );
    n.requires = vec!["s_lorentz".into()];
    n.citation = Some("Froissart 1961; Martin 1966".into());
    nodes.push(n);

    let mut n = node(
        "cn_anomaly",
        NodeKind::Constraint,
        "Anomaly cancellation",
        "All gauge anomalies cancel across one SM generation.",
        ClaimStatus::Verified,
    );
    n.requires = vec![
        "s_su3".into(),
        "s_su2".into(),
        "s_u1".into(),
        "f_fermions".into(),
    ];
    n.citation = Some("Bouchiat-Iliopoulos-Meyer 1972".into());
    nodes.push(n);

    let mut n = node(
        "cn_ngt3_chirality",
        NodeKind::Constraint,
        "BT-3: H4 alone is vector-like",
        "Boundary theorem: 600-cell D_F is antipodal -> vector-like. Falsifies any board that tries to derive chirality from H4 + 600-cell alone.",
        ClaimStatus::HighRiskOrFalsified,
    );
    n.tags.push("no_go".into());
    n.citation = Some("proofs/trinity/BoundaryTheorems.v (BT-3)".into());
    nodes.push(n);

    let mut n = node(
        "cn_ngt1_cosmology",
        NodeKind::Constraint,
        "BT-1: φ^a·π^b·e^c cannot fit Λ",
        "Boundary theorem: no monomial in (φ, π, e) reproduces both Λ and Ω_b.",
        ClaimStatus::HighRiskOrFalsified,
    );
    n.tags.push("no_go".into());
    n.citation = Some("proofs/trinity/BoundaryTheorems.v (BT-1)".into());
    nodes.push(n);

    // --- Data tower: observables ---
    let mut n = node(
        "o_higgs_mass",
        NodeKind::Observable,
        "m_H",
        "Higgs boson mass. Tile carries an illustrative `predicted` value only if a player wires a Higgs prediction node to it.",
        ClaimStatus::EmpiricalFit,
    );
    n.value = Some(125.20);
    n.uncertainty = Some(0.11);
    n.unit = Some("GeV".into());
    n.requires = vec!["f_higgs".into()];
    n.citation = Some("PDG 2024".into());
    nodes.push(n);

    let mut n = node(
        "o_alpha_em_inv",
        NodeKind::Observable,
        "1/α_em",
        "Inverse fine-structure constant.",
        ClaimStatus::EmpiricalFit,
    );
    n.value = Some(137.035_999_084);
    n.uncertainty = Some(2.1e-8);
    n.requires = vec!["c_alpha_em".into()];
    n.citation = Some("PDG 2024".into());
    nodes.push(n);

    let mut n = node(
        "o_sin2_theta_w",
        NodeKind::Observable,
        "sin²θ_W",
        "Weak mixing angle (MS-bar). Sensitive to scheme; see sin2thetaW_schemes.md.",
        ClaimStatus::EmpiricalFit,
    );
    n.value = Some(0.231_22);
    n.uncertainty = Some(0.000_04);
    n.requires = vec!["s_su2".into(), "s_u1".into()];
    n.citation = Some("PDG 2024".into());
    nodes.push(n);

    let mut n = node(
        "o_mt_over_mb",
        NodeKind::Observable,
        "m_t / m_b",
        "Top to bottom quark mass ratio.",
        ClaimStatus::EmpiricalFit,
    );
    n.value = Some(41.5);
    n.uncertainty = Some(0.6);
    n.requires = vec!["f_fermions".into()];
    n.citation = Some("PDG 2024 pole masses".into());
    nodes.push(n);

    let mut n = node(
        "o_cosmo_lambda",
        NodeKind::Observable,
        "Λ (cosmological constant)",
        "Effective vacuum energy density inferred from Planck 2018.",
        ClaimStatus::EmpiricalFit,
    );
    n.value = Some(1.105e-52);
    n.uncertainty = Some(2.4e-54);
    n.unit = Some("m^-2".into());
    n.citation = Some("Planck 2018".into());
    nodes.push(n);

    // Evoformer-style triangle hints: triples that should travel together.
    let triangles = vec![
        ["s_su2".into(), "s_u1".into(), "f_higgs".into()],
        ["s_su3".into(), "s_su2".into(), "s_u1".into()],
        ["s_h4".into(), "g_600cell".into(), "cn_ngt3_chirality".into()],
        ["g_ncg_triple".into(), "g_cl8".into(), "f_fermions".into()],
        ["s_lorentz".into(), "cn_unitarity".into(), "f_graviton".into()],
    ];

    Catalog { nodes, triangles }
}

/// A small "benchmark" / CASP-style held-out set: nodes whose `value` field
/// is hidden from the player until they submit. The Rust CLI exposes this
/// via `--benchmark`; the web UI hides it behind a "Benchmark mode" toggle.
pub fn benchmark_holdout_ids() -> &'static [&'static str] {
    &["o_cosmo_lambda", "o_mt_over_mb"]
}
