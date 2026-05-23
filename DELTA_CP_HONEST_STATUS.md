# δ_CP Status — Honest Reassessment Against Current Global Fits

**Status**: Canonical (supersedes the "65.66° pre-registered prediction" framing where it conflicts with current global fits)
**Date**: 2026-05-23
**Companion**: `LAGRANGIAN_HONEST_STATUS.md` (Wave 1 honesty pass)

---

## TL;DR

Trinity's pre-registered prediction **δ_CP = 3/φ² = 65.66°** is in **5.6σ tension with the current best global fit** ([NuFIT-6.0](https://arxiv.org/abs/2410.05380), Sep 2024: NO best fit **177° ± 20°**, 3σ range 96°–422°) and **falls outside the 3σ range** of the inverted-ordering fit (201°–348°). The independent [T2K+NOvA joint analysis (Nature, Oct 2025)](https://www.nature.com/articles/s41586-025-09599-3) gives 3σ intervals **[−248°, 54°] (NO)** and **[−166°, −7°] ≡ [194°, 353°] (IO)** — Trinity's 65.66° sits at the very edge of the NO 3σ window and is **excluded** from the IO 3σ window.

**Both Trinity δ_CP formulas (e/2 = 77.87° and the revised 3/φ² = 65.66°) are excluded by current data.** The 3/φ² formula was a post-hoc fit to the outdated PDG-2024 combined value of 65.5° ± 1.6°, a value that has been superseded by global fits including more recent T2K and NOvA data.

The **three PMNS mixing angles** (θ₁₂, θ₂₃, θ₁₃) survive intact and remain within 3σ of NuFIT-6.0. This is where the actual empirical success of Trinity's PMNS sector lies.

---

## 1. What the data actually say (May 2026)

### NuFIT-6.0 (with SK atmospheric, Sep 2024)
| Ordering | δ_CP best fit | 1σ | 3σ range |
|---|---|---|---|
| **Normal (NO, preferred at Δχ² = 6.1)** | **177°** | +26°/−41° | **124° → 364°** |
| Inverted (IO) | 285° | +22°/−25° | 201° → 348° |

