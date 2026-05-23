# Preparing Zenodo Release — Trinity S3AI

**Version**: v1.0-wave14  
**Date**: 2026-05-23  
**Status**: Constructive negative result

> **IMPORTANT**: This is a "constructive negative result" release. The DOI will point
> to a software record documenting No-Go theorems and falsification tests, not to
> a positive unification claim.

---

## Step 1: Enable Zenodo–GitHub Integration

> **Screenshot 1** — Zenodo GitHub settings page showing the toggle for
> `gHashTag/trinity-s3ai` switched to **ON**.

1. Log in to [https://zenodo.org](https://zenodo.org) using your GitHub or ORCID account.
2. Navigate to **Settings → GitHub** → [https://zenodo.org/account/settings/github/](https://zenodo.org/account/settings/github/)
3. Find `gHashTag/trinity-s3ai` in the repository list.
4. Click **Enable** (toggle to ON).
5. Zenodo will now automatically monitor this repository for new release tags.

---

## Step 2: Push Tag `v1.0-wave14` to GitHub

> **Screenshot 2** — Terminal showing `git push origin v1.0-wave14` and the
> successful remote confirmation.

```bash
# Verify the tag exists locally
git tag -l v1.0-wave14

# Push the annotated tag to GitHub
git push origin v1.0-wave14
```

Alternatively, run the helper script (does **not** execute automatically):

```bash
# Review the script first
cat scripts/push_release.sh

# Make executable and run when ready
chmod +x scripts/push_release.sh
./scripts/push_release.sh
```

---

## Step 3: Zenodo Auto-Creates a Record and Reserved DOI

> **Screenshot 3** — Zenodo deposit page showing a new draft record with status
> **Draft** and a reserved DOI badge.

1. Within ~5 minutes of pushing the tag, Zenodo creates a new draft record.
2. Go to [https://zenodo.org/deposit](https://zenodo.org/deposit).
3. Locate the draft titled *"Trinity S3AI: A Constructive Negative Result in Geometric Unification"*.
4. A DOI is **reserved** at this stage but is not public until you publish.

---

## Step 4: Edit the Zenodo Record

> **Screenshot 4** — Zenodo metadata edit form with fields filled:
> Title, Authors, Description, Keywords, License, and Related identifiers.

Click **Edit** on the draft record and complete or verify the following fields:

| Field | Value |
|-------|-------|
| **Title** | Trinity S3AI: A Constructive Negative Result in Geometric Unification |
| **Authors** | [Fill in real names and ORCID iDs] |
| **Description** | Formal proofs, numerical validation, and discrete spectral geometry testing the hypothesis that Standard Model parameters derive from the H4 Coxeter group and 600-cell. |
| **Resource type** | Software |
| **License** | MIT |
| **Keywords** | noncommutative geometry, Coxeter groups, Standard Model, Coq, formal proof |
| **Version** | v1.0-wave14 |
| **Related identifiers** | GitHub: `https://github.com/gHashTag/trinity-s3ai` |

Add any additional references, funding information, or institutional affiliations as needed.

---

## Step 5: Publish and Copy the DOI

> **Screenshot 5** — Published Zenodo record page displaying the final DOI
> (`10.5281/zenodo.XXXXXXX`) and citation widget.

1. Click **Publish** in the Zenodo edit form.
2. The DOI (e.g., `10.5281/zenodo.1234567`) becomes active immediately.
3. Copy the exact DOI string.

### Update `CITATION.cff`

Replace the placeholder:

```yaml
# Before:
doi: 10.5281/zenodo.PLACEHOLDER  # Replace with real DOI after Zenodo sync

# After:
doi: 10.5281/zenodo.XXXXXXX
```

### Update `README.md`

Add the Zenodo DOI badge near the top of the file:

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

Commit and push the updates:

```bash
git add CITATION.cff README.md
git commit -m "docs: add Zenodo DOI v1.0-wave14"
git push origin main
```

---

## Post-Release Verification

```bash
# Verify the DOI resolves
curl -sI "https://doi.org/10.5281/zenodo.XXXXXXX" | head -5

# Inspect Zenodo API metadata
curl -s "https://zenodo.org/api/records/XXXXXXX" | python3 -m json.tool | head -40
```

---

## Checklist

- [ ] Zenodo–GitHub integration enabled for `gHashTag/trinity-s3ai`
- [ ] Local tag `v1.0-wave14` pushed to GitHub (`git push origin v1.0-wave14`)
- [ ] Zenodo draft record appears at [https://zenodo.org/deposit](https://zenodo.org/deposit)
- [ ] Metadata (title, authors, description, keywords, license) verified in Zenodo
- [ ] Record published and DOI obtained
- [ ] DOI copied into `CITATION.cff`
- [ ] DOI badge added to `README.md`
- [ ] Changes committed and pushed to `main`

---

*Wave 15.3 — Trinity S3AI Zenodo Release Preparation*
