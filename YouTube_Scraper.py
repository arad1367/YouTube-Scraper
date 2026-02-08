### Code by Pejman Ebrahimi - 08.02.2026
"""
Installation: pip install google-api-python-client

"""

import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import csv
from datetime import datetime

API_KEY = "PUT YouTube API HERE!"

youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_videos(query, max_results=50, order='relevance', published_after=None):
    videos = []
    next_page_token = None

    while len(videos) < max_results:
        try:
            search_params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': min(50, max_results - len(videos)),
                'order': order,
                'pageToken': next_page_token
            }

            if published_after:
                search_params['publishedAfter'] = published_after

            search_response = youtube.search().list(**search_params).execute()

            for item in search_response.get('items', []):
                video_id = item['id']['videoId']
                videos.append({
                    'video_id': video_id,
                    'title': item['snippet']['title'],
                    'channel_id': item['snippet']['channelId'],
                    'channel_title': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt'],
                    'description': item['snippet']['description']
                })

            next_page_token = search_response.get('nextPageToken')
            if not next_page_token:
                break

        except HttpError as e:
            print(f"HTTP Error: {e}")
            break

    return videos

def get_video_statistics(video_ids):
    stats = []

    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        try:
            stats_response = youtube.videos().list(
                part='statistics,contentDetails',
                id=','.join(batch_ids)
            ).execute()

            for item in stats_response.get('items', []):
                stats.append({
                    'video_id': item['id'],
                    'view_count': item['statistics'].get('viewCount', 0),
                    'like_count': item['statistics'].get('likeCount', 0),
                    'comment_count': item['statistics'].get('commentCount', 0),
                    'duration': item['contentDetails']['duration']
                })
        except HttpError as e:
            print(f"HTTP Error: {e}")
            break

    return stats

def get_video_comments(video_id, max_comments=100):
    comments = []
    next_page_token = None

    while len(comments) < max_comments:
        try:
            comment_params = {
                'part': 'snippet',
                'videoId': video_id,
                'maxResults': min(100, max_comments - len(comments)),
                'order': 'relevance',
                'textFormat': 'plainText',
                'pageToken': next_page_token
            }

            comment_response = youtube.commentThreads().list(**comment_params).execute()

            for item in comment_response.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'comment_id': item['id'],
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                    'like_count': comment['likeCount'],
                    'published_at': comment['publishedAt']
                })

            next_page_token = comment_response.get('nextPageToken')
            if not next_page_token:
                break

        except HttpError as e:
            if 'commentsDisabled' in str(e):
                break
            print(f"HTTP Error for video {video_id}: {e}")
            break

    return comments

def collect_youtube_data(search_query, max_videos=50, max_comments_per_video=100, published_after=None):
    print(f"Searching for videos: {search_query}")
    videos = search_videos(search_query, max_results=max_videos, published_after=published_after)
    print(f"Found {len(videos)} videos")

    video_ids = [v['video_id'] for v in videos]
    print("Getting video statistics...")
    statistics = get_video_statistics(video_ids)

    stats_dict = {s['video_id']: s for s in statistics}

    for video in videos:
        vid_id = video['video_id']
        if vid_id in stats_dict:
            video.update(stats_dict[vid_id])

    with open('youtube_videos.csv', 'w', newline='', encoding='utf-8') as f:
        if videos:
            writer = csv.DictWriter(f, fieldnames=videos[0].keys())
            writer.writeheader()
            writer.writerows(videos)
    print(f"Saved video data to youtube_videos.csv")

    all_comments = []
    print(f"Collecting comments from {len(videos)} videos...")
    for idx, video in enumerate(videos):
        print(f"Processing video {idx+1}/{len(videos)}: {video['title'][:50]}...")
        comments = get_video_comments(video['video_id'], max_comments=max_comments_per_video)
        for comment in comments:
            comment['video_id'] = video['video_id']
            comment['video_title'] = video['title']
        all_comments.extend(comments)

    if all_comments:
        with open('youtube_comments.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=all_comments[0].keys())
            writer.writeheader()
            writer.writerows(all_comments)
        print(f"Saved {len(all_comments)} comments to youtube_comments.csv")

    return videos, all_comments

if __name__ == "__main__":
    search_query = "Capital organisations during geopolitical crises" # change any topic here 
    max_videos = 500 # max 10,000 units per day for youtube
    max_comments_per_video = 100
    published_after = "2024-01-01T00:00:00Z"

    videos, comments = collect_youtube_data(
        search_query=search_query,
        max_videos=max_videos,
        max_comments_per_video=max_comments_per_video,
        published_after=published_after
    )

    print(f"\nCollection complete!")
    print(f"Total videos: {len(videos)}")
    print(f"Total comments: {len(comments)}")