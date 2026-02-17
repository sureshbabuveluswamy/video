# YouTube Activity Monitor & Summarizer

A machine learning-powered system to monitor YouTube activity and generate intelligent summaries of video content.

## Features

- **YouTube API Integration**: Monitor channels, trending videos, and search results
- **AI-Powered Summarization**: Uses transformer models (BART) for text summarization
- **Audio Transcription**: Optional Whisper-based audio transcription for deeper analysis
- **Web Interface**: Beautiful Streamlit dashboard for monitoring and analytics
- **CLI Support**: Command-line interface for automated monitoring
- **Real-time Analytics**: Engagement metrics, view statistics, and keyword analysis

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Video
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Install additional system dependencies:
```bash
# For macOS
brew install ffmpeg

# For Ubuntu/Debian
sudo apt-get install ffmpeg

# For audio transcription (optional)
pip install yt-dlp
```

## Getting API Keys

### YouTube Data API v3
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "YouTube Data API v3"
4. Create credentials → API Key
5. Copy the API key to your `.env` file

### OpenAI API (Optional, for alternative models)
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an API key
3. Add to your `.env` file

## Usage

### Web Interface (Recommended)

Start the web application:
```bash
python main.py --mode web
```

Then open http://localhost:8501 in your browser.

### CLI Interface

Monitor a specific channel:
```bash
python main.py --mode cli --channel-id UCxxxxxxxxxxxx --max-videos 20
```

With audio transcription:
```bash
python main.py --mode cli --channel-id UCxxxxxxxxxxxx --use-transcription
```

### Using Your Own API Key

```bash
python main.py --api-key YOUR_API_KEY --channel-id UCxxxxxxxxxxxx
```

## Project Structure

```
Video/
├── src/
│   ├── youtube_monitor.py    # YouTube API integration
│   ├── video_summarizer.py   # ML summarization models
│   └── app.py               # Streamlit web interface
├── main.py                  # Entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Features Explained

### Monitoring Capabilities
- **Channel Monitoring**: Track new videos from specific channels
- **Trending Videos**: Monitor trending content by region
- **Search Monitoring**: Track videos matching specific keywords
- **Activity Detection**: Identify new content and engagement changes

### Summarization Methods
1. **Metadata Summarization**: Fast analysis using titles, descriptions, and comments
2. **Content Summarization**: Deep analysis with audio transcription
3. **Batch Processing**: Handle multiple videos efficiently

### Analytics Dashboard
- View count distributions
- Engagement rate analysis
- Keyword extraction from summaries
- Trending topics identification

## Configuration Options

### Summarization Models
- Default: `facebook/bart-large-cnn`
- Alternative: `t5-small`, `t5-base`, `pegasus-xsum`

### Transcription Models
- Default: Whisper `base` model
- Alternatives: `small`, `medium`, `large` (requires more resources)

## API Limits

- YouTube API: 10,000 units per day (default quota)
- Rate limiting implemented to prevent quota exhaustion
- Batch processing reduces API calls

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure YouTube Data API v3 is enabled
   - Check API key is correct and has proper permissions

2. **FFmpeg Error**
   - Install FFmpeg for audio processing
   - Ensure FFmpeg is in your PATH

3. **Memory Issues**
   - Reduce batch size for processing
   - Use smaller models for transcription

4. **Network Issues**
   - Check internet connection
   - Verify API endpoints are accessible

### Performance Tips

- Use metadata summarization for faster processing
- Limit concurrent video processing
- Cache results to avoid reprocessing
- Use GPU for ML models when available

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation
- Open an issue on GitHub

---

**Note**: This tool is for educational and research purposes. Please respect YouTube's Terms of Service and API usage policies.
