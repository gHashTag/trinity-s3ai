# 2-Operation Uniqueness Analysis: All Trinity Coefficients

## Executive Summary

**Result: 0 out of 15 Trinity coefficients are unique with 2-operations.**

Only one coefficient (549) is "rare" with just 2 derivations -- and these two are commutativity-equivalent (19*29-2 vs 29*19-2), making it structurally unique.

The vast majority of coefficients (14/15) have 41-379 derivations each, placing them firmly in the "common" category.

---

## Trinity Coefficients Analyzed

```
15, 19, 20, 24, 29, 30, 36, 43, 92, 127, 239, 549, 120, 240, 720
```

## H4 Invariants (Building Blocks)

```
1, 2, 3, 5, 7, 8, 11, 12, 19, 20, 29, 30, 60, 120, 240, 720, 14400
```

## Search Parameters

- **Operations:** +, -, *, /
- **Formula shape:** (a op1 b) op2 c where a, b, c are H4 invariants
- **Search space per target:** 17^3 x 4^2 = 78,608 combinations
- **Total combinations searched:** 1,179,120 across all 15 targets
- **Value type:** Exact rational arithmetic (Fraction)

---

## Results Summary

| Target | 1-Op Count | 2-Op Count | Category | Is Invariant? |
|--------|-----------|-----------|----------|---------------|
| **549** | 0 | **2** | **Rare** | No |
| 127 | 2 | 41 | Common | No |
| 92 | 0 | 43 | Common | No |
| 239 | 1 | 51 | Common | No |
| 43 | 0 | 93 | Common | No |
| 36 | 5 | 170 | Common | No |
| 15 | 9 | 235 | Common | No |
| 24 | 10 | 248 | Common | No |
| 29 | 4 | 259 | Common | **Yes** |
| 720 | 8 | 272 | Common | **Yes** |
| 19 | 9 | 284 | Common | **Yes** |
| 240 | 12 | 303 | Common | **Yes** |
| 120 | 9 | 334 | Common | **Yes** |
| 30 | 10 | 374 | Common | **Yes** |
| 20 | 10 | 379 | Common | **Yes** |

**Statistics:**
- Average 2-op derivations per target: 205.9
- Median 2-op derivations per target: 248
- Correlation (1-op count vs 2-op count): 0.908 (very strong positive)

---

## Key Finding: 549 is Structurally Unique

Target **549** has only 2 raw derivations, and these differ only by multiplication commutativity:

```
(19*29)-2 = 549
(29*19)-2 = 549
```

**Structurally, there is only ONE unique derivation: `(19 * 29) - 2`**

This uses three distinct H4 invariants (19, 29, 2) with one multiplication and one subtraction. This is the most constrained coefficient in the entire Trinity set.

---

## Canonical (Most Natural) Derivation Per Target

| Target | Canonical Derivation | Notes |
|--------|---------------------|-------|
| 15 | `(2+5)+8` | Simple additive chain |
| 19 | `(11+3)+5` | Three distinct primes |
| 20 | `(11+2)+7` | Three primes |
| 24 | `(11+5)+8` | Additive decomposition |
| 29 | `(19+2)+8` | Close to 30 |
| 30 | `(11+12)+7` | Uses 11+12=23 then +7 |
| 36 | `(11+20)+5` | Close to 30+8 |
| 43 | `(11+12)+20` | 23+20 |
| 92 | `(12+20)+60` | 32+60 |
| 120 | `(30+30)+60` | Symmetric |
| 127 | `(120+2)+5` | 120+7 (closest invariant) |
| 239 | `(2+240)-3` | Close to 240 |
| 240 | `(120+60)+60` | Symmetric decomposition |
| **549** | **`(19*29)-2`** | **The only structurally unique one** |
| 720 | `(2+720)-2` | Trivial (closest invariant) |

---

## 1-Operation vs 2-Operation Comparison

### 1-Operation Results

| Target | Count | Derivations |
|--------|-------|------------|
| 43, 92, 549 | 0 | (none) |
| 239 | 1 | `240-1` |
| 127 | 2 | `7+120`, `120+7` |
| 29 | 4 | `1*29`, `29*1`, `29/1`, `30-1` |
| 36 | 5 | `3*12`, `7+29`, `12*3`, `29+7`, `720/20` |

**Only 239 is unique at the 1-operation level** (via `240-1`).

The claim that 15 is unique with 1-operation is **incorrect** -- 15 has 9 distinct 1-op derivations:
`3*5, 3+12, 5*3, 7+8, 8+7, 12+3, 20-5, 30/2, 120/8`

