
import os
from functools import lru_cache
from dotenv import load_dotenv
from google import genai

load_dotenv()


@lru_cache(maxsize=1)
def get_best_available_model(client: genai.Client = None) -> str:
    """Discovers active models for the API key and returns the best available Flash model."""
    if client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment!")
        client = genai.Client(api_key=api_key)

    # Preferred models in priority order
    priority_order = [
        "gemini-3.5-flash-lite",
        "gemini-3.5-flash",
        "gemini-flash-lite-latest",
        "gemini-flash-latest",
        "gemini-3.8-flash",
    ]

    try:
        available_names = [m.name.replace("models/", "") for m in client.models.list()]

        for pref in priority_order:
            if pref in available_names:
                return pref

        # Fallback to the first model matching 'flash'
        for name in available_names:
            if "flash" in name:
                return name

        return available_names[0] if available_names else "gemini-3.5-flash-lite"
    except Exception as e:
        print(f"⚠️ Model discovery failed ({e}), falling back to gemini-3.5-flash-lite")
        return "gemini-3.5-flash-lite"


if __name__ == "__main__":
    print("Testing model discovery...")
    selected = get_best_available_model()
    print(f"✅ Best available model selected: {selected}")