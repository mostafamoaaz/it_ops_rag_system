
from typing import Any
import numpy as np
from rank_bm25 import BM25Okapi
from preprocessing import preprocess_text

MODEL_NAME = "all-MiniLM-L6-v2"
_model = None


def get_embedding_model():
    """Lazy-loads the SentenceTransformer model on first actual usage."""
    global _model
    if _model is None:
        print(f"Loading dense embedding model: {MODEL_NAME}...")
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def get_dense_embeddings(texts: list[str]) -> np.ndarray:
    model = get_embedding_model()
    return model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )


def build_bm25_index(chunks: list[dict[str, Any]]) -> BM25Okapi:
    tokenized_corpus = [preprocess_text(c["text"]) for c in chunks]
    return BM25Okapi(tokenized_corpus)


def min_max_normalize(scores: np.ndarray) -> np.ndarray:
    min_val = np.min(scores)
    max_val = np.max(scores)
    if max_val == min_val:
        return np.zeros_like(scores, dtype=float)
    return (scores - min_val) / (max_val - min_val)


def compute_hybrid_scores(
    dense_scores: np.ndarray, lexical_scores: np.ndarray, alpha: float = 0.5
) -> np.ndarray:
    norm_dense = min_max_normalize(dense_scores)
    norm_lexical = min_max_normalize(lexical_scores)
    return alpha * norm_dense + (1.0 - alpha) * norm_lexical