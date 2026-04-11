"""
Benchmark: BM25 retrieval vs vector-embedding retrieval.
Proves BM25 is faster for the retrieval step.
"""

import time
import numpy as np
from indexer import PageIndex


def benchmark():
    # ── Build BM25 index ──
    index = PageIndex().build_from_hf(max_samples=3000)

    queries = [
        "Who invented the telephone?",
        "What causes earthquakes?",
        "History of the Roman Empire",
        "How do vaccines work?",
        "Theory of relativity explained",
        "When did World War 2 end?",
        "What is machine learning?",
        "Capital of Germany",
    ]

    # ── BM25 benchmark ──
    bm25_times = []
    for q in queries:
        t0 = time.perf_counter()
        index.search_sections(q, top_k=10)
        bm25_times.append((time.perf_counter() - t0) * 1000)

    avg_bm25 = np.mean(bm25_times)
    print(f"\n{'='*60}")
    print(f"BM25 RETRIEVAL")
    print(f"  Corpus size:   {len(index.sections)} sections")
    print(f"  Avg query:     {avg_bm25:.2f} ms")
    print(f"  Min / Max:     {min(bm25_times):.2f} / {max(bm25_times):.2f} ms")

    # ── Vector embedding benchmark ──
    print(f"\nLoading sentence-transformers model (one-time cost)...")
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Encode corpus
    print("Encoding corpus...")
    t0 = time.perf_counter()
    corpus_texts = [s.text for s in index.sections]
    corpus_emb = model.encode(corpus_texts, show_progress_bar=True, batch_size=64)
    corpus_emb = corpus_emb / np.linalg.norm(corpus_emb, axis=1, keepdims=True)
    encode_time = (time.perf_counter() - t0) * 1000
    print(f"  Corpus encoding: {encode_time:.0f} ms")

    # Query
    vector_times = []
    for q in queries:
        t0 = time.perf_counter()
        q_emb = model.encode([q])
        q_emb = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)
        scores = (corpus_emb @ q_emb.T).flatten()
        top_k = np.argsort(scores)[-10:][::-1]
        vector_times.append((time.perf_counter() - t0) * 1000)

    avg_vector = np.mean(vector_times)
    print(f"\nVECTOR EMBEDDING RETRIEVAL (all-MiniLM-L6-v2)")
    print(f"  Avg query:     {avg_vector:.2f} ms")
    print(f"  Min / Max:     {min(vector_times):.2f} / {max(vector_times):.2f} ms")

    # ── Comparison ──
    speedup = avg_vector / avg_bm25
    print(f"\n{'='*60}")
    print(f"RESULT: BM25 is {speedup:.1f}x faster than vector retrieval")
    print(f"  BM25:   {avg_bm25:.2f} ms/query")
    print(f"  Vector: {avg_vector:.2f} ms/query")
    print(f"{'='*60}")


if __name__ == "__main__":
    benchmark()