From Coq Require Import Reals Lia.
From CliffordCl8 Require Import CliffordAlgebra.
Open Scope R_scope.

Lemma test_fin_val (i : Fin 8) :
  fin_val i = fin_val i.
Proof.
  assert (Hi : fin_val i < 8) by apply fin_lt.
  destruct (fin_val i) as [|n];
    [ reflexivity |
      destruct n as [|n]; [ reflexivity |
        destruct n as [|n]; [ reflexivity |
          destruct n as [|n]; [ reflexivity |
            destruct n as [|n]; [ reflexivity |
              destruct n as [|n]; [ reflexivity |
                destruct n as [|n]; [ reflexivity |
                  destruct n as [|n]; [ reflexivity |
                    exfalso; lia
                  ]
                ]
              ]
            ]
          ]
        ]
      ]
    ].
Qed.