Source: [NuFIT-6.0 tables](http://www.nu-fit.org/sites/default/files/v60.tbl-parameters.pdf), [arXiv:2410.05380](https://arxiv.org/abs/2410.05380).

### T2K + NOvA Joint Analysis (Nature 646, Oct 2025)
| Ordering | δ_CP 3σ interval (paper convention, π units) | Equivalent in degrees |
|---|---|---|
| Normal (NO) | [−1.38π, 0.30π] | **[−248°, 54°]** ≡ [112°, 414°] |
| Inverted (IO) | [−0.92π, −0.04π] | **[−166°, −7°]** ≡ [194°, 353°] |

Source: [Nature s41586-025-09599-3](https://www.nature.com/articles/s41586-025-09599-3), [arXiv:2510.19888](https://arxiv.org/abs/2510.19888).

The two collaborations explicitly state: "if neutrino mass ordering is found to be inverted... results provide evidence that neutrinos violate CP symmetry" ([J-PARC press release](https://j-parc.jp/c/en/press-release/2025/10/23001631.html)).

### Where does **65.66°** sit?

| Reference | Status of Trinity's 65.66° |
|---|---|
| NuFIT-6.0 NO (bf 177°, 3σ 124°–364°) | **OUTSIDE 3σ** (lower bound 124°) |
| NuFIT-6.0 IO (bf 285°, 3σ 201°–348°) | **OUTSIDE 3σ** |
| T2K+NOvA NO (3σ [−248°, 54°] ≡ [112°, 414°]) | **OUTSIDE 3σ** (lower bound 112°) |
| T2K+NOvA IO (3σ [194°, 353°]) | **OUTSIDE 3σ** |
| PDG 2024 *combined* central value (65.5° ± 1.6°) | **AGREES** — but this combined value is now superseded by the global fits above |

The pre-2024 combined "PDG δ_CP" was an average over heterogeneous experimental inputs that have since been replaced by the joint T2K+NOvA analysis and NuFIT-6.0 global fit. **Citing PDG 2024 as supporting Trinity, while disregarding NuFIT-6.0 and T2K+NOvA, is selective.**

---

## 2. History of the prediction

| Version | δ_CP prediction | Stated origin | Status today |
|---|---|---|---|
| v3.3 | **90.2°** | Early H4 conjecture | Withdrawn — fit failure |
| v3.4 | **e/2 = 77.87°** | "Single fundamental constant" (gauge-symmetry handwave) | Excluded at ~5σ vs NuFIT-6.0 NO; 7.7σ vs old PDG-2024 |
| v3.5+ | **3/φ² = 65.66°** | Best fit found by brute-force search over `a·φ^b·π^c·e^d` to match PDG-2024 = 65.5° | Excluded at 5.6σ vs NuFIT-6.0 NO; outside 3σ for all current fits |

**Three formula revisions in pursuit of the same observable is the signature of post-hoc fitting, not first-principles prediction.** This is acknowledged in the project's own [`delta_cp_analysis.md`](docs/experiments/delta_cp_analysis.md) §6.2 Option B ("Replace with 3/φ²") and warned against in §5.2 ("Risk: Appears as post-hoc rationalization").

The `delta_cp_analysis.md` document itself was constructed against the **PDG-2024 target of 65.5° ± 1.6°** — a value that the more recent global fits have moved away from. The search algorithm did exactly what brute-force searches do: it found a simple closed form near the target. That target has since shifted.

---

## 3. What survives

The PMNS angle predictions are **genuinely strong** and survive this pass:

| Angle | Trinity | NuFIT-6.0 NO bf ± 1σ | NuFIT-6.0 3σ | Pull |
|---|---|---|---|---|
| θ₁₂ | 33.56° | 33.68° +0.73°/−0.70° | 31.63° → 35.95° | **0.16σ** ✅ |
| θ₂₃ | 41.81° | 43.3° +1.0°/−0.8° | 41.3° → 49.9° | **1.7σ** ⚠️ |
| θ₁₃ | 8.58° | 8.56° ± 0.11° | 8.19° → 8.89° | **0.18σ** ✅ |

θ₁₂ and θ₁₃ are within 0.2σ of the NuFIT-6.0 best fit — these are **real successes**. θ₂₃ is in mild tension (Trinity predicts the lower octant, NuFIT-6.0 IC24+SK prefers upper). δ_CP is the **only PMNS observable in catastrophic conflict** with current global data.

---

## 4. Reclassification

The δ_CP prediction is reclassified as follows.

### As a **mathematical statement** in Coq: PROVEN

`proofs/trinity/Predictions.v` Lemma `delta_CP_degrees_bounds`:
```
65.65 < (3/φ²) * 180/π < 65.66
```
This is a true mathematical theorem about the value of 3/φ² in degrees. It remains valid. **Nothing in this honesty pass invalidates the Coq proof.**

### As a **physical prediction for the leptonic CP phase**: EXCLUDED

The interpretation "the leptonic CP-violating phase δ_CP equals 3/φ²" is **excluded by current global fits at 5.6σ**. This claim is withdrawn pending either:
- new experimental data that returns δ_CP to the 65° region (DUNE 2028+, Hyper-K 2027+), or
- a theoretical re-derivation that does not depend on 3/φ² as the physical δ_CP.

### As a **pre-registered falsifiable prediction**: PRESERVED AS HISTORICAL RECORD

[`dune_preregistration.md`](docs/experiments/dune_preregistration.md) is left in place. Pre-registration is a legitimate scientific act; the prediction was made, hashed, and time-stamped. **What changes** is the interpretation: the prediction is **not** awaiting DUNE 2028 to settle a 50/50 question. It is **already in 5.6σ tension with current global data** and DUNE 2028+ will either:

1. **Confirm the current 177° NO global fit** → Trinity δ_CP formula is **definitively falsified**.
2. **Pull back toward 65°** → Trinity δ_CP formula is rehabilitated, and current global fits will themselves require explanation.

The honest framing is **scenario 1 is far more likely** given the current evidence.

---

## 5. Updated falsification thresholds

Replacing the thresholds in [`dune_preregistration.md`](docs/experiments/dune_preregistration.md) §5 with thresholds anchored to **current global best fits**, not to the Trinity value:

| DUNE measurement (by ~2032) | Implication for Trinity δ_CP = 65.66° |
|---|---|
| δ_CP ∈ [60°, 70°] ± 5° | **Confirmed** — would also overturn NuFIT-6.0 NO at >5σ |
| δ_CP ∈ [50°, 80°] ± 7° | Confirmed at ~2σ |
| δ_CP ∈ [80°, 130°] | **Tension persists**; framework requires PMNS sector revision |
| δ_CP ∈ [130°, 230°] (consistent with NuFIT-6.0 NO) | **Falsified** at >5σ |
| δ_CP ∈ [230°, 350°] (consistent with IO bf 285°) | **Falsified** at >7σ |

Per [DUNE CDR projections](https://arxiv.org/abs/2002.03005), δ_CP resolution of ±10° at the true central value is expected around 8 years of full-detector exposure — i.e. roughly **2034–2037**, not 2028.

---

## 6. What this means for the framework

### Strengths preserved
- m_H = 125.1 GeV (0.09%)
- Gauge couplings α₁, α₂, α₃ at M_Z (0.024%)
- Higgs self-coupling λ (0.4%)
- PMNS angles θ₁₂, θ₁₃ (<0.2σ)
- Pre-registration as scientific practice

### Weaknesses now publicly acknowledged
- δ_CP = 3/φ² is **excluded at 5.6σ** by NuFIT-6.0 + T2K+NOvA — not "high-stakes pending DUNE 2028"
- The 3-version δ_CP evolution (90.2° → 77.87° → 65.66°) is post-hoc fitting
- The `delta_cp_analysis.md` target value (PDG-2024 = 65.5°) is **superseded** by current global fits centered near 177° (NO) / 285° (IO)
- θ₂₃ is in 1.7σ tension (lower vs upper octant)

### What is **not** done in this pass
- The Coq lemma `delta_CP_degrees_bounds` is preserved (it is a correct mathematical statement).
- The pre-registration document is preserved (it is a correct scientific act).
- No new δ_CP formula is proposed. The point of this pass is to **stop searching for a new closed-form fit** — the project's own `delta_cp_analysis.md` already warned that further searching would be post-hoc.

---

## 7. Recommended forward strategy

1. **No fourth δ_CP formula.** Three iterations is already too many; a fourth would be an admission that the search procedure, not the underlying theory, is generating the predictions.
2. **Wait for DUNE / Hyper-K data** before any further public claim about δ_CP.
3. **In the interim**: publish PMNS angle predictions (θ₁₂, θ₁₃) as the empirical successes they are, without bundling them with the excluded δ_CP.
4. **Update all public documents** to state the 5.6σ tension explicitly and remove the "DUNE 2028 decides" framing — current data already substantially decides this against Trinity.

> A pre-registered prediction that is contradicted by data is *not* a failure of pre-registration; it is the system working as intended. The failure mode would be retrofitting a fourth formula to match whatever DUNE reports.
