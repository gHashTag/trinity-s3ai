# LEGACY DOCUMENT (historical Zenodo archive preparation — Wave 19)
# Current status: This is a historical planning document. See TECH_TREE.md and
# RESEARCH_STATUS.md for current canonical assessment.

# Zenodo Archive Preparation — Wave 19

**Dataset**: H₄ Numerological Atlas
**Version**: v1.0-wave19
**License**: MIT (code) / CC-BY-4.0 (data)

---

## Metadata

| Field | Value |
|-------|-------|
| Title | H₄ Numerological Atlas: A Catalog of Standard Model Parameter Formulas |
| Authors | [TBD] |
| Publication date | 2026-05-22 |
| DOI | 10.5281/zenodo.XXXXXX (reserve after GitHub release) |
| Keywords | Standard Model, particle physics, golden ratio, data catalog, formal verification, Coq, Lean |
| License | MIT + CC-BY-4.0 |

## Files to Upload

```
trinity-s3ai-v1.0-wave19.tar.gz
├── proofs/              # Coq proof files (79 .v files)
├── derivations/         # Audit reports, MC results, σ-ranking
├── scripts/             # Python validation + MC engine
├── validate_v4.py       # Main validation script
├── FORMULAS.md          # Human-readable catalog
├── paper/               # LaTeX source of data paper
├── talks/               # Beamer talk source
├── README.md            # Project overview
└── CITATION.bib         # BibTeX citation
```

## GitHub-Zenodo Integration

1. Enable Zenodo webhook on GitHub repository
2. Create release `v1.0-wave19`
3. Zenodo auto-archives the release
4. Update DOI in paper and README

## Citation

```bibtex
@dataset{trinity2026atlas,
  title={H4 Numerological Atlas: A Catalog of Standard Model Parameter Formulas},
  author={[Author List]},
  year={2026},
  publisher={Zenodo},
  doi={10.5281/zenodo.XXXXXX},
  url={https://github.com/gHashTag/trinity-s3ai}
}
```
