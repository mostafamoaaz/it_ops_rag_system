"""
tune_pipeline.py - Unified Multi-Hyperparameter Grid Search Evaluator
Evaluates chunk_size, overlap, top_k, and alpha together against phrase-level ground truth.
"""

import numpy as np
from documents import DOCUMENTS
from chunking import build_chunked_corpus
from preprocessing import preprocess_text
from vector_representation import build_bm25_index, get_dense_embeddings, compute_hybrid_scores

# 1. Dev Query Dataset with Phrase-Level Verbatim Ground Truth
DEV_QUERIES = [
    {
        "query": "How do I recover when /var/mqm is 100% full?",
        "target_phrase": "rm -rf AMQ7247.0.FDC"
    },
    {
        "query": "What command safely truncates active stdout logs without deleting the file?",
        "target_phrase": "truncate -s 0 stdout"
    },
    {
        "query": "How do I delete a customer user in the private tool database?",
        "target_phrase": "DELETE FROM users WHERE email"
    },
    {
        "query": "How do I extract an SSL certificate from a remote HTTPS endpoint?",
        "target_phrase": "openssl s_client -connect"
    },
    {
        "query": "What command dumps the IBM MQ queue manager configuration?",
        "target_phrase": "dmpmqcfg -m MQM"
    }
]


def evaluate_retrieval(chunks: list[dict], dev_set: list[dict], top_k: int, alpha: float) -> dict:
    """
    Evaluates phrase-level Hit Rate@K and Mean Reciprocal Rank (MRR) for a specific parameter combination.
    """
    if not chunks:
        return {"hit_rate": 0.0, "mrr": 0.0}

    doc_texts = [c["text"] for c in chunks]
    
    # Pre-compute Dense Embeddings & BM25 Index for the current chunk corpus
    dense_embeddings = get_dense_embeddings(doc_texts)
    bm25_corpus = [{"text": t} for t in doc_texts]
    bm25_index = build_bm25_index(bm25_corpus)

    hits = 0
    reciprocal_ranks = []

    for item in dev_set:
        query = item["query"]
        target = item["target_phrase"].lower()

        # 1. Dense Scores
        query_embed = get_dense_embeddings([query])
        dense_scores = np.dot(dense_embeddings, query_embed.T).flatten()

        # 2. BM25 Scores
        q_tokens = preprocess_text(query)
        bm25_scores = np.array(bm25_index.get_scores(q_tokens))

        # 3. Hybrid Fusion
        final_scores = compute_hybrid_scores(dense_scores, bm25_scores, alpha=alpha)
        top_indices = np.argsort(final_scores)[::-1][:top_k]

        # Check for phrase-level match in top_k results
        rank_found = 0
        for rank, idx in enumerate(top_indices, start=1):
            chunk_text_lower = doc_texts[idx].lower()
            if target in chunk_text_lower:
                rank_found = rank
                break

        if rank_found > 0:
            hits += 1
            reciprocal_ranks.append(1.0 / rank_found)
        else:
            reciprocal_ranks.append(0.0)

    hit_rate = hits / len(dev_set)
    mrr = float(np.mean(reciprocal_ranks))

    return {"hit_rate": hit_rate, "mrr": mrr}


def run_full_pipeline_tuning():
    """
    Sweeps across candidate chunk_sizes, overlaps, top_k values, and alpha balances.
    """
    # Hyperparameter Grid Definition
    chunk_sizes = [35, 45, 60]
    overlaps = [0, 5, 10]
    top_k_values = [2, 3, 4]
    alpha_values = [0.2, 0.5, 0.8]  # 0.2 = BM25-heavy, 0.5 = Balanced, 0.8 = Dense-heavy

    results = []

    print("🔍 Running Comprehensive RAG Pipeline Grid Search...\n")
    print(f"{'Size':<5} | {'Overlap':<7} | {'Top-K':<5} | {'Alpha':<5} | {'Est. Words':<10} | {'Hit Rate':<10} | {'MRR':<8}")
    print("-" * 72)

    for size in chunk_sizes:
        for overlap in overlaps:
            if overlap >= size:
                continue

            # Build chunk corpus for this size/overlap
            chunks = build_chunked_corpus(DOCUMENTS, chunk_size=size, overlap=overlap)
            current_chunks = [c for c in chunks if c.get("is_current", True)]

            for k in top_k_values:
                for alpha in alpha_values:
                    metrics = evaluate_retrieval(current_chunks, DEV_QUERIES, top_k=k, alpha=alpha)
                    est_words = k * size

                    results.append({
                        "chunk_size": size,
                        "overlap": overlap,
                        "top_k": k,
                        "alpha": alpha,
                        "est_words": est_words,
                        "hit_rate": metrics["hit_rate"],
                        "mrr": metrics["mrr"]
                    })

                    print(f"{size:<5} | {overlap:<7} | {k:<5} | {alpha:<5.1f} | {est_words:<10} | {metrics['hit_rate']*100:>7.1f}% | {metrics['mrr']:.4f}")

    # Multi-Tiered Ranking Strategy:
    # 1. Highest Hit Rate
    # 2. Highest MRR
    # 3. Fits inside 350-word budget (lowest est_words)
    # 4. Smallest chunk_size
    best = sorted(
        results,
        key=lambda r: (r["hit_rate"], r["mrr"], -r["est_words"], -r["chunk_size"]),
        reverse=True
    )[0]

    print("\n" + "=" * 72)
    print("🏆 GLOBAL OPTIMAL PIPELINE CONFIGURATION:")
    print(f"   • Chunk Size:        {best['chunk_size']} words")
    print(f"   • Overlap:           {best['overlap']} words")
    print(f"   • Top-K Candidates:  {best['top_k']} chunks")
    print(f"   • Hybrid Alpha:      {best['alpha']} (Dense weight)")
    print(f"   • Est. Context Size: {best['est_words']} words")
    print(f"   • Hit Rate:          {best['hit_rate'] * 100:.1f}%")
    print(f"   • Mean Reciprocal R: {best['mrr']:.4f}")
    print("=" * 72)


if __name__ == "__main__":
    run_full_pipeline_tuning()