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

---

## Peer-reviewed scientific foundation (updated Wave 24)

The **Gourlay & Gresnigt 2024** paper (*Eur. Phys. J. C* **84**, 1129)
provides the algebraic mechanism that Track B seeks to formalize:

- **Algebra:** Complex sedenions **C ⊗ S** have automorphism group  
  Aut(S) = G₂ × **S₃**.
- **Clifford structure:** The left multiplication algebra of C ⊗ S is  
  **Cl(8)**.
- **Generation mechanism:** The **S₃** factor permutes three minimal
  left ideals of Cl(8). Each ideal hosts one generation of SM fermions
  with unbroken SU(3)C × U(1)em.
- **Independence:** The three generations are **linearly independent**.

This is the most rigorous known route from exceptional algebra to three
freedoms. It bypasses H4-specific obstructions BT-3 and BT-4 by using a
different algebraic starting point.

**Honesty note:** The formal bridge between H4 and Cl(8) (e.g. via
Dechant's E8 → H4 pinor construction) is still an open problem.

## Relation to Trinity's boundary theorems

| H4 obstruction | How Cl(8) may bypass it |
|----------------|--------------------------|
| BT-3: 600-cell D_F is vector-like (antipodal symmetry) | Cl(8) spinors are not constrained by antipodal symmetry; chirality comes from the even/odd grading |
| BT-4: 2I-equivariant D_F cannot reproduce lepton masses | Cl(8) mass matrices arise from sedenion automorphisms, not 2I-equivariance |
| BT-2: No NCG σ-field from H4 root structure alone | Cl(8) may admit a natural Dirac operator via its spinor structure |

*This is a hypothesis, not a proven detour.*
