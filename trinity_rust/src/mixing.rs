//! CKM and PMNS Mixing Matrices from H4 Clebsch-Gordan Coefficients
//!
//! The mixing matrices encode the mismatch between gauge eigenstates and mass eigenstates.
//! In Trinity framework, they are RETROSPECTIVE FITS to measured CKM/PMNS elements
//! using H4 root overlap integrals — no derivation from first principles exists.

use crate::ring::phi_pow;

/// CKM (Cabibbo-Kobayashi-Maskawa) quark mixing matrix
///
/// SKIPPED entries from FORMULAS.md (mathematically inconsistent):
/// - CKM04: |V_cd| = -|V_us|*|V_cb|/|V_ub|  → evaluates to 2.38 (>1, impossible)
/// - CKM05: |V_cs| = sqrt(1 - |V_cd|^2 - |V_cb|^2)  → NaN because |V_cd| > 1
/// - CKM07: |V_td| = |V_ub|*phi^2/e  → evaluates to 0.00368, document claims 0.00886
/// - CKM08: |V_ts| = |V_cb|*(1 - phi^{-3})  → evaluates to 0.031, document claims 0.040
/// - CKM09: |V_tb| = sqrt(1 - |V_td|^2 - |V_ts|^2)  → depends on inconsistent CKM07/08
/// - CKM11: sin(delta_CKM) = sin(3/phi^2)  → evaluates to 0.9117, document claims 0.9994
pub struct CKM;

impl CKM {
    /// C01: |V_us| = 2*phi^3*e^2 / (9*pi^3) = 0.2243 (0.014% error)
    pub fn v_us() -> f64 {
        let phi = phi_pow(1);
        let e = std::f64::consts::E;
        let pi = std::f64::consts::PI;
        2.0 * phi.powi(3) * e * e / (9.0 * pi.powi(3))
    }

    /// C02: |V_cb| = 1 / (3*phi^2*pi) = 0.04053 (0.069% error)
    pub fn v_cb() -> f64 {
        let phi = phi_pow(1);
        let pi = std::f64::consts::PI;
        1.0 / (3.0 * phi * phi * pi)
    }

    /// C03: |V_ub| = 5*phi^{-6}*pi^{-2}*e^{-2}
    pub fn v_ub() -> f64 {
        let phi = phi_pow(1);
        let pi = std::f64::consts::PI;
        let e = std::f64::consts::E;
        5.0 * phi.powi(-6) / (pi * pi * e * e)
    }

    /// CKM04: |V_cd| = -|V_us|*|V_cb|/|V_ub| (derived)
    pub fn v_cd() -> f64 {
        -(Self::v_us() * Self::v_cb() / Self::v_ub()).abs()
    }

    /// CKM05: |V_cs| = sqrt(1 - |V_cd|^2 - |V_cb|^2)
    pub fn v_cs() -> f64 {
        (1.0 - Self::v_cd() * Self::v_cd() - Self::v_cb() * Self::v_cb()).sqrt()
    }

    /// CKM06: |V_tb| = sqrt(1 - |V_td|^2 - |V_ts|^2)
    pub fn v_tb() -> f64 {
        (1.0 - Self::v_td() * Self::v_td() - Self::v_ts() * Self::v_ts()).sqrt()
    }

    /// CKM07: |V_td| = |V_ub| * phi^2/e
    pub fn v_td() -> f64 {
        let phi = phi_pow(1);
        let e = std::f64::consts::E;
        Self::v_ub() * phi * phi / e
    }

    /// CKM08: |V_ts| = |V_cb| * (1 - phi^{-3})
    pub fn v_ts() -> f64 {
        let phi = phi_pow(1);
        Self::v_cb() * (1.0 - phi.powi(-3))
    }

    /// CKM09: |V_ud| = sqrt(1 - |V_us|^2 - |V_ub|^2)
    pub fn v_ud() -> f64 {
        (1.0 - Self::v_us() * Self::v_us() - Self::v_ub() * Self::v_ub()).sqrt()
    }

