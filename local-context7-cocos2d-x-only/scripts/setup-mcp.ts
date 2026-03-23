import { execFileSync } from 'child_process';
import { existsSync } from 'fs';
import {
  dirname,
  join,
  resolve,
} from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const MCP_NAME = 'context7-cocos'
const PROJECT_ROOT = resolve(__dirname, '..')
const BUILD_ENTRY = join(PROJECT_ROOT, 'build', 'index.js').replace(/\\/g, '/')

// ─── helpers ────────────────────────────────────────────────────────────────

function log(msg: string) { console.error(msg) }

// ─── main ────────────────────────────────────────────────────────────────────

const args = process.argv.slice(2)
const removeOnly = args.includes('-r') || args.includes('--remove')

if (removeOnly) {
    log(`\n🗑️   Remove: ${MCP_NAME}`)
    try {
        execFileSync('claude', ['mcp', 'remove', MCP_NAME, '--scope', 'user'], { stdio: 'inherit' })
        log(`\n✅  Removed "${MCP_NAME}" (user scope) — restart Claude Code to apply\n`)
    } catch {
        log(`\n⚠️   "${MCP_NAME}" was not registered (nothing to remove)\n`)
    }
    process.exit(0)
}

log(`\n🔧  Setup: ${MCP_NAME}`)
log(`   entry : ${BUILD_ENTRY}`)

// 1. Verify build exists
if (!existsSync(BUILD_ENTRY)) {
    log(`\n❌  build/index.js not found. Run first:\n\n    npm run build\n`)
    process.exit(1)
}

// 2. Register via claude mcp add (removes old entry first to update path)
try {
    execFileSync('claude', ['mcp', 'remove', MCP_NAME, '--scope', 'user'], { stdio: 'pipe' })
} catch {
    // ignore — server may not exist yet
}

const addCmd = `claude mcp add --scope user ${MCP_NAME} -- node ${BUILD_ENTRY}`

try {
    execFileSync('claude', [
        'mcp', 'add',
        '--scope', 'user',
        MCP_NAME,
        '--',
        'node', BUILD_ENTRY,
    ], { stdio: 'inherit' })
} catch (err) {
    log(`\n❌  Failed to register "${MCP_NAME}" automatically.`)
    log(`\n   Run manually in cmd:\n`)
    log(`   ${addCmd}\n`)
    process.exit(1)
}

log(`\n✅  Registered "${MCP_NAME}" (user scope) — restart Claude Code to apply`)
log(`\n   Verify with:  claude mcp list\n`)
