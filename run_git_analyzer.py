#!/usr/bin/env python3
"""
Git Operations Analyzer - Streamlit App Launcher
"""

import subprocess
import sys
import os

def main():
    print("🔧 Starting Git Operations Analyzer...")
    print("📺 This app analyzes YouTube videos for Git operations")
    print("🌐 Opening web interface at http://localhost:8501")
    print()
    print("Features:")
    print("- Analyze any YouTube video about Git")
    print("- Categorize operations into Read vs Non-Read")
    print("- AI-powered video summarization")
    print("- Comment analysis for Git commands")
    print("- Export results as JSON")
    print()
    print("⚠️  Make sure you have a YouTube API key ready!")
    print()
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "git_operations_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        print("Make sure you have all dependencies installed:")
        print("pip install streamlit google-api-python-client transformers torch")

if __name__ == "__main__":
    main()
