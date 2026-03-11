from transformers import pipeline
import torch

print("Loading MiniLM sentiment model...")

# -----------------------------
# LABEL MAP (CRITICAL FIX)
# -----------------------------
LABEL_MAP = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive",
}

# -----------------------------
# Load pipeline
# -----------------------------
sentiment_pipeline = pipeline(
    "text-classification",
    model="./minilm-twitter-sentiment",
    tokenizer="./minilm-twitter-sentiment",
    top_k=None,
    truncation=True,
    max_length=160,
    device=0 if torch.cuda.is_available() else -1
)

print("Model loaded successfully")


# ---------------------------------------------------
# Helper: summarize comment predictions
# ---------------------------------------------------
def summarize_comment_sentiments(results):
    pos = sum(1 for r in results if r["label"] == "positive")
    neg = sum(1 for r in results if r["label"] == "negative")
    neu = sum(1 for r in results if r["label"] == "neutral")

    total = max(len(results), 1)

    return pos / total, neg / total, neu / total


# ---------------------------------------------------
# Main video sentiment analyzer
# ---------------------------------------------------
def analyze_video_comments(comments, views: int, likes: int):
    """
    Returns per-video sentiment metrics.
    """

    # -----------------------------
    # SAFETY: no comments
    # -----------------------------
    if not comments:
        return {
            "sentiment_score": 0,
            "positive_ratio": 0,
            "negative_ratio": 0,
            "neutral_ratio": 1,
            "views": views,
            "likes": likes,
        }

    # -----------------------------
    # BATCH INFERENCE
    # -----------------------------
    results = sentiment_pipeline(comments, batch_size=16)

    # -----------------------------
    # PARSE + MAP LABELS (CRITICAL)
    # -----------------------------
    parsed = []

    for r in results:
        if isinstance(r, list):
            best = max(r, key=lambda x: x["score"])
        else:
            best = r

        raw_label = best["label"]
        mapped_label = LABEL_MAP.get(raw_label, raw_label).lower()

        parsed.append({
            "label": mapped_label,
            "score": best["score"]
        })

    # -----------------------------
    # RATIOS
    # -----------------------------
    pos_ratio, neg_ratio, neu_ratio = summarize_comment_sentiments(parsed)

    # -----------------------------
    # SOFTER SENTIMENT FORMULA
    # -----------------------------
    score = (
        (-1 * neg_ratio)
        + (0.1 * neu_ratio)  # softer neutral weight
        + (1 * pos_ratio)
    )

    return {
        "sentiment_score": score,
        "positive_ratio": pos_ratio,
        "negative_ratio": neg_ratio,
        "neutral_ratio": neu_ratio,
        "views": views,
        "likes": likes,
    }
