#!/usr/bin/env python3
"""
YouTube Activity Monitor & Summarizer
Main entry point for the application
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from youtube_monitor import YouTubeMonitor
from video_summarizer import VideoSummarizer

def main():
    parser = argparse.ArgumentParser(description='YouTube Activity Monitor & Summarizer')
    parser.add_argument('--mode', choices=['cli', 'web'], default='web',
                       help='Run mode: CLI or Web interface')
    parser.add_argument('--channel-id', help='YouTube channel ID to monitor')
    parser.add_argument('--api-key', help='YouTube API key')
    parser.add_argument('--max-videos', type=int, default=10, 
                       help='Maximum number of videos to process')
    parser.add_argument('--use-transcription', action='store_true',
                       help='Use audio transcription for summarization')
    
    args = parser.parse_args()
    
    # Load environment variables dd
    load_dotenv()
    
    api_key = args.api_key or os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("Error: YouTube API key is required.")
        print("Set YOUTUBE_API_KEY environment variable or use --api-key argument")
        sys.exit(1)
    
    if args.mode == 'cli':
        run_cli_mode(api_key, args)
    else:
        run_web_mode()

def run_cli_mode(api_key, args):
    """Run in CLI mode"""
    print("📺 YouTube Activity Monitor & Summarizer (CLI Mode)")
    print("=" * 50)
    
    if not args.channel_id:
        print("Error: Channel ID is required for CLI mode")
        print("Use --channel-id argument")
        sys.exit(1)
    
    try:
        # Initialize services
        monitor = YouTubeMonitor(api_key)
        summarizer = VideoSummarizer()
        
        print(f"🔍 Monitoring channel: {args.channel_id}")
        print(f"📊 Max videos to process: {args.max_videos}")
        print(f"🎵 Audio transcription: {'Enabled' if args.use_transcription else 'Disabled'}")
        print()
        
        # Get videos
        print("📥 Fetching videos...")
        videos = monitor.get_channel_videos(args.channel_id, args.max_videos)
        
        if not videos:
            print("❌ No videos found or error occurred")
            return
        
        print(f"✅ Found {len(videos)} videos")
        print()
        
        # Get detailed information
        print("📋 Getting video details...")
        detailed_videos = []
        for i, video in enumerate(videos, 1):
            print(f"Processing video {i}/{len(videos)}: {video['title'][:50]}...")
            details = monitor.get_video_details(video['video_id'])
            if details:
                comments = monitor.get_video_comments(details['video_id'], 20)
                details['comments'] = comments
                detailed_videos.append(details)
        
        print(f"✅ Got details for {len(detailed_videos)} videos")
        print()
        
        # Generate summaries
        print("📝 Generating summaries...")
        summaries = summarizer.batch_summarize_videos(
            detailed_videos, 
            use_transcription=args.use_transcription
        )
        
        print(f"✅ Generated {len(summaries)} summaries")
        print()
        
        # Display results
        print("📊 RESULTS")
        print("=" * 50)
        
        for i, summary in enumerate(summaries, 1):
            print(f"\n📹 Video {i}: {summary['title']}")
            print(f"👁️  Views: {summary['view_count']:,}")
            print(f"💬 Engagement: {summary['engagement_score']:.2f}%")
            print(f"📄 Summary:")
            print(f"   {summary['summary']}")
            print("-" * 50)
        
        # Save results
        import json
        output_file = f"youtube_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(summaries, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def run_web_mode():
    """Run in web mode using Streamlit"""
    print("🌐 Starting web interface...")
    print("Open http://localhost:8501 in your browser")
    
    import subprocess
    import sys
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        os.path.join("src", "app.py"),
        "--server.port", "8501",
        "--server.address", "localhost"
    ])

if __name__ == "__main__":
    main()
