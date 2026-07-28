From Coq Require Import Reals Lia.
From CliffordCl8 Require Import CliffordAlgebra.
Open Scope R_scope.

Ltac destruct_fin8 x :=
  destruct x as [|n1]; [ | destruct n1 as [|n2]; [ | destruct n2 as [|n3]; [ | destruct n3 as [|n4]; [ | destruct n4 as [|n5]; [ | destruct n5 as [|n6]; [ | destruct n6 as [|n7]; [ | destruct n7 as [|n8]; [ | idtac ] ] ] ] ] ] ] ].

Lemma test_destruct2 (i : Fin 8) :
  fin_val i = fin_val i.
Proof.
  destruct_fin8 (fin_val i).
  all: reflexivity.
Qed.
