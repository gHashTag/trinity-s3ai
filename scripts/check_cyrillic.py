#!/usr/bin/env python3
"""
CI gate: Reject new Cyrillic text in markdown and documentation files.
Allow existing legacy files with explicit LEGACY header.
"""
import sys, os, re

LEGACY_HEADER = "LEGACY: Russian-language document"
CYRILLIC_RE = re.compile(r'[А-Яа-яЁё]')

EXCLUDED_PATHS = [
    ".git",
    "archive/",
]

EXIT_OK = 0
EXIT_FAIL = 1

def main():
    failures = []
    for root, dirs, files in os.walk('.'):
        # Skip excluded dirs
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}]
        for fname in files:
            if not fname.endswith(('.md', '.txt', '.yaml', '.yml', '.rst')):
                continue
            path = os.path.join(root, fname)
            # Skip excluded paths
            if any(ex in path for ex in EXCLUDED_PATHS):
                continue
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except (UnicodeDecodeError, IOError):
                continue
            if not CYRILLIC_RE.search(content):
                continue
            # Allow if LEGACY header is present
            if LEGACY_HEADER in content[:500]:
                continue
            failures.append(path)
    
    if failures:
        print("ERROR: Cyrillic text found in documentation files without LEGACY header:")
        for p in failures:
            print(f"  {p}")
        print("\nAll public documentation must be in English.")
        print("If this is an intentional legacy Russian document, add this header to the first line:")
        print(f'  {LEGACY_HEADER} — translation pending')
        return EXIT_FAIL
    
    print("OK: No undocumented Cyrillic text found.")
    return EXIT_OK

if __name__ == '__main__':
    sys.exit(main())
