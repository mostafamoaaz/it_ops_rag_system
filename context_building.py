"""
context_building.py - Context Package Builder
Formats retrieved chunks, enforces strict token/word budgets, and deduplicates content.
"""

from typing import Any
from retrieve import hybrid_search

# Maximum words allowed in the prompt's context block
DEFAULT_WORD_BUDGET = 250


def build_context_package(
    chunks: list[dict[str, Any]],
    word_budget: int = DEFAULT_WORD_BUDGET,
    include_metadata: bool = True
) -> str:
    """
    Formats retrieved chunks into a structured context string for prompt injection.
    Stops adding chunks when the word budget is reached.
    """
    if not chunks:
        return "No relevant operational runbooks found."

    package_blocks = []
    accumulated_words = 0
    seen_chunk_ids = set()

    for chunk in chunks:
        if chunk.get("hybrid_score", 0) < 0.20:
            continue
        c_id = chunk["chunk_id"]
        if c_id in seen_chunk_ids:
            continue
        seen_chunk_ids.add(c_id)

        meta = chunk.get("metadata", {})
        title = meta.get("title", "Unknown Procedure")
        dept = meta.get("department", "Operations")
        doc_type = meta.get("doc_type", "runbook")
        text = chunk.get("text", "").strip()

        if include_metadata:
            block = f"[{title} | Dept: {dept} | Type: {doc_type}]\n{text}"
        else:
            block = text

        block_word_count = len(block.split())

        # If adding this block exceeds the budget, check if we already have some context
        if accumulated_words + block_word_count > word_budget:
            if not package_blocks:
                # If even the first chunk exceeds, truncate it to fit
                words = block.split()[:word_budget]
                package_blocks.append(" ".join(words) + " ...")
            break

        package_blocks.append(block)
        accumulated_words += block_word_count

    return "\n\n---\n\n".join(package_blocks)


def retrieve_and_build_context(
    query: str,
    top_k: int | None = None,
    alpha: float | None = None,
    word_budget: int = DEFAULT_WORD_BUDGET,
    current_only: bool = True
) -> tuple[str, list[dict[str, Any]]]:
    """
    End-to-end convenience function: retrieves candidate chunks and packages them.
    Defers top_k and alpha defaults directly to hybrid_search() in retrieve.py.
    """
    # Build kwargs dynamically, omitting top_k and alpha if None so hybrid_search uses its own defaults
    search_kwargs: dict[str, Any] = {"query": query, "current_only": current_only}
    if top_k is not None:
        search_kwargs["top_k"] = top_k
    if alpha is not None:
        search_kwargs["alpha"] = alpha

    chunks = hybrid_search(**search_kwargs)
    context = build_context_package(chunks, word_budget=word_budget)
    return context, chunks


if __name__ == "__main__":
    test_q = "How to recover when /var/mqm is 100% full?"
    ctx, matches = retrieve_and_build_context(test_q, top_k=3, alpha=0.5)
    print("=== ASSEMBLED CONTEXT PACKAGE ===")
    print(ctx)