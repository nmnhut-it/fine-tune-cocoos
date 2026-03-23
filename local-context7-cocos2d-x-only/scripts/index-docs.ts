import { readFileSync, readdirSync, statSync } from 'fs'
import { join, extname, relative } from 'path'
import { initDb, clearLibrary, insertChunksBatch, upsertLibrary } from '../src/db.js'
import { embedBatch } from '../src/embeddings.js'
import type { ChunkRow, LibraryConfig } from '../src/types.js'

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const config: LibraryConfig = JSON.parse(
    readFileSync('./docs/library.json', 'utf-8')
)

// ---------------------------------------------------------------------------
// Chunk types
// ---------------------------------------------------------------------------

interface RawChunk {
    title: string
    body: string
    sourceFile: string
}

// ---------------------------------------------------------------------------
// Chunking helpers
// ---------------------------------------------------------------------------

function mergeAndSplit(chunks: RawChunk[]): RawChunk[] {
    // Pass 1: merge short chunks (body < 50 chars) into next chunk
    const merged: RawChunk[] = []
    let pending: RawChunk | null = null

    for (const chunk of chunks) {
        if (pending !== null) {
            if (pending.body.trim().length < 50) {
                // Merge pending into current: append body, keep pending title
                pending = {
                    title: pending.title,
                    body: pending.body + '\n' + chunk.body,
                    sourceFile: pending.sourceFile,
                }
                continue
            } else {
                merged.push(pending)
                pending = chunk
            }
        } else {
            pending = chunk
        }
    }
    if (pending !== null) {
        merged.push(pending)
    }

    // Pass 2: split large chunks (body > 2000 chars) by double newline
    const result: RawChunk[] = []
    for (const chunk of merged) {
        if (chunk.body.length > 2000) {
            const parts = chunk.body.split(/\n\n+/)
            for (const part of parts) {
                if (part.trim().length === 0) continue
                result.push({
                    title: chunk.title,
                    body: part,
                    sourceFile: chunk.sourceFile,
                })
            }
        } else {
            result.push(chunk)
        }
    }

    return result
}

function chunkMarkdown(content: string, sourceFile: string): RawChunk[] {
    const lines = content.split('\n')
    const raw: RawChunk[] = []

    let currentTitle = ''
    let parentTitle = ''
    let currentDepth = 0
    let bodyLines: string[] = []

    function finalizeChunk() {
        const body = bodyLines.join('\n').trim()
        if (currentTitle || body) {
            raw.push({ title: currentTitle, body, sourceFile })
        }
        bodyLines = []
    }

    for (const line of lines) {
        const headingMatch = line.match(/^(#{1,6})\s+(.+)/)
        if (headingMatch) {
            finalizeChunk()
            const depth = headingMatch[1].length
            const headingText = headingMatch[2].trim()

            if (depth === 1) {
                parentTitle = headingText
                currentDepth = 1
                currentTitle = headingText
            } else if (depth > currentDepth || depth > 1) {
                if (parentTitle && depth > 1) {
                    currentTitle = `${parentTitle} > ${headingText}`
                } else {
                    currentTitle = headingText
                }
                // Update parent tracking for deeper nesting
                if (depth <= 2) {
                    parentTitle = headingText
                }
                currentDepth = depth
            } else {
                currentTitle = headingText
                currentDepth = depth
                if (depth === 1) {
                    parentTitle = headingText
                }
            }
        } else {
            bodyLines.push(line)
        }
    }
    finalizeChunk()

    return mergeAndSplit(raw)
}

function chunkText(content: string, sourceFile: string): RawChunk[] {
    const paragraphs = content.split(/\n\n+/)
    const raw: RawChunk[] = paragraphs
        .map((para) => {
            const trimmed = para.trim()
            if (!trimmed) return null
            const firstLine = trimmed.split('\n')[0].slice(0, 80)
            return {
                title: firstLine,
                body: trimmed,
                sourceFile,
            }
        })
        .filter((c): c is RawChunk => c !== null)

    return mergeAndSplit(raw)
}

// ---------------------------------------------------------------------------
// File scanning
// ---------------------------------------------------------------------------

function scanDir(dir: string): string[] {
    const files: string[] = []
    for (const entry of readdirSync(dir)) {
        if (entry === 'library.json' || entry === '.gitkeep') continue
        const fullPath = join(dir, entry)
        const stat = statSync(fullPath)
        if (stat.isDirectory()) {
            files.push(...scanDir(fullPath))
        } else {
            const ext = extname(entry).toLowerCase()
            if (ext === '.md' || ext === '.txt') {
                files.push(fullPath)
            }
        }
    }
    return files
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
    const db = initDb(config.db_path)
    clearLibrary(db, config.library_id)
    console.error(`[index] Library "${config.library_id}" cleared.`)

    const files = scanDir(config.docs_dir)
    console.error(`[index] Found ${files.length} file(s) to index.`)

    let totalChunks = 0

    for (const filePath of files) {
        const relPath = relative(config.docs_dir, filePath)
        const ext = extname(filePath).toLowerCase()
        const content = readFileSync(filePath, 'utf-8')

        let rawChunks: RawChunk[]
        if (ext === '.md') {
            rawChunks = chunkMarkdown(content, relPath)
        } else {
            rawChunks = chunkText(content, relPath)
        }

        if (rawChunks.length === 0) {
            console.error(`[index] ${relPath}: 0 chunks, skipping.`)
            continue
        }

        // Embed all chunks in one batch
        const texts = rawChunks.map((c) => c.title + '\n' + c.body)
        const embeddings = await embedBatch(texts)

        const chunkRows: ChunkRow[] = rawChunks.map((c, i) => ({
            library_id: config.library_id,
            source_file: c.sourceFile,
            title: c.title,
            body: c.body,
            embedding: JSON.stringify(embeddings[i]),
        }))

        insertChunksBatch(db, chunkRows)
        totalChunks += chunkRows.length
        console.error(`[index] ${relPath}: ${chunkRows.length} chunk(s) indexed.`)
    }

    upsertLibrary(db, {
        id: config.library_id,
        name: config.library_name,
        description: config.description,
        version: config.version,
    })

    console.error(
        `[index] Done. Library "${config.library_id}" — ${files.length} file(s), ${totalChunks} chunk(s) total.`
    )
}

main().catch((err) => {
    console.error('[index] Fatal error:', err)
    process.exit(1)
})
