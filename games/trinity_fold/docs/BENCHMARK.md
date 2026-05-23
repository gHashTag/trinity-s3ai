# Benchmark mode (CASP analogue)

CASP works by inviting structure-prediction methods to predict targets
whose true structures are known to the organizers but withheld from the
predictors until after submissions close. Trinity Fold's `benchmark` mode
is a small, single-player echo of that idea.

When the `--benchmark` flag is set on the CLI, or the **Benchmark mode**
checkbox is enabled in the web UI, the `value` and `uncertainty` fields of
specific observables are stripped before scoring. The player can still see
the observable exists (and that its value is hidden), but the
`observable_fit` term cannot reward agreement with a held-out target.

## Held-out set

The default held-out ids are listed in `crates/ring3_adapters/src/fixtures.rs` under
`benchmark_holdout_ids`:

| id | name | rationale for holding out |
|---|---|---|
| `o_cosmo_lambda` | Λ (cosmological constant) | Covered by NGT1; a strong test of whether a board can avoid known no-go territory. |
| `o_mt_over_mb` | m_t / m_b | A clean dimensionless target sensitive to the Yukawa sector. |

## What this does **not** simulate

A serious held-out evaluation would require:

- **Versioned catalogs.** Hiding only the value still leaks the existence
  and the unit of the target.
- **Submission protocol.** Real CASP locks predictions before targets are
  revealed; the prototype does not enforce this.
- **Multiple targets per round and per method.** Single-player only.

If you build on this, treat the benchmark mode as a discipline cue, not as
a substitute for blinded evaluation. The repo's broader experimental
preregistration lives in
[`experimental_protocol.md`](../../../experimental_protocol.md) and
[`dune_preregistration.md`](../../../dune_preregistration.md); those are the
real instruments.
