"""
Two-stage LLM reasoning layer:
  Stage 1 — Context Selection:  LLM evaluates retrieved sections,
             picks the relevant ones, explains why, refines the context.
  Stage 2 — Answer Generation:  LLM answers from the refined context only.

This gives explainability (we can show *why* certain sections were chosen)
and higher accuracy (irrelevant BM25 hits are filtered out by the LLM).
"""

import os
import re
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ── Prompts ──────────────────────────────────────────────────────────

SELECTION_PROMPT = """\
You are a context-selection agent. You receive a user QUERY and a numbered
list of CANDIDATE SECTIONS retrieved from a document corpus.

Your job:
1. Read each section carefully.
2. Decide which sections are truly relevant to answering the query.
3. Discard noisy / off-topic sections.
4. Output a refined, consolidated context from the selected sections.

QUERY: {query}

CANDIDATE SECTIONS:
{candidates}

Respond in EXACTLY this format (keep the labels):

SELECTED: <comma-separated indices of relevant sections, e.g. 0,2,5>
REASONING: <1-3 sentences explaining why you selected those and rejected others>
REFINED_CONTEXT: <merged text from selected sections that directly helps answer the query>
"""

GENERATION_PROMPT = """\
Answer the user's query using ONLY the provided context.
Be precise. Cite the page title when possible.

Query: {query}

Context (curated by reasoning layer):
{refined_context}

Selection reasoning: {reasoning}

Answer:"""


# ── Engine ───────────────────────────────────────────────────────────


def get_llm() -> ChatOpenAI:
    """
    Returns a ChatOpenAI instance.
    Works with OpenAI, Groq, Ollama, LM Studio — anything
    that exposes an OpenAI-compatible /v1/chat/completions endpoint.
    """
    return ChatOpenAI(
        model=os.getenv("MODEL_NAME", "gpt-3.5-turbo"),
        base_url=os.getenv("OPENAI_BASE_URL", None),
        api_key=os.getenv("OPENAI_API_KEY", ""),
        temperature=0,
        max_tokens=1024,
    )


class ReasoningEngine:
    def __init__(self, llm=None):
        self.llm = llm or get_llm()
        self._select_chain = (
            ChatPromptTemplate.from_template(SELECTION_PROMPT)
            | self.llm
            | StrOutputParser()
        )
        self._generate_chain = (
            ChatPromptTemplate.from_template(GENERATION_PROMPT)
            | self.llm
            | StrOutputParser()
        )

    # ── Stage 1: select & refine context ──

    def select_context(self, query: str, sections: List[dict]) -> dict:
        candidates = "\n\n".join(
            f"[{i}] Page: \"{s['page_title']}\"  |  Section {s['section_id']}  |  "
            f"BM25={s['bm25_score']}\n{s['text'][:600]}"
            for i, s in enumerate(sections)
        )
        raw = self._select_chain.invoke(
            {"query": query, "candidates": candidates}
        )
        return self._parse_selection(raw)

    # ── Stage 2: generate answer from refined context ──

    def generate(self, query: str, refined_context: str, reasoning: str) -> str:
        return self._generate_chain.invoke(
            {
                "query": query,
                "refined_context": refined_context,
                "reasoning": reasoning,
            }
        )

    # ── convenience: full pipeline ──

    def run(self, query: str, sections: List[dict]) -> dict:
        selection = self.select_context(query, sections)
        answer = self.generate(query, selection["refined_context"], selection["reasoning"])
        return {
            "answer": answer,
            "selected_indices": selection["selected_indices"],
            "reasoning": selection["reasoning"],
            "refined_context": selection["refined_context"],
        }

    # ── parse the structured LLM output ──

    @staticmethod
    def _parse_selection(raw: str) -> dict:
        selected = []
        reasoning = ""
        refined = ""

        # Extract SELECTED indices
        m = re.search(r"SELECTED:\s*(.+)", raw)
        if m:
            selected = [
                int(x.strip()) for x in m.group(1).split(",") if x.strip().isdigit()
            ]

        # Extract REASONING
        m = re.search(r"REASONING:\s*(.+?)(?=REFINED_CONTEXT:|$)", raw, re.S)
        if m:
            reasoning = m.group(1).strip()

        # Extract REFINED_CONTEXT
        m = re.search(r"REFINED_CONTEXT:\s*(.+)", raw, re.S)
        if m:
            refined = m.group(1).strip()

        return {
            "selected_indices": selected,
            "reasoning": reasoning,
            "refined_context": refined,
            "raw": raw,
        }