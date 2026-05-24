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

## 9. Posit Hardware Ecosystem (2025–2026)

The **Posit** format (Gustafson 2017) is historically orthogonal to GF16 — it
uses variable-length regime fields and a *quire* accumulator rather than
fixed IEEE-style exponent/mantissa. However, 2025–2026 saw a surge in
Posit hardware prototypes that occupy the same "custom low-bit format" niche
as GF4/GF16.

### 9.1 PVU — Posit Vector Unit (arXiv 2025)

**Paper:** "PVU: A Posit Vector Processor Unit Based on RISC-V Extension for
Advanced Floating-Point Computation"  
**Authors:** Southwest University of Science and Technology  
**Venue:** arXiv:2503.01313v1 (March 2025)  
**Link:** [arXiv:2503.01313](https://arxiv.org/abs/2503.01313)

**Key claim:**
- First **open-source Posit Vector Arithmetic Unit** in Chisel, integrated with
  RISC-V Vector Extension (RVV).
- Supports vector add/sub/mul/div/dot with parameterized bit-width and
  exponent size (`ES`).
- FPGA validation: **65,407 LUTs**, 100% accuracy for add/mul/dot, 95.84% for
  div (Newton reciprocal).

**Honest gap:**
- Posit variable-length regime is **fundamentally different** from GF16's
  fixed 1-6-9 layout. No φ-connection whatsoever.
- PVU is **vector CPU**, not dot-product accelerator. Different design point.

### 9.2 SPADE — SIMD Posit MAC for DNNs (arXiv 2026)

**Paper:** "SPADE: A SIMD Posit-enabled Compute Engine for Accelerating DNN
Efficiency"  
**Authors:** IIT Indore et al.  
**Venue:** arXiv:2601.17279 (January 2026)  
**Link:** [arXiv:2601.17279](https://arxiv.org/abs/2601.17279)

**Key claim:**
- Unified multi-precision Posit MAC supporting Posit(8,0), Posit(16,1),
  Posit(32,2) via hierarchical lane fusion.
- ASIC (TSMC 28nm): **1.38 GHz at 6.1 mW**, 0.025 mm².
- FPGA (Virtex-7): **45.13% LUT reduction** vs standalone Posit MACs.

**Honest gap:**
- Multi-precision fusion is **similar in spirit** to GoldenFloat family
  (GF4–GF32), but Posit uses quire accumulation, not φ-spacing.
- No physics-data accuracy claims; evaluated on MNIST/CIFAR-10 only.

### 9.3 B-Posit — Bounded-Regime Posit (arXiv 2026)

**Paper:** "Closing the Gap Between Float and Posit Hardware Efficiency"  
**Authors:** BITS Pilani / Arizona State University  
**Venue:** arXiv:2603.01615v1 (March 2026)  
**Link:** [arXiv:2603.01615](https://arxiv.org/abs/2603.01615)

**Key claim:**
- **b-posit** limits max regime length (`rS = 6`) to reduce variable-length
  decode overhead, compensating with larger exponent (`eS = 5`).
- Post-layout ASIC (FreePDK45): b-posit32 decoder is **79% less power**,
  **71% smaller area**, **60% lower latency** than standard posit32 decoder.
- At 64-bit, b-posit decode is **2× faster** than IEEE float64, **3× faster**
  than standard posit64.

**Honest gap:**
- B-Posit **beats IEEE float on hardware efficiency** — a rare result for
  non-standard formats. This raises the bar for any new format (including
  GF16) to prove similar efficiency gains.
- No golden-ratio connection; the bounded-regime trick is purely engineering.

### 9.4 EULER-ADAS — Approximate B-Posit Engine (arXiv 2026)

**Paper:** "EULER-ADAS: Energy-Efficient & SIMD-Unified Logarithmic-Posit
Engine for Precision-Reconfigurable Approximate ADAS Acceleration"  
**Authors:** IIT Indore, University of Ljubljana, Bar-Ilan University  
**Venue:** arXiv:2605.06875 (May 2026)  
**Link:** [arXiv:2605.06875](https://arxiv.org/abs/2605.06875)

**Key claim:**
- First **approximate Bounded-Posit neural compute engine** combining:
  bounded-regime Posit + stage-adaptive logarithmic multiplier (ILM) +
  SIMD-shared quire accumulation.
- ASIC (28nm): **0.013–0.016 mm²**, **19.8–22.1 mW**, **1.84 GHz**.
- **10× lower EDP** than exact radix-4 Booth Posit multipliers.
- Tiny-YOLOv3 on Pynq-Z2: **78 ms/frame at 0.29 W** (22.6 mJ/frame).

**Honest gap:**
- Approximate arithmetic is **not comparable** to GF16's exact φ-structured
  rounding. Different accuracy/complexity trade-off.
- Posit quire accumulator has no GF16 equivalent.

---

## 10. Logarithmic Number Systems for Deep Learning (2025)

### 10.1 Dynamic LNS for LLMs — PNNL (MICRO 2024 / Jan 2025)

**Paper:** "Bridging the Gap Between LLMs and LNS with Dynamic Data Format
and Architecture Codesign"  
**Authors:** Pacific Northwest National Laboratory (PNNL)  
**Venue:** MICRO 2024 (published January 2025)  
**Link:** [PNNL publication](https://www.pnnl.gov/publications/bridging-gap-between-llms-and-lns-dynamic-data-format-and-architecture-codesign)

**Key claim:**
- **Dynamic LNS** format with per-vector outlier detection, allocating higher
  precision to outliers via flexible encoding.
- Implemented on Alveo U280 FPGA systolic array.
- **15.4% accuracy improvement** over floating-point and **16% over original
  LNS** on four state-of-the-art LLMs.
- NVIDIA has demonstrated LNS potential for next-generation tensor cores.

**Relevance to GF16:**
Both GF16 and Dynamic LNS reject uniform IEEE-754 in favor of a **domain-
specific encoding**: GF16 uses φ-spacing, LNS uses log-domain quantization
with outlier-aware dynamic range.

**Honest gap:**
- LNS requires **log/exp conversion** on every operation; GF16 uses standard
  FP add/mul with bias=31. The hardware cost models are not comparable.
- No head-to-head accuracy or compression benchmark.

---

## 11. M2XFP — Shanghai Jiao Tong University / Huawei (ASPLOS 2026)

**Paper:** "M²XFP: A Metadata-Augmented Microscaling Data Format for
Efficient Low-bit Quantization"  
**Authors:** Weiming Hu et al., SJTU + Huawei  
**Venue:** ASPLOS 2026 (arXiv:2601.19213)  
**Code:** [SJTU-ReArch-Group/M2XFP_ASPLOS26](https://github.com/SJTU-ReArch-Group/M2XFP_ASPLOS26)  
**Link:** [arXiv:2601.19213](https://arxiv.org/abs/2601.19213)

**Key claim:**
- **4.5 effective bits** per element (0.25 bits metadata overhead on top of
  FP4) via hybrid metadata: element-level extra mantissa (Elem-EM) for
  dynamic activations, subgroup-level extra mantissa + adaptive shared scale
  for static weights.
- Hardware PE tile is **~4.0% larger** than MXFP4 PE, adding only decoder
  and shift-and-add logic (no multipliers).
- **70.63% accuracy-loss reduction** vs MXFP4 on LLaMA-2/3, Mistral, Falcon,
  OPT benchmarks. **1.91× speedup** and **1.75× energy savings** vs MicroScopiQ
  baseline.

**Relevance to GF16:**
M2XFP addresses the same core problem as GF4: **4-bit quantization is too
coarse for LLM weights**. M2XFP solves it with metadata augmentation; GF4
solves it with φ-structured mantissa spacing. Both are custom low-bit formats
that reject vanilla FP4.

**Honest gap:**
- M2XFP has **peer-reviewed ASPLOS acceptance** + **open evaluation code**;
  GF4 has neither yet.
- M2XFP targets **LLM inference** with proven accuracy recovery; GF4 targets
  **physics-structured data** with no LLM accuracy data published.
- No head-to-head benchmark on the same model.

---

## 12. AetherFloat — Keita Morisaki (2026)

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

## 13. TinyTapeout / Open-Silicon Floating-Point Projects

### 13.1 `tt_um_float_synth` — NikLeberg

**Repo:** [github.com/NikLeberg/tt_um_float_synth](https://github.com/NikLeberg/tt_um_float_synth)  
**Shuttle:** IHP26A (TinyTapeout)

Synthesizes floating-point units (VHDL/Verilog) using open-source toolchains
(Yosys, GHDL, OpenROAD) on the IHP 130nm open PDK.

### 13.2 `Systolic_Array_with_DFT_v2` — Essenceia

**Repo:** [github.com/Essenceia/Systolic_Array_with_DFT_v2](https://github.com/Essenceia/Systolic_Array_with_DFT_v2)  
**Shuttle:** IHP26A (TinyTapeout)

2×2 bfloat16 matrix-multiplication accelerator with DFT (design-for-test)
infrastructure. Custom bfloat16: no subnormals, no NaN/∞, round-toward-zero
only.

**Relevance to Trinity:** These projects demonstrate that **custom FP formats
on open PDKs** are feasible and actively being taped out. Trinity's GF16
submission to TTSKY26a follows the same open-silicon methodology.

---

## 14. Custom FP for FPGAs (ECP5)

**Repo:** [Marc103/Floating-Point-Image-Processing-SV-RTL](https://github.com/Marc103/Floating-Point-Image-Processing-SV-RTL)

Custom, area-efficient FP adder/multiplier/divider in SystemVerilog for
FPGA deployment (ECP5). Allows custom exponent/fraction widths and
simplifies IEEE-754 features (no subnormals, simplified rounding) — similar
philosophy to DLFloat/GF16.

---

## 15. GoldenFloat Paper (t27 Project, NeurIPS 2026 OPT target)

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

**Note:** The NeurIPS paper draft (t27 repo) does **not** cite DLFloat16.
This documentation gap was **closed in the `zig-golden-float` whitepaper v1.1**
(commit `965b5a3`, April 2026), which explicitly states:
"GF16 = IBM DLFloat (1/6/9 format, Agrawal 2019). Format is NOT novel.
Our novelty: integer-backed u16 implementation + FPGA characterization."
The NeurIPS camera-ready version should carry the same citation.

---

## 16. zig-golden-float — Zig Reference Implementation (2026)

**Repo:** [github.com/gHashTag/zig-golden-float](https://github.com/gHashTag/zig-golden-float)  
**Authors:** Dmitrii Vasilev (gHashTag)  
**Status:** Active development; BENCH-001–006 completed

**What it is:**
A clean-room **Zig** implementation of the GoldenFloat family (GF4–GF32) using
integer-backed storage (`u16` / `u32`) to avoid native `f16` compiler bugs.
The decoder expands to `f32` only at the final computation step.

**Key benchmarks (BENCH-001–006):**

| Bench | Claim | Result | Status |
|-------|-------|--------|--------|
| BENCH-001 | MNIST MLP accuracy gap vs f32 = 0% | **97.67%** (f32 = 97.67%, gap 0.00%) | PASS |
| BENCH-002 | BF16 catastrophic failure on same MLP | **9.80%** accuracy (BF16 baseline) | Confirmed |
| BENCH-003 | FPGA LUT overhead vs ternary MAC | **1.37×** at MAC level; 47–59× at unit level | Documented |
| BENCH-004 | Compiler stability (no f16 native bugs) | Zero LLVM/Zig f16 crashes across 62+ known cases | PASS |
| BENCH-005 | Energy projection vs FP32 inference | **~10×** savings (projected, not measured) | Design target |
| BENCH-006 | Cross-language bindings (Rust/C++) | Zig `export` + C ABI verified | PASS |

**Honest gap:**
- The MNIST result is on a **toy network** (784-128-10 MLP). No ResNet-50 or
  LLaMA accuracy data yet.
- BENCH-005 energy numbers are **projected from synthesis reports**, not
  wall-power measurements.
- The repo does **not** include TinyTapeout RTL; it is a software reference
  for algorithmic validation only.

**Relevance to GF16:**
`zig-golden-float` provides an **independent software replication** of the
GF16/GoldenFloat encoding/decoding logic. The BENCH-001 zero-gap result
supports the claim that φ-anchored quantization does not degrade accuracy
on φ-structured data, but it does not prove hardware correctness.

---

## 17. HiFloat4 (HiF4) — Huawei (arXiv 2026)

**Paper:** "HiFloat4: A 4-bit Block Floating-Point Format for Efficient LLM
Inference"  
**Authors:** Huawei Noah's Ark Lab  
**Venue:** arXiv:2602.11287 (February 2026)  
**Link:** [arXiv:2602.11287](https://arxiv.org/abs/2602.11287)

**Key claim:**
- **4-bit BFP** with a three-level scaling hierarchy: E6M2 global scale +
  micro-exponents per 64-element group.
- Outperforms NVIDIA NVFP4 on accuracy with lower incremental hardware area
  for matrix multiplication.

**Relevance to GF16:**
HiF4 and GF4 occupy the same 4-bit niche. Both reject vanilla IEEE-754 in
favor of a domain-specific layout. HiF4 uses block-scaling; GF4 uses
φ-structured mantissa.

**Honest gap:**
- HiF4 is **block-scale-dependent** (needs per-block AMAX extraction); GF4 is
  **static** (single bias=31).
- HiF4 has a **Huawei Ascend/NVIDIA silicon roadmap**; GF4 has only a
  **TinyTapeout open-PDK submission**. The industrial traction gap is large.
- No head-to-head accuracy or compression benchmark.

---

## 18. Harmonia — Algorithm-Hardware Co-Design (arXiv 2026)

**Paper:** "Harmonia: Algorithm-Hardware Co-Design for Memory- and
Compute-Efficient BFP-based LLM Inference"  
**Authors:** Academic team (target venue not specified)  
**Venue:** arXiv:2602.04595 (February 2026)  
**Link:** [arXiv:2602.04595](https://arxiv.org/abs/2602.04595)

**Key claim:**
- All-layer BFP inference for LLMs, converting both linear and attention layers.
- Mixed precision: 8-bit mantissa for activations, 4-bit for KV-cache.
- **5.05× area efficiency** and **3.90× energy efficiency** vs. baseline on
  TSMC 28nm test chip.

**Relevance to GF16:**
Harmonia demonstrates that **non-uniform precision across layers** is viable
in silicon. GF16's φ-structured allocation is a different flavor of the same
principle: not all bits need the same precision everywhere.

**Honest gap:**
- Harmonia is **BFP** (shared exponent per block); GF16 is **per-element FP**.
- The 28nm test chip validates the BFP approach but says nothing about
  φ-structured formats.

---

## 19. TinyTapeout IHP26A Ecosystem (2025–2026)

The **IHP26A** shuttle (IHP 130nm `sg13g2` open PDK) launched November 2025,
with chips expected **September 2026**. It carries a dense cluster of
custom floating-point and MAC experiments — a parallel open-silicon universe
to TTSKY26a/b.

| Project # | Title | Author | Format | Frequency |
|-----------|-------|--------|--------|-----------|
| **232** | 8-bit SEM Floating-Point Multiplier | Jordan Delos Reyes | SEM 1-4-3 | — |
| **370** | 8Bit Posit MAC Unit | Ripunjay Singh et al. | Posit8 | — |
| **489** | OCP MXFP8 Streaming MAC Unit | Olivier Chatelain | MXFP8 | — |
| **497** | 2×2 Systolic Array with DFT and bfloat16 v2 | Julia Desmazes | bfloat16 subset | 100 MHz target |
| **528** | float_synth | Niklaus Leuenberger | float8 | 550 MHz |
| **714** | SEQ_MAC_INF_16H3 — NN Inference Accelerator | Neuromurf | Mixed | — |

**Relevance to Trinity:**
The IHP26A cluster proves that **custom numeric formats on open PDKs** are
now a crowded field. Trinity's differentiation is not "custom FP on open
silicon" (many do this), but the **φ-semantic overlay + formal theorems +
reset-time anchor** combination.

**Honest gap:**
IHP26A uses a **different foundry** (IHP 130nm) and **different shuttle
infrastructure** than TTSKY26a/b (SkyWater 130nm via TinyTapeout). The two
tapeout streams are independent; IHP26A success does not imply TTSKY26a/b
success.

---

## 20. Summary: Where Trinity Fits

| Project | Base | Layout | φ-aware? | Silicon? | Format type |
|---------|------|--------|----------|----------|-------------|
| **DLFloat16** | IBM | 1-6-9 bias 31 | No | Yes (VLSI 2018) | Custom FP16 |
| **Golden Quantizer** | Linköping | Fibonacci bins | **Yes** | No | Scalar quantizer |
| **GF16 / GoldenFloat** | Trinity | 1-6-9 bias 31 | **Yes** | Submitted (TTSKY26a/b) | Custom FP16 |
| **zig-golden-float** | Trinity | 1-6-9 bias 31 (Zig ref) | **Yes** | Software only | Reference impl |
| **AetherFloat** | Morisaki | Quad-radix base-4 | No | Yes (130nm chip) | Custom FP |
| **HiFloat4** | Huawei | 4-bit BFP E6M2+micro | No | Yes (Ascend/NVIDIA) | Block FP4 |
| **Harmonia** | Academic | Mixed BFP (8/4-bit) | No | Yes (28nm test chip) | Block FP |
| **FlexiBit** | UC Irvine | Arbitrary | No | FPGA/ASIC | Flexible FP/INT |
| **F-BFQ** | Glasgow | BFP | No | FPGA (KV260) | Block FP |
| **DB-Attn** | SEU/Houmo | BFP | No | FPGA/ASIC | Block FP |
| **BBAL** | SEU/Houmo | BBFP | No | ASIC | Block FP |
| **ZipNN** | IBM | BF16 + exponent codec | No | Software | Lossless codec |
| **DFloat11** | Rice | Huffman exponents | No | Software | Dynamic FP |
| **ECF8** | Rice | Alpha-stable FP8 | No | Software | Data-tuned FP8 |
| **M2XFP** | SJTU/Huawei | Metadata-augmented FP4 | No | Yes (ASPLOS 2026) | Research format |
| **PVU** | SWUST | Posit vector (RISC-V) | No | FPGA | Vector CPU |
| **SPADE** | IIT Indore | Posit SIMD MAC | No | Yes (TSMC 28nm) | Custom FP |
| **B-Posit** | BITS/ASU | Bounded-regime Posit | No | Yes (FreePDK45) | Custom FP |
| **EULER-ADAS** | IIT Indore | Approx B-Posit | No | Yes (TSMC 28nm) | Approximate FP |
| **Dynamic LNS** | PNNL | Log-domain + outlier-aware | No | FPGA (Alveo U280) | LNS |
| **MXFP4/6/8** | OCP | Micro-block scaled | No | Yes (multiple vendors) | Industry standard |
| **tt_um_float_synth** | Community | Custom | No | IHP26A submitted | Open-silicon FP |
| **Systolic_Array** | Community | bfloat16 subset | No | IHP26A submitted | Open-silicon FP |

**Trinity's unique claim:** The only project that combines (a) a proven
16-bit FP layout (DLFloat16) with (b) **three formal theorems** linking the
bit split to the golden ratio, (c) a **published φ-quantization predecessor**
(Golden Quantizer 2017), (d) a **hardware-silicon binding**
(0x47C0 reset witness, Three Crowns milestones), and (e) an **independent
software reference implementation** (`zig-golden-float`) with reproducible
benchmarks (BENCH-001–006).

Whether the φ-structured quantization theory provides measurable compression
or accuracy advantages beyond the base DLFloat16 layout is an **open
empirical question** — tracked in `docs/hardware/bpb_benchmark.py` and
`gHashTag/zig-golden-float` BENCH-001–006.

---

## 20. References

- `docs/hardware/gf16_spec.md` — Format specification with DLFloat16 relation
- `docs/hardware/gf16_mathematics.md` — φ-step and optimal field derivations
- `docs/hardware/silicon_anchor.md` — TTSKY26a/b submission status
- `docs/HARDWARE_ATTESTATION.md` — Honest proof inventory
- `gHashTag/zig-golden-float` — Zig reference implementation with BENCH-001–006
- arXiv:2503.01313 — PVU (Posit Vector Unit, RISC-V)
- arXiv:2601.17279 — SPADE (SIMD Posit MAC)
- arXiv:2603.01615 — B-Posit (bounded-regime Posit)
- arXiv:2605.06875 — EULER-ADAS (approximate B-Posit engine)
- PNNL MICRO 2024 — Dynamic LNS for LLMs
- arXiv:2601.19213 — M2XFP (SJTU/Huawei, ASPLOS 2026)
- arXiv:2602.11287 — HiFloat4 (Huawei)
- arXiv:2602.04595 — Harmonia (algorithm-hardware co-design)
- [TinyTapeout IHP26A chip list](https://tinytapeout.com/chips/ttihp26a/) — Open-silicon FP ecosystem
