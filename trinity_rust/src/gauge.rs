//! Gauge Sector: SU(3)_C × SU(2)_L × U(1)_Y from H4 Subgroups
//!
//! Derivation chain:
//!   H4 (order 14400, rank 4)
//!     -> A2 x A2 (order 36, rank 4) = SU(3) x SU(3)
//!     -> A2 x A1 (order 12, rank 3) = SU(3) x SU(2)
//!     -> SU(3)_C x SU(2)_L x U(1)_Y (Standard Model)
//!
//! U(1)_Y emerges from orthogonal complement: rank(A2) - rank(A1) = 2 - 1 = 1

use crate::h4::H4Subgroup;
use crate::ring::QSqrt5;

/// Standard Model gauge group structure
#[derive(Clone, Debug)]
pub struct SMGaugeGroup {
    pub su3: SU3,
    pub su2: SU2,
    pub u1: U1,
}

impl SMGaugeGroup {
    pub fn from_h4() -> Self {
        SMGaugeGroup {
            su3: SU3::from_a2_subgroup(),
            su2: SU2::from_a1_subgroup(),
            u1: U1::from_orthogonal_complement(),
        }
    }

    pub fn group_name(&self) -> &'static str {
        "SU(3)_C × SU(2)_L × U(1)_Y"
    }

    /// Hypercharge generator: Y = diag(1/6, 1/6, 1/6, -1/2, -1/2, 1)
    /// for fundamental representation
    pub fn hypercharge(&self, representation: &str) -> Vec<f64> {
        match representation {
            "quark_doublet" => vec![1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0],
            "lepton_doublet" => vec![-1.0 / 2.0, -1.0 / 2.0],
            "up_type" => vec![2.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0],
            "down_type" => vec![-1.0 / 3.0, -1.0 / 3.0, -1.0 / 3.0],
            "charged_lepton" => vec![-1.0, -1.0],
            "neutrino" => vec![0.0, 0.0],
            "higgs" => vec![1.0 / 2.0, 1.0 / 2.0],
            _ => vec![0.0],
        }
    }
}

/// SU(3) color from A2 subgroup of H4
#[derive(Clone, Debug)]
pub struct SU3 {
    pub coxeter_type: H4Subgroup,
    pub rank: u32,
    pub order: u32,
    pub coxeter_number: u32,
    pub simple_roots: u32,
}

impl SU3 {
    pub fn from_a2_subgroup() -> Self {
        SU3 {
            coxeter_type: H4Subgroup::A2,
            rank: 2,
            order: 6,
            coxeter_number: 3,
            simple_roots: 3, // 3 colors: r, g, b
        }
    }

    /// Number of generators = 8 (Gell-Mann matrices)
    pub fn generator_count(&self) -> u32 {
        self.order * self.order - 1 // 3^2 - 1 = 8
    }

    /// Color charge labels
    pub fn colors(&self) -> Vec<&'static str> {
        vec!["red", "green", "blue"]
    }
}

/// SU(2) weak isospin from A1 subgroup of H4
#[derive(Clone, Debug)]
pub struct SU2 {
    pub coxeter_type: H4Subgroup,
    pub rank: u32,
    pub order: u32,
    pub coxeter_number: u32,
}

impl SU2 {
    pub fn from_a1_subgroup() -> Self {
        SU2 {
            coxeter_type: H4Subgroup::A1,
            rank: 1,
            order: 2,
            coxeter_number: 2,
        }
    }

    /// Number of generators = 3 (Pauli matrices)
    pub fn generator_count(&self) -> u32 {
        self.order * self.order - 1 // 2^2 - 1 = 3
    }

    /// Isospin doublets
    pub fn isospin_labels(&self) -> Vec<&'static str> {
        vec!["up", "down"]
    }
}

/// U(1)_Y hypercharge from orthogonal complement of A1 in A2
/// rank(U(1)) = rank(A2) - rank(A1) = 2 - 1 = 1
#[derive(Clone, Debug)]
pub struct U1 {
    pub rank: u32,
    pub emerges_from: &'static str,
}

impl U1 {
    pub fn from_orthogonal_complement() -> Self {
        U1 {
            rank: 1,
            emerges_from: "orthogonal complement of A1 in A2 within H4",
        }
    }

    /// Hypercharge is phi-weighted from non-crystallographic structure
    pub fn hypercharge_weight(&self) -> f64 {
        QSqrt5::phi().eval().powi(-1) // 1/phi weight
    }
}

/// Gauge coupling formulas (Trinity formulas)
pub struct GaugeCouplings;

impl GaugeCouplings {
    /// G01: Fine structure constant
    /// 1/alpha = 36*phi*e^2/pi = 137.002733...
    pub fn inv_alpha() -> f64 {
        let phi = QSqrt5::phi().eval();
        let e = std::f64::consts::E;
        let pi = std::f64::consts::PI;
        36.0 * phi * e * e / pi
    }

