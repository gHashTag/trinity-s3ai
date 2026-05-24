# Related Work — Custom Floating-Point Formats and Hardware Accelerators

**Date:** 2026-05-25
**Scope:** Peer-reviewed and open-source silicon projects that overlap with
Trinity's GF16 / GoldenFloat family.

---

## 1. DLFloat16 — IBM Research (ARITH 2019)

**Paper:** "DLFloat: A 16-b Floating Point Format Designed for Deep Learning
Training and Inference"  
**Authors:** IBM Research  
**Venue:** ARITH 2019 / VLSI 2018 (silicon demonstration)  
**Link:** [IBM Research publication](https://research.ibm.com/publications/dlfloat-a-16-b-floating-point-format-designed-for-deep-learning-training-and-inference)

**Overlap with GF16:**
- **Identical bit layout:** 1 sign + 6 exponent + 9 mantissa, bias 31.
- **Silicon proof:** IBM built a 1.5 TFLOPS AI core with **512 DLFloat16
  FPUs**, demonstrating ~20× area savings over 64-bit FPUs.

**Difference:**
- DLFloat16 was designed for **deep-learning training convergence** (gradient
  dynamic range).
- GF16 re-interprets the same layout as a **φ-anchored quantization basis**
  for physics-structured data.

**Honesty note:** Trinity does not claim the 1-6-9 layout as original. The
original contribution is the φ-semantic overlay (bias=31 chosen to anchor
1.0 at the φ center, not the DL midpoint) and the hardware-silicon binding
(0x47C0, Three Crowns).

---

## 2. FlexiBit — UC Irvine (arXiv 2024–2025)

**Paper:** arXiv:2411.18065v2 (June 2025)  
**Title:** "FlexiBit: A Fully Flexible Precision Bit-Parallel Accelerator for
Quantized Deep Learning"  
**Link:** [arXiv:2411.18065](https://arxiv.org/pdf/2411.18065)

**Relevance:**
- Hardware accelerator supporting **arbitrary-precision FP and INT** in
  bit-parallel fashion.
- Flexible Bit Reduction Tree (FBRT) and flexible bit exponent adder (FBEA).
- 1.66× higher performance/area on GPT-3 (FP6) vs. Tensor Core-like
  architectures.

**Difference from Trinity:** FlexiBit uses standard binary (base-2) arithmetic
with flexible bit-width allocation, not a φ-structured quantization ladder.

---

## 3. F-BFQ — University of Glasgow (arXiv 2025)

**Paper:** arXiv:2510.13401v1 (October 2025)  
**Title:** "F-BFQ: An FPGA-based Flexible Block Floating-Point Quantization
Accelerator for LLMs"  
**Link:** [arXiv:2510.13401](https://arxiv.org/pdf/2510.13401)

**Relevance:**
- FPGA-based edge accelerator for Block Floating-Point (BFP) quantized LLMs.
- Dynamic switching between Q2_K and Q3_K variants without reconfiguration.
- Deployed on AMD Kria KV260; ~1.4× speedup over Arm NEON.

**Difference:** Standard binary BFP, not φ-structured formats.

---

## 4. DB-Attn / DBFP — Southeast University / Houmo AI (arXiv 2025)

**Paper:** arXiv:2502.00026v2 (February 2025)  
**Title:** "Pushing the Limits of BFP on Narrow Precision LLM Inference"  
**Link:** [arXiv:2502.00026](https://arxiv.org/html/2502.00026v2)

**Relevance:**
- Dynamic Block Floating-Point (DBFP) for nonlinear Transformer operations
  (Softmax, GELU, SILU).
- 74% GPU speedup on LLaMA Softmax; 10× FOM improvement over prior FPGA
  Softmax accelerators.

**Difference:** Extends BFP within standard binary arithmetic; no φ-quantization.

---

## 5. BBAL — Bidirectional Block Floating-Point (arXiv 2025)

**Paper:** arXiv:2504.15721v1 (April 2025)  
**Title:** "BBAL: A Bidirectional Block Floating Point-Based Quantisation
Accelerator"  
**Link:** [arXiv:2504.15721](https://arxiv.org/pdf/2504.15721)

**Relevance:**
- Bidirectional BFP (BBFP) with 1-bit flag + overlap bits for outlier capture.
- 22% accuracy improvement vs. outlier-aware accelerators at similar
  efficiency.

**Difference:** Standard binary with novel exponent-alignment strategy, not
φ-based.

---

## 6. TinyTapeout / Open-Silicon Floating-Point Projects

### 6.1 `tt_um_float_synth` — NikLeberg

**Repo:** [github.com/NikLeberg/tt_um_float_synth](https://github.com/NikLeberg/tt_um_float_synth)  
**Shuttle:** IHP26A (TinyTapeout)

Synthesizes floating-point units (VHDL/Verilog) using open-source toolchains
(Yosys, GHDL, OpenROAD) on the IHP 130nm open PDK.

### 6.2 `Systolic_Array_with_DFT_v2` — Essenceia

**Repo:** [github.com/Essenceia/Systolic_Array_with_DFT_v2](https://github.com/Essenceia/Systolic_Array_with_DFT_v2)  
**Shuttle:** IHP26A (TinyTapeout)

2×2 bfloat16 matrix-multiplication accelerator with DFT (design-for-test)
infrastructure. Custom bfloat16: no subnormals, no NaN/∞, round-toward-zero
only.

**Relevance to Trinity:** These projects demonstrate that **custom FP formats
on open PDKs** are feasible and actively being taped out. Trinity's GF16
submission to TTSKY26a follows the same open-silicon methodology.

---

## 7. Custom FP for FPGAs (ECP5)

**Repo:** [Marc103/Floating-Point-Image-Processing-SV-RTL](https://github.com/Marc103/Floating-Point-Image-Processing-SV-RTL)

Custom, area-efficient FP adder/multiplier/divider in SystemVerilog for
FPGA deployment (ECP5). Allows custom exponent/fraction widths and
simplifies IEEE-754 features (no subnormals, simplified rounding) — similar
philosophy to DLFloat/GF16.

---

### 6.5 GoldenFloat Paper (t27 Project, NeurIPS 2026 OPT target)

**Paper:** "GoldenFloat: A Formally Verified, φ-Optimal Floating-Point
Family for Ternary-Native Mixed-Precision Computing" (April 2026)  
**Target:** NeurIPS 2026 OPT Workshop  
**Authors:** t27 Project Team

**Formal results:**
- **Proposition 1 (Golden Self-Similarity):** φ is the unique self-similar
  proportion for bit allocation. Proven from first principles; not an
  optimization outcome.
- **Proposition 2 (Optimal Integer Rounding):** `round((N−1)/φ²)` gives the
  optimal exponent split; verified 7/7 for the GoldenFloat family.
- **Theorem 3 (Universal Attractor):** φ is the unique fixed point of the
  balancing recursion `f(x) = (x + x⁻¹ + 1)/2` (Banach fixed-point proof).

**Honest limitations stated in the paper:**
- "No ternary hardware implementation: GF benchmarks are software
  simulations. Direct hardware comparison requires ternary silicon, which
  does not yet exist."
- "Universal optimality: φ-guided allocation is not proven optimal for all
  possible workloads."
- "General irrational constants: For π, e, and other irrationals without
  denominator factor 3, GF does not have advantage over IEEE formats."

**Note:** The NeurIPS paper does **not** cite DLFloat16. This is a
documentation gap that should be closed in the camera-ready version.

---

## 8. Summary: Where Trinity Fits

| Project | Base | Layout | φ-aware? | Silicon? |
|---------|------|--------|----------|----------|
| **DLFloat16** | IBM | 1-6-9 bias 31 | No | Yes (VLSI 2018) |
| **GF16 / GoldenFloat** | Trinity | 1-6-9 bias 31 | **Yes** | Submitted (TTSKY26a) |
| **FlexiBit** | UC Irvine | Arbitrary | No | FPGA/ASIC |
| **F-BFQ** | Glasgow | BFP | No | FPGA (KV260) |
| **DB-Attn** | SEU/Houmo | BFP | No | FPGA/ASIC |
| **BBAL** | SEU/Houmo | BBFP | No | ASIC |
| **tt_um_float_synth** | Community | Custom | No | IHP26A submitted |
| **Systolic_Array** | Community | bfloat16 subset | No | IHP26A submitted |

**Trinity's unique claim:** The only project that combines (a) a proven
16-bit FP layout (DLFloat16) with (b) **three formal theorems** linking the
bit split to the golden ratio, and (c) a **hardware-silicon binding**
(0x47C0 reset witness, Three Crowns milestones).

Whether the φ-structured quantization theory provides measurable compression
or accuracy advantages beyond the base DLFloat16 layout is an **open
empirical question** — tracked in `docs/hardware/bpb_benchmark.py`.

---

## 9. References

- `docs/hardware/gf16_spec.md` — Format specification with DLFloat16 relation
- `docs/hardware/gf16_mathematics.md` — φ-step and optimal field derivations
- `docs/hardware/silicon_anchor.md` — TTSKY26a submission status
- `docs/HARDWARE_ATTESTATION.md` — Honest proof inventory
