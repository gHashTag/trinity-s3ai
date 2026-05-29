---
name: claim-ledger
description: Edit the Trinity S3AI claim ledger — SSOT rules, YAML editing, and regeneration workflow
trigger:
  paths:
    - "docs/claims.yaml"
    - "README.md"
    - "games/trinity_fold/fixtures/generated_claim_cards.json"
---

# Claim Ledger Workflow

## SSOT Rule

`docs/claims.yaml` is the **Single Source of Truth** for all claim status information.

**Never** edit these derived artifacts by hand:
- `README.md` claim table (between `<!-- CLAIMS_TABLE:START -->` and `<!-- CLAIMS_TABLE:END -->`)
- `games/trinity_fold/fixtures/generated_claim_cards.json`

## Editing Claims

1. **Edit `docs/claims.yaml`** — add, remove, or update claim entries.
2. **Run generator** — `python3 scripts/generate_claims.py`
3. **Commit both** — the YAML and all regenerated artifacts.
4. **CI verification** — the script runs with `--check` in CI and fails if stale.

## Claim Entry Structure

Each claim in the YAML must include:
- `id` — unique identifier
- `title` — human-readable description
- `layer` — `L0` through `L7` (infrastructure → publication)
- `status` — `verified` | `empirical_fit` | `open_conjecture` | `high_risk_or_falsified` | `unverified`
- `evidence` — file paths or URLs
- `blocking_gap` — what prevents promotion (empty if none)

## Status Promotion Rules

| From | To | Allowed? | Condition |
|------|-----|----------|-----------|
| `unverified` | `verified` | Only if Coq `Qed.` or equivalent proof exists |
| `unverified` | `empirical_fit` | If numeric match with honesty tag |
| `empirical_fit` | `verified` | **Only** with physical derivation, not interval bound |
| `open_conjecture` | `verified` | Only if proof is closed |
| any | `high_risk_or_falsified` | If refuted by data or formal proof |

## Layer Definitions

| Layer | Scope |
|-------|-------|
| L0 | Infrastructure (CI, build, deploy) |
| L1 | Claim ledger, epistemology |
| L2 | Formal proofs (Coq) |
| L3 | Geometry (H4 root system, 600-cell) |
| L4 | NCG / Lagrangian / spectral action |
| L5 | Numerical fits and phenomenology |
| L6 | GOLDEN CHAIN game |
| L7 | Publication (paper, talks, Zenodo) |

## Commands

```bash
# Regenerate all derived artifacts
python3 scripts/generate_claims.py

# Check consistency without writing
python3 scripts/generate_claims.py --check

# Validate the YAML schema
python3 scripts/validators/validate_v4.py
```
