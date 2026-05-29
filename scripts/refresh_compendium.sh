#!/usr/bin/env bash
# refresh_compendium.sh — drop a new GOLDEN CHAIN Compendium PDF into this repo.
#
# What it does:
#   1. Copies the supplied PDF into releases/GOLDEN_CHAIN_compendium_v<N>.pdf
#   2. Renders page 1 (cover) into figures/golden_chain_compendium_cover.png
#      and figures/golden_chain_compendium_v<N>_cover.png
#   3. Computes the SHA-256 and prints a ready-to-paste README metadata block
#   4. (Optional) Patches the README table in place when --patch-readme is set
#
# Usage:
#   ./scripts/refresh_compendium.sh <path-to-pdf> <version> [upstream_commit] [--patch-readme]
#
# Example:
#   ./scripts/refresh_compendium.sh \
#       /path/to/trios-mcp-rag/generated/out/GOLDEN_CHAIN_2026-05-29.pdf \
#       v12 \
#       abcdef0 \
#       --patch-readme
#
# Requirements: pdftoppm (poppler-utils), pdfinfo, sha256sum, awk, sed.

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <pdf-path> <version> [upstream_commit] [--patch-readme]" >&2
  exit 64
fi

PDF_SRC="$1"
VERSION="$2"
UPSTREAM_COMMIT="${3:-}"
PATCH_README="false"
for arg in "$@"; do
  [[ "$arg" == "--patch-readme" ]] && PATCH_README="true"
done

if [[ ! -f "$PDF_SRC" ]]; then
  echo "error: $PDF_SRC not found" >&2
  exit 66
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RELEASE_DIR="$REPO_ROOT/releases"
FIG_DIR="$REPO_ROOT/figures"
mkdir -p "$RELEASE_DIR" "$FIG_DIR"

PDF_DST="$RELEASE_DIR/GOLDEN_CHAIN_compendium_${VERSION}.pdf"
cp "$PDF_SRC" "$PDF_DST"

# Cover preview (latest + versioned copy)
TMP_COVER_PREFIX="$(mktemp -d)/cover"
pdftoppm -f 1 -l 1 -png -r 110 "$PDF_DST" "$TMP_COVER_PREFIX"
COVER_RENDERED="${TMP_COVER_PREFIX}-001.png"
cp "$COVER_RENDERED" "$FIG_DIR/golden_chain_compendium_cover.png"
cp "$COVER_RENDERED" "$FIG_DIR/golden_chain_compendium_${VERSION}_cover.png"

# Stats
SHA256="$(sha256sum "$PDF_DST" | awk '{print $1}')"
PAGES="$(pdfinfo "$PDF_DST" | awk '/^Pages:/ {print $2}')"
SIZE_BYTES="$(stat -c%s "$PDF_DST")"
SIZE_MB="$(awk -v b="$SIZE_BYTES" 'BEGIN { printf "%.2f", b/1024/1024 }')"
TODAY="$(date -u +%Y-%m-%d)"

echo
echo "=== refresh_compendium summary ==="
echo "PDF       : releases/$(basename "$PDF_DST")"
echo "Cover     : figures/golden_chain_compendium_cover.png (+ ${VERSION}_cover.png)"
echo "Version   : $VERSION"
echo "Pages     : $PAGES"
echo "Size      : ${SIZE_MB} MB"
echo "SHA-256   : $SHA256"
echo "Upstream  : ${UPSTREAM_COMMIT:-<unset>}"
echo

# Render the markdown block users can paste into README
cat <<EOF
=== README block (paste into the 'Latest GOLDEN CHAIN Compendium' table) ===
| Version | **${VERSION}** (${TODAY}) |
| Download | [\`releases/GOLDEN_CHAIN_compendium_${VERSION}.pdf\`](releases/GOLDEN_CHAIN_compendium_${VERSION}.pdf) (${SIZE_MB} MB) |
| Pages | ${PAGES} (A4) |
| SHA-256 | \`${SHA256}\` |
EOF

if [[ -n "$UPSTREAM_COMMIT" ]]; then
  echo "| Upstream commit | [\`trios-mcp-rag@${UPSTREAM_COMMIT}\`](https://github.com/gHashTag/trios-mcp-rag/commit/${UPSTREAM_COMMIT}) |"
fi

if [[ "$PATCH_README" == "true" ]]; then
  README="$REPO_ROOT/README.md"
  [[ -f "$README" ]] || { echo "error: README.md missing"; exit 70; }
  python3 - "$README" "$VERSION" "$TODAY" "$SIZE_MB" "$PAGES" "$SHA256" "$UPSTREAM_COMMIT" <<'PY'
import re, sys, pathlib
readme_path, version, today, size_mb, pages, sha, upstream = sys.argv[1:]
p = pathlib.Path(readme_path)
text = p.read_text(encoding="utf-8")

def sub(pat, repl, label):
    new, n = re.subn(pat, repl, text, count=1)
    if n == 0:
        print(f"warn: {label} pattern not matched, skipping", file=sys.stderr)
    return new

text = sub(r"\| Version \| \*\*v\d+\*\* \([\d-]+\) \|",
           f"| Version | **{version}** ({today}) |", "version row")
text = sub(r"\| Download \| \[`releases/GOLDEN_CHAIN_compendium_v\d+\.pdf`\]\(releases/GOLDEN_CHAIN_compendium_v\d+\.pdf\) \([\d.]+ MB\) \|",
           f"| Download | [`releases/GOLDEN_CHAIN_compendium_{version}.pdf`](releases/GOLDEN_CHAIN_compendium_{version}.pdf) ({size_mb} MB) |",
           "download row")
text = sub(r"\| Pages \| \d+ \(A4\) \|",
           f"| Pages | {pages} (A4) |", "pages row")
text = sub(r"\| SHA-256 \| `[0-9a-f]{64}` \|",
           f"| SHA-256 | `{sha}` |", "sha row")
# Cover link points at the *latest versioned PDF* (we keep older files for history).
text = sub(r'<a href="releases/GOLDEN_CHAIN_compendium_v\d+\.pdf">',
           f'<a href="releases/GOLDEN_CHAIN_compendium_{version}.pdf">',
           "cover anchor")
if upstream:
    text = sub(r"\| Upstream commit \| \[`trios-mcp-rag@[0-9a-f]+`\]\(https://github\.com/gHashTag/trios-mcp-rag/commit/[0-9a-f]+\) \|",
               f"| Upstream commit | [`trios-mcp-rag@{upstream}`](https://github.com/gHashTag/trios-mcp-rag/commit/{upstream}) |",
               "upstream row")
p.write_text(text, encoding="utf-8")
print("README.md patched in place.")
PY
fi
