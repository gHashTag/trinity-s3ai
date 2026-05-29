# Vasilev–Pellis–Olsen short paper — reproducibility capsule

**Title.** *A Constrained Symbolic Search for φ-Structured Physical
Constants: A Report, an Independent Numerical Audit, and a Roadmap for the
Vasilev–Pellis–Olsen Programme.*

This directory is the source + reproducibility capsule for the short paper.
It is a **companion long-form report** to the GOLDEN CHAIN / TRIOS S³AI
compendium. Every empirical statement in the PDF carries an explicit
**claim-status label** (Verified / Empirical fit / Open conjecture /
High-risk / Retracted), and every open conjecture carries a written
falsification path. No physical derivation of the constants is claimed.

## Provenance note (read this first)

The LaTeX source `pellis_vasilev_letter.tex` in this capsule was
**reconstructed from the verified text of the previously-audited PDF**, not
recovered from an original `.tex` (the original source file was lost). The
reconstruction transcribes the audited PDF verbatim; **no data was
fabricated**. Every numerical deviation in the tables was re-verified
independently at 50-digit precision with `audit.py` before the build was
labelled clean. See the critical-honesty notes below.

## Files

| File | Description |
| --- | --- |
| `pellis_vasilev_letter.tex` | LaTeX source (claim-status macros, Tables 1–4, 13-entry bibliography). |
| `make_figure.py` | matplotlib script regenerating Figure 1 (conjectured phase transition). |
| `phase_transition.pdf` / `.png` | Figure 1 (embedded in the paper). |
| `audit.py` | Independent 50-digit `mpmath` audit of every printed deviation. |
| `apply_metadata.py` | Re-applies PDF metadata (Title + Author) after each tectonic compile. |
| `pellis_vasilev_letter.pdf` | Compiled output, 18 pages. |

## Build (tectonic only)

The pipeline is **tectonic only** — never a Python/ReportLab/wkhtmltopdf
path. After compiling, metadata must be re-applied (tectonic wipes it).

```bash
python3 make_figure.py                       # regenerate Figure 1
tectonic pellis_vasilev_letter.tex --keep-logs
python3 apply_metadata.py                     # Title + Author=Perplexity Computer
```

## Audit

```bash
python3 audit.py        # requires: pip install mpmath
```

Audited values (mpmath, dps=50), all reproduced:

- α⁻¹ Pellis anchor `360φ⁻² − 2φ⁻³ + (3φ)⁻⁵` = 137.035999165, rel. dev.
  **8.93×10⁻¹¹** vs CODATA 137.035999177.
- α⁻¹ compact fit `36 π⁻¹ φ e²` = 137.0027, rel. dev. **2.43×10⁻⁴**.
- α_s(m_Z) ≈ α_φ = ½φ⁻³ = 0.118034, rel. dev. **2.88×10⁻⁴**.
- μ leading term `φ¹⁶/√5` = 987.0002 (schematic only; `F₈·L₈ = 21·47 = 987`).
- δ_CP formula `8π³/(9e²)` = 3.730 rad / 213.7°, **off ~8.4%** vs the
  measured ~3.44 rad (197°, PDG 2024).

## Changelog — adversarial-hardening wave (May 2026)

This wave hardened the manuscript against referee attack without changing
any audited number (all figures still reproduce at `dps=50`). Edits:

- **A1.** Tightened the epistemic-status convention: `Verified` is now
  defined in exactly three senses, and sense (iii) — *faithful
  transcription* of the unpublished GOLDEN CHAIN compendium — explicitly
  caps the underlying scientific claim at `Open conjecture` (Track-1 rule).
- **A2.** Added the exact combinatorial derivation of the hypothesis-class
  cardinality `|S(C)| = Σⱼ 2ʲ C(4,j) C(C,j)` (leading `(2C)⁴/4! = ⅔C⁴`),
  and a `High-risk` note that the prefactor `n` is *unbounded above*, so
  the true class size is `|S(C)| × N_max` (catalogue reaches n = 8715) —
  multiplying, not dividing, the look-elsewhere burden.
- **A3.** Flagged the "15 of 128,400" look-elsewhere count as a **lower
  bound** (one target, one tolerance, C≤4, n≤400); the real exposure over
  all ~42 targets × forms × higher C is larger by orders of magnitude.
- **A4.** Reframed the Strand-I/III correspondence from "genuine
  unification" to an **algebraic re-grouping** (a faithful change of basis,
  not a derivation, no information-theoretic gain).
