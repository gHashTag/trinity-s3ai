# arXiv Submission Prep Guide — hep-th

## Step-by-step submission checklist

### 1. Pre-submission checks
- [ ] Paper compiles cleanly with `pdflatex` (zero errors, minimal warnings)
- [ ] All figures are included in the submission tarball
- [ ] Bibliography is either inline (`thebibliography`) or a generated `.bbl` file
- [ ] No proprietary fonts or packages that arXiv does not support

### 2. Required files

| File | Purpose | arXiv location |
|------|---------|----------------|
| `wave13_paper.tex` | Main source | Root |
| `wave13_paper.bbl` | Bibliography (if using BibTeX) | Root |
| `*.png` / `*.pdf` | Figures | Root or `figures/` |
| `anc/` | Ancillary files (code, data) | `anc/` directory |

**Note:** `wave13_paper.tex` uses an inline `thebibliography`, so no `.bbl` file is required.

### 3. Build the submission tarball

```bash
cd paper/
tar -czvf trinity-s3ai-arxiv.tar.gz \
  wave13_paper.tex \
  ../figures/fig1_h4_coxeter.png \
  ../figures/fig2_600cell.png \
  ../figures/fig3_accuracy.png \
  ../figures/fig4_couplings.png \
  ../figures/fig5_spectrum.png
```

If including code/data:
```bash
mkdir -p anc
cp -r ../proofs/trinity anc/
cp -r ../trinity_rust anc/
tar -czvf trinity-s3ai-arxiv.tar.gz wave13_paper.tex figures/ anc/
```

### 4. arXiv web upload
1. Go to https://arxiv.org/submit
2. Select **Category:** `hep-th` (High Energy Physics - Theory)
3. Upload the `.tar.gz` tarball
4. Fill metadata:
   - **Title:** Trinity S$^3$AI: A Constructive Negative Result in Geometric Unification
   - **Authors:** [Author List TBD]
   - **Abstract:** (copy from `paper/abstract.txt`)
   - **Comments:** 6 pages, 5 figures
   - **Report number:** (optional)
5. Process files → check the generated PDF preview
6. Submit

### 5. Endorsement request template

If you are a first-time arXiv submitter in hep-th, you need an endorser.

**Subject:** Endorsement request — hep-th submission on geometric unification

```
Dear [Dr. Endorser Name],

I am preparing a submission to arXiv hep-th and would be grateful for your endorsement.

**Paper:** "Trinity S³AI: A Constructive Negative Result in Geometric Unification"
**Category:** hep-th
**Abstract:** [paste abstract]
**Repository:** https://github.com/gHashTag/trinity-s3ai

The paper reports a machine-assisted falsification of a discrete spectral-action model for the Standard Model based on the H₄ Coxeter group and the 600-cell. The result is negative (a No-Go theorem), but it is constructive: all theorems are formally proved in Coq/Rocq 8.20.1, and every numerical claim is reproducible in Python.

I have verified that the manuscript compiles with pdflatex and that all figures are vector or high-resolution PNG. The source code and proof scripts are included in the `anc/` directory.

Would you be willing to endorse this submission?

Thank you for your time.

Best regards,
[Your Name]
[Your Affiliation]
[Your Email]
```

### 6. Post-submission
- [ ] Note the arXiv identifier (e.g., `arXiv:2605.XXXXX`)
- [ ] Update `CITATION.cff` and `README.md` with the arXiv ID
- [ ] Create a Zenodo release and link the DOI
- [ ] Tweet / post to Mastodon with the arXiv link

## Current status (Wave 14.5)

- `wave13_paper.tex`: compiles, 6 pages, minor hyperref warnings (math in bookmarks)
- Figures: 5 PNGs ready
- Code in `anc/`: not yet bundled (do before final upload)
- Endorsement: not yet requested
