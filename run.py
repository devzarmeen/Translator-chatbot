"""
Quick launcher script for AI Translator Chatbot.
Run this file to start the Streamlit application.
"""

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    # Get the frontend app path
    app_path = Path(__file__).parent / "frontend" / "app.py"
    
    # Run streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])
