From Coq Require Import Reals Lia.
From CliffordCl8 Require Import CliffordAlgebra.
Open Scope R_scope.

Ltac destruct_fin8 i Hi :=
  destruct i as [i Hi];
  destruct i as [|i]; [ idtac |
    destruct i as [|i]; [ idtac |
      destruct i as [|i]; [ idtac |
        destruct i as [|i]; [ idtac |
          destruct i as [|i]; [ idtac |
            destruct i as [|i]; [ idtac |
              destruct i as [|i]; [ idtac |
                destruct i as [|i]; [ idtac |
                  inversion Hi
                ]
              ]
            ]
          ]
        ]
      ]
    ]
  ].

Lemma test_fin_val (i : Fin 8) (j : Fin 8) :
  fin_val i = fin_val i.
Proof.
  destruct_fin8 i Hi;
  destruct_fin8 j Hj;
  reflexivity.
Qed.
