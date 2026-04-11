"""
Quick CLI demo — no server needed.
Shows: indexing → BM25 retrieval → LLM reasoning → answer.
"""

import os, time, json
from dotenv import load_dotenv

load_dotenv()

from indexer import PageIndex
from reasoning import ReasoningEngine, get_llm


def main():
    # ── 1. Build index from HuggingFace SQuAD ──
    index = PageIndex().build_from_hf(
        dataset_name="rajpurkar/squad",
        max_samples=3000,
    )

    queries = [
        "What is the capital of France?",
        "When was the University of Warsaw founded?",
        "How does the immune system fight infections?",
    ]

    # ── 2. Pure retrieval demo (no LLM) ──
    print("\n" + "=" * 70)
    print("STAGE 1 — BM25 RETRIEVAL (no embeddings, no LLM)")
    print("=" * 70)

    for q in queries:
        sections, ms = index.search_sections(q, top_k=5)
        pages, _ = index.search_pages(q, top_k=5)
        print(f"\nQuery: '{q}'")
        print(f"  Retrieval time: {ms:.2f} ms")
        print(f"  Pages matched: {list(pages.keys())}")
        for s in sections[:3]:
            print(
                f"    [{s['rank']}] Page='{s['page_title']}' "
                f"Sec={s['section_id']}  BM25={s['bm25_score']}"
            )
            print(f"        {s['text'][:120]}...")

    # ── 3. Full pipeline with LLM reasoning ──
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        print("\n[!] Set OPENAI_API_KEY (or point to Groq/Ollama) to see LLM reasoning.")
        return

    print("\n" + "=" * 70)
    print("STAGE 2 — LLM REASONING + GENERATION")
    print("=" * 70)

    engine = ReasoningEngine(get_llm())

    for q in queries:
        sections, ret_ms = index.search_sections(q, top_k=8)

        t0 = time.perf_counter()
        result = engine.run(q, sections)
        llm_ms = (time.perf_counter() - t0) * 1000

        print(f"\nQuery: '{q}'")
        print(f"  BM25 retrieval:    {ret_ms:.2f} ms")
        print(f"  LLM reasoning+gen: {llm_ms:.0f} ms")
        print(f"  Selected indices:  {result['selected_indices']}")
        print(f"  Reasoning:         {result['reasoning'][:200]}")
        print(f"  Answer:            {result['answer'][:300]}")
        print("-" * 70)


if __name__ == "__main__":
    main()