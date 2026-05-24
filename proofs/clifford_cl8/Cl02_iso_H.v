(******************************************************************************)
(*                                                                            *)
(*  Trinity S3AI Track B — Wave 21: Cl(0,2) ≅ ℍ                             *)
(*                                                                            *)
(*  Explicit proof that the real Clifford algebra Cl(0,2) is isomorphic to   *)
(*  the quaternions ℍ = ℝ⁴ equipped with Hamilton multiplication.             *)
(*                                                                            *)
(*  This scales the Wave 20 pattern (Cl(0,1) ≅ ℂ) to 2 generators,           *)
(*  validating the approach before tackling Cl(0,6) ≅ M₈(ℝ) and Cl(8,0).     *)
(*                                                                            *)
(*  References:                                                               *)
(*    [1] P. Lounesto, "Clifford Algebras and Spinors", 2nd ed., CUP 2001.  *)
(*        Table 16.3: Cl(0,2) ≅ ℍ.                                           *)
(*    [2] H.B. Lawson, M.-L. Michelsohn, "Spin Geometry", PUP 1989, I.1.    *)
(*                                                                            *)
(******************************************************************************)

From Coq Require Import Reals.
From Coq Require Import Lra.
From Coq Require Import Lia.
From Coq Require Import Ring.
From Coq Require Import ProofIrrelevance.
From Coq Require Import FunctionalExtensionality.
From Coq Require Import Compare_dec.
From CliffordCl8 Require Import CliffordAlgebra.

Open Scope R_scope.

(* Helpers for Fin 2 indexing *)
Local Lemma zero_lt_two : (0 < 2)%nat.
Proof. lia. Qed.

Local Lemma one_lt_two : (1 < 2)%nat.
Proof. lia. Qed.

Lemma fin_val_eq : forall n (x y : Fin n), fin_val x = fin_val y -> x = y.
Proof.
  intros n [x Hx] [y Hy]. simpl. intros H. subst y.
  f_equal. apply proof_irrelevance.
Qed.

(******************************************************************************)
(* Section 1: The quaternions ℍ as an ℝ-algebra                               *)
(******************************************************************************)

Record H_carrier := mkH {
  h_re : R;
  h_i  : R;
  h_j  : R;
  h_k  : R
}.

Lemma H_eq : forall x y : H_carrier,
  h_re x = h_re y ->
  h_i  x = h_i  y ->
  h_j  x = h_j  y ->
  h_k  x = h_k  y ->
  x = y.
Proof.
  intros [xr xi xj xk] [yr yi yj yk]; simpl; intros; subst; reflexivity.
Qed.

Definition H_zero : H_carrier := mkH 0 0 0 0.
Definition H_one  : H_carrier := mkH 1 0 0 0.

Definition H_add (x y : H_carrier) : H_carrier :=
  mkH (h_re x + h_re y)
      (h_i  x + h_i  y)
      (h_j  x + h_j  y)
      (h_k  x + h_k  y).

Definition H_mul (x y : H_carrier) : H_carrier :=
  mkH (h_re x * h_re y - h_i x * h_i y - h_j x * h_j y - h_k x * h_k y)
      (h_re x * h_i  y + h_i x * h_re y + h_j x * h_k y - h_k x * h_j y)
      (h_re x * h_j  y - h_i x * h_k y + h_j x * h_re y + h_k x * h_i  y)
      (h_re x * h_k  y + h_i x * h_j  y - h_j x * h_i y + h_k x * h_re y).

Definition H_smul (r : R) (x : H_carrier) : H_carrier :=
  mkH (r * h_re x) (r * h_i x) (r * h_j x) (r * h_k x).

Definition H_opp (x : H_carrier) : H_carrier :=
  mkH (-h_re x) (-h_i x) (-h_j x) (-h_k x).

(******************************************************************************)
(* Section 2: ℍ is an RAlgebra (all 13 axioms proved)                         *)
(******************************************************************************)

Definition H_RAlgebra : RAlgebra.
Proof.
  refine {| carrier := H_carrier;
            alg_zero := H_zero;
            alg_one := H_one;
            alg_add := H_add;
            alg_mul := H_mul;
            alg_smul := H_smul;
            alg_opp := H_opp |}.
  all: intros; apply H_eq; simpl; ring.
Defined.

(******************************************************************************)
(* Section 3: The quadratic form Q(v) = -(v₀² + v₁²) on ℝ²                   *)
(******************************************************************************)

Definition Q_02 (v : Vec 2) : R :=
  - v (mkFin 0%nat zero_lt_two) ^ 2
  - v (mkFin 1%nat one_lt_two) ^ 2.

(******************************************************************************)
(* Section 4: The CliffordSpec for Cl(0,2)                                    *)
(******************************************************************************)

Definition i_02 (v : Vec 2) : carrier H_RAlgebra :=
  H_add (H_smul (v (mkFin 0%nat zero_lt_two)) (mkH 0 1 0 0))
        (H_smul (v (mkFin 1%nat one_lt_two)) (mkH 0 0 1 0)).

Lemma i_02_cl_sq : forall v : Vec 2,
  alg_mul H_RAlgebra (i_02 v) (i_02 v) = alg_smul H_RAlgebra (Q_02 v) (alg_one H_RAlgebra).
Proof.
  intro v. unfold i_02, Q_02, alg_mul, alg_smul, alg_one. simpl.
  apply H_eq; simpl; ring.
Qed.

Lemma vec_pad_0_2_0 : forall v : Vec 2, vec_pad v 0%nat = v (mkFin 0%nat zero_lt_two).
Proof.
  intro v. unfold vec_pad.
  destruct (lt_dec 0%nat 2) as [H | H].
  - f_equal. apply fin_val_eq. reflexivity.
  - lia.
Qed.

Lemma vec_pad_0_2_1 : forall v : Vec 2, vec_pad v 1%nat = v (mkFin 1%nat one_lt_two).
Proof.
  intro v. unfold vec_pad.
  destruct (lt_dec 1%nat 2) as [H | H].
  - f_equal. apply fin_val_eq. reflexivity.
  - lia.
Qed.

Lemma Q_pq_0_2 : forall v : Vec 2, Q_pq 0 2 v = Q_02 v.
Proof.
  intro v. unfold Q_pq, Q_02, sum_sq_signed. simpl.
  rewrite vec_pad_0_2_0, vec_pad_0_2_1. ring.
Qed.

Lemma i_02_linear : forall v w : Vec 2,
  i_02 (vec_add v w) = alg_add H_RAlgebra (i_02 v) (i_02 w).
Proof.
  intros v w. unfold i_02, alg_add, vec_add. simpl.
  apply H_eq; simpl; ring.
