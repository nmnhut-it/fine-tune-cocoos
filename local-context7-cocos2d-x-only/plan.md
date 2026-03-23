# Local Context7 MCP Server — Implementation Plan

## Progress Checklist

- [x] **Phase 1** — Project scaffold & config
- [x] **Phase 2** — Database layer (SQLite + FTS5)
- [x] **Phase 3** — Embedding layer (local model)
- [x] **Phase 4** — Indexer CLI script
- [x] **Phase 5** — Hybrid search engine
- [x] **Phase 6** — MCP server (tools)
- [ ] **Phase 7** — Build & Claude Code registration ← `npm run build` ✓, cần register MCP

---

## Phase 1 — Project Scaffold & Config

### Files to create
- `package.json`
- `tsconfig.json`
- `.gitignore`
- `src/` directory
- `docs/` directory (empty, user places doc files here)
- `data/` directory (SQLite output)
- `scripts/` directory

### package.json

```json
{
  "name": "context7-local",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "build": "tsc",
    "dev": "tsx src/index.ts",
    "index": "tsx scripts/index-docs.ts",
    "index:watch": "tsx watch scripts/index-docs.ts"
  },
  "dependencies": {
    "@huggingface/transformers": "^3.x",
    "@modelcontextprotocol/sdk": "^1.x",
    "better-sqlite3": "^9.x",
    "zod": "^3.x"
  },
  "devDependencies": {
    "@types/better-sqlite3": "^7.x",
    "@types/node": "^20.x",
    "tsx": "^4.x",
    "typescript": "^5.x"
  }
}
```

### tsconfig.json targets

- `target`: ES2022
- `module`: Node16
- `moduleResolution`: Node16
- `outDir`: `./build`
- `rootDir`: `./src`
- `strict`: true

### Checklist Phase 1

