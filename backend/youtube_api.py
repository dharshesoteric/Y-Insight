import os
from googleapiclient.discovery import build

# 🔑 Put your API key here or use env variable
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "AIzaSyDkTo99VwKqmzwkJEXx70VLQlEjcmHGvmc")

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


# ---------------------------------------------------
# Get channel ID from channel name
# ---------------------------------------------------
def get_channel_id(channel_name: str):
    request = youtube.search().list(
        q=channel_name,
        part="snippet",
        type="channel",
        maxResults=1,
    )
    response = request.execute()

    items = response.get("items", [])
    if not items:
        return None

    return items[0]["snippet"]["channelId"]


# ---------------------------------------------------
# Get recent videos from channel
# ---------------------------------------------------
def get_channel_videos(channel_name: str, max_results: int = 5):
    channel_id = get_channel_id(channel_name)
    if not channel_id:
        return []

    # get uploads playlist
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id,
    )
    response = request.execute()

    uploads_playlist = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # fetch videos
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_playlist,
        maxResults=max_results,
    )
    playlist_response = request.execute()

    videos = []

    for item in playlist_response.get("items", []):
        video_id = item["snippet"]["resourceId"]["videoId"]

        # get video stats
        stats_request = youtube.videos().list(
            part="statistics",
            id=video_id,
        )
        stats_response = stats_request.execute()

        stats = stats_response["items"][0]["statistics"]

        videos.append({
            "video_id": video_id,
            "title": item["snippet"]["title"],
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
        })

    return videos


# ---------------------------------------------------
# Get comments for a video
# ---------------------------------------------------
def get_video_comments(video_id: str, max_comments: int = 50):
    comments = []

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText",
        )

        response = request.execute()

        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

            if len(comments) >= max_comments:
                break

    except Exception:
        # comments may be disabled
        pass

    return comments
