(** * The golden weight alphabet, machine-checked.

    A ternary network multiplies by weights drawn from a three-symbol alphabet
    {-r, 0, +r}.  For the datapath to contain no multiplier, the product of a
    weight with a value must fall back into the lattice the datapath already
    forms by addition.  Written down, that requirement is r^2 = r + 1.

    Three results are proved here:

      1. [phi_quadratic] and [phi_unique] -- the base is forced, not chosen.
      2. [mulphi_correct], [addp_correct] -- integer pairs realise the arithmetic
         exactly, with one integer addition per weight and no shift.
      3. [dot_exact] -- the ENTIRE linear path of such a network, at arbitrary
         fan-in, equals the real-valued result with no rounding error at all.

    Result 3 is the one that matters: elsewhere formats are compared by the size
    of their error, and here there is no error to compare. *)

Require Import Reals.
Require Import Lra.
Require Import List.
Import ListNotations.
Open Scope R_scope.

Definition phi : R := (1 + sqrt 5) / 2.

Lemma sqrt5_sq : sqrt 5 * sqrt 5 = 5.
Proof. apply sqrt_sqrt. lra. Qed.

Lemma sqrt5_gt2 : sqrt 5 > 2.
Proof.
  assert (H0 : 0 <= sqrt 5) by apply sqrt_pos.
  assert (H := sqrt5_sq).
  nra.
Qed.

(** ** 1. The base is forced *)

Lemma phi_quadratic : phi * phi = phi + 1.
Proof. unfold phi. assert (H := sqrt5_sq). nra. Qed.

Theorem phi_unique :
  forall r : R, r > 1 -> r * r = r + 1 -> r = phi.
Proof.
  intros r Hr Hq.
  assert (H := sqrt5_sq).
  assert (H2 := sqrt5_gt2).
  assert (Hfac : (r - phi) * (r - (1 - sqrt 5) / 2) = 0) by (unfold phi; nra).
  assert (Hne : r - (1 - sqrt 5) / 2 <> 0) by (unfold phi in *; nra).
  apply Rminus_diag_uniq.
  destruct (Rmult_integral _ _ Hfac) as [Hl | Hr']; [exact Hl | contradiction].
Qed.

(** ** 2. Integer pairs realise the arithmetic exactly *)

Definition Zphi : Type := (Z * Z)%type.

Definition val (p : Zphi) : R := IZR (fst p) + IZR (snd p) * phi.

(** Multiplying by phi is the Fibonacci step: one integer addition, no shift. *)
Definition mulphi (p : Zphi) : Zphi := (snd p, (fst p + snd p)%Z).
Definition addp (p q : Zphi) : Zphi := ((fst p + fst q)%Z, (snd p + snd q)%Z).
Definition negp (p : Zphi) : Zphi := ((- fst p)%Z, (- snd p)%Z).

Theorem mulphi_correct : forall p, val (mulphi p) = phi * val p.
Proof.
  intros [a b]. unfold val, mulphi. simpl.
  rewrite plus_IZR.
  replace (phi * (IZR a + IZR b * phi))
     with (phi * IZR a + IZR b * (phi * phi)) by ring.
  rewrite phi_quadratic. ring.
Qed.

Theorem addp_correct : forall p q, val (addp p q) = val p + val q.
Proof.
  intros [a b] [c d]. unfold val, addp. simpl.
  rewrite !plus_IZR. lra.
Qed.

Theorem negp_correct : forall p, val (negp p) = - val p.
Proof.
  intros [a b]. unfold val, negp. simpl.
  rewrite !opp_IZR. lra.
Qed.

(** ** 3. The whole linear path is exact *)

Inductive W : Type := Wneg | Wzero | Wpos.   (* -phi, 0, +phi *)

Definition applyw (w : W) (x : Zphi) : Zphi :=
  match w with
  | Wpos  => mulphi x
  | Wneg  => negp (mulphi x)
  | Wzero => (0%Z, 0%Z)
  end.

Definition rapplyw (w : W) (x : R) : R :=
  match w with
  | Wpos  => phi * x
  | Wneg  => - (phi * x)
  | Wzero => 0
  end.

Fixpoint dot (ws : list W) (xs : list Zphi) : Zphi :=
  match ws, xs with
  | w :: ws', x :: xs' => addp (applyw w x) (dot ws' xs')
  | _, _ => (0%Z, 0%Z)
  end.

Fixpoint rdot (ws : list W) (xs : list Zphi) : R :=
  match ws, xs with
  | w :: ws', x :: xs' => rapplyw w (val x) + rdot ws' xs'
  | _, _ => 0
  end.

Lemma val_zero : val (0%Z, 0%Z) = 0.
Proof. unfold val. simpl. lra. Qed.

Lemma applyw_correct : forall w x, val (applyw w x) = rapplyw w (val x).
Proof.
  intros [] x; simpl.
  - rewrite negp_correct, mulphi_correct. lra.
  - apply val_zero.
  - apply mulphi_correct.
Qed.

(** The headline: an accumulator of two exact integer registers reproduces the
    real-valued layer output for ANY fan-in and ANY weight pattern.  Nothing in
    the datapath rounds. *)
Theorem dot_exact : forall ws xs, val (dot ws xs) = rdot ws xs.
Proof.
  induction ws as [| w ws IH]; intros [| x xs]; simpl;
    try apply val_zero.
  rewrite addp_correct, applyw_correct, IH. reflexivity.
Qed.

(** ** Corollary: depth is free of multipliers.

    The gain of k stacked layers is F_k * phi + F_(k-1), a pair of integers, so
    rescaling between layers is a shift-and-add rather than a multiplication. *)

Fixpoint fib (n : nat) : Z :=
  match n with
  | 0 => 0%Z
  | S k => match k with
           | 0 => 1%Z
           | S j => (fib k + fib j)%Z
           end
  end.

Fixpoint phipow (n : nat) : R :=
  match n with 0 => 1 | S k => phi * phipow k end.

Theorem phi_pow_fib :
  forall n, phipow (S n) = IZR (fib (S n)) * phi + IZR (fib n).
Proof.
  induction n as [| n IH].
  - simpl. lra.
  - replace (phipow (S (S n))) with (phi * phipow (S n)) by reflexivity.
    rewrite IH.
    replace (fib (S (S n))) with (fib (S n) + fib n)%Z by reflexivity.
    rewrite plus_IZR.
    replace (phi * (IZR (fib (S n)) * phi + IZR (fib n)))
       with (IZR (fib (S n)) * (phi * phi) + phi * IZR (fib n)) by ring.
    rewrite phi_quadratic. ring.
Qed.
