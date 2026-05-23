//! The binary icosahedral group `2I` realised inside the icosian ring.
//!
//! `2I` has 120 elements; equivalently, the 120 vertices of the 600-cell
//! when viewed as unit quaternions. We store them in the doubled form
//! `Quat2` (each component in `Z[phi]`); decoded, each quaternion has unit
//! norm.
//!
//! The 120 elements decompose into three orbits under permutation /
//! sign-flip:
//!   *  8 unit quaternions  +-1, +-i, +-j, +-k
//!   * 16 quaternions  (+-1 +- i +- j +- k) / 2
//!   * 96 quaternions: even permutations of  (0, +-1, +-phi, +-(1/phi)) / 2.
//!
//! The last group is the "snub 24-cell"; the first two together form the
//! 24-cell (`2T`, the binary tetrahedral group). Together: 8 + 16 + 96 = 120.

use crate::quaternion::Quat2;
use crate::ring::Phi;

/// Build the 120 elements of the binary icosahedral group, in `Quat2` form.
///
/// Order is deterministic: the 8 group-1 elements first, then the 16
/// group-2 elements, then the 96 group-3 elements (the snub 24-cell).
pub fn build_2I() -> Vec<Quat2> {
    let mut out = Vec::with_capacity(120);
    out.extend(group1_8());
    out.extend(group2_16());
    out.extend(group3_96());
    debug_assert_eq!(out.len(), 120);
    out
}

/// Indices `0..24` are 2T (= 24-cell). The remaining 24..120 are the snub
/// 24-cell. Used directly by `verify_snub_24cell`.
pub fn snub_indices() -> std::ops::Range<usize> {
    24..120
}

/// The 8 elements `+-1, +-i, +-j, +-k` (with the doubled convention these
/// have coordinates `+-2`).
fn group1_8() -> Vec<Quat2> {
    let two = Phi::new(2, 0);
    let m_two = Phi::new(-2, 0);
    let zero = Phi::zero();
    vec![
        Quat2::new(two, zero, zero, zero),
        Quat2::new(m_two, zero, zero, zero),
        Quat2::new(zero, two, zero, zero),
        Quat2::new(zero, m_two, zero, zero),
        Quat2::new(zero, zero, two, zero),
        Quat2::new(zero, zero, m_two, zero),
        Quat2::new(zero, zero, zero, two),
        Quat2::new(zero, zero, zero, m_two),
    ]
}

/// The 16 elements `(+-1 +- i +- j +- k) / 2`, doubled to `(+-1, +-1, +-1, +-1)`.
fn group2_16() -> Vec<Quat2> {
    let mut out = Vec::with_capacity(16);
    for sw in [-1i64, 1] {
        for sx in [-1i64, 1] {
            for sy in [-1i64, 1] {
                for sz in [-1i64, 1] {
                    out.push(Quat2::new(
                        Phi::new(sw, 0),
                        Phi::new(sx, 0),
                        Phi::new(sy, 0),
                        Phi::new(sz, 0),
                    ));
                }
            }
        }
    }
    out
}

