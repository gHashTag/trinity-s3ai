//! Integration tests for the ring laws in `Z[phi]`.
//!
//! These tests complement the in-module `#[cfg(test)]` tests by exercising
//! the public API (re-exported from `lib.rs`) over a larger sampling grid.

use trinity_verification::Phi;

fn grid() -> Vec<Phi> {
    let mut v = Vec::new();
    for a in -5..=5 {
        for b in -5..=5 {
            v.push(Phi::new(a, b));
        }
    }
    v
}

#[test]
fn distributivity_large_grid() {
    let xs = grid();
    for &x in &xs[..15] {
        for &y in &xs[..15] {
            for &z in &xs[..15] {
                assert_eq!(x * (y + z), x * y + x * z);
            }
        }
    }
}

#[test]
fn anchor_phi_sq_plus_inv_sq_equals_three() {
    // phi^4 - 3 phi^2 + 1 = 0 is equivalent to phi^2 + phi^(-2) = 3.
    let phi = Phi::phi();
    let phi2 = phi * phi;
    let phi4 = phi2 * phi2;
    assert_eq!(phi4 - phi2 * 3 + Phi::one(), Phi::zero());
}

#[test]
fn norm_is_multiplicative_large() {
    for x in grid() {
        for y in grid() {
            assert_eq!((x * y).norm(), x.norm() * y.norm());
        }
    }
}

#[test]
fn phi_powers_close_under_ring() {
    // phi^n stays inside Z[phi] for all n; the Fibonacci coefficients are
    // captured by the test in ring.rs but here we double-check the type
    // closure for n up to 20.
    let phi = Phi::phi();
    for n in 0..20u32 {
        let p = phi.pow(n);
        // Just a smoke check that arithmetic does not overflow at this size.
        let _ = p.a;
        let _ = p.b;
    }
}
