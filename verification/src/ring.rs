//! Exact arithmetic on the golden-ratio ring `Z[phi]`.
//!
//! Elements are pairs `(a, b)` representing `a + b*phi`. Multiplication
//! uses the defining relation `phi^2 = phi + 1`, which makes the ring
//! closed under multiplication while keeping coefficients in `i64`.
//!
//! This is the *anchor* algebra of trinity-s3ai: every exact identity
//! that hinges on `phi^2 + phi^(-2) = 3` is checked here.

use std::ops::{Add, Mul, Neg, Sub};

/// An element `a + b*phi` of `Z[phi]` (a.k.a. the ring of integers of `Q(sqrt 5)`).
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct Phi {
    pub a: i64,
    pub b: i64,
}

impl Phi {
    /// Construct `a + b*phi`.
    #[inline]
    pub const fn new(a: i64, b: i64) -> Self {
        Phi { a, b }
    }

    /// The zero element.
    #[inline]
    pub const fn zero() -> Self {
        Phi { a: 0, b: 0 }
    }

    /// The multiplicative identity.
    #[inline]
    pub const fn one() -> Self {
        Phi { a: 1, b: 0 }
    }

    /// The generator `phi`.
    #[inline]
    pub const fn phi() -> Self {
        Phi { a: 0, b: 1 }
    }

    /// The conjugate root `psi = 1 - phi` (also denoted `phi^{-1} * (-1)`).
    /// In the algebraic-conjugation sense, `Phi { a, b }` conjugates to
    /// `Phi { a + b, -b }` because `psi = 1 - phi` so substituting
    /// `phi -> 1 - phi` sends `a + b*phi -> (a + b) - b*phi`.
    #[inline]
    pub const fn conj(self) -> Self {
        Phi {
            a: self.a + self.b,
            b: -self.b,
        }
    }

    /// Norm form `N(a + b phi) = (a + b phi)(a + b psi) = a^2 + a b - b^2`.
    ///
    /// Equivalently, `N(x) = x * x.conj()` projected onto the integer axis.
    #[inline]
    pub const fn norm(self) -> i64 {
        self.a * self.a + self.a * self.b - self.b * self.b
    }

    /// Is this the zero element?
    #[inline]
    pub const fn is_zero(self) -> bool {
        self.a == 0 && self.b == 0
    }

    /// Evaluate to `f64`. Only for printing — never used for ring decisions.
    pub fn to_f64(self) -> f64 {
        let golden = (1.0 + 5.0f64.sqrt()) / 2.0;
        (self.a as f64) + (self.b as f64) * golden
    }

    /// Non-negative integer power. For exponent zero returns `one`.
    pub fn pow(self, n: u32) -> Self {
        let mut acc = Self::one();
        let mut base = self;
        let mut k = n;
        while k > 0 {
            if k & 1 == 1 {
                acc = acc * base;
            }
            base = base * base;
            k >>= 1;
        }
        acc
    }
}

impl Add for Phi {
    type Output = Self;
    #[inline]
    fn add(self, rhs: Self) -> Self {
        Phi {
            a: self.a + rhs.a,
            b: self.b + rhs.b,
        }
    }
}

impl Sub for Phi {
    type Output = Self;
    #[inline]
    fn sub(self, rhs: Self) -> Self {
        Phi {
            a: self.a - rhs.a,
            b: self.b - rhs.b,
        }
    }
}

impl Neg for Phi {
    type Output = Self;
    #[inline]
    fn neg(self) -> Self {
        Phi {
            a: -self.a,
            b: -self.b,
        }
    }
}

impl Mul for Phi {
    type Output = Self;
    #[inline]
    fn mul(self, rhs: Self) -> Self {
        // (a1 + b1 phi)(a2 + b2 phi)
        //   = a1 a2 + (a1 b2 + a2 b1) phi + b1 b2 phi^2
        //   = a1 a2 + b1 b2 + (a1 b2 + a2 b1 + b1 b2) phi    [phi^2 = phi + 1]
        Phi {
            a: self.a * rhs.a + self.b * rhs.b,
            b: self.a * rhs.b + self.b * rhs.a + self.b * rhs.b,
        }
    }
}

