#!/usr/bin/env bash
# check_english_only.sh — scan top-level public-facing docs for Cyrillic text.
#
# Scope: files that a first-time visitor or peer reviewer is likely to read.
# Out of scope: derivations/**/*.md (private research notes), generated
# artifacts (arxiv_submission/, figures/, paper/*.tex), binaries.
#
# Exit codes:
#   0 — no Cyrillic in any scanned file.
#   1 — Cyrillic found; the script prints file:line for every hit.
#
# Run from the repo root:
#   bash scripts/check_english_only.sh

set -u
shopt -s nullglob

# Files to scan. Glob expansion happens here; missing paths are silently skipped.
TARGETS=(
  README.md
  SECURITY.md
  HONESTY_MANIFEST.md
  RESEARCH_STATUS.md
  CONTRIBUTING.md
  ROADMAP.md
  ROADMAP_WAVE17_PLUS.md
  FORMULAS.md
  docs/status/COQ_HONEST_STATUS.md
  CITATION.cff
  CITATION.bib
  derivations/formulas_cleanup/PROPOSAL.md
  talks/SPEAKER_NOTES.md
)

# Add globbed sets — include the public-facing docs/ subfolders introduced in
# the Phase-1 repository cleanup (status/, roadmaps/, applications/).
for f in docs/*.md docs/status/*.md docs/roadmaps/*.md \
         docs/applications/*.md .github/*.md scripts/*.md; do
  TARGETS+=("$f")
done

# Cyrillic Unicode block: U+0400..U+04FF (and supplement U+0500..U+052F).
# grep -P understands \p{Cyrillic}; if -P is unavailable, we fall back to a
# Python one-liner. We prefer ripgrep when present.
status=0
hits=0

scan_file() {
  local file="$1"
  [[ -f "$file" ]] || return 0
  # Use python3 for portable Unicode range matching.
  python3 - "$file" <<'PY'
import re, sys
fn = sys.argv[1]
pat = re.compile(r'[Ѐ-ԯ]')
try:
    with open(fn, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if pat.search(line):
                print(f"{fn}:{i}: {line.rstrip()}")
                sys.exit(2)
except Exception as e:
    print(f"{fn}: ERROR {e}", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
PY
}

for f in "${TARGETS[@]}"; do
  if scan_file "$f"; then
    :
  else
    rc=$?
    if [[ $rc -eq 2 ]]; then
      hits=$((hits + 1))
      status=1
    fi
  fi
done

if [[ $status -eq 0 ]]; then
  echo "check_english_only: PASS — no Cyrillic found in $(printf '%s ' "${TARGETS[@]}" | wc -w) scanned files."
else
  echo
  echo "check_english_only: FAIL — Cyrillic found in $hits file(s). See lines above."
  echo "Public-facing docs must be English-only. Translate or move the content to a non-public location."
fi

exit $status
