From Coq Require Import Reals Lia Lra FunctionalExtensionality Psatz.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Definition gamma_1 : Mat 8 := fun i j =>
  match i, j with
  | mkFin 0 _, mkFin 1 _ => -1 | mkFin 1 _, mkFin 0 _ => 1
  | mkFin 2 _, mkFin 3 _ => -1 | mkFin 3 _, mkFin 2 _ => 1
  | mkFin 4 _, mkFin 5 _ => -1 | mkFin 5 _, mkFin 4 _ => 1
  | mkFin 6 _, mkFin 7 _ => -1 | mkFin 7 _, mkFin 6 _ => 1
  | _, _ => 0 end.

Definition gamma_2 : Mat 8 := fun i j =>
  match i, j with
  | mkFin 0 _, mkFin 3 _ => -1 | mkFin 1 _, mkFin 2 _ => -1
  | mkFin 2 _, mkFin 1 _ => 1 | mkFin 3 _, mkFin 0 _ => 1
  | mkFin 4 _, mkFin 7 _ => -1 | mkFin 5 _, mkFin 6 _ => -1
  | mkFin 6 _, mkFin 5 _ => 1 | mkFin 7 _, mkFin 4 _ => 1
  | _, _ => 0 end.

Definition gamma_3 : Mat 8 := fun i j =>
  match i, j with
  | mkFin 0 _, mkFin 6 _ => -1 | mkFin 1 _, mkFin 7 _ => 1
  | mkFin 2 _, mkFin 4 _ => 1 | mkFin 3 _, mkFin 5 _ => -1
  | mkFin 4 _, mkFin 2 _ => -1 | mkFin 5 _, mkFin 3 _ => 1
  | mkFin 6 _, mkFin 0 _ => 1 | mkFin 7 _, mkFin 1 _ => -1
  | _, _ => 0 end.

Ltac destruct_fin8 x :=
  let H := fresh "H" in
  destruct x as [x H];
  destruct x as [|x]; [ idtac |
    destruct x as [|x]; [ idtac |
      destruct x as [|x]; [ idtac |
        destruct x as [|x]; [ idtac |
          destruct x as [|x]; [ idtac |
            destruct x as [|x]; [ idtac |
              destruct x as [|x]; [ idtac |
                destruct x as [|x]; [ idtac |
                  inversion H; try lia
                ]
              ]
            ]
          ]
        ]
      ]
    ]
  ].

Ltac prove_gamma_sq g :=
  apply functional_extensionality; intros i;
  apply functional_extensionality; intros j;
  unfold mat_mul, mat_mul_aux, g, mat_opp, mat_one, fin_nat;
  destruct_fin8 i;
  destruct_fin8 j;
  vm_compute; ring.

Lemma gamma_1_sq : mat_mul gamma_1 gamma_1 = mat_opp (mat_one 8).
Proof. prove_gamma_sq gamma_1. Qed.

Lemma gamma_2_sq : mat_mul gamma_2 gamma_2 = mat_opp (mat_one 8).
Proof. prove_gamma_sq gamma_2. Qed.

Lemma gamma_3_sq : mat_mul gamma_3 gamma_3 = mat_opp (mat_one 8).
Proof. prove_gamma_sq gamma_3. Qed.
