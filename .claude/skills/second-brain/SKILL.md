---
name: second-brain
description: Query the Trinity S3AI second brain (RAG) via the trios-mcp-rag MCP server — chapter search, claim status, honest counters, PDF pipeline
---

# /second-brain

Query the Trinity S3AI second brain through the dedicated `trios-mcp-rag` MCP server.

## MCP Server

- **Name:** `trios-mcp-rag`
- **Binary:** `/Users/playra/trios-mcp-rag/target/release/trios-mcp-rag`
- **Database:** Railway PostgreSQL (`ssot_brochure.chapters` — 80 chapters, 58K words)
- **Env:** `DATABASE_URL` (set in `~/.zshenv`)

## Available Tools

| Tool | Purpose |
|------|---------|
| `search_chapters` | Full-text search across all 80 GOLDEN CHAIN chapters |
| `get_chapter` | Fetch full chapter content by slug |
| `list_chapters` | List all chapter slugs with metadata |
| `forbidden_audit` | Scan for policy violations (prohibited terms) |
| `build_cover` | Generate LaTeX titlepage |
| `build_pdf` | Run SSOT→Markdown→pandoc→tectonic→PDF pipeline (dry-run by default) |
| `build_book` | Extended PDF pipeline with TOC and book-mode |
| `get_claim_status` | Search chapters for claim-status markers |
| `list_claims` | Scan all chapters for claim-status vocabulary |
| `get_honest_counters` | Return audited trinity-s3ai proof counters |
| `preview_chapter_update` | Dry-run: show SQL diff for proposed chapter update |
| `backup_ssot` | Create timestamped backup table (requires confirm=true) |

## Usage Patterns

### Search chapters for a topic
```
Use MCP tool trios-mcp-rag.search_chapters with query="boundary theorems"
```

### Get full chapter
```
Use MCP tool trios-mcp-rag.get_chapter with slug="bt-1-obstruction"
```

### List all claims with status
```
Use MCP tool trios-mcp-rag.list_claims
```

### Get honest counters
```
Use MCP tool trios-mcp-rag.get_honest_counters
```

### Build PDF (dry-run)
```
Use MCP tool trios-mcp-rag.build_pdf with dry_run=true
```

## Notes

- The `trios-mcp-rag` server connects to `ssot_brochure.chapters` (publication subset).
- For raw SQL access to the full database (ssot schema, scarab tables, BPB samples), use the `trinity-postgres` MCP server (generic postgres).
- All write operations (backup_ssot, build_pdf with dry_run=false) require explicit confirmation.
- The server follows AGENTS.md safety rules: read-only by default, backup-first for writes.
