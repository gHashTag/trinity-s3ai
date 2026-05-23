# Scoring specification

The composite score is

```
total = ( w_c · consistency
       + w_d · dimensional_sanity
       + w_o · observable_fit
       + w_s · simplicity
       + w_y · symmetry_coherence
       + w_r · reproducibility
       - w_p · proof_debt_penalty
       - w_f · falsification_penalty )
       / (w_c + w_d + w_o + w_s + w_y + w_r)
```

with defaults

| Weight | Symbol | Value |
|---|---|---|
| consistency | w_c | 1.0 |
| dimensional_sanity | w_d | 1.0 |
| observable_fit | w_o | 1.5 |
| simplicity | w_s | 0.5 |
| symmetry_coherence | w_y | 0.75 |
| reproducibility | w_r | 0.5 |
| proof_debt_penalty | w_p | 1.0 |
| falsification_penalty | w_f | 4.0 |

If any tile carries `ClaimStatus::HighRiskOrFalsified` or the `falsified` /
`no_go` tag, the final total is capped at `min(total, -0.25)`. This is the
**honesty floor**, and it is non-negotiable.

## Component definitions

### consistency

Let `R` be the number of `requires` edges satisfied (target tile present)
and `B` the number of unmet `requires` plus the number of `incompatible_with`
violations.

```
consistency = R / (R + B)   if R + B > 0
            = 1             otherwise
```

### dimensional_sanity

Let `Σ` be the per-base-dimension sum over the board (e.g.
`{mass: 1, length: -1}` summed across all selected `Node.dimension` maps,
with zero entries removed).

```
imbalance         = Σ_k |Σ_k|
dimensional_sanity = 1               if Σ is empty
                  = 1 / (1 + imbalance) otherwise
```

The function does not parse Lagrangians; it just sums signatures of the
selected tiles. If you want this term to matter for a custom catalog, make
sure your tiles' `dimension` maps are filled in.

### observable_fit

For each `Observable` tile with both `value` and `predicted` set:

```
σ   = max(uncertainty, |value| · 1e-3)   if uncertainty is missing
z   = |predicted - value| / σ
contrib = (1 / (1 + z²)) · claim_weight
```

`claim_weight` follows the table in [`README.md`](../README.md#claim-status-policy).
`observable_fit` is the mean `contrib` over all eligible observables (zero
if none).

In **benchmark mode**, the `value` of any held-out observable is set to
`None` before scoring. This makes the contribution from that observable
zero — the player cannot tune `predicted` against an unknown ground truth.

### proof_debt_penalty

For each selected tile:

```
claim_cost = { verified: 0, empirical_fit: 0.2,
               open_conjecture: 0.5, unverified: 0.7,
               high_risk_or_falsified: 0 }[claim]
tag_cost   = 0.3 if "proof_debt" in tags else 0
```

Average across the board, capped at 1.

### falsification_penalty

Fraction of selected tiles with `ClaimStatus::HighRiskOrFalsified` or any of
the tags `falsified` / `no_go`. Capped at 1. Also triggers the honesty
floor.

### simplicity

```
dev        = |n - 10|
simplicity = 1 / (1 + 0.05 · dev²)
```

Peaks at `n = 10` selected tiles. Both very small (under-constrained) and
very large (over-decorated) boards are penalized.

### symmetry_coherence

Let `hits = #{triangle | every tile in triangle is on board}`.

```
tri_score = hits / total_triangles    if catalog has triangles
          = 0.5                       otherwise

symmetry_coherence
  = 0.5 + 0.5 · tri_score   if board has ≥1 Symmetry and ≥1 Geometry tile
  = 0.25 · tri_score        if exactly one of the two
  = 0                       otherwise
```

### reproducibility

Fraction of selected tiles whose `citation` field is non-empty. A
deliberately mechanical proxy for CASP-style traceability.

## Tuning

Weights live in `scoring::ScoreWeights`. The CLI does not yet expose them
as flags; if you need to experiment, call `score_board_with` directly.
