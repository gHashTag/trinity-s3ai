#!/usr/bin/env python3
"""
syntactic_check.py — Lightweight syntactic validator for TrinityLean .lean files.

Wave 10.3 CI check.  Does NOT require elan/lake/Lean to be installed.

Checks performed for each .lean file:
  1. Count `def`, `theorem`, `lemma`, `axiom`, `noncomputable def` declarations.
  2. Verify each declaration has a body (`:=`, `by`, or `where` follows header).
  3. Detect suspicious typo patterns: `= =`, `-> ->`, `by by`.
  4. Count `sorry` occurrences and report their line numbers.
  5. Count `axiom` declarations (explicit, non-sorry).

Output: JSON summary to stdout + per-file details.
Exit code: 0 if no sorries, 1 if sorries found (for CI gating).
"""

import re
import sys
import json
import pathlib
import textwrap

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

# Declaration starters (non-capturing prefix so we can extract the name)
DECL_PATTERN = re.compile(
    r'^\s*(?:noncomputable\s+)?'
    r'(def|theorem|lemma|axiom|instance|structure|inductive|class)\s+'
    r'(\w+)',
    re.MULTILINE,
)

# A declaration line that has no body on the same line and the next
# non-blank line does not start with `|`, `:=`, `by`, `where`, `·`
# — we do a simple paired check below instead.

TYPO_PATTERNS = [
    (re.compile(r'= ='), '`= =` (double equals, likely typo)'),
    (re.compile(r'→ →'), '`→ →` (double arrow, likely typo)'),
    (re.compile(r'-> ->'), '`-> ->` (double arrow, likely typo)'),
    (re.compile(r'\bby\s+by\b'), '`by by` (duplicate tactic keyword)'),
    (re.compile(r'\bdo\s+do\b'), '`do do` (duplicate do keyword)'),
]

SORRY_PATTERN   = re.compile(r'\bsorry\b')
# Pattern to strip Lean single-line comments before sorry check
LEAN_COMMENT    = re.compile(r'--.*$')
AXIOM_PATTERN   = re.compile(r'^\s*axiom\s+(\w+)', re.MULTILINE)
TODO_PATTERN    = re.compile(r'--\s*TODO', re.IGNORECASE)

# ---------------------------------------------------------------------------
# File analysis
# ---------------------------------------------------------------------------

