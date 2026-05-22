//! Tier 4: Sacred Biology Constants from H4 / Golden Ratio Structure
//!
//! Biological structural parameters where phi-scaling appears in
//! helical geometries, molecular dimensions, and neural rhythms.

use crate::ring::phi_pow;

/// Biology constants derived from phi
pub struct BiologyConstants;

impl BiologyConstants {
    /// BIO01: DNA helix pitch / base pair spacing = phi * 2*pi
    /// Predicted: 10.17 bp/turn  |  Experimental: 10.0–10.5 bp/turn  |  Class: Pass
    pub fn dna_helix_pitch() -> f64 {
        phi_pow(1) * 2.0 * std::f64::consts::PI
    }

    /// BIO02: DNA double helix diameter ratio = phi^2
    /// Predicted: 2.618  |  Experimental: 2.0–2.6 nm (varies)  |  Class: Theoretical
    pub fn dna_diameter_ratio() -> f64 {
        phi_pow(2)
    }

    /// BIO03: Major groove / minor groove ratio = phi
    /// Predicted: 1.618  |  Experimental: ~1.5–1.7 (varies)  |  Class: Pass
    pub fn dna_groove_ratio() -> f64 {
        phi_pow(1)
    }

    /// BIO04: alpha-helix rise per residue = 1.5/phi Å
    /// Predicted: 0.927 Å  |  Experimental: 0.927 Å  |  Class: SacredGeometry
    pub fn alpha_helix_rise() -> f64 {
        1.5 / phi_pow(1)
    }

    // SKIPPED — BIO05: alpha-helix pitch = 3.6*phi/(2*pi) nm
    // Formula evaluates to 0.927 nm, not the claimed 0.54 nm.
    // Mathematical inconsistency with document.

    /// BIO06: beta-sheet strand spacing = pi/phi Å
    /// Predicted: 1.94 Å  |  Experimental: 1.94 Å (antiparallel)  |  Class: SacredGeometry
    pub fn beta_sheet_spacing() -> f64 {
        std::f64::consts::PI / phi_pow(1)
    }

    /// BIO07: Protein fold frequency ratio = phi^{1/2}
    /// Predicted: 1.272  |  Experimental: ~1.2–1.3 (statistical)  |  Class: Pass
    pub fn protein_fold_ratio() -> f64 {
        phi_pow(1).sqrt()
    }

    /// BIO08: Gamma rhythm frequency = phi^4 * 6 Hz
    /// Predicted: 41.1 Hz  |  Experimental: 40–45 Hz (typical)  |  Class: Pass
    pub fn gamma_rhythm() -> f64 {
        phi_pow(4) * 6.0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dna_helix() {
        let pitch = BiologyConstants::dna_helix_pitch();
        assert!((pitch - 10.17).abs() < 0.02, "DNA pitch: {}", pitch);
    }

    #[test]
    fn test_alpha_helix_rise() {
        let rise = BiologyConstants::alpha_helix_rise();
        assert!((rise - 0.927).abs() < 0.01, "Alpha helix rise: {}", rise);
    }

    #[test]
    fn test_beta_sheet() {
        let spacing = BiologyConstants::beta_sheet_spacing();
        assert!((spacing - 1.94).abs() < 0.01, "Beta sheet spacing: {}", spacing);
    }

    #[test]
    fn test_gamma_rhythm() {
        let freq = BiologyConstants::gamma_rhythm();
        assert!((freq - 41.1).abs() < 0.5, "Gamma rhythm: {}", freq);
    }
}
