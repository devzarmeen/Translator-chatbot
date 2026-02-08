# 🌐 AI Translator Chatbot

A complete, production-ready AI Translator Chatbot that combines advanced Google Translate functionality with AI assistance. Built with Python and Streamlit, featuring automatic language detection, voice input/output, OCR capabilities, and intelligent text simplification.

## ✨ Features

### Core Translation Features
- **Automatic Language Detection**: Automatically detects the language of input text and voice
- **Multi-language Translation**: Translate between 100+ languages
- **Auto-Translate-to-English Mode**: Automatically translate all input to English
- **Language Lock Mode**: Lock bot responses to a specific language until changed

### Voice Features
- **Speech-to-Text (STT)**: Convert voice input to text using Google Speech Recognition or OpenAI Whisper
- **Text-to-Speech (TTS)**: Convert translated text to speech with selectable accents:
  - British English
  - American English
  - Neutral (Australian)

### OCR Features
- **Image-to-Text Extraction**: Extract text from images using OCR
- **OCR Translation**: Translate extracted text automatically
- **OCR Read Aloud**: Read extracted text using TTS
- **OCR Copy**: Copy extracted text to clipboard

### AI Features
- **Simplifier Mode**: Convert complex text into easy, beginner-friendly language using OpenAI
- **Context-Aware Responses**: Maintains conversation context for better translations
- **Regenerate Response**: Regenerate translations with context awareness

### User Experience Features
- **Session-Based Memory**: Maintains conversation history throughout the session
- **Bookmark System**: Save important translations for later reference
- **Action Buttons**: For each response:
  - 👍 Like / 👎 Dislike
  - 🔄 Regenerate
  - 📋 Copy Text
  - 🔊 Read Aloud
  - ⭐ Bookmark
- **Dark Mode Toggle**: Switch between light and dark themes
- **Conversation Reset**: Clear conversation history
- **Export Conversation**: Export conversation and bookmarks as JSON

## 📁 Project Structure

```
Translator/
├── backend/
│   ├── translation.py      # Translation and language detection logic
│   ├── speech.py           # Speech-to-Text and Text-to-Speech
│   ├── ocr.py              # OCR image-to-text extraction
│   └── state_manager.py    # Session state and conversation management
├── frontend/
│   └── app.py              # Streamlit UI application
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Installation

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Tesseract OCR** (for OCR functionality):
   - **Windows**: Download from [UB Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr` (Ubuntu/Debian)

3. **OpenAI API Key** (optional but recommended):
   - Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Required for simplifier mode and Whisper STT fallback

### Step 1: Clone or Navigate to Project Directory

```bash
cd e:\Translator
```

### Step 2: Create Virtual Environment (Recommended)

**Quick Setup (Automated):**

**Windows:**
```batch
# Option 1: Using batch script
setup_venv.bat

# Option 2: Using Python script
python setup_venv.py

# Option 3: Manual
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
# Option 1: Using shell script
chmod +x setup_venv.sh
./setup_venv.sh

# Option 2: Using Python script
python3 setup_venv.py

# Option 3: Manual
python3 -m venv venv
source venv/bin/activate
```

**📚 For detailed setup instructions, see [SETUP_VENV.md](SETUP_VENV.md)**

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** Installation may take 5-10 minutes. All packages will be installed in the virtual environment only.

**PyAudio (optional, for microphone input):** PyAudio is not in the main requirements because it often fails on Windows (requires PortAudio C library). The app runs fully without it—only live microphone recording won't work. To enable microphone:
- **Python 3.8–3.13 on Windows:** `pip install -r requirements-voice.txt`
- **Python 3.14 on Windows:** No pre-built wheel yet; use Python 3.12/3.13 if you need microphone

### Step 4: Verify Installation

Verify that packages are installed correctly:
```bash
python verify_venv.py
```

Or manually check:
```bash
pip list
python -c "import streamlit; print('Streamlit OK')"
```

**📚 For quick command reference, see [VENV_COMMANDS.md](VENV_COMMANDS.md)**

