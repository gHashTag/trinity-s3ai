# ROADMAP: Fix All Gaps and Problems
## Trinity S3AI v3.5 — Complete Action Plan

## Category A: Critical (Blocks scientific acceptance)

### A1. Coq Compilation — Rocq 9.1.1 setup
- [ ] Install Rocq 9.1.1 via opam
- [ ] Install coq-interval 4.11.4
- [ ] Install coquelicot 4.2.0
- [ ] Compile ALL 16 .v files
- [ ] Verify: 0 errors, 0 Admitted
- [ ] Screenshot for README

### A2. Honest P-Value — Monte-Carlo simulation
- [ ] Run honest_pvalue.py (1M trials)
- [ ] Document results in HonestPValue.v
- [ ] Cross-check with analytical bound

### A3. Missing Formulas — improve W-class to V-class
- [ ] sin²θ₁₃ = φ^(3/2)/(30π) — verify numerically
- [ ] λ = √φ/π² — verify vs LHC Run 3
- [ ] Check if any W-class can be improved

## Category B: Important (Strengthens credibility)

### B1. GitHub Repository
- [ ] Initialize remote
- [ ] Add .gitignore
- [ ] Push all 25 files
- [ ] Create GitHub Actions CI (compile + test)
- [ ] Add README badges

### B2. Documentation Unification
- [ ] Merge AGENTS.md into README
- [ ] Create single paper.md (merged from all sources)
- [ ] Add FAQ section (10 common questions)
- [ ] Create CITATION.bib

### B3. Test Coverage
- [ ] Python test for ALL 25 formulas (currently 23)
- [ ] Add test for new SG-4,5,6,7
- [ ] Add numerical verification script

## Category C: Nice to have (Future work)

### C1. ArXiv Preparation
- [ ] Format paper to arXiv standards
- [ ] Create ancillary files (Coq + Python)
- [ ] Write abstract (< 1920 chars)

### C2. Collaboration Outreach
- [ ] Draft email to Morató de Dalmases
- [ ] Draft email to Dechant
- [ ] Draft email to potential endorsers

### C3. Public Engagement
- [ ] Create simple HTML visualization
- [ ] Create formula reference card (PDF)
- [ ] Twitter/thread summary

## Execution Order
Phase 1 (now): A1, A2, A3, B3
Phase 2 (next): B1, B2
Phase 3 (future): C1, C2, C3
