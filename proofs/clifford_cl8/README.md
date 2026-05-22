# Track B — Cl(p,q) Clifford algebra formalization

**Wave 12 launch:** T1–T3 of the 12-theorem programme defined in
`outputs/B_program_T1_T12.md` (Trinity S3AI Cl(8)/J3(O) pivot).

This directory is the **scaffolding** for a multi-month effort to formalize
real Clifford algebras Cl(p,q) and their matrix-algebra classification (the
Atiyah-Bott-Shapiro mod-8 periodicity table), ultimately feeding into the
three-generations question via J3(O) and Cl(8) triality.

## Files

| File | Theorem | Status |
|------|---------|--------|
| `CliffordAlgebra.v` | T1 — Cl(p,q) definition via universal property | **Mostly Qed**; one polarization-identity lemma `Admitted` (TRACK_B_CLIFFORD) |
| `Cl6_iso_M8R.v` | T2 — Cl(0,6) ≅ M_8(R) ⊕ M_8(R) | **Stated, Admitted** with full citation (Lounesto Table 16.3, Wieser-Song §6) |
| `Cl8_periodicity.v` | T3 — Cl(n+8) ≅ Cl(n) ⊗ Cl(8) (Bott periodicity) | **Stated, Admitted** with full citation (Atiyah-Bott-Shapiro 1964 Table 3) |

## Honesty

This PR is the **launch** of Track B. The realistic deliverable for the launch
PR (per the user-supplied brief) is:

- **T1**: definitions + universal-property record + a small handful of
  Qed-closed corollaries. Coq stdlib does not provide a turnkey tensor algebra,
  so we adopt the universal-property characterization (Wieser-Song §3) as the
  primary abstraction. One polarization identity (`T1_polarization`) is
  Admitted as a follow-up since proving it in the abstract `RAlgebra` setting
  without a ring-tactic is mechanically tedious; the identity is in Lounesto §1.2.
- **T2**: statement-level only. The explicit 8×8 matrix construction of the
  six generators (Lounesto §16.4, Wieser-Song §6) and the verification that
  it gives an R-algebra iso is mechanical-but-lengthy (multi-week). Admitted
  with citation.
- **T3**: statement-level only. The proof requires an explicit
  tensor-product-of-R-algebras infrastructure (`RAlg_tensor`) that we
  axiomatize here. Discharging it would either (i) port the Wieser-Song
  Lean 3 module to Rocq, (ii) wait for mathlib4's CliffordAlgebra to grow
  the missing periodicity lemma, or (iii) reproduce the proof from scratch
  via Lawson-Michelsohn I.4.

## Convention note (T2)

The B-program spec (`outputs/B_program_T1_T12.md`, §T1) writes
"Cl(6) ≅ M_8(R) ⊕ M_8(R)". In Lounesto's convention this is **Cl(0,6)**
(six minus-generators, e_i² = −1). The other-signature variant **Cl(6,0)**
sits at row (6,0) of Lounesto Table 16.3 with Cl(6,0) ≅ M_8(C). The user-
supplied brief's "Cl(6) via 2³ = 8 dim representation" matches the Cl(0,6)
convention (single 8-dim real spinor representation). We follow that.

## References

- **[Wieser & Song 2022]** "Formalizing Geometric Algebra in Lean", *Adv.
  Appl. Clifford Algebras* 32, 28 (2022). arXiv:2110.03551.
- **[Atiyah, Bott, Shapiro 1964]** "Clifford modules", *Topology* 3 Suppl. 1,
  3–38. DOI 10.1016/0040-9383(64)90003-5.
- **[Lawson & Michelsohn 1989]** *Spin Geometry*, Princeton University Press.
  Prop. I.4.1 (8-periodicity).
- **[Lounesto 2001]** *Clifford Algebras and Spinors* (2nd ed.), Cambridge
  University Press. Tables 16.1–16.4.
- **[Farnsworth 2025]** "The n-point Exceptional Universe", arXiv:2503.10744 —
  J3(O) spectral geometry context relevant to later T6–T12.

## Build

This directory has its own `_CoqProject` (`-Q . CliffordCl8`). The files are
written for Coq 8.20+ / Rocq 9.1 and depend only on `Coq.Reals`, `Coq.Arith`,
`Coq.Lia`, `Coq.Lra`. No `From Trinity ...` imports — Track B is intentionally
decoupled from the H4/600-cell core so it can be maintained as a stand-alone
library.

## What's next (Track B follow-up PRs)

1. Discharge `T1_polarization` — write the abstract polarization proof
   directly using the `RAlgebra` axioms or expose a tactic.
2. Construct one concrete `CliffordSpec p q` for small (p, q), giving a
   witness for the spec record (kills the `Cl06_spec` and `Cl_n0_spec` axioms).
3. Build `RAlg_tensor` concretely (or port from MathComp-Analysis).
4. T4–T6 from `B_program_T1_T12.md`: spinor modules, minimal left ideals
   (Furey 2018), and SU(3)c × U(1)em quantum numbers from Cl(6) ideals.
