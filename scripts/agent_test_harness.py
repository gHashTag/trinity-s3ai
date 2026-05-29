#!/usr/bin/env python3
"""
Agent Test Harness — Evaluation-gated updates for safe self-improvement.

Runs project validators + agent-specific smoke tests.
Only PASS allows promote from agent-exp/* to agent-dev.
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run(cmd, cwd=None):
    """Run a command, return (returncode, stdout, stderr)."""
    if cwd is None:
        cwd = REPO_ROOT
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, capture_output=True, text=True
    )
    return result.returncode, result.stdout, result.stderr


def banner(name):
    print(f"\n{'='*60}\n  {name}\n{'='*60}")


def test_validator(name, cmd):
    banner(f"Validator: {name}")
    rc, out, err = run(cmd)
    if rc != 0:
        print(f"  FAIL (exit {rc})")
        print(out)
        print(err)
        return False
    print("  PASS")
    return True


def test_skills_smoke():
    """Parse all SKILL.md files to ensure they are well-formed."""
    banner("Skills Smoke Test")
    skills_dir = REPO_ROOT / ".claude" / "skills"
    if not skills_dir.exists():
        print("  FAIL: .claude/skills/ not found")
        return False

    all_ok = True
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            print(f"  FAIL: {skill_dir.name}/SKILL.md missing")
            all_ok = False
            continue
        content = skill_md.read_text()
        if "## " not in content:
            print(f"  FAIL: {skill_md} missing markdown headers")
            all_ok = False
            continue
        print(f"  OK: {skill_dir.name}")
    return all_ok


def test_claude_md_exists():
    banner("CLAUDE.md Existence")
    claude_md = REPO_ROOT / "CLAUDE.md"
    if not claude_md.exists():
        print("  FAIL: CLAUDE.md missing")
        return False
    print("  PASS")
    return True


def test_agent_overseer_syntax():
    banner("Agent Overseer Syntax")
    overseer = REPO_ROOT / "scripts" / "agent_overseer.py"
    if not overseer.exists():
        print("  FAIL: agent_overseer.py missing")
        return False
    rc, _, err = run(f"{sys.executable} -m py_compile {overseer}")
    if rc != 0:
        print(f"  FAIL: syntax error\n{err}")
        return False
    print("  PASS")
    return True


def main():
    print("Agent Test Harness starting...")
    results = []

    results.append(test_validator("Anti-Numerology Gate", "python3 scripts/anti_numerology_gate.py"))
    results.append(test_validator("Claims Generator Check", "python3 scripts/generate_claims.py --check"))
    results.append(test_validator("English-Only Check", "bash scripts/check_english_only.sh"))
    results.append(test_validator("Admitted Counter", "python3 scripts/count_admitted_honest.py"))

    results.append(test_skills_smoke())
    results.append(test_claude_md_exists())
    results.append(test_agent_overseer_syntax())

    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} passed")
    if all(results):
        print("HARNESS PASS")
        return 0
    else:
        print("HARNESS FAIL")
        return 1


if __name__ == "__main__":
    sys.exit(main())
