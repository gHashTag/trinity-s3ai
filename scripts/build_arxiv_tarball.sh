#!/usr/bin/env bash
# =============================================================================
# Trinity S^3AI — arXiv Submission Tarball Builder
# Wave 15.2
# =============================================================================
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

SUBDIR="arxiv_submission"
TARBALL="trinity-s3ai-arxiv.tar.gz"
MAX_SIZE_MB=10

# ---------------------------------------------------------------------------
# 1. Verify source compiles
# ---------------------------------------------------------------------------
echo "=== Step 1: Verifying LaTeX compilation ==="
cd "$PROJECT_ROOT/paper"

# Clean previous build artifacts
rm -f wave13_paper.aux wave13_paper.log wave13_paper.out wave13_paper.pdf

# Compile
pdflatex -interaction=nonstopmode wave13_paper.tex > /dev/null 2>&1 || {
  echo "ERROR: pdflatex failed on wave13_paper.tex"
  exit 1
}

# Note: wave13_paper.tex uses inline thebibliography, so bibtex is NOT needed.
# natbib is loaded for citation formatting but all \bibitem entries are inline.

echo "OK: wave13_paper.tex compiles to PDF."

# ---------------------------------------------------------------------------
# 2. Assemble submission directory
# ---------------------------------------------------------------------------
echo ""
echo "=== Step 2: Assembling $SUBDIR/ ==="
cd "$PROJECT_ROOT"

rm -rf "$SUBDIR"
mkdir -p "$SUBDIR/anc"

# Core source
cp "paper/wave13_paper.tex" "$SUBDIR/"
cp "paper/wave13_paper.pdf" "$SUBDIR/"  # reference copy, not submitted to arXiv

# Figures
cp -r "figures" "$SUBDIR/"

# Ancillary Python scripts
cp "scripts/validators/validate_v4.py" "$SUBDIR/anc/"
cp "derivations/trinity_d4/d4_analysis.py" "$SUBDIR/anc/"
cp "derivations/higgs_spectral_action/spectral_action.py" "$SUBDIR/anc/"
cp "derivations/f4_spectrum/f4_spectrum.py" "$SUBDIR/anc/"

# Ancillary README
cat > "$SUBDIR/anc/README_anc.txt" << 'EOF'
Trinity S^3AI — Ancillary Files
================================

This directory contains Python validation scripts accompanying the paper
"Trinity S^3AI: An Active Boundary-Mapping Research Program in Geometric Unification".

Files
-----
validate_v4.py
  Comprehensive validation of 25 SM parameter formulas against PDG 2024.
  Requirements: mpmath, numpy
  Run: python3 validate_v4.py

d4_analysis.py
  Discrete Dirac operator on the 24-cell (D4 roots) with KO-dimension
  computation. Demonstrates KO-dim = 5 (mod 8) != 6.
  Requirements: numpy, sympy, mpmath
  Run: python3 d4_analysis.py

spectral_action.py
  Spectral action on the 600-cell discrete Dirac operator. Computes
  tree-level Higgs mass ~132.88 GeV (no sigma-field correction).
  Requirements: numpy, scipy, mpmath
  Run: python3 spectral_action.py

f4_spectrum.py
  Full Dirac spectrum on the binary octahedral group (F4/2O system).
  Verifies KO-dimension 6 (mod 8) for the F4 case.
  Requirements: numpy
  Run: python3 f4_spectrum.py

Notes
-----
- All scripts are self-contained and do not require network access.
- Exact reproduction may depend on the Python and library versions
  documented in the repository README.
- Full Coq/Rocq proof sources are available in the repository
  https://github.com/gHashTag/trinity-s3ai (not included here due to size).
EOF

# ---------------------------------------------------------------------------
# 3. Optional: strip comments from .tex (kept disabled by default)
# ---------------------------------------------------------------------------
# Uncomment the following line to strip percent-comments from the .tex file:
# sed -i.bak '/^%/d; s/  *%.*$//' "$SUBDIR/wave13_paper.tex" && rm -f "$SUBDIR/wave13_paper.tex.bak"

# ---------------------------------------------------------------------------
# 4. Create tarball
# ---------------------------------------------------------------------------
echo ""
echo "=== Step 3: Creating tarball ==="
cd "$PROJECT_ROOT"
tar -czf "$TARBALL" \
  "$SUBDIR/wave13_paper.tex" \
  "$SUBDIR/figures/" \
  "$SUBDIR/anc/"

TARBALL_SIZE=$(stat -f%z "$TARBALL" 2>/dev/null || stat -c%s "$TARBALL" 2>/dev/null)
TARBALL_SIZE_MB=$(awk "BEGIN {printf \"%.2f\", $TARBALL_SIZE / 1024 / 1024}")

echo "Tarball: $TARBALL"
echo "Size:    $TARBALL_SIZE bytes ($TARBALL_SIZE_MB MB)"

# Validate size
if (( $(echo "$TARBALL_SIZE_MB > $MAX_SIZE_MB" | bc -l) )); then
  echo "WARNING: Tarball exceeds arXiv $MAX_SIZE_MB MB limit!"
  exit 1
else
  echo "OK: Tarball is within the $MAX_SIZE_MB MB limit."
fi

# ---------------------------------------------------------------------------
# 5. Print upload instructions
# ---------------------------------------------------------------------------
echo ""
echo "=== arXiv Upload Instructions ==="
echo ""
echo "1. Go to https://arxiv.org/submit"
echo "2. Select Category: hep-th (High Energy Physics - Theory)"
echo "3. Upload the tarball: $PROJECT_ROOT/$TARBALL"
echo "4. Metadata:"
echo "   Title:   Trinity S^3AI: An Active Boundary-Mapping Research Program in Geometric Unification"
echo "   Authors: [Author List TBD]"
echo "   Abstract: (copy from paper/arxiv_abstract.txt)"
echo "   Comments: 6 pages, ancillary files include Python validation scripts"
echo "5. Process files and check the generated PDF preview."
echo "6. Submit."
echo ""
echo "NOTE: If you are a first-time hep-th submitter, you need an endorser."
echo "      See paper/endorsement_request.txt for a template email."
echo ""
echo "Done."
