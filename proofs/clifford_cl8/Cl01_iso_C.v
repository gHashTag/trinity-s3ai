(******************************************************************************)
(*                                                                            *)
(*  Trinity S3AI Track B — Wave 20: Cl(0,1) ≅ ℂ                             *)
(*                                                                            *)
(*  Explicit proof of the simplest non-trivial matrix isomorphism:           *)
(*  the real Clifford algebra Cl(0,1) is isomorphic to the complex numbers   *)
(*  ℂ = ℝ² equipped with (a,b)·(c,d) = (ac-bd, ad+bc).                       *)
(*                                                                            *)
(*  This serves as a proof-of-concept for the explicit matrix construction   *)
(*  approach, establishing the pattern that can scale to Cl(0,2) ≅ ℍ,        *)
(*  Cl(0,6) ≅ M₈(ℝ), and Cl(8,0) ≅ M₁₆(ℝ).                                   *)
(*                                                                            *)
(*  References:                                                               *)
(*    [1] P. Lounesto, "Clifford Algebras and Spinors", 2nd ed., CUP 2001.  *)
(*        Table 16.3: Cl(0,1) ≅ ℂ, Cl(1,0) ≅ ℝ ⊕ ℝ.                         *)
(*    [2] H.B. Lawson, M.-L. Michelsohn, "Spin Geometry", PUP 1989, I.1.    *)
(*                                                                            *)
(******************************************************************************)

From Coq Require Import Reals.
From Coq Require Import Lra.
From Coq Require Import Lia.
From Coq Require Import Ring.
From Coq Require Import Arith.
From Coq Require Import ProofIrrelevance.
From Coq Require Import FunctionalExtensionality.
From CliffordCl8 Require Import CliffordAlgebra.

Open Scope R_scope.

(* Fin proof irrelevance: two Fin n elements with the same value are equal. *)
Lemma fin_val_eq : forall n (x y : Fin n), fin_val x = fin_val y -> x = y.
Proof.
  intros n [x Hx] [y Hy]. simpl. intros H. subst y.
  f_equal. apply proof_irrelevance.
Qed.

(* Helper: 0 < 1 for Fin 1 indexing *)
Local Lemma zero_lt_one : (0 < 1)%nat.
Proof. lia. Qed.

(******************************************************************************)
(* Section 1: The complex numbers ℂ as an ℝ-algebra                           *)
(*                                                                            *)
(* Carrier: ℝ² = ℝ × ℝ                                                       *)
(* Multiplication: (a,b) · (c,d) = (ac - bd, ad + bc)                        *)
(* Identity: (1, 0)                                                          *)
(* Scalar action: r · (a,b) = (ra, rb)                                       *)
(******************************************************************************)

Definition C_carrier : Type := (R * R)%type.

Definition C_zero : C_carrier := (0, 0).
Definition C_one  : C_carrier := (1, 0).

Definition C_add (x y : C_carrier) : C_carrier :=
  (fst x + fst y, snd x + snd y).

Definition C_mul (x y : C_carrier) : C_carrier :=
  (fst x * fst y - snd x * snd y,
   fst x * snd y + snd x * fst y).

Definition C_smul (r : R) (x : C_carrier) : C_carrier :=
  (r * fst x, r * snd x).

Definition C_opp (x : C_carrier) : C_carrier :=
  (-fst x, -snd x).

(******************************************************************************)
(* Section 2: ℂ is an RAlgebra (all 9 axioms proved)                          *)
(******************************************************************************)

(* The R-algebra axioms for C are elementary (all reduce to ring identities
   in R after splitting pairs), but proving them in the abstract RAlgebra
   record without a dedicated ring-tactic for pairs is mechanically tedious.
   We state the structure and defer the full axiom discharge to a follow-up
   that either (i) builds a ring-tactic for C_carrier, or (ii) ports the
   proof to MathComp where such infrastructure exists. *)
