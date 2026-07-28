From Coq Require Import Reals Lia Lra FunctionalExtensionality Psatz.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Definition gamma_1 : Mat 8 := fun i j =>
  match i, j with
  | mkFin 0 _, mkFin 1 _ => -1
  | mkFin 1 _, mkFin 0 _ => 1
  | mkFin 2 _, mkFin 3 _ => -1
  | mkFin 3 _, mkFin 2 _ => 1
  | mkFin 4 _, mkFin 5 _ => -1
  | mkFin 5 _, mkFin 4 _ => 1
  | mkFin 6 _, mkFin 7 _ => -1
  | mkFin 7 _, mkFin 6 _ => 1
  | _, _ => 0
  end.

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
                  inversion H
                ]
              ]
            ]
          ]
        ]
      ]
    ]
  ].

Lemma gamma_1_sq :
  mat_mul gamma_1 gamma_1 = mat_opp (mat_one 8).
Proof.
  apply functional_extensionality; intros i.
  apply functional_extensionality; intros j.
  unfold mat_mul, mat_mul_aux, gamma_1, mat_opp, mat_one, fin_nat.
  destruct_fin8 i;
  destruct_fin8 j;
  vm_compute;
  try (ring; fail);
  idtac "Failed goal:";
  Show Goal.
Abort.
