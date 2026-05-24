# Related Work — Custom Floating-Point Formats and Hardware Accelerators

**Date:** 2026-05-25
**Scope:** Peer-reviewed and open-source silicon projects that overlap with
Trinity's GF16 / GoldenFloat family, plus φ-structured quantization
predecessors and exponent-compression research.

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

## 2. Golden Quantizer — Larsson et al. (arXiv 2017)

**Paper:** "The Golden Quantizer: Scalar Quantization Based on the Golden
Ratio and the Fibonacci Sequence"  
**Authors:** Daniel Larsson, Jens Rasmussen, Ulf Skoglund (Linköping University)  
**Venue:** arXiv:1709.03102 (2017)  
**Link:** [arXiv:1709.03102](https://arxiv.org/abs/1709.03102)

**Key idea:**
The authors construct a **scalar quantizer** whose reconstruction levels are
placed according to the golden angle (≈137.5°) in a spiral-phyllotaxis
packing. The resulting bins follow Fibonacci spacing, giving an optimal
lattice for isotropic sources in 2-D.

**Relevance to GF16:**
- This is the **closest published predecessor** to φ-structured quantization.
  The Golden Quantizer uses φ to decide *where to place quantization levels*;
  GF16 uses φ to decide *how to allocate bits between exponent and mantissa*.
- Both exploit the same mathematical identity: `φ² = φ + 1` creates a
  self-similar subdivision.

**Honest gap:**
The Golden Quantizer is **not a floating-point format**. It is a fixed
scalar quantizer for image coding. The jump from φ-lattice bins to
φ-optimal FP bit-split (Proposition 2 in the GoldenFloat paper) is
Trinity's contribution, not Larsson's. Citing the Golden Quantizer closes
the "no prior art" objection for φ-quantization, but does not close the
"why 6/9" objection — that requires the GoldenFloat formal propositions.

---

## 3. FlexiBit — UC Irvine (arXiv 2024–2025)

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

## 4. F-BFQ — University of Glasgow (arXiv 2025)

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

## 5. DB-Attn / DBFP — Southeast University / Houmo AI (arXiv 2025)

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

## 6. BBAL — Bidirectional Block Floating-Point (arXiv 2025)

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

## 7. Compression and Exponent-Concentrated Formats

### 7.1 ZipNN — IBM Research (arXiv 2025)

**Paper:** "ZipNN: Lossless Compression for Deep Learning Weights"  
**Authors:** Moshik Hershcovitch et al., IBM Research  
**Venue:** arXiv:2411.05239 (2025)  
**Link:** [arXiv:2411.05239](https://arxiv.org/abs/2411.05239)

**Key claim:**
- **~33% compression** on BF16 weights by exploiting the observation that
  **exponents dominate entropy** in neural-network parameter distributions.
- Lossless; no accuracy degradation.

**Relevance to GF16:**
Supports the Trinity claim that φ-structured exponents (clustered around
`log₂(φ) ≈ 0.694` spacing) can be compressed more efficiently than
IEEE-exponent patterns. The ZipNN result is independent evidence that
exponent concentration is a real, measurable phenomenon.

**Honest gap:**
ZipNN operates on **standard IEEE exponents**; it does not prove that a
φ-biased exponent would compress *even better*. That experiment has not been
done.

### 7.2 DFloat11 — Rice University (NeurIPS 2025)

**Paper:** "DFloat11: Dynamic Floating-Point with Huffman-Coded Exponents"  
**Authors:** Peiran Zhang et al., Rice University  
**Venue:** NeurIPS 2025 (arXiv:2504.11651)  
**Link:** [arXiv:2504.11651](https://arxiv.org/abs/2504.11651)

**Key claim:**
- Average **~11 bits** per weight (down from 16) by Huffman-coding the
  exponent field and sharing mantissa precision dynamically.
- ~30% effective bandwidth reduction with <0.1% accuracy loss on LLaMA-3.

**Relevance to GF16:**
DFloat11 and GF16 share the same core insight: **not all bit positions are
equally informative**. DFloat11 uses Huffman coding; GF16 uses φ-spacing.
Whether φ-spacing outperforms Huffman on physics-structured data is an
open empirical question.

**Honest gap:**
DFloat11 is a **dynamic software codec**; GF16 is a **static hardware format**.
Direct comparison requires measuring BPB on the same dataset with both
encoders — this has not been published.

### 7.3 ECF8 — Rice University (ICLR 2026)

**Paper:** "ECF8: Exponent-Concentrated FP8 for Deep Learning"  
**Authors:** Zhiwen Yang et al., Rice University  
**Venue:** ICLR 2026 (arXiv:2510.02676)  
**Link:** [arXiv:2510.02676](https://arxiv.org/abs/2510.02676)

**Key claim:**
- FP8 format whose exponent range is **concentrated** around the modes of
  SGD weight distributions, modeled as alpha-stable processes.
- Theoretical limit of **FP4.67** (4.67 effective bits) for the studied
  workloads.

**Relevance to GF16:**
ECF8 provides a **statistical justification** for exponent concentration:
weights are not uniformly distributed in log-space; they cluster. Trinity's
φ-quantizer makes a stronger geometric claim (the clusters sit at φ-spaced
lattice points), but ECF8's alpha-stable model is a rigorous alternative.

**Honest gap:**
ECF8 is **data-dependent** (re-tunes per layer); GF16 is **universal**
(single bias=31). The trade-off is flexibility vs. hardware simplicity.
No head-to-head benchmark exists.

---

## 8. Industry Microscaling Initiatives

### 8.1 OCP MX Alliance / Microscaling (2023)

**Paper:** "Microscaling Data Formats for Deep Learning"  
**Authors:** AMD, Arm, Intel, Meta, Microsoft, NVIDIA, Qualcomm (OCP joint)  
**Venue:** arXiv:2310.10537 (2023)  
**Link:** [arXiv:2310.10537](https://arxiv.org/abs/2310.10537)

**Key claim:**
- **MXFP8 / MXFP6 / MXFP4** formats with per-micro-block scaling factors
  (e.g., 32-element blocks).
- 4×–8× throughput improvement over fp16 on supported hardware.

**Relevance to GF16:**
MXFP4 and GF4 occupy the same 4-bit niche. The OCP standard is backed by
multiple vendors; GF4 is backed by a single open-silicon project. The OCP
approach uses block scaling; GF4 uses φ-structured mantissa.

**Honest gap:**
No OCP hardware implements φ-aware rounding or Lucas-chain anchors.
Trinity's 0x47C0 binding is a **proprietary design choice**, not a standard.

### 8.2 NVIDIA Blackwell (2024–2025)

**Product:** NVIDIA B100 / B200 / GB200 (Blackwell architecture)  
**Relevant features:**
- Native **FP4, FP6, FP8** support in Tensor Cores.
- **NVFP4** with micro-block scaling (2×4 blocks, similar to OCP MX).
- **5× inference throughput** vs. Hopper on FP4-quantized LLMs.

**Relevance to GF16:**
NVIDIA is pushing the industry to sub-8-bit formats. GF16/GF4 sit in the
same trajectory but from the **open-PDK / TinyTapeout** side. Blackwell
proves the market demand; Trinity's TTSKY26b submission proves the
feasibility on open silicon.

**Honest gap:**
Blackwell is **silicon-verified and shipping**; TTSKY26b is **submitted and
pending**. No performance comparison is meaningful until post-silicon data
is available.

### 8.3 AMD MI300 (2024)

**Product:** AMD Instinct MI300X  
**Relevant features:**
- Native **FP8** support but with a **different encoding** than NVIDIA H100.
- AMD uses E4M3 / E5M2; NVIDIA uses E4M3 / E5M2 with subtle bit-pattern
differences.

**Relevance to GF16:**
The AMD/NVIDIA FP8 split shows **industry fragmentation** in low-precision
formats. A vendor-neutral, φ-anchored format (GF16) could theoretically serve
as a unifying alternative — but only if it achieves comparable accuracy
and is adopted by a major compiler stack. That is not the case today.

**Honest gap:**
GF16 has **no compiler or framework support** (no PyTorch dtype, no ONNX
operator). The only runtime is the TinyTapeout Verilog wrapper.

---

## 9. AetherFloat — Keita Morisaki (2026)

**Paper:** "AetherFloat: A Quad-Radix Floating-Point Format for Deep Learning"  
**Author:** Keita Morisaki  
**Venue:** arXiv:2603.08741 (2026)  
**Link:** [arXiv:2603.08741](https://arxiv.org/abs/2603.08741)

**Key claim:**
- **Quad-radix (base-4)** FP format with block-scale-free encoding.
- **33.17% area reduction** vs. IEEE-754 fp32 on a 130nm test chip.
- Optimized for matrix-multiplication datapaths.

**Relevance to GF16:**
AetherFloat is the most recent **custom-layout competitor** to GF16. Both
reject IEEE-754 in favor of a domain-specific format. AetherFloat chooses
radix-4 for hardware simplicity; GF16 chooses φ-rooting for compression.

**Honest gap:**
- AetherFloat is **radix-4**, not φ-rooted. No golden-ratio connection.
- AetherFloat has a **130nm test chip**; GF16 has a **Sky130 tapeout
  pending** (TTSKY26a/b). The AetherFloat silicon result is ahead.
- No head-to-head benchmark on the same workload.

---

## 10. TinyTapeout / Open-Silicon Floating-Point Projects

### 10.1 `tt_um_float_synth` — NikLeberg

**Repo:** [github.com/NikLeberg/tt_um_float_synth](https://github.com/NikLeberg/tt_um_float_synth)  
**Shuttle:** IHP26A (TinyTapeout)

Synthesizes floating-point units (VHDL/Verilog) using open-source toolchains
(Yosys, GHDL, OpenROAD) on the IHP 130nm open PDK.

### 10.2 `Systolic_Array_with_DFT_v2` — Essenceia

**Repo:** [github.com/Essenceia/Systolic_Array_with_DFT_v2](https://github.com/Essenceia/Systolic_Array_with_DFT_v2)  
**Shuttle:** IHP26A (TinyTapeout)

2×2 bfloat16 matrix-multiplication accelerator with DFT (design-for-test)
infrastructure. Custom bfloat16: no subnormals, no NaN/∞, round-toward-zero
only.

**Relevance to Trinity:** These projects demonstrate that **custom FP formats
on open PDKs** are feasible and actively being taped out. Trinity's GF16
submission to TTSKY26a follows the same open-silicon methodology.

---

## 11. Custom FP for FPGAs (ECP5)

**Repo:** [Marc103/Floating-Point-Image-Processing-SV-RTL](https://github.com/Marc103/Floating-Point-Image-Processing-SV-RTL)

Custom, area-efficient FP adder/multiplier/divider in SystemVerilog for
FPGA deployment (ECP5). Allows custom exponent/fraction widths and
simplifies IEEE-754 features (no subnormals, simplified rounding) — similar
philosophy to DLFloat/GF16.

---

## 12. GoldenFloat Paper (t27 Project, NeurIPS 2026 OPT target)

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

## 13. Summary: Where Trinity Fits

| Project | Base | Layout | φ-aware? | Silicon? | Format type |
|---------|------|--------|----------|----------|-------------|
| **DLFloat16** | IBM | 1-6-9 bias 31 | No | Yes (VLSI 2018) | Custom FP16 |
| **Golden Quantizer** | Linköping | Fibonacci bins | **Yes** | No | Scalar quantizer |
| **GF16 / GoldenFloat** | Trinity | 1-6-9 bias 31 | **Yes** | Submitted (TTSKY26a/b) | Custom FP16 |
| **AetherFloat** | Morisaki | Quad-radix base-4 | No | Yes (130nm chip) | Custom FP |
| **FlexiBit** | UC Irvine | Arbitrary | No | FPGA/ASIC | Flexible FP/INT |
| **F-BFQ** | Glasgow | BFP | No | FPGA (KV260) | Block FP |
| **DB-Attn** | SEU/Houmo | BFP | No | FPGA/ASIC | Block FP |
| **BBAL** | SEU/Houmo | BBFP | No | ASIC | Block FP |
| **ZipNN** | IBM | BF16 + exponent codec | No | Software | Lossless codec |
| **DFloat11** | Rice | Huffman exponents | No | Software | Dynamic FP |
| **ECF8** | Rice | Alpha-stable FP8 | No | Software | Data-tuned FP8 |
| **MXFP4/6/8** | OCP | Micro-block scaled | No | Yes (multiple vendors) | Industry standard |
| **tt_um_float_synth** | Community | Custom | No | IHP26A submitted | Open-silicon FP |
| **Systolic_Array** | Community | bfloat16 subset | No | IHP26A submitted | Open-silicon FP |

**Trinity's unique claim:** The only project that combines (a) a proven
16-bit FP layout (DLFloat16) with (b) **three formal theorems** linking the
bit split to the golden ratio, (c) a **published φ-quantization predecessor**
(Golden Quantizer 2017), and (d) a **hardware-silicon binding**
(0x47C0 reset witness, Three Crowns milestones).

Whether the φ-structured quantization theory provides measurable compression
or accuracy advantages beyond the base DLFloat16 layout is an **open
empirical question** — tracked in `docs/hardware/bpb_benchmark.py`.

---

## 14. References

- `docs/hardware/gf16_spec.md` — Format specification with DLFloat16 relation
- `docs/hardware/gf16_mathematics.md` — φ-step and optimal field derivations
- `docs/hardware/silicon_anchor.md` — TTSKY26a/b submission status
- `docs/HARDWARE_ATTESTATION.md` — Honest proof inventory
