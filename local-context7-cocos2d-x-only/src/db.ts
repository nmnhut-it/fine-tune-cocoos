import Database from 'better-sqlite3'
import { ChunkRow, LibraryRow } from './types.js'
import path from 'path'
import fs from 'fs'

const SCHEMA_SQL = `
CREATE TABLE IF NOT EXISTS chunks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    library_id  TEXT    NOT NULL,
    source_file TEXT    NOT NULL,
    title       TEXT    NOT NULL DEFAULT '',
    body        TEXT    NOT NULL,
    embedding   TEXT,
    created_at  INTEGER DEFAULT (unixepoch())
);

CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
    title,
    body,
    tokenize = 'porter ascii',
    content  = 'chunks',
    content_rowid = 'id'
);

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

CREATE TABLE IF NOT EXISTS libraries (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT,
    version     TEXT,
    indexed_at  INTEGER DEFAULT (unixepoch())
);
`

export function initDb(dbPath: string): Database.Database {
    // Ensure parent directory exists
    const dir = path.dirname(dbPath)
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true })
    }

    const db = new Database(dbPath)

    // Enable WAL mode for better concurrency
    db.pragma('journal_mode = WAL')
    db.pragma('foreign_keys = ON')

    // Run schema statements one at a time (exec handles multiple statements)
    db.exec(SCHEMA_SQL)

    return db
}

export function clearLibrary(db: Database.Database, libraryId: string): void {
    // Deleting from chunks triggers chunks_ad which cleans FTS automatically
    const stmt = db.prepare('DELETE FROM chunks WHERE library_id = ?')
    stmt.run(libraryId)
}

export function insertChunk(db: Database.Database, chunk: ChunkRow): number {
    const stmt = db.prepare(`
        INSERT INTO chunks (library_id, source_file, title, body, embedding)
        VALUES (@library_id, @source_file, @title, @body, @embedding)
    `)
    const result = stmt.run({
        library_id: chunk.library_id,
        source_file: chunk.source_file,
        title: chunk.title,
        body: chunk.body,
        embedding: chunk.embedding ?? null,
    })
    return result.lastInsertRowid as number
}

export function insertChunksBatch(db: Database.Database, chunks: ChunkRow[]): void {
    const insert = db.prepare(`
        INSERT INTO chunks (library_id, source_file, title, body, embedding)
        VALUES (@library_id, @source_file, @title, @body, @embedding)
    `)
    const runMany = db.transaction((rows: ChunkRow[]) => {
        for (const row of rows) {
            insert.run({
                library_id: row.library_id,
                source_file: row.source_file,
                title: row.title,
                body: row.body,
                embedding: row.embedding ?? null,
            })
        }
    })
    runMany(chunks)
}

export function getAllChunks(db: Database.Database, libraryId: string): ChunkRow[] {
    const stmt = db.prepare(`
        SELECT id, library_id, source_file, title, body, embedding
        FROM chunks
        WHERE library_id = ?
    `)
    return stmt.all(libraryId) as ChunkRow[]
}

export function upsertLibrary(db: Database.Database, lib: LibraryRow): void {
    const stmt = db.prepare(`
        INSERT INTO libraries (id, name, description, version, indexed_at)
        VALUES (@id, @name, @description, @version, unixepoch())
        ON CONFLICT(id) DO UPDATE SET
            name        = excluded.name,
            description = excluded.description,
            version     = excluded.version,
            indexed_at  = unixepoch()
    `)
    stmt.run({
        id: lib.id,
        name: lib.name,
        description: lib.description ?? null,
        version: lib.version ?? null,
    })
}

export function listLibraries(db: Database.Database): (LibraryRow & { chunk_count: number })[] {
    const stmt = db.prepare(`
        SELECT l.id, l.name, l.description, l.version, COUNT(c.id) as chunk_count
        FROM libraries l
        LEFT JOIN chunks c ON c.library_id = l.id
        GROUP BY l.id
    `)
    return stmt.all() as (LibraryRow & { chunk_count: number })[]
}

export function getLibraryChunkCount(db: Database.Database, libraryId: string): number {
    const stmt = db.prepare('SELECT COUNT(*) as cnt FROM chunks WHERE library_id = ?')
    const row = stmt.get(libraryId) as { cnt: number }
    return row.cnt
}