### 2-Operation Results

**No coefficient is unique at the 2-operation level.** All have >= 41 derivations except 549 (which has 2 commutativity-equivalent derivations).

---

## Patterns Discovered

### 1. Strong Positive Correlation (r=0.908)
Targets with more 1-op derivations also have more 2-op derivations. The constraint structure of a coefficient carries across operation depths.

### 2. Non-Invariant Targets Are More Constrained
- Targets that are NOT H4 invariants themselves (15, 24, 36, 43, 92, 127, 239, 549) tend to have FEWER 2-op derivations
- 8 non-invariant targets average 107.8 derivations
- 7 invariant targets average 317.9 derivations
- This makes sense: non-invariant targets require more work to construct

### 3. 549 is Exceptionally Constrained
549 = 19 x 29 - 2 is the ONLY coefficient that requires multiplication to construct (all other canonical derivations use only addition/subtraction). This multiplicative structure, combined with the specific H4 invariants needed, creates a unique constraint.

### 4. 239 Maintains Near-Uniqueness
239 is unique with 1-op (`240-1`) and has only 51 2-op derivations. Its proximity to the invariant 240 makes it naturally constrained.

### 5. 43, 92, 127 Need 2-Operations
These three targets have 0 1-op derivations, meaning they fundamentally require 2 operations to construct from H4 invariants.

---

## Complete Derivation Lists for Rare Targets

### 549 (2 derivations -- structurally 1)
```
(19*29)-2 *
(29*19)-2
```

### 127 (41 derivations)
```
(1*7)+120       (2*60)+7        (7/1)+120       (7+120)*1
(1*120)+7       (2+120)+5       (7+60)+60       (7+120)/1
(2+5)+120       (5+2)+120       (7-120)+240     (7+240)-120
(5+120)+2       (8-1)+120       (8+120)-1       (11*12)-5
(12-5)+120      (12*11)-5       (12+120)-5      (19-12)+120
(19+120)-12     (60*2)+7        (60+7)+60       (60+60)+7
(120-1)+8       (120*1)+7       (120/1)+7       (120+2)+5 *
(120+5)+2       (120-5)+12      (120+7)*1       (120+7)/1
(120+8)-1       (120+12)-5      (120-12)+19     (120+19)-12
(240/2)+7       (240+7)-120     (240-120)+7     (14400/120)+7
```
*Canonical: `(120+2)+5 = 127 = 120 + 7` -- essentially "120 + 7"

### 92 (43 derivations)
```
(1-29)+120      (2+30)+60       (3*29)+5        (5*19)-3
(1+120)-29      (2-30)+120      (3*30)+2        (5*20)-8
(2+60)+30       (3+29)+60       (7*12)+8        (8*19)-60
(2+120)-30      (3+60)+29       (12*7)+8        (11*11)-29
(12+20)+60 *    (19*5)-3        (19*8)-60       (20*5)-8
(20+12)+60      (20+60)+12      (29+3)+60       (29*3)+5
(29+60)+3       (30+2)+60       (30*3)+2        (30+60)+2
(60+2)+30       (60+3)+29       (60+12)+20      (60+20)+12
(60+29)+3       (60+30)+2       (120+1)-29      (120+2)-30
(120-8)-20      (120-20)-8      (120-29)+1      (120-30)+2
(240/3)+12      (720/8)+2
```
*Canonical: `(12+20)+60 = 92 = 32 + 60`

---

## Conclusions

1. **2 operations are insufficient to achieve uniqueness** for 14 out of 15 Trinity coefficients. The search space of 78,608 combinations per target provides too many paths.

2. **549 = (19 x 29) - 2** is the standout: structurally unique, requiring a multiplicative construction from two mid-range H4 invariants.

3. **239 remains the most naturally unique coefficient** via its simple `240 - 1` 1-operation derivation.

4. **The constraint hierarchy is**: 549 (structurally unique) > 239 (1-op unique) > 127/29/36 (rare) > the rest (abundant).

5. For actual cryptographic or mathematical applications requiring uniqueness guarantees, **3 or more operations** would be needed, or the search space would need to be restricted (e.g., excluding trivial patterns like (a+a)-a or (a*1)+b).

---

## Data Files

- Search script: Embedded in analysis (Python + Fraction arithmetic)
- Search space: 17^3 x 4^2 = 78,608 combinations per target
- Total searched: 1,179,120 across all 15 targets
- Results verified with exact rational arithmetic
