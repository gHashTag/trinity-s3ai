# Honesty Manifest — Trinity S³AI

**Version:** Wave 23  
**Date:** 2026-05-31  
**Policy:** No fake proofs. No cosmetic edits to hide gaps.

---

## 1. How Statistics Are Computed

All numbers below are produced by [`scripts/count_admitted_honest.py`](scripts/count_admitted_honest.py), a parser that **strips Coq comments and strings before counting**.

### Algorithm
1. Walk every `.v` file in `proofs/` and `derivations/`.
2. Character-by-character state machine:
   - `"`  → enter **STRING** (skip `"` and `\x` escapes).
   - `(*` → enter **COMMENT** (nested `(* … *)` supported).
   - `*)` → exit comment when nesting depth returns to 0.
3. On the remaining code text, count occurrences of:
   - `Qed.`, `Defined.`
   - `Admitted.`
   - `Axiom`, `Conjecture`, `Parameter`
   - `refuted` (theorem names that document falsified claims)
4. Each token is matched with Coq-aware word boundaries so identifiers such as `Axiom6Orientation` or `invariant_720_refuted` are **not** double-counted.

### Why This Matters
A naive `grep -c "Admitted" counts **77** occurrences in `proofs/trinity/*.v`, but **every single one is inside a comment** (historical notes, TODOs, or honesty tags).  
The honest parser finds **0** real `Admitted.` proof obligations in `proofs/trinity/`.

---

## 2. Current Honest Status

| Metric | Count |
|--------|-------|
| Coq `.v` files scanned | **100** (56 in `proofs/trinity/` + 6 in `proofs/clifford_cl8/` + 38 in `derivations/`) |
| `Qed.` + `Defined.` | **2 104** (of which 2,098 are theorems with `Qed.` and 6 with `Defined.`) |
| Real `Admitted.` (comment-stripped) | **0** globally (proofs/trinity/: 0; proofs/clifford_cl8/: 0; derivations/: 0) |
| Mentions of `Admitted.` inside comments | ~25 across all files (historical notes only, not obligations) |
| `Axiom` + `Conjecture` + `Parameter` | **93** (82 `Axiom` + 11 `Parameter`; 0 `Conjecture`) |
| Refutation theorems (`refuted`) | **14** |

### Breakdown by directory

| Directory | Files | Qed+Def | Admitted | Axioms | Refutations |
|-----------|-------|---------|----------|--------|-------------|
| `proofs/trinity/` | 56 | 1 130 | **0** | 51 | 11 |
| `proofs/trinity/coq_models/` | 11 | 86 | **0** | 3 | 0 |
| `proofs/clifford_cl8/` | 6 | 174 | **0** | 9 | 0 |
| `proofs/catalog/` | 1 | 1 | **0** | 0 | 0 |
| *derivations/* | 26 | 713 | 0 | 30 | 3 |

### Comment-only `Admitted.` mentions (not real obligations)

All `.v` files in `proofs/trinity/` and `proofs/clifford_cl8/` contain **zero** real `Admitted.` commands. Historical mentions exist inside `(* ... *)` comments only, documenting:
- Waves where a theorem was planned but later proved or refuted.
- Honesty tags explaining why a gap existed at the time.
- Cross-references to `admitted_log.md` and wave logs.

Load-bearing gaps in `proofs/clifford_cl8/` (Track B) are declared as **well-cited `Axiom`** statements (e.g., Bott periodicity with ABS 1964 citation), not as `Admitted.`

We **do not delete** these comments; they are valuable provenance metadata.

---

## 3. Commitment

1. **No fake proofs.** Every `Qed.` is a real Coq proof (or a `refuted` theorem with an explicit counter-example).
2. **No cosmetic edits.** We will not remove `Admitted` from comments to make grep look better.
3. **Living audit.** This manifest is regenerated automatically by `scripts/count_admitted_honest.py` and its output is treated as ground truth for all public-facing statistics.
4. **If a number drops, we explain why.** For example, if an `Admitted` is closed, the release notes will name the file, the theorem, and the wave that closed it.

---

## 4. How to Reproduce

```bash
python3 scripts/count_admitted_honest.py
```

The script prints a human-readable table and a JSON block to stdout.  
No external dependencies beyond Python 3.
