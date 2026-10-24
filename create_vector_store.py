
from pathlib import Path
import chromadb

from documents import DOCUMENTS
from chunking import build_chunked_corpus
from vector_representation import get_dense_embeddings

# Define persistent database path
CHROMA_PATH = Path("./chroma_db")
COLLECTION_NAME = "it_ops_runbooks"


def initialize_vector_store():
    """
    Creates or connects to a persistent ChromaDB instance and populates it with chunk embeddings.
    """
    print(f"Connecting to persistent ChromaDB at: {CHROMA_PATH.resolve()}...")
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    # Retrieve or create collection using cosine similarity space
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    print("Generating chunks from operational documents...")
    chunks = build_chunked_corpus(DOCUMENTS, chunk_size=40, overlap=10)
    print(f"Total chunks to index: {len(chunks)}")

    ids = [c["chunk_id"] for c in chunks]
    texts = [c["text"] for c in chunks]

    # ChromaDB metadata values must be int, float, str, or bool
    metadatas = [
        {
            "document_id": c["document_id"],
            "chunk_index": c["chunk_index"],
            "title": c["title"],
            "department": c["department"],
            "doc_type": c["doc_type"],
            "effective_date": c["effective_date"],
            "is_current": c["is_current"],
        }
        for c in chunks
    ]

    print("Encoding dense embeddings for chunks...")
    embeddings = get_dense_embeddings(texts).tolist()

    print("Upserting records into ChromaDB collection...")
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )

    count = collection.count()
    print(f"✅ Successfully initialized '{COLLECTION_NAME}'. Total indexed chunks in ChromaDB: {count}")
    return client, collection


if __name__ == "__main__":
    initialize_vector_store()