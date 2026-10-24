
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

from context_building import retrieve_and_build_context
from list_gemini_models import get_best_available_model

# 1. Environment & API Initialization
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file! Please verify your configuration.")

client = genai.Client(api_key=api_key)

# 2. Strict Grounded System Prompt
SYSTEM_PROMPT = """You are an Enterprise Systems Administrator and Senior DevOps Assistant.
Your primary role is to provide accurate, grounded technical instructions based strictly on the operational runbooks provided in the context.

STRICT OPERATIONAL RULES:
1. Base your answer ONLY on the provided runbook snippets.
2. For every step or command you provide, cite the runbook title using bracket format (e.g., [IBM MQ /var/mqm 100% Full Disk Space Recovery]).
3. If the provided context does NOT contain the answer, or if the system/tool is out of scope (e.g., Terraform, AWS DynamoDB), state clearly:
   "The available operational runbooks do not cover this procedure." Do NOT invent or hallucinate command flags or scripts.
4. Always highlight safety warnings, required pre-execution backups (e.g., mysqldump, VM snapshots), and verification commands."""


def format_user_prompt(query: str, context: str) -> str:
    """Formats the prompt with retrieved runbook passages and user incident query."""
    return f"""OPERATIONAL RUNBOOKS CONTEXT:
{context}

USER TECHNICAL INCIDENT / INQUIRY:
{query}

TECHNICAL RESOLUTION:"""


def generate_rag_response(
    query: str,
    alpha: float = 0.5,
    top_k: int = 4,
    word_budget: int = 350,
    model: str = None
) -> dict:
    """
    Executes hybrid retrieval, builds context, and invokes the selected Gemini model.
    Automatically resolves the best active model if none is explicitly provided.
    """
    # Dynamically select active model from list_gemini_models.py if unspecified
    if not model:
        model = get_best_available_model(client)

    # Retrieve candidate chunks and package within word budget
    context, retrieved_chunks = retrieve_and_build_context(
        query=query,
        top_k=top_k,
        alpha=alpha,
        word_budget=word_budget,
        current_only=True
    )

    user_message = format_user_prompt(query, context)
    answer = None

    # Retry loop with exponential backoff for handling transient 503 / rate spike errors
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=model,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.0,  # Deterministic output for technical procedures
                ),
            )
            answer = response.text
            break
        except Exception as e:
            err_msg = str(e)
            if ("503" in err_msg or "UNAVAILABLE" in err_msg) and attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            answer = f"⚠️ Gemini API Error on model '{model}': {err_msg}\n\n(Retrieved context is still accessible below)."
            break

    return {
        "query": query,
        "answer": answer,
        "context": context,
        "chunks": retrieved_chunks,
        "model_used": model
    }


if __name__ == "__main__":
    test_q = "How do I resolve an emergency where /var/mqm is completely full?"
    print(f"Testing RAG prompt generation for: '{test_q}'\n")
    res = generate_rag_response(test_q, alpha=0.5)
    print(f"--- Model Selected: {res['model_used']} ---")
    print("=== MODEL RESOLUTION ===")
    print(res["answer"])
