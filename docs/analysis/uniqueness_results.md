# Uniqueness Enumeration: Trinity Coefficients from H4 Invariants

**H4 Invariants:** {1, 2, 7, 11, 12, 19, 20, 29, 30, 120, 240}

**Trinity Coefficients:** {1, 2, 3, 4, 8, 10, 14, 15, 18, 24, 36, 48, 92, 239, 549}

**Operations:** +, -, *, // (integer division)

---

## Summary Table

| Coefficient | Derivation Count | Unique? | Derivations |
|-------------|-----------------|---------|-------------|
| 1 | 16 | NO — 16 ways | 1 * 1 = 1; 1 // 1 = 1; 2 - 1 = 1; 2 // 2 = 1; 7 // 7 = 1; 11 // 11 = 1; 12 - 11 = 1; 12 // 12 = 1; 19 // 19 = 1; 20 - 19 = 1; 20 // 20 = 1; 29 // 29 = 1; 30 - 29 = 1; 30 // 30 = 1; 120 // 120 = 1; 240 // 240 = 1 |
| 2 | 5 | NO — 5 ways | 1 + 1 = 2; 1 * 2 = 2; 2 * 1 = 2; 2 // 1 = 2; 240 // 120 = 2 |
| 3 | 2 | NO — 2 ways | 1 + 2 = 3; 2 + 1 = 3 |
| 4 | 4 | NO — 4 ways | 2 + 2 = 4; 2 * 2 = 4; 11 - 7 = 4; 120 // 30 = 4 |
| 8 | 5 | NO — 5 ways | 1 + 7 = 8; 7 + 1 = 8; 19 - 11 = 8; 20 - 12 = 8; 240 // 30 = 8 |
| 10 | 6 | NO — 6 ways | 11 - 1 = 10; 12 - 2 = 10; 20 // 2 = 10; 29 - 19 = 10; 30 - 20 = 10; 120 // 12 = 10 |
| 14 | 5 | NO — 5 ways | 2 * 7 = 14; 2 + 12 = 14; 7 * 2 = 14; 7 + 7 = 14; 12 + 2 = 14 |
| 15 | 1 | YES | 30 // 2 = 15 |
| 18 | 6 | NO — 6 ways | 7 + 11 = 18; 11 + 7 = 18; 19 - 1 = 18; 20 - 2 = 18; 29 - 11 = 18; 30 - 12 = 18 |
| 24 | 3 | NO — 3 ways | 2 * 12 = 24; 12 * 2 = 24; 12 + 12 = 24 |
| 36 | 2 | NO — 2 ways | 7 + 29 = 36; 29 + 7 = 36 |
| 48 | 2 | NO — 2 ways | 19 + 29 = 48; 29 + 19 = 48 |
| 92 | 0 | NO — 0 ways | NONE |
| 239 | 1 | YES | 240 - 1 = 239 |
| 549 | 0 | NO — 0 ways | NONE |

**Total derivations:** 58
**Unique coefficients:** 2 / 15
**Non-unique coefficients:** [1, 2, 3, 4, 8, 10, 14, 18, 24, 36, 48, 92, 549]

---

## Detailed Derivation Breakdown

### Coefficient 1
**Derivation count:** 16

❌ **NON-UNIQUE — Multiple derivations:**
  1. 1 * 1 = 1  (operation: mul, a=1, b=1)
  2. 1 // 1 = 1  (operation: div, a=1, b=1)
  3. 2 - 1 = 1  (operation: sub, a=2, b=1)
  4. 2 // 2 = 1  (operation: div, a=2, b=2)
  5. 7 // 7 = 1  (operation: div, a=7, b=7)
  6. 11 // 11 = 1  (operation: div, a=11, b=11)
  7. 12 - 11 = 1  (operation: sub, a=12, b=11)
  8. 12 // 12 = 1  (operation: div, a=12, b=12)
  9. 19 // 19 = 1  (operation: div, a=19, b=19)
  10. 20 - 19 = 1  (operation: sub, a=20, b=19)
  11. 20 // 20 = 1  (operation: div, a=20, b=20)
  12. 29 // 29 = 1  (operation: div, a=29, b=29)
  13. 30 - 29 = 1  (operation: sub, a=30, b=29)
  14. 30 // 30 = 1  (operation: div, a=30, b=30)
  15. 120 // 120 = 1  (operation: div, a=120, b=120)
  16. 240 // 240 = 1  (operation: div, a=240, b=240)

### Coefficient 2
**Derivation count:** 5

❌ **NON-UNIQUE — Multiple derivations:**
  1. 1 + 1 = 2  (operation: add, a=1, b=1)
  2. 1 * 2 = 2  (operation: mul, a=1, b=2)
  3. 2 * 1 = 2  (operation: mul, a=2, b=1)
  4. 2 // 1 = 2  (operation: div, a=2, b=1)
  5. 240 // 120 = 2  (operation: div, a=240, b=120)