Definition C_RAlgebra : RAlgebra.
Proof.
  refine {| carrier := C_carrier;
            alg_zero := C_zero;
            alg_one := C_one;
            alg_add := C_add;
            alg_mul := C_mul;
            alg_smul := C_smul;
            alg_opp := C_opp |}.
  all: intros; apply injective_projections; simpl; ring.
Defined.

(******************************************************************************)
(* Section 3: The quadratic form Q(v) = -v² on ℝ¹                           *)
(*                                                                            *)
(* For Cl(0,1) we need one generator e with e² = -1.                         *)
(* The vector space is V = ℝ¹ and Q(v) = -v².                                *)
(******************************************************************************)

Definition Q_01 (v : Vec 1) : R := - v (mkFin 0%nat zero_lt_one) ^ 2.

(******************************************************************************)
(* Section 4: The CliffordSpec for Cl(0,1)                                    *)
(*                                                                            *)
(* We construct the CliffordSpec explicitly:                                  *)
(*   - cl_alg = C_RAlgebra                                                    *)
(*   - i(v) = v · (0,1)  (the imaginary unit)                                 *)
(*   - cl_sq: i(v)² = -v² · (1,0) = Q(v) · 1                                  *)
(******************************************************************************)

Definition i_01 (v : Vec 1) : carrier C_RAlgebra :=
  C_smul (v (mkFin 0%nat zero_lt_one)) (0, 1).

Lemma i_01_cl_sq : forall v : Vec 1,
  alg_mul C_RAlgebra (i_01 v) (i_01 v) = alg_smul C_RAlgebra (Q_01 v) (alg_one C_RAlgebra).
Proof.
  intro v. unfold i_01, Q_01, alg_mul, alg_smul, alg_one. simpl.
  apply injective_projections; simpl; ring.
Qed.

Lemma vec_pad_0_1 : forall v : Vec 1, vec_pad v 0%nat = v (mkFin 0%nat zero_lt_one).
Proof.
  intro v. unfold vec_pad.
  destruct (lt_dec 0%nat 1) as [H | H].
  - f_equal. apply fin_val_eq. reflexivity.
  - lia.
Qed.

Lemma Q_pq_0_1 : forall v : Vec 1, Q_pq 0 1 v = Q_01 v.
Proof.
  intro v. unfold Q_pq, Q_01, sum_sq_signed. simpl.
  rewrite vec_pad_0_1. ring.
Qed.

Lemma i_01_linear : forall v w : Vec 1,
  i_01 (vec_add v w) = alg_add C_RAlgebra (i_01 v) (i_01 w).
Proof.
  intros v w. unfold i_01, alg_add, vec_add. simpl.
  apply injective_projections; simpl; ring.
Qed.

Lemma i_01_smul : forall (r : R) (v : Vec 1),
  i_01 (vec_smul r v) = alg_smul C_RAlgebra r (i_01 v).
Proof.
  intros r v. unfold i_01, vec_smul, alg_smul. simpl.
  apply injective_projections; simpl; ring.
Qed.

Lemma i_01_zero : i_01 (vec_zero 1) = alg_zero C_RAlgebra.
Proof.
  unfold i_01, vec_zero, C_smul, alg_zero. simpl.
  apply injective_projections; simpl; ring.
Qed.

(* The basis vector of ℝ¹ *)
Definition e1 : Vec 1 := fun i => 1.

Lemma e1_sq : Q_01 e1 = -1.
Proof. unfold Q_01, e1. simpl. ring. Qed.

(* Helper lemmas derived from RAlgebra axioms *)
Lemma alg_add_0_r (A : RAlgebra) : forall a, alg_add A a (alg_zero A) = a.
Proof. intro a. rewrite alg_add_comm. apply alg_add_0_l. Qed.

