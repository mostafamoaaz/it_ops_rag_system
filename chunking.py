from typing import Any
from documents import DOCUMENTS


def chunk_document(
    doc: dict[str, Any],
    chunk_size: int = 40,
    overlap: int = 10
) -> list[dict[str, Any]]:
    """
    Splits a single document's text into fixed-size chunks with overlap.
    Inherits parent metadata to enable downstream metadata filtering and source citation.
    """
    text = doc.get("text", "").strip()
    words = text.split()
    
    if not words:
        return []

    # If the document is shorter than the chunk size, keep it intact
    if len(words) <= chunk_size:
        return [
            {
                "chunk_id": f"{doc['document_id']}_c0",
                "document_id": doc["document_id"],
                "chunk_index": 0,
                "title": doc.get("title", ""),
                "department": doc.get("department", ""),
                "doc_type": doc.get("doc_type", ""),
                "effective_date": doc.get("effective_date", ""),
                "is_current": doc.get("is_current", True),
                "text": text,
            }
        ]

    chunks = []
    step = max(1, chunk_size - overlap)
    chunk_idx = 0

    for i in range(0, len(words), step):
        chunk_words = words[i : i + chunk_size]
        chunk_text = " ".join(chunk_words)

        chunks.append(
            {
                "chunk_id": f"{doc['document_id']}_c{chunk_idx}",
                "document_id": doc["document_id"],
                "chunk_index": chunk_idx,
                "title": doc.get("title", ""),
                "department": doc.get("department", ""),
                "doc_type": doc.get("doc_type", ""),
                "effective_date": doc.get("effective_date", ""),
                "is_current": doc.get("is_current", True),
                "text": chunk_text,
            }
        )
        chunk_idx += 1

        # Stop when the remaining words are covered
        if i + chunk_size >= len(words):
            break

    return chunks


def build_chunked_corpus(
    documents: list[dict[str, Any]],
    chunk_size: int = 40,
    overlap: int = 10
) -> list[dict[str, Any]]:
    """
    Generates a flattened list of all chunks across the document corpus.
    """
    all_chunks = []
    for doc in documents:
        doc_chunks = chunk_document(doc, chunk_size=chunk_size, overlap=overlap)
        all_chunks.extend(doc_chunks)
    return all_chunks


if __name__ == "__main__":
    chunks = build_chunked_corpus(DOCUMENTS, chunk_size=40, overlap=10)
    print(f"Total documents: {len(DOCUMENTS)}")
    print(f"Total chunks generated: {len(chunks)}")
    if chunks:
        sample = chunks[0]
        print(f"\nSample Chunk ID: {sample['chunk_id']}")
        print(f"Parent Title: {sample['title']}")
        print(f"Text: {sample['text']}")