def analyze_file(path: pathlib.Path) -> dict:
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()

    result = {
        'file': str(path),
        'declarations': [],
        'declaration_count': 0,
        'sorry_count': 0,
        'sorry_lines': [],
        'axiom_count': 0,
        'axiom_names': [],
        'typo_warnings': [],
        'todo_count': 0,
        'ok': True,
    }

    # 1. Declarations — strip comments first to avoid matching inside doc strings
    # We do a preliminary strip for the declaration count
    text_stripped_for_decls = re.sub(r'/-.*?-/', '', text, flags=re.DOTALL)
    text_stripped_for_decls = re.sub(r'--[^\n]*', '', text_stripped_for_decls)
    decls = DECL_PATTERN.findall(text_stripped_for_decls)
    result['declarations'] = [f'{kind} {name}' for kind, name in decls]
    result['declaration_count'] = len(decls)

    # 2. Sorry occurrences — strip all comments first, then scan for bare sorry
    # Strip Lean block comments (/- ... -/) from entire text
    text_no_block = re.sub(r'/-.*?-/', '', text, flags=re.DOTALL)
    # Strip single-line comments (-- ...)
    text_no_comments = re.sub(r'--[^\n]*', '', text_no_block)
    code_lines = text_no_comments.splitlines()
    for i, line in enumerate(code_lines, start=1):
        if SORRY_PATTERN.search(line):
            result['sorry_count'] += 1
            result['sorry_lines'].append(i)

    # 3. Axiom declarations (only in comment-stripped code)
    axioms = []
    for line in code_lines:  # code_lines already has all comments stripped
        m = re.match(r'\s*axiom\s+(\w+)', line)
        if m:
            axioms.append(m.group(1))
    result['axiom_names'] = axioms
    result['axiom_count'] = len(axioms)

    # 4. Typo patterns
    for lineno, line in enumerate(lines, start=1):
        for pattern, label in TYPO_PATTERNS:
            if pattern.search(line):
                result['typo_warnings'].append({
                    'line': lineno,
                    'pattern': label,
                    'text': line.strip()[:80],
                })

    # 5. TODO count
    result['todo_count'] = len(TODO_PATTERN.findall(text))

    # 6. Basic body check: every `theorem`/`lemma` should be followed by
    #    `:= by`, `:= {`, `where`, or just `by` within the next 600 chars.
    #    NOTE: multi-line type signatures push the body indicator further ahead;
    #    we search within 600 chars (roughly 15 lines) to reduce false positives.
    missing_body = []
    for m in re.finditer(
        r'^\s*(?:noncomputable\s+)?(?:theorem|lemma)\s+(\w+)([^\n]*)',
        text_stripped_for_decls, re.MULTILINE
    ):
        name = m.group(1)
        start_pos = m.end()
        # Grab up to 600 chars after the header to find := or by
        snippet = text_stripped_for_decls[start_pos:start_pos + 600]
        if not re.search(r':=|where\b|\bby\b', snippet):
            missing_body.append(name)

    result['missing_body_warnings'] = missing_body

    if result['sorry_count'] > 0:
        result['ok'] = False

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    lean_dir = pathlib.Path(__file__).parent / 'TrinityLean'
    lean_files = sorted(lean_dir.glob('*.lean'))

    if not lean_files:
        print(json.dumps({'error': f'No .lean files found in {lean_dir}'}))
        sys.exit(0)

    file_results = []
    total_sorry = 0
    total_decls = 0
    total_axioms = 0
    total_todos = 0

    for fp in lean_files:
        r = analyze_file(fp)
        file_results.append(r)
        total_sorry  += r['sorry_count']
        total_decls  += r['declaration_count']
        total_axioms += r['axiom_count']
        total_todos  += r['todo_count']

    summary = {
        'total_files': len(file_results),
        'total_declarations': total_decls,
        'total_sorry': total_sorry,
        'total_axioms': total_axioms,
        'total_todos': total_todos,
        'all_ok': total_sorry == 0,
        'files': file_results,
    }

    print(json.dumps(summary, indent=2))

    # Human-readable summary to stderr
    sep = '-' * 60
    print(sep, file=sys.stderr)
    print('TrinityLean Syntactic Check — Wave 10.3', file=sys.stderr)
    print(sep, file=sys.stderr)
    for r in file_results:
        name = pathlib.Path(r['file']).name
        status = 'OK' if r['ok'] else f"FAIL ({r['sorry_count']} sorry)"
        print(f"  {name:<40} {r['declaration_count']:3} decls  "
              f"{r['axiom_count']:2} axioms  "
              f"{r['sorry_count']:2} sorry  {status}",
              file=sys.stderr)
        if r['typo_warnings']:
            for w in r['typo_warnings']:
                print(f"    WARN line {w['line']}: {w['pattern']}", file=sys.stderr)
        if r['missing_body_warnings']:
            for name_d in r['missing_body_warnings']:
                print(f"    WARN: theorem/lemma '{name_d}' may lack body", file=sys.stderr)
    print(sep, file=sys.stderr)
    print(f'  TOTAL  decls={total_decls}  axioms={total_axioms}  '
          f'sorry={total_sorry}  todos={total_todos}', file=sys.stderr)
    print(f'  STATUS: {"PASS — no sorry" if total_sorry == 0 else "FAIL — sorry found"}',
          file=sys.stderr)
    print(sep, file=sys.stderr)

    sys.exit(0 if total_sorry == 0 else 1)


if __name__ == '__main__':
    main()
