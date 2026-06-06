# Wave 23 Status — phi-paper v2.3 (BNF equivalence-class result)

> Wave 23 is a **cross-repo scientific wave**, not a code wave.
> The deliverable is the **phi-paper v2.3-draft** prepared in the
> [`gHashTag/phi-paper`](https://github.com/gHashTag/phi-paper) repo
> (PRIVATE; methodological short paper). This `trinity-s3ai` repo
> remains the canonical owner of the H4/600-cell/Cl(8) hardware,
> formal proofs, and silicon-anchor narrative; the phi-paper is the
> external methodology-only audit that frames the `phi^2 + phi^-2 = 3`
> identity as an MDL-canonical Lucas-symmetric form within an
> explicitly bounded grammar.

---

## Scope of Wave 23

The 2026-06-06 Pellis review letter (archived verbatim in
`gHashTag/phi-paper` as `pellis_letter_2026-06-06.md`) asked, among
other things, whether the central identity `phi^2 + phi^-2 = 3 = L_2`
is **specifically** distinguished within a precisely bounded grammar,
or whether the claim of "uniqueness" was over-stated. Wave 23 answers
that question by exhaustive enumeration with a frozen reproducibility
capsule.

The result lands as a new subsection in the phi-paper short paper
(v2.3, draft only, **not yet on `gHashTag/phi-paper` master**), pending
Pellis approval.

---

## The BNF equivalence-class result (v2.3-draft)

Within the bounded depth-≤2 BNF grammar over Q(phi) generators:

```
E ::= phi^k | E op E,    k in {-2,-1,0,1,2},  op in {+,-,*,/}
```

| Layer | Count | Interpretation |
|-------|------:|----------------|
| Total syntactically distinct expressions | 40,100 | full BNF enumeration |
| Algebraically equal to 3 via `sympy.simplify` | 501 | L_2-equivalence class |
| Contain phi symbolically in source | 497 | phi-native subset |
| **After anti-cancellation filter** | **394** | essential phi-native forms |

Within the 394 essential phi-native forms:

- `G_phi = phi^2 + phi^-2` has **MDL-rank 2 of 394** under the
  string-length MDL proxy.
- Rank 1 is the commutative twin `phi^-2 + phi^2` (identical algebraic
  content); under sum-order canonicalisation both collapse to a
  single equivalence-class representative.
- Bootstrap (B = 10,000): `p(MDL <= 12) = 0.0039`; empirical one-sided
  p-value for "G_phi ranks at or above its observed position" is
  `0.0051`.
- Null hypothesis "G_phi is a random form in this equivalence class" is
  **rejected at p < 0.01**.

**Honest scope statement.** This is not a claim that `phi^2 + phi^-2 = 3`
is uniquely distinguished among all possible mathematical expressions.
It is a claim that within an explicitly bounded grammar with an explicit
anti-cancellation filter and an explicit MDL proxy, `G_phi` is
MDL-rank 2/394 at p < 0.01. **The bounds are part of the result.**

---

## Frozen audit trail (v2.3 capsule)

Pinned in `gHashTag/phi-paper/reproducibility/v23/`:

| Artefact | Role | SHA-256 (first 16 hex of 64) |
|----------|------|------------------------------|
| `v23C_full_enumerate.py` | 40,100-expr BNF enumerator | `e0f792f3def5f7ae...` |
| `results_v23C_full.json` | 501 matches, by classification | `f3dd8e5a29a5a9e3...` |
| `v23C_anticancel_bootstrap.py` | W1+W8 filter + bootstrap driver | `8f2cdcf3357e87b7...` |
| `results_v23C_anticancel.json` | 394 essential, rank = 2 | `c82075742bae5581...` |
| `results_v23C_bootstrap.json` | p = 0.0039, B = 10,000 | `75cbf04361bdf0ba...` |

Full 64-hex hashes ship in `gHashTag/phi-paper/reproducibility/v23/SHA256SUMS.txt`
**after** Pellis approves the v2.3 §6.3 formulation. Until then, the
capsule is local-only to avoid silent change of the central claim.

---

## v2.3 manuscript additions

In `gHashTag/phi-paper/pellis_vasilev_letter.tex` (local draft, not
yet pushed):

- **New §6.3** "Equivalence-class analysis and MDL-canonical Lucas form
  (v2.3)" — the BNF result above, with SHA-256 table and three
  falsification paths (structural, coding-scheme, grammar-extension).
- **New §6.4** "Relation to prior BNF symbolic regression and
  equality-saturation" — explicit prior-art acknowledgement of
  Finkelstein 2024 BNF, Jiang EGG-SR 2026 ICLR, Yu SR4MDL, Desmond
  exhaustive SR, Raz/Shalyt Euler-to-AI, De Laet description-language
  dependence, Beit-Halachmi/Kaminer Ramanujan Library.
- **Conj 7.6** Grammar-extension robustness + Fpath.
- **Conj 7.7** Rissanen-Grünwald MDL robustness + Fpath.
- **8 new bibitems** in the bibliography (`finkelstein2024bnf`,
  `jiang2026eggsr`, `yu2024sr4mdl`, `desmond2025exhaustive`,
  `raz2025shalyt`, `beithalachmi2024ramanujan`, `delaet2026mdl`,
  `grunwald2024safetests`).

Version bump: v2.1 → **v2.3-draft** (title page + PDF metadata).

Compile result: 22 pages (was 19 at v2.1); QA pattern passes
(0 undefined references; qpdf OK; hype-scan clean except disclaimer
in §1.4; visual inspection of §6.3 pages shows no broken text).

---

## Relation to this repo (`trinity-s3ai`) silicon anchor

The phi-paper v2.3 result **strengthens** the silicon-anchor narrative
used here:

```
phi^2 + phi^-2 = 3   →   L_2 = 3   →   dot4 = 0x47C0
       ^                   ^               ^
       |                   |               |
v2.3: MDL-canonical    Trinity        TTSKY26b reset
in 394-form class      anchor         witness (METAPHOR
at p < 0.01            (Verified)     only, FL-2)
```

What changes: the leftmost arrow is no longer just `\Verified` algebra —
it is also `\Conj` at p < 0.01 within the explicitly-bounded BNF +
anti-cancellation grammar. The Trinity anchor itself (`phi^2 + phi^-2 = 3`)
remains theorem-`\Verified`.

What does **not** change:

- The control-grammar test of phi-paper §5 (37/40 random grammars beat
  G_phi on Catalog15 aggregate) stands. `phi`-specificity for
  **constant compression** remains `\Retr`.
- The hardware claims in `docs/hardware/` (GF16 6-difference doc,
  full-ladder round rule 9/9, RTL-across-ladder for GF4..GF256,
  GF256 bias `[Open]` flag) are independent of the BNF result and
  retain their existing claim-status.
- FL-2 (silicon-provenance reset value `0x47C0` vs the predicted
  constant) remains `\Conj`/`\Risk`, used nowhere in physics claims.

---

## Ten weak points before v2.3 — closure status

A pre-v2.3 inventory identified ten weak points (W1-W10). Current
closure as of 2026-06-06:

| # | Weak point | Severity | v2.3 status |
|---|------------|----------|-------------|
| W1 | G_phi not MDL-min in raw class (rank 4/497) | CRITICAL | **CLOSED** by anti-cancel filter → rank 2/394 |
| W2 | Grammar too narrow (no int coefs / depth > 2) | CRITICAL | scope locked + Conj 7.6 |
| W3 | "Lucas-like" classification is grep-based | HIGH | open — needs Galois-theoretic classes (v2.4) |
| W4 | Pre-reg does not pin sympy version | HIGH | pin via SHA256SUMS (v2.4) |
| W5 | Finkelstein 2024 precedes our BNF methodology | HIGH | **CLOSED** — cited in §6.4 |
| W6 | EGG-SR (Jiang 2026) is the proper e-graph tool | HIGH | declared limitation v2.3 + Risk R-v23-C-1 |
| W7 | MDL = string proxy, not Rissanen-Grünwald | MEDIUM | Conj 7.7 + Fpath |
| W8 | No bootstrap distribution | MEDIUM | **CLOSED** — p = 0.0039 |
| W9 | Pellis Letter III used stale numbers (~100) | MEDIUM | **CLOSED** — letter v2 with 394/p=0.0039 |
| W10 | arXiv cs.AR endorsement may not cover stat.ML | LOW | open — verify before submit |

Five of ten closed in v2.3; four legalised through explicit Conj/Risk
+ prior-art citation; three (W3, W4, W10) remain open for follow-up.

---

## Next-loop collaboration variants (priority order)

Three independent validators identified, each closing a different
weak point:

1. **Aaron Finkelstein** (BNF SR author, arXiv:2410.08137) — closes W5
   (BNF authorship); cost 15 min; reply window 1-4 weeks.
2. **Peter Grünwald** (CWI Amsterdam + Leiden; ERC AdvGrant 2024 safe
   testing; `pdg@cwi.nl`) — closes W7 (real Rissanen-Grünwald MDL);
   cost 30 min; reply window 2-3 weeks.
3. **ReScience C journal** — peer-reviewed replication venue with
   frozen capsule structurally compatible with v2.3; cost 4-6h; review
   window 3-6 months.

Detailed plan: `COLLABORATION_VARIANTS_LOOP_NEXT.md` (in Perplexity
Computer workspace; cross-referenced from
`gHashTag/phi-paper/README.md` after Pellis approval).

---

## Gating rule (HARD)

Wave 23 deliverables remain **local-only** until Stergios Pellis
approves the v2.3 §6.3 formulation in writing. Specifically:

1. **DO NOT push v2.3 to `gHashTag/phi-paper master`** — that would be
   a silent change of the central claim in the audit trail.
2. **DO NOT submit phi-paper to arXiv** — co-authors (Pellis, Olsen)
   have not consented to the v2.3 formulation; the cs.AR endorsement
   from Laslo Hunhold (`QFHDTL`) covers `arXiv:2606.05017` (GoldenFloat)
   only, not stat.ML / cs.LG.
3. **DO NOT advertise the v2.3 result in public outreach** until the
   capsule is on `gHashTag/phi-paper master` with a `v2.3` tag.

These three rules together preserve the audit-trail integrity that
distinguishes this programme from numerology.

---

## File map (this Wave 23)

In `trinity-s3ai`:

- `WAVE23_PHI_PAPER_v23_STATUS.md` — this file (cross-repo pointer).

In `gHashTag/phi-paper` (PRIVATE; local draft):

- `pellis_vasilev_letter.tex` — v2.3-draft source (~1575 lines).
- `pellis_vasilev_letter.pdf` — v2.3-draft compiled (22 pages).
- `reproducibility/v23/{v23C_full_enumerate.py, results_v23C_full.json,
  v23C_anticancel_bootstrap.py, results_v23C_anticancel.json,
  results_v23C_bootstrap.json, SHA256SUMS.txt}` — frozen audit trail.

In Perplexity Computer workspace (working artefacts):

- `audit_2026-06-06/weaknesses_inventory_v23_2026-06-06.md` — W1-W10.
- `audit_2026-06-06/literature_scan_v23_2026-06-06.md` — 18 publications.
- `audit_2026-06-06/v23_plan/DECOMPOSED_PLAN_v23.md` — §6.3 LaTeX
  ready-to-paste, 9 bibitems, 5-step roadmap, arXiv decision tree.
- `outbox/letter_to_stergios_pellis_2026-06-06_v2.md` — letter draft
  with correct numbers (394/rank 2/p=0.0039) + 4 explicit questions.
- `FINAL_REPORT_LOOP_2026-06-06.md` — loop summary.
- `COLLABORATION_VARIANTS_LOOP_NEXT.md` — next-loop variants.

---

## Anchor

> Within depth-≤2 BNF over `{phi^k : k in [-2,2]}` with binary operators
> and an anti-cancellation filter, `G_phi = phi^2 + phi^-2` is the
> MDL-canonical Lucas-symmetric representative `L_2 = phi^n + (-phi)^-n`
> at n = 2, with p < 0.01 significance. **The result is conditional on
> the specific grammar and the string-length MDL proxy; the bounds are
> part of the result.**

Not "uniqueness". Not "fundamental". Statistically significant within
a precisely specified scope. Survives the five-point invariance ledger
(`pellis_vasilev_letter.tex` §7) because the bounds are now explicit.
