# Quick Setup Guide for YouTube Video Analysis

## 🎯 Your Video
**URL**: https://www.youtube.com/watch?v=Uszj_k0DGsg  
**Video ID**: Uszj_k0DGsg

## 🚀 Setup Steps

### 1. Get YouTube API Key (2 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click "Select a project" → "NEW PROJECT" → Name it "YouTube Monitor"
4. In the search bar, search "YouTube Data API v3"
5. Click on it and press "ENABLE"
6. Go to "Credentials" → "Create Credentials" → "API Key"
7. Copy the API key (it looks like: `AIzaSy...`)

### 2. Configure the System

Edit the `.env` file:
```bash
# Replace with your actual API key
YOUTUBE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### 3. Analyze Your Video

Run the analysis:
```bash
python analyze_video.py
```

## 📊 What You'll Get

The system will provide:
- **Video Details**: Title, views, likes, comments, publish date
- **AI Summary**: Machine-generated summary of the content
- **Top Comments**: Most engaging comments from the video
- **Engagement Score**: Calculated engagement rate
- **JSON Export**: Complete analysis saved to file

## 🔧 Alternative: Web Interface

For a more visual experience:
```bash
python main.py --mode web
```

Then:
1. Open http://localhost:8501
2. Enter your API key in the sidebar
3. Paste the video URL or channel ID
4. Click "Start Monitoring"

## 🎬 Expected Output

```
📺 Analyzing Video ID: Uszj_k0DGsg
==================================================
🔍 Fetching video details...
✅ Found video: [Video Title]
👁️  Views: [number]
👍 Likes: [number] 
💬 Comments: [number]
📅 Published: [date]

💬 Fetching top comments...
✅ Found [number] comments

📝 Generating AI summary...
📊 ANALYSIS RESULTS
==================================================
🎬 Title: [Video Title]
👁️  Views: [number]
📈 Engagement: [percentage]%

🤖 AI Summary:
[AI-generated summary of the video content]

💬 Top Comments:
1. [Author]: [Comment text]...
   👍 [likes] likes
```

## 🚨 Troubleshooting

**API Key Error**: 
- Make sure YouTube Data API v3 is enabled
- Check the API key is copied correctly (no extra spaces)

**Video Not Found**:
- Video might be private or deleted
- Check if the URL is correct

**Dependencies Error**:
```bash
pip install -r requirements.txt
```

## 📁 Files Created

- `video_analysis_Uszj_k0DGsg_[timestamp].json` - Complete analysis
- `channel_state_[channel_id].json` - Monitoring state (if monitoring channels)

---

**Ready to analyze your video!** 🎥
