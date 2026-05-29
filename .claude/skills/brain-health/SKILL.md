---
name: brain-health
description: Audit and heal anomalies in the Trinity S3AI second brain database
---

# /brain-health

Run a comprehensive health audit on the second brain database and heal any anomalies.

## Anomaly Types

### 1. Status Mismatch
**Symptom:** `brain_status`, `rag_status`, or `ssot_status` counters do not match actual table row counts.

**Audit query:**
```sql
SELECT 
  b.phd_rows, b.phd_chunks, b.phd_embedded,
  b.memories_rows, b.memories_embedded,
  (SELECT COUNT(*) FROM ssot.chapters) as actual_chapters,
  (SELECT COUNT(*) FROM ssot.embeddings) as actual_embeddings,
  (SELECT COUNT(*) FROM ssot.agent_memory) as actual_memories
FROM ssot.brain_status b;
```

**Heal:** Update status tables with actual counts.
```sql
UPDATE ssot.brain_status SET
  phd_rows = (SELECT COUNT(*) FROM ssot.chapters),
  phd_chunks = (SELECT COUNT(*) FROM ssot.embeddings),
  phd_embedded = (SELECT COUNT(*) FROM ssot.embeddings WHERE embedding IS NOT NULL),
  memories_rows = (SELECT COUNT(*) FROM ssot.agent_memory),
  memories_embedded = (SELECT COUNT(*) FROM ssot.agent_memory WHERE embedding IS NOT NULL);

UPDATE ssot.rag_status SET
  total_chunks = (SELECT COUNT(*) FROM ssot.embeddings),
  embedded_chunks = (SELECT COUNT(*) FROM ssot.embeddings WHERE embedding IS NOT NULL),
  coverage_pct = 100.0 * (SELECT COUNT(*) FROM ssot.embeddings WHERE embedding IS NOT NULL) / NULLIF((SELECT COUNT(*) FROM ssot.embeddings), 0);
```

### 2. Missing Embeddings
**Symptom:** Chapters exist but have no embeddings, or `agent_memory` rows lack embeddings.

**Audit query:**
```sql
-- Chapters without embeddings
SELECT c.slug, c.title
FROM ssot.chapters c
LEFT JOIN ssot.embeddings e ON c.slug = e.chapter_slug
WHERE e.id IS NULL;

-- Memories without embeddings
SELECT id, agent_id, title
FROM ssot.agent_memory
WHERE embedding IS NULL;
```

**Heal:** Requires re-running the embedding pipeline (not available via SQL alone). Document missing embeddings and flag for re-indexing.

### 3. Chunk Content Errors
**Symptom:** Empty `chunk_text`, null `embedding`, mismatched `sha256`, duplicate chunks, wrong `anchor`.

**Audit query:**
```sql
SELECT 
  COUNT(*) FILTER (WHERE chunk_text = '' OR chunk_text IS NULL) as empty_chunks,
  COUNT(*) FILTER (WHERE embedding IS NULL) as null_embeddings,
  COUNT(*) FILTER (WHERE anchor IS NULL OR anchor != 'phi^2 + phi^-2 = 3') as bad_anchors,
  COUNT(*) as total
FROM ssot.embeddings;

-- Duplicates
SELECT chapter_slug, chunk_index, COUNT(*) as dup_count
FROM ssot.embeddings
GROUP BY chapter_slug, chunk_index
HAVING COUNT(*) > 1;
```

**Heal:** Delete bad chunks; re-chunk affected chapters.
```sql
DELETE FROM ssot.embeddings WHERE chunk_text = '' OR chunk_text IS NULL;
DELETE FROM ssot.embeddings WHERE embedding IS NULL;
DELETE FROM ssot.embeddings WHERE anchor IS NULL OR anchor != 'phi^2 + phi^-2 = 3';
```

### 4. Schema Mismatch (ssot vs ssot_brochure)
**Symptom:** Chapters exist in one schema but not the other, or `word_count` differs.

**Audit query:**
```sql
SELECT 'Only in ssot' as diff_type, COUNT(*) 
FROM ssot.chapters s
LEFT JOIN ssot_brochure.chapters b ON s.slug = b.slug
WHERE b.slug IS NULL
UNION ALL
SELECT 'Only in ssot_brochure', COUNT(*)
FROM ssot_brochure.chapters b
LEFT JOIN ssot.chapters s ON b.slug = s.slug
WHERE s.slug IS NULL
UNION ALL
SELECT 'Word count mismatch', COUNT(*)
FROM ssot.chapters s
JOIN ssot_brochure.chapters b ON s.slug = b.slug
WHERE s.word_count != b.word_count;
```

**Heal:** This is usually expected — `ssot_brochure` is a curated subset. Report only unexpected divergences.

## Report Format

```
Brain Health Audit
==================
Status Mismatch:     [PASS/FAIL] — details
Missing Embeddings:  [PASS/FAIL] — X chapters, Y memories
Chunk Errors:        [PASS/FAIL] — empty: X, null: Y, bad anchors: Z, dups: W
Schema Mismatch:     [PASS/FAIL] — only in ssot: X, only in brochure: Y, wc diff: Z

Healed: [Y/N]
Remaining issues: [...]
```
