import Database from 'better-sqlite3'
import { embed, cosineSimilarity } from './embeddings.js'
import { getAllChunks } from './db.js'
import type { SearchResult } from './types.js'

export interface SearchOptions {
    libraryId: string
    query: string
    maxResults?: number     // default: 10
    ftsMinResults?: number  // min FTS hits before fallback (default: 3)
}

// ---------------------------------------------------------------------------
// FTS5 query sanitisation
// ---------------------------------------------------------------------------

const FTS5_SPECIAL = /[():*"^]/

function sanitizeFtsQuery(query: string): string {
    if (FTS5_SPECIAL.test(query)) {
        // Escape internal double-quotes by doubling them, then wrap in quotes
        // for a phrase search that avoids syntax errors.
        const escaped = query.replace(/"/g, '""')
        return `"${escaped}"`
    }
    return query
}

// ---------------------------------------------------------------------------
// hybridSearch
// ---------------------------------------------------------------------------

export async function hybridSearch(
    db: Database.Database,
    options: SearchOptions
): Promise<SearchResult[]> {
    const { libraryId, query } = options
    const maxResults = options.maxResults ?? 10
    const ftsMinResults = options.ftsMinResults ?? 3

    // --- FTS5 attempt ---
    let ftsRows: Array<{ id: number; title: string; body: string; library_id: string; score: number }> = []
    let ftsSucceeded = false

    try {
        const ftsQuery = sanitizeFtsQuery(query)
        const stmt = db.prepare<[string, string]>(`
            SELECT c.id, c.title, c.body, c.library_id,
                   bm25(chunks_fts, 5.0, 1.0) as score
            FROM chunks c
            JOIN chunks_fts ON chunks_fts.rowid = c.id
            WHERE chunks_fts MATCH ?
              AND c.library_id = ?
            ORDER BY bm25(chunks_fts, 5.0, 1.0)
            LIMIT 20
        `)
        ftsRows = stmt.all(ftsQuery, libraryId) as typeof ftsRows
        ftsSucceeded = true
    } catch (_err) {
        // Bad FTS query syntax — fall through to semantic search
        ftsSucceeded = false
    }

    if (ftsSucceeded && ftsRows.length >= ftsMinResults) {
        return ftsRows.slice(0, maxResults).map((row) => ({
            id: row.id,
            title: row.title,
            body: row.body,
            score: Math.abs(row.score),
            source: 'fts' as const,
        }))
    }

    // --- Semantic fallback ---
    const queryVec = await embed(query)
    const allChunks = getAllChunks(db, libraryId)

    const scored: Array<{ chunk: typeof allChunks[number]; similarity: number }> = []

    for (const chunk of allChunks) {
        if (!chunk.embedding) continue
        const vec: number[] = JSON.parse(chunk.embedding)
        const similarity = cosineSimilarity(queryVec, vec)
        scored.push({ chunk, similarity })
    }

    scored.sort((a, b) => b.similarity - a.similarity)

    return scored.slice(0, maxResults).map((entry) => ({
        id: entry.chunk.id as number,
        title: entry.chunk.title,
        body: entry.chunk.body,
        score: entry.similarity,
        source: 'semantic' as const,
    }))
}

// ---------------------------------------------------------------------------
// formatResults
// ---------------------------------------------------------------------------

export function formatResults(results: SearchResult[]): string {
    return results
        .map((r) => `## ${r.title}\n\n${r.body}`)
        .join('\n\n---\n\n')
}
