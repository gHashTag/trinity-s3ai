# Next Waves — Trinity S³AI / IGLA RACE

**Date:** 2026-05-31  
**Current:** Wave 24 complete (φ falsifiability ablation), Wave 23 complete (honesty audit), Wave 12 complete (communication)  
**Status:** Wave 24 classified `[high_risk_or_falsified]`; Waves 25–28 queued

---

## Wave 24 — φ Falsifiability (Epic #181)

**Goal:** Experimentally determine whether φ-anchored hyperparameters improve BPB or are aesthetic only.

**Design:** Already in `docs/audit/PHI_ABLATION_DESIGN.md`
- Control: lr=0.001, wd=0.01, beta1=0.9 (conventional)
- Treatment: lr=φ⁻³≈0.236, wd=φ⁻³≈0.236, beta1=1/φ≈0.618 (phi)
- Fixed: seed=1597, bf16, hidden=128, AdamW, 81K steps

**Implementation:**
- [x] Deploy Control service to Railway (conventional: lr=0.001, wd=0.01, beta1=0.9)
- [x] Deploy Treatment service to Railway (φ: lr=φ⁻³, wd=φ⁻³, beta1=1/φ)
- [x] Harvest both at 81K steps — Control best=2.6167, Treatment best=2.7180
- [x] Classify: **`[high_risk_or_falsified]`** — Treatment worse by +0.1013 BPB (~3.9%)
- [x] Document result in `docs/audit/PHI_ABLATION_DESIGN.md` and `derivations/falsifiability/wave24_phi_ablation.md`

**Honest label:** `[Open conjecture]` → **`[high_risk_or_falsified]`**

---

## Wave 25 — Coq Library Gap Closure

**Goal:** Close the 3-file Coq build blocker.

**Gap:** `Interval.Tactic` missing from `coq-interval` package.
**Files:** `Bounds_Mixing.v`, `HiggsPotentialCorrected.v`, `E6vsH4.v`

**Steps:**
- [ ] Install `coq-interval` via opam
- [ ] Verify all 3 files compile
- [ ] Update `docs/COQ_INTERVAL_LIBRARY_GAP.md` → closed
- [ ] Update CI to include `coq-interval`

**Honest label:** `[LIBRARY_GAP]` → `verified`

---

## Wave 26 — IGLA RACE Gate-2 Push

**Goal:** Achieve BPB < 1.85 on 3 seeds with step ≥ 4000.

**Current best:** 2.4872 (scarab-fp16-seed77) — gap 0.6372
**Approach:**
- [x] Run phi ablation (Wave 24) — treatment **lost** (+0.1013 BPB worse); no scaling needed
- [ ] Evaluate Muon vs AdamW on winning config (P1 null was negative, but new configs may differ)
- [ ] Try larger hidden (512, 828) with bf16/gf16
- [ ] Document null results honestly

**Honest label:** `[Open conjecture]` — not yet achieved

---

## Wave 27 — Lean 4 Port Completion

**Goal:** Close 6 remaining `sorry` in Lean 4 port.

**Location:** `derivations/lean_port/TrinityLean/`
**Approach:**
- [ ] Map each `sorry` to its Coq original
- [ ] Prioritize by difficulty (structural → numerical)
- [ ] Port or admit with honest tag

**Honest label:** `[MATH_TODO]` or `[LIBRARY_GAP]`

---

## Wave 28 — GOLDEN CHAIN Game Integration

**Goal:** Link GOLDEN CHAIN puzzle to Trinity research artifacts.

**Current:** 5-ring Rust workspace in `games/trinity_fold/`
**Steps:**
- [ ] Formalize ring-0 (Proof) — link to Coq `Qed.` count
- [ ] Formalize ring-1 (Formula) — link to catalog formulas
- [ ] Formalize ring-2 (Boundary) — link to BT-1..BT-4
- [ ] Formalize ring-3 (Prediction) — link to falsifiable predictions
- [ ] Formalize ring-4 (Honesty) — link to Admitted count

**Honest label:** `[MATH_TODO]` for formalization; `[Verified]` once game checks pass

---

## Wave 29+ — Physics (Speculative)

Only if Wave 24–28 deliver clean results:

- **Wave 29:** 1-loop Higgs correction (Wave 12.4 open)
- **Wave 30:** E₆/E₇ explicit D_P (Wave 12.5 open)
- **Wave 31:** arXiv paper — single result, not catalog

---

*Wave 24 is the only immediate priority. Waves 25–28 are queued and activated by RALPH or manual trigger.*