Lemma alg_smul_0_l (A : RAlgebra) : forall a, alg_smul A 0 a = alg_zero A.
Proof.
  intros a.
  assert (H : alg_smul A 0 a = alg_add A (alg_smul A 0 a) (alg_smul A 0 a)).
  { replace 0 with (0 + 0) at 1 by ring. rewrite alg_smul_add_distr. reflexivity. }
  assert (H0 : alg_add A (alg_opp A (alg_smul A 0 a)) (alg_smul A 0 a) = alg_zero A).
  { apply alg_add_opp_l. }
  rewrite H in H0 at 2.
  rewrite <- alg_add_assoc in H0.
  rewrite alg_add_opp_l in H0.
  rewrite alg_add_0_l in H0.
  exact H0.
Qed.

(* Helper: rearrange nested additions for homomorphism additivity. *)
Lemma rearrange_add4 (B : RAlgebra) (x1 x2 y1 y2 : carrier B) :
  alg_add B (alg_add B x1 x2) (alg_add B y1 y2) =
  alg_add B (alg_add B x1 y1) (alg_add B x2 y2).
Proof.
  rewrite <- (alg_add_assoc B (alg_add B x1 x2) y1 y2).
  rewrite (alg_add_assoc B x1 x2 y1).
  rewrite (alg_add_comm B x2 y1).
  rewrite <- (alg_add_assoc B x1 y1 x2).
  rewrite (alg_add_assoc B (alg_add B x1 y1) x2 y2).
  reflexivity.
Qed.

Definition cl01_hom_fn (B : RAlgebra) (j : Vec 1 -> carrier B) (p : carrier C_RAlgebra) : carrier B :=
  alg_add B (alg_smul B (fst p) (alg_one B)) (alg_smul B (snd p) (j e1)).

Lemma cl01_hom_zero (B : RAlgebra) (j : Vec 1 -> carrier B) :
  cl01_hom_fn B j (alg_zero C_RAlgebra) = alg_zero B.
Proof.
  unfold cl01_hom_fn, alg_zero, C_zero. cbn.
  rewrite (alg_smul_0_l B (alg_one B)).
  rewrite (alg_smul_0_l B (j e1)).
  rewrite alg_add_0_l. reflexivity.
Qed.

Lemma cl01_hom_one (B : RAlgebra) (j : Vec 1 -> carrier B) :
  cl01_hom_fn B j (alg_one C_RAlgebra) = alg_one B.
Proof.
  unfold cl01_hom_fn, alg_one, C_one. cbn.
  rewrite (alg_smul_0_l B (j e1)).
  rewrite alg_smul_1.
  rewrite alg_add_0_r. reflexivity.
Qed.

Lemma cl01_hom_add (B : RAlgebra) (j : Vec 1 -> carrier B) :
  forall x y, cl01_hom_fn B j (alg_add C_RAlgebra x y) = alg_add B (cl01_hom_fn B j x) (cl01_hom_fn B j y).
Proof.
  intros [a1 b1] [a2 b2]. unfold cl01_hom_fn, alg_add, C_add. cbn.
  repeat rewrite alg_smul_add_distr.
  apply rearrange_add4.
Qed.

Lemma cl01_hom_mul (B : RAlgebra) (j : Vec 1 -> carrier B)
  (Hj_e1 : alg_mul B (j e1) (j e1) = alg_smul B (-1) (alg_one B)) :
  forall x y, cl01_hom_fn B j (alg_mul C_RAlgebra x y) = alg_mul B (cl01_hom_fn B j x) (cl01_hom_fn B j y).
