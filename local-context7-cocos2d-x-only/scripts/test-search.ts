/**
 * Quick test script — bypass MCP layer, call search functions directly.
 * Usage:
 *   npm run test:search
 *   npm run test:search -- --query "your query here" --library fetchkit
 */

import { initDb, listLibraries, getLibraryChunkCount } from '../src/db.js'
import { hybridSearch, formatResults } from '../src/search.js'
import { resolve } from 'path'
import { readFileSync } from 'fs'
import type { LibraryConfig } from '../src/types.js'

// --- parse CLI args ---
const args = process.argv.slice(2)
const get = (flag: string, fallback?: string) => {
  const i = args.indexOf(flag)
  return i !== -1 ? args[i + 1] : fallback
}

const config: LibraryConfig = JSON.parse(
  readFileSync(resolve('docs/library.json'), 'utf-8')
)

const query     = get('--query',   'how to make a request')
const libraryId = get('--library', config.library_id)
const maxResults = Number(get('--max', '5'))

// --- init ---
const db = initDb(config.db_path)

// --- show indexed state ---
const libs = listLibraries(db)
console.error('\n=== Indexed libraries ===')
if (libs.length === 0) {
  console.error('  (none) — run `npm run index` first')
} else {
  for (const lib of libs) {
    console.error(`  [${lib.id}] ${lib.name} — ${lib.chunk_count} chunks`)
  }
}

// --- run search ---
console.error(`\n=== Search ===`)
console.error(`  library : ${libraryId}`)
console.error(`  query   : "${query}"`)
console.error(`  maxResults: ${maxResults}`)
console.error('')

const results = await hybridSearch(db, { libraryId, query, maxResults })

if (results.length === 0) {
  console.error('No results found.')
  process.exit(0)
}

console.error(`Found ${results.length} result(s) via ${results[0].source === 'fts' ? 'FTS5 keyword' : 'semantic'} search\n`)

// --- print results ---
console.log(formatResults(results))

// --- debug: show scores ---
console.error('\n=== Scores ===')
for (const r of results) {
  console.error(`  [${r.source}] score=${r.score.toFixed(4)}  "${r.title.slice(0, 60)}"`)
}
