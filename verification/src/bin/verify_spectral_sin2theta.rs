//! `verify_spectral_sin2theta` — Wave 4 W4.8.
//!
//! Replaces `wave4_spectral_sin2theta.py`. Reproduces the one-loop RG
//! running of `sin^2 theta_W` from the Pati–Salam unification boundary
//! `sin^2 theta_W(M_PS) = 2/7 = 0.285714...` down to `M_Z` and compares
//! against the PDG-2022 best fit `sin^2 theta_W(M_Z) ≈ 0.23122`.
//!
//! The flow is the only place in this crate that uses `f64`: gauge-coupling
//! running is a continuous numerical computation, not an algebraic
//! identity. Every other binary in `trinity-verification` is exact in
//! `Z[phi]`.

use std::process::ExitCode;

/// Standard Model gauge group beta-function coefficients at one loop.
/// The hypercharge value is GUT-normalised.
const B_U1: f64 = 41.0 / 10.0;
const B_SU2: f64 = -19.0 / 6.0;

/// Z-boson mass [GeV].
const M_Z: f64 = 91.1876;

/// Pati–Salam unification scale [GeV] used by trinity-s3ai (W4.8).
const M_PS: f64 = 1.0e15;

/// PDG 2022 effective sin^2 theta_W at M_Z (on-shell scheme).
const SIN2_THETA_PDG: f64 = 0.23122;

/// Pati–Salam unification boundary condition: sin^2 theta_W = 2/7.
const SIN2_AT_M_PS: f64 = 2.0 / 7.0;

/// Run sin^2 theta_W from M_PS down to M_Z at one loop.
fn run_sin2_theta_one_loop(m_high: f64, m_low: f64, sin2_high: f64) -> f64 {
    // Boundary inputs: g_1^2(M_high) and g_2^2(M_high), reconstructed from
    // the relation sin^2 theta_W = g_1^2 / (g_1^2 + g_2^2) using a chosen
    // common unified value of alpha at the high scale.
    let alpha_gut = 1.0 / 40.0; // typical SUSY-GUT-like value, used as the
                                // common starting point for both couplings.
    let g1_sq_high = 4.0 * std::f64::consts::PI * alpha_gut * sin2_high;
    let g2_sq_high = 4.0 * std::f64::consts::PI * alpha_gut * (1.0 - sin2_high);

    // One-loop running: 1/alpha_i(mu) = 1/alpha_i(M_high) - b_i/(2 pi) * ln(mu / M_high).
    // Equivalently g_i^2(mu) is obtained by inverting this.
    let log_ratio = (m_low / m_high).ln();
    let alpha_1_low_inv = (4.0 * std::f64::consts::PI / g1_sq_high) - (B_U1 / (2.0 * std::f64::consts::PI)) * log_ratio;
    let alpha_2_low_inv = (4.0 * std::f64::consts::PI / g2_sq_high) - (B_SU2 / (2.0 * std::f64::consts::PI)) * log_ratio;
    let g1_sq_low = 4.0 * std::f64::consts::PI / alpha_1_low_inv;
    let g2_sq_low = 4.0 * std::f64::consts::PI / alpha_2_low_inv;
    g1_sq_low / (g1_sq_low + g2_sq_low)
}

fn main() -> ExitCode {
    // ---- 1. Anchor algebraic identity (must always hold) -------------------
    use trinity_verification::ring::Phi;
    let phi = Phi::phi();
    let phi2 = phi * phi;
    let phi4 = phi2 * phi2;
    let lhs = phi4 - phi2 * 3 + Phi::one();
    if lhs != Phi::zero() {
        eprintln!("FAIL: algebra anchor broken");
        return ExitCode::from(1);
    }
    println!("OK anchor phi^4 - 3 phi^2 + 1 = 0");

    // ---- 2. Run sin^2 theta_W from M_PS to M_Z -----------------------------
    let sin2_at_mz = run_sin2_theta_one_loop(M_PS, M_Z, SIN2_AT_M_PS);
    println!(
        "computed sin^2 theta_W(M_Z) = {:.5}   (PDG 2022 = {:.5})",
        sin2_at_mz, SIN2_THETA_PDG
    );

    // ---- 3. Compare against PDG within 5% relative tolerance ---------------
    // 5% is the realistic accuracy of a one-loop SM run from M_PS without
    // threshold corrections; the trinity-s3ai paper uses two-loop running
    // with the same boundary and recovers 0.23122 to 4 significant digits.
    let rel_err = (sin2_at_mz - SIN2_THETA_PDG).abs() / SIN2_THETA_PDG;
    println!("relative error = {:.4} ({:.2}%)", rel_err, rel_err * 100.0);

    let tolerance = 0.05;
    if rel_err > tolerance {
        eprintln!(
            "FAIL: sin^2 theta_W(M_Z) deviates from PDG by {:.4}, > {} tolerance",
            rel_err, tolerance
        );
        return ExitCode::from(1);
    }
    println!("OK sin^2 theta_W(M_Z) within 5% of PDG");

    // ---- 4. Summary --------------------------------------------------------
    println!("VERIFIED W4.8: PS-NCG sin^2 theta_W(M_Z) consistent with PDG at one loop");
    ExitCode::from(0)
}