- [ ] `package.json` created với đủ dependencies
- [ ] `tsconfig.json` created
- [ ] `.gitignore` created (node_modules, data/*.sqlite, build/)
- [ ] `npm install` thành công
- [ ] Thư mục `src/`, `docs/`, `data/`, `scripts/` tồn tại

---

## Phase 2 — Database Layer

### File: `src/db.ts`

**Mục đích:** Khởi tạo SQLite database, tạo schema, export các prepared statements.

### Schema chi tiết

```sql
-- Bảng chính lưu doc chunks
CREATE TABLE IF NOT EXISTS chunks (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  library_id  TEXT    NOT NULL,       -- e.g. "cocos2dx"
  source_file TEXT    NOT NULL,       -- e.g. "docs/cocos2dx.md"
  title       TEXT    NOT NULL,       -- heading của section
  body        TEXT    NOT NULL,       -- nội dung section
  embedding   TEXT,                   -- JSON array số thực (float32[])
  created_at  INTEGER DEFAULT (unixepoch())
);

-- FTS5 virtual table cho keyword search
-- content= mode: FTS5 lấy dữ liệu từ bảng chunks, không duplicate
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
  title,
  body,
  tokenize = 'porter ascii',          -- porter stemming: "running" ~ "run"
  content  = 'chunks',
  content_rowid = 'id'
);

-- Triggers để sync FTS khi insert/update/delete chunks
CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
  INSERT INTO chunks_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
END;

CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
  INSERT INTO chunks_fts(chunks_fts, rowid, title, body)
    VALUES ('delete', old.id, old.title, old.body);
END;

CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
  INSERT INTO chunks_fts(chunks_fts, rowid, title, body)
    VALUES ('delete', old.id, old.title, old.body);
  INSERT INTO chunks_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
END;

-- Bảng metadata libraries
CREATE TABLE IF NOT EXISTS libraries (
  id          TEXT PRIMARY KEY,       -- e.g. "cocos2dx"
  name        TEXT NOT NULL,          -- e.g. "Cocos2d-x"
  description TEXT,
  version     TEXT,
  indexed_at  INTEGER DEFAULT (unixepoch())
);
```

### Exported functions từ `src/db.ts`

```typescript
// Khởi tạo DB, chạy migrations
export function initDb(dbPath: string): Database.Database

// Xóa toàn bộ chunks của 1 library (trước khi re-index)
export function clearLibrary(db: Database.Database, libraryId: string): void

// Insert 1 chunk (embedding optional, thêm sau)
export function insertChunk(db: Database.Database, chunk: ChunkRow): number

// Upsert library metadata
export function upsertLibrary(db: Database.Database, lib: LibraryRow): void

// Lấy tất cả chunks của library (cho semantic search)
export function getAllChunks(db: Database.Database, libraryId: string): ChunkRow[]

// Lấy danh sách libraries
export function listLibraries(db: Database.Database): LibraryRow[]
```

### Types (`src/types.ts`)

```typescript
export interface ChunkRow {
  id?: number
  library_id: string
  source_file: string
  title: string
  body: string
  embedding?: string   // JSON stringified float32[]
}

export interface LibraryRow {
  id: string
  name: string
  description?: string
  version?: string
}

export interface SearchResult {
  id: number
  title: string
  body: string
  score: number
  source: 'fts' | 'semantic'
}
```

### Checklist Phase 2

- [ ] `src/types.ts` created với đủ interfaces
- [ ] `src/db.ts` created với `initDb()` tạo đúng schema
- [ ] FTS5 triggers hoạt động (test: insert chunk → FTS tìm được)
- [ ] Tất cả exported functions hoạt động đúng

---

## Phase 3 — Embedding Layer

### File: `src/embeddings.ts`

**Mục đích:** Wrapper singleton cho `@huggingface/transformers`, lazy-load model lần đầu dùng, expose `embed()` function.

### Model sử dụng

- `Xenova/all-MiniLM-L6-v2`
- Kích thước: ~23 MB (ONNX quantized int8)
- Output dimension: 384
- Download tự động lần đầu, cache vào `~/.cache/huggingface/` (hoặc `data/models/`)

### API của `src/embeddings.ts`

```typescript
// Load model lần đầu (lazy), sau đó cache trong process
export async function getEmbedder(): Promise<FeatureExtractionPipeline>

// Embed 1 đoạn text → float32 array 384 chiều
export async function embed(text: string): Promise<number[]>

// Embed nhiều đoạn text cùng lúc (batch, hiệu quả hơn)
export async function embedBatch(texts: string[]): Promise<number[][]>

// Tính cosine similarity giữa 2 normalized vectors (dot product)
export function cosineSimilarity(a: number[], b: number[]): number
```

### Lưu ý quan trọng

- Model phải load async, chỉ load 1 lần (singleton pattern)
- Cache model vào `data/models/` để tránh download lại khi dùng trên server nội bộ
- Khi index docs: batch embed tất cả chunks → lưu vào DB dưới dạng `JSON.stringify(array)`
- Khi search: embed query → load tất cả embeddings từ DB → sort by cosine similarity

### Checklist Phase 3

- [ ] `src/embeddings.ts` created
- [ ] Model load thành công lần đầu (download ~23MB)
- [ ] `embed("hello world")` trả về array 384 số
- [ ] `cosineSimilarity()` trả về đúng giá trị (1.0 với vector giống nhau)
- [ ] Model cache hoạt động (lần 2 không download lại)

---

## Phase 4 — Indexer CLI Script

### File: `scripts/index-docs.ts`

**Mục đích:** Đọc các file từ thư mục `docs/`, chunk content theo headings, embed từng chunk, lưu vào SQLite.

**Chạy bằng:** `npm run index`

### Chunking strategy

Chia file markdown thành các sections theo heading:

```
# Title          → chunk title = "Title"
content...       → chunk body = content đến heading tiếp theo

## Sub-section   → chunk title = "Title > Sub-section"
content...       → chunk body = content đến heading tiếp theo
```

**Rules:**
- Mỗi chunk = 1 section (heading + body)
- Nếu body quá ngắn (< 50 chars): merge với chunk tiếp theo
- Nếu body quá dài (> 2000 chars): split theo paragraph, mỗi phần giữ lại title
- File không phải markdown (`.txt`): chunk theo paragraph (2+ newlines)

### Config (đọc từ `docs/library.json` hoặc hardcode default)

```json
{
  "library_id": "cocos2dx",
  "library_name": "Cocos2d-x",
  "description": "Cocos2d-x game engine documentation",
  "version": "4.0",
  "docs_dir": "./docs",
  "db_path": "./data/context7.sqlite"
}
```

### Flow indexer

```
1. Đọc config từ docs/library.json (hoặc dùng default)
2. initDb(config.db_path)
3. clearLibrary(db, config.library_id)   ← xóa data cũ
4. Scan tất cả *.md, *.txt trong docs_dir
5. Với mỗi file:
   a. Parse → chunks[] (title + body)
   b. embedBatch([chunk.title + "\n" + chunk.body for chunk in chunks])
   c. insertChunk() cho mỗi chunk (kèm embedding)
6. upsertLibrary() với metadata
7. In summary: N files, M chunks indexed
```

### Checklist Phase 4

- [ ] `scripts/index-docs.ts` created
- [ ] `docs/library.json` example created
- [ ] Chunking markdown theo headings hoạt động đúng
- [ ] Chunking file .txt theo paragraph hoạt động
- [ ] Chunk quá ngắn được merge, quá dài được split
- [ ] Embedding được lưu vào DB (kiểm tra: `SELECT length(embedding) FROM chunks LIMIT 1`)
- [ ] `npm run index` chạy thành công với file test

---

## Phase 5 — Hybrid Search Engine

### File: `src/search.ts`

**Mục đích:** Thực hiện hybrid search: FTS5 trước, fallback semantic nếu kết quả không đủ.

### API

```typescript
export interface SearchOptions {
  libraryId: string
  query: string
  maxResults?: number       // default: 10
  ftsThreshold?: number     // min FTS results trước khi fallback (default: 3)
  semanticTopK?: number     // số kết quả semantic trả về (default: 10)
}

export async function hybridSearch(
  db: Database.Database,
  options: SearchOptions
): Promise<SearchResult[]>
```

### Logic chi tiết

```
1. Sanitize query (escape ký tự đặc biệt FTS5: " ' * : )
2. FTS5 search:
   SELECT id, title, body, rank
   FROM chunks_fts
   WHERE chunks_fts MATCH ? AND library_id_filter
   ORDER BY bm25(chunks_fts, 5.0, 1.0)  -- title weighted 5x
   LIMIT 20

   Lưu ý: FTS5 content= mode cần JOIN với chunks để lấy library_id filter:
   SELECT c.id, c.title, c.body, c.library_id
   FROM chunks c
   JOIN chunks_fts f ON f.rowid = c.id
   WHERE chunks_fts MATCH ? AND c.library_id = ?
   ORDER BY rank
   LIMIT 20

3. Nếu FTS trả về >= ftsThreshold results → return top maxResults
4. Nếu FTS < ftsThreshold:
   a. embed(query) → queryVec
   b. getAllChunks(db, libraryId) → chunks với embedding
   c. Tính cosine similarity mỗi chunk
   d. Sort descending, lấy top semanticTopK
   e. Return với source='semantic'

5. Format kết quả thành markdown text để trả về MCP
```

### Format output

```markdown
## {title}

{body}

---
```

Mỗi result cách nhau bằng `---`, tối đa `maxResults` chunks.

### Checklist Phase 5

- [ ] `src/search.ts` created
- [ ] FTS5 query sanitization hoạt động (không crash với ký tự đặc biệt)
- [ ] FTS5 search trả về kết quả đúng library
- [ ] Semantic fallback hoạt động khi FTS < threshold
- [ ] Kết quả được format đúng markdown
- [ ] Test: query chính xác → FTS wins; query mơ hồ → semantic wins

---

## Phase 6 — MCP Server

### File: `src/index.ts`

**Mục đích:** Entry point MCP server, expose 2 tools tương thích Context7.

### Tools

#### Tool 1: `resolve-library-id`

```typescript
// Input
{
  libraryName: z.string().describe("Library name to search for")
}

// Logic
// 1. listLibraries(db)
// 2. Filter/match theo libraryName (case-insensitive contains)
// 3. Format output text

// Output format
`Available Libraries:

- Library ID: /cocos2dx
  Name: Cocos2d-x
  Description: Cocos2d-x game engine documentation
  Version: 4.0
  Chunks: 234
`
```

#### Tool 2: `get-library-docs`

```typescript
// Input
{
  libraryId: z.string().describe(
    "Library ID returned by resolve-library-id, e.g. '/cocos2dx'"
  ),
  query: z.string().describe(
    "Specific question or topic to search for in the documentation"
  ),
  tokens: z.number().optional().describe(
    "Max tokens to return (approximate, default 10000)"
  )
}

// Logic
// 1. Normalize libraryId (strip leading "/")
// 2. hybridSearch(db, { libraryId, query, maxResults })
// 3. Concatenate formatted results
// 4. Truncate nếu vượt tokens limit (estimate: 1 token ≈ 4 chars)

// Output
// Plain text markdown của các chunks tìm được
```

### Server setup

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js"

const server = new McpServer({
  name: "context7-local",
  version: "1.0.0"
})

// NEVER use console.log() — corrupts stdio JSON-RPC stream
// Always use console.error() for logging
```

### Checklist Phase 6

- [ ] `src/index.ts` created
- [ ] `resolve-library-id` trả về danh sách libraries đúng format
- [ ] `get-library-docs` gọi hybridSearch và trả về text
- [ ] Tokens limit được apply đúng
- [ ] Server khởi động không có lỗi (`tsx src/index.ts`)
- [ ] Không dùng `console.log()` ở bất kỳ đâu

---

## Phase 7 — Build & Claude Code Registration

### Build

```bash
npm run build
# Output: build/index.js
```

### Register với Claude Code

```bash
# Scope local (chỉ máy này, project hiện tại)
claude mcp add --transport stdio context7-local -- node "F:/cocos2dx-context7/build/index.js"

# Verify
claude mcp list
```

### Config file tương đương (`.mcp.json` ở project root)

```json
{
  "mcpServers": {
    "context7-local": {
      "command": "node",
      "args": ["F:/cocos2dx-context7/build/index.js"]
    }
  }
}
```

### Smoke test

Sau khi đăng ký, trong Claude Code conversation:
1. "Use context7-local to find docs about [topic]"
2. Verify tool được gọi và trả về docs

### Checklist Phase 7

- [ ] `npm run build` thành công, không có TypeScript errors
- [ ] `build/index.js` tồn tại
- [ ] `claude mcp add` thành công
- [ ] `claude mcp list` hiển thị `context7-local`
- [ ] Smoke test: tool được gọi từ Claude Code và trả về kết quả

---

## Notes

### Thêm library mới sau này

1. Tạo thư mục `docs-{libname}/` hoặc thêm config mới
2. Sửa `docs/library.json` với library mới
3. `npm run index`

### Deploy lên server nội bộ

1. Copy toàn bộ project lên server
2. `npm install && npm run build`
3. Chạy như HTTP MCP server (thêm `--transport http` flag sau)
4. Các máy khác dùng `claude mcp add --transport http context7-local http://server:PORT/mcp`

### Cấu trúc thư mục cuối cùng

```
F:/cocos2dx-context7/
├── build/                  ← compiled JS (gitignored)
│   └── index.js
├── data/                   ← gitignored
│   ├── context7.sqlite
│   └── models/             ← HuggingFace model cache
├── docs/                   ← USER PLACES DOC FILES HERE
│   ├── library.json        ← library metadata config
│   └── cocos2dx.md         ← (example)
├── scripts/
│   └── index-docs.ts
├── src/
│   ├── index.ts            ← MCP server entry point
│   ├── db.ts               ← database layer
│   ├── embeddings.ts       ← local embedding model
│   ├── search.ts           ← hybrid search
│   └── types.ts            ← TypeScript types
├── .gitignore
├── package.json
├── tsconfig.json
└── plan.md                 ← this file
```
