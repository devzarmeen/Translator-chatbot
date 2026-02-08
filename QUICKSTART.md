# 🚀 Quick Start Guide

## Installation (5 minutes)

1. **Install Python 3.8+** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)

2. **Install Tesseract OCR** (for OCR features)
   - Windows: [Download installer](https://github.com/UB-Mannheim/tesseract/wiki)
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

3. **Clone/Navigate to project**
   ```bash
   cd e:\Translator
   ```

4. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Configure environment**
   ```bash
   copy .env.example .env
   ```
   Edit `.env` and add your OpenAI API key (optional but recommended):
   ```
   OPENAI_API_KEY=your_key_here
   ```

## Running the App

**Option 1: Using run script**
```bash
python run.py
```

**Option 2: Direct Streamlit command**
```bash
streamlit run frontend/app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## First Steps

1. **Select target language** from sidebar
2. **Type a message** in any language
3. **See automatic translation** with detected source language
4. **Try voice input** - Upload audio file
5. **Try OCR** - Upload image with text
6. **Enable features**:
   - Auto-English Mode
   - Simplifier Mode
   - Language Lock

## Features Overview

- ✅ **Text Translation**: Type and translate instantly
- ✅ **Voice Input**: Upload audio files for transcription + translation
- ✅ **OCR**: Extract text from images and translate
- ✅ **TTS**: Listen to translations with accent selection
- ✅ **Bookmarks**: Save important translations
- ✅ **Simplifier**: Convert complex text to beginner-friendly
- ✅ **Dark Mode**: Toggle theme

## Troubleshooting

**App won't start?**
- Check Python version: `python --version` (need 3.8+)
- Verify dependencies: `pip list`
- Check for errors in terminal

**OCR not working?**
- Install Tesseract OCR
- Set `TESSERACT_CMD` in `.env` if custom location

**Simplifier not working?**
- Add OpenAI API key to `.env` file
- Get key from: https://platform.openai.com/api-keys

**Translation errors?**
- Check internet connection (Google Translate needs internet)
- Some languages may have limited support

---

**Need help?** Check the full [README.md](README.md) for detailed documentation.
