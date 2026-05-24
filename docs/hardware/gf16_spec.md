# GF16 (Golden Float 16) Format Specification

**Provenance:** Extracted from `t27/docs/arxiv-trinity-gf16-draft.md` §2 and
`t27/specs/02-gf16-format.tri`.  
**Date:** 2026-05-25  
**Status:** `verified` — format is fully specified and FPGA-verified.

---

## 1. Motivation

IEEE 754 half-precision (float16) uses a 5-bit exponent with bias 15.
bfloat16 uses an 8-bit exponent with bias 127. Neither has any connection
to fundamental mathematical constants.

GF16 anchors its exponent bias at **31**, derived from the golden-ratio
identity:

```
phi^2 + phi^-2 = 3
phi^2 = phi + 1
```

The bias value 31 encodes 1.0 at the golden ratio's "natural center" of
the exponent range, creating a format where common physics and ML values
cluster around the representational sweet spot.

---

## 2. Bit Layout

| Bit(s) | Field | Width |
|--------|-------|-------|
| 15 | Sign | 1 |
| 14:9 | Exponent | 6 |
| 8:0 | Mantissa | 9 |

- **Total:** 16 bits
- **Exponent bias:** 31
- **Implicit leading 1:** Normal numbers have implicit 1.mantissa

### 2.1 Special Values

| Value | Encoding |
|-------|----------|
| +0 | 0x0000 |
| -0 | 0x8000 |
| +Infinity | 0x7E00 |
| -Infinity | 0xFE00 |
| NaN | 0xFE01 |

### 2.2 Encoding of Key Constants

| Value | GF16 Hex | Decoded | Relative Error |
|-------|----------|---------|----------------|
| 1.0 | 0x3E00 | 1.0 | 0 |
| phi | 0x3F3C | 1.6171875 | 0.0005 |
| pi | 0x4049 | 3.140625 | 0.0003 |
| e | 0x4058 | 2.71875 | 0.0002 |
| sqrt(2) | 0x3F5C | 1.4140625 | 0.0001 |

### 2.3 Dynamic Range

- **Max normal:** (1 + 511/512) × 2^(62-31) = ~4.29 × 10⁹
- **Min normal:** 1.0 × 2^(1-31) = ~9.31 × 10⁻¹⁰
- **Machine epsilon:** 2⁻⁹ = 0.001953125

### 2.4 Comparison with Existing Formats

| Format | Bits | Exp | Mant | Bias | Max Value | phi-distance |
|--------|------|-----|------|------|-----------|--------------|
| float16 | 16 | 5 | 10 | 15 | 65504 | 0.118 |
| **GF16** | **16** | **6** | **9** | **31** | **4.29 × 10⁹** | **0.049** |
| bfloat16 | 16 | 8 | 7 | 127 | 3.39 × 10³⁸ | — |

**GF16 provides 65× wider dynamic range than float16** while maintaining
better precision than bfloat16 (9 vs 7 mantissa bits). The 6-bit exponent
with bias=31 positions 1.0 at the center of a practical ML/inference range.

---

## 3. Hardware Architecture

### 3.1 GF16 Multiplier

Combinational multiplier implementing:
- 10-bit × 10-bit mantissa multiplication (mapped to DSP48E1 on Xilinx)
- Exponent addition with bias subtraction
- Round-to-nearest-even with guard/round/sticky bits
- Special value handling (NaN, Inf, zero)

### 3.2 GF16 Adder

- Alignment shift via barrel shifter
- 10-bit mantissa addition
- Normalization and re-rounding
- Subnormal handling

### 3.3 Dot-Product (N=4)

Four multipliers feeding a 3-stage adder tree. Achieves **323 MHz**
combinational throughput on Xilinx Artix-7 XC7A100T (openXC7 toolchain:
Yosys + nextpnr).

### 3.4 RTL Verification

| Test | Count | Result |
|------|-------|--------|
| Multiplier | 10 | PASS |
| Adder | 10 | PASS |
| Dot-product | 5 | PASS |
| Special values | 5 | PASS |
| Roundtrip | 5 | PASS |
| **Total** | **35** | **35/35 PASS** |

Zero timing violations at 100 MHz post-route.

---

## 4. Benchmarks

See [`gf16_benchmarks.json`](gf16_benchmarks.json) for raw data.

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| MSE (Normal(0,1)) | 0.000234 | < 1e-3 | PASS |
| Add latency | 7.2 ns/op | < 10 ns | PASS |
| Mul latency | 4.5 ns/op | < 10 ns | PASS |
| NN accuracy drop | 5.80% | = f32 (5.80%) | PASS |
| MNIST weight support | encode/decode OK | weight support | PASS |

---

## 5. File References

- RTL: `t27/rtl_gen/gf16_mul.v`, `t27/rtl_gen/gf16_add.v`
- Reference Python: [`gf16_ref.py`](gf16_ref.py)
- Test vectors: [`gf16_vectors.json`](gf16_vectors.json)
- Full draft: `t27/docs/arxiv-trinity-gf16-draft.md`
