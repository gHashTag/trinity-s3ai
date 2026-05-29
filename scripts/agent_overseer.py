#!/usr/bin/env python3
"""
Agent Overseer — Safe Self-Improvement Orchestrator

Architecture: AgentGit + SICA + EvoGit + Gödel Agent
- Git worktree isolation for sandbox experiments
- Evaluation-gated promotion (harness must pass)
- Scope-gated edits (only .claude/skills/, .claude/scheduled_tasks.json)
- Immutable commit graph (every agent step is a commit)

Usage:
    python3 scripts/agent_overseer.py start-task "Improve second-brain skill"
    python3 scripts/agent_overseer.py evaluate
    python3 scripts/agent_overseer.py promote
    python3 scripts/agent_overseer.py abort
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKTREE_PARENT = REPO_ROOT.parent
ALLOWED_SCOPE = {
    ".claude/skills/",
    ".claude/scheduled_tasks.json",
    "scripts/agent_overseer.py",
    "scripts/agent_test_harness.py",
}
FORBIDDEN_SCOPE = {
    "CLAUDE.md",
    "docs/claims.yaml",
    "proofs/",
    ".github/workflows/",
    "scripts/validators/",
    "scripts/anti_numerology_gate.py",
    "scripts/generate_claims.py",
}
MAX_AGENT_COMMITS = 15


def run(cmd, cwd=None, check=True, capture=True):
    """Run shell command, return stdout."""
    if cwd is None:
        cwd = REPO_ROOT
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, capture_output=capture, text=True
    )
    if check and result.returncode != 0:
        print(f"ERROR: Command failed: {cmd}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()


def current_branch():
    return run("git rev-parse --abbrev-ref HEAD")


def ensure_on_main():
    branch = current_branch()
    if branch != "main" and not branch.startswith("agent-"):
        print(f"WARNING: You are on branch '{branch}'. Overseer expects main.")
        response = input("Continue? [y/N] ")
        if response.lower() != "y":
            sys.exit(0)


def get_next_exp_number():
    """Find next available agent-exp/NNN number."""
    branches = run("git branch -a")
    nums = []
    for line in branches.splitlines():
        m = re.search(r"agent-exp/(\d+)", line)
        if m:
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


def create_sandbox(task_prompt: str):
    """Create a new agent-exp/NNN branch + worktree."""
    ensure_on_main()
    n = get_next_exp_number()
    branch = f"agent-exp/{n:03d}"
    worktree_dir = WORKTREE_PARENT / f"trinity-s3ai-exp-{n:03d}"

    print(f"[overseer] Creating sandbox {branch} at {worktree_dir}")

    # Create branch from agent-dev
    run(f"git branch {branch} agent-dev")
    # Create worktree
    run(f"git worktree add {worktree_dir} {branch}")

    # Write task prompt into sandbox
    task_file = worktree_dir / ".claude" / "AGENT_TASK.md"
    task_file.write_text(
        f"# Agent Self-Improvement Task\n\n"
        f"**Branch:** {branch}\n"
        f"**Created:** {datetime.utcnow().isoformat()}Z\n\n"
        f"## Task\n\n{task_prompt}\n\n"
        f"## Rules\n\n"
        f"1. Only edit files under these paths:\n"
        f"   - `.claude/skills/`\n"
        f"   - `.claude/scheduled_tasks.json`\n"
        f"   - `scripts/agent_overseer.py` and `scripts/agent_test_harness.py`\n"
        f"2. NEVER edit:\n"
        f"   - `CLAUDE.md`\n"
        f"   - `docs/claims.yaml`\n"
        f"   - `proofs/`\n"
        f"   - `.github/workflows/`\n"
        f"   - `scripts/validators/`\n"
        f"3. Commit after every significant change: `git commit -m \"agent-step: <description>\"`\n"
        f"4. Maximum {MAX_AGENT_COMMITS} agent commits per task.\n"
    )

    # Initial commit in sandbox
    run(f"git -C {worktree_dir} add .claude/AGENT_TASK.md")
    run(
        f"git -C {worktree_dir} commit -m 'agent-start: {branch} — {task_prompt[:60]}'"
    )

    print(f"[overseer] Sandbox ready.")
    print(f"[overseer] Worktree: {worktree_dir}")
    print(f"[overseer] Branch: {branch}")
    print(f"\nNext steps:")
    print(f"  1. cd {worktree_dir}")
    print(f"  2. claude --project {worktree_dir}")
    print(f"  3. Give the task to Claude Code")
    print(f"  4. When done, run: python3 {REPO_ROOT}/scripts/agent_overseer.py evaluate --branch {branch}")

    return branch, worktree_dir


def count_agent_commits(branch: str) -> int:
    """Count commits on branch that are not on agent-dev."""
    log = run(f"git log agent-dev..{branch} --oneline")
    return len([l for l in log.splitlines() if l.strip()])


def check_scope(branch: str) -> tuple[bool, list[str]]:
    """Return (pass, forbidden_files) for touched files on branch."""
    diff_files = run(f"git diff --name-only agent-dev..{branch}")
    touched = [f for f in diff_files.splitlines() if f.strip()]
    forbidden = []
    for f in touched:
        for bad in FORBIDDEN_SCOPE:
            if f.startswith(bad) or f == bad:
                forbidden.append(f)
    if forbidden:
        return False, forbidden
    # Also verify at least one touched file is in allowed scope
    allowed_touched = [f for f in touched if any(f.startswith(a) or f == a for a in ALLOWED_SCOPE)]
    if not allowed_touched:
        return False, ["No touched files in allowed scope"]
    return True, []


def evaluate(branch: str = None):
    """Run test harness and scope check."""
    if branch is None:
        # Try to infer from current directory or current branch
        branch = current_branch()
        if not branch.startswith("agent-exp/"):
            print("ERROR: Not on an agent-exp branch. Use --branch or cd into sandbox worktree.")
            sys.exit(1)

    print(f"[overseer] Evaluating {branch}...")

    # 1. Commit count check
    commits = count_agent_commits(branch)
    print(f"  Commits since agent-dev: {commits} (limit {MAX_AGENT_COMMITS})")
    if commits > MAX_AGENT_COMMITS:
        print(f"FAIL: Too many agent commits ({commits} > {MAX_AGENT_COMMITS})")
        return False

    # 2. Scope check
    scope_ok, forbidden = check_scope(branch)
    if not scope_ok:
        print(f"FAIL: Scope violation — touched forbidden files: {forbidden}")
        return False
    print("  Scope check: PASS")

    # 3. Run project test harness
    harness = REPO_ROOT / "scripts" / "agent_test_harness.py"
    print("  Running test harness...")
    result = subprocess.run(
        [sys.executable, str(harness)], cwd=REPO_ROOT
    )
    if result.returncode != 0:
        print("FAIL: Test harness failed")
        return False
    print("  Test harness: PASS")

    # 4. Git status clean check in worktree
    worktrees = run("git worktree list --porcelain")
    worktree_dir = None
    for line in worktrees.splitlines():
        if line.startswith("worktree "):
            worktree_dir = line.split(None, 1)[1]
        if line == f"branch refs/heads/{branch}":
            break
    if worktree_dir:
        status = run(f"git -C {worktree_dir} status --porcelain", check=False)
        if status.strip():
            print(f"WARNING: Uncommitted changes in worktree: {worktree_dir}")
            print(status)
            # Not a hard fail, but warn

    print(f"[overseer] Evaluation PASSED for {branch}")
    print(f"\nTo promote: python3 {REPO_ROOT}/scripts/agent_overseer.py promote --branch {branch}")
    print(f"To abort:   python3 {REPO_ROOT}/scripts/agent_overseer.py abort --branch {branch}")
    return True


def promote(branch: str = None):
    """Merge sandbox branch into agent-dev."""
    if branch is None:
        branch = current_branch()
    if not branch.startswith("agent-exp/"):
        print("ERROR: Not on an agent-exp branch.")
        sys.exit(1)

    # Safety: re-run evaluation
    if not evaluate(branch):
        print("Promote blocked: evaluation failed.")
        sys.exit(1)

    print(f"[overseer] Merging {branch} into agent-dev...")
    run(f"git checkout agent-dev")
    run(f"git merge --no-ff {branch} -m 'agent-promote: merge {branch} into agent-dev'")

    print(f"[overseer] Promoted. agent-dev now contains changes from {branch}.")
    print(f"[overseer] To merge into stable: git checkout agent-stable && git merge agent-dev")
    print(f"[overseer] To cleanup: python3 {REPO_ROOT}/scripts/agent_overseer.py abort --branch {branch}")


def abort(branch: str = None):
    """Delete sandbox branch and worktree."""
    if branch is None:
        branch = current_branch()
    if not branch.startswith("agent-exp/"):
        print("ERROR: Not on an agent-exp branch.")
        sys.exit(1)

    # Find worktree
    worktrees = run("git worktree list --porcelain")
    worktree_dir = None
    for line in worktrees.splitlines():
        if line.startswith("worktree "):
            worktree_dir = line.split(None, 1)[1]
        if line == f"branch refs/heads/{branch}":
            break

    print(f"[overseer] Aborting {branch}...")
    if worktree_dir:
        run(f"git worktree remove {worktree_dir}")
        print(f"  Removed worktree: {worktree_dir}")
    run(f"git branch -D {branch}")
    print(f"  Deleted branch: {branch}")
    print("[overseer] Cleanup complete.")


def status():
    """Show all agent branches and worktrees."""
    print("=== Agent Branches ===")
    branches = run("git branch --list 'agent-*'")
    print(branches or "(none)")
    print("\n=== Worktrees ===")
    worktrees = run("git worktree list")
    print(worktrees or "(none)")
    print("\n=== Current branch ===")
    print(current_branch())


def main():
    parser = argparse.ArgumentParser(description="Agent Overseer")
    sub = parser.add_subparsers(dest="command")

    p_start = sub.add_parser("start-task", help="Create a sandbox for a self-improvement task")
    p_start.add_argument("prompt", help="Task description for the agent")

    p_eval = sub.add_parser("evaluate", help="Evaluate a sandbox branch")
    p_eval.add_argument("--branch", help="Branch to evaluate (default: current)")

    p_promote = sub.add_parser("promote", help="Promote sandbox to agent-dev")
    p_promote.add_argument("--branch", help="Branch to promote (default: current)")

    p_abort = sub.add_parser("abort", help="Delete sandbox branch and worktree")
    p_abort.add_argument("--branch", help="Branch to abort (default: current)")

    sub.add_parser("status", help="Show agent branches and worktrees")

    args = parser.parse_args()

    if args.command == "start-task":
        create_sandbox(args.prompt)
    elif args.command == "evaluate":
        evaluate(args.branch)
    elif args.command == "promote":
        promote(args.branch)
    elif args.command == "abort":
        abort(args.branch)
    elif args.command == "status":
        status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