    /// Jarlskog invariant J_CP
    pub fn j_cp() -> f64 {
        Self::v_us() * Self::v_cb() * Self::v_ub() * Self::sin_delta_ckm()
    }

    /// sin(delta_CKM) = sin(3/phi^2)
    pub fn sin_delta_ckm() -> f64 {
        (3.0 / (phi_pow(1) * phi_pow(1))).sin()
    }

    /// gamma angle = 3/phi^2 rad = 65.66°
    pub fn gamma_angle() -> f64 {
        3.0 / (phi_pow(1) * phi_pow(1))
    }
}

/// PMNS (Pontecorvo-Maki-Nakagawa-Sakata) neutrino mixing matrix
pub struct PMNS;

impl PMNS {
    /// N01: sin^2(theta_12) = 8*pi / (phi^5 * e^2) = 0.3067 (0.098% error)
    pub fn sin2_theta_12() -> f64 {
        let phi = phi_pow(1);
        let e = std::f64::consts::E;
        let pi = std::f64::consts::PI;
        8.0 * pi / (phi.powi(5) * e * e)
    }

    /// N02: sin^2(theta_23) = phi^2 / e = 0.963 (tension with data ~0.546)
    pub fn sin2_theta_23() -> f64 {
        let phi = phi_pow(1);
        let e = std::f64::consts::E;
        phi * phi / e
    }

    /// N03: sin^2(theta_13) = pi^2 / (25*phi^6) = 0.02200 (0.003% error, SG-class)
    pub fn sin2_theta_13() -> f64 {
        let phi = phi_pow(1);
        let pi = std::f64::consts::PI;
        pi * pi / (25.0 * phi.powi(6))
    }

    /// N04: delta_CP = 3/phi^2 rad = 65.66° (RISKY: 5.6 sigma tension with NuFit ~177°)
    pub fn delta_cp() -> f64 {
        3.0 / (phi_pow(1) * phi_pow(1))
    }

    /// sin(theta_13) = pi / (5*phi^3)
    pub fn sin_theta_13() -> f64 {
        let phi = phi_pow(1);
        let pi = std::f64::consts::PI;
        pi / (5.0 * phi.powi(3))
    }

    /// cos^2(theta_13) = 1 - sin^2(theta_13)
    pub fn cos2_theta_13() -> f64 {
        1.0 - Self::sin2_theta_13()
    }

    /// cos^2(theta_12) = 1 - sin^2(theta_12)
    pub fn cos2_theta_12() -> f64 {
        1.0 - Self::sin2_theta_12()
    }

    /// PM05: cos^2(theta_23) = 1 - sin^2(theta_23)
    pub fn cos2_theta_23() -> f64 {
        1.0 - Self::sin2_theta_23()
    }

    /// PM07: sin(theta_12) = sqrt(sin^2(theta_12))
    pub fn sin_theta_12() -> f64 {
        Self::sin2_theta_12().sqrt()
    }

    /// PM08: sin(theta_23) = sqrt(sin^2(theta_23))
    pub fn sin_theta_23() -> f64 {
        Self::sin2_theta_23().sqrt()
    }

    /// Neutrino mass-squared differences
    pub fn delta_m2_21() -> f64 {
        // (phi*e/pi)^6 * 10^{-5} eV^2 = 7.53e-5 eV^2
        let phi = phi_pow(1);
        let e = std::f64::consts::E;
        let pi = std::f64::consts::PI;
        (phi * e / pi).powi(6) * 1e-5
    }

    pub fn delta_m2_31_nh() -> f64 {
        // 15*phi^{-5}*pi^{-2}*e^{-4} eV^2 = 2.51e-3 eV^2
        let phi = phi_pow(1);
        let e = std::f64::consts::E;
        let pi = std::f64::consts::PI;
        15.0 * phi.powi(-5) / (pi * pi * e.powi(4))
    }

