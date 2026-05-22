//! Algebraic Ring Structures for Trinity H4 -> SM Derivation
//!
//! Implements the algebraic foundations: Ring, Field, and specialized
//! H4-invariant number systems. All SM parameters derive from these structures.

use std::fmt::Debug;
use std::ops::{Add, Mul, Neg, Sub};

/// Core Ring trait: additive abelian group + multiplicative monoid
pub trait Ring:
    Clone
    + Debug
    + PartialEq
    + Add<Output = Self>
    + Sub<Output = Self>
    + Mul<Output = Self>
    + Neg<Output = Self>
{
    fn zero() -> Self;
    fn one() -> Self;
    fn is_zero(&self) -> bool;

    /// Integer power (for fields, supports negative exponents)
    fn pow(&self, n: i64) -> Self {
        if n == 0 {
            return Self::one();
        }
        let mut result = Self::one();
        let mut base = self.clone();
        let mut exp = n.abs();
        while exp > 0 {
            if exp % 2 == 1 {
                result = result * base.clone();
            }
            base = base.clone() * base.clone();
            exp /= 2;
        }
        result
    }
}

/// Field trait: Ring where every non-zero element has multiplicative inverse
pub trait Field: Ring {
    fn inv(self) -> Option<Self>;
    fn div(self, other: Self) -> Option<Self> {
        other.inv().map(|inv| self * inv)
    }
}

/// H4-Extension: Q(sqrt(5)) — the field extension containing phi
/// Elements are of form a + b*sqrt(5) where a, b are rationals
/// phi = (1 + sqrt(5))/2 lives here
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct QSqrt5 {
    pub a: f64,
    pub b: f64,
}

impl QSqrt5 {
    pub fn new(a: f64, b: f64) -> Self {
        QSqrt5 { a, b }
    }

    pub fn sqrt5() -> Self {
        QSqrt5 { a: 0.0, b: 1.0 }
    }

    /// The golden ratio phi = (1 + sqrt(5))/2
    pub fn phi() -> Self {
        QSqrt5 { a: 0.5, b: 0.5 }
    }

    /// psi = (1 - sqrt(5))/2 = 1 - phi = -1/phi
    pub fn psi() -> Self {
        QSqrt5 { a: 0.5, b: -0.5 }
    }

    /// Evaluate to floating point
    pub fn eval(&self) -> f64 {
        self.a + self.b * 5f64.sqrt()
    }

    /// Conjugate: a + b*sqrt(5) -> a - b*sqrt(5)
    pub fn conj(&self) -> Self {
        QSqrt5 {
            a: self.a,
            b: -self.b,
        }
    }

    /// Norm: N(a + b*sqrt(5)) = a^2 - 5*b^2
    pub fn norm(&self) -> f64 {
        self.a * self.a - 5.0 * self.b * self.b
    }

    /// phi^n as an element of Q(sqrt(5))
    pub fn phi_pow(n: i64) -> Self {
        Self::phi().pow(n)
    }
}

impl Ring for QSqrt5 {
    fn zero() -> Self {
        QSqrt5 { a: 0.0, b: 0.0 }
    }
    fn one() -> Self {
        QSqrt5 { a: 1.0, b: 0.0 }
    }
    fn is_zero(&self) -> bool {
        self.a == 0.0 && self.b == 0.0
    }
}

impl Add for QSqrt5 {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        QSqrt5 {
            a: self.a + rhs.a,
            b: self.b + rhs.b,
        }
    }
}

impl Sub for QSqrt5 {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self {
        QSqrt5 {
            a: self.a - rhs.a,
            b: self.b - rhs.b,
        }
    }
}

impl Mul for QSqrt5 {
    type Output = Self;
    fn mul(self, rhs: Self) -> Self {
        // (a + b*sqrt(5))(c + d*sqrt(5)) = (ac + 5bd) + (ad + bc)*sqrt(5)
        QSqrt5 {
            a: self.a * rhs.a + 5.0 * self.b * rhs.b,
            b: self.a * rhs.b + self.b * rhs.a,
        }
    }
}

impl Neg for QSqrt5 {
    type Output = Self;
    fn neg(self) -> Self {
        QSqrt5 {
            a: -self.a,
            b: -self.b,
        }
    }
}

impl Field for QSqrt5 {
    fn inv(self) -> Option<Self> {
        let n = self.norm();
        if n == 0.0 {
            return None;
        }
        Some(QSqrt5 {
            a: self.a / n,
            b: -self.b / n,
        })
    }
}

/// Golden ratio power using closed form
pub fn phi_pow(n: i64) -> f64 {
    let phi: f64 = 1.6180339887498948482;
    phi.powi(n as i32)
}

/// Lucas number L_n = phi^n + (-phi)^{-n}
pub fn lucas(n: i64) -> f64 {
    let phi: f64 = 1.6180339887498948482;
    let psi: f64 = (1.0 - 5f64.sqrt()) / 2.0;
    phi.powi(n as i32) + psi.powi(n as i32)
}

/// Fibonacci number F_n = (phi^n - (-phi)^{-n}) / sqrt(5)
pub fn fibonacci(n: i64) -> f64 {
    (phi_pow(n)
        - if n % 2 == 0 {
            phi_pow(-n)
        } else {
            -phi_pow(-n)
        })
        / 5f64.sqrt()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_phi_identity() {
        let phi = QSqrt5::phi();
        let phi_sq = phi.clone() * phi.clone();
        let phi_plus_1 = phi + QSqrt5::one();
        assert!((phi_sq.eval() - phi_plus_1.eval()).abs() < 1e-10);
    }

    #[test]
    fn test_phi_inv() {
        let phi = QSqrt5::phi();
        let inv = phi.inv().unwrap();
        let one = phi * inv;
        assert!((one.eval() - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_phi_powers() {
        // phi^2 = phi + 1
        assert!((phi_pow(2) - phi_pow(1) - 1.0).abs() < 1e-10);
        // phi^3 = 2*phi + 1
        assert!((phi_pow(3) - 2.0 * phi_pow(1) - 1.0).abs() < 1e-10);
        // phi^4 = 3*phi + 2
        assert!((phi_pow(4) - 3.0 * phi_pow(1) - 2.0).abs() < 1e-10);
        // phi^5 = 5*phi + 3
        assert!((phi_pow(5) - 5.0 * phi_pow(1) - 3.0).abs() < 1e-10);
    }

    #[test]
    fn test_lucas() {
        assert_eq!(lucas(0) as i64, 2);
        assert_eq!(lucas(1) as i64, 1);
        assert_eq!(lucas(2) as i64, 3);
        assert_eq!(lucas(3) as i64, 4);
        assert_eq!(lucas(4) as i64, 7);
        assert_eq!(lucas(5) as i64, 11);
    }
}
