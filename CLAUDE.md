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
| `games/trinity_fold/` | GOLDEN CHAIN puzzle (Rust + wasm, 5-ring workspace) |
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

## Safe Self-Improvement Protocol

The agent (Claude Code with custom skills/hooks) can self-improve, but **only inside a sandbox**.
This prevents the "agent breaks itself and I have to rollback manually" problem.

### Architecture (AgentGit + SICA + EvoGit + Gödel Agent)

```
agent-stable  (protected)  ← merge only from agent-dev + CI pass
      ↑
agent-dev     (testing)    ← merge feature- branches + harness pass
      ↑
agent-exp/NNN (sandbox)    ← agent edits itself here
```

### Branches

| Branch | Purpose | Direct edits? |
|--------|---------|-------------|
| `main` | Physics project trunk | Yes (physics work) |
| `agent-stable` | Release version of agent config | **No** — only fast-forward from agent-dev |
| `agent-dev` | Integration branch for agent improvements | **No** — only merge from agent-exp/* |
| `agent-exp/NNN` | Sandbox for one self-improvement task | **Yes** — agent edits only here |

### Commands

```bash
# 1. Start a self-improvement task in sandbox
python3 scripts/agent_overseer.py start-task "Improve second-brain skill"
#    → creates agent-exp/001 + worktree at ../trinity-s3ai-exp-001

# 2. Work in the sandbox (Claude Code runs there)
cd ../trinity-s3ai-exp-001
claude --project ../trinity-s3ai-exp-001

# 3. Evaluate when done
python3 scripts/agent_overseer.py evaluate --branch agent-exp/001
#    → runs harness + scope gate

# 4. Promote or abort
python3 scripts/agent_overseer.py promote --branch agent-exp/001   # merge into agent-dev
python3 scripts/agent_overseer.py abort --branch agent-exp/001     # delete sandbox
```

### Scope Gate (Gödel Agent pattern)

Allowed to edit in sandbox:
- `.claude/skills/*`
- `.claude/scheduled_tasks.json`
- `scripts/agent_overseer.py`, `scripts/agent_test_harness.py`

**Forbidden** (overseer auto-rejects if touched):
- `CLAUDE.md`
- `docs/claims.yaml`
- `proofs/`
- `.github/workflows/`
- `scripts/validators/`, `scripts/anti_numerology_gate.py`, `scripts/generate_claims.py`

### Rules for the agent

1. If asked to self-improve, **always use `python3 scripts/agent_overseer.py start-task`**.
2. Never edit `.claude/skills/` directly on `main`, `agent-stable`, or `agent-dev`.
3. Commit after every significant agent step: `git commit -m "agent-step: ..."`.
4. Maximum 15 agent commits per sandbox task.

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

## Own language first

When this project publishes something about itself, it publishes in **this
project's own language and format** -- not translated into somebody else's.

Owner's rule, 2026-09-20: stop writing in other people's languages, we have our
own.

This bites on any file whose only reason to exist is that an outside tool
expects that shape: `llms.txt`, `agents.json`, `ai.txt`, `.well-known/*.json`,
A2A agent cards, `ai-plugin` manifests, OpenAPI stubs, JSON-LD blocks, a README
that restates a spec. The reflex is to write four of them in four foreign
formats, and the reflex is wrong: a project whose claim is "here is a language
worth writing" and which then describes itself in three of other people's
formats has published three documents that are not true of it.

**The move:** find the address the outside world already fetches, then serve our
own language at it. `/llms.txt` at t27.ai **is** a t27 module -- `llms.txt`
requires nothing but text, and every prose line of a `.t27` file is a `;`
comment, so it stays readable to anything that cannot compile it.

**Three qualifications, so the rule stays honest:**

- A format a resolver genuinely parses -- a sitemap, `package.json`, a lockfile
  -- is machinery, not a description. **Generate** it from our own source; never
  hand-write it into a second home for the truth.
- Code against someone else's API uses their types. Prose for a human who has
  never heard of the project uses that human's language.
- If a format demands a claim we cannot back, **publish nothing**. An A2A card
  with no A2A server behind it is a false claim, and a missing file is more
  honest than a lying one.

The test: *is this file the project speaking about itself?* If yes, it speaks
our language. If it is plumbing, it speaks the plumbing's.

**Worked example, compiler-checked rather than asserted:** in `gHashTag/trinity`,
`apps/website/public/t27/files/specs/catalog/onboarding.t27` generates
`/llms.txt` and `/agents.t27` byte-identically, gated in CI as
`check:onboarding`. The generator evaluates the spec's own `test` blocks --
`typecheck.ok` stays true for `assert 1 > 2`, so a compiler saying "this parses"
is not a compiler saying "this is true" -- and re-compiles the rendered document
before writing it.

**The full rule lives in exactly one place: the `own-language-first` skill**
(`~/.claude/skills/own-language-first/SKILL.md`). It carries the consent gate for
documents addressed to other people's agents, the six negative controls, and the
`;`-alone-on-a-line trap that silently discards a `module` declaration. This
section is a pointer, not a copy -- the recorded defect in this codebase family
is the hand-copied rule that only two of its three homes knew about.
