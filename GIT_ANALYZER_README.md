# 🔧 Git Operations Analyzer

A Streamlit web application that analyzes YouTube videos about Git and categorizes operations into Read vs Non-Read operations with AI-powered summarization.

## 🚀 Features

### 📺 Video Analysis
- **YouTube Integration**: Analyze any YouTube video about Git
- **AI Summarization**: Automatic video content summarization using transformer models
- **Comment Analysis**: Extract Git commands from video comments
- **Real-time Processing**: Fast analysis with detailed results

### 🔧 Git Operations Categorization
- **Read Operations**: View-only commands (git log, git status, git diff, etc.)
- **Non-Read Operations**: Commands that modify repository (git add, git commit, git push, etc.)
- **Smart Detection**: Automatically identifies Git commands in video content
- **Comprehensive Reference**: Built-in reference for all Git operations

### 📊 Analytics & Export
- **Statistics Dashboard**: Visual breakdown of operations found
- **JSON Export**: Download complete analysis results
- **Engagement Metrics**: View counts, likes, comments analysis
- **Operation Frequency**: Most commonly mentioned Git commands

## 🛠️ Installation

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up YouTube API Key**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable "YouTube Data API v3"
   - Create API key
   - Add to `.env` file:
   ```env
   YOUTUBE_API_KEY=your_api_key_here
   ```

## 🎯 Quick Start

### Method 1: Use the Launcher (Recommended)
```bash
python run_git_analyzer.py
```

### Method 2: Direct Streamlit
```bash
streamlit run git_operations_app.py
```

The app will open at http://localhost:8501

## 📱 How to Use

1. **Enter API Key**: Add your YouTube API key in the sidebar
2. **Paste YouTube URL**: Enter any YouTube video about Git
3. **Click Analyze**: The app will process the video and show results
4. **View Results**: See categorized Git operations and statistics
5. **Export Data**: Download analysis as JSON

## 📋 Git Operations Reference

### 📖 Read Operations (View-Only)
- `git log` - View commit history
- `git status` - Check repository status
- `git diff` - View changes between commits
- `git show` - Show commit details
- `git branch` - List branches
- `git remote -v` - Show remote repositories
- And more...

### ✏️ Non-Read Operations (Modify Repository)
- `git add` - Stage files for commit
- `git commit` - Create a new commit
- `git push` - Push changes to remote
- `git merge` - Merge branches
- `git rebase` - Rebase commits
- `git branch <name>` - Create new branch
- And more...

## 🎬 Example Analysis

Try analyzing these videos:
- https://www.youtube.com/watch?v=Uszj_k0DGsg (Git for Professionals)
- Any Git tutorial from YouTube

## 📊 Analysis Features

### Video Content Analysis
- **Title & Description**: Extract Git commands from video metadata
- **AI Summary**: Machine-generated content summary
- **Comment Mining**: Find Git commands in user comments
- **Smart Categorization**: Automatic read vs non-read classification

### Statistics Dashboard
- **Operation Count**: Total operations found by category
- **Engagement Metrics**: Video performance data
- **Comment Analysis**: Git commands mentioned in comments
- **Export Options**: JSON download for further analysis

## 🔧 Technical Details

### Components
- **YouTube Monitor**: Fetches video data and comments
- **Video Summarizer**: AI-powered content analysis
- **Git Operations Analyzer**: Categorizes Git commands
- **Streamlit Interface**: Interactive web dashboard

### AI Models Used
- **BART Transformer**: For text summarization
- **Custom Git Parser**: For command identification
- **Pattern Matching**: For operation categorization

## 🚨 Troubleshooting

### Common Issues

1. **API Key Error**:
   - Ensure YouTube Data API v3 is enabled
   - Check API key is correct and has permissions

2. **Video Not Found**:
   - Video might be private or deleted
   - Check if URL format is correct

3. **Dependencies Error**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Port Already in Use**:
   ```bash
   streamlit run git_operations_app.py --server.port 8502
   ```

## 📁 File Structure

```
Video/
├── git_operations_app.py          # Main Streamlit application
├── git_operations_analyzer.py      # Git operations classification
├── run_git_analyzer.py           # App launcher
├── src/
│   ├── youtube_monitor.py        # YouTube API integration
│   └── video_summarizer.py       # AI summarization
├── requirements.txt              # Python dependencies
└── .env                         # Environment variables
```

## 🎯 Use Cases

### For Developers
- **Learning**: Understand which Git operations are commonly used
- **Teaching**: Create educational content about Git
- **Analysis**: Analyze Git tutorials for completeness

### For Teams
- **Training**: Identify important Git operations for team training
- **Documentation**: Generate Git operation references
- **Best Practices**: Learn from professional Git tutorials

### For Content Creators
- **Research**: Analyze existing Git tutorials
- **Planning**: Identify gaps in Git education
- **Validation**: Verify coverage of Git operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the application
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**🔧 Start analyzing Git videos now!** 

Run `python run_git_analyzer.py` and visit http://localhost:8501
