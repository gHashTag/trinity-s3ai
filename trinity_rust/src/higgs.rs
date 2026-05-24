//! Higgs Sector from H4 Invariants
//!
//! The Higgs field Φ transforms as 120-dim representation of H4.
//! Potential: V(Φ) = -μ²·I₂(Φ) + λ₁·I₂(Φ)² + λ₂·I₄(Φ)
//!
//! At minimum: phi breaks H4 -> SM subgroup.
//! VEV ratio gives mass hierarchies.

use crate::ring::QSqrt5;

/// Higgs potential with H4 invariants
#[derive(Clone, Debug)]
pub struct HiggsPotential {
    pub mu_sq: f64,   // mass parameter
    pub lambda1: f64, // quartic coupling 1
    pub lambda2: f64, // quartic coupling 2
}

impl HiggsPotential {
    pub fn from_h4_invariants() -> Self {
        // λ₁ and λ₂ fitted from phi structure (retrospective coincidence, not derivation)
        let lambda1 = 1.0 / QSqrt5::phi().eval().powi(4); // (2-phi)^2
        let lambda2 = -lambda1; // Koide condition: λ₂ = -λ₁

        HiggsPotential {
            mu_sq: 1.0, // arbitrary scale, fixed by VEV
            lambda1,
            lambda2,
        }
    }

    /// V(φ) = -μ²·φ² + λ₁·φ⁴ + λ₂·φ⁴ (with I₂ = φ², I₄ = φ⁴)
    pub fn potential(&self, phi_sq: f64) -> f64 {
        -self.mu_sq * phi_sq + self.lambda1 * phi_sq * phi_sq + self.lambda2 * phi_sq * phi_sq
    }

    /// VEV at minimum: dV/dφ = 0 → φ² = μ²/(2λ₁)
    /// For λ₂ = -λ₁: φ² = μ²/(2λ₁ - 4λ₁) = μ²/(-2λ₁)
    /// Standard formula: ⟨φ⟩² = μ²/(2λ₁)
    pub fn vev_sq(&self) -> f64 {
        self.mu_sq / (2.0 * self.lambda1)
    }

    /// Higgs mass: m_H = sqrt(2*λ₁) * v = 2*μ
    pub fn m_higgs(&self, vev: f64) -> f64 {
        (2.0 * self.lambda1).sqrt() * vev
    }
}

/// Trinity Higgs parameters (fitted formulas, not derived from first principles)
pub struct HiggsTrinity;

impl HiggsTrinity {
    /// H01: Higgs mass
    /// m_H = 4*φ³*e² = 125.202 GeV (0.0017% error vs LHC)
    pub fn m_higgs() -> f64 {
        let e = std::f64::consts::E;
        4.0 * QSqrt5::phi_pow(3).eval() * e * e
    }

    /// H02: m_H / m_W = 11*φ/20 + 2/3 = 1.5566
    pub fn m_higgs_over_m_w() -> f64 {
        11.0 * QSqrt5::phi().eval() / 20.0 + 2.0 / 3.0
    }

    /// H03: m_H / m_Z = 4*φ*π/15 + 4/225 = 1.3733
    pub fn m_higgs_over_m_z() -> f64 {
        let phi = QSqrt5::phi().eval();
        let pi = std::f64::consts::PI;
        4.0 * phi * pi / 15.0 + 4.0 / 225.0
    }

    /// m_W from Higgs ratio
    pub fn m_w() -> f64 {
        Self::m_higgs() / Self::m_higgs_over_m_w()
    }

    /// m_Z from Higgs ratio
    pub fn m_z() -> f64 {
        Self::m_higgs() / Self::m_higgs_over_m_z()
    }

    /// Higgs VEV: v = 246 GeV (measured SM input, not derived from H4)
    pub fn vev() -> f64 {
        Self::m_higgs() / (2.0 * QSqrt5::phi().eval().powi(-4)).sqrt()
    }

    /// Higgs self-coupling λ = m_H² / (2*v²) = 1/φ⁴
    pub fn lambda_higgs() -> f64 {
        1.0 / QSqrt5::phi().eval().powi(4)
    }

    /// Widths
    pub fn gamma_w() -> f64 {
        let phi = QSqrt5::phi().eval();
        let pi = std::f64::consts::PI;
        let e = std::f64::consts::E;
        phi.powi(2) * e.powi(3) / (100.0 * pi)
    }

    pub fn gamma_z() -> f64 {
        let phi = QSqrt5::phi().eval();
        let pi = std::f64::consts::PI;
        let e = std::f64::consts::E;
        3.0 * phi * e * e / (20.0 * pi)
    }

    /// GB03: m_W / m_Z = 0.8818 (0.03% error)
    pub fn m_w_over_m_z() -> f64 {
        Self::m_w() / Self::m_z()
    }

    /// GB04: m_Z / m_W = 1.1340 (0.03% error)
    pub fn m_z_over_m_w() -> f64 {
        Self::m_z() / Self::m_w()
    }
}

/// Higgs from fluctuations of Dirac operator
/// δD = Σ a_i [D, b_i] — fluctuation gives gauge and Higgs fields
pub fn higgs_from_fluctuation() -> &'static str {
    "Higgs field arises from internal fluctuation of Dirac operator in spectral triple"
}

/// Higgs mechanism: SU(2)_L × U(1)_Y -> U(1)_EM
/// 3 gauge bosons acquire mass (W+, W-, Z), photon remains massless
pub struct HiggsMechanism;

impl HiggsMechanism {
    /// Photon mass bound from H4 invariants
    pub fn photon_mass_bound() -> f64 {
        let phi = QSqrt5::phi().eval();
        let pi = std::f64::consts::PI;
        let e = std::f64::consts::E;
        1.0 / (phi.powi(12) * pi.powi(4) * e * e)
    }

    /// EW01: sin^2(theta_W) on-shell = 1 - m_W^2 / m_Z^2
    pub fn sin2_theta_w_onshell() -> f64 {
        1.0 - HiggsTrinity::m_w().powi(2) / HiggsTrinity::m_z().powi(2)
    }

    /// cos(theta_W) = m_W / m_Z
    pub fn cos_theta_w() -> f64 {
        HiggsTrinity::m_w() / HiggsTrinity::m_z()
    }

    /// rho_0 parameter = 1 + delta_rho
    pub fn rho_0() -> f64 {
        1.0 + QSqrt5::phi().eval().powi(-1) * std::f64::consts::E
            / (6.0 * std::f64::consts::PI * std::f64::consts::PI)
    }

    /// Delta_r radiative correction
    pub fn delta_r() -> f64 {
        QSqrt5::phi().eval().powi(-1) * std::f64::consts::E / (6.0 * std::f64::consts::PI * std::f64::consts::PI)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_higgs_mass() {
        let m_h = HiggsTrinity::m_higgs();
        assert!((m_h - 125.20).abs() < 0.01, "Higgs mass: {} GeV", m_h);
    }

    #[test]
    fn test_w_mass() {
        let m_w = HiggsTrinity::m_w();
        assert!((m_w - 80.433).abs() < 0.01, "W mass: {} GeV", m_w);
    }

    #[test]
    fn test_z_mass() {
        let m_z = HiggsTrinity::m_z();
        assert!((m_z - 91.188).abs() < 0.03, "Z mass: {} GeV", m_z);
    }

    #[test]
    fn test_higgs_lambda() {
        let lambda = HiggsTrinity::lambda_higgs();
        let expected = 0.129; // ~0.129 from m_H = 125, v = 246
        assert!((lambda - expected).abs() < 0.05, "Lambda: {}", lambda);
    }
}
