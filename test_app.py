import streamlit as st

st.set_page_config(page_title="Test App", page_icon="🧪", layout="wide")

st.title("🧪 Git Operations Analyzer - Test")
st.write("This is a test to ensure the app works!")

if st.button("Test Button"):
    st.success("✅ App is working!")

st.write("Enter a YouTube URL to test:")
url = st.text_input("YouTube URL:")
if url:
    st.write(f"URL entered: {url}")

# Test Git operations analyzer
try:
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from git_operations_analyzer import GitOperationsAnalyzer
    
    analyzer = GitOperationsAnalyzer()
    st.write("✅ Git Operations Analyzer loaded successfully!")
    
    # Test analysis
    test_text = "git add and git commit are important"
    result = analyzer.analyze_text_for_git_operations(test_text)
    st.write("Test analysis result:", result)
    
except Exception as e:
    st.error(f"❌ Error: {e}")
