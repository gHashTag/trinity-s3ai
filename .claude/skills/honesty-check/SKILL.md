---
name: honesty-check
description: Run the complete Trinity S3AI honesty validation suite
---

# /honesty-check

Run the complete Trinity S3AI validation suite and report PASS/FAIL for each check.

## Steps

1. **Anti-numerology gate**: `python3 scripts/anti_numerology_gate.py`
2. **Honest admitted counter**: `python3 scripts/count_admitted_honest.py`
3. **Formula bounds validator**: `python3 scripts/validators/validate_v4.py`
4. **Claim ledger consistency**: `python3 scripts/generate_claims.py --check`
5. **English-only scan**: `bash scripts/check_english_only.sh`
6. **Coq build** (optional, slow): `cd proofs/trinity && coq_makefile -f _CoqProject -o Makefile.coq && make -f Makefile.coq -j$(nproc)`
7. **Rust tests** (optional): `cd games/trinity_fold && cargo test --workspace`

## Report format

```
Honesty Check Results
=====================
1. Anti-numerology gate:    [PASS/FAIL]
2. Admitted counter:        [PASS/FAIL] — X real Admitted found
3. Formula bounds:          [PASS/FAIL] — mean error: Y
4. Claim ledger:            [PASS/FAIL]
5. English-only:            [PASS/FAIL]
6. Coq build:               [PASS/FAIL] (if run)
7. Rust tests:              [PASS/FAIL] (if run)

FINAL VERDICT: [PASS / FAIL]
```

## Notes

- If any check fails, explain what failed and suggest the fix.
- The admitted counter strips comments before counting — a naive `grep` would find 77 occurrences, all inside comments.
- `docs/claims.yaml` is the SSOT; never edit the README claim table by hand.
