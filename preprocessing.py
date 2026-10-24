import re

# Domain-specific negation and critical status words that must NEVER be stripped
PRESERVED_TOKENS = {"not", "no", "never", "none", "without", "down", "fail", "failed", "stop", "kill"}

# Common English stopwords (excluding preserved operational tokens)
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down",
    "during", "each", "few", "for", "from", "further", "had", "has", "have",
    "having", "he", "her", "here", "hers", "herself", "him", "himself", "his",
    "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me",
    "more", "most", "my", "myself", "nor", "of", "off", "on", "once", "only",
    "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
    "same", "she", "should", "so", "some", "such", "than", "that", "the", "their",
    "theirs", "them", "themselves", "then", "there", "these", "they", "this",
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "we",
    "were", "what", "when", "where", "which", "while", "who", "whom", "why",
    "with", "would", "you", "your", "yours", "yourself", "yourselves"
} - PRESERVED_TOKENS


def tokenize(text: str) -> list[str]:
    """
    Extracts lowercase alphanumeric tokens, preserving technical identifiers like
    port numbers, error codes, and server names.
    """
    return re.findall(r"[a-z0-9_\-\.]+", text.lower())



def preprocess_text(text: str, remove_stopwords: bool = True) -> list[str]:
    """
    Tokenizes text and selectively removes stopwords while preserving critical
    operational negation and status keywords.
    """
    tokens = tokenize(text)
    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS]
    return tokens


def build_search_text(doc: dict) -> str:
    """Enriches operational document text with parent metadata for hybrid indexing."""
    parts = [
        f"Title: {doc.get('title', '')}",
        f"Department: {doc.get('department', '')}",
        f"Type: {doc.get('doc_type', '')}",
        doc.get("text", "")
    ]
    return "\n".join(parts)