# Agent Architecture: Safe Self-Improvement

## Problem

The agent (Claude Code with custom skills/hooks) breaks its own configuration during self-improvement tasks. Manual rollback is required every time.

## Solution: Git-Native Sandbox + Evaluation-Gated Promotion

Based on 5 scientific papers from 2024–2025:

| Paper | Core Idea | How We Use It |
|-------|-----------|---------------|
| **AgentGit** (arXiv:2511.00628) | Git-like version control for multi-agent systems: rollback, branching, checkpoint/revert | `git worktree` for parallel stable/dev/exp sessions |
| **SICA** (arXiv:2504.15228v2) | Self-improving coding agent with overseer, sandboxing, evaluation-gated updates | `agent_overseer.py` + `agent_test_harness.py` |
| **EvoGit** (arXiv:2506.02049) | Git phylogenetic graph — every edit is an immutable commit | Every agent step is a `git commit` |
| **Gödel Agent** (ACL 2025) | Recursive self-modification with sandboxing and constrained edits | Scope gate: only `.claude/skills/` and `scheduled_tasks.json` are editable |
| **AUTOEXPERIMENT** (arXiv:2506.19724) | Sandboxed evaluation, dynamic debugging | CI-ified harness with project validators |

## Branch Topology

```
main          ← physics project trunk (your work)
  ↑
agent-stable  ← release version of agent config
  ↑ fast-forward only
agent-dev     ← integration branch for tested improvements
  ↑ merge only after harness pass
agent-exp/001 ← sandbox: agent edits itself here
agent-exp/002 ← another sandbox
```

### Worktree Layout

```
/Users/playra/trinity-s3ai          → main / agent-stable
/Users/playra/trinity-s3ai-dev      → agent-dev (git worktree)
/Users/playra/trinity-s3ai-exp-001  → agent-exp/001 (git worktree, created on demand)
```

Each worktree has its own `.claude/` directory. The agent runs in the sandbox worktree. If it breaks, delete the worktree — stable is untouched.

## Components

### 1. `scripts/agent_overseer.py`

Orchestrator. Commands:
- `start-task <prompt>` — creates `agent-exp/NNN` branch + worktree, writes task file
- `evaluate --branch NNN` — runs harness + scope gate
- `promote --branch NNN` — merges into `agent-dev` (only if evaluate passed)
- `abort --branch NNN` — deletes branch + worktree
- `status` — lists all agent branches and worktrees

Safety features:
- **Scope gate**: checks `git diff --name-only agent-dev..BRANCH`. Auto-rejects if forbidden files touched.
- **Commit limit**: max 15 agent commits per task.
- **Evaluation gate**: promote blocked unless harness passes.

### 2. `scripts/agent_test_harness.py`

Test suite for agent changes:
- Project validators: `anti_numerology_gate.py`, `generate_claims.py --check`, `check_english_only.sh`, `validators/test_comprehensive.py`
- Skills smoke test: parses all `SKILL.md` files
- `CLAUDE.md` existence check
- `agent_overseer.py` syntax check

### 3. `.github/workflows/agent-ci.yml`

CI for `agent-stable` and `agent-dev` pushes:
- Runs harness
- Runs project validators
- Blocks direct push to `agent-stable` (scope gate)

## Workflow Example

```bash
# User wants the agent to improve the second-brain skill
python3 scripts/agent_overseer.py start-task \
  "Add error handling to the second-brain skill"
# → creates ../trinity-s3ai-exp-001

# Work in sandbox
cd ../trinity-s3ai-exp-001
claude --project ../trinity-s3ai-exp-001
# (agent edits SKILL.md, commits)

# Evaluate
python3 scripts/agent_overseer.py evaluate --branch agent-exp/001
# → harness runs, scope check passes

# Promote to dev
python3 scripts/agent_overseer.py promote --branch agent-exp/001
# → merged into agent-dev

# Cleanup sandbox
python3 scripts/agent_overseer.py abort --branch agent-exp/001
```

## Rollback

If the agent breaks in sandbox:
```bash
python3 scripts/agent_overseer.py abort --branch agent-exp/001
```
This deletes the branch and worktree. `agent-stable` and `main` are untouched.

## Future Extensions

- **Golden tasks benchmark**: Add agent-specific benchmark tasks (e.g., "Run `/second-brain` query, verify output format") to harness.
- **Overseer-as-daemon**: Run overseer as a background watcher that auto-aborts if harness fails on a timer.
- **A/B testing**: Run two `agent-exp/` branches in parallel, compare harness scores.

## References

- AgentGit: [arXiv:2511.00628](https://arxiv.org/pdf/2511.00628)
- SICA: [arXiv:2504.15228v2](https://arxiv.org/html/2504.15228v2)
- EvoGit: [arXiv:2506.02049](https://arxiv.org/pdf/2506.02049)
- Gödel Agent: [ACL 2025](https://aclanthology.org/2025.acl-long.1354.pdf)
- AUTOEXPERIMENT: [arXiv:2506.19724](https://arxiv.org/pdf/2506.19724)
