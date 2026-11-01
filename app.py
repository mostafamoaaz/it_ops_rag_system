import streamlit as st
from prompting import generate_rag_response

# Streamlit Page Configuration
st.set_page_config(
    page_title="IT Ops Runbook Assistant",
    page_icon="🛠️",
    layout="wide"
)

# Header
st.title("🛠️ IT Ops Incident & Runbook Assistant")
st.markdown("Search verified enterprise runbooks, emergency procedures, and deployment workflows.")

# Clean Sidebar: Focused purely on Quick Operational Incident Presets
st.sidebar.header("📌 Quick Runbook Queries")
example_queries = [
    "How to recover when /var/mqm is 100% full?",
    "How do I delete a customer user in the private tool database?",
    "What command safely truncates active stdout logs?",
    "How do I extract an SSL certificate from a remote HTTPS endpoint?",
    "Managing Remedy services during Windows maintenance updates",
]

selected_example = st.sidebar.radio("Select an operational incident:", ["Custom Query"] + example_queries)

# Main Input Section
default_val = "" if selected_example == "Custom Query" else selected_example
query = st.text_input("Enter incident description, error log, or command inquiry:", value=default_val)

col1, _ = st.columns([1, 6])
with col1:
    search_clicked = st.button("Run Resolution", type="primary")

# Execution & Resolution Card
if (search_clicked or query) and query.strip():
    with st.spinner("Finding verified procedures in operational runbooks..."):
        # Automatically inherits optimal retrieval defaults (alpha=0.8, top_k=4) from retrieve.py
        result = generate_rag_response(query=query.strip())

    # Resolution Output Block
    st.subheader("📋 Operational Procedure")
    st.markdown(result["answer"])

    # Source Citations for Transparency & Trust
    with st.expander("📖 Referenced Runbooks & Verification Details", expanded=False):
        for i, chunk in enumerate(result["chunks"], start=1):
            meta = chunk.get("metadata", {})
            st.markdown(f"**{i}. {meta.get('title')}** `({meta.get('department')} | {meta.get('doc_type')})`")
            st.caption(f"Effective Date: {meta.get('effective_date')} | Relevance Score: {chunk.get('hybrid_score', 0):.2f}")
            st.code(chunk.get("text", ""), language="text")