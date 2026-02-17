#!/usr/bin/env python3
"""
Analyze a specific YouTube video
"""

import os
import sys
import json
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from youtube_monitor import YouTubeMonitor
from video_summarizer import VideoSummarizer
from dotenv import load_dotenv

def analyze_video(video_url: str):
    """Analyze a specific YouTube video"""
    
    # Load environment variables
    load_dotenv()
    
    # Extract video ID from URL
    if 'v=' in video_url:
        video_id = video_url.split('v=')[1].split('&')[0] if '&' in video_url.split('v=')[1] else video_url.split('v=')[1]
    else:
        print("Invalid YouTube URL format")
        return
    
    print(f"📺 Analyzing Video ID: {video_id}")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("❌ Error: YouTube API key not found")
        print("Please set YOUTUBE_API_KEY in your .env file")
        print("You can get one from: https://console.cloud.google.com/")
        return
    
    try:
        # Initialize services
        monitor = YouTubeMonitor(api_key)
        summarizer = VideoSummarizer()
        
        print("🔍 Fetching video details...")
        
        # Get video details
        video_details = monitor.get_video_details(video_id)
        
        if not video_details:
            print("❌ Could not fetch video details. The video might be private or not exist.")
            return
        
        print(f"✅ Found video: {video_details['title']}")
        print(f"👁️  Views: {video_details['view_count']:,}")
        print(f"👍 Likes: {video_details['like_count']:,}")
        print(f"💬 Comments: {video_details['comment_count']:,}")
        print(f"📅 Published: {video_details['published_at']}")
        print()
        
        # Get comments
        print("💬 Fetching top comments...")
        comments = monitor.get_video_comments(video_id, 50)
        video_details['comments'] = comments
        print(f"✅ Found {len(comments)} comments")
        print()
        
        # Generate summary
        print("📝 Generating AI summary...")
        summary = summarizer.summarize_video_metadata(video_details)
        
        print("📊 ANALYSIS RESULTS")
        print("=" * 50)
        print(f"🎬 Title: {summary['title']}")
        print(f"👁️  Views: {summary['view_count']:,}")
        print(f"📈 Engagement: {summary['engagement_score']:.2f}%")
        print()
        print("🤖 AI Summary:")
        print(summary['summary'])
        print()
        
        # Show top comments
        if comments:
            print("💬 Top Comments:")
            for i, comment in enumerate(comments[:5], 1):
                print(f"{i}. {comment['author']}: {comment['text'][:100]}...")
                print(f"   👍 {comment['like_count']} likes")
            print()
        
        # Save results
        results = {
            'video_url': video_url,
            'video_id': video_id,
            'analysis_date': datetime.now().isoformat(),
            'video_details': video_details,
            'summary': summary
        }
        
        output_file = f"video_analysis_{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Results saved to: {output_file}")
        
        return results
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    # Use the video URL from the user
    video_url = "https://www.youtube.com/watch?v=Uszj_k0DGsg"
    analyze_video(video_url)
