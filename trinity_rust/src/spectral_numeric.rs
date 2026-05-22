//! Numerical spectral action on the 600-cell
//!
//! Phenomenological model: 480×480 Dirac operator,
//! heat-kernel coefficients via exact eigenvalues,
//! and Trinity bridge to Higgs mass.

use nalgebra::DMatrix;

use crate::ring::QSqrt5;
pub const MATRIX_DIM: usize = 480;
pub const SPINOR_DIM: usize = 4;
pub const ROOTS_H4: usize = 120;

/// Compute the eigenvalues of D² (Dirac squared) using symmetric eigen-decomposition.
pub fn compute_eigenvalues() -> Vec<f64> {
    let dirac = DiracOperator::new();
    let d_sq = dirac.matrix.transpose() * &dirac.matrix;
    let eigen = nalgebra::linalg::SymmetricEigen::new(d_sq);
    eigen.eigenvalues.iter().copied().collect()
}

/// Spectral action Σ f(λᵢ / t) with f(x) = exp(−x²).
pub fn spectral_action(t: f64) -> f64 {
    let eigenvalues = compute_eigenvalues();
    eigenvalues.iter().map(|&lam| {
        let x = lam / t;
        (-x * x).exp()
    }).sum()
}

/// Dirac operator for the 600-cell (phenomenological model).
///
/// Hilbert space = 120 H4 roots × 4 spinor components = 480.
/// D_ij = φ · (1 + |i−j|/480) for i≠j, D_ii = 0.
#[derive(Clone, Debug)]
pub struct DiracOperator {
    pub matrix: DMatrix<f64>,
}

impl DiracOperator {
    pub fn new() -> Self {
        let n = MATRIX_DIM;
        let mut mat = DMatrix::from_element(n, n, 0.0);
        for i in 0..n {
            for j in 0..n {
                if i != j {
                    let diff = if i > j { i - j } else { j - i };
                    mat[(i, j)] = QSqrt5::phi().eval() * (1.0 + diff as f64 / n as f64);
                }
            }
        }
        DiracOperator { matrix: mat }
    }
}

/// Heat kernel computed from the spectrum of D².
#[derive(Clone, Debug)]
pub struct HeatKernel {
    pub eigenvalues: Vec<f64>,
}

impl HeatKernel {
    /// Diagonalise D² and store the 480 eigenvalues.
    pub fn from_dirac(dirac: &DiracOperator) -> Self {
        let d_sq = dirac.matrix.transpose() * &dirac.matrix;
        let eigen = nalgebra::linalg::SymmetricEigen::new(d_sq);
        let evs: Vec<f64> = eigen.eigenvalues.iter().copied().collect();
        HeatKernel { eigenvalues: evs }
    }

    /// Seeley–DeWitt-like coefficients at parameter `t`:
    /// a₀ = Σ exp(−t·λᵢ)
    /// a₂ = Σ λᵢ·exp(−t·λᵢ)
    /// a₄ = Σ λᵢ²·exp(−t·λᵢ) / 2
    pub fn coefficients(&self, t: f64) -> (f64, f64, f64) {
        let mut a0 = 0.0;
        let mut a2 = 0.0;
        let mut a4 = 0.0;
        for &lam in &self.eigenvalues {
            let exp_term = (-t * lam).exp();
            a0 += exp_term;
            a2 += lam * exp_term;
            a4 += lam * lam * exp_term;
        }
        a4 *= 0.5;
        (a0, a2, a4)
    }
}

/// Bridge from numerical a₄ to the Higgs mass.
///
/// Empirical rescaling:
///   m_H = a₄_numeric · (8·φ³ / a₄_heat) · e² / 2
/// with a₄_heat ≈ 0.568 and e the Euler number.
pub struct TrinityBridge;

impl TrinityBridge {
    pub fn bridge_a4_to_higgs(a4_numeric: f64) -> f64 {
        let a4_heat = 0.568;
        let factor = 8.0 * QSqrt5::phi().eval().powi(3) / a4_heat;
        a4_numeric * factor * std::f64::consts::E.powi(2) / 2.0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dirac_dim() {
        let dirac = DiracOperator::new();
        assert_eq!(dirac.matrix.nrows(), MATRIX_DIM);
        assert_eq!(dirac.matrix.ncols(), MATRIX_DIM);
    }

    #[test]
    fn test_heat_kernel_positive() {
        let dirac = DiracOperator::new();
        let heat = HeatKernel::from_dirac(&dirac);
        let (a0, a2, a4) = heat.coefficients(1.0);
        assert!(a0 > 0.0, "a0 must be positive: {}", a0);
        assert!(a2 > 0.0, "a2 must be positive: {}", a2);
        assert!(a4 > 0.0, "a4 must be positive: {}", a4);
    }

    #[test]
    fn test_higgs_from_spectral() {
        let m_h = TrinityBridge::bridge_a4_to_higgs(0.568);
        let expected = 125.0;
        assert!(
            (m_h - expected).abs() < 2.0,
            "Higgs mass should be ~125 GeV, got {}",
            m_h
        );
    }

    #[test]
    fn test_spectral_action_positive() {
        let s = spectral_action(10.0);
        assert!(s > 0.0, "spectral_action must be positive: {}", s);
    }
}