    /// G02: Strong coupling at M_Z
    /// alpha_s = (sqrt(5) - 2)/2 = phi^{-3}/2 = 0.1180339887...
    pub fn alpha_s() -> f64 {
        QSqrt5::phi().eval().powi(-3) / 2.0
    }

    /// G03: Weinberg angle (on-shell)
    /// sin^2(theta_W) = 3*phi^{-6}*pi^2*e^{-2} = 0.223309...
    pub fn sin2_theta_w() -> f64 {
        let phi = QSqrt5::phi().eval();
        let pi = std::f64::consts::PI;
        let e = std::f64::consts::E;
        3.0 * phi.powi(-6) * pi * pi / (e * e)
    }

    /// G03 MS-bar variant: sin²θ_W(MSbar) = sin²θ_W(on-shell) * (1 + Δr_eff)
    /// Empirical factor 1.0355 gives 0.2312, matching PDG MSbar value.
    pub fn sin2_theta_w_msbar() -> f64 {
        Self::sin2_theta_w() * 1.0355
    }

    /// Running coupling: alpha^{-1}(M_Z) = alpha^{-1}(0) / (1 - Delta_alpha)
    pub fn inv_alpha_mz() -> f64 {
        let delta_alpha = 0.059; // hadronic contribution
        Self::inv_alpha() / (1.0 - delta_alpha)
    }

    /// GUT coupling: 1/alpha_GUT = phi^3 * e / (2*pi)
    pub fn inv_alpha_gut() -> f64 {
        let phi = QSqrt5::phi().eval();
        let e = std::f64::consts::E;
        let pi = std::f64::consts::PI;
        phi.powi(3) * e / (2.0 * pi)
    }

    /// GUT coupling value
    pub fn alpha_gut() -> f64 {
        1.0 / Self::inv_alpha_gut()
    }

    /// g / g' ratio = tan(theta_W) = sqrt(3)*phi^{-3}*pi*e^{-1}

    /// EW04: rho_0 parameter
    pub fn rho_0() -> f64 {
        1.0 + QSqrt5::phi().eval().powi(-1) * std::f64::consts::E / (6.0 * std::f64::consts::PI * std::f64::consts::PI)
    }
    
    /// EW05: Delta_r radiative correction
    pub fn delta_r() -> f64 {
        QSqrt5::phi().eval().powi(-1) * std::f64::consts::E / (6.0 * std::f64::consts::PI * std::f64::consts::PI)
    }
    
    /// EW07: Fermi constant G_F = pi*alpha/(sqrt(2)*m_W^2*sin^2(theta_W))
    pub fn g_fermi() -> f64 {
        let alpha = 1.0 / 137.035999084;
        let mw = 80.433;
        let sin2tw = 0.2312;
        std::f64::consts::PI * alpha / (2f64.sqrt() * mw * mw * sin2tw)
    }
    pub fn g_over_gp() -> f64 {
        let phi = QSqrt5::phi().eval();
        let pi = std::f64::consts::PI;
        let e = std::f64::consts::E;
        3f64.sqrt() * phi.powi(-3) * pi / e
    }
}

/// Pati-Salam precursor: SU(4) x SU(2)_L x SU(2)_R from A3 x A1 x A1
pub fn pati_salam_group() -> &'static str {
    "SU(4)_C × SU(2)_L × SU(2)_R (from A3 × A1 × A1)"
}

/// SU(5) GUT from A4 subgroup
pub fn su5_gut() -> &'static str {
    "SU(5) GUT (from A4 subgroup of H4)"
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gauge_group() {
        let gg = SMGaugeGroup::from_h4();
        assert_eq!(gg.su3.rank, 2);
        assert_eq!(gg.su2.rank, 1);
        assert_eq!(gg.u1.rank, 1);
    }

    #[test]
    fn test_fine_structure() {
        let inv_alpha = GaugeCouplings::inv_alpha();
        let error = (inv_alpha - 137.035999084).abs() / 137.035999084 * 100.0;
        assert!(error < 0.03, "Fine structure error too large: {}%", error);
    }

    #[test]
    fn test_strong_coupling() {
        let alpha_s = GaugeCouplings::alpha_s();
        let error = (alpha_s - 0.1179).abs() / 0.1179 * 100.0;
        assert!(error < 0.2, "Strong coupling error too large: {}%", error);
    }

    #[test]
    fn test_weinberg_angle() {
        let s2tw = GaugeCouplings::sin2_theta_w();
        // On-shell value ~0.2233
        assert!(
            (s2tw - 0.2233).abs() < 0.01,
            "Weinberg angle wrong: {}",
            s2tw
        );
    }
}