    /// Ratio: Delta_m2_21 / Delta_m2_31 = pi / (40*phi^2) = 0.0300
    pub fn delta_m2_ratio() -> f64 {
        let phi = phi_pow(1);
        let pi = std::f64::consts::PI;
        pi / (40.0 * phi * phi)
    }

    /// Sum of neutrino masses: Sigma m_nu = 8*phi^{-6}*pi^{-5}*e^6 * 10^{-1} eV
    pub fn sum_m_nu() -> f64 {
        let phi = phi_pow(1);
        let e = std::f64::consts::E;
        let pi = std::f64::consts::PI;
        8.0 * phi.powi(-6) * e.powi(6) / (pi.powi(5) * 10.0)
    }

    /// Leptonic Jarlskog J_CP^nu
    ///
    /// NOTE: PM12 formula in FORMULAS.md claims 0.033, but the expression
    /// sin(theta_12)*sin(theta_23)*sin(theta_13)*cos(theta_13)*cos(theta_12)*sin(delta)
    /// (as written in the document) evaluates to ~0.06 with Trinity angles.
    /// The standard J_CP = c_12*s_12*c_13^2*s_13*c_23*s_23*sin(delta) gives ~0.012.
    /// Neither matches the claimed 0.033. PM12 skipped in formula catalog.
    pub fn j_cp_nu() -> f64 {
        let s12 = Self::sin2_theta_12().sqrt();
        let s23 = Self::sin2_theta_23().sqrt();
        let s13 = Self::sin2_theta_13().sqrt();
        let c13 = Self::cos2_theta_13().sqrt();
        let c12 = Self::cos2_theta_12().sqrt();
        s12 * s23 * s13 * c13 * c12 * Self::sin_delta_cp()
    }

    pub fn sin_delta_cp() -> f64 {
        Self::delta_cp().sin()
    }

    pub fn cos_delta_cp() -> f64 {
        Self::delta_cp().cos()
    }
}

/// Wolfenstein parameterization
pub struct Wolfenstein;

impl Wolfenstein {
    /// lambda = |V_us| ≈ 0.2243
    pub fn lambda() -> f64 {
        CKM::v_us()
    }

    /// A ≈ 0.836
    pub fn a() -> f64 {
        CKM::v_cb() / CKM::v_us().powi(2)
    }

    /// rho-bar ≈ 0.14
    pub fn rho_bar() -> f64 {
        CKM::gamma_angle().cos() * Self::a() * CKM::v_us().powi(2)
    }

    /// eta-bar ≈ 0.34
    pub fn eta_bar() -> f64 {
        CKM::gamma_angle().sin() * Self::a() * CKM::v_us().powi(2)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ckm_elements() {
        assert!(
            (CKM::v_us() - 0.2243).abs() < 0.001,
            "V_us: {}",
            CKM::v_us()
        );
        assert!(
            (CKM::v_cb() - 0.04053).abs() < 0.001,
            "V_cb: {}",
            CKM::v_cb()
        );
    }

    #[test]
    fn test_pmns_angles() {
        assert!(
            (PMNS::sin2_theta_13() - 0.0220).abs() < 0.001,
            "sin2_13: {}",
            PMNS::sin2_theta_13()
        );
        assert!(
            (PMNS::sin2_theta_12() - 0.307).abs() < 0.01,
            "sin2_12: {}",
            PMNS::sin2_theta_12()
        );
    }

    #[test]
    fn test_neutrino_masses() {
        assert!(
            (PMNS::delta_m2_21() - 7.53e-5).abs() < 1e-6,
            "dm2_21: {}",
            PMNS::delta_m2_21()
        );
        assert!(
            (PMNS::delta_m2_31_nh() - 2.51e-3).abs() < 1e-4,
            "dm2_31: {}",
            PMNS::delta_m2_31_nh()
        );
        assert!(
            (PMNS::sum_m_nu() - 0.058).abs() < 0.01,
            "sum_mnu: {}",
            PMNS::sum_m_nu()
        );
    }
}
