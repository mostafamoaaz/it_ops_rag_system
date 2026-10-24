import streamlit as st
from prompting import generate_rag_response

# Production Defaults (Tuned for balanced hybrid search)
DEFAULT_ALPHA = 0.5
DEFAULT_TOP_K = 4
DEFAULT_WORD_BUDGET = 350

st.set_page_config(
    page_title="IT Ops Runbook Assistant",
    page_icon="🛠️",
    layout="wide"
)

# Header
st.title("🛠️ IT Ops Incident & Runbook Assistant")
st.markdown("Search verified enterprise runbooks, emergency procedures, and deployment workflows.")

# Sidebar: Simple user-centric options only
st.sidebar.header("📌 Quick Runbook Queries")
example_queries = [
    "How to recover when /var/mqm is 100% full?",
    "How do I delete a customer user in the private tool database?",
    "What command safely truncates active stdout logs?",
    "How do I extract an SSL certificate from a remote HTTPS endpoint?",
    "Managing Remedy services during Windows maintenance updates",
]

selected_example = st.sidebar.radio("Select an operational incident:", ["Custom Query"] + example_queries)

# Optional collapsed admin view for troubleshooting only
with st.sidebar.expander("🔧 Advanced Diagnostic Settings", expanded=False):
    alpha = st.slider("Retrieval Hybrid Balance (Alpha)", 0.0, 1.0, DEFAULT_ALPHA, step=0.1,
                      help="0.0 = Exact keyword focus (BM25), 1.0 = Semantic meaning focus")
    top_k = st.number_input("Evidence Chunks (Top-K)", min_value=1, max_value=8, value=DEFAULT_TOP_K)
    word_budget = st.number_input("Context Word Budget", min_value=100, max_value=600, value=DEFAULT_WORD_BUDGET, step=50)

# Main input area
default_val = "" if selected_example == "Custom Query" else selected_example
query = st.text_input("Enter incident description, error log, or command inquiry:", value=default_val)

col1, col2 = st.columns([1, 6])
with col1:
    search_clicked = st.button("Run Resolution", type="primary")

if (search_clicked or query) and query.strip():
    with st.spinner("Finding verified procedures in operational runbooks..."):
        result = generate_rag_response(
            query=query.strip(),
            alpha=alpha,
            top_k=top_k,
            word_budget=word_budget
        )

    # Resolution Card
    st.subheader("📋 Operational Procedure")
    st.markdown(result["answer"])

    # Expandable Source Citations (Trust & Verification)
    with st.expander("📑 Referenced Runbooks & Verification Details", expanded=False):
        for i, chunk in enumerate(result["chunks"], start=1):
            meta = chunk.get("metadata", {})
            st.markdown(f"**{i}. {meta.get('title')}** `({meta.get('department')} | {meta.get('doc_type')})`")
            st.caption(f"Effective Date: {meta.get('effective_date')} | Relevance Score: {chunk.get('hybrid_score', 0):.2f}")
            st.code(chunk.get("text", ""), language="text")