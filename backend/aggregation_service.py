import math
from typing import List, Dict


def compute_sentiment_index(score: float) -> float:
    """
    Convert raw sentiment (-1 to 1) → 0–100 scale
    """
    return round(((score + 1) / 2) * 100, 2)


def compute_controversy(pos_ratio: float, neg_ratio: float, neu_ratio: float) -> float:
    """
    Smoothed controversy metric.
    """
    base = 1 - max(pos_ratio, neg_ratio, neu_ratio)
    return round(min(1.0, max(0.0, base)), 3)



def aggregate_channel_metrics(videos: List[Dict]) -> Dict:
    """
    Aggregates per-video sentiment into channel-level intelligence.
    """

    if not videos:
        return {}

    weighted_sum = 0
    weight_total = 0

    pos_total = 0
    neg_total = 0
    neu_total = 0
    engagement_total = 0

    for v in videos:
        views = v.get("views", 0)
        likes = v.get("likes", 0)

        # 🔥 engagement-aware weight
        weight = math.log(views + 1)

        weighted_sum += v["sentiment_score"] * weight
        weight_total += weight

        pos_total += v["positive_ratio"]
        neg_total += v["negative_ratio"]
        neu_total += v["neutral_ratio"]

        if views > 0:
            engagement_total += likes / views

    avg_score = weighted_sum / weight_total if weight_total else 0
    video_count = len(videos)

    pos_ratio = pos_total / video_count
    neg_ratio = neg_total / video_count
    neu_ratio = neu_total / video_count

    return {
        "sentiment_index": compute_sentiment_index(avg_score),
        "raw_sentiment_score": round(avg_score, 3),
        "positive_ratio": round(pos_ratio, 3),
        "negative_ratio": round(neg_ratio, 3),
        "neutral_ratio": round(neu_ratio, 3),
        "engagement_score": round(engagement_total / video_count, 3),
        "controversy_score": compute_controversy(pos_ratio, neg_ratio, neu_ratio),
        "video_count": video_count,
    }
