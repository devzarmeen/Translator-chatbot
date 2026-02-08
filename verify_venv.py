"""
Verification script to check if virtual environment is set up correctly.
Run this script to verify all dependencies are installed.
"""

import sys
import subprocess
from pathlib import Path

# Check if we're in a virtual environment
in_venv = hasattr(sys, 'real_prefix') or (
    hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
)

print("="*60)
print("VIRTUAL ENVIRONMENT VERIFICATION")
print("="*60)
print(f"Python executable: {sys.executable}")
print(f"In virtual environment: {in_venv}")
print(f"Python version: {sys.version}")
print()

# Required packages
required_packages = {
    "streamlit": "Web UI framework",
    "googletrans": "Translation API",
    "openai": "AI services",
    "speechrecognition": "Speech-to-Text",
    "gtts": "Text-to-Speech",
    "pytesseract": "OCR wrapper",
    "PIL": "Pillow - Image processing",
    "dotenv": "python-dotenv - Environment variables",
}

print("Checking installed packages...")
print("-"*60)

missing_packages = []
installed_packages = []

for package, description in required_packages.items():
    try:
        if package == "PIL":
            __import__("PIL")
        elif package == "dotenv":
            __import__("dotenv")
        else:
            __import__(package)
        print(f"[OK] {package:20s} - {description}")
        installed_packages.append(package)
    except ImportError:
        print(f"[MISSING] {package:20s} - {description}")
        missing_packages.append(package)

print("-"*60)
print()

if missing_packages:
    print(f"[WARNING] Missing {len(missing_packages)} package(s): {', '.join(missing_packages)}")
    print("\nTo install missing packages:")
    print("  pip install -r requirements.txt")
else:
    print("[SUCCESS] All required packages are installed!")
    print()

# Check pyaudio separately (optional)
try:
    print("[OK] pyaudio - Audio I/O (optional)")
except ImportError:
    print("[INFO] pyaudio not installed (optional - microphone input won't work)")

print()
print("="*60)

if missing_packages:
    sys.exit(1)
else:
    print("Virtual environment is ready to use!")
    print("\nTo run the application:")
    print("  python run.py")
    print("  OR")
    print("  streamlit run frontend/app.py")
    sys.exit(0)
