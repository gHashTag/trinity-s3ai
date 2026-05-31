# CI Coverage Gap — `proofs/lean/` (Wave 24+)

**Status:** OPEN | **Severity:** Medium | **Owner:** `.github/workflows/lean.yml`

## Finding

The new Lean 4 skeleton `proofs/lean/` (created in Wave 24+) is **not**
covered by the existing Lean CI workflow (`.github/workflows/lean.yml`).

Current CI only builds:
```yaml
cd derivations/lean_port/TrinityLean
lake build
```

The `proofs/lean/` workspace (with its own `lakefile.lean` requiring
mathlib `v4.13.0`) is never compiled in CI.

## Risk

- The `H4RootSystem.lean` file could bit-rot (break against future mathlib
  updates) without anyone noticing.
- Contributors might add `sorry`-tagged Lean code that does not even
  type-check.

## Fix (requires touching `.github/workflows/`)

Add a second `lake build` step to `.github/workflows/lean.yml`:

```yaml
      - name: Build proofs/lean
        run: |
          cd proofs/lean
          lake update -R
          lake exe cache get || true
          lake build
```

**Scope-gate note:** Per `CLAUDE.md` §Safe Self-Improvement Protocol,
`.github/workflows/` is in the **forbidden** list for direct agent edits.
This fix must be applied by a human or via the `agent_overseer.py`
sandbox workflow.

## Workaround (until CI fix)

- Manual `lake build` in `proofs/lean/` before any PR that touches `.lean`
  files.
- Document the CI gap in this file (done).

---

*Report generated 2026-05-31 by loop audit agent.*