### Step 6: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   # Windows
   copy .env.example .env
   
   # macOS/Linux
   cp .env.example .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

3. (Optional) If Tesseract is installed in a custom location on Windows, uncomment and set:
   ```
   TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
   ```

## 🎯 Running the Application

**Important:** Make sure your virtual environment is activated before running!

### Start the Streamlit App

**Option 1: Using run script**
```bash
python run.py
```

**Option 2: Direct Streamlit command**
```bash
streamlit run frontend/app.py
```

**Option 3: Without activating venv (Windows)**
```batch
.\venv\Scripts\python.exe run.py
```

**Option 4: Without activating venv (macOS/Linux)**
```bash
./venv/bin/python run.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

**📚 For more commands, see [VENV_COMMANDS.md](VENV_COMMANDS.md)**

## 📖 Usage Guide

### Basic Translation

1. Select your target language from the sidebar
2. Type your text in the chat input
3. The bot will automatically detect the source language and translate

### Voice Input

1. Select "Voice" input method
2. Upload an audio file (WAV, MP3, OGG, M4A)
3. Click "Process Voice Input"
4. The transcribed text will be automatically translated

### OCR Translation

1. Select "Image" input method
2. Upload an image containing text
3. Click "Extract Text from Image"
4. Choose to Translate, Read Aloud, or Copy the extracted text

### Using Features

- **Auto-English Mode**: Enable in sidebar to automatically translate all input to English
- **Simplifier Mode**: Enable to convert complex text into beginner-friendly language
- **Language Lock**: Lock bot responses to your selected language
- **Accent Selection**: Choose TTS accent (British, American, or Neutral)
- **Bookmarks**: Click ⭐ button on any response to save it
- **Read Aloud**: Click 🔊 button to hear the translation
- **Regenerate**: Click 🔄 to regenerate a response with context

## 🔧 Configuration

### API Keys

- **OpenAI API Key**: Required for simplifier mode and Whisper STT fallback
  - Get from: https://platform.openai.com/api-keys
  - Add to `.env` file as `OPENAI_API_KEY`

### Tesseract OCR

- **Windows**: Install from [UB Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

If installed in a custom location, set `TESSERACT_CMD` in `.env` file.

## 🛠️ Troubleshooting

### Common Issues

1. **"Tesseract OCR not found"**
   - Install Tesseract OCR (see Installation section)
   - Set `TESSERACT_CMD` in `.env` if using custom installation path

2. **"OpenAI API key not configured"**
   - Simplifier mode requires OpenAI API key
   - Add your API key to `.env` file

3. **Speech recognition not working**
   - Ensure microphone permissions are granted
   - For audio file uploads, ensure file format is supported (WAV, MP3, OGG, M4A)

4. **Translation errors**
   - Check internet connection (Google Translate requires internet)
   - Verify language codes are valid
   - Some languages may have limited support

5. **PyAudio / microphone not working (Windows)**
   - PyAudio is optional. Install with `pip install -r requirements-voice.txt` (requires Python 3.8–3.13; no wheel for 3.14 yet)

## 📚 Dependencies

- **streamlit**: Web UI framework
- **googletrans**: Google Translate API wrapper
- **openai**: OpenAI API client (for simplifier and Whisper)
- **speechrecognition**: Speech-to-Text functionality
- **gtts**: Google Text-to-Speech
- **pytesseract**: OCR wrapper for Tesseract
- **Pillow**: Image processing
- **python-dotenv**: Environment variable management
- **pyaudio**: Audio I/O (for microphone input)

## 🔒 Security Notes

- Never commit `.env` file to version control
- Keep your OpenAI API key secure
- The application uses environment variables for secure API key handling
- All API keys are loaded from `.env` file, not hardcoded

## 📝 License

This project is open source and available for educational and personal use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Support

For issues, questions, or suggestions, please open an issue on the project repository.

---

**Built with ❤️ using Python, Streamlit, and AI**
