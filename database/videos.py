from googleapiclient.discovery import build
import json


def video():
    api_key = "AIzaSyDA9oyLvTcv-kBPPQWfaoHBjZMJ3gjFEes"

    youtube = build("youtube", "v3", developerKey=api_key)

    search_response = youtube.search().list(
        q="obesity",
        part="id, snippet",
        maxResults=10,
        type="video"
    ).execute()

    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]

    video_response = youtube.videos().list(
        id=','.join(video_ids),
        part='snippet, contentDetails, statistics'
    ).execute()

    for video in video_response.get('items', []):
        video_details = {
            'title': video['snippet']['title'],
            'description': video['snippet']['description'],
            'thumbnail_url': video['snippet']['thumbnails']['high']['url'],
            'video_url': f"https://www.youtube.com/watch?v={video['id']}",
            'view_count': video['statistics']['viewCount'],
        }
        # print(json.dumps(video_details, indent=4, ensure_ascii=False))
    return video_response