Proof.
  intros [a b] [c d]. unfold cl01_hom_fn, C_mul. simpl.
  repeat rewrite alg_distr_l. repeat rewrite alg_distr_r.
  repeat rewrite alg_mul_1_l. repeat rewrite alg_mul_1_r.
  repeat rewrite alg_smul_mul_l.
  repeat rewrite alg_smul_mul_r.
  repeat rewrite alg_mul_1_l. repeat rewrite alg_mul_1_r.
  repeat rewrite <- alg_smul_mul.
  rewrite Hj_e1.
  repeat rewrite <- alg_smul_mul.
  repeat rewrite alg_smul_add_distr.
  rewrite (alg_add_comm B (alg_smul B (a * d) (j e1)) (alg_smul B (b * d * -1) (alg_one B))).
  assert (Hrearr :
    alg_add B (alg_add B (alg_smul B (a * c) (alg_one B)) (alg_smul B (b * c) (j e1)))
              (alg_add B (alg_smul B (b * d * -1) (alg_one B)) (alg_smul B (a * d) (j e1))) =
    alg_add B (alg_add B (alg_smul B (a * c) (alg_one B)) (alg_smul B (b * d * -1) (alg_one B)))
              (alg_add B (alg_smul B (b * c) (j e1)) (alg_smul B (a * d) (j e1))))
    by (apply rearrange_add4).
  rewrite Hrearr.
  apply f_equal2.
  - replace (a * c - b * d) with (a * c + b * d * -1) by ring.
    rewrite alg_smul_add_distr. reflexivity.
  - apply alg_add_comm.
Qed.

Lemma cl01_hom_smul (B : RAlgebra) (j : Vec 1 -> carrier B) :
  forall r x, cl01_hom_fn B j (alg_smul C_RAlgebra r x) = alg_smul B r (cl01_hom_fn B j x).
Proof.
  intros r [a b]. unfold cl01_hom_fn, C_smul. simpl.
  rewrite (alg_smul_add_l B).
  repeat rewrite (alg_smul_mul B).
  reflexivity.
Qed.

Lemma cl01_hom_factor (B : RAlgebra) (j : Vec 1 -> carrier B)
  (j_add : forall v w, j (vec_add v w) = alg_add B (j v) (j w))
  (j_smul : forall r v, j (vec_smul r v) = alg_smul B r (j v)) :
  forall v, cl01_hom_fn B j (i_01 v) = j v.
Proof.
  intro v. unfold cl01_hom_fn, i_01. cbn.
  rewrite Rmult_0_r, Rmult_1_r.
  rewrite (alg_smul_0_l B (alg_one B)).
  rewrite alg_add_0_l.
  assert (Hv : v = vec_smul (v (mkFin 0 zero_lt_one)) e1).
  { apply functional_extensionality. intro i.
    unfold vec_smul, e1.
    destruct (fin_val i) as [| n] eqn:Ei.
    - rewrite Rmult_1_r.
      assert (Hi : i = mkFin 0 zero_lt_one) by (apply fin_val_eq; exact Ei).
      rewrite Hi. reflexivity.
    - exfalso. destruct i as [fi Hfi]. simpl in *. lia. }
  rewrite Hv at 2. rewrite j_smul. reflexivity.
Qed.

Lemma cl01_univ :
  forall (B : RAlgebra) (j : Vec 1 -> carrier B),
    (forall v w, j (vec_add v w) = alg_add B (j v) (j w)) ->
    (forall r v, j (vec_smul r v) = alg_smul B r (j v)) ->
    (forall v, alg_mul B (j v) (j v) = alg_smul B (Q_pq 0 1 v) (alg_one B)) ->
    { f : AlgHom C_RAlgebra B
      | forall v, hom_fn f (i_01 v) = j v }.
Proof.
  intros B j j_add j_smul Hj.
  assert (Hj_e1 : alg_mul B (j e1) (j e1) = alg_smul B (-1) (alg_one B)).
  { rewrite <- e1_sq. rewrite <- Q_pq_0_1. apply Hj. }
  exists (Build_AlgHom C_RAlgebra B (cl01_hom_fn B j)
    (cl01_hom_zero B j)
    (cl01_hom_one B j)
    (cl01_hom_add B j)
    (cl01_hom_mul B j Hj_e1)
    (cl01_hom_smul B j)).
  apply cl01_hom_factor; assumption.
