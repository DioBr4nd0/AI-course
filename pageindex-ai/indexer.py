"""
PageIndex: Page-level & section-level BM25 structured index.
Zero vector embeddings — uses inverted-index term matching.
"""

import re
import time
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datasets import load_dataset
from rank_bm25 import BM25Okapi


@dataclass
class Section:
    page_title: str
    page_id: int
    section_id: int
    text: str


class PageIndex:
    """
    Structured document index with page-level and section-level
    BM25 retrieval. No vector embeddings anywhere in the pipeline.
    """

    def __init__(self):
        self.pages: Dict[str, List[Section]] = {}
        self.sections: List[Section] = []
        self.bm25: Optional[BM25Okapi] = None
        self._corpus_tokens: List[List[str]] = []

    # ------------------------------------------------------------------
    # Build from any HuggingFace dataset that has 'title' + 'context'
    # ------------------------------------------------------------------
    def build_from_hf(
        self,
        dataset_name: str = "rajpurkar/squad",
        split: str = "train",
        max_samples: int = 3000,
    ) -> "PageIndex":
        print(f"[indexer] Loading '{dataset_name}' (first {max_samples} rows)...")
        ds = load_dataset(dataset_name, split=f"{split}[:{max_samples}]")

        page_id_counter = {}
        seen_contexts = set()

        for row in ds:
            title = row["title"]
            context = row["context"]
            key = (title, context)
            if key in seen_contexts:
                continue
            seen_contexts.add(key)

            if title not in page_id_counter:
                page_id_counter[title] = len(page_id_counter)
                self.pages[title] = []

            sec = Section(
                page_title=title,
                page_id=page_id_counter[title],
                section_id=len(self.pages[title]),
                text=context,
            )
            self.pages[title].append(sec)
            self.sections.append(sec)

        # Build BM25 over section texts
        t0 = time.perf_counter()
        self._corpus_tokens = [self._tokenize(s.text) for s in self.sections]
        self.bm25 = BM25Okapi(self._corpus_tokens)
        build_ms = (time.perf_counter() - t0) * 1000

        print(
            f"[indexer] Done — {len(self.pages)} pages, "
            f"{len(self.sections)} sections, "
            f"index built in {build_ms:.1f}ms"
        )
        return self

    # ------------------------------------------------------------------
    # Tokenizer (simple, deterministic — no ML model needed)
    # ------------------------------------------------------------------
    @staticmethod
    def _tokenize(text: str) -> List[str]:
        # lowercase + split on non-word chars
        return re.findall(r"\w+", text.lower())

    # ------------------------------------------------------------------
    # Section-level retrieval
    # ------------------------------------------------------------------
    def search_sections(self, query: str, top_k: int = 8) -> List[dict]:
        t0 = time.perf_counter()
        scores = self.bm25.get_scores(self._tokenize(query))
        top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[
            :top_k
        ]
        elapsed_ms = (time.perf_counter() - t0) * 1000

        results = []
        for rank, i in enumerate(top_idx):
            if scores[i] <= 0:
                continue
            s = self.sections[i]
            results.append(
                {
                    "rank": rank + 1,
                    "page_title": s.page_title,
                    "page_id": s.page_id,
                    "section_id": s.section_id,
                    "text": s.text,
                    "bm25_score": round(float(scores[i]), 4),
                }
            )

        return results, elapsed_ms

    # ------------------------------------------------------------------
    # Page-level grouped retrieval
    # ------------------------------------------------------------------
    def search_pages(self, query: str, top_k: int = 8) -> Dict[str, List[dict]]:
        results, elapsed_ms = self.search_sections(query, top_k)
        grouped: Dict[str, List[dict]] = {}
        for r in results:
            grouped.setdefault(r["page_title"], []).append(r)
        return grouped, elapsed_ms