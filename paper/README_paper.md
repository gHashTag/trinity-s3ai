# README: Trinity-s3ai Paper for arXiv (Wave 10.1)

**Paper file:** `wave10_paper.tex`  
**Bibliography:** `wave10_paper.bib`  
**Status:** Draft, ready for compilation and checking  
**Preparation date:** June 2026  
**Principle:** "Do not lie!! Be honest!"

---

## 1. Paper Description

**Title:**  
*Trinity-s3ai: An Active Boundary-Mapping Research Program on H4-Based Standard Model Unification*  
*(Subtitle: Four Boundary Theorems for NCG Approaches Founded on the 600-Cell)*

**Authors:** `[Anonymous, gHashTag]` — fill in before submission.

**Abstract (250 words):** Presented in the `abstract` section of `wave10_paper.tex`.  
Key thesis: H4/600-cell in the current formulation **cannot** derive the parameters  
of the Standard Model — four boundary theorems (BT-1–4) prove this.  
Six positive structural results survive.

---

## 2. How to Compile

### 2.1 Requirements

- **TeX distribution:** TeX Live 2023 or MiKTeX 24 (full installation)
- **Compiler:** `pdflatex` or `lualatex` (`pdflatex` recommended)
- **Bibliography processor:** `biber` (NOT `bibtex` — uses `biblatex`)
- **Main packages:** amsmath, amssymb, hyperref, biblatex, listings, booktabs,
  longtable, lmodern, microtype, geometry, xcolor, caption

### 2.2 Compilation Commands

Execute strictly in the indicated order:

```bash
cd /home/user/workspace/trinity-s3ai/paper

# Step 1: first pdflatex pass (creates .aux)
pdflatex wave10_paper.tex

# Step 2: biber processes bibliography
biber wave10_paper

# Step 3: second pdflatex pass (inserts references)
pdflatex wave10_paper.tex

# Step 4: third pdflatex pass (final table of contents)
pdflatex wave10_paper.tex
```

### 2.3 Single script (bash)

```bash
#!/bin/bash
set -e
cd "$(dirname "$0")"  # change to paper/ directory
NAME="wave10_paper"
pdflatex "$NAME.tex"
biber "$NAME"
pdflatex "$NAME.tex"
pdflatex "$NAME.tex"
echo "Done: $NAME.pdf"
```

### 2.4 Makefile (optional)

```makefile
NAME = wave10_paper
.PHONY: all clean

all: $(NAME).pdf

$(NAME).pdf: $(NAME).tex $(NAME).bib
	pdflatex $(NAME)
	biber $(NAME)
	pdflatex $(NAME)
	pdflatex $(NAME)

clean:
	rm -f *.aux *.bbl *.blg *.bcf *.log *.out *.run.xml *.toc *.lof *.lot
```

### 2.5 Syntax Check Without LaTeX

```bash
# Check for unbalanced curly braces
python3 -c "
content = open('wave10_paper.tex').read()
d = 0
for i, ch in enumerate(content):
    if ch == '{': d += 1
    elif ch == '}': d -= 1
    if d < 0:
        print(f'Unmatched }} at position {i}'); break
print(f'Final depth: {d}')
"
```

Expected result: `Final depth: 0`

---

## 3. arXiv Submission Status

**Current status:** ❌ NOT yet submitted.

Necessary steps before submission:

- [ ] Fill in author field (replace `[Anonymous, gHashTag]`)
- [ ] Add ORCID, if available
- [ ] Compile PDF and check formatting
- [ ] Check all bibliography links (DOIs active)
- [ ] Request endorsement (see Section 5)
- [ ] Write an explanation letter (for arXiv reviewer)

---

## 4. arXiv Categories

**Primary category:** `hep-th`  
Justification: paper on high-energy physics theories, noncommutative geometry,  
Dirac operator, attempt at Standard Model unification.

**Secondary categories:**
- `math-ph` — mathematical physics: KO-dimension theorems, η-invariant, Coxeter groups
- `cs.LO` — logic in computer science: Coq formalization, ~730 Qed, Lean 4 scaffold

**How to specify at submission:**  
At the "Subject Class" step in the arXiv submission interface:
```
Primary:   hep-th
Secondary: math-ph cs.LO
```

---

## 5. Endorsement Requirements

arXiv requires **endorsement** for the first submission to category `hep-th`.

### 5.1 Who Can Endorse

Any active arXiv author with ≥ 3 publications in `hep-th` in the last 5 years.

### 5.2 How to Request

1. Register at https://arxiv.org
2. Attempt to submit the paper — the system will ask for an endorser
3. Write a letter to the endorser (template below)

### 5.3 Endorser Letter Template (English)

