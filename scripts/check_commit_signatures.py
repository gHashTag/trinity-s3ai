#!/usr/bin/env python3
"""
check_commit_signatures.py — CI-level check that all commits in a range are GPG-signed.

Trinity S3AI requires signed commits on `main` to prevent authorship forgery.
This script is intended to run in CI (e.g., after merge or on PR) and fails
if any commit in the checked range lacks a verified signature.

USAGE (local):
    python3 scripts/check_commit_signatures.py HEAD~10..HEAD

USAGE (CI — GitHub Actions):
    python3 scripts/check_commit_signatures.py ${{ github.event.pull_request.base.sha }}..${{ github.event.pull_request.head.sha }}

EXIT CODES
    0 — all commits signed (or range is empty).
    1 — one or more commits are unsigned.
    2 — bad arguments / not a git repo.
"""

import os
import subprocess
import sys
from pathlib import Path


def should_skip() -> bool:
    """Check whether the skip override is active."""
    commit_msg = os.environ.get("GIT_COMMIT_MSG", "") or os.environ.get("COMMIT_MESSAGE", "")
    if "[skip-signature-check]" in commit_msg:
        print("[WARN] [skip-signature-check] in commit message — signature gate downgraded to warning", file=sys.stderr)
        return True
    return False


def run_git(args: list[str]) -> str:
    """Run git and return stdout, or raise on error."""
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parent.parent,
    )
    if result.returncode != 0:
        print(f"[ERROR] git {' '.join(args)} failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(2)
    return result.stdout


def check_range(commit_range: str) -> list[str]:
    """Return list of unsigned commit SHAs in the given range."""
    # %G?  — show signature status: G=good, B=bad, U=unknown, X=expired, Y=expired key, R=revoked, N=no signature
    raw = run_git(["log", "--pretty=format:%H %G? %s", commit_range])
    unsigned = []
    for line in raw.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split(" ", 2)
        if len(parts) < 2:
            continue
        sha, sig_flag = parts[0], parts[1]
        # Accept: G (good), U (unknown but present), Y (expired key but valid sig)
        # Reject: N (no signature), B (bad signature), X (expired), R (revoked)
        if sig_flag not in {"G", "U", "Y"}:
            unsigned.append(line)
    return unsigned


def main() -> int:
    if len(sys.argv) < 2:
        # Default: check all commits on current branch not on main
        print("Usage: python3 scripts/check_commit_signatures.py <commit-range>")
        print("Example: python3 scripts/check_commit_signatures.py main..HEAD")
        print()
        print("Checking default range: origin/main..HEAD")
        commit_range = "origin/main..HEAD"
    else:
        commit_range = sys.argv[1]

    print(f"Scanning commit range: {commit_range}")
    unsigned = check_range(commit_range)

    if not unsigned:
        print("✓ All commits are signed.")
        return 0

    print(f"✗ Found {len(unsigned)} unsigned commit(s):")
    for line in unsigned:
        print(f"  {line}")
    print()
    print("REMINDER: Configure commit signing:")
    print("  1. gpg --full-generate-key")
    print("  2. git config --global user.signingkey <KEY_ID>")
    print("  3. git config --global commit.gpgsign true")
    print("  4. git commit -S --amend  # to re-sign the last commit")
    print()

    if should_skip():
        print("[WARN] Gate overridden — exiting with 0 (warnings only)")
        return 0

    print("To bypass in an emergency, add [skip-signature-check] to the commit message.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