### Coefficient 3
**Derivation count:** 2

❌ **NON-UNIQUE — Multiple derivations:**
  1. 1 + 2 = 3  (operation: add, a=1, b=2)
  2. 2 + 1 = 3  (operation: add, a=2, b=1)

### Coefficient 4
**Derivation count:** 4

❌ **NON-UNIQUE — Multiple derivations:**
  1. 2 + 2 = 4  (operation: add, a=2, b=2)
  2. 2 * 2 = 4  (operation: mul, a=2, b=2)
  3. 11 - 7 = 4  (operation: sub, a=11, b=7)
  4. 120 // 30 = 4  (operation: div, a=120, b=30)

### Coefficient 8
**Derivation count:** 5

❌ **NON-UNIQUE — Multiple derivations:**
  1. 1 + 7 = 8  (operation: add, a=1, b=7)
  2. 7 + 1 = 8  (operation: add, a=7, b=1)
  3. 19 - 11 = 8  (operation: sub, a=19, b=11)
  4. 20 - 12 = 8  (operation: sub, a=20, b=12)
  5. 240 // 30 = 8  (operation: div, a=240, b=30)

### Coefficient 10
**Derivation count:** 6

❌ **NON-UNIQUE — Multiple derivations:**
  1. 11 - 1 = 10  (operation: sub, a=11, b=1)
  2. 12 - 2 = 10  (operation: sub, a=12, b=2)
  3. 20 // 2 = 10  (operation: div, a=20, b=2)
  4. 29 - 19 = 10  (operation: sub, a=29, b=19)
  5. 30 - 20 = 10  (operation: sub, a=30, b=20)
  6. 120 // 12 = 10  (operation: div, a=120, b=12)

### Coefficient 14
**Derivation count:** 5

❌ **NON-UNIQUE — Multiple derivations:**
  1. 2 * 7 = 14  (operation: mul, a=2, b=7)
  2. 2 + 12 = 14  (operation: add, a=2, b=12)
  3. 7 * 2 = 14  (operation: mul, a=7, b=2)
  4. 7 + 7 = 14  (operation: add, a=7, b=7)
  5. 12 + 2 = 14  (operation: add, a=12, b=2)

### Coefficient 15
**Derivation count:** 1

✅ **UNIQUE:** 30 // 2 = 15

### Coefficient 18
**Derivation count:** 6

❌ **NON-UNIQUE — Multiple derivations:**
  1. 7 + 11 = 18  (operation: add, a=7, b=11)
  2. 11 + 7 = 18  (operation: add, a=11, b=7)
  3. 19 - 1 = 18  (operation: sub, a=19, b=1)
  4. 20 - 2 = 18  (operation: sub, a=20, b=2)
  5. 29 - 11 = 18  (operation: sub, a=29, b=11)
  6. 30 - 12 = 18  (operation: sub, a=30, b=12)

### Coefficient 24
**Derivation count:** 3

❌ **NON-UNIQUE — Multiple derivations:**
  1. 2 * 12 = 24  (operation: mul, a=2, b=12)
  2. 12 * 2 = 24  (operation: mul, a=12, b=2)
  3. 12 + 12 = 24  (operation: add, a=12, b=12)

### Coefficient 36
**Derivation count:** 2

❌ **NON-UNIQUE — Multiple derivations:**
  1. 7 + 29 = 36  (operation: add, a=7, b=29)
  2. 29 + 7 = 36  (operation: add, a=29, b=7)

### Coefficient 48
**Derivation count:** 2

❌ **NON-UNIQUE — Multiple derivations:**
  1. 19 + 29 = 48  (operation: add, a=19, b=29)
  2. 29 + 19 = 48  (operation: add, a=29, b=19)

### Coefficient 92
**Derivation count:** 0

⚠️ **NO derivation found from H4 invariants with single binary operation!**

### Coefficient 239
**Derivation count:** 1

✅ **UNIQUE:** 240 - 1 = 239

### Coefficient 549
**Derivation count:** 0

⚠️ **NO derivation found from H4 invariants with single binary operation!**

---

## Operation-Type Analysis

