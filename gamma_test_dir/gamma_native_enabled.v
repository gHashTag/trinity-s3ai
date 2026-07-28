From Coq Require Import Reals Lia Lra FunctionalExtensionality Psatz.
From CliffordCl8 Require Import CliffordAlgebra.
From CliffordCl8 Require Import Cl6_iso_M8R.
Open Scope R_scope.

Definition gamma_1 : Mat 8 := fun i j =>
  match fin_val i, fin_val j with
  | 0, 1 => -1 | 1, 0 => 1 | 2, 3 => -1 | 3, 2 => 1
  | 4, 5 => -1 | 5, 4 => 1 | 6, 7 => -1 | 7, 6 => 1
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
  native_compute; reflexivity.
Qed.