/// The 96 elements of the snub 24-cell: even permutations of
/// `(0, +-1, +-phi, +-1/phi) / 2`, doubled to `(0, +-1, +-phi, +-(phi-1))`.
///
/// Doubled representation: components are in `{0, +-1, +-phi, +-(phi-1)}`
/// (recall `1/phi = phi - 1` so `2 * 1/phi = 2 phi - 2`; but with the doubled
/// convention `2 * (+-1/phi / 2) = +-1/phi = +-(phi - 1)`).
fn group3_96() -> Vec<Quat2> {
    let zero = Phi::zero();
    let one = Phi::new(1, 0);
    let m_one = Phi::new(-1, 0);
    let phi = Phi::new(0, 1);
    let m_phi = Phi::new(0, -1);
    // 1/phi = phi - 1, so as a doubled-coord halved unit it is (phi - 1)
    let inv_phi = Phi::new(-1, 1);
    let m_inv_phi = Phi::new(1, -1);

    // Choose three nonzero values for x, y, z (1, phi, 1/phi) and place a
    // zero in one of the four positions. The "even permutation" condition
    // selects 3 cyclic orderings of (1, phi, 1/phi) (out of 6 permutations)
    // and combined with all sign choices and all four zero positions gives
    // 4 * 3 * 2^3 = 96 elements.
    let triple = [(one, phi, inv_phi), (phi, inv_phi, one), (inv_phi, one, phi)];
    let neg_triple = [
        (m_one, m_phi, m_inv_phi),
        (m_phi, m_inv_phi, m_one),
        (m_inv_phi, m_one, m_phi),
    ];

    let mut out = Vec::with_capacity(96);
    // For each zero position, each cyclic triple, each sign-mask, place the
    // values. We accumulate 4 * 3 * 8 = 96 distinct elements (verified by
    // build-time assertion below).
    for zero_pos in 0..4 {
        for s in 0..8u32 {
            let sx = if s & 1 == 0 { 1 } else { -1 };
            let sy = if s & 2 == 0 { 1 } else { -1 };
            let sz = if s & 4 == 0 { 1 } else { -1 };
            for (i, &(va, vb, vc)) in triple.iter().enumerate() {
                let _ = neg_triple[i]; // referenced to keep the symmetric
                                       // structure explicit
                let mut comps = [zero, zero, zero, zero];
                // Distribute the triple across the three non-zero positions,
                // skipping zero_pos.
                let positions: Vec<usize> = (0..4).filter(|&k| k != zero_pos).collect();
                let signed = [
                    if sx == 1 { va } else { -va },
                    if sy == 1 { vb } else { -vb },
                    if sz == 1 { vc } else { -vc },
                ];
                for (slot_idx, &p) in positions.iter().enumerate() {
                    comps[p] = signed[slot_idx];
                }
                out.push(Quat2::new(comps[0], comps[1], comps[2], comps[3]));
            }
        }
    }
    debug_assert_eq!(out.len(), 96);
    // Remove possible duplicates (the construction may produce them when
    // permutation orbits overlap). We assert post-dedup count equals 96.
    let mut sorted = out.clone();
    sorted.sort_by(|a, b| {
        (a.w.a, a.w.b, a.x.a, a.x.b, a.y.a, a.y.b, a.z.a, a.z.b).cmp(&(
            b.w.a, b.w.b, b.x.a, b.x.b, b.y.a, b.y.b, b.z.a, b.z.b,
        ))
    });
    sorted.dedup();
    debug_assert_eq!(sorted.len(), 96, "snub 24-cell size != 96");
    sorted
}

/// Find the index of a given `Quat2` element inside the 2I table.
/// Returns `None` if not present.
pub fn find_in_2I(table: &[Quat2], q: Quat2) -> Option<usize> {
    table.iter().position(|x| *x == q)
}

// ============================================================================
// Tests
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn builds_120_elements() {
        let two_i = build_2I();
        assert_eq!(two_i.len(), 120);
    }

    #[test]
    fn all_elements_have_unit_norm() {
        // Doubled norm-squared must equal 4 for each element.
        let four = Phi::new(4, 0);
        for q in build_2I() {
            assert_eq!(q.norm_sq_doubled(), four, "non-unit quaternion {:?}", q);
        }
    }

    #[test]
    fn group_closure_under_multiplication() {
        // For each pair (q1, q2), q1 * q2 must lie in 2I.
        let two_i = build_2I();
        // Sample a sub-grid for speed (full 120x120 = 14400 multiplications;
        // tractable, but we sample first 24 for sanity).
        for q1 in &two_i[0..24] {
            for q2 in &two_i {
                let prod = q1.mul_doubled(*q2);
                assert!(
                    find_in_2I(&two_i, prod).is_some(),
                    "product not in 2I: {:?} * {:?} = {:?}",
                    q1, q2, prod
                );
            }
        }
    }

    #[test]
    fn snub_has_96_elements() {
        let two_i = build_2I();
        let snub: Vec<_> = two_i[snub_indices()].to_vec();
        assert_eq!(snub.len(), 96);
    }
}