| Operation | Count | Derivations |
|-----------|-------|-------------|
| add (+) | 16 | 1 + 1 = 2; 1 + 2 = 3; 2 + 1 = 3; 2 + 2 = 4; 1 + 7 = 8; 7 + 1 = 8; 2 + 12 = 14; 7 + 7 = 14; 12 + 2 = 14; 7 + 11 = 18; 11 + 7 = 18; 12 + 12 = 24; 7 + 29 = 36; 29 + 7 = 36; 19 + 29 = 48; 29 + 19 = 48 |
| sub (-) | 16 | 2 - 1 = 1; 12 - 11 = 1; 20 - 19 = 1; 30 - 29 = 1; 11 - 7 = 4; 19 - 11 = 8; 20 - 12 = 8; 11 - 1 = 10; 12 - 2 = 10; 29 - 19 = 10; 30 - 20 = 10; 19 - 1 = 18; 20 - 2 = 18; 29 - 11 = 18; 30 - 12 = 18; 240 - 1 = 239 |
| mul (*) | 8 | 1 * 1 = 1; 1 * 2 = 2; 2 * 1 = 2; 2 * 2 = 4; 2 * 7 = 14; 7 * 2 = 14; 2 * 12 = 24; 12 * 2 = 24 |
| div (//) | 18 | 1 // 1 = 1; 2 // 2 = 1; 7 // 7 = 1; 11 // 11 = 1; 12 // 12 = 1; 19 // 19 = 1; 20 // 20 = 1; 29 // 29 = 1; 30 // 30 = 1; 120 // 120 = 1; 240 // 240 = 1; 2 // 1 = 2; 240 // 120 = 2; 120 // 30 = 4; 240 // 30 = 8; 20 // 2 = 10; 120 // 12 = 10; 30 // 2 = 15 |

---

## Appendix: Full Pair Enumeration

All results of a op b for every (a,b) in H4 × H4:

| a | b | a+b | a-b | a*b | a//b |
|---|---|-----|-----|-----|------|
| 1 | 1 | 2 | 0 | 1 | 1 |
| 1 | 2 | 3 | -1 | 2 | N/A |
| 1 | 7 | 8 | -6 | 7 | N/A |
| 1 | 11 | 12 | -10 | 11 | N/A |
| 1 | 12 | 13 | -11 | 12 | N/A |
| 1 | 19 | 20 | -18 | 19 | N/A |
| 1 | 20 | 21 | -19 | 20 | N/A |
| 1 | 29 | 30 | -28 | 29 | N/A |
| 1 | 30 | 31 | -29 | 30 | N/A |
| 1 | 120 | 121 | -119 | 120 | N/A |
| 1 | 240 | 241 | -239 | 240 | N/A |
| 2 | 1 | 3 | 1 | 2 | 2 |
| 2 | 2 | 4 | 0 | 4 | 1 |
| 2 | 7 | 9 | -5 | 14 | N/A |
| 2 | 11 | 13 | -9 | 22 | N/A |
| 2 | 12 | 14 | -10 | 24 | N/A |
| 2 | 19 | 21 | -17 | 38 | N/A |
| 2 | 20 | 22 | -18 | 40 | N/A |
| 2 | 29 | 31 | -27 | 58 | N/A |
| 2 | 30 | 32 | -28 | 60 | N/A |
| 2 | 120 | 122 | -118 | 240 | N/A |
| 2 | 240 | 242 | -238 | 480 | N/A |
| 7 | 1 | 8 | 6 | 7 | 7 |
| 7 | 2 | 9 | 5 | 14 | N/A |
| 7 | 7 | 14 | 0 | 49 | 1 |
| 7 | 11 | 18 | -4 | 77 | N/A |
| 7 | 12 | 19 | -5 | 84 | N/A |
| 7 | 19 | 26 | -12 | 133 | N/A |
| 7 | 20 | 27 | -13 | 140 | N/A |
| 7 | 29 | 36 | -22 | 203 | N/A |
| 7 | 30 | 37 | -23 | 210 | N/A |
| 7 | 120 | 127 | -113 | 840 | N/A |
| 7 | 240 | 247 | -233 | 1680 | N/A |
| 11 | 1 | 12 | 10 | 11 | 11 |
| 11 | 2 | 13 | 9 | 22 | N/A |
| 11 | 7 | 18 | 4 | 77 | N/A |
| 11 | 11 | 22 | 0 | 121 | 1 |
| 11 | 12 | 23 | -1 | 132 | N/A |
| 11 | 19 | 30 | -8 | 209 | N/A |
| 11 | 20 | 31 | -9 | 220 | N/A |
| 11 | 29 | 40 | -18 | 319 | N/A |
| 11 | 30 | 41 | -19 | 330 | N/A |
| 11 | 120 | 131 | -109 | 1320 | N/A |
| 11 | 240 | 251 | -229 | 2640 | N/A |
| 12 | 1 | 13 | 11 | 12 | 12 |
| 12 | 2 | 14 | 10 | 24 | 6 |
| 12 | 7 | 19 | 5 | 84 | N/A |
| 12 | 11 | 23 | 1 | 132 | N/A |
| 12 | 12 | 24 | 0 | 144 | 1 |
| 12 | 19 | 31 | -7 | 228 | N/A |
| 12 | 20 | 32 | -8 | 240 | N/A |
| 12 | 29 | 41 | -17 | 348 | N/A |
| 12 | 30 | 42 | -18 | 360 | N/A |
| 12 | 120 | 132 | -108 | 1440 | N/A |
| 12 | 240 | 252 | -228 | 2880 | N/A |
| 19 | 1 | 20 | 18 | 19 | 19 |
| 19 | 2 | 21 | 17 | 38 | N/A |
| 19 | 7 | 26 | 12 | 133 | N/A |
| 19 | 11 | 30 | 8 | 209 | N/A |
| 19 | 12 | 31 | 7 | 228 | N/A |
| 19 | 19 | 38 | 0 | 361 | 1 |
| 19 | 20 | 39 | -1 | 380 | N/A |
| 19 | 29 | 48 | -10 | 551 | N/A |
| 19 | 30 | 49 | -11 | 570 | N/A |
| 19 | 120 | 139 | -101 | 2280 | N/A |
| 19 | 240 | 259 | -221 | 4560 | N/A |
| 20 | 1 | 21 | 19 | 20 | 20 |
| 20 | 2 | 22 | 18 | 40 | 10 |
| 20 | 7 | 27 | 13 | 140 | N/A |
| 20 | 11 | 31 | 9 | 220 | N/A |
| 20 | 12 | 32 | 8 | 240 | N/A |
| 20 | 19 | 39 | 1 | 380 | N/A |
| 20 | 20 | 40 | 0 | 400 | 1 |
| 20 | 29 | 49 | -9 | 580 | N/A |
| 20 | 30 | 50 | -10 | 600 | N/A |
| 20 | 120 | 140 | -100 | 2400 | N/A |
| 20 | 240 | 260 | -220 | 4800 | N/A |
| 29 | 1 | 30 | 28 | 29 | 29 |
| 29 | 2 | 31 | 27 | 58 | N/A |
| 29 | 7 | 36 | 22 | 203 | N/A |
| 29 | 11 | 40 | 18 | 319 | N/A |
| 29 | 12 | 41 | 17 | 348 | N/A |
| 29 | 19 | 48 | 10 | 551 | N/A |
| 29 | 20 | 49 | 9 | 580 | N/A |
| 29 | 29 | 58 | 0 | 841 | 1 |
| 29 | 30 | 59 | -1 | 870 | N/A |
| 29 | 120 | 149 | -91 | 3480 | N/A |
| 29 | 240 | 269 | -211 | 6960 | N/A |
| 30 | 1 | 31 | 29 | 30 | 30 |
| 30 | 2 | 32 | 28 | 60 | 15 |
| 30 | 7 | 37 | 23 | 210 | N/A |
| 30 | 11 | 41 | 19 | 330 | N/A |
| 30 | 12 | 42 | 18 | 360 | N/A |
| 30 | 19 | 49 | 11 | 570 | N/A |
| 30 | 20 | 50 | 10 | 600 | N/A |
| 30 | 29 | 59 | 1 | 870 | N/A |
| 30 | 30 | 60 | 0 | 900 | 1 |
| 30 | 120 | 150 | -90 | 3600 | N/A |
| 30 | 240 | 270 | -210 | 7200 | N/A |
| 120 | 1 | 121 | 119 | 120 | 120 |
| 120 | 2 | 122 | 118 | 240 | 60 |
| 120 | 7 | 127 | 113 | 840 | N/A |
| 120 | 11 | 131 | 109 | 1320 | N/A |
| 120 | 12 | 132 | 108 | 1440 | 10 |
| 120 | 19 | 139 | 101 | 2280 | N/A |
| 120 | 20 | 140 | 100 | 2400 | 6 |
| 120 | 29 | 149 | 91 | 3480 | N/A |
| 120 | 30 | 150 | 90 | 3600 | 4 |
| 120 | 120 | 240 | 0 | 14400 | 1 |
| 120 | 240 | 360 | -120 | 28800 | N/A |
| 240 | 1 | 241 | 239 | 240 | 240 |
| 240 | 2 | 242 | 238 | 480 | 120 |
| 240 | 7 | 247 | 233 | 1680 | N/A |
| 240 | 11 | 251 | 229 | 2640 | N/A |
| 240 | 12 | 252 | 228 | 2880 | 20 |
| 240 | 19 | 259 | 221 | 4560 | N/A |
| 240 | 20 | 260 | 220 | 4800 | 12 |
| 240 | 29 | 269 | 211 | 6960 | N/A |
| 240 | 30 | 270 | 210 | 7200 | 8 |
| 240 | 120 | 360 | 120 | 28800 | 2 |
| 240 | 240 | 480 | 0 | 57600 | 1 |

---

*Generated by uniqueness_enumeration.py*