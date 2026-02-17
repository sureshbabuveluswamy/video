import streamlit as st
import sys
import os
import re
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from youtube_monitor import YouTubeMonitor
from video_summarizer import VideoSummarizer
from os_commands_analyzer import OSCommandsAnalyzer
from keystroke_detector import KeystrokeDetector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="OS Commands Analyzer",
    page_icon="�",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0078D4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .operation-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #007acc;
    }
    .read-operation {
        border-left-color: #28a745;
    }
    .non-read-operation {
        border-left-color: #dc3545;
    }
    .summary-box {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #0078D4;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL"""
    if not url:
        return ""
    
    # Handle different YouTube URL formats
    import re
    
    # Standard format: https://www.youtube.com/watch?v=VIDEO_ID
    # Shorts format: https://www.youtube.com/shorts/VIDEO_ID
    # Embed format: https://www.youtube.com/embed/VIDEO_ID
    # youtu.be format: https://youtu.be/VIDEO_ID
    pattern1 = r'(?:youtube\.com/watch\?v=|youtube\.com/shorts/|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern1, url)
    
    if match:
        return match.group(1)
    
    # Fallback for basic v= parameter
    if 'v=' in url:
        video_id = url.split('v=')[1]
        return video_id.split('&')[0] if '&' in video_id else video_id
    
    return ""

def main():
    st.markdown('<h1 class="main-header">� OS Commands Analyzer</h1>', unsafe_allow_html=True)
    
    # Initialize analyzer
    os_analyzer = OSCommandsAnalyzer()
    keystroke_detector = KeystrokeDetector()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Auto-load API key from .env file
        api_key = os.getenv('YOUTUBE_API_KEY')
        
        if api_key:
            st.success("✅ YouTube API Key configured")
        else:
            st.error("❌ YouTube API Key not found")
            st.warning("Please add YOUTUBE_API_KEY to your .env file")
            st.info("Get your API key from Google Cloud Console")
            return
        
        st.subheader("Analysis Options")
        show_all_commands = st.checkbox("Show All OS Commands Reference", False)
        analyze_comments = st.checkbox("Analyze Comments for OS Commands", True)
        capture_keystrokes = st.checkbox("Capture All Keystrokes", True)
        
        st.subheader("Filter Commands")
        filter_read_commands = st.checkbox("Show Read Commands", True)
        filter_non_read_commands = st.checkbox("Show Non-Read Commands", True)
        filter_admin_commands = st.checkbox("Show Admin Commands", True)
        
        st.subheader("About")
        st.info("""
        This app analyzes YouTube videos 
        about operating systems and categorizes commands 
        into Read vs Non-Read operations.
        """)

    # Main content area
    # API key is already loaded and validated in sidebar

    # URL input section
    st.header("📺 YouTube Video Analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        video_url = st.text_input("Enter YouTube URL:", 
                                 placeholder="https://www.youtube.com/watch?v=...",
                                 help="Enter any YouTube video about OS commands (Linux, Unix, Windows, Ubuntu, etc.)")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button("Analyze Video", type="primary")

    # Show all operations reference
    if show_all_commands:
        st.header("📚 OS Commands Reference")
        
        # Get commands based on OS filter
        if os_filter == "Linux/Unix":
            commands = os_analyzer.get_commands_by_os('linux')
        elif os_filter == "Windows":
            commands = os_analyzer.get_commands_by_os('windows')
        else:
            commands = os_analyzer.get_command_summary()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📖 Read Operations")
            for op, desc in commands['read_operations'].items():
                st.markdown(f'<div class="operation-card read-operation"><code>{op}</code><br><small>{desc}</small></div>', 
                          unsafe_allow_html=True)
        
        with col2:
            st.subheader("✏️ Non-Read Operations")
            for op, desc in commands['non_read_operations'].items():
                st.markdown(f'<div class="operation-card non-read-operation"><code>{op}</code><br><small>{desc}</small></div>', 
                          unsafe_allow_html=True)

    # Analyze video if URL provided
    if video_url and analyze_button:
        video_id = extract_video_id(video_url)
        
        if not video_id:
            st.error("Invalid YouTube URL format")
            return
        
        st.header(f"📊 Analysis Results")
        
        try:
            # Initialize services
            monitor = YouTubeMonitor(api_key)
            summarizer = VideoSummarizer()
            
            with st.spinner("Fetching video details..."):
                # Get video details
                video_details = monitor.get_video_details(video_id)
                
                if not video_details:
                    st.error("Could not fetch video details. The video might be private or not exist.")
                    return
                
                # Get comments if enabled
                comments = []
                if analyze_comments:
                    comments = monitor.get_video_comments(video_id, 50)
                    video_details['comments'] = comments
            
            # Display video information (no view count focus)
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Title", video_details['title'][:50] + "..." if len(video_details['title']) > 50 else video_details['title'])
            
            with col2:
                st.metric("Comments", len(comments))
            
            # Generate summary
            with st.spinner("Generating AI summary..."):
                summary = summarizer.summarize_video_metadata(video_details)
            
            st.markdown(f'<div class="summary-box"><h3>🤖 AI Summary</h3>{summary["summary"]}</div>', 
                      unsafe_allow_html=True)
            
            # Analyze for OS commands
            st.header("🔍 OS Commands Analysis")
            
            # Combine text for analysis
            analysis_text = f"{video_details.get('title', '')} {video_details.get('description', '')} {summary.get('summary', '')}"
            
            # Add comments to analysis if enabled
            if analyze_comments and comments:
                comment_text = " ".join([comment['text'] for comment in comments[:20]])
                analysis_text += " " + comment_text
            
            # Analyze operations
            operations_found = os_analyzer.analyze_text_for_os_commands(analysis_text)
            
            # Analyze admin commands if enabled
            admin_commands_found = []
            if filter_admin_commands:
                admin_commands_found = os_analyzer.analyze_text_for_admin_commands(analysis_text)
            
            # Display results with filtering
            if filter_read_commands or filter_non_read_commands or filter_admin_commands:
                if filter_read_commands:
                    with col1:
                        st.subheader("📖 Read Operations Found")
                        if operations_found['read_operations']:
                            for op in operations_found['read_operations']:
                                st.markdown(f'<div class="operation-card read-operation">{op}</div>', 
                                          unsafe_allow_html=True)
                        else:
                            st.info("No read operations found in the video content")
                
                if filter_non_read_commands:
                    with col2:
                        st.subheader("✏️ Non-Read Operations Found")
                        if operations_found['non_read_operations']:
                            for op in operations_found['non_read_operations']:
                                st.markdown(f'<div class="operation-card non-read-operation">{op}</div>', 
                                          unsafe_allow_html=True)
                        else:
                            st.info("No non-read operations found in the video content")
                
                if filter_admin_commands and admin_commands_found:
                    st.subheader("🔐 Admin Commands Found")
                    for op in admin_commands_found:
                        st.markdown(f'<div class="operation-card non-read-operation">{op}</div>', 
                                  unsafe_allow_html=True)
            else:
                st.info("Please select at least one command type to display")
            
            # Summary statistics
            st.header("📈 Analysis Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Read Operations", len(operations_found['read_operations']))
            
            with col2:
                st.metric("Non-Read Operations", len(operations_found['non_read_operations']))
            
            with col3:
                total_ops = len(operations_found['read_operations']) + len(operations_found['non_read_operations'])
                st.metric("Total Operations", total_ops)
            
            with col4:
                if total_ops > 0:
                    non_read_percentage = (len(operations_found['non_read_operations']) / total_ops) * 100
                    st.metric("Non-Read %", f"{non_read_percentage:.1f}%")
                else:
                    st.metric("Non-Read %", "0%")
            
            # Keystroke Analysis
            if capture_keystrokes:
                st.header("⌨️ Keystroke Analysis")
                
                with st.spinner("Analyzing keystrokes..."):
                    # Prepare video data for keystroke analysis
                    video_data_for_keystrokes = {
                        'title': video_details.get('title', ''),
                        'description': video_details.get('description', ''),
                        'summary': summary.get('summary', ''),
                        'comments': comments if analyze_comments else []
                    }
                    
                    keystroke_analysis = keystroke_detector.analyze_video_content(video_data_for_keystrokes)
                    keystroke_stats = keystroke_detector.get_keystroke_statistics(keystroke_analysis)
                
                # Display keystroke statistics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Keystrokes", keystroke_stats['total_events'])
                
                with col2:
                    st.metric("Keyboard Shortcuts", keystroke_stats['keyboard_shortcuts'])
                
                with col3:
                    st.metric("Typed Commands", keystroke_stats['typed_commands'])
                
                with col4:
                    st.metric("File Operations", keystroke_stats['file_operations'])
                
                # OS Detection
                os_detection = keystroke_stats['operating_system_hints']
                st.subheader("🖥️ Operating System Detection")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Detected OS", f"{os_detection['detected_os']} ({os_detection['confidence']:.0%})")
                
                with col2:
                    st.write("OS Scores:")
                    for os_name, score in os_detection['scores'].items():
                        st.write(f"- {os_name}: {score}")
                
                # Most common commands
                if keystroke_stats['most_common_commands']:
                    st.subheader("🔥 Most Common Commands")
                    for cmd_info in keystroke_stats['most_common_commands'][:10]:
                        st.write(f"- **{cmd_info['command']}** ({cmd_info['count']} times)")
                
                # Detailed keystroke events
                st.subheader("⌨️ Detailed Keystroke Events")
                
                # Tabs for different types of keystrokes
                tab1, tab2, tab3, tab4 = st.tabs(["All Events", "Shortcuts", "Commands", "File Ops"])
                
                with tab1:
                    if keystroke_analysis['keystroke_events']:
                        for i, event in enumerate(keystroke_analysis['keystroke_events'][:20], 1):
                            with st.expander(f"Event {i}: {event.command} (Confidence: {event.confidence:.0%})"):
                                st.write(f"**Command:** {event.command}")
                                st.write(f"**Context:** {event.context}")
                                st.write(f"**Confidence:** {event.confidence:.0%}")
                    else:
                        st.info("No keystroke events detected")
                
                with tab2:
                    if keystroke_analysis['keyboard_shortcuts']:
                        for event in keystroke_analysis['keyboard_shortcuts']:
                            st.markdown(f'<div class="operation-card read-operation"><code>{event.command}</code><br><small>{event.context}</small></div>', 
                                      unsafe_allow_html=True)
                    else:
                        st.info("No keyboard shortcuts detected")
                
                with tab3:
                    if keystroke_analysis['typed_commands']:
                        for event in keystroke_analysis['typed_commands']:
                            st.markdown(f'<div class="operation-card non-read-operation"><code>{event.command}</code><br><small>{event.context}</small></div>', 
                                      unsafe_allow_html=True)
                    else:
                        st.info("No typed commands detected")
                
                with tab4:
                    if keystroke_analysis['file_operations']:
                        for event in keystroke_analysis['file_operations']:
                            st.markdown(f'<div class="operation-card non-read-operation"><code>{event.command}</code><br><small>{event.context}</small></div>', 
                                      unsafe_allow_html=True)
                    else:
                        st.info("No file operations detected")
            
            # Comments analysis if enabled
            if analyze_comments and comments:
                st.header("💬 Comments Analysis")
                
                # Show comments that mention OS commands
                os_commands = ['ls', 'cat', 'cd', 'mkdir', 'rm', 'cp', 'mv', 'chmod', 'grep', 'find', 'ps', 'kill', 'dir', 'type', 'del', 'copy', 'move', 'powershell']
                os_comments = []
                for comment in comments:
                    comment_lower = comment['text'].lower()
                    if any(cmd in comment_lower for cmd in os_commands):
                        os_comments.append(comment)
                
                if os_comments:
                    st.write(f"Found {len(os_comments)} comments mentioning OS commands:")
                    for i, comment in enumerate(os_comments[:10], 1):
                        with st.expander(f"Comment {i}: {comment['author']} ({comment['like_count']} likes)"):
                            st.write(comment['text'])
                else:
                    st.info("No comments mentioning OS commands found")
            
            # Export results
            st.header("💾 Export Results")
            
            results = {
                'video_url': video_url,
                'video_id': video_id,
                'analysis_date': datetime.now().isoformat(),
                'video_details': video_details,
                'summary': summary,
                'os_commands_found': operations_found,
                'keystroke_analysis': keystroke_analysis if capture_keystrokes else None,
                'keystroke_statistics': keystroke_stats if capture_keystrokes else None,
                'statistics': {
                    'read_operations_count': len(operations_found['read_operations']),
                    'non_read_operations_count': len(operations_found['non_read_operations']),
                    'total_operations': len(operations_found['read_operations']) + len(operations_found['non_read_operations']),
                    'total_keystrokes': keystroke_stats['total_events'] if capture_keystrokes else 0
                }
            }
            
            # Download button
            if st.button("Download Analysis as JSON"):
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(results, indent=2),
                    file_name=f"os_analysis_{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
        except Exception as e:
            st.error(f"Error analyzing video: {e}")

if __name__ == "__main__":
    main()
