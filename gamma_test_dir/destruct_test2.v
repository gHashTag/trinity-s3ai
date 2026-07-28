From Coq Require Import Reals Lia.
From CliffordCl8 Require Import CliffordAlgebra.
Open Scope R_scope.

Lemma test_destruct (i : Fin 8) :
  fin_val i = fin_val i.
Proof.
  destruct (fin_val i) as [|n1].
  - reflexivity.
  - destruct n1 as [|n2]; try reflexivity.
    destruct n2 as [|n3]; try reflexivity.
    destruct n3 as [|n4]; try reflexivity.
    destruct n4 as [|n5]; try reflexivity.
    destruct n5 as [|n6]; try reflexivity.
    destruct n6 as [|n7]; try reflexivity.
    destruct n7 as [|n8]; try reflexivity.
    destruct n8 as [|n9]; try reflexivity.
    reflexivity.
Qed.
