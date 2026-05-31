# Wave 24 — φ Falsifiability Ablation Result

**Date:** 2026-05-31  
**Wave:** 24 (IGLA RACE φ ablation)  
**Classification:** `[high_risk_or_falsified]`  
**Related:** [`docs/audit/PHI_ABLATION_DESIGN.md`](../../docs/audit/PHI_ABLATION_DESIGN.md)

---

## Summary

A controlled ablation test on the IGLA RACE benchmark falsifies the hypothesis that φ-anchored hyperparameters (lr = φ⁻³, wd = φ⁻³, beta1 = 1/φ) improve language-model BPB. The conventional control arm outperforms the φ treatment arm by 0.1013 BPB (~3.9% relative).

---

## Results table

| Metric | Control (conventional) | Treatment (φ-anchored) | Delta |
|--------|------------------------|------------------------|-------|
| Best BPB @ 81K steps | **2.6167** | 2.7180 | +0.1013 (treatment worse) |
| Final BPB @ 81K steps | 2.6596 | 2.6981 | +0.0385 |
| nca_h | 1.287 | 0.451 | — |
| Wall time | ~16,567 s | ~16,653 s | comparable |

---

## Step-by-step trajectory

Both arms started from identical initial loss (~7.0 BPB). The control arm consistently led:

| Step | Control | Treatment | Lead |
|------|---------|-----------|------|
| 20K | 2.6995 | 3.0922 | +0.3927 |
| 30K | 2.6378 | 3.0509 | +0.4131 |
| 40K | 2.6088 | 2.9379 | +0.3291 |
| 50K | 2.5781 | 2.8210 | +0.2429 |
| 60K | 2.6167* | 2.8519 | +0.2352 |
| 65K | 2.6167* | 2.8148 | +0.1981 |
| 75K | 2.6167* | 2.7483 | +0.1316 |
| 81K | 2.6167* | 2.7180 | +0.1013 |

\*Control best achieved at 60K; no further improvement.

---

## Interpretation

### What this means

φ-anchored hyperparameters are **not universally beneficial**. On this specific model configuration (hidden=128, 2-layer Transformer, bf16, AdamW, 81K steps, seed=1597), they degrade performance compared to well-tuned conventional values.

### What this does NOT mean

- It does not falsify the broader H4 → SM hypothesis (that is a physics claim, not an ML engineering claim).
- It does not prove φ-anchored hyperparameters are never useful; a different architecture, scale, or task might show benefit.
- It does not affect the mathematical validity of Coq-proven H4 theorems.

### Boundary-mapping value

This is a **positive scientific result**: it closes one speculative avenue ("φ hyperparameters are magic") and directs attention back to the physics content of the project.

---

## Comparison to best known result

The best BPB achieved in the IGLA RACE fleet (as of 2026-05-31) is **2.4872** (`scarab-fp16-seed77`, conventional hyperparameters with fp16). Both ablation arms are substantially above this:

- Control: 2.6167 (+0.1295 above best)
- Treatment: 2.7180 (+0.2308 above best)

This suggests the ablation model size (hidden=128) is under-parameterized relative to the fleet leaders, but the **relative comparison** between Control and Treatment remains valid.

---

## Honest caveats

1. **Single seed:** Only seed=1597 was tested. Multi-seed variance could shift the classification.
2. **Single scale:** hidden=128 is small. φ benefits might emerge at different scales.
3. **Task-specific:** IGLA RACE is a character-level language model on φ-structured data. Other tasks (vision, protein folding) are untested.
4. **No theoretical derivation:** Even if φ hyperparameters had won, the result would be `[empirical_fit]`, not `[verified]`, because no first-principles derivation links φ to optimal learning rates.

---

## Next steps

- **Wave 24.1 (optional):** Multi-seed replication (3 seeds) to confirm NULL vs FALSIFIED. Not prioritized unless physics track advances.
- **Wave 26:** IGLA Gate-2 push (BPB < 1.85) — independent of φ ablation result.

---

*Wave 24 — 2026-05-31. Trinity S³AI: an honest boundary-mapping research program.*
