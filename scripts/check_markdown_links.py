#!/usr/bin/env python3
"""Markdown link checker for trinity-s3ai.

Validates:
  * Relative markdown links (`./foo`, `bar/baz.md`, `../qux`) — file must exist.
  * `https://github.com/gHashTag/trinity-s3ai/blob/<ref>/<path>` links — the
    `<path>` portion must resolve to a real file in the working tree.

External HTTP(S) links are intentionally **not** fetched: this keeps the
checker deterministic and CI-friendly (no flaky network).

Usage:
    python3 scripts/check_markdown_links.py            # scan default doc set
    python3 scripts/check_markdown_links.py --all      # scan every *.md
    python3 scripts/check_markdown_links.py --check    # CI mode, exit 1 on broken

Exit codes:
    0  no broken links found
    1  one or more broken links found (only meaningful in --check mode)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
REPO_OWNER_REPO = "gHashTag/trinity-s3ai"

# Default scan list: top-level public-facing docs plus docs/ and derivations/.
DEFAULT_GLOBS: list[str] = [
    "README.md",
    "FORMULAS.md",
    "ROADMAP*.md",
    "docs/**/*.md",
    "derivations/**/*.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "FOUNDATIONS.md",
    "HONESTY_MANIFEST.md",
]

# Match `[text](target)` but not images (`![alt](url)`) — and not reference
# definitions. We deliberately keep this regex tolerant of nested parens by
# limiting target chars; complicated cases are rare in this repo.
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

# Skip these path prefixes when present in raw link targets (binary, vendored,
# or non-tracked artifacts that the script should not try to resolve).
SKIP_PREFIXES = ("mailto:", "tel:", "#")


def collect_files(extra_all: bool) -> list[Path]:
    files: list[Path] = []
    if extra_all:
        files.extend(REPO_ROOT.rglob("*.md"))
    else:
        for pattern in DEFAULT_GLOBS:
            files.extend(REPO_ROOT.glob(pattern))
    # Drop anything inside .git / node_modules / target / vendor and dedupe.
    excluded_parts = {".git", "node_modules", "target", "vendor"}
    seen: set[Path] = set()
    out: list[Path] = []
    for f in files:
        if any(part in excluded_parts for part in f.relative_to(REPO_ROOT).parts):
            continue
        if f in seen or not f.is_file():
            continue
        seen.add(f)
        out.append(f)
    return sorted(out)


def is_external(target: str) -> bool:
    parsed = urlparse(target)
    return bool(parsed.scheme and parsed.scheme in {"http", "https"})


def resolve_relative(md_file: Path, target: str) -> Path:
    # Strip anchor / query for filesystem resolution.
    raw = target.split("#", 1)[0].split("?", 1)[0]
    raw = unquote(raw)
    if raw == "":
        return md_file  # pure-anchor link, treat as self
    base = md_file.parent
    return (base / raw).resolve()


def parse_repo_blob_path(target: str) -> str | None:
    """Return the in-repo path for a github blob URL pointing at this repo,
    or None if the URL does not match this repo.
    """
    parsed = urlparse(target)
    if parsed.netloc != "github.com":
        return None
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 4:
        return None
    owner, repo, kind = parts[0], parts[1], parts[2]
    if f"{owner}/{repo}" != REPO_OWNER_REPO:
        return None
    if kind not in {"blob", "tree", "raw"}:
        return None
    # parts[3] is the ref (branch/tag/sha); parts[4:] is the file path.
    return "/".join(parts[4:]) if len(parts) > 4 else ""


FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def check_file(md_file: Path) -> list[tuple[int, str, str]]:
    """Return list of (line_no, target, reason) for broken links.

    Lines inside fenced code blocks (``` … ``` or ~~~ … ~~~) are skipped,
    and inline `code spans` are stripped before parsing, so syntax like
    `[D, L_g](q)` inside math/code is not misread as a link.
    """
    broken: list[tuple[int, str, str]] = []
    text = md_file.read_text(encoding="utf-8", errors="replace")
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        scan_line = INLINE_CODE_RE.sub("", line)
        for match in LINK_RE.finditer(scan_line):
            target = match.group(1).strip()
            if not target or target.startswith(SKIP_PREFIXES):
                continue
            if is_external(target):
                blob_path = parse_repo_blob_path(target)
                if blob_path is None:
                    continue  # external non-repo URL → skip
                if blob_path == "":
                    continue  # blob root → repo itself, OK
                candidate = (REPO_ROOT / blob_path).resolve()
                if not candidate.exists():
                    broken.append((lineno, target, f"repo blob path missing: {blob_path}"))
                continue
            resolved = resolve_relative(md_file, target)
            if not resolved.exists():
                try:
                    rel = resolved.relative_to(REPO_ROOT)
                except ValueError:
                    rel = resolved
                broken.append((lineno, target, f"missing: {rel}"))
    return broken


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--all", action="store_true",
        help="scan every *.md in the repo (excluding .git/vendor/target)",
    )
    parser.add_argument(
        "--check", action="store_true",
        help="exit 1 if any broken link is found (CI mode)",
    )
    parser.add_argument(
        "--files", nargs="*", default=[],
        help="explicit list of markdown files to scan (overrides default set)",
    )
    args = parser.parse_args()

    if args.files:
        files = [REPO_ROOT / f if not Path(f).is_absolute() else Path(f) for f in args.files]
    else:
        files = collect_files(args.all)

    total_links = 0
    broken_total: list[tuple[Path, int, str, str]] = []
    for f in files:
        # Count all link occurrences for reporting.
        text = f.read_text(encoding="utf-8", errors="replace")
        total_links += len(LINK_RE.findall(text))
        for lineno, target, reason in check_file(f):
            broken_total.append((f, lineno, target, reason))

    print(f"Scanned {len(files)} markdown files, {total_links} links total.")
    if not broken_total:
        print("OK: no broken internal or repo-blob links.")
        return 0

    print(f"Broken links: {len(broken_total)}")
    for f, lineno, target, reason in broken_total:
        rel = f.relative_to(REPO_ROOT)
        print(f"  {rel}:{lineno}  {target}  [{reason}]")
    return 1 if args.check else 0


if __name__ == "__main__":
    sys.exit(main())
