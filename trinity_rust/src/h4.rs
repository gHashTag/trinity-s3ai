//! H4 Coxeter Group and Root System
//!
//! H4 is the symmetry group of the 600-cell (and dual 120-cell).
//! Order: 14400 = 2^6 * 3^2 * 5^2
//! Rank: 4
//! Degrees: {2, 12, 20, 30}
//! Coxeter number: h = 30
//! Exponents: {1, 11, 19, 29}
//!
//! Key property: H4 is the ONLY finite reflection group where phi appears in roots.

use crate::ring::{Field, QSqrt5, Ring};

/// H4 group invariants
pub const H4_ORDER: u64 = 14400;
pub const H4_RANK: u32 = 4;
pub const H4_COXETER_NUMBER: u32 = 30;
pub const H4_ROOT_COUNT: u32 = 120;
pub const H4_REFLECTION_COUNT: u32 = 60;

/// H4 degrees (fundamental invariant degrees)
pub const H4_DEGREES: [u32; 4] = [2, 12, 20, 30];

/// H4 exponents
pub const H4_EXPONENTS: [u32; 4] = [1, 11, 19, 29];

/// Sum of degrees = 2 + 12 + 20 + 30 = 64
pub const H4_DEGREE_SUM: u32 = 64;

/// Product of degrees = 2 * 12 * 20 * 30 = 14400 = |H4|
pub const H4_DEGREE_PRODUCT: u64 = 14400;

/// Schlafli symbol for H4: {3, 3, 5}
pub const H4_SCHLAFLI: [u32; 3] = [3, 3, 5];

/// A root in the H4 root system (4D vector with coefficients in Q(phi))
#[derive(Clone, Debug, PartialEq)]
pub struct H4Root {
    pub coords: [QSqrt5; 4],
}

impl H4Root {
    pub fn new(c0: f64, c1: f64, c2: f64, c3: f64) -> Self {
        H4Root {
            coords: [
                QSqrt5::new(c0, 0.0),
                QSqrt5::new(c1, 0.0),
                QSqrt5::new(c2, 0.0),
                QSqrt5::new(c3, 0.0),
            ],
        }
    }

    pub fn new_phi(
        c0_a: f64,
        c0_b: f64,
        c1_a: f64,
        c1_b: f64,
        c2_a: f64,
        c2_b: f64,
        c3_a: f64,
        c3_b: f64,
    ) -> Self {
        H4Root {
            coords: [
                QSqrt5::new(c0_a, c0_b),
                QSqrt5::new(c1_a, c1_b),
                QSqrt5::new(c2_a, c2_b),
                QSqrt5::new(c3_a, c3_b),
            ],
        }
    }

    /// Evaluate to floating point coordinates
    pub fn eval(&self) -> [f64; 4] {
        [
            self.coords[0].eval(),
            self.coords[1].eval(),
            self.coords[2].eval(),
            self.coords[3].eval(),
        ]
    }

    /// Norm squared of the root
    pub fn norm_sq(&self) -> QSqrt5 {
        let mut sum = QSqrt5::zero();
        for c in &self.coords {
            let sq = c.clone() * c.clone();
            sum = sum + sq;
        }
        sum
    }

    /// Check if `other` belongs to the H4 root system.
    pub fn is_root(&self, other: &H4Root) -> bool {
        generate_h4_roots().contains(other)
    }
}

