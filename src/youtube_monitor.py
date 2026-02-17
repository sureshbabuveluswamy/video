import os
import json
import time
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from typing import List, Dict, Optional

class YouTubeMonitor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        
    def get_channel_videos(self, channel_id: str, max_results: int = 50) -> List[Dict]:
        """Get recent videos from a channel"""
        try:
            response = self.youtube.search().list(
                part='id,snippet',
                channelId=channel_id,
                maxResults=max_results,
                order='date',
                type='video'
            ).execute()
            
            videos = []
            for item in response['items']:
                video_data = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'published_at': item['snippet']['publishedAt'],
                    'thumbnail_url': item['snippet']['thumbnails']['high']['url']
                }
                videos.append(video_data)
            
            return videos
        except HttpError as e:
            print(f"Error fetching videos: {e}")
            return []
    
    def get_video_details(self, video_id: str) -> Dict:
        """Get detailed information about a specific video"""
        try:
            response = self.youtube.videos().list(
                part='statistics,contentDetails,snippet',
                id=video_id
            ).execute()
            
            if not response['items']:
                return {}
            
            video = response['items'][0]
            return {
                'video_id': video['id'],
                'title': video['snippet']['title'],
                'description': video['snippet']['description'],
                'published_at': video['snippet']['publishedAt'],
                'duration': video['contentDetails']['duration'],
                'view_count': int(video['statistics'].get('viewCount', 0)),
                'like_count': int(video['statistics'].get('likeCount', 0)),
                'comment_count': int(video['statistics'].get('commentCount', 0)),
                'tags': video['snippet'].get('tags', [])
            }
        except HttpError as e:
            print(f"Error fetching video details: {e}")
            return {}
    
    def get_video_comments(self, video_id: str, max_comments: int = 100) -> List[Dict]:
        """Get comments from a video"""
        try:
            response = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=max_comments,
                order='relevance'
            ).execute()
            
            comments = []
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                    'like_count': comment['likeCount'],
                    'published_at': comment['publishedAt']
                })
            
            return comments
        except HttpError as e:
            print(f"Error fetching comments: {e}")
            return []
    
    def search_trending_videos(self, region_code: str = 'US', max_results: int = 50) -> List[Dict]:
        """Get trending videos"""
        try:
            response = self.youtube.videos().list(
                part='snippet,statistics',
                chart='mostPopular',
                regionCode=region_code,
                maxResults=max_results
            ).execute()
            
            videos = []
            for item in response['items']:
                video_data = {
                    'video_id': item['id'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'published_at': item['snippet']['publishedAt'],
                    'view_count': int(item['statistics'].get('viewCount', 0)),
                    'like_count': int(item['statistics'].get('likeCount', 0)),
                    'comment_count': int(item['statistics'].get('commentCount', 0)),
                    'tags': item['snippet'].get('tags', [])
                }
                videos.append(video_data)
            
            return videos
        except HttpError as e:
            print(f"Error fetching trending videos: {e}")
            return []
    
    def monitor_channel_activity(self, channel_id: str, interval_minutes: int = 60) -> Dict:
        """Monitor channel for new activity"""
        current_videos = self.get_channel_videos(channel_id)
        
        # Load previous state if exists
        state_file = f"channel_state_{channel_id}.json"
        previous_videos = []
        
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                previous_data = json.load(f)
                previous_videos = previous_data.get('videos', [])
        
        # Find new videos
        previous_ids = {v['video_id'] for v in previous_videos}
        new_videos = [v for v in current_videos if v['video_id'] not in previous_ids]
        
        # Update state
        with open(state_file, 'w') as f:
            json.dump({'videos': current_videos, 'last_check': datetime.now().isoformat()}, f)
        
        return {
            'new_videos': new_videos,
            'total_videos': len(current_videos),
            'last_check': datetime.now().isoformat()
        }
