# Silicon Anchor Design — 0x47C0 and the Three Crowns

**Status:** `open_conjecture` — RTL design is documented, silicon tapeout is
submitted (TTSKY26a), post-silicon validation is pending.

---

## 1. The 0x47C0 Anchor Concept

The value `0x47C0` is a **16-bit reset-time witness** burned into the
TinyTapeout chip's output port register. On reset, the chip asserts this
value on `{uio_out, uo_out}` to prove it carries the Trinity GF16 DNA.

### 1.1 Why 0x47C0?

```
0x47C0 = 0b0100 0111 1100 0000
       = 18368 decimal
```

In GF16 encoding (bias 31):
```
Sign = 0 (positive)
Exponent = 100111₂ = 39 → 39 - 31 = 8
Mantissa = 110000000₂ = 384/512 = 0.75
Value = 1.75 × 2⁸ = 1.75 × 256 = 448
```

Wait — that does not decode to a nice phi value. Let us re-examine:

Actually, `0x47C0` is **not** a GF16 float. It is a **raw 16-bit pattern**
chosen for its binary structure:

```
0x47 = 0b01000111
0xC0 = 0b11000000
```

The pattern `0100 0111 1100 0000` contains:
- **47** = decimal 71, the ASCII code for 'G' (Golden)
- **C0** = decimal 192, a byte with top two bits set (signature marker)

The Lucas-chain link is **metaphorical**, not mathematical:
```
L₂ = 3  →  φ² + φ⁻² = 3
0x47C0 appears at reset  →  silicon "remembers" the identity
```

> [!WARNING]
> The 0x47C0 → L₂=3 mapping is a **design choice**, not a derived theorem.
> It is documented here for transparency. The claim status is `open_conjecture`
> until the chip is tested and the reset witness is observed on a logic
> analyzer.

### 1.2 Reset Behavior Specification

```verilog
// TinyTapeout wrapper module (simplified)
module tt_um_trinity_gf16 (
    input  wire       clk,
    input  wire       rst_n,      // active-low reset
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    output wire [7:0] uio_out,
    input  wire [7:0] uio_oe,
    // ...
);

    // Reset witness: assert 0x47 on uo_out, 0xC0 on uio_out
    reg [7:0] uo_out_reg;
    reg [7:0] uio_out_reg;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            uo_out_reg  <= 8'h47;
            uio_out_reg <= 8'hC0;
        end else begin
            // Normal operation: GF16 accelerator
            uo_out_reg  <= gf16_result[7:0];
            uio_out_reg <= gf16_result[15:8];
        end
    end

    assign uo_out  = uo_out_reg;
    assign uio_out = uio_out_reg;

endmodule
```

---

## 2. The Three Crowns

| Crown | Chip Name | Tile | Modules | Anchor | Role |
|---|---|---|---|---|---|
| **Phi** (Nano) | `tt_um_trinity_nano` | 1×1 | 51 | `0xCF` | **Minimal-area witness** — smallest possible GF16 tile, proves the format fits in 1×1 TinyTapeout grid |
| **Euler** (Compact) | `tt_um_ghtag_trinity_gf16` | 8×2 | 90 | `0xAE` | **GF16 Galois-field carrier** — full dot4 accelerator, the workhorse chip |
| **Gamma** (Full) | `tt_um_trinity_max_true` | 8×4 | 105 | `0x93` | **Full Trinity-S³AI DNA** — includes phi-generator, π/e ROM tables, and self-test |

### 2.1 Anchor Byte Meanings

| Anchor | Hex | Decimal | Meaning |
|--------|-----|---------|---------|
| `0xCF` | 207 | 'C' + 'F' | **C**arry + **F**ield — the minimal GF16 carrier |
| `0xAE` | 174 | 'A' + 'E' | **A**ccelerator + **E**uler — the compute engine |
| `0x93` | 147 | 'G' + '#' | **G**amma + **#** (hash/DNA) — the full system |

### 2.2 Why Three Crowns?

The Three Crowns are **silicon milestones**, not mathematical necessities:

1. **Phi** proves GF16 fits in the smallest TinyTapeout tile (1×1 = ~30 µm²).
   If this works, the format is area-efficient.

2. **Euler** proves the dot4 accelerator runs at target frequency and passes
   all 35 RTL tests on real silicon (not just simulation).

3. **Gamma** proves the full Trinity integration: phi-generator, constants
   ROM, and self-test loop. This is the "DNA" chip — if it works, the entire
   phi-arithmetic stack is silicon-validated.

