# Trinity S3AI — Claude Code Context

## Project

Trinity S³AI is an active boundary-mapping research program investigating whether geometric invariants of the H4 Coxeter group (and related structures such as the 600-cell and Clifford algebra Cl(8)) can encode or constrain the parameters of the Standard Model of particle physics.

**Repository:** https://github.com/gHashTag/trinity-s3ai  
**Second brain (RAG):** `trios-mcp-rag` MCP server — https://github.com/gHashTag/trios-mcp-rag  
**Live game:** https://t27.ai/trinity-s3ai/

**Most important rule:** A numeric coincidence is not a derivation.

---

## Conventions

### Honesty Tags (mandatory for every multi-atom `phi/π/e` formula)
- `[phenomenological_fit]` — numerical coincidence with SM parameter
- `[NUMERICAL_FIT]` — explicit numerical fit (legacy tag)
- `[PHYSICAL_AXIOM]` — physically motivated assumption
- `[MATH_TODO]` — mathematical gap, needs proof
- `[LIBRARY_GAP]` — blocked by missing Coq library
- `[OPEN_PROBLEM]` — honestly open problem

### Claim Statuses (canonical vocabulary)
- `verified` — Coq `Qed.` or equivalent formal proof
- `empirical_fit` — numerical coincidence, tagged in source
- `open_conjecture` — honestly open, not yet proved or refuted
- `high_risk_or_falsified` — refuted by data or proof
- `unverified` / `retracted` — not yet assessed or withdrawn

### Boundary Theorems (BT-1..BT-4)
These are `verified` impossibility results. They prove that *certain direct constructions* from H4 geometry do not reproduce the SM. They are **guideposts**, not tombstones.

---

## Commands

### Validation (run before any PR)
```bash
python3 scripts/anti_numerology_gate.py
python3 scripts/count_admitted_honest.py
python3 scripts/validators/validate_v4.py
python3 scripts/generate_claims.py --check
bash scripts/check_english_only.sh
```

### Coq Build
```bash
cd proofs/trinity && coq_makefile -f _CoqProject -o Makefile.coq && make -f Makefile.coq -j$(nproc)
```

### Rust Tests
```bash
cd games/trinity_fold && cargo test --workspace
cd trinity_rust && cargo test
```

### RAG / Second Brain
```bash
# MCP server is auto-started by Claude Code via ~/.claude/mcp.json
# Use /mcp to see available servers (trios-mcp-rag, trinity-postgres)
```

---

## File Structure

| Directory | What it holds |
|-----------|---------------|
| `proofs/trinity/` | 50 Coq files, 1045+ `Qed`, 0 real `Admitted` (Wave 17) |
| `proofs/clifford_cl8/` | Track B: Cl(8) formalization (4 honest `Admitted` with citations) |
| `proofs/catalog/` | Standalone reference catalog |
| `docs/claims.yaml` | **SSOT** — machine-readable claim ledger |
| `scripts/` | Validators, gates, and generators (CI-critical) |
| `games/trinity_fold/` | GOLDEN BRIDGE puzzle (Rust + wasm, 5-ring workspace) |
| `trinity_rust/` | Rust formula catalog and numeric checks |
| `paper/` | LaTeX sources and Markdown paper drafts |
| `derivations/` | Per-topic derivation notes across 54 subdirectories |

---

## Rules / Gotchas

1. **Never promote `empirical_fit` to `verified`** without a *physical* derivation (not just an interval bound).
2. **`Admitted.` without a tag is indistinguishable from a deliberate hole** — always add an approved honesty tag.
3. **Boundary theorems BT-1–BT-4 are `verified` impossibility results**, not dead ends.
4. **`HONESTY_MANIFEST.md` is ground truth** — if another document contradicts it, the manifest wins.
5. **No ToE claims, no prize claims — ever.**
6. **Public docs are English-only.** No new Cyrillic without `LEGACY:` header.
7. **Edit `docs/claims.yaml` first**, then run `python3 scripts/generate_claims.py` to regenerate derived artifacts (README table, game cards).
8. **CI runs all validators with `--check`** and fails if anything is stale.

---

## MCP & Second Brain

Two MCP servers are configured in `~/.claude/mcp.json`:

### `trios-mcp-rag` (dedicated RAG server)
- **Binary:** `/Users/playra/trios-mcp-rag/target/release/trios-mcp-rag`
- **Database:** Railway PostgreSQL `ssot_brochure.chapters` (80 chapters)
- **Tools:** `search_chapters`, `get_chapter`, `list_chapters`, `forbidden_audit`, `build_cover`, `build_pdf`, `build_book`, `get_claim_status`, `list_claims`, `get_honest_counters`, `preview_chapter_update`, `backup_ssot`
- **Rules:** Read-only by default; writes require `confirm=true` or `dry_run=false` + explicit confirmation

### `trinity-postgres` (generic SQL access)
- **Package:** `@modelcontextprotocol/server-postgres`
- **Database:** Full Railway PostgreSQL instance (all schemas: `ssot`, `ssot_brochure`, `public`)
- **Use for:** Raw SQL queries, `brain_status` audit, BPB benchmarks, scarab fleet data

**Environment variable:** `DATABASE_URL` is set in `~/.zshenv` and points to the Railway PostgreSQL instance.

**To activate:** Restart Claude Code or run `/mcp` to see registered servers.
