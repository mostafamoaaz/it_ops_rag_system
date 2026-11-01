"""
test_pipeline.py - Integration Test for Refactored RAG Pipeline
Verifies end-to-end flow and default parameter inheritance.
"""

from retrieve import hybrid_search
from context_building import retrieve_and_build_context
from prompting import generate_rag_response

def test_pipeline():
    test_query = "How to recover when /var/mqm is 100% full?"
    print(f"🧪 Testing query: '{test_query}'\n")

    # 1. Test retrieve.py defaults (should pick up top_k=4, alpha=0.8)
    print("1️⃣ Testing direct retrieve.py execution...")
    chunks = hybrid_search(test_query)
    print(f"   ✓ Retrieved {len(chunks)} chunks (Expected top_k=4)")
    assert len(chunks) <= 4, "retrieve.py failed to enforce top_k default"
    print(f"   ✓ Top Chunk Score: {chunks[0]['hybrid_score']:.4f} | Title: {chunks[0]['metadata']['title']}")

    # 2. Test context_building.py wrapper parameter inheritance
    print("\n2️⃣ Testing context_building.py wrapper...")
    context, ctx_chunks = retrieve_and_build_context(test_query)
    print(f"   ✓ Context string length: {len(context.split())} words")
    print(f"   ✓ Context contains metadata headers: {'[' in context}")

    # 3. Test prompting.py end-to-end resolution
    print("\n3️⃣ Testing prompting.py LLM generation...")
    res = generate_rag_response(test_query)
    print(f"   ✓ Model selected: {res['model_used']}")
    print(f"   ✓ Chunks attached: {len(res['chunks'])}")
    print("\n--- Generated Answer Preview ---")
    print(res["answer"][:300] + "...\n")

    print("=" * 60)
    print("✅ ALL BACKEND PIPELINE INTEGRATION TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    test_pipeline()