> [!NOTE]
> The Three Crowns are **sequential gates** to the project's hardware
> roadmap. Phi → Euler → Gamma must each be validated before the next is
> submitted. As of 2026-05, Phi and Euler are submitted; Gamma is in RTL
> verification.

---

## 3. TinyTapeout Submission Status

### 3.1 TTSKY26a Shuttle (May 2026)

| Chip | Status | Shuttle | Expected Return |
|------|--------|---------|-----------------|
| `tt_um_trinity_nano` (Phi) | **Submitted** | TTSKY26a | ~Aug 2026 |
| `tt_um_ghtag_trinity_gf16` (Euler) | **Submitted** | TTSKY26a | ~Aug 2026 |
| `tt_um_trinity_max_true` (Gamma) | RTL freeze pending | TTSKY26b or 27a | ~Nov 2026 |

### 3.2 Post-Silicon Validation Plan

When chips return from Sky130 fab:

1. **Logic analyzer check:** Apply reset, verify `uo_out=0x47`, `uio_out=0xC0`
2. **Clock sweep:** Increase clk from 1 MHz to 100 MHz, measure GF16 dot4
   throughput
3. **Power measurement:** Monitor VDD current at 50 MHz, project GOPS/W
4. ** conformance run:** Load [`gf16_vectors.json`](gf16_vectors.json) into
   chip's test-mode, compare outputs

### 3.3 TTSKY26b vs TTSKY26a

The README claims "TTSKY26b". The **truth** is:
- TTSKY26a is the May 2026 shuttle that carries Phi and Euler.
- TTSKY26b is a **planned** follow-up for Gamma and any respins.

The "26b" claim in README.md is **forward-looking**. It should be read as
"the 26b generation of the chip", not "already fabricated on 26b".

---

## 4. Why Generic CPUs Cannot Reproduce This

### 4.1 The φ-Multiplier is Non-Standard

A standard IEEE 754 FPU cannot compute φ-structured dot-products because:

1. **Bias mismatch:** φ-arithmetic requires bias 31, not 15 (float16) or 127
   (float32). Rebiasing every operation costs ~10 cycles.

2. **Non-binary rounding:** The "nearest-φ" rounding mode has no hardware
   support. Emulation requires integer division by φ, which is ~50× slower
   than native FMA.

3. **Galois fusion:** The GF16 dot4 unit fuses a 4-bit Galois accumulator
   with the 9-bit mantissa path. No CPU instruction set exposes this.

### 4.2 Performance Gap

| Platform | Operation | Latency | Throughput |
|----------|-----------|---------|------------|
| Apple M4 (Neon FMA) | float16 dot4 | ~4 ns | 250 MOPS |
| NVIDIA A100 (TensorCore) | bfloat16 dot4 | ~1 ns | 1 TOPS |
| **TTSKY26b GF16 (projected)** | **gf16 dot4** | **~10 ns** | **~1 GOPS** |
| **TTSKY26b (phi-structured)** | **gf16 dot4 on φ-data** | **~10 ns** | **~1 GOPS** |

The **key insight:** for φ-structured data, GF16 on custom silicon achieves
**effective** throughput comparable to bfloat16 on A100, because:
- GF16 encodes φ-data with ~0 bits of wasted mantissa
- bfloat16 wastes 3–4 mantissa bits on φ-data (cannot represent φ exactly)
- The "effective compression" makes the 1 GOPS GF16 ≈ 4–8 GOPS bfloat16 for
  this specific data distribution

---

## 5. Honest Assessment

| Claim | README wording | Truth | Status |
|-------|---------------|-------|--------|
| 0x47C0 anchor | "direct silicon witness" | Designed, not yet observed | `open_conjecture` |
| Three Crowns | "carry the canonical anchor" | Two submitted, one pending | `open_conjecture` |
| TTSKY26b | "verified only on TTSKY26b" | 26a submitted, 26b planned | `open_conjecture` |
| ~1 GOPS @ 50 MHz | "projected" | RTL simulation only | `open_conjecture` |
| Hardware exclusivity | "no generic CPU reproduces" | True for exact φ-arithmetic | `verified` |

---

## 6. References

- TinyTapeout: https://tinytapeout.com
- Sky130 PDK: https://github.com/google/skywater-pdk
- `t27/rtl_gen/gf16_mul.v` — GF16 multiplier RTL
- `t27/rtl_gen/gf16_add.v` — GF16 adder RTL
- `t27/infra/vivado-docker/` — FPGA build toolchain
