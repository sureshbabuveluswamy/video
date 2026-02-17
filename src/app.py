import streamlit as st
import os
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

from youtube_monitor import YouTubeMonitor
from video_summarizer import VideoSummarizer

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="YouTube Activity Monitor & Summarizer",
    page_icon="📺",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF0000;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .summary-box {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #FF0000;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">📺 YouTube Activity Monitor & Summarizer</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        api_key = st.text_input("YouTube API Key", type="password", 
                               help="Get your API key from Google Cloud Console")
        
        if api_key:
            os.environ['YOUTUBE_API_KEY'] = api_key
        
        st.subheader("Monitoring Options")
        monitor_type = st.selectbox("Monitor Type", 
                                   ["Channel", "Trending", "Search"])
        
        if monitor_type == "Channel":
            channel_id = st.text_input("Channel ID", 
                                      help="Find this in channel URL or use channel username")
            max_videos = st.slider("Max Videos", 10, 100, 50)
        
        elif monitor_type == "Trending":
            region_code = st.selectbox("Region", 
                                      ["US", "GB", "CA", "AU", "IN", "DE", "FR", "JP"])
            max_videos = st.slider("Max Videos", 10, 100, 50)
        
        else:  # Search
            search_query = st.text_input("Search Query")
            max_videos = st.slider("Max Videos", 10, 100, 50)
        
        st.subheader("Summarization Options")
        use_transcription = st.checkbox("Use Audio Transcription (Slower)", 
                                      help="Download and transcribe video audio")
        summary_length = st.slider("Summary Length", 50, 300, 150)
        
        auto_refresh = st.checkbox("Auto Refresh (minutes)")
        if auto_refresh:
            refresh_interval = st.slider("Refresh Interval", 5, 60, 15)
    
    # Main content area
    if not api_key:
        st.warning("Please enter your YouTube API Key to continue.")
        st.info("To get a YouTube API Key:")
        st.code("""
1. Go to Google Cloud Console
2. Create a new project
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Copy and paste the key here
        """)
        return
    
    # Initialize monitor and summarizer
    try:
        monitor = YouTubeMonitor(api_key)
        summarizer = VideoSummarizer()
    except Exception as e:
        st.error(f"Error initializing services: {e}")
        return
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Monitor", "📝 Summaries", "📈 Analytics"])
    
    with tab1:
        st.header("YouTube Activity Monitor")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("Start Monitoring", type="primary"):
                with st.spinner("Fetching YouTube data..."):
                    if monitor_type == "Channel" and channel_id:
                        videos = monitor.get_channel_videos(channel_id, max_videos)
                    elif monitor_type == "Trending":
                        videos = monitor.search_trending_videos(region_code, max_videos)
                    elif monitor_type == "Search" and search_query:
                        # This would require implementing search functionality
                        st.info("Search functionality coming soon!")
                        videos = []
                    else:
                        videos = []
                    
                    if videos:
                        st.session_state.videos = videos
                        st.success(f"Found {len(videos)} videos!")
                    else:
                        st.error("No videos found or error occurred.")
        
        with col2:
            if st.button("Clear Data"):
                if 'videos' in st.session_state:
                    del st.session_state.videos
                if 'summaries' in st.session_state:
                    del st.session_state.summaries
        
        # Display videos
        if 'videos' in st.session_state and st.session_state.videos:
            videos_df = pd.DataFrame(st.session_state.videos)
            
            st.subheader(f"Found {len(videos_df)} Videos")
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Videos", len(videos_df))
            with col2:
                avg_views = videos_df['view_count'].mean() if 'view_count' in videos_df.columns else 0
                st.metric("Avg Views", f"{avg_views:,.0f}")
            with col3:
                total_views = videos_df['view_count'].sum() if 'view_count' in videos_df.columns else 0
                st.metric("Total Views", f"{total_views:,.0f}")
            with col4:
                st.metric("Date Range", "Last 30 days")
            
            # Video table
            st.dataframe(
                videos_df[['title', 'published_at', 'view_count']].head(10),
                use_container_width=True
            )
    
    with tab2:
        st.header("Video Summaries")
        
        if 'videos' in st.session_state and st.session_state.videos:
            if st.button("Generate Summaries", type="primary"):
                with st.spinner("Generating summaries..."):
                    videos = st.session_state.videos
                    
                    # Get detailed video information
                    detailed_videos = []
                    for video in videos[:10]:  # Limit to 10 for demo
                        details = monitor.get_video_details(video['video_id'])
                        if details:
                            # Get comments
                            comments = monitor.get_video_comments(details['video_id'], 20)
                            details['comments'] = comments
                            detailed_videos.append(details)
                    
                    # Generate summaries
                    summaries = summarizer.batch_summarize_videos(
                        detailed_videos, 
                        use_transcription=use_transcription
                    )
                    
                    st.session_state.summaries = summaries
                    st.success(f"Generated {len(summaries)} summaries!")
        
        # Display summaries
        if 'summaries' in st.session_state and st.session_state.summaries:
            summaries = st.session_state.summaries
            
            for i, summary in enumerate(summaries):
                with st.expander(f"📹 {summary['title'][:50]}...", expanded=i==0):
                    st.markdown(f'<div class="summary-box">{summary["summary"]}</div>', 
                              unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Views", f"{summary['view_count']:,}")
                    with col2:
                        st.metric("Engagement", f"{summary['engagement_score']:.2f}%")
                    with col3:
                        st.metric("Video ID", summary['video_id'][:10])
                    
                    if 'transcription' in summary and summary['transcription']:
                        with st.expander("🎵 Audio Transcription"):
                            st.text(summary['transcription'])
    
    with tab3:
        st.header("Analytics Dashboard")
        
        if 'summaries' in st.session_state and st.session_state.summaries:
            summaries = st.session_state.summaries
            summaries_df = pd.DataFrame(summaries)
            
            # Views distribution
            if 'view_count' in summaries_df.columns:
                fig_views = px.histogram(
                    summaries_df, 
                    x='view_count', 
                    nbins=10,
                    title="View Count Distribution",
                    labels={'view_count': 'Views', 'count': 'Number of Videos'}
                )
                st.plotly_chart(fig_views, use_container_width=True)
            
            # Engagement scores
            if 'engagement_score' in summaries_df.columns:
                fig_engagement = px.scatter(
                    summaries_df,
                    x='view_count',
                    y='engagement_score',
                    title="Views vs Engagement Score",
                    labels={'view_count': 'Views', 'engagement_score': 'Engagement %'}
                )
                st.plotly_chart(fig_engagement, use_container_width=True)
            
            # Summary word cloud (simple implementation)
            st.subheader("Summary Keywords")
            all_summaries = " ".join([s['summary'] for s in summaries])
            
            # Simple word frequency
            words = all_summaries.lower().split()
            word_freq = {}
            for word in words:
                if len(word) > 3:  # Filter short words
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Display top words
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
            words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
            
            fig_words = px.bar(
                words_df,
                x='Frequency',
                y='Word',
                orientation='h',
                title="Top Keywords in Summaries"
            )
            fig_words.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_words, use_container_width=True)
        
        else:
            st.info("Generate summaries first to see analytics.")

if __name__ == "__main__":
    main()
