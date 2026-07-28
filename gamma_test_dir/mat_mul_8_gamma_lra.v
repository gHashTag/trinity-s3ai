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

Definition mat_mul_8 (A B : Mat 8) : Mat 8 := fun i j =>
  A i f0 * B f0 j +
  A i f1 * B f1 j +
  A i f2 * B f2 j +
  A i f3 * B f3 j +
  A i f4 * B f4 j +
  A i f5 * B f5 j +
  A i f6 * B f6 j +
  A i f7 * B f7 j.

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
  mat_mul_8 gamma_1 gamma_1 = mat_opp (mat_one 8).
Proof.
  apply functional_extensionality; intros i.
  apply functional_extensionality; intros j.
  unfold mat_mul_8, gamma_1, mat_opp, mat_one.
  destruct_fin8 i;
  destruct_fin8 j;
  vm_compute; lra.
Qed.
