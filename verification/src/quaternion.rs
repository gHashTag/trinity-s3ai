//! Quaternions with coordinates in `Z[phi]`.
//!
//! We never store half-integer coordinates directly. Instead, every
//! quaternion `q = w + x i + y j + z k` of the binary icosahedral group `2I`
//! is stored as `Quat2 = 2 * q`, i.e. with each component in `Z[phi]`.
//!
//! Multiplication then satisfies
//!     `Quat2(q_1) * Quat2(q_2) = 2 * Quat2(q_1 q_2)`
//! so the doubled product is divisible by 2. The division-by-2 is exact
//! on `2I` and is performed by halving each component (checked by an
//! assertion in debug builds).

use crate::ring::Phi;

/// A quaternion with coefficients in `Z[phi]`, representing twice a
/// "physical" quaternion. Components are `2 w`, `2 x`, `2 y`, `2 z`.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct Quat2 {
    pub w: Phi,
    pub x: Phi,
    pub y: Phi,
    pub z: Phi,
}

impl Quat2 {
    /// Construct from the four doubled-coordinate `Z[phi]` components.
    pub const fn new(w: Phi, x: Phi, y: Phi, z: Phi) -> Self {
        Quat2 { w, x, y, z }
    }

    /// The doubled identity quaternion `2 = (2, 0, 0, 0)`.
    pub const fn identity_2() -> Self {
        Quat2 {
            w: Phi::new(2, 0),
            x: Phi::zero(),
            y: Phi::zero(),
            z: Phi::zero(),
        }
    }

    /// The doubled `-1` element.
    pub const fn neg_identity_2() -> Self {
        Quat2 {
            w: Phi::new(-2, 0),
            x: Phi::zero(),
            y: Phi::zero(),
            z: Phi::zero(),
        }
    }

    /// Quaternionic conjugation: `q -> w - x i - y j - z k`.
    pub fn conjugate(self) -> Self {
        Quat2 {
            w: self.w,
            x: -self.x,
            y: -self.y,
            z: -self.z,
        }
    }

    /// Quaternion product of two *doubled* quaternions, **returned doubled**.
    /// Internally computes `4 * (q_1 q_2)`, which is divisible by 2 when both
    /// inputs come from `2I`. We halve componentwise and assert exactness.
    pub fn mul_doubled(self, rhs: Self) -> Self {
        // Compute 4 * (q1 * q2) coordinatewise using the Hamilton rules
        // (i^2 = j^2 = k^2 = ijk = -1).
        let a1 = self.w;
        let b1 = self.x;
        let c1 = self.y;
        let d1 = self.z;
        let a2 = rhs.w;
        let b2 = rhs.x;
        let c2 = rhs.y;
        let d2 = rhs.z;
        let prod_w = a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2;
        let prod_x = a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2;
        let prod_y = a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2;
        let prod_z = a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2;
        // Each component is now 4 times the corresponding component of q1*q2;
        // dividing by 2 gives twice the component, which is the doubled
        // representation we want.
        Quat2 {
            w: half(prod_w),
            x: half(prod_x),
            y: half(prod_y),
            z: half(prod_z),
        }
    }

    /// Componentwise negation.
    pub fn neg(self) -> Self {
        Quat2 {
            w: -self.w,
            x: -self.x,
            y: -self.y,
            z: -self.z,
        }
    }

    /// Squared norm `|q|^2 = w^2 + x^2 + y^2 + z^2`, as an element of `Z[phi]`,
    /// computed on the doubled representation. The result is therefore
    /// `4 |q|^2`. For elements of `2I`, `|q| = 1` so this returns the doubled
    /// representation of `4`, i.e. `Phi::new(4, 0)`.
    pub fn norm_sq_doubled(self) -> Phi {
        self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z
    }
}

/// Halve a `Phi` element. Panics in debug builds if it is not exactly halvable.
#[inline]
fn half(p: Phi) -> Phi {
    debug_assert!(
        p.a.rem_euclid(2) == 0 && p.b.rem_euclid(2) == 0,
        "Phi value {:?} is not divisible by 2",
        p
    );
    Phi::new(p.a / 2, p.b / 2)
}

// ============================================================================
// Tests
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn identity_squares_to_identity() {
        let id = Quat2::identity_2();
        let prod = id.mul_doubled(id);
        assert_eq!(prod, id);
    }

    #[test]
    fn neg_identity_squares_to_identity() {
        let nid = Quat2::neg_identity_2();
        let id = Quat2::identity_2();
        assert_eq!(nid.mul_doubled(nid), id);
    }

    #[test]
    fn i_squares_to_minus_one() {
        // 2 i  =  (0, 2, 0, 0)
        let two_i = Quat2::new(Phi::zero(), Phi::new(2, 0), Phi::zero(), Phi::zero());
        let prod = two_i.mul_doubled(two_i);
        assert_eq!(prod, Quat2::neg_identity_2());
    }

    #[test]
    fn j_squares_to_minus_one() {
        let two_j = Quat2::new(Phi::zero(), Phi::zero(), Phi::new(2, 0), Phi::zero());
        let prod = two_j.mul_doubled(two_j);
        assert_eq!(prod, Quat2::neg_identity_2());
    }

    #[test]
    fn k_squares_to_minus_one() {
        let two_k = Quat2::new(Phi::zero(), Phi::zero(), Phi::zero(), Phi::new(2, 0));
        let prod = two_k.mul_doubled(two_k);
        assert_eq!(prod, Quat2::neg_identity_2());
    }

    #[test]
    fn ij_equals_k() {
        let two_i = Quat2::new(Phi::zero(), Phi::new(2, 0), Phi::zero(), Phi::zero());
        let two_j = Quat2::new(Phi::zero(), Phi::zero(), Phi::new(2, 0), Phi::zero());
        let two_k = Quat2::new(Phi::zero(), Phi::zero(), Phi::zero(), Phi::new(2, 0));
        assert_eq!(two_i.mul_doubled(two_j), two_k);
    }

    #[test]
    fn norm_of_identity_is_four() {
        let id = Quat2::identity_2();
        assert_eq!(id.norm_sq_doubled(), Phi::new(4, 0));
    }
}