- **A5.** Strengthened the silicon `0x47C0`/TTSKY26b provenance disclaimer
  (private, single-source, **not falsifiable as stated**, used nowhere);
  clarified that the Coldea et al. `E₈` result is one specific 1D Ising
  chain (CoNb₂O₆), **not** a general appearance of φ "in nature."
- **A6.** Added a `High-risk`/`Open conjecture` note that the Bayes factor
  is an **empty functional without a published prior**, with a
  falsification path requiring a pre-registered description-length prior.
- **A7.** Added a new **"Threats to validity"** section aggregating every
  known failure (negative single-constant MDL, look-elsewhere, generator
  choice, retracted circular δ_CP, retracted fabricated μ form, eight
  flagged rows, empty Bayes factor, non-falsifiable provenance, no
  external peer review, code-relative MDL).
- `audit.py` extended: cardinality is now checked by **brute-force
  enumeration** against the closed form (129/321/8361 all match), plus a
  structural MDL sub-cost check. The toy ΔMDL reconstruction was removed
  because it gave the wrong sign and would contradict the paper's encoder;
  the frozen −2.3/−5.4/−5.8-bit figures are reported as referee-recompute
  targets.
- Claim-status counts after this wave: Verified 15, Empirical fit 1,
  Open conjecture 19, High-risk 21, Retracted 4, Falsification-path 14.

## Critical-honesty notes (not hidden)

1. **A small deviation is not evidence of structure.** With `|S(C)| ~ (2/3)C⁴`
   candidate expressions and a look-elsewhere effect (15 of 128,400 φ-forms
   land within 3×10⁻⁴ of α⁻¹), finding *some* φ-form near a target is
   expected. The audit confirms arithmetic only.
2. **δ_CP anti-circularity.** A table row once listed the target as
   `3.73 rad` — exactly the formula's own output, a circular self-match. The
   real measured PMNS phase is ~197° / 3.44 rad (PDG 2024); the formula is
   off ~8.4%. The claim `δ_CP = 3/φ²` is **retracted**.
3. **μ.** Only the schematic Fibonacci–Lucas form is reported. An earlier
   draft form `μ³² = φ⁻⁴² F₅¹⁶⁰ L₅⁴⁷ L₁₉^(40/19)` failed reproduction by
   ~56 orders of magnitude and is **never** re-promoted.
4. **MDL.** Under honest prefactor-charging, even the compact α⁻¹ fit yields
   a *negative* per-constant MDL gain — no single formula "compresses" α⁻¹.
   Only a possible aggregate effect over many constants could decide the
   programme, and that is flagged as the number a referee must recompute.
5. **Eight flagged rows** (Table 3) do not survive a 50-digit audit and are
   excluded from the paper's quantitative claims.

## Strand / author attribution

- **Vasilev** — Strands I & II: grammar 𝒢_φ, MDL framework, Catalog42
  protocol, Trinity anchor `φ² + φ⁻² = 3`, silicon anchor, the Bridge,
  falsification ledger.
- **Pellis** (University of Ioannina) — Strand III: closed-form α⁻¹ and μ,
  φ-additive formulas, the hierarchical expansion.
- **Olsen** (College of Central Florida, Emeritus) — Tier-D: cross-scale
  φ-cosmology, log-periodic falsification signal.

## Build environment (reproducible-build record)

- tectonic **0.16.9** (the operating-rules pin is 0.15.0; this is a version
  difference flagged per the TRIOS tectonic-pinning rule — a full QA run was
  re-executed, and output hashes recorded below).
- mpmath 1.4.1, pypdf 6.x, matplotlib, numpy.
- Output `sha256`:
  - `pellis_vasilev_letter.pdf` — `2a93bd20dadf998440857fcdec9d5ea3eaa5cb141442acdbecdc435c55e3c9c6`
  - `phase_transition.pdf` — `cbd2e23d42503e37d7bcf4e4b34b858b039b878c93e756ab2a8ef974789d441d`

  (The PDF hash is recorded pre-metadata; `apply_metadata.py` mutates the
  trailer afterward, so a post-metadata rebuild will differ in the metadata
  dictionary only.)

## Data availability

Target constants are drawn from PDG (S. Navas et al., Phys. Rev. D 110,
030001, 2024) and CODATA.

Contact: admin@t27.ai