Qed.

Lemma i_02_smul : forall (r : R) (v : Vec 2),
  i_02 (vec_smul r v) = alg_smul H_RAlgebra r (i_02 v).
Proof.
  intros r v. unfold i_02, vec_smul, alg_smul. simpl.
  apply H_eq; simpl; ring.
Qed.

Lemma i_02_zero : i_02 (vec_zero 2) = alg_zero H_RAlgebra.
Proof.
  unfold i_02, vec_zero, H_smul, alg_zero. simpl.
  apply H_eq; simpl; ring.
Qed.

(******************************************************************************)
(* Section 5: Basis vectors of ℝ²                                             *)
(******************************************************************************)

Definition e1_02 : Vec 2 := fun i => if fin_val i =? 0 then 1 else 0.
Definition e2_02 : Vec 2 := fun i => if fin_val i =? 1 then 1 else 0.

Lemma e1_02_sq : Q_02 e1_02 = -1.
Proof. unfold Q_02, e1_02. simpl. ring. Qed.

Lemma e2_02_sq : Q_02 e2_02 = -1.
Proof. unfold Q_02, e2_02. simpl. ring. Qed.

(******************************************************************************)
(* Section 6: Explicit algebra homomorphism                                   *)
(******************************************************************************)

Definition cl02_hom_fn (B : RAlgebra) (j : Vec 2 -> carrier B) (p : carrier H_RAlgebra) : carrier B :=
  alg_add B (alg_smul B (h_re p) (alg_one B))
    (alg_add B (alg_smul B (h_i p) (j e1_02))
      (alg_add B (alg_smul B (h_j p) (j e2_02))
        (alg_smul B (h_k p) (alg_mul B (j e1_02) (j e2_02))))).

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