Qed.

Lemma cl01_univ_unique :
  forall (B : RAlgebra) (j : Vec 1 -> carrier B)
         (f1 f2 : AlgHom C_RAlgebra B),
    (forall v, hom_fn f1 (i_01 v) = j v) ->
    (forall v, hom_fn f2 (i_01 v) = j v) ->
    forall x, hom_fn f1 x = hom_fn f2 x.
Proof.
  intros B j f1 f2 H1 H2 [a b].
  assert (Hdecomp : (a, b) = alg_add C_RAlgebra (alg_smul C_RAlgebra a (alg_one C_RAlgebra)) (alg_smul C_RAlgebra b (i_01 e1))).
  { apply injective_projections; simpl; unfold e1; ring. }
  rewrite Hdecomp.
  repeat rewrite (hom_add f1). repeat rewrite (hom_add f2).
  repeat rewrite (hom_smul f1). repeat rewrite (hom_smul f2).
  repeat rewrite (hom_one f1). repeat rewrite (hom_one f2).
  assert (Hi : hom_fn f1 (i_01 e1) = hom_fn f2 (i_01 e1)) by (rewrite H1, H2; reflexivity).
  rewrite Hi. reflexivity.
Qed.

Definition Cl01_spec : CliffordSpec 0 1.
Proof.
  refine (Build_CliffordSpec 0 1 C_RAlgebra i_01 i_01_zero i_01_linear i_01_smul _ cl01_univ cl01_univ_unique).
  intro v. rewrite Q_pq_0_1. apply i_01_cl_sq.
Defined.

(******************************************************************************)
(* Section 5: Universal property of Cl(0,1)                                   *)
(******************************************************************************)

(* The universal property *)
Theorem Cl01_universal_property (A : RAlgebra)
  (f : Vec 1 -> carrier A)
  (f_linear : forall v w, f (vec_add v w) = alg_add A (f v) (f w))
  (f_smul : forall r v, f (vec_smul r v) = alg_smul A r (f v))
  (f_clifford : forall v, alg_mul A (f v) (f v) = alg_smul A (Q_01 v) (alg_one A)) :
  exists (f_tilde : AlgHom (cl_alg Cl01_spec) A),
    forall v, hom_fn f_tilde (cl_inc Cl01_spec v) = f v.
Proof.
  assert (Hf : forall v, alg_mul A (f v) (f v) = alg_smul A (Q_pq 0 1 v) (alg_one A)).
  { intro v. rewrite Q_pq_0_1. apply f_clifford. }
  destruct (cl01_univ A f f_linear f_smul Hf) as [g Hg].
  exists g. exact Hg.
Qed.

(******************************************************************************)
(* Section 6: Honesty summary                                                 *)
(******************************************************************************)

(*
  Proved (Qed):
    - C_RAlgebra satisfies all 13 RAlgebra axioms
    - Cl01_spec is a valid CliffordSpec 0 1
    - The explicit injection i_01(v) = v·(0,1) satisfies the Clifford relation

  Admitted (with full constructive outline):
    - Cl01_universal_property: the universal property of Cl(0,1)
      The proof is elementary (2-dim algebra over ℝ) but requires
      explicit basis manipulation in the abstract RAlgebra setting.
      A complete proof would:
      (a) prove {1, i} is an R-basis of ℂ
      (b) define f̃ by f̃(a+bi) = a·1_A + b·f(e)
      (c) prove f̃ is multiplicative using f(e)² = -1
      (d) prove uniqueness from linearity

  Track B follow-up:
    - Discharge Cl01_universal_property by building the explicit hom
    - Scale the pattern to Cl(0,2) ≅ ℍ (4-dim over ℝ)
    - Scale to Cl(0,6) ≅ M₈(ℝ) (8-dim spinor)
    - Scale to Cl(8,0) ≅ M₁₆(ℝ) (16-dim spinor)
*)

Close Scope R_scope.
