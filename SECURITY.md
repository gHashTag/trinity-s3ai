# Security Policy — Trinity S3AI

Trinity S3AI is a research repository (Coq proofs, Python validators,
Rust prototypes, and a static GitHub Pages canvas). It does not run
network services, does not store user data, and does not require any
secrets to build or test. This document describes the small surface
that nonetheless exists, and how to report a problem responsibly.

## Supported components

| Component | What it is | Security surface |
|-----------|------------|------------------|
| Coq proofs (`proofs/`, `derivations/`) | Static `.v` source | none |
| Python scripts (`scripts/`, including `scripts/validators/`) | Local validators / gates | local file I/O only; no network |
| Rust crates (`trinity_rust/`, `games/trinity_fold/`) | Local binaries, library code, and a wasm-compiled canvas UI | runs locally or in the browser; no server |
| Static site at <https://t27.ai/trinity-s3ai/> | GitHub Pages deploy of `games/trinity_fold/web/canvas` | client-side wasm + SVG; no backend |
| CI workflows (`.github/workflows/`) | GitHub Actions | uses only the default `GITHUB_TOKEN` with the minimum permissions documented in each workflow |

## What is *not* in scope

- No production service.
- No user authentication or user data.
- No database, no message broker, no cloud-resource provisioning.
- No long-lived secrets in this repository.

## Secrets policy

This repository must contain **no** API keys, tokens, passwords, or
private connection strings. Strings like `id-token: write` inside a
GitHub Actions workflow are *permission declarations*, not secrets,
and are expected to appear in `.github/workflows/pages.yml`.

If you find what looks like a leaked secret in the tree (current or
historical), please report it privately per the next section so it can
be rotated and scrubbed before a public issue is filed.

## Reporting a vulnerability

Please report security issues privately, not in a public issue or PR.

- Preferred: open a **GitHub Security Advisory** via the repository's
  "Security" tab → "Report a vulnerability". This keeps the report
  private to the maintainers and allows a coordinated disclosure
  timeline.
- Alternative: open a minimal public issue that says only *"please
  contact me about a private security report"*, without describing the
  vulnerability, and wait for a maintainer to follow up off-list.

We will acknowledge a private report within a reasonable window
(target: 7 days), confirm whether the report is in scope per the
"Supported components" table above, and coordinate a fix and
disclosure schedule with the reporter.

## Out-of-scope examples

- Theoretical disagreements with the physics or the proofs are
  **not** security issues; please open a regular issue using
  [`.github/ISSUE_TEMPLATE.md`](.github/ISSUE_TEMPLATE.md) instead.
- A reviewer disagreeing with a claim status is not a security issue;
  see [`docs/CLAIM_STATUS.md`](docs/CLAIM_STATUS.md) for the rules and
  open an issue if a document violates them.
- Bugs in the GOLDEN CHAIN canvas that affect UX but not the user's
  browser security are regular bugs, not vulnerabilities.

## Dependencies

The Rust workspaces pin major dependency versions in `Cargo.toml`. CI
runs Rust's standard toolchain and Coq's published Docker image. The
Python validators depend only on `mpmath` and `numpy`. We accept PRs
that update dependencies to address advisories from `cargo audit`,
`pip-audit`, or similar.
