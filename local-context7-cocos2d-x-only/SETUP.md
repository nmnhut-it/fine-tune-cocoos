# Setup Guide — Local Context7 MCP

Hướng dẫn từng bước để setup, update docs và đăng ký MCP server với Claude Code.

---

## Tổng quan

```
docs/*.md  →  npm run index  →  data/context7.sqlite  →  npm run build  →  Claude Code
(raw docs)     (embed + index)   (vector DB)              (compile)         (MCP tool)
```

---

## 1. Cài dependencies (lần đầu)

```bash
npm install
```

> Lần đầu chạy indexer sẽ tự download embedding model ~23MB về `data/models/`.

---

## 2. Cấu hình library (`docs/library.json`)

File này khai báo metadata của library được index ví dụ:

```json
{
    "library_id": "cocos2dx-js",
    "library_name": "Cocos2d-x JavaScript API",
    "description": "Cocos2d-x v3.1 JavaScript/TypeScript API — cc, ccui, ccs, sp namespaces",
    "version": "3.1.0",
    "docs_dir": "./docs",
    "db_path": "./data/context7.sqlite"
}
```

- `library_id` — ID dùng khi tra cứu (ví dụ: `/cocos2dx-js`)
- `docs_dir` — thư mục chứa các file `.md` / `.txt`
- `db_path` — nơi lưu SQLite database

---

## 3. Thêm / cập nhật docs

Đặt file `.md` vào thư mục `docs/`. Mỗi file nên có cấu trúc:

```markdown
# Tên chủ đề (H1 — title của document, thành 1 chunk đầu)

Mô tả ngắn...

## Tên API / Class (H2 — mỗi heading = 1 chunk riêng)

Mô tả, parameters, example...

## Tên API khác

...
```

**Quy tắc chunking:**
- `#` H1 + nội dung trước `##` đầu tiên = chunk 1
- Mỗi `##` H2 = 1 chunk độc lập
- Chunk quá ngắn (<50 chars) được merge với chunk kế tiếp
- Chunk quá dài (>2000 chars) được split theo paragraph

---

## 4. Index docs vào database

```bash
npm run index
```

Output mẫu:
```
[index] Library: Cocos2d-x JavaScript API (cocos2dx-js)
[index] Scanning: F:/cocos2dx-context7/docs
[index] Found 14 files
[index] Indexing cocos2dx-actions.md ... 28 chunks
[index] Indexing cocos2dx-audio.md ... 3 chunks
...
[index] Done: 14 files, 187 chunks indexed
```

> Mỗi lần chạy `index` sẽ **xóa sạch data cũ** của library rồi index lại từ đầu. An toàn để chạy nhiều lần.

**Test search sau khi index:**
```bash
npm run test:search
```

---

## 5. Build server

```bash
npm run build
```

Output: `build/index.js`

> Cần build lại mỗi khi sửa code trong `src/`. Không cần build lại khi chỉ cập nhật docs (chỉ cần `npm run index`).

---

## 6. Đăng ký MCP với Claude Code

### Cách A — Claude Code CLI (recommended)

```bash
# Đăng ký scope local (chỉ project hiện tại)
claude mcp add --scope local context7-local node "F:/cocos2dx-context7/build/index.js"

# Hoặc scope global (tất cả project)
claude mcp add --scope user context7-local node "F:/cocos2dx-context7/build/index.js"

# Kiểm tra đã đăng ký chưa
claude mcp list
```

### Cách B — File `.mcp.json` (đặt tại project root)

Tạo file `F:/your-game-project/.mcp.json`:

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

### Cách C — Claude Code global settings

Sửa file `C:\Users\<username>\.claude\settings.json`:

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

---

## 7. Smoke test

Trong Claude Code conversation, thử:

```
Use context7 to find docs about cc.Node actions
```

Hoặc hỏi trực tiếp Claude để gọi tool:

```
Look up the cocos2dx-js docs for how to use cc.Sprite
```

Claude sẽ tự động:
1. Gọi `resolve-library-id` → tìm `cocos2dx-js`
2. Gọi `get-library-docs` với query → trả về chunks liên quan

---

## Workflow hàng ngày

### Khi update docs

```bash
# 1. Sửa/thêm file trong docs/
# 2. Re-index
npm run index
# Xong — không cần build lại, không cần restart Claude
```

### Khi sửa source code (src/)

```bash
npm run build
# Restart MCP trong Claude Code (hoặc restart Claude Code)
```

### Khi đổi library_id

```bash
# Sửa docs/library.json
npm run index   # xóa data cũ, index lại
# Cập nhật cách gọi: /new-library-id
```

---

## Cấu trúc project

```
F:/cocos2dx-context7/
├── build/              ← compiled JS (chạy MCP server này)
│   └── index.js
├── data/
│   ├── context7.sqlite ← vector database
│   └── models/         ← HuggingFace embedding model cache
├── docs/               ← ĐẶT DOC FILES Ở ĐÂY
│   ├── library.json    ← config metadata
│   └── cocos2dx-*.md   ← doc files
├── scripts/
│   └── index-docs.ts   ← indexer script
├── src/
│   ├── index.ts        ← MCP server entry point
│   ├── db.ts           ← SQLite layer
│   ├── embeddings.ts   ← local embedding model
│   ├── search.ts       ← hybrid search (FTS5 + semantic)
│   └── types.ts
├── package.json
└── SETUP.md            ← file này
```

---

## Troubleshooting

### MCP không nhận docs mới
```bash
npm run index   # re-index
# Không cần restart gì thêm
```

### Lỗi "cannot find module build/index.js"
```bash
npm run build
```

### Lỗi TypeScript khi build
```bash
npx tsc --noEmit   # xem lỗi chi tiết
```

### Model không download được (offline)
- Model cache tại `data/models/`
- Copy từ máy khác có cache: `~/.cache/huggingface/hub/`

### Kiểm tra database
```bash
# Xem số chunks đã index
sqlite3 data/context7.sqlite "SELECT library_id, count(*) FROM chunks GROUP BY library_id"

# Xem danh sách libraries
sqlite3 data/context7.sqlite "SELECT * FROM libraries"
```

### Test search từ CLI
```bash
npm run test:search
```
