#!/usr/bin/env python3
"""
Brain Health Audit Script for Trinity S3AI Second Brain

Usage:
    export TRINITY_DATABASE_URL="postgresql://postgres:..."
    python3 scripts/audit_brain.py

Or with hardcoded URL (not recommended):
    python3 scripts/audit_brain.py --url "postgresql://..."
"""

import os
import sys
import argparse

try:
    import psycopg2
except ImportError:
    print("ERROR: psycopg2 is required. Install: pip install psycopg2-binary")
    sys.exit(1)


def get_connection(url=None):
    if url is None:
        url = os.environ.get("TRINITY_DATABASE_URL")
        if not url:
            print("ERROR: Set TRINITY_DATABASE_URL environment variable or use --url")
            sys.exit(1)
    return psycopg2.connect(url)


def run_audit(conn):
    cur = conn.cursor()
    issues = []
    print("=" * 60)
    print("Trinity S3AI — Brain Health Audit")
    print("=" * 60)
    print()

    # 1. Status Mismatch Audit
    print("[1] Status Mismatch Audit")
    print("-" * 40)
    cur.execute("""
        SELECT
            b.phd_rows, b.phd_chunks, b.phd_embedded,
            b.memories_rows, b.memories_embedded,
            (SELECT COUNT(*) FROM ssot.chapters) as actual_chapters,
            (SELECT COUNT(*) FROM ssot.embeddings) as actual_embeddings,
            (SELECT COUNT(*) FROM ssot.embeddings WHERE embedding IS NOT NULL) as actual_embedded,
            (SELECT COUNT(*) FROM ssot.agent_memory) as actual_memories,
            (SELECT COUNT(*) FROM ssot.agent_memory WHERE embedding IS NOT NULL) as actual_mem_embedded
        FROM ssot.brain_status b
    """)
    row = cur.fetchone()
    (
        claimed_phd_rows, claimed_phd_chunks, claimed_phd_embedded,
        claimed_mem_rows, claimed_mem_embedded,
        actual_chapters, actual_embeddings, actual_embedded,
        actual_memories, actual_mem_embedded
    ) = row

    checks = [
        ("phd_rows", claimed_phd_rows, actual_chapters),
        ("phd_chunks", claimed_phd_chunks, actual_embeddings),
        ("phd_embedded", claimed_phd_embedded, actual_embedded),
        ("memories_rows", claimed_mem_rows, actual_memories),
        ("memories_embedded", claimed_mem_embedded, actual_mem_embedded),
    ]

    for name, claimed, actual in checks:
        status = "PASS" if claimed == actual else "FAIL"
        if status == "FAIL":
            issues.append(f"brain_status.{name}: claimed={claimed}, actual={actual}")
        print(f"  {name}: claimed={claimed}, actual={actual} [{status}]")

    # Check rag_status
    cur.execute("""
        SELECT
            r.total_chunks, r.embedded_chunks, r.coverage_pct,
            (SELECT COUNT(*) FROM ssot.embeddings) as actual_total,
            (SELECT COUNT(*) FROM ssot.embeddings WHERE embedding IS NOT NULL) as actual_embedded
        FROM ssot.rag_status r
    """)
    rag = cur.fetchone()
    claimed_total, claimed_emb, claimed_cov, actual_total, actual_emb = rag
    rag_ok = (claimed_total == actual_total and claimed_emb == actual_emb)
    status = "PASS" if rag_ok else "FAIL"
    if not rag_ok:
        issues.append(f"rag_status: claimed_total={claimed_total}, actual={actual_total}, claimed_emb={claimed_emb}, actual={actual_emb}")
    print(f"  rag_status: total={claimed_total}/{actual_total}, embedded={claimed_emb}/{actual_emb}, coverage={claimed_cov}% [{status}]")

    # Check ssot_brochure.rag_status
    cur.execute("""
        SELECT
            r.total_chunks, r.embedded_chunks, r.coverage_pct,
            (SELECT COUNT(*) FROM ssot_brochure.embeddings) as actual_total,
            (SELECT COUNT(*) FROM ssot_brochure.embeddings WHERE embedding IS NOT NULL) as actual_embedded
        FROM ssot_brochure.rag_status r
    """)
    brag = cur.fetchone()
    if brag:
        bclaimed_total, bclaimed_emb, bclaimed_cov, bactual_total, bactual_emb = brag
        brag_ok = (bclaimed_total == bactual_total and bclaimed_emb == bactual_emb)
        status = "PASS" if brag_ok else "FAIL"
        if not brag_ok:
            issues.append(f"ssot_brochure.rag_status: claimed_total={bclaimed_total}, actual={bactual_total}")
        print(f"  ssot_brochure.rag_status: total={bclaimed_total}/{bactual_total}, embedded={bclaimed_emb}/{bactual_emb} [{status}]")

    # Check ssot_brochure.ssot_status
    cur.execute("""
        SELECT
            s.chapters, s.rag_chunks,
            (SELECT COUNT(*) FROM ssot_brochure.chapters) as actual_chapters,
            (SELECT COUNT(*) FROM ssot_brochure.embeddings) as actual_rag_chunks
        FROM ssot_brochure.ssot_status s
    """)
    ss = cur.fetchone()
    if ss:
        schapters, srag, actual_sch, actual_srag = ss
        ss_ok = (schapters == actual_sch and srag == actual_srag)
        status = "PASS" if ss_ok else "FAIL"
        if not ss_ok:
            issues.append(f"ssot_brochure.ssot_status: chapters={schapters}/{actual_sch}, rag_chunks={srag}/{actual_srag}")
        print(f"  ssot_brochure.ssot_status: chapters={schapters}/{actual_sch}, rag_chunks={srag}/{actual_srag} [{status}]")

    print()

    # 2. Missing Embeddings
    print("[2] Missing Embeddings Audit")
    print("-" * 40)
    cur.execute("""
        SELECT c.slug, c.title, c.word_count
        FROM ssot.chapters c
        LEFT JOIN ssot.embeddings e ON c.slug = e.chapter_slug
        WHERE e.id IS NULL
    """)
    missing_chapters = cur.fetchall()
    if missing_chapters:
        issues.append(f"{len(missing_chapters)} chapters without embeddings")
        for slug, title, wc in missing_chapters:
            print(f"  FAIL: chapter '{slug}' ({title}, {wc} words) has no embeddings")
    else:
        print("  PASS: All chapters have embeddings")

    cur.execute("""
        SELECT id, agent_id, memory_kind, title
        FROM ssot.agent_memory
        WHERE embedding IS NULL
    """)
    missing_memories = cur.fetchall()
    if missing_memories:
        issues.append(f"{len(missing_memories)} agent_memory rows without embeddings")
        for mid, agent_id, kind, title in missing_memories:
            print(f"  FAIL: agent_memory id={mid} (agent={agent_id}, kind={kind}, title={title}) has no embedding")
    else:
        print("  PASS: All agent_memory rows have embeddings")

    print()

    # 3. Chunk Content Errors
    print("[3] Chunk Content Errors Audit")
    print("-" * 40)
    cur.execute("""
        SELECT
            COUNT(*) FILTER (WHERE chunk_text = '' OR chunk_text IS NULL) as empty_chunks,
            COUNT(*) FILTER (WHERE embedding IS NULL) as null_embeddings,
            COUNT(*) FILTER (WHERE anchor IS NULL OR anchor != 'phi^2 + phi^-2 = 3') as bad_anchors,
            COUNT(*) as total
        FROM ssot.embeddings
    """)
    empty, null_emb, bad_anchors, total = cur.fetchone()
    if empty > 0:
        issues.append(f"{empty} empty chunks in ssot.embeddings")
    if null_emb > 0:
        issues.append(f"{null_emb} null embeddings in ssot.embeddings")
    if bad_anchors > 0:
        issues.append(f"{bad_anchors} bad anchors in ssot.embeddings")
    print(f"  empty_chunks={empty}, null_embeddings={null_emb}, bad_anchors={bad_anchors}, total={total}")
    print(f"  [{'PASS' if (empty == 0 and null_emb == 0 and bad_anchors == 0) else 'FAIL'}]")

    # Duplicate chunks
    cur.execute("""
        SELECT chapter_slug, chunk_index, COUNT(*) as dup_count
        FROM ssot.embeddings
        GROUP BY chapter_slug, chunk_index
        HAVING COUNT(*) > 1
        ORDER BY dup_count DESC
    """)
    dups = cur.fetchall()
    if dups:
        issues.append(f"{len(dups)} duplicate chunk indices in ssot.embeddings")
        for slug, idx, count in dups[:5]:
            print(f"  FAIL: {slug}[{idx}] has {count} duplicates")
        if len(dups) > 5:
            print(f"  ... and {len(dups) - 5} more")
    else:
        print("  PASS: No duplicate chunk indices")

    # Same checks for ssot_brochure
    cur.execute("""
        SELECT
            COUNT(*) FILTER (WHERE chunk_text = '' OR chunk_text IS NULL) as empty_chunks,
            COUNT(*) FILTER (WHERE embedding IS NULL) as null_embeddings,
            COUNT(*) FILTER (WHERE anchor IS NULL OR anchor != 'phi^2 + phi^-2 = 3') as bad_anchors,
            COUNT(*) as total
        FROM ssot_brochure.embeddings
    """)
    bempty, bnull, bbad, btotal = cur.fetchone()
    if bempty > 0:
        issues.append(f"{bempty} empty chunks in ssot_brochure.embeddings")
    if bnull > 0:
        issues.append(f"{bnull} null embeddings in ssot_brochure.embeddings")
    if bbad > 0:
        issues.append(f"{bbad} bad anchors in ssot_brochure.embeddings")
    print(f"  ssot_brochure: empty={bempty}, null={bnull}, bad_anchors={bbad}, total={btotal}")
    print(f"  [{'PASS' if (bempty == 0 and bnull == 0 and bbad == 0) else 'FAIL'}]")

    print()

    # 4. Schema Mismatch (ssot vs ssot_brochure)
    print("[4] Schema Mismatch Audit (ssot vs ssot_brochure)")
    print("-" * 40)
    cur.execute("""
        SELECT s.slug, s.title
        FROM ssot.chapters s
        LEFT JOIN ssot_brochure.chapters b ON s.slug = b.slug
        WHERE b.slug IS NULL
    """)
    only_ssot = cur.fetchall()
    cur.execute("""
        SELECT b.slug, b.title
        FROM ssot_brochure.chapters b
        LEFT JOIN ssot.chapters s ON b.slug = s.slug
        WHERE s.slug IS NULL
    """)
    only_brochure = cur.fetchall()
    cur.execute("""
        SELECT s.slug, s.title, s.word_count as ssot_wc, b.word_count as bro_wc
        FROM ssot.chapters s
        JOIN ssot_brochure.chapters b ON s.slug = b.slug
        WHERE s.word_count != b.word_count
    """)
    wc_diff = cur.fetchall()

    if only_ssot:
        print(f"  INFO: {len(only_ssot)} chapters only in ssot (expected — brochure is a subset)")
        for slug, title in only_ssot[:3]:
            print(f"    - {slug}: {title}")
        if len(only_ssot) > 3:
            print(f"    ... and {len(only_ssot) - 3} more")
    else:
        print("  PASS: No chapters only in ssot")

    if only_brochure:
        issues.append(f"{len(only_brochure)} chapters only in ssot_brochure (missing from ssot)")
        for slug, title in only_brochure:
            print(f"  FAIL: {slug} exists only in ssot_brochure but not in ssot: {title}")
    else:
        print("  PASS: No chapters only in ssot_brochure")

    if wc_diff:
        issues.append(f"{len(wc_diff)} chapters with word_count mismatch between ssot and ssot_brochure")
        for slug, title, swc, bwc in wc_diff[:5]:
            print(f"  FAIL: {slug} word_count mismatch: ssot={swc}, brochure={bwc}")
        if len(wc_diff) > 5:
            print(f"  ... and {len(wc_diff) - 5} more")
    else:
        print("  PASS: No word_count mismatches")

    print()
    print("=" * 60)
    if issues:
        print(f"RESULT: FAIL — {len(issues)} issue(s) found:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    else:
        print("RESULT: PASS — No anomalies detected. Brain is healthy.")
    print("=" * 60)

    cur.close()
    return len(issues)


def main():
    parser = argparse.ArgumentParser(description="Trinity S3AI Brain Health Audit")
    parser.add_argument("--url", help="Database connection string (or set TRINITY_DATABASE_URL env var)")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix healable issues (status mismatches only)")
    args = parser.parse_args()

    conn = get_connection(args.url)
    issue_count = run_audit(conn)

    if args.fix and issue_count > 0:
        print()
        print("[FIX MODE] Attempting to heal status mismatches...")
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE ssot.brain_status SET
                    phd_rows = (SELECT COUNT(*) FROM ssot.chapters),
                    phd_chunks = (SELECT COUNT(*) FROM ssot.embeddings),
                    phd_embedded = (SELECT COUNT(*) FROM ssot.embeddings WHERE embedding IS NOT NULL),
                    memories_rows = (SELECT COUNT(*) FROM ssot.agent_memory),
                    memories_embedded = (SELECT COUNT(*) FROM ssot.agent_memory WHERE embedding IS NOT NULL);
            """)
            cur.execute("""
                UPDATE ssot.rag_status SET
                    total_chunks = (SELECT COUNT(*) FROM ssot.embeddings),
                    embedded_chunks = (SELECT COUNT(*) FROM ssot.embeddings WHERE embedding IS NOT NULL),
                    coverage_pct = 100.0 * (SELECT COUNT(*) FROM ssot.embeddings WHERE embedding IS NOT NULL) / NULLIF((SELECT COUNT(*) FROM ssot.embeddings), 0);
            """)
            cur.execute("""
                UPDATE ssot_brochure.rag_status SET
                    total_chunks = (SELECT COUNT(*) FROM ssot_brochure.embeddings),
                    embedded_chunks = (SELECT COUNT(*) FROM ssot_brochure.embeddings WHERE embedding IS NOT NULL),
                    coverage_pct = 100.0 * (SELECT COUNT(*) FROM ssot_brochure.embeddings WHERE embedding IS NOT NULL) / NULLIF((SELECT COUNT(*) FROM ssot_brochure.embeddings), 0);
            """)
            cur.execute("""
                UPDATE ssot_brochure.ssot_status SET
                    chapters = (SELECT COUNT(*) FROM ssot_brochure.chapters),
                    rag_chunks = (SELECT COUNT(*) FROM ssot_brochure.embeddings);
            """)
            conn.commit()
            print("Status tables healed successfully.")
            print("Re-running audit...")
            print()
            issue_count = run_audit(conn)
        except Exception as e:
            conn.rollback()
            print(f"FIX FAILED: {e}")
        finally:
            cur.close()

    conn.close()
    sys.exit(0 if issue_count == 0 else 1)


if __name__ == "__main__":
    main()