impl Mul<i64> for Phi {
    type Output = Self;
    #[inline]
    fn mul(self, k: i64) -> Self {
        Phi {
            a: self.a * k,
            b: self.b * k,
        }
    }
}

// ============================================================================
// Tests for the ring laws.
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    fn samples() -> Vec<Phi> {
        let mut v = Vec::new();
        for a in -3..=3i64 {
            for b in -3..=3i64 {
                v.push(Phi::new(a, b));
            }
        }
        v
    }

    #[test]
    fn add_is_associative() {
        let xs = samples();
        for &x in &xs {
            for &y in &xs {
                for &z in &xs {
                    assert_eq!((x + y) + z, x + (y + z));
                }
            }
        }
    }

    #[test]
    fn add_is_commutative() {
        let xs = samples();
        for &x in &xs {
            for &y in &xs {
                assert_eq!(x + y, y + x);
            }
        }
    }

    #[test]
    fn add_zero_is_identity() {
        for x in samples() {
            assert_eq!(x + Phi::zero(), x);
        }
    }

    #[test]
    fn add_inverse_is_neg() {
        for x in samples() {
            assert_eq!(x + (-x), Phi::zero());
        }
    }

    #[test]
    fn mul_is_associative() {
        let xs = samples();
        for &x in &xs {
            for &y in &xs {
                for &z in &xs {
                    assert_eq!((x * y) * z, x * (y * z));
                }
            }
        }
    }

    #[test]
    fn mul_is_commutative() {
        let xs = samples();
        for &x in &xs {
            for &y in &xs {
                assert_eq!(x * y, y * x);
            }
        }
    }

    #[test]
    fn mul_one_is_identity() {
        for x in samples() {
            assert_eq!(x * Phi::one(), x);
            assert_eq!(Phi::one() * x, x);
        }
    }

    #[test]
    fn distributivity() {
        let xs = samples();
        for &x in &xs {
            for &y in &xs {
                for &z in &xs {
                    assert_eq!(x * (y + z), x * y + x * z);
                }
            }
        }
    }

    #[test]
    fn golden_equation() {
        // phi^2 = phi + 1
        let phi = Phi::phi();
        assert_eq!(phi * phi, phi + Phi::one());
    }

    #[test]
    fn phi_sq_plus_phi_minus_two_equals_three() {
        // The anchor identity: phi^2 + phi^(-2) = 3.
        // phi^(-2) is not in Z[phi], so we verify
        // phi^2 * phi^(-2) = 1 and phi^2 + 1/phi^2 = 3 via
        //   phi^2 = phi + 1
        //   1/phi^2 = 1/(phi + 1) = (phi - 1)/phi^2 ... continued numerically.
        // Exact form: phi^2 + phi^(-2) = 3  iff  phi^4 - 3 phi^2 + 1 = 0.
        // Verify the polynomial identity in Z[phi].
        let phi = Phi::phi();
        let phi2 = phi * phi;
        let phi4 = phi2 * phi2;
        // phi^4 - 3 phi^2 + 1
        let lhs = phi4 - phi2 * 3 + Phi::one();
        assert_eq!(lhs, Phi::zero(), "anchor phi^4 - 3 phi^2 + 1 = 0 failed");
    }

    #[test]
    fn norm_is_multiplicative() {
        let xs = samples();
        for &x in &xs {
            for &y in &xs {
                assert_eq!((x * y).norm(), x.norm() * y.norm(), "N(xy) != N(x) N(y)");
            }
        }
    }

    #[test]
    fn conjugation_is_involution() {
        for x in samples() {
            assert_eq!(x.conj().conj(), x);
        }
    }

    #[test]
    fn fibonacci_pattern_in_powers() {
        // phi^n = F_n * phi + F_{n-1}, with F_0 = 0, F_1 = 1, F_2 = 1, ...
        let phi = Phi::phi();
        let fibs: [i64; 12] = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89];
        for n in 1..fibs.len() - 1 {
            let lhs = phi.pow(n as u32);
            let rhs = Phi::new(fibs[n - 1], fibs[n]);
            assert_eq!(lhs, rhs, "phi^{} mismatch", n);
        }
    }
}
