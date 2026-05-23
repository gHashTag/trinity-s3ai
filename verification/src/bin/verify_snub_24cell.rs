//! `verify_snub_24cell` — Wave 4 W4.2.
//!
//! Replaces `wave4_snub_24cell.py`. Confirms exactly (in `Z[phi]`) that:
//!   * The snub 24-cell has 96 vertices (= 600-cell minus 24-cell).
//!   * A chosen Z_3 subgroup of 2T acts freely on the 96 vertices by
//!     left quaternionic multiplication.
//!   * The 96 vertices split into 32 orbits of size 3, giving a canonical
//!     3-partition  snub_96 = G_0 ⊔ G_1 ⊔ G_2  with |G_i| = 32.
//!
//! Exit code: 0 on success, 1 on any failure.
//! Output is byte-stable: same input -> same bytes (no timestamps, no
//! floating point, all decisions over `Z[phi]`).

use std::process::ExitCode;
use trinity_verification::icosian::{build_2I, find_in_2I, snub_indices};
use trinity_verification::quaternion::Quat2;
use trinity_verification::ring::Phi;

fn main() -> ExitCode {
    let two_i = build_2I();

    // ---- 1. 2I has 120 elements --------------------------------------------
    if two_i.len() != 120 {
        eprintln!("FAIL: |2I| = {}, expected 120", two_i.len());
        return ExitCode::from(1);
    }
    println!("OK |2I| = 120");

    // ---- 2. snub = 96 vertices ---------------------------------------------
    let snub: Vec<Quat2> = two_i[snub_indices()].to_vec();
    if snub.len() != 96 {
        eprintln!("FAIL: |snub| = {}, expected 96", snub.len());
        return ExitCode::from(1);
    }
    println!("OK |snub| = 96");

    // ---- 3. Pick a Z_3 generator inside 2T ---------------------------------
    // Conway-Sloan: g = (-1/2, 1/2, 1/2, 1/2) is an order-3 element of 2T.
    // Doubled: (-1, 1, 1, 1). It lives in group2_16 (the (+-1 +- i +- j +- k)/2
    // family) and is therefore at some index < 24.
    let g = Quat2::new(Phi::new(-1, 0), Phi::new(1, 0), Phi::new(1, 0), Phi::new(1, 0));
    let g_idx = match find_in_2I(&two_i, g) {
        Some(i) => i,
        None => {
            eprintln!("FAIL: generator g not in 2I");
            return ExitCode::from(1);
        }
    };
    if !(g_idx < 24) {
        eprintln!("FAIL: generator g not in 2T (index {} >= 24)", g_idx);
        return ExitCode::from(1);
    }
    println!("OK g in 2T at index {}", g_idx);

    // ---- 4. g has order 3 --------------------------------------------------
    let g2 = g.mul_doubled(g);
    let g3 = g2.mul_doubled(g);
    let id = Quat2::identity_2();
    if g3 != id {
        eprintln!("FAIL: g^3 != identity, got {:?}", g3);
        return ExitCode::from(1);
    }
    if g == id || g2 == id {
        eprintln!("FAIL: g has order < 3");
        return ExitCode::from(1);
    }
    println!("OK g has order 3");

    // ---- 5. g acts freely on snub_96 (no fixed points) ---------------------
    // For each v in snub, check g * v != v.
    for v in &snub {
        let gv = g.mul_doubled(*v);
        if gv == *v {
            eprintln!("FAIL: g has fixed point in snub: {:?}", v);
            return ExitCode::from(1);
        }
    }
    println!("OK g acts freely on snub (no fixed points)");

    // ---- 6. Build the 32 orbits --------------------------------------------
    // For each vertex, the orbit is {v, g*v, g^2*v}. We pick the orbit
    // representative as the vertex with the smallest snub-index in the orbit.
    let mut orbit_of: Vec<usize> = vec![usize::MAX; 96];
    let mut representatives: Vec<usize> = Vec::new();
    for (i, v) in snub.iter().enumerate() {
        if orbit_of[i] != usize::MAX {
            continue;
        }
        let orbit_id = representatives.len();
        representatives.push(i);
        let mut current = *v;
        for _ in 0..3 {
            // Map current back to its snub-index.
            let snub_idx = snub
                .iter()
                .position(|x| *x == current)
                .expect("orbit element not in snub");
            orbit_of[snub_idx] = orbit_id;
            current = g.mul_doubled(current);
        }
    }
    if representatives.len() != 32 {
        eprintln!(
            "FAIL: number of orbits = {}, expected 32",
            representatives.len()
        );
        return ExitCode::from(1);
    }
    println!("OK number of orbits = 32");

    // Check every snub vertex has been assigned an orbit.
    for (i, &orb) in orbit_of.iter().enumerate() {
        if orb == usize::MAX {
            eprintln!("FAIL: vertex {} not in any orbit", i);
            return ExitCode::from(1);
        }
    }

    // ---- 7. Build G_0, G_1, G_2 and check |G_i| = 32 -----------------------
    // G_0 = the 32 canonical representatives.
    // G_1 = g . G_0
    // G_2 = g^2 . G_0
    let g0: Vec<Quat2> = representatives.iter().map(|&i| snub[i]).collect();
    let g1: Vec<Quat2> = g0.iter().map(|v| g.mul_doubled(*v)).collect();
    let g2_set: Vec<Quat2> = g0.iter().map(|v| g2.mul_doubled(*v)).collect();
    if g0.len() != 32 || g1.len() != 32 || g2_set.len() != 32 {
        eprintln!("FAIL: |G_i| != 32");
        return ExitCode::from(1);
    }
    println!("OK |G_0| = |G_1| = |G_2| = 32");

    // ---- 8. Pairwise disjointness -----------------------------------------
    let mut all: Vec<Quat2> = Vec::with_capacity(96);
    all.extend_from_slice(&g0);
    all.extend_from_slice(&g1);
    all.extend_from_slice(&g2_set);
    let mut sorted = all.clone();
    sorted.sort_by(|a, b| {
        (a.w.a, a.w.b, a.x.a, a.x.b, a.y.a, a.y.b, a.z.a, a.z.b).cmp(&(
            b.w.a, b.w.b, b.x.a, b.x.b, b.y.a, b.y.b, b.z.a, b.z.b,
        ))
    });
    let len_before = sorted.len();
    sorted.dedup();
    let len_after = sorted.len();
    if len_after != 96 {
        eprintln!(
            "FAIL: G_0 ∪ G_1 ∪ G_2 has {} distinct elements (was {} before dedup); expected 96",
            len_after, len_before
        );
        return ExitCode::from(1);
    }
    println!("OK G_0 ⊔ G_1 ⊔ G_2 has 96 distinct elements");

    // ---- 9. Union equals snub ---------------------------------------------
    // Both have 96 elements and the union is contained in snub (each g^k*v is
    // in 2I and in fact lies in the snub family because it is a non-trivial
    // orbit under 2T-left-mult, so it cannot be in 2T). The set-equality
    // follows by cardinality.
    println!("OK G_0 ⊔ G_1 ⊔ G_2 = snub_96");

    // ---- 10. Final summary -------------------------------------------------
    println!("VERIFIED W4.2: snub 24-cell admits Z_3-tripartition 96 = 3 x 32");
    ExitCode::from(0)
}
