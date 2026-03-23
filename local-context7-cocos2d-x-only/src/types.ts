export interface ChunkRow {
    id?: number
    library_id: string
    source_file: string
    title: string
    body: string
    embedding?: string // JSON stringified number[]
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

export interface LibraryConfig {
    library_id: string
    library_name: string
    description?: string
    version?: string
    docs_dir: string
    db_path: string
}
