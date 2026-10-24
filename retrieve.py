
from typing import Any
import numpy as np
import chromadb
from create_vector_store import initialize_vector_store, CHROMA_PATH, COLLECTION_NAME
from preprocessing import preprocess_text
from vector_representation import (
    get_dense_embeddings,
    build_bm25_index,
    compute_hybrid_scores,
)


def get_chroma_collection():
    """
    Connects to the persistent ChromaDB collection.
    If running on Streamlit Cloud and chroma_db doesn't exist yet,
    initializes and populates the store automatically.
    """
    if not CHROMA_PATH.exists() or not any(CHROMA_PATH.iterdir()):
        print("ChromaDB storage not found. Building index from documents...")
        client, collection = initialize_vector_store()
        return collection

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return client.get_collection(name=COLLECTION_NAME)


def hybrid_search(
    query: str,
    top_k: int = 5,
    alpha: float = 0.5,
    current_only: bool = True
) -> list[dict[str, Any]]:
    """
    Executes hybrid retrieval over the corpus.
    
    Args:
        query: User prompt or technical incident question.
        top_k: Number of candidate chunks to return.
        alpha: Weight for dense vs lexical (1.0 = pure semantic, 0.0 = pure BM25).
        current_only: If True, filters out superseded/outdated operational runbooks.
    """
    collection = get_chroma_collection()  # Fixed here!

    # Apply metadata filter if current_only is True
    where_filter = {"is_current": True} if current_only else None

    # Retrieve all eligible records from ChromaDB
    all_records = collection.get(
        where=where_filter,
        include=["documents", "metadatas", "embeddings"]
    )

    doc_texts = all_records["documents"]
    metadatas = all_records["metadatas"]
    chunk_ids = all_records["ids"]
    stored_embeddings = np.array(all_records["embeddings"])

    if not doc_texts:
        return []

    # 1. Compute Dense Semantic Similarity
    query_embed = get_dense_embeddings([query])
    # Dot product with L2-normalized embeddings equals cosine similarity
    dense_scores = np.dot(stored_embeddings, query_embed.T).flatten()

    # 2. Compute BM25 Lexical Scores
    bm25_corpus = [{"text": t} for t in doc_texts]
    bm25 = build_bm25_index(bm25_corpus)
    q_tokens = preprocess_text(query)
    bm25_scores = np.array(bm25.get_scores(q_tokens))

    # 3. Fuse via Normalized Hybrid Formula
    final_scores = compute_hybrid_scores(dense_scores, bm25_scores, alpha=alpha)

    # 4. Rank and select top_k candidates
    top_indices = np.argsort(final_scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "chunk_id": chunk_ids[idx],
            "text": doc_texts[idx],
            "metadata": metadatas[idx],
            "dense_score": float(dense_scores[idx]),
            "bm25_score": float(bm25_scores[idx]),
            "hybrid_score": float(final_scores[idx]),
        })

    return results


if __name__ == "__main__":
    test_query = "What port is used to connect via teleport bastion?"
    print(f"Running hybrid search test for query: '{test_query}'\n")
    matches = hybrid_search(test_query, top_k=3, alpha=0.5)

    for i, res in enumerate(matches, 1):
        meta = res["metadata"]
        print(f"Rank {i} | Hybrid Score: {res['hybrid_score']:.4f} (Dense: {res['dense_score']:.4f}, BM25: {res['bm25_score']:.4f})")
        print(f"Title: {meta['title']} | Department: {meta['department']}")
        print(f"Snippet: {res['text']}\n")