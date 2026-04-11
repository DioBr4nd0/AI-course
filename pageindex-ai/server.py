"""
FastAPI server exposing /search  and  /ask  endpoints.
Reports retrieval + reasoning + generation timings per request.
"""

import os
import time
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from indexer import PageIndex
from reasoning import ReasoningEngine, get_llm

load_dotenv()

# ── Globals (populated on startup) ──
index: PageIndex = None  # type: ignore
engine: ReasoningEngine = None  # type: ignore


@asynccontextmanager
async def lifespan(app: FastAPI):
    global index, engine
    # Build index once at startup
    index = PageIndex().build_from_hf(max_samples=3000)
    engine = ReasoningEngine(get_llm())
    print("[server] Ready.")
    yield


app = FastAPI(title="PageIndex AI", lifespan=lifespan)


# ── Request / Response models ──

class QueryRequest(BaseModel):
    query: str
    top_k: int = 8


class SearchResponse(BaseModel):
    sections: list
    pages: dict
    retrieval_ms: float


class AskResponse(BaseModel):
    answer: str
    reasoning: str
    refined_context: str
    retrieved_sections: list
    timings: dict


# ── Endpoints ──

@app.post("/search", response_model=SearchResponse)
def search(req: QueryRequest):
    """Pure BM25 retrieval — no LLM, ultra-fast."""
    sections, retrieval_ms = index.search_sections(req.query, req.top_k)
    pages, _ = index.search_pages(req.query, req.top_k)
    return SearchResponse(
        sections=sections,
        pages=pages,
        retrieval_ms=round(retrieval_ms, 2),
    )


@app.post("/ask", response_model=AskResponse)
def ask(req: QueryRequest):
    """Full pipeline: BM25 → LLM selection → LLM generation."""
    t0 = time.perf_counter()

    # Step 1 — BM25 retrieval
    sections, retrieval_ms = index.search_sections(req.query, req.top_k)

    # Step 2 — LLM context selection & refinement
    t1 = time.perf_counter()
    selection = engine.select_context(req.query, sections)
    reasoning_ms = (time.perf_counter() - t1) * 1000

    # Step 3 — LLM answer generation
    t2 = time.perf_counter()
    answer = engine.generate(
        req.query, selection["refined_context"], selection["reasoning"]
    )
    generation_ms = (time.perf_counter() - t2) * 1000

    total_ms = (time.perf_counter() - t0) * 1000

    return AskResponse(
        answer=answer,
        reasoning=selection["reasoning"],
        refined_context=selection["refined_context"],
        retrieved_sections=sections,
        timings={
            "retrieval_ms": round(retrieval_ms, 2),
            "reasoning_ms": round(reasoning_ms, 2),
            "generation_ms": round(generation_ms, 2),
            "total_ms": round(total_ms, 2),
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)