/// Generate the 120 roots of H4
///
/// The 120 roots consist of:
/// - 8 roots: permutations of (±2, 0, 0, 0)
/// - 16 roots: all sign combinations of (±1, ±1, ±1, ±1)
/// - 96 roots: even permutations of (±phi, ±1, ±1/phi, 0)
pub fn generate_h4_roots() -> Vec<H4Root> {
    let mut roots = Vec::with_capacity(120);
    let phi = QSqrt5::phi();
    let phi_inv = phi.inv().unwrap(); // 1/phi = phi - 1

    // Type 1: (±2, 0, 0, 0) and permutations — 8 roots
    for i in 0..4 {
        for sign in [-1.0f64, 1.0] {
            let mut coords = [QSqrt5::zero(); 4];
            coords[i] = QSqrt5::new(2.0 * sign, 0.0);
            roots.push(H4Root { coords });
        }
    }

    // Type 2: (±1, ±1, ±1, ±1) — 16 roots
    for a in [-1.0f64, 1.0] {
        for b in [-1.0f64, 1.0] {
            for c in [-1.0f64, 1.0] {
                for d in [-1.0f64, 1.0] {
                    roots.push(H4Root {
                        coords: [
                            QSqrt5::new(a, 0.0),
                            QSqrt5::new(b, 0.0),
                            QSqrt5::new(c, 0.0),
                            QSqrt5::new(d, 0.0),
                        ],
                    });
                }
            }
        }
    }

    // Type 3: even permutations of (±phi, ±1, ±1/phi, 0) — 96 roots
    let even_perms: [[usize; 4]; 12] = [
        [0, 1, 2, 3],
        [1, 0, 3, 2],
        [2, 3, 0, 1],
        [3, 2, 1, 0],
        [2, 0, 1, 3],
        [1, 2, 0, 3],
        [3, 0, 2, 1],
        [1, 3, 2, 0],
        [2, 1, 3, 0],
        [3, 1, 0, 2],
        [0, 3, 1, 2],
        [0, 2, 3, 1],
    ];

    for s_phi in [-1.0f64, 1.0] {
        let phi_signed = phi * QSqrt5::new(s_phi, 0.0);
        for s1 in [-1.0f64, 1.0] {
            for s_inv in [-1.0f64, 1.0] {
                let inv_signed = phi_inv * QSqrt5::new(s_inv, 0.0);
                let base = [phi_signed, QSqrt5::new(s1, 0.0), inv_signed, QSqrt5::zero()];
                for perm in &even_perms {
                    roots.push(H4Root {
                        coords: [base[perm[0]], base[perm[1]], base[perm[2]], base[perm[3]]],
                    });
                }
            }
        }
    }

    roots
}

/// Reflection subgroup types of H4
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum H4Subgroup {
    Empty,
    A1,      // Order 2 — SU(2)_L
    A2,      // Order 6 — SU(3)_C
    I2_5,    // Order 10 — H2 dihedral
    A1A2,    // Order 12 — SU(2) x SU(3)
    A3,      // Order 24 — SU(4)
    H3,      // Order 120 — icosahedral
    H4,      // Order 14400 — full group
    A2A2,    // Order 36 — SU(3) x SU(3)
    D4,      // Order 192 — SO(8)
    A4,      // Order 120 — SU(5) GUT
    H3A1,    // Order 240 — extended icosahedral
    I2_5Sq, // Order 100 — H2 x H2
    A3A1,    // Order 8
    A4A1,    // Order 16
}

impl H4Subgroup {
    pub fn order(&self) -> u32 {
        match self {
            H4Subgroup::Empty => 1,
            H4Subgroup::A1 => 2,
            H4Subgroup::A2 => 6,
            H4Subgroup::I2_5 => 10,
            H4Subgroup::A1A2 => 12,
            H4Subgroup::A3 => 24,
            H4Subgroup::H3 => 120,
            H4Subgroup::H4 => 14400,
            H4Subgroup::A2A2 => 36,
            H4Subgroup::D4 => 192,
            H4Subgroup::A4 => 120,
            H4Subgroup::H3A1 => 240,
            H4Subgroup::I2_5Sq => 100,
            H4Subgroup::A3A1 => 8,
            H4Subgroup::A4A1 => 16,
        }
    }

    pub fn rank(&self) -> u32 {
        match self {
            H4Subgroup::Empty => 0,
            H4Subgroup::A1 => 1,
            H4Subgroup::A2 => 2,
            H4Subgroup::I2_5 => 2,
            H4Subgroup::A1A2 => 3,
            H4Subgroup::A3 => 3,
            H4Subgroup::H3 => 3,
            H4Subgroup::H4 => 4,
            H4Subgroup::A2A2 => 4,
            H4Subgroup::D4 => 4,
            H4Subgroup::A4 => 4,
            H4Subgroup::H3A1 => 4,
            H4Subgroup::I2_5Sq => 4,
            H4Subgroup::A3A1 => 3,
            H4Subgroup::A4A1 => 4,
        }
    }

    pub fn coxeter_number(&self) -> u32 {
        match self {
            H4Subgroup::Empty => 0,
            H4Subgroup::A1 => 2,
            H4Subgroup::A2 => 3,
            H4Subgroup::I2_5 => 5,
            H4Subgroup::A1A2 => 6, // lcm(2,3)
            H4Subgroup::A3 => 4,
            H4Subgroup::H3 => 10,
            H4Subgroup::H4 => 30,
            H4Subgroup::A2A2 => 6,
            H4Subgroup::D4 => 6,
            H4Subgroup::A4 => 5,
            H4Subgroup::H3A1 => 10,
            H4Subgroup::I2_5Sq => 5,
            H4Subgroup::A3A1 => 4,
            H4Subgroup::A4A1 => 5,
        }
    }

    /// Standard Model gauge group connection
    pub fn sm_connection(&self) -> &'static str {
        match self {
            H4Subgroup::Empty => "Trivial",
            H4Subgroup::A1 => "SU(2)_L (weak isospin)",
            H4Subgroup::A2 => "SU(3)_C (color)",
            H4Subgroup::I2_5 => "H2 dihedral (non-crystallographic)",
            H4Subgroup::A1A2 => "SU(2)_L x SU(3)_C (partial SM)",
            H4Subgroup::A3 => "SU(4) (Pati-Salam precursor)",
            H4Subgroup::H3 => "Icosahedral symmetry",
            H4Subgroup::H4 => "Full H4 (unified)",
            H4Subgroup::A2A2 => "SU(3) x SU(3) (Trinity intermediate)",
            H4Subgroup::D4 => "SO(8) (triality)",
            H4Subgroup::A4 => "SU(5) GUT",
            H4Subgroup::H3A1 => "Extended icosahedral",
            H4Subgroup::I2_5Sq => "H2 x H2",
            H4Subgroup::A3A1 => "Subgroup",
            H4Subgroup::A4A1 => "Subgroup",
        }
    }
}

/// Maximal subgroups of H4
pub fn maximal_subgroups() -> Vec<(u32, &'static str, &'static str)> {
    vec![
        (144, "W(A2 x A2) semidirect Z4", "SU(3) x SU(3) extension"),
        (240, "W(H3) x Z2", "Icosahedral x Z2"),
        (400, "[W(H2) x W(H2)] semidirect Z4", "Non-crystallographic"),
        (576, "Extension of W(SO(8))", "SO(8) extension"),
    ]
}

/// The SM gauge group derivation chain: H4 -> A2^2 -> A2 x A1 -> A1 x A1 -> SM
pub fn sm_derivation_chain() -> Vec<(&'static str, &'static str)> {
    vec![
        ("H4 (order 14400, rank 4)", "Full exceptional group"),
        ("A2 x A2 (order 36, rank 4)", "SU(3) x SU(3) intermediate"),
        ("A2 x A1 (order 12, rank 3)", "SU(3) x SU(2) partial"),
        ("SU(3)_C x SU(2)_L x U(1)_Y", "Standard Model gauge group"),
    ]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_h4_invariants() {
        assert_eq!(H4_ORDER, 14400);
        assert_eq!(H4_RANK, 4);
        assert_eq!(H4_COXETER_NUMBER, 30);
        assert_eq!(H4_ROOT_COUNT, 120);
    }

    #[test]
    fn test_subgroup_orders() {
        assert_eq!(H4Subgroup::A1.order(), 2);
        assert_eq!(H4Subgroup::A2.order(), 6);
        assert_eq!(H4Subgroup::A2A2.order(), 36);
        assert_eq!(H4Subgroup::A4.order(), 120);
        assert_eq!(H4Subgroup::H4.order(), 14400);
    }

    #[test]
    fn test_generate_roots() {
        let roots = generate_h4_roots();
        assert_eq!(
            roots.len(),
            120,
            "Expected exactly 120 roots, got {}",
            roots.len()
        );

        // Verify uniqueness (no duplicates generated)
        let mut unique = roots.clone();
        unique.sort_by(|a, b| {
            let ae = a.eval();
            let be = b.eval();
            ae[0]
                .partial_cmp(&be[0])
                .unwrap()
                .then_with(|| ae[1].partial_cmp(&be[1]).unwrap())
                .then_with(|| ae[2].partial_cmp(&be[2]).unwrap())
                .then_with(|| ae[3].partial_cmp(&be[3]).unwrap())
        });
        unique.dedup_by(|a, b| a == b);
        assert_eq!(
            unique.len(),
            120,
            "Expected 120 unique roots, found duplicates"
        );
    }
}
