Trinity S^3AI — Ancillary Files
================================

This directory contains Python validation scripts accompanying the paper
"Trinity S^3AI: A Constructive Negative Result in Geometric Unification".

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
