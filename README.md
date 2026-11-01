# 🛠️ IT Ops Incident & Runbook Assistant (RAG System)

An enterprise-grade Retrieval-Augmented Generation (RAG) assistant designed for IT operations, systems administrators, and middleware engineers. The system delivers verified, source-grounded emergency procedures, command-line steps, and troubleshooting workflows from production runbooks while filtering out deprecated or legacy instructions.

🚀 **Live Streamlit App:** [IT Ops RAG Assistant](https://itopsragsystem-fkiyu6zimghapkzthnplmp.streamlit.app/)

---

## 🌟 Key Features

* **Hybrid Retrieval Engine:** Fuses **BM25 lexical keyword matching** with **SentenceTransformers dense vector embeddings** () via ChromaDB.
* **Empirically Tuned Parameters:** Built using a joint multi-parameter grid search () that optimized chunking and search balance for peak retrieval accuracy:
  * **Chunk Size:** 35 words
  * **Overlap:** 0 words
  * **Top-K Candidates:** 4 chunks
  * **Hybrid Alpha (α):** 0.8 (Dense-leaning hybrid weight)
  * **Hit Rate@K:** **80.0%** (validated against phrase-level ground truth)
* **Metadata Filtering ():** Filters out outdated or superseded operational documents at the database layer before scoring, preventing legacy commands from polluting prompt context.
* **Strict Context Word Budgeting:** Enforces a 350-word context ceiling to keep prompts focused, eliminate 'lost-in-the-middle' LLM attention degradation, and maintain sub-2-second API response times.
* **Grounded LLM Integration:** Uses Google's Gemini API with zero temperature () and safety guardrails to eliminate hallucinations and mandate strict inline source citations.

---

## 🏗️ Architecture & Pipeline Flow



---

## 📂 Project Structure



---

## 🛠️ Local Setup & Deployment

1. **Clone the Repository:**
   Set up your local directory and install required packages from .

2. **Initialize Vector Database:**
   Run  to index your operational runbooks into ChromaDB.

3. **Hyperparameter Tuning:**
   Execute  to verify grid search accuracy across candidate retrieval configurations.

4. **Launch Streamlit App:**
   Run  to start the web application.

---

## 📊 Evaluation & Empirical Results

During empirical grid-search testing (), parameters were evaluated against phrase-level ground-truth target outputs:

| Chunk Size | Overlap | Top-K | Hybrid Alpha (α) | Est. Context | Hit Rate | MRR |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **35 words** | **0 words** | **4** | **0.8 (Dense)** | **140 words** | **80.0%** | **0.5500** |
| 35 words | 10 words | 4 | 0.8 | 140 words | 80.0% | 0.5500 |
| 45 words | 0 words | 4 | 0.8 | 180 words | 40.0% | 0.2500 |

* **Finding:** Pairing smaller 35-word chunks with K=4 and a dense-leaning α=0.8 maximized accuracy while keeping the total context size at a lean 140 words.
