# Wave 24 — φ Falsifiability Ablation Design

**Epic:** #181  
**Date:** 2026-05-31  
**Status:** COMPLETE — both arms reached 81K steps; result classified  
**Principle:** A numeric coincidence is not a derivation. Aesthetic hyperparameters must beat random baselines.

---

## Hypothesis

> φ-anchored hyperparameters (lr = φ⁻³, wd = φ⁻³, beta1 = 1/φ) improve language-model BPB compared to conventional hyperparameters on the IGLA RACE benchmark.

**Honest label:** `[Open conjecture]` → will become `[ empirical_fit ]`, `[ high_risk_or_falsified ]`, or `[ open_conjecture ]`.

---

## Design

### Fixed parameters (both arms)

| Parameter | Value |
|-----------|-------|
| Model | Transformer, hidden=128, 2 layers |
| Precision | bf16 |
| Optimizer | AdamW |
| Seed | 1597 |
| Steps | 81,000 |
| Batch | 64 |

### Control arm (conventional)

| Parameter | Value |
|-----------|-------|
| Learning rate | 0.001 |
| Weight decay | 0.01 |
| Beta1 | 0.9 |
| Beta2 | 0.999 |

### Treatment arm (φ-anchored)

| Parameter | Value | φ expression |
|-----------|-------|--------------|
| Learning rate | 0.2360679… | φ⁻³ = 1/φ³ |
| Weight decay | 0.2360679… | φ⁻³ = 1/φ³ |
| Beta1 | 0.6180339… | 1/φ |
| Beta2 | 0.999 | fixed (not φ-derived) |

---

## Falsification criterion

| Outcome | Classification | Condition |
|---------|---------------|-----------|
| **FALSIFIED** | `[high_risk_or_falsified]` | Treatment best BPB > Control best BPB by >0.05 (significant degradation) |
| **NULL** | `[open_conjecture]` | Difference < 0.05 (no meaningful effect) |
| **EMPIRICAL_FIT** | `[empirical_fit]` | Treatment best BPB < Control best BPB by >0.05 (genuine improvement) |

---

## Execution

Both services deployed to Railway fleet via `trios-trainer-igla` repo:
- `phi-ablation-control` — conventional hyperparameters
- `phi-ablation-treat` — φ-anchored hyperparameters

Harvested via `/tmp/harvest_single.sh` → `trios-trainer-igla/.trinity/gardener_harvest.log`.

---

## Results

| Arm | Best BPB @ 81K | Final BPB @ 81K | nca_h | Status |
|-----|---------------|-------------------|-------|--------|
| Control (conventional) | **2.6167** | 2.6596 | 1.287 | ✅ Better |
| Treatment (φ-anchored) | **2.7180** | 2.6981 | 0.451 | ❌ Worse |

**Delta:** Treatment is **0.1013 BPB higher** than Control (~3.9% relative degradation).

---

## Classification

**`[high_risk_or_falsified]`**

The hypothesis that φ-anchored hyperparameters improve BPB is **falsified** by this controlled ablation. On the tested configuration (hidden=128, bf16, AdamW, 81K steps, seed=1597), φ-derived lr/wd/beta1 produce measurably worse convergence than conventional values.

**Honest note:** This is a single-seed, single-scale experiment. A multi-seed replication could change the classification to NULL if variance dominates. However, the consistent gap across all checkpoints (Control < Treatment at every measured step) makes a NULL classification unlikely.

---

## Artefacts

- Harvest log: `trios-trainer-igla/.trinity/gardener_harvest.log`
- This design doc: `docs/audit/PHI_ABLATION_DESIGN.md`
- Result registry: `derivations/falsifiability/wave24_phi_ablation.md`

---

*Wave 24 — 2026-05-31. Trinity S³AI: an honest boundary-mapping research program.*