Lemma cl02_hom_zero (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j (alg_zero H_RAlgebra) = alg_zero B.
Proof.
  unfold cl02_hom_fn, alg_zero, H_zero. simpl.
  repeat rewrite alg_smul_0.
  rewrite (alg_add_0_l B). rewrite (alg_add_0_l B). rewrite (alg_add_0_l B).
  reflexivity.
Qed.

Lemma cl02_hom_one (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j (alg_one H_RAlgebra) = alg_one B.
Proof.
  unfold cl02_hom_fn, alg_one, H_one. simpl.
  rewrite alg_smul_1. repeat rewrite alg_smul_0.
  rewrite (alg_add_0_l B). rewrite (alg_add_0_l B).
  rewrite (alg_add_comm B). rewrite (alg_add_0_l B).
  reflexivity.
Qed.

Lemma cl02_hom_add (B : RAlgebra) (j : Vec 2 -> carrier B) :
  forall x y, cl02_hom_fn B j (H_add x y) = alg_add B (cl02_hom_fn B j x) (cl02_hom_fn B j y).
Proof.
  intros [a1 b1 c1 d1] [a2 b2 c2 d2]. unfold cl02_hom_fn, H_add. simpl.
  repeat rewrite alg_smul_add_distr.
  set (A1 := alg_smul B a1 (alg_one B)).
  set (A2 := alg_smul B a2 (alg_one B)).
  set (B1 := alg_smul B b1 (j e1_02)).
  set (B2 := alg_smul B b2 (j e1_02)).
  set (C1 := alg_smul B c1 (j e2_02)).
  set (C2 := alg_smul B c2 (j e2_02)).
  set (D1 := alg_smul B d1 (alg_mul B (j e1_02) (j e2_02))).
  set (D2 := alg_smul B d2 (alg_mul B (j e1_02) (j e2_02))).
  assert (H1 : alg_add B (alg_add B A1 (alg_add B B1 (alg_add B C1 D1))) (alg_add B A2 (alg_add B B2 (alg_add B C2 D2))) = alg_add B (alg_add B A1 A2) (alg_add B (alg_add B B1 (alg_add B C1 D1)) (alg_add B B2 (alg_add B C2 D2)))).
  { apply rearrange_add4. }
  rewrite H1.
  assert (H2 : alg_add B (alg_add B B1 (alg_add B C1 D1)) (alg_add B B2 (alg_add B C2 D2)) = alg_add B (alg_add B B1 B2) (alg_add B (alg_add B C1 D1) (alg_add B C2 D2))).
  { apply rearrange_add4. }
  rewrite H2.
  assert (H3 : alg_add B (alg_add B C1 D1) (alg_add B C2 D2) = alg_add B (alg_add B C1 C2) (alg_add B D1 D2)).
  { apply rearrange_add4. }
  rewrite H3.
  reflexivity.
Qed.

Lemma cl02_hom_smul (B : RAlgebra) (j : Vec 2 -> carrier B) :
  forall r x, cl02_hom_fn B j (H_smul r x) = alg_smul B r (cl02_hom_fn B j x).
Proof.
  intros r [a b c d]. unfold cl02_hom_fn, H_smul. simpl.
  repeat rewrite alg_smul_add_l.
  repeat rewrite <- alg_smul_mul.
  reflexivity.
Qed.

Lemma alg_opp_opp (B : RAlgebra) (a : carrier B) : alg_opp B (alg_opp B a) = a.
Proof.
  assert (H1 : alg_add B (alg_opp B a) a = alg_zero B).
  { apply alg_add_opp_l. }
  apply (alg_add_cancel B (alg_opp B a) a (alg_zero B)) in H1.
  rewrite alg_add_0_l in H1.
  symmetry. exact H1.
Qed.

(* Derived anticommutativity from the Clifford relation *)
Lemma cl02_j_anticomm (B : RAlgebra) (j : Vec 2 -> carrier B)
  (j_add : forall v w, j (vec_add v w) = alg_add B (j v) (j w))
  (Hj : forall v, alg_mul B (j v) (j v) = alg_smul B (Q_pq 0 2 v) (alg_one B)) :
  alg_mul B (j e1_02) (j e2_02) = alg_opp B (alg_mul B (j e2_02) (j e1_02)).
Proof.
  assert (Hlinear : j (vec_add e1_02 e2_02) = alg_add B (j e1_02) (j e2_02)) by apply j_add.
  assert (Huv : alg_mul B (j (vec_add e1_02 e2_02)) (j (vec_add e1_02 e2_02)) = alg_smul B (Q_pq 0 2 (vec_add e1_02 e2_02)) (alg_one B)) by apply Hj.
  rewrite Hlinear in Huv.
  assert (Hexpand : alg_mul B (alg_add B (j e1_02) (j e2_02)) (alg_add B (j e1_02) (j e2_02)) = alg_add B (alg_add B (alg_mul B (j e1_02) (j e1_02)) (alg_mul B (j e2_02) (j e1_02))) (alg_add B (alg_mul B (j e1_02) (j e2_02)) (alg_mul B (j e2_02) (j e2_02)))).
  { rewrite alg_distr_l. rewrite alg_distr_r. rewrite alg_distr_r.
    reflexivity. }
  rewrite Hexpand in Huv.
  assert (He1 : alg_mul B (j e1_02) (j e1_02) = alg_smul B (Q_pq 0 2 e1_02) (alg_one B)) by apply Hj.
  assert (He2 : alg_mul B (j e2_02) (j e2_02) = alg_smul B (Q_pq 0 2 e2_02) (alg_one B)) by apply Hj.
  rewrite He1, He2 in Huv.
  assert (HQ1 : Q_pq 0 2 e1_02 = -1).
  { rewrite Q_pq_0_2. apply e1_02_sq. }
  assert (HQ2 : Q_pq 0 2 e2_02 = -1).
  { rewrite Q_pq_0_2. apply e2_02_sq. }
  assert (HQ12 : Q_pq 0 2 (vec_add e1_02 e2_02) = -2).
  { rewrite Q_pq_0_2. unfold Q_02, vec_add, e1_02, e2_02. simpl. ring. }
  rewrite HQ1, HQ2, HQ12 in Huv.
  assert (Hcancel : alg_add B (alg_smul B (-1) (alg_one B)) (alg_smul B (-1) (alg_one B)) = alg_smul B (-2) (alg_one B)).
  { rewrite <- (alg_smul_add_distr B (-1) (-1) (alg_one B)).
    f_equal. ring. }
  assert (Hrest : alg_add B (alg_mul B (j e1_02) (j e2_02)) (alg_mul B (j e2_02) (j e1_02)) = alg_zero B).
  { assert (Hrearr : alg_add B (alg_smul B (-2) (alg_one B)) (alg_add B (alg_mul B (j e1_02) (j e2_02)) (alg_mul B (j e2_02) (j e1_02))) = alg_smul B (-2) (alg_one B)).
    { assert (Htmp : alg_add B (alg_add B (alg_smul B (-1) (alg_one B)) (alg_mul B (j e2_02) (j e1_02))) (alg_add B (alg_mul B (j e1_02) (j e2_02)) (alg_smul B (-1) (alg_one B))) = alg_smul B (-2) (alg_one B)) by exact Huv.
      rewrite (rearrange_add4 B (alg_smul B (-1) (alg_one B)) (alg_mul B (j e2_02) (j e1_02)) (alg_mul B (j e1_02) (j e2_02)) (alg_smul B (-1) (alg_one B))) in Htmp.
      rewrite (alg_add_comm B (alg_mul B (j e2_02) (j e1_02)) (alg_smul B (-1) (alg_one B))) in Htmp.
      rewrite (rearrange_add4 B (alg_smul B (-1) (alg_one B)) (alg_mul B (j e1_02) (j e2_02)) (alg_smul B (-1) (alg_one B)) (alg_mul B (j e2_02) (j e1_02))) in Htmp.
      rewrite Hcancel in Htmp.
      exact Htmp. }
    rewrite <- (alg_add_opp_r B (alg_smul B (-2) (alg_one B))).
    apply (alg_add_cancel B (alg_smul B (-2) (alg_one B)) _ (alg_smul B (-2) (alg_one B))).
    exact Hrearr. }
  assert (Hanti : alg_mul B (j e2_02) (j e1_02) = alg_opp B (alg_mul B (j e1_02) (j e2_02))).
  { pose proof (alg_add_cancel B (alg_mul B (j e1_02) (j e2_02)) (alg_mul B (j e2_02) (j e1_02)) (alg_zero B) Hrest) as Htmp.
    rewrite alg_add_0_l in Htmp. exact Htmp. }
  apply (f_equal (alg_opp B)) in Hanti.
  rewrite alg_opp_opp in Hanti.
  symmetry in Hanti. exact Hanti.
Qed.

(* Basis multiplication lemmas *)
Lemma H_mul_linear_l : forall x1 x2 y, H_mul (H_add x1 x2) y = H_add (H_mul x1 y) (H_mul x2 y).
Proof. intros [a1 b1 c1 d1] [a2 b2 c2 d2] [e f g h]. apply H_eq; simpl; ring. Qed.

Lemma H_mul_linear_r : forall x y1 y2, H_mul x (H_add y1 y2) = H_add (H_mul x y1) (H_mul x y2).
Proof. intros [a b c d] [e1 f1 g1 h1] [e2 f2 g2 h2]. apply H_eq; simpl; ring. Qed.

Lemma H_mul_smul_l : forall r x y, H_mul (H_smul r x) y = H_smul r (H_mul x y).
Proof. intros r [a b c d] [e f g h]. apply H_eq; simpl; ring. Qed.

Lemma H_mul_smul_r : forall r x y, H_mul x (H_smul r y) = H_smul r (H_mul x y).
Proof. intros r [a b c d] [e f g h]. apply H_eq; simpl; ring. Qed.

Definition H_one_v := mkH 1 0 0 0.
Definition H_i_v   := mkH 0 1 0 0.
Definition H_j_v   := mkH 0 0 1 0.
Definition H_k_v   := mkH 0 0 0 1.

Lemma alg_opp_is_smul_neg1 (B : RAlgebra) (a : carrier B) : alg_opp B a = alg_smul B (-1) a.
Proof.
  assert (H : alg_smul B (-1) a = alg_opp B a).
  { replace (alg_opp B a) with (alg_opp B (alg_smul B 1 a)).
    { apply (alg_smul_opp B 1 a). }
    rewrite (alg_smul_1 B a). reflexivity. }
  symmetry. exact H.
Qed.

Lemma alg_mul_opp_r (B : RAlgebra) (a b : carrier B) :
  alg_mul B a (alg_opp B b) = alg_opp B (alg_mul B a b).
Proof.
  rewrite (alg_opp_is_smul_neg1 B b).
  rewrite (alg_opp_is_smul_neg1 B (alg_mul B a b)).
  apply (alg_smul_mul_r B (-1) a b).
Qed.

Lemma alg_mul_opp_l (B : RAlgebra) (a b : carrier B) :
  alg_mul B (alg_opp B a) b = alg_opp B (alg_mul B a b).
Proof.
  rewrite (alg_opp_is_smul_neg1 B a).
  rewrite (alg_opp_is_smul_neg1 B (alg_mul B a b)).
  apply (alg_smul_mul_l B (-1) a b).
Qed.

Lemma cl02_hom_fn_one_v (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j H_one_v = alg_one B.
Proof. unfold H_one_v. apply cl02_hom_one. Qed.

Lemma cl02_hom_fn_i_v (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j H_i_v = j e1_02.
Proof.
  unfold cl02_hom_fn, H_i_v. simpl.
  repeat rewrite (alg_smul_0 B). repeat rewrite (alg_add_0_l B). repeat rewrite (alg_add_0_r B).
  rewrite (alg_smul_1 B (j e1_02)). reflexivity.
Qed.

Lemma cl02_hom_fn_j_v (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j H_j_v = j e2_02.
Proof.
  unfold cl02_hom_fn, H_j_v. simpl.
  repeat rewrite (alg_smul_0 B). repeat rewrite (alg_add_0_l B). repeat rewrite (alg_add_0_r B).
  rewrite (alg_smul_1 B (j e2_02)). reflexivity.
Qed.

Lemma cl02_hom_fn_k_v (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j H_k_v = alg_mul B (j e1_02) (j e2_02).
Proof.
  unfold cl02_hom_fn, H_k_v. simpl.
  repeat rewrite (alg_smul_0 B). repeat rewrite (alg_add_0_l B). repeat rewrite (alg_add_0_r B).
  rewrite (alg_smul_1 B (alg_mul B (j e1_02) (j e2_02))). reflexivity.
Qed.

Lemma H_basis_1_1 (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j (H_mul H_one_v H_one_v) = alg_mul B (cl02_hom_fn B j H_one_v) (cl02_hom_fn B j H_one_v).
Proof.
  assert (H : H_mul H_one_v H_one_v = H_one_v) by (apply H_eq; simpl; ring).
  rewrite H. repeat rewrite cl02_hom_fn_one_v.
  rewrite alg_mul_1_l. reflexivity.
Qed.

Lemma H_basis_1_i (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j (H_mul H_one_v H_i_v) = alg_mul B (cl02_hom_fn B j H_one_v) (cl02_hom_fn B j H_i_v).
Proof.
  assert (H : H_mul H_one_v H_i_v = H_i_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_fn_one_v. rewrite cl02_hom_fn_i_v.
  rewrite alg_mul_1_l. reflexivity.
Qed.

Lemma H_basis_1_j (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j (H_mul H_one_v H_j_v) = alg_mul B (cl02_hom_fn B j H_one_v) (cl02_hom_fn B j H_j_v).
Proof.
  assert (H : H_mul H_one_v H_j_v = H_j_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_fn_one_v. rewrite cl02_hom_fn_j_v.
  rewrite alg_mul_1_l. reflexivity.
Qed.

Lemma H_basis_1_k (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j (H_mul H_one_v H_k_v) = alg_mul B (cl02_hom_fn B j H_one_v) (cl02_hom_fn B j H_k_v).
Proof.
  assert (H : H_mul H_one_v H_k_v = H_k_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_fn_one_v. rewrite cl02_hom_fn_k_v.
  rewrite alg_mul_1_l. reflexivity.
Qed.

Lemma H_basis_i_1 (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j (H_mul H_i_v H_one_v) = alg_mul B (cl02_hom_fn B j H_i_v) (cl02_hom_fn B j H_one_v).
Proof.
  assert (H : H_mul H_i_v H_one_v = H_i_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_fn_i_v. rewrite cl02_hom_fn_one_v.
  rewrite alg_mul_1_r. reflexivity.
Qed.

Lemma H_basis_i_i (B : RAlgebra) (j : Vec 2 -> carrier B)
  (j_add : forall v w, j (vec_add v w) = alg_add B (j v) (j w))
  (Hj : forall v, alg_mul B (j v) (j v) = alg_smul B (Q_pq 0 2 v) (alg_one B)) :
  cl02_hom_fn B j (H_mul H_i_v H_i_v) = alg_mul B (cl02_hom_fn B j H_i_v) (cl02_hom_fn B j H_i_v).
Proof.
  assert (H : H_mul H_i_v H_i_v = H_smul (-1) H_one_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_smul. rewrite cl02_hom_fn_one_v. rewrite cl02_hom_fn_i_v.
  assert (He1 : alg_mul B (j e1_02) (j e1_02) = alg_smul B (-1) (alg_one B)).
  { assert (Htmp : Q_pq 0 2 e1_02 = -1). { rewrite Q_pq_0_2. apply e1_02_sq. } assert (Hj_e1 : alg_mul B (j e1_02) (j e1_02) = alg_smul B (Q_pq 0 2 e1_02) (alg_one B)) by apply Hj. rewrite Hj_e1. rewrite Htmp. reflexivity. }
  rewrite He1. reflexivity.
Qed.

Lemma H_basis_i_j (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j (H_mul H_i_v H_j_v) = alg_mul B (cl02_hom_fn B j H_i_v) (cl02_hom_fn B j H_j_v).
Proof.
  assert (H : H_mul H_i_v H_j_v = H_k_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_fn_i_v. rewrite cl02_hom_fn_j_v. rewrite cl02_hom_fn_k_v.
  reflexivity.
Qed.

Lemma H_basis_i_k (B : RAlgebra) (j : Vec 2 -> carrier B)
  (j_add : forall v w, j (vec_add v w) = alg_add B (j v) (j w))
  (Hj : forall v, alg_mul B (j v) (j v) = alg_smul B (Q_pq 0 2 v) (alg_one B)) :
  cl02_hom_fn B j (H_mul H_i_v H_k_v) = alg_mul B (cl02_hom_fn B j H_i_v) (cl02_hom_fn B j H_k_v).
Proof.
  assert (H : H_mul H_i_v H_k_v = H_smul (-1) H_j_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_smul. rewrite cl02_hom_fn_i_v. rewrite cl02_hom_fn_k_v.
  assert (Hac : alg_mul B (j e1_02) (alg_mul B (j e1_02) (j e2_02)) = alg_opp B (j e2_02)).
  { rewrite <- (alg_mul_assoc B (j e1_02) (j e1_02) (j e2_02)).
    assert (He1 : alg_mul B (j e1_02) (j e1_02) = alg_smul B (-1) (alg_one B)).
    { assert (Htmp : Q_pq 0 2 e1_02 = -1). { rewrite Q_pq_0_2. apply e1_02_sq. } assert (Hj_e1 : alg_mul B (j e1_02) (j e1_02) = alg_smul B (Q_pq 0 2 e1_02) (alg_one B)) by apply Hj. rewrite Hj_e1. rewrite Htmp. reflexivity. }
    rewrite He1. rewrite alg_smul_mul_l. rewrite alg_mul_1_l.
    rewrite alg_opp_is_smul_neg1. reflexivity. }
  rewrite Hac. rewrite cl02_hom_fn_j_v.
  rewrite alg_opp_is_smul_neg1. reflexivity.
Qed.

Lemma H_basis_j_1 (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j (H_mul H_j_v H_one_v) = alg_mul B (cl02_hom_fn B j H_j_v) (cl02_hom_fn B j H_one_v).
Proof.
  assert (H : H_mul H_j_v H_one_v = H_j_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_fn_j_v. rewrite cl02_hom_fn_one_v.
  rewrite alg_mul_1_r. reflexivity.
Qed.

Lemma H_basis_j_i (B : RAlgebra) (j : Vec 2 -> carrier B)
  (j_add : forall v w, j (vec_add v w) = alg_add B (j v) (j w))
  (Hj : forall v, alg_mul B (j v) (j v) = alg_smul B (Q_pq 0 2 v) (alg_one B)) :
  cl02_hom_fn B j (H_mul H_j_v H_i_v) = alg_mul B (cl02_hom_fn B j H_j_v) (cl02_hom_fn B j H_i_v).
Proof.
  assert (H : H_mul H_j_v H_i_v = H_smul (-1) H_k_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_smul. rewrite cl02_hom_fn_j_v. rewrite cl02_hom_fn_i_v. rewrite cl02_hom_fn_k_v.
  rewrite (cl02_j_anticomm B j j_add Hj).
  rewrite alg_opp_is_smul_neg1.
  rewrite <- alg_smul_mul.
  replace ((-1) * (-1)) with 1 by ring.
  rewrite alg_smul_1.
  reflexivity.
Qed.

Lemma H_basis_j_j (B : RAlgebra) (j : Vec 2 -> carrier B)
  (j_add : forall v w, j (vec_add v w) = alg_add B (j v) (j w))
  (Hj : forall v, alg_mul B (j v) (j v) = alg_smul B (Q_pq 0 2 v) (alg_one B)) :
  cl02_hom_fn B j (H_mul H_j_v H_j_v) = alg_mul B (cl02_hom_fn B j H_j_v) (cl02_hom_fn B j H_j_v).
Proof.
  assert (H : H_mul H_j_v H_j_v = H_smul (-1) H_one_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_smul. rewrite cl02_hom_fn_j_v. rewrite cl02_hom_fn_one_v.
  assert (He2 : alg_mul B (j e2_02) (j e2_02) = alg_smul B (-1) (alg_one B)).
  { assert (Htmp : Q_pq 0 2 e2_02 = -1). { rewrite Q_pq_0_2. apply e2_02_sq. } assert (Hj_e2 : alg_mul B (j e2_02) (j e2_02) = alg_smul B (Q_pq 0 2 e2_02) (alg_one B)) by apply Hj. rewrite Hj_e2. rewrite Htmp. reflexivity. }
  rewrite He2. reflexivity.
Qed.

Lemma H_basis_j_k (B : RAlgebra) (j : Vec 2 -> carrier B)
  (j_add : forall v w, j (vec_add v w) = alg_add B (j v) (j w))
  (Hj : forall v, alg_mul B (j v) (j v) = alg_smul B (Q_pq 0 2 v) (alg_one B)) :
  cl02_hom_fn B j (H_mul H_j_v H_k_v) = alg_mul B (cl02_hom_fn B j H_j_v) (cl02_hom_fn B j H_k_v).
Proof.
  assert (H : H_mul H_j_v H_k_v = H_i_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_fn_j_v. rewrite cl02_hom_fn_k_v. rewrite cl02_hom_fn_i_v.
  assert (Hac : alg_mul B (j e2_02) (alg_mul B (j e1_02) (j e2_02)) = j e1_02).
  { assert (Hanti2 : alg_mul B (j e2_02) (j e1_02) = alg_opp B (alg_mul B (j e1_02) (j e2_02))).
    { assert (Hanti : alg_mul B (j e1_02) (j e2_02) = alg_opp B (alg_mul B (j e2_02) (j e1_02))) by (apply cl02_j_anticomm; assumption).
      apply (f_equal (alg_opp B)) in Hanti.
      rewrite alg_opp_opp in Hanti.
      symmetry in Hanti. exact Hanti. }
    rewrite <- (alg_mul_assoc B (j e2_02) (j e1_02) (j e2_02)).
    rewrite Hanti2. rewrite alg_mul_opp_l.
    assert (Hjk : alg_mul B (alg_mul B (j e1_02) (j e2_02)) (j e2_02) = alg_opp B (j e1_02)).
    { rewrite (alg_mul_assoc B (j e1_02) (j e2_02) (j e2_02)).
      assert (He2 : alg_mul B (j e2_02) (j e2_02) = alg_smul B (-1) (alg_one B)).
      { assert (Htmp : Q_pq 0 2 e2_02 = -1). { rewrite Q_pq_0_2. apply e2_02_sq. } assert (Hj_e2 : alg_mul B (j e2_02) (j e2_02) = alg_smul B (Q_pq 0 2 e2_02) (alg_one B)) by apply Hj. rewrite Hj_e2. rewrite Htmp. reflexivity. }
      rewrite He2. rewrite alg_smul_mul_r. rewrite alg_mul_1_r.
      rewrite alg_opp_is_smul_neg1. reflexivity. }
    rewrite Hjk. apply alg_opp_opp. }
  rewrite Hac. reflexivity.
Qed.

Lemma H_basis_k_1 (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j (H_mul H_k_v H_one_v) = alg_mul B (cl02_hom_fn B j H_k_v) (cl02_hom_fn B j H_one_v).
Proof.
  assert (H : H_mul H_k_v H_one_v = H_k_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_fn_k_v. rewrite cl02_hom_fn_one_v.
  rewrite alg_mul_1_r. reflexivity.
Qed.

Lemma H_basis_k_i (B : RAlgebra) (j : Vec 2 -> carrier B)
  (j_add : forall v w, j (vec_add v w) = alg_add B (j v) (j w))
  (Hj : forall v, alg_mul B (j v) (j v) = alg_smul B (Q_pq 0 2 v) (alg_one B)) :
  cl02_hom_fn B j (H_mul H_k_v H_i_v) = alg_mul B (cl02_hom_fn B j H_k_v) (cl02_hom_fn B j H_i_v).
Proof.
  assert (H : H_mul H_k_v H_i_v = H_j_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_fn_k_v. rewrite cl02_hom_fn_i_v. rewrite cl02_hom_fn_j_v.
  assert (Hanti : alg_mul B (j e1_02) (j e2_02) = alg_opp B (alg_mul B (j e2_02) (j e1_02))) by (apply cl02_j_anticomm; assumption).
  rewrite Hanti.
  rewrite alg_mul_opp_l.
  rewrite (alg_mul_assoc B (j e2_02) (j e1_02) (j e1_02)).
  assert (He1 : alg_mul B (j e1_02) (j e1_02) = alg_smul B (-1) (alg_one B)).
  { assert (Htmp : Q_pq 0 2 e1_02 = -1). { rewrite Q_pq_0_2. apply e1_02_sq. } assert (Hj_e1 : alg_mul B (j e1_02) (j e1_02) = alg_smul B (Q_pq 0 2 e1_02) (alg_one B)) by apply Hj. rewrite Hj_e1. rewrite Htmp. reflexivity. }
  rewrite He1. rewrite alg_smul_mul_r. rewrite alg_mul_1_r.
  rewrite alg_opp_is_smul_neg1.
  rewrite <- alg_smul_mul.
  replace ((-1) * (-1)) with 1 by ring.
  rewrite alg_smul_1.
  reflexivity.
Qed.

Lemma H_basis_k_j (B : RAlgebra) (j : Vec 2 -> carrier B)
  (j_add : forall v w, j (vec_add v w) = alg_add B (j v) (j w))
  (Hj : forall v, alg_mul B (j v) (j v) = alg_smul B (Q_pq 0 2 v) (alg_one B)) :
  cl02_hom_fn B j (H_mul H_k_v H_j_v) = alg_mul B (cl02_hom_fn B j H_k_v) (cl02_hom_fn B j H_j_v).
Proof.
  assert (H : H_mul H_k_v H_j_v = H_smul (-1) H_i_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_smul. rewrite cl02_hom_fn_k_v. rewrite cl02_hom_fn_j_v. rewrite cl02_hom_fn_i_v.
  assert (Hjk : alg_mul B (alg_mul B (j e1_02) (j e2_02)) (j e2_02) = alg_opp B (j e1_02)).
  { rewrite (alg_mul_assoc B (j e1_02) (j e2_02) (j e2_02)).
    assert (He2 : alg_mul B (j e2_02) (j e2_02) = alg_smul B (-1) (alg_one B)).
    { assert (Htmp : Q_pq 0 2 e2_02 = -1). { rewrite Q_pq_0_2. apply e2_02_sq. } assert (Hj_e2 : alg_mul B (j e2_02) (j e2_02) = alg_smul B (Q_pq 0 2 e2_02) (alg_one B)) by apply Hj. rewrite Hj_e2. rewrite Htmp. reflexivity. }
    rewrite He2. rewrite alg_smul_mul_r. rewrite alg_mul_1_r.
    rewrite alg_opp_is_smul_neg1. reflexivity. }
  rewrite Hjk. rewrite alg_opp_is_smul_neg1. reflexivity.
Qed.

Lemma H_basis_k_k (B : RAlgebra) (j : Vec 2 -> carrier B)
  (j_add : forall v w, j (vec_add v w) = alg_add B (j v) (j w))
  (Hj : forall v, alg_mul B (j v) (j v) = alg_smul B (Q_pq 0 2 v) (alg_one B)) :
  cl02_hom_fn B j (H_mul H_k_v H_k_v) = alg_mul B (cl02_hom_fn B j H_k_v) (cl02_hom_fn B j H_k_v).
Proof.
  assert (H : H_mul H_k_v H_k_v = H_smul (-1) H_one_v) by (apply H_eq; simpl; ring).
  rewrite H. rewrite cl02_hom_smul. rewrite cl02_hom_fn_k_v. rewrite cl02_hom_fn_one_v.
  assert (Hjk_sq : alg_mul B (alg_mul B (j e1_02) (j e2_02)) (alg_mul B (j e1_02) (j e2_02)) = alg_smul B (-1) (alg_one B)).
  { assert (Hjk_je1 : alg_mul B (alg_mul B (j e1_02) (j e2_02)) (j e1_02) = j e2_02).
    { assert (Hanti : alg_mul B (j e1_02) (j e2_02) = alg_opp B (alg_mul B (j e2_02) (j e1_02))) by (apply cl02_j_anticomm; assumption).
      rewrite Hanti.
      rewrite alg_mul_opp_l.
      rewrite (alg_mul_assoc B (j e2_02) (j e1_02) (j e1_02)).
      assert (He1 : alg_mul B (j e1_02) (j e1_02) = alg_smul B (-1) (alg_one B)).
      { assert (Htmp : Q_pq 0 2 e1_02 = -1). { rewrite Q_pq_0_2. apply e1_02_sq. } assert (Hj_e1 : alg_mul B (j e1_02) (j e1_02) = alg_smul B (Q_pq 0 2 e1_02) (alg_one B)) by apply Hj. rewrite Hj_e1. rewrite Htmp. reflexivity. }
      rewrite He1. rewrite alg_smul_mul_r. rewrite alg_mul_1_r.
      rewrite alg_opp_is_smul_neg1.
      rewrite <- alg_smul_mul.
      replace ((-1) * (-1)) with 1 by ring.
      rewrite alg_smul_1.
      reflexivity. }
    rewrite <- (alg_mul_assoc B (alg_mul B (j e1_02) (j e2_02)) (j e1_02) (j e2_02)).
    rewrite Hjk_je1.
    assert (He2 : alg_mul B (j e2_02) (j e2_02) = alg_smul B (-1) (alg_one B)).
    { assert (Htmp : Q_pq 0 2 e2_02 = -1). { rewrite Q_pq_0_2. apply e2_02_sq. } assert (Hj_e2 : alg_mul B (j e2_02) (j e2_02) = alg_smul B (Q_pq 0 2 e2_02) (alg_one B)) by apply Hj. rewrite Hj_e2. rewrite Htmp. reflexivity. }
    rewrite He2. reflexivity. }
  rewrite Hjk_sq. reflexivity.
Qed.

Lemma cl02_hom_mul (B : RAlgebra) (j : Vec 2 -> carrier B)
  (j_add : forall v w, j (vec_add v w) = alg_add B (j v) (j w))
  (Hj : forall v, alg_mul B (j v) (j v) = alg_smul B (Q_pq 0 2 v) (alg_one B)) :
  forall x y, cl02_hom_fn B j (H_mul x y) = alg_mul B (cl02_hom_fn B j x) (cl02_hom_fn B j y).
Proof.
  intros x y.
  assert (Hone : forall y, cl02_hom_fn B j (H_mul H_one_v y) = alg_mul B (cl02_hom_fn B j H_one_v) (cl02_hom_fn B j y)).
  { intros y'.
    assert (Hy' : y' = H_add (H_smul (h_re y') H_one_v) (H_add (H_smul (h_i y') H_i_v) (H_add (H_smul (h_j y') H_j_v) (H_smul (h_k y') H_k_v)))) by (apply H_eq; simpl; ring).
    rewrite Hy'.
    repeat (first [rewrite H_mul_linear_r | rewrite H_mul_smul_r]).
    repeat (first [rewrite cl02_hom_add | rewrite cl02_hom_smul]).
    repeat (first [rewrite alg_distr_l | rewrite alg_smul_mul_r]).
    rewrite H_basis_1_1.
    rewrite H_basis_1_i.
    rewrite H_basis_1_j.
    rewrite H_basis_1_k.
    reflexivity. }
  assert (Hi : forall y, cl02_hom_fn B j (H_mul H_i_v y) = alg_mul B (cl02_hom_fn B j H_i_v) (cl02_hom_fn B j y)).
  { intros y'.
    assert (Hy' : y' = H_add (H_smul (h_re y') H_one_v) (H_add (H_smul (h_i y') H_i_v) (H_add (H_smul (h_j y') H_j_v) (H_smul (h_k y') H_k_v)))) by (apply H_eq; simpl; ring).
    rewrite Hy'.
    repeat (first [rewrite H_mul_linear_r | rewrite H_mul_smul_r]).
    repeat (first [rewrite cl02_hom_add | rewrite cl02_hom_smul]).
    repeat (first [rewrite alg_distr_l | rewrite alg_smul_mul_r]).
    rewrite H_basis_i_1.
    rewrite (H_basis_i_i B j j_add Hj).
    rewrite H_basis_i_j.
    rewrite (H_basis_i_k B j j_add Hj).
    reflexivity. }
  assert (Hj_v : forall y, cl02_hom_fn B j (H_mul H_j_v y) = alg_mul B (cl02_hom_fn B j H_j_v) (cl02_hom_fn B j y)).
  { intros y'.
    assert (Hy' : y' = H_add (H_smul (h_re y') H_one_v) (H_add (H_smul (h_i y') H_i_v) (H_add (H_smul (h_j y') H_j_v) (H_smul (h_k y') H_k_v)))) by (apply H_eq; simpl; ring).
    rewrite Hy'.
    repeat (first [rewrite H_mul_linear_r | rewrite H_mul_smul_r]).
    repeat (first [rewrite cl02_hom_add | rewrite cl02_hom_smul]).
    repeat (first [rewrite alg_distr_l | rewrite alg_smul_mul_r]).
    rewrite H_basis_j_1.
    rewrite (H_basis_j_i B j j_add Hj).
    rewrite (H_basis_j_j B j j_add Hj).
    rewrite (H_basis_j_k B j j_add Hj).
    reflexivity. }
  assert (Hk : forall y, cl02_hom_fn B j (H_mul H_k_v y) = alg_mul B (cl02_hom_fn B j H_k_v) (cl02_hom_fn B j y)).
  { intros y'.
    assert (Hy' : y' = H_add (H_smul (h_re y') H_one_v) (H_add (H_smul (h_i y') H_i_v) (H_add (H_smul (h_j y') H_j_v) (H_smul (h_k y') H_k_v)))) by (apply H_eq; simpl; ring).
    rewrite Hy'.
    repeat (first [rewrite H_mul_linear_r | rewrite H_mul_smul_r]).
    repeat (first [rewrite cl02_hom_add | rewrite cl02_hom_smul]).
    repeat (first [rewrite alg_distr_l | rewrite alg_smul_mul_r]).
    rewrite H_basis_k_1.
    rewrite (H_basis_k_i B j j_add Hj).
    rewrite (H_basis_k_j B j j_add Hj).
    rewrite (H_basis_k_k B j j_add Hj).
    reflexivity. }
  assert (Hx : x = H_add (H_smul (h_re x) H_one_v) (H_add (H_smul (h_i x) H_i_v) (H_add (H_smul (h_j x) H_j_v) (H_smul (h_k x) H_k_v)))) by (apply H_eq; simpl; ring).
  rewrite Hx.
  repeat (first [rewrite H_mul_linear_l | rewrite H_mul_smul_l]).
  repeat (first [rewrite cl02_hom_add | rewrite cl02_hom_smul]).
  repeat rewrite alg_distr_r.
  repeat rewrite alg_smul_mul_l.
  rewrite Hone.
  rewrite Hi.
  rewrite Hj_v.
  rewrite Hk.
  reflexivity.
Qed.
Lemma cl02_hom_i (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j (mkH 0 1 0 0) = j e1_02.
Proof.
  unfold cl02_hom_fn. simpl.
  rewrite alg_smul_1.
  repeat rewrite alg_smul_0.
  rewrite (alg_add_0_l B). rewrite (alg_add_0_l B).
  rewrite (alg_add_comm B). rewrite (alg_add_0_l B).
  reflexivity.
Qed.

Lemma cl02_hom_j (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j (mkH 0 0 1 0) = j e2_02.
Proof.
  unfold cl02_hom_fn. simpl.
  rewrite alg_smul_1.
  repeat rewrite alg_smul_0.
  rewrite (alg_add_0_l B). rewrite (alg_add_0_l B).
  rewrite (alg_add_comm B). rewrite (alg_add_0_l B).
  reflexivity.
Qed.

Lemma cl02_hom_k (B : RAlgebra) (j : Vec 2 -> carrier B) :
  cl02_hom_fn B j (mkH 0 0 0 1) = alg_mul B (j e1_02) (j e2_02).
Proof.
  unfold cl02_hom_fn. simpl.
  rewrite alg_smul_1.
  repeat rewrite alg_smul_0.
  rewrite (alg_add_0_l B). rewrite (alg_add_0_l B). rewrite (alg_add_0_l B).
  reflexivity.
Qed.

Lemma i_02_e1 : i_02 e1_02 = mkH 0 1 0 0.
Proof.
  unfold i_02, e1_02. simpl.
  apply H_eq; simpl; ring.
Qed.

Lemma i_02_e2 : i_02 e2_02 = mkH 0 0 1 0.
Proof.
  unfold i_02, e2_02. simpl.
  apply H_eq; simpl; ring.
Qed.

Lemma cl02_hom_factor (B : RAlgebra) (j : Vec 2 -> carrier B)
  (j_add : forall v w, j (vec_add v w) = alg_add B (j v) (j w))
  (j_smul : forall r v, j (vec_smul r v) = alg_smul B r (j v)) :
  forall v, cl02_hom_fn B j (i_02 v) = j v.
Proof.
  intro v.
  assert (Hv : v = vec_add (vec_smul (v (mkFin 0%nat zero_lt_two)) e1_02) (vec_smul (v (mkFin 1%nat one_lt_two)) e2_02)).
  { apply functional_extensionality. intro i.
    unfold vec_add, vec_smul, e1_02, e2_02.
    destruct (fin_val i) as [| n] eqn:Ei.
    - assert (Hi : i = mkFin 0 zero_lt_two) by (apply fin_val_eq; exact Ei).
      rewrite Hi. simpl. ring.
    - destruct n as [| m].
      + assert (Hi : i = mkFin 1 one_lt_two) by (apply fin_val_eq; exact Ei).
        rewrite Hi. simpl. ring.
      + exfalso. destruct i as [fi Hfi]. simpl in *. lia. }
  rewrite Hv.
  rewrite i_02_linear. rewrite i_02_smul. rewrite i_02_smul.
  rewrite cl02_hom_add. rewrite cl02_hom_smul. rewrite cl02_hom_smul.
  rewrite i_02_e1, i_02_e2.
  rewrite cl02_hom_i, cl02_hom_j.
  rewrite <- j_smul, <- j_smul.
  rewrite <- j_add.
  reflexivity.
Qed.

(******************************************************************************)
(* Section 7: Universal property and uniqueness                               *)
(******************************************************************************)

Lemma cl02_univ :
  forall (B : RAlgebra) (j : Vec 2 -> carrier B),
    (forall v w, j (vec_add v w) = alg_add B (j v) (j w)) ->
    (forall r v, j (vec_smul r v) = alg_smul B r (j v)) ->
    (forall v, alg_mul B (j v) (j v) = alg_smul B (Q_pq 0 2 v) (alg_one B)) ->
    { f : AlgHom H_RAlgebra B
      | forall v, hom_fn f (i_02 v) = j v }.
Proof.
  intros B j j_add j_smul Hj.
  exists (Build_AlgHom H_RAlgebra B (cl02_hom_fn B j)
    (cl02_hom_zero B j)
    (cl02_hom_one B j)
    (cl02_hom_add B j)
    (cl02_hom_mul B j j_add Hj)
    (cl02_hom_smul B j)).
  apply cl02_hom_factor; assumption.
Qed.

Lemma cl02_univ_unique :
  forall (B : RAlgebra) (j : Vec 2 -> carrier B)
         (f1 f2 : AlgHom H_RAlgebra B),
    (forall v, hom_fn f1 (i_02 v) = j v) ->
    (forall v, hom_fn f2 (i_02 v) = j v) ->
    forall x, hom_fn f1 x = hom_fn f2 x.
Proof.
  intros B j f1 f2 H1 H2 [a b c d].
  assert (Hdecomp : mkH a b c d = alg_add H_RAlgebra (alg_smul H_RAlgebra a (alg_one H_RAlgebra)) (alg_add H_RAlgebra (alg_smul H_RAlgebra b (i_02 e1_02)) (alg_add H_RAlgebra (alg_smul H_RAlgebra c (i_02 e2_02)) (alg_smul H_RAlgebra d (alg_mul H_RAlgebra (i_02 e1_02) (i_02 e2_02)))))).
  { rewrite i_02_e1, i_02_e2.
    unfold alg_one, alg_smul, alg_mul, alg_add. simpl.
    apply H_eq; simpl; ring. }
  rewrite Hdecomp.
  repeat rewrite (hom_add f1). repeat rewrite (hom_add f2).
  repeat rewrite (hom_smul f1). repeat rewrite (hom_smul f2).
  repeat rewrite (hom_one f1). repeat rewrite (hom_one f2).
  assert (Hi1 : hom_fn f1 (i_02 e1_02) = hom_fn f2 (i_02 e1_02)) by (rewrite H1, H2; reflexivity).
  assert (Hi2 : hom_fn f1 (i_02 e2_02) = hom_fn f2 (i_02 e2_02)) by (rewrite H1, H2; reflexivity).
  rewrite Hi1, Hi2.
  assert (Hik : hom_fn f1 (alg_mul H_RAlgebra (i_02 e1_02) (i_02 e2_02)) = hom_fn f2 (alg_mul H_RAlgebra (i_02 e1_02) (i_02 e2_02))).
  { rewrite (hom_mul f1). rewrite (hom_mul f2). rewrite Hi1, Hi2. reflexivity. }
  rewrite Hik. reflexivity.
Qed.

Definition Cl02_spec : CliffordSpec 0 2.
Proof.
  refine (Build_CliffordSpec 0 2 H_RAlgebra i_02 i_02_zero i_02_linear i_02_smul _ cl02_univ cl02_univ_unique).
  intro v. rewrite Q_pq_0_2. apply i_02_cl_sq.
Defined.

(******************************************************************************)
(* Section 8: Universal property theorem                                      *)
(******************************************************************************)

Theorem Cl02_universal_property (A : RAlgebra)
  (f : Vec 2 -> carrier A)
  (f_linear : forall v w, f (vec_add v w) = alg_add A (f v) (f w))
  (f_smul : forall r v, f (vec_smul r v) = alg_smul A r (f v))
  (f_clifford : forall v, alg_mul A (f v) (f v) = alg_smul A (Q_02 v) (alg_one A)) :
  exists (f_tilde : AlgHom (cl_alg Cl02_spec) A),
    forall v, hom_fn f_tilde (cl_inc Cl02_spec v) = f v.
Proof.
  assert (Hf : forall v, alg_mul A (f v) (f v) = alg_smul A (Q_pq 0 2 v) (alg_one A)).
  { intro v. rewrite Q_pq_0_2. apply f_clifford. }
  destruct (cl02_univ A f f_linear f_smul Hf) as [g Hg].
  exists g. exact Hg.
Qed.

(******************************************************************************)
(* Section 9: Honesty summary                                                 *)
(******************************************************************************)

(*
  Proved (Qed):
    - H_RAlgebra satisfies all 13 RAlgebra axioms
    - Cl02_spec is a valid CliffordSpec 0 2
    - The explicit injection i_02(v) = v₀·i + v₁·j satisfies the Clifford relation
    - Q_pq_0_2: equality of Q_pq 0 2 with Q_02
    - cl02_univ / cl02_univ_unique: universal property of Cl(0,2)
    - Cl02_universal_property: explicit algebra homomorphism construction

  Remaining admitted in Track B:
    - Cl6_iso_M8R.v: Cl(0,6) ≅ M₈(ℝ) (64-dim, scale-up from ℍ pattern)
    - Cl8_periodicity.v: Bott periodicity for Cl(8,0)
    - ChiralityAnalysis.v: chiral operator properties
*)

Close Scope R_scope.
