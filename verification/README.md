# trinity-verification — Rust exact-arithmetic verification crate

This crate replaces the earlier Python verification scripts for
Wave 4 / Wave 6 of `trinity-s3ai`. Per project rule **R1** (no Python in
the verification path), every numerical anchor that `trinity-s3ai`
depends on is re-derived here from integer-coefficient elements in the
golden-ratio ring `Z[phi]` and the icosian ring of quaternions.

## Anchor identity

Proven structurally in `ring::tests::phi_sq_plus_phi_minus_two_equals_three`:

    phi^2 + phi^(-2) = 3      <==>      phi^4 - 3 phi^2 + 1 = 0   in Z[phi].

## Layout

    src/
      lib.rs           — re-exports
      ring.rs          — Phi { a, b: i64 }, ring laws, anchor identity
      quaternion.rs    — Quat2 (doubled-quaternion encoding)
      icosian.rs       — the 120 elements of 2I as Quat2 (24-cell + snub)
      bin/
        verify_snub_24cell.rs        — Wave 4 W4.2
        verify_e8_to_h4.rs           — Wave 4 W4.3
        verify_spectral_sin2theta.rs — Wave 4 W4.8
        verify_duality_8x12_3x32.rs  — Wave 6 W6.3
    tests/
      ring_laws.rs     — integration tests for Phi ring laws

## Usage

    cd verification
    cargo build --release
    cargo test --release
    cargo run --release --bin verify_snub_24cell
    cargo run --release --bin verify_e8_to_h4
    cargo run --release --bin verify_spectral_sin2theta
    cargo run --release --bin verify_duality_8x12_3x32

Each binary prints byte-stable output and exits with code 0 on success,
code 1 on any structural failure.

## Dependencies

None outside the Rust standard library. All exact arithmetic is built
on `i64`. The one binary that uses `f64` (`verify_spectral_sin2theta`)
does so because gauge-coupling RG running is a continuous numerical
computation, not an algebraic identity — every other check is exact.

## Replacement table

| Was (Python)                          | Now (Rust)                                            |
| ------------------------------------- | ----------------------------------------------------- |
| `wave4_snub_24cell.py`                | `bin/verify_snub_24cell.rs`                           |
| `wave4_e8_to_h4.py`                   | `bin/verify_e8_to_h4.rs`                              |
| `wave4_spectral_sin2theta.py`         | `bin/verify_spectral_sin2theta.rs`                    |
| `wave6_duality_8x12_3x32.py`          | `bin/verify_duality_8x12_3x32.rs`                     |
