Definition C_RAlgebra : RAlgebra.
Proof.
  refine {| carrier := C_carrier;
            alg_zero := C_zero;
            alg_one := C_one;
            alg_add := C_add;
            alg_mul := C_mul;
            alg_smul := C_smul;
            alg_opp := C_opp |}.
  (* Additive axioms *)
  1-4,13: intros; unfold C_add, C_opp, C_zero; simpl; f_equal; lra.
  (* Multiplicative axioms *)
  5-9: intros; unfold C_mul, C_one; simpl; f_equal; field.
  (* Scalar axioms *)
  10-12: intros; unfold C_smul, C_add; simpl; f_equal; lra.
Defined.
