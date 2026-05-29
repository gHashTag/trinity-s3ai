---
name: golden-chain
description: GOLDEN CHAIN puzzle — hardware-verified proof chain, ClaimStatus rules, scoring, ring architecture, and how to modify the game
trigger:
  paths:
    - "games/trinity_fold/**/*.rs"
    - "games/trinity_fold/fixtures/*.json"
---

# GOLDEN CHAIN Game Reference

## What It Is

GOLDEN CHAIN is a **hardware-verified proof chain**, not evidence. It is implemented as a Rust + wasm 5-ring workspace:

```
ring0_core       → ClaimStatus enum, claim definitions
ring1_constraints → Validation rules, anti-numerology gates
ring2_search      → Search algorithms for tile placement
ring3_adapters    → Adapters to external data sources
ring4_canvas      → UI / rendering layer
app               → Web application entry point (wasm)
```

Every link in the chain is either a Coq `Qed.`, a silicon anchor (`0x47C0`), or a documented boundary theorem.

## ClaimStatus Enum

```rust
enum ClaimStatus {
    Verified,           // Coq Qed. or equivalent
    EmpiricalFit,       // Numerical coincidence with honesty tag
    OpenConjecture,     // Honestly open
    HighRiskOrFalsified,// Refuted
    Unverified,         // Not yet assessed
}
```

**Rule:** The enum must stay in sync with `docs/claims.yaml` status vocabulary. If you add a new status to the YAML, you must add it here and regenerate `fixtures/generated_claim_cards.json`.

## Scoring Rules

- **Verified claims** score highest but are rare (only BT-1..BT-4 and infrastructure claims).
- **Empirical fits** score lower and must carry an honesty tag.
- **Open conjectures** score zero but are tracked for progress.
- **High-risk / falsified** claims score negative (they break the chain).

## How to Add a New Tile / Claim

1. Add the claim to `docs/claims.yaml` with proper `id`, `layer`, `status`, `evidence`.
2. Run `python3 scripts/generate_claims.py` to regenerate `fixtures/generated_claim_cards.json`.
3. If the claim introduces a new status, update `ring0_core::ClaimStatus`.
4. Run `cd games/trinity_fold && cargo test --workspace`.
5. Deploy: the wasm build is served from GitHub Pages at https://t27.ai/trinity-s3ai/

## Anti-Numerology Gate in the Game

The game enforces the same regex patterns as `scripts/anti_numerology_gate.py`:
- Every `EmpiricalFit` claim must have an approved honesty tag.
- Formulas with `phi`, `π`, `e` without a tag are rejected.

## Live Deployment

- URL: https://t27.ai/trinity-s3ai/
- CI: `.github/workflows/pages.yml` builds and deploys on every push to `main`.
- The canvas is a wasm bundle compiled from `games/trinity_fold/app`.
