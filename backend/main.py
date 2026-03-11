from fastapi import FastAPI
from pydantic import BaseModel

from youtube_api import get_channel_videos, get_video_comments
from sentiment import analyze_video_comments
from aggregation_service import aggregate_channel_metrics
from groq_service import generate_channel_insights


app = FastAPI()


# =====================================================
# Request Models
# =====================================================

class ChannelRequest(BaseModel):
    channel_name: str


class CompareRequest(BaseModel):
    channel_names: list[str]


# =====================================================
# Helper — analyze single channel (REUSABLE CORE)
# =====================================================

def analyze_single_channel(channel_name: str):
    videos = get_channel_videos(channel_name)

    video_results = []

    for video in videos:
        comments = get_video_comments(video["video_id"])

        metrics = analyze_video_comments(
            comments,
            views=video.get("views", 0),
            likes=video.get("likes", 0),
        )

        video_results.append(metrics)

    channel_metrics = aggregate_channel_metrics(video_results)

    return {
        "channel_name": channel_name,
        "metrics": channel_metrics,
    }


# =====================================================
# Existing Endpoint — Single Analysis
# =====================================================

@app.post("/analyze-channel")
def analyze_channel(request: ChannelRequest):
    result = analyze_single_channel(request.channel_name)

    return {
        "channel_name": result["channel_name"],
        "metrics": result["metrics"],
    }


# =====================================================
# NEW — Multi Channel Comparison ⭐⭐⭐⭐⭐
# =====================================================

@app.post("/compare-channels")
def compare_channels(request: CompareRequest):
    names = [n.strip() for n in request.channel_names if n.strip()][:3]

    if not names:
        return {"error": "No valid channel names provided"}

    results = []

    for name in names:
        try:
            result = analyze_single_channel(name)
            results.append(result)
        except Exception as e:
            results.append({
                "channel_name": name,
                "error": str(e)
            })

    # -----------------------------
    # Ranking by sentiment index
    # -----------------------------
    valid_results = [r for r in results if "metrics" in r]

    ranked = sorted(
        valid_results,
        key=lambda x: x["metrics"]["sentiment_index"],
        reverse=True
    )

    # -----------------------------
    # Gemini Insights
    # -----------------------------
    ai_insights = generate_channel_insights(ranked)

    return {
        "comparison": ranked,
        "ai_insights": ai_insights
    }
