# arXiv Submission Prep Guide — hep-th

## Step-by-step submission checklist

### 1. Pre-submission checks
- [x] Paper compiles cleanly with `pdflatex` (zero errors, minimal warnings)
- [x] All figures are included in the submission tarball
- [x] Bibliography is inline (`thebibliography`), no `.bbl` file required
- [x] No proprietary fonts or packages that arXiv does not support

### 2. Required files

| File | Purpose | arXiv location |
|------|---------|----------------|
| `wave13_paper.tex` | Main source | Root |
| `*.png` | Figures | `figures/` subdirectory |
| `anc/` | Ancillary files (code, data) | `anc/` directory |

**Note:** `wave13_paper.tex` uses an inline `thebibliography`, so no `.bbl` file is required. The `natbib` package is loaded only for citation formatting (`numbers,sort&compress`).

### 3. Build the submission tarball

Run the automated build script:

```bash
bash scripts/build_arxiv_tarball.sh
```

This script will:
1. Verify that `paper/wave13_paper.tex` compiles with `pdflatex`.
2. Assemble `arxiv_submission/` with the `.tex`, figures, and ancillary files.
3. Create `trinity-s3ai-arxiv.tar.gz`.
4. Validate the tarball size is under 10 MB.
5. Print upload instructions.

**Manual equivalent (if you prefer not to use the script):**

```bash
cd /Users/playra/trinity-s3ai
mkdir -p arxiv_submission/anc
cp paper/wave13_paper.tex arxiv_submission/
cp -r figures arxiv_submission/
cp scripts/validators/validate_v4.py derivations/trinity_d4/d4_analysis.py \
   derivations/higgs_spectral_action/spectral_action.py \
   derivations/f4_spectrum/f4_spectrum.py arxiv_submission/anc/
tar -czf trinity-s3ai-arxiv.tar.gz arxiv_submission/
```

### 4. arXiv web upload

1. Go to https://arxiv.org/submit
2. Select **Category:** `hep-th` (High Energy Physics - Theory)
3. Upload the `.tar.gz` tarball (`trinity-s3ai-arxiv.tar.gz`)
4. Fill metadata:
   - **Title:** Trinity S$^3$AI: An Active Boundary-Mapping Research Program in Geometric Unification
   - **Authors:** [Author List TBD]
   - **Abstract:** (copy from `paper/arxiv_abstract.txt`)
   - **Comments:** 6 pages, ancillary files include Python validation scripts
   - **Report number:** (optional)
5. Process files → check the generated PDF preview
6. Submit

#### Submitting the paper — screenshot walkthrough

After logging in to arXiv and starting a new submission, you will see a multi-step form:

1. **Start** — Select "hep-th" as the primary category. No secondary categories are required, but you may add "math-ph" or "gr-qc" if desired.
2. **Upload** — Drag and drop `trinity-s3ai-arxiv.tar.gz` into the file upload area. arXiv will unpack it and show a file tree. You should see:
   ```
   wave13_paper.tex
   figures/
     fig1_h4_coxeter.png
     fig2_600cell.png
     fig3_accuracy.png
     fig4_couplings.png
     fig5_spectrum.png
   anc/
     README_anc.txt
     validate_v4.py
     d4_analysis.py
     spectral_action.py
     f4_spectrum.py
   ```
3. **Metadata** — Paste the title, authors, and the plain-text abstract from `paper/arxiv_abstract.txt`.
4. **Preview** — arXiv compiles the source and shows a PDF preview. Verify that:
   - The PDF has 6 pages.
   - All equations render correctly.
   - No "missing package" or font-substitution warnings appear.
5. **Submit** — Click the final submit button. You will receive an automated confirmation email with a temporary identifier.

### 5. Endorsement request template

If you are a first-time arXiv submitter in hep-th, you need an endorser.

**Subject:** Endorsement request — hep-th submission on geometric unification

```
Dear [Dr. Endorser Name],

I am preparing a submission to arXiv hep-th and would be grateful for your endorsement.

**Paper:** "Trinity S³AI: An Active Boundary-Mapping Research Program in Geometric Unification"
**Category:** hep-th
**Abstract:** [paste abstract from paper/arxiv_abstract.txt]
**Repository:** https://github.com/gHashTag/trinity-s3ai

The paper reports a machine-assisted falsification of a discrete spectral-action model for the Standard Model based on the H₄ Coxeter group and the 600-cell. The result is negative (a Boundary theorem), but it is constructive: all theorems are formally proved in Coq/Rocq 8.20.1, and every numerical claim is reproducible in Python.

I have verified that the manuscript compiles with pdflatex and that all figures are high-resolution PNG. The source code and proof scripts are included in the `anc/` directory.

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

## Current status (Wave 15.2)

- `wave13_paper.tex`: compiles, 6 pages, minor hyperref warnings (math in bookmarks)
- Figures: 5 PNGs ready
- Code in `anc/`: bundled (validate_v4.py, d4_analysis.py, spectral_action.py, f4_spectrum.py)
- Tarball: `trinity-s3ai-arxiv.tar.gz` (~1 MB, well under 10 MB limit)
- Endorsement: not yet requested
- arXiv category: **hep-th**
