import path from 'path';

const MODEL_NAME = 'Xenova/all-MiniLM-L6-v2';
const MODEL_DIR = path.join(process.cwd(), 'data', 'models');

let extractor: any = null;

export async function getEmbedder(): Promise<any> {
  if (extractor !== null) {
    return extractor;
  }

  const { pipeline, env } = await import('@huggingface/transformers');

  env.localModelPath = MODEL_DIR;
  env.cacheDir = MODEL_DIR;

  console.error(`[embeddings] Loading model ${MODEL_NAME} from ${MODEL_DIR} ...`);
  extractor = await pipeline('feature-extraction', MODEL_NAME);
  console.error(`[embeddings] Model loaded successfully.`);

  return extractor;
}

export async function embed(text: string): Promise<number[]> {
  const embedder = await getEmbedder();
  const output = await embedder(text, { pooling: 'mean', normalize: true });
  const result: number[][] = output.tolist();
  return result[0];
}

export async function embedBatch(texts: string[]): Promise<number[][]> {
  const embedder = await getEmbedder();
  const output = await embedder(texts, { pooling: 'mean', normalize: true });
  const result: number[][] = output.tolist();
  return result;
}

export function cosineSimilarity(a: number[], b: number[]): number {
  let dot = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
  }
  return dot;
}
