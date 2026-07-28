From Coq Require Import Reals Lia Lra FunctionalExtensionality Psatz.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Definition f0 : Fin 8. refine (mkFin 0 _). lia. Defined.
Definition f1 : Fin 8. refine (mkFin 1 _). lia. Defined.
Definition f2 : Fin 8. refine (mkFin 2 _). lia. Defined.
Definition f3 : Fin 8. refine (mkFin 3 _). lia. Defined.
Definition f4 : Fin 8. refine (mkFin 4 _). lia. Defined.
Definition f5 : Fin 8. refine (mkFin 5 _). lia. Defined.
Definition f6 : Fin 8. refine (mkFin 6 _). lia. Defined.
Definition f7 : Fin 8. refine (mkFin 7 _). lia. Defined.

Lemma fin_nat_8_0 : fin_nat (Nat.lt_0_succ 7) 0 = f0.
Proof. apply fin_val_eq. simpl. reflexivity. Qed.
Lemma fin_nat_8_1 : fin_nat (Nat.lt_0_succ 7) 1 = f1.
Proof. apply fin_val_eq. simpl. reflexivity. Qed.
Lemma fin_nat_8_2 : fin_nat (Nat.lt_0_succ 7) 2 = f2.
Proof. apply fin_val_eq. simpl. reflexivity. Qed.
Lemma fin_nat_8_3 : fin_nat (Nat.lt_0_succ 7) 3 = f3.
Proof. apply fin_val_eq. simpl. reflexivity. Qed.
Lemma fin_nat_8_4 : fin_nat (Nat.lt_0_succ 7) 4 = f4.
Proof. apply fin_val_eq. simpl. reflexivity. Qed.
Lemma fin_nat_8_5 : fin_nat (Nat.lt_0_succ 7) 5 = f5.
Proof. apply fin_val_eq. simpl. reflexivity. Qed.
Lemma fin_nat_8_6 : fin_nat (Nat.lt_0_succ 7) 6 = f6.
Proof. apply fin_val_eq. simpl. reflexivity. Qed.
Lemma fin_nat_8_7 : fin_nat (Nat.lt_0_succ 7) 7 = f7.
Proof. apply fin_val_eq. simpl. reflexivity. Qed.

Definition mat_mul_8 (A B : Mat 8) : Mat 8 := fun i j =>
  A i f0 * B f0 j +
  A i f1 * B f1 j +
  A i f2 * B f2 j +
  A i f3 * B f3 j +
  A i f4 * B f4 j +
  A i f5 * B f5 j +
  A i f6 * B f6 j +
  A i f7 * B f7 j.

Lemma mat_mul_8_eq : forall A B, mat_mul_8 A B = mat_mul A B.
Proof.
  intros A B.
  apply functional_extensionality; intros i.
  apply functional_extensionality; intros j.
  unfold mat_mul_8, mat_mul, mat_mul_aux.
  do 7 (rewrite sum_R_S).
  simpl.
  rewrite fin_nat_8_7, fin_nat_8_6, fin_nat_8_5, fin_nat_8_4.
  rewrite fin_nat_8_3, fin_nat_8_2, fin_nat_8_1, fin_nat_8_0.
  ring.
Qed.

Definition gamma_1 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 1 => -1 | 1, 0 => 1 | 2, 3 => -1 | 3, 2 => 1
  | 4, 5 => -1 | 5, 4 => 1 | 6, 7 => -1 | 7, 6 => 1
  | _, _ => 0
  end.

Definition gamma_2 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 3 => -1 | 1, 2 => -1 | 2, 1 => 1 | 3, 0 => 1
  | 4, 7 => -1 | 5, 6 => -1 | 6, 5 => 1 | 7, 4 => 1
  | _, _ => 0
  end.

Ltac prove_gamma_sq g :=
  apply functional_extensionality; intros i;
  apply functional_extensionality; intros j;
  unfold mat_mul_8, g, mat_one, mat_opp;
  destruct (fin_val i) eqn:?;
    try (destruct n as [|n1]; try lia;
         destruct n1 as [|n2]; try lia;
         destruct n2 as [|n3]; try lia;
         destruct n3 as [|n4]; try lia;
         destruct n4 as [|n5]; try lia;
         destruct n5 as [|n6]; try lia;
         destruct n6 as [|n7]; try lia;
         destruct n7 as [|n8]; try lia);
  destruct (fin_val j) eqn:?;
    try (destruct n0 as [|n1]; try lia;
         destruct n1 as [|n2]; try lia;
         destruct n2 as [|n3]; try lia;
         destruct n3 as [|n4]; try lia;
         destruct n4 as [|n5]; try lia;
         destruct n5 as [|n6]; try lia;
         destruct n6 as [|n7]; try lia;
         destruct n7 as [|n8]; try lia);
  simpl; ring.

Lemma gamma_1_sq : mat_mul_8 gamma_1 gamma_1 = mat_opp (mat_one 8).
Proof. prove_gamma_sq gamma_1. Qed.

Lemma gamma_2_sq : mat_mul_8 gamma_2 gamma_2 = mat_opp (mat_one 8).
Proof. prove_gamma_sq gamma_2. Qed.
