# Loop Report — Anomaly Audit Cycle 3 (Wave 24+, 2026-05-31)

## Summary

Third full-repository anomaly audit completed. All 5 validators pass. 162 files modified this session. Critical structural anomaly found in Lean 4 workspace.

---

## Fixes Applied This Cycle

### LEGACY Headers Added (Historical Roadmaps)

| File | Wave Era | Previous Header |
|------|----------|-----------------|
| `ROADMAP_WAVE17_PLUS.md` | Wave 17.2 | "Roadmap Wave 17+" |
| `ROADMAP.md` | Waves 1–7 | "Improvement Plan" |
| `docs/roadmaps/ROADMAP_WAVE15_PLUS.md` | Waves 16–20 | "Roadmap Waves 16–20" |
| `docs/roadmaps/IMPROVEMENT_PLAN.md` | Wave 20 | "Strategic Improvement Plan" |

---

## Critical Anomaly Found — Lean 4 Workspace Structure

### Finding

The Lean 4 lake workspace at `derivations/lean_port/TrinityLean/` has a **structural anomaly** where source files exist in two overlapping locations:

| Location | Files | Status |
|----------|-------|--------|
| `TrinityLean/*.lean` (top-level) | 8 files | **Incorrect for lake** |
| `TrinityLean/TrinityLean/*.lean` (nested) | 8 files | **Correct for lake** |

### Why This Matters

`TrinityLean.lean` (root file) imports modules as `TrinityLean.KODimension`, `TrinityLean.QuaternionicLinearity`, etc. Lake resolves these imports by looking in `TrinityLean/` relative to the package root. Files in top-level `TrinityLean/*.lean` are **not importable** via the `TrinityLean.*` namespace — they would need to be at `TrinityLean/TrinityLean/*.lean`.

### Overlap Analysis

| File | Top-level | Nested | Differs? | Newer? |
|------|-----------|--------|----------|--------|
| `H4RootSystem.lean` | ✅ | ✅ | YES (imports) | Top-level |
| `HamiltonFano.lean` | ✅ | ✅ | NO | Top-level |
| `Snub24Z3.lean` | ✅ | ✅ | YES (`maxRecDepth`) | Top-level |
| `KODimension.lean` | ✅ | ✅ | YES (major) | Nested |
| `QuaternionicLinearity.lean` | ✅ | ✅ | YES (major) | Nested |
| `CorePhi.lean` | ✅ | ❌ | — | Top-level only |
| `TrinityLean.lean` | ✅ | ❌ | — | Root file (correct at top-level) |
| `DiracOperator.lean` | ❌ | ✅ | — | Nested only |
| `EtaInvariant.lean` | ❌ | ✅ | — | Nested only |
| `Spectrum600Cell.lean` | ❌ | ✅ | — | Nested only |

### Impact

- **Top-level `H4RootSystem.lean`, `HamiltonFano.lean`, `Snub24Z3.lean`** are newer than nested versions but in the wrong location. Lake will import the older nested versions, ignoring top-level changes.
- **`KODimension.lean` and `QuaternionicLinearity.lean`** have diverged significantly. The nested versions are newer but may lack content from top-level versions (or vice versa).
- **This is a silent bug** — `lake build` may succeed but compile stale code from nested directory while developers edit top-level files.

### Recommended Fix (NOT applied — requires lake build verification)

1. For each file present in both locations, perform a 3-way merge resolving differences.
2. Move the canonical merged version to `TrinityLean/TrinityLean/`.
3. Delete duplicate top-level `.lean` files (keep `TrinityLean.lean`, `lakefile.lean`, `README.md`, `CorePhi.lean` which are intentionally top-level).
4. Run `lake build` to verify.
5. Update `docs/reports/lean_ci_gap.md` to document resolved structure.

---

## Placeholder Check

Template/checklist files with example placeholders were reviewed. These are instructional documents, not claims:

| File | Placeholder | Context |
|------|-------------|---------|
| `scripts/prepare_arxiv.md` | `arXiv:2605.XXXXX` | Template instruction |
| `scripts/prepare_zenodo.md` | `10.5281/zenodo.XXXXXXX` | Template instruction |
| `paper/arxiv_checklist.md` | `arXiv:2501.xxxxx` | Template checklist |
| `paper/snub24_z3/arxiv_checklist.md` | `arXiv:2505.XXXXX` | Template checklist |

These are **not anomalies** — they are standard submission checklists with placeholder examples. No action needed.

---

## Validator Status

| Validator | Result |
|-----------|--------|
| `anti_numerology_gate.py` | 61 PASS, 0 FLAG |
| `count_admitted_honest.py` | 100 files, 2098 Qed, 0 Admitted, 93 obligations |
| `generate_claims.py --check` | 21 claims, artefacts current |
| `check_english_only.sh` | PASS (0 Cyrillic) |
| `check_markdown_links.py` | 0 broken (164 files, 683 links) |

---

## Remaining Open Items

1. **Commit queue**: 162 modified files awaiting commit (requires user authorization)
2. **Lean workspace structural anomaly**: Documented above — needs lake build verification before file moves
3. **Lean CI gap**: `proofs/lean/` and `derivations/lean_port/TrinityLean/` not built by CI
4. **Wave 24+ paper**: No current LaTeX source for Wave 24+ claims
5. **Zenodo DOI**: Still `[PENDING]` — requires manual GitHub release + Zenodo webhook

---

## Three Collaboration Variants for Next Loop

### Variant A — Lean 4 Workspace Fix
**Goal**: Resolve the structural anomaly in `derivations/lean_port/TrinityLean/`.
**What we need**: A developer with `lake` CLI access who can run `lake build`, compare compilation results, and perform the 3-way merge of divergent files.
**Deliverable**: Clean lake workspace with all 8 modules in correct `TrinityLean/TrinityLean/` location, 0 build errors, updated README.
**Risk**: Low if done with lake build verification after each move.

### Variant B — Formal Proof Sprint (Coq)
**Goal**: Reduce 51 obligations in `proofs/trinity/` by targeting the 2 physical Axioms in `RGRunning.v` (gU2inv_window, alpha_run_window) and 2 in `AltCrystallography.v` (eta_S3_2T, eta_S3_2O).
**What we need**: Coq mathematician with knowledge of renormalization group or crystallographic embeddings.
**Deliverable**: 4 fewer Axioms (converted to Qed theorems or tagged with `[OPEN_PROBLEM]` justification).
**Risk**: Medium — these may require domain-specific physics knowledge beyond pure math.

### Variant C — Wave 24+ Paper Draft
**Goal**: Create a current LaTeX source documenting Wave 24 results (φ falsification, IGLA RACE BPB benchmarks, Cl(8) Track B status).
**What we need**: Physics writer with LaTeX + academic publishing experience.
**Deliverable**: `paper/wave24_status.tex` — data paper (not theory paper) with BPB tables, φ ablation design, and honest assessment of 93 proof obligations.
**Risk**: Low — this is reporting, not research.

---

*Report generated: 2026-05-31*
*Next loop: /loop 15m recurring task (cron 8ccacaf2)*
