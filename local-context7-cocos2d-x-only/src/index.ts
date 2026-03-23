import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { z } from 'zod'
import { readFileSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'
import { initDb, listLibraries, getLibraryChunkCount } from './db.js'
import { hybridSearch, formatResults } from './search.js'
import type { LibraryConfig } from './types.js'

// ---------------------------------------------------------------------------
// Bootstrap
// ---------------------------------------------------------------------------

const __dirname = dirname(fileURLToPath(import.meta.url))
const projectRoot = resolve(__dirname, '..')

const configPath = resolve(projectRoot, 'docs/library.json')
const config: LibraryConfig = JSON.parse(readFileSync(configPath, 'utf-8'))

const db = initDb(resolve(projectRoot, config.db_path))

const server = new McpServer({
    name: 'context7-local',
    version: '1.0.0',
})

// ---------------------------------------------------------------------------
// Tool: resolve-library-id
// ---------------------------------------------------------------------------

server.tool(
    'resolve-library-id',
    'Search for available libraries by name and return their IDs.',
    {
        libraryName: z.string().describe('Library name to search for, e.g. "cocos2dx" or "Cocos2d-x"'),
    },
    async ({ libraryName }) => {
        const allLibs = listLibraries(db)
        const needle = libraryName.toLowerCase()

        let matched = allLibs.filter(
            (lib) =>
                lib.id.toLowerCase().includes(needle) ||
                lib.name.toLowerCase().includes(needle)
        )

        if (matched.length === 0) {
            matched = allLibs
        }

        const lines: string[] = ['Available Libraries:', '']

        for (const lib of matched) {
            lines.push(`- Library ID: /${lib.id}`)
            lines.push(`  Name: ${lib.name}`)
            if (lib.description) {
                lines.push(`  Description: ${lib.description}`)
            }
            if (lib.version) {
                lines.push(`  Version: ${lib.version}`)
            }
            lines.push(`  Chunks: ${lib.chunk_count}`)
            lines.push('')
        }

        lines.push('Use the library ID (starting with /) with get-library-docs to retrieve documentation.')

        const formattedText = lines.join('\n')

        return { content: [{ type: 'text', text: formattedText }] }
    }
)

// ---------------------------------------------------------------------------
// Tool: get-library-docs
// ---------------------------------------------------------------------------

server.tool(
    'get-library-docs',
    'Retrieve documentation chunks from a library using semantic/FTS search.',
    {
        libraryId: z.string().describe(
            "Exact library ID from resolve-library-id, e.g. '/cocos2dx'"
        ),
        query: z.string().describe(
            'Specific question or topic to find in the documentation'
        ),
        tokens: z.number().optional().describe(
            'Approximate maximum tokens to return (default: 10000)'
        ),
    },
    async ({ libraryId, query, tokens }) => {
        const id = libraryId.replace(/^\//, '')
        const maxTokens = tokens ?? 10000
        const maxChars = maxTokens * 4

        const results = await hybridSearch(db, { libraryId: id, query, maxResults: 15 })

        if (results.length === 0) {
            return {
                content: [
                    {
                        type: 'text',
                        text: 'No documentation found for query: "' + query + '". Try resolve-library-id to check available libraries.',
                    },
                ],
            }
        }

        let text = formatResults(results)

        if (text.length > maxChars) {
            text = text.slice(0, maxChars) + '\n\n[... truncated ...]'
        }

        return { content: [{ type: 'text', text }] }
    }
)

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
    const transport = new StdioServerTransport()
    await server.connect(transport)
    console.error('[context7-local] MCP server started')
}

main().catch((err) => {
    console.error('[context7-local] Fatal error:', err)
    process.exit(1)
})