```
Subject: arXiv endorsement request for hep-th submission

Dear Professor [Name],

I am writing to request arXiv endorsement for a submission to hep-th.

The paper, "Trinity-s3ai: An Active Boundary-Mapping Research Program on H4-Based
Standard Model Unification," presents four machine-verified boundary theorems
showing that the H4 Coxeter group (600-cell symmetry group) cannot serve as
the geometric foundation for deriving Standard Model parameters in the
noncommutative geometry (NCG) framework.

Key features of the paper:
- Four explicit boundary theorems (cosmological impossibility, no sigma-field,
  vector-like spectrum, mass hierarchy obstruction via Schur's lemma)
- Six positive structural results (KO-dim 6 mod 8, eta = -2, first-order
  condition, etc.)
- ~730 machine-verified Coq Qed theorems (73 .v files)
- Honest comparison with Distler-Garibaldi theorem for E8

My arXiv ID: [fill in]
My paper arXiv ID: [fill in after submission system provides it]

Thank you for your consideration.
[Name]
```

### 5.4 Alternative Category Without Endorsement

If endorsement for `hep-th` is not obtained, one can try `math-ph` (requirements are softer).  
Cross-listing to `hep-th` and `cs.LO` is done automatically.

---

## 6. Paper Structure

| Section | Title | Pages (estimate) |
|--------|-------|-----------------|
| 1 | Introduction | ~3 |
| 2 | H4 and the 600-Cell | ~3 |
| 3 | Catalog: 25 formulas | ~4 |
| 4 | Positive structural results (P1–P6) | ~5 |
| 5 | Boundary theorems (BT-1–4) | ~7 |
| 6 | Comparison with prior work | ~2 |
| 7 | Coq/Lean 4 formalization | ~2 |
| 8 | Falsifiability | ~2 |
| 9 | Discussion | ~2 |
| 10 | Conclusion | ~1 |
| App A | Coq theorem table | ~2 |
| App B | Reproducibility | ~1 |
| **Total** | | **~34 pages** |

---

## 7. Bibliography

File `wave10_paper.bib` contains 34 entries (exceeds the required 30).  
Format: biblatex (style `numeric-comp`).

**Key references:**
- Chamseddine-Connes 1996–2012 (NCG SM) — 6 entries
- Connes NCG book + 2006 article — 3 entries
- Lisi 2007 + Distler-Garibaldi 2010 — 2 entries
- Coxeter, Conway-Smith (H4, quaternions) — 2 entries
- APS η-invariant (Atiyah-Patodi-Singer, Gilkey) — 2 entries
- Planck 2018, DESI 2024, NuFit 6.0, PDG 2022 — 4 entries
- DUNE 2020 — 1 entry
- Coq, Lean 4, Hales (formalization) — 3 entries
- Coleman-Mandula, Haag-Lopuszanski-Sohnius — 2 entries
- Weinberg cosmological constant — 1 entry
- Koide 1983, Shechtman 1984 — 2 entries
- F-theory (Beasley-Heckman-Vafa) — 1 entry
- Krajewski, Barrett, Devastato (NCG classification) — 3 entries
- Boyle-Farnsworth, Furey — 2 entries
- Serre (representations), Loday (Hochschild) — 2 entries

---

## 8. Honesty and Key Caveats

The paper follows the project principle "Do not lie." Main honest statements:

1. **The abstract explicitly says "boundary-mapping research program" and "boundary"** — do not soften the honesty, but update the framing.
2. **0 out of 25 formulas have class R (strict derivation)** — this is stated in the text.
3. **754σ** falsification of baryon density — the number is present in the abstract and text.
4. **\(\sigdist = 5.62\)** for BT-4 — machine-verified, do not reduce.
5. **7 Admitted** — all listed with explanations in the appendix.
6. **\(\delta_{CP} = 65.66°\)** — explicitly marked as NF (Numerical Fit), not "prediction".

---

## 9. Author Information

**Author field in paper:** `[Anonymous, gHashTag]`  
**Replace with:** `[Real name], [Affiliation]`

If publishing anonymously (allowed on arXiv):  
- Repository: `https://github.com/[gHashTag]/trinity-s3ai`
- Contact: via GitHub Issues

---

## 10. Pre-Submission Checklist

- [ ] PDF compiled without LaTeX errors
- [ ] All \cite{...} references resolve
- [ ] Tables do not overflow margins (check longtable)
- [ ] Abstract ≤ 250 words (count: `wc -w abstract.txt`)
- [ ] File `wave10_paper.bib` is in the same directory
- [ ] Author and date filled in
- [ ] Git tag `wave10-submission` created:
      `git tag -a wave10-submission -m "arXiv submission Wave 10.1"`
- [ ] SHA-256 hash of .vo files recorded in `checksums.txt`
- [ ] DUNE pre-registration `registered_predictions.md` already in repository ✓

---

*Document prepared as part of Wave 10.1 of the Trinity S3AI project. June 2026.*
