import os
import torch
import whisper
import ffmpeg
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from typing import Dict, List, Optional
import requests
from urllib.parse import urlparse
import tempfile
import json

class VideoSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """Initialize the summarization model"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.summarizer = pipeline(
            "summarization",
            model=model_name,
            tokenizer=model_name,
            device=0 if self.device == "cuda" else -1
        )
        
        # Initialize Whisper for transcription
        self.whisper_model = whisper.load_model("base")
        
    def transcribe_audio(self, video_path: str) -> str:
        """Extract and transcribe audio from video"""
        try:
            # Extract audio using ffmpeg
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                (
                    ffmpeg
                    .input(video_path)
                    .output(temp_audio.name, acodec='pcm_s16le', ac=1, ar='16000')
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )
                
                # Transcribe using Whisper
                result = self.whisper_model.transcribe(temp_audio.name)
                os.unlink(temp_audio.name)
                
                return result['text']
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return ""
    
    def download_video_audio(self, video_url: str, output_path: str) -> str:
        """Download video from YouTube (requires yt-dlp)"""
        try:
            import yt_dlp
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192',
                }],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            return output_path.replace('.mp3', '.wav')
        except ImportError:
            print("yt-dlp not installed. Install with: pip install yt-dlp")
            return ""
        except Exception as e:
            print(f"Error downloading video: {e}")
            return ""
    
    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """Summarize text using the ML model"""
        try:
            if len(text) < 50:
                return text
            
            # Split long texts into chunks
            max_chunk_size = 1024
            if len(text) > max_chunk_size:
                chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
                summaries = []
                
                for chunk in chunks:
                    summary = self.summarizer(
                        chunk,
                        max_length=max_length // len(chunks) + 20,
                        min_length=min_length // len(chunks) + 10,
                        do_sample=False
                    )
                    summaries.append(summary[0]['summary_text'])
                
                return " ".join(summaries)
            else:
                summary = self.summarizer(
                    text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                return summary[0]['summary_text']
        except Exception as e:
            print(f"Error summarizing text: {e}")
            return text[:max_length] + "..." if len(text) > max_length else text
    
    def summarize_video_metadata(self, video_data: Dict) -> Dict:
        """Summarize video based on metadata (title, description, comments)"""
        combined_text = f"Title: {video_data.get('title', '')}\n\n"
        combined_text += f"Description: {video_data.get('description', '')}\n\n"
        
        # Add top comments if available
        if 'comments' in video_data and video_data['comments']:
            combined_text += "Top Comments:\n"
            for comment in video_data['comments'][:5]:  # Top 5 comments
                combined_text += f"- {comment.get('text', '')}\n"
        
        summary = self.summarize_text(combined_text)
        
        return {
            'video_id': video_data.get('video_id'),
            'title': video_data.get('title'),
            'summary': summary,
            'view_count': video_data.get('view_count', 0),
            'engagement_score': self._calculate_engagement_score(video_data)
        }
    
    def summarize_video_content(self, video_url: str, video_data: Dict) -> Dict:
        """Summarize video content including audio transcription"""
        # Download and transcribe
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            audio_path = self.download_video_audio(video_url, temp_file.name)
            
            if audio_path and os.path.exists(audio_path):
                transcription = self.transcribe_audio(audio_path)
                os.unlink(audio_path)
            else:
                transcription = ""
        
        # Combine transcription with metadata
        combined_text = f"Title: {video_data.get('title', '')}\n\n"
        combined_text += f"Description: {video_data.get('description', '')}\n\n"
        
        if transcription:
            combined_text += f"Transcription: {transcription}\n\n"
        
        # Add comments if available
        if 'comments' in video_data and video_data['comments']:
            combined_text += "Top Comments:\n"
            for comment in video_data['comments'][:10]:
                combined_text += f"- {comment.get('text', '')}\n"
        
        summary = self.summarize_text(combined_text, max_length=200, min_length=80)
        
        return {
            'video_id': video_data.get('video_id'),
            'title': video_data.get('title'),
            'summary': summary,
            'transcription': transcription[:500] + "..." if len(transcription) > 500 else transcription,
            'view_count': video_data.get('view_count', 0),
            'engagement_score': self._calculate_engagement_score(video_data)
        }
    
    def _calculate_engagement_score(self, video_data: Dict) -> float:
        """Calculate engagement score based on likes, comments, and views"""
        views = video_data.get('view_count', 0)
        likes = video_data.get('like_count', 0)
        comments = video_data.get('comment_count', 0)
        
        if views == 0:
            return 0.0
        
        # Engagement rate = (likes + comments) / views * 100
        engagement_rate = ((likes + comments) / views) * 100
        return round(engagement_rate, 2)
    
    def batch_summarize_videos(self, videos: List[Dict], use_transcription: bool = False) -> List[Dict]:
        """Summarize multiple videos"""
        summaries = []
        
        for video in videos:
            if use_transcription and 'url' in video:
                summary = self.summarize_video_content(video['url'], video)
            else:
                summary = self.summarize_video_metadata(video)
            
            summaries.append(summary)
        
        return summaries
