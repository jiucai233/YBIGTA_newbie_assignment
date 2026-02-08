"""Ingest embeddings into Pinecone vector index.

Batch upsert: 100 vectors per call.
Metadata: text truncated to 1000 chars (40KB limit).
"""

import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone
from tqdm import tqdm

load_dotenv()

RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"

BATCH_SIZE = 100
TEXT_LIMIT = 1000  # metadata text truncation


def ingest(progress_callback=None):
    """Batch upsert embeddings into Pinecone vector index.

    Args:
        progress_callback: Optional callback(current, total) for progress updates.

    Returns:
        int: Number of vectors upserted.

    Hints:
        - Load embeddings from PROCESSED_DIR / "embeddings.npy"
        - Load IDs from PROCESSED_DIR / "embedding_ids.json"
        - Load texts from RAW_DIR / "corpus.jsonl" for metadata
        - Connect: Pinecone(api_key=...) → pc.Index(index_name)
        - Upsert format: {"id": ..., "values": [...], "metadata": {"text": ...}}
        - Batch size: BATCH_SIZE (100), truncate text to TEXT_LIMIT (1000) chars
    """
    # TODO: Implement Pinecone upsert
    embeddings = np.load(PROCESSED_DIR / "embeddings.npy")
    with open(PROCESSED_DIR / "embedding_ids.json", "r", encoding="utf-8") as f:
        ids = json.load(f)
    with open(RAW_DIR / "corpus.jsonl", encoding="utf-8") as f:
        texts = [json.loads(line)["text"] for line in f]
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(os.getenv("PINECONE_INDEX"))
    total_vectors = len(ids)
    for start_idx in tqdm(range(0, total_vectors, BATCH_SIZE)):
        end_idx = min(start_idx + BATCH_SIZE, total_vectors)
        batch_vectors = []
        for i in range(start_idx, end_idx):
            vector = {
                "id": ids[i],
                "values": embeddings[i].tolist(),
                "metadata": {"text": texts[i][:TEXT_LIMIT]},
            }
            batch_vectors.append(vector)
        index.upsert(vectors=batch_vectors)
        if progress_callback:
            progress_callback(end_idx, total_vectors)
    return total_vectors


if __name__ == "__main__":
    ingest()
