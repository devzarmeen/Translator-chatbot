# 🐍 Virtual Environment Setup Guide

This guide provides step-by-step instructions for creating and configuring a Python virtual environment for the AI Translator Chatbot project.

## 📋 Prerequisites

- **Python 3.8 or higher** installed on your system
- Internet connection for downloading packages
- Terminal/Command Prompt access

## 🚀 Quick Setup (Automated)

### Windows

**Option 1: Using Batch Script**
```batch
setup_venv.bat
```

**Option 2: Using Python Script**
```batch
python setup_venv.py
```

### macOS/Linux

**Option 1: Using Shell Script**
```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

**Option 2: Using Python Script**
```bash
python3 setup_venv.py
```

## 📝 Manual Setup (Step-by-Step)

### Step 1: Navigate to Project Directory

**Windows:**
```batch
cd e:\Translator
```

**macOS/Linux:**
```bash
cd /path/to/Translator
```

### Step 2: Create Virtual Environment

**Windows:**
```batch
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

This creates a new directory called `venv` containing:
- Python interpreter
- pip package manager
- Isolated package installation space

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```batch
.\venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Verification:** After activation, your prompt should show `(venv)` at the beginning.

### Step 4: Upgrade pip

```batch
python -m pip install --upgrade pip
```

**macOS/Linux:**
```bash
python3 -m pip install --upgrade pip
```

### Step 5: Install Required Packages

```batch
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

This will install all dependencies listed in `requirements.txt`:
- streamlit (Web UI framework)
- googletrans (Translation API)
- openai (AI features)
- speechrecognition (Speech-to-Text)
- gtts (Text-to-Speech)
- pytesseract (OCR)
- Pillow (Image processing)
- python-dotenv (Environment variables)
- pyaudio (Audio I/O)

**Note:** Installation may take 5-10 minutes depending on your internet connection.

### Step 6: Verify Installation

Check installed packages:
```batch
pip list
```

Verify key packages:
```batch
pip show streamlit googletrans openai
```

## 🔧 Troubleshooting

### Issue: "python: command not found"

**Solution:**
- Windows: Use `py` instead of `python`
- macOS/Linux: Use `python3` instead of `python`
- Ensure Python is installed and in PATH

### Issue: "pip: command not found"

**Solution:**
```batch
python -m pip install --upgrade pip
```

### Issue: PyAudio Installation Fails (Windows)

**Solution 1: Use pipwin**
```batch
pip install pipwin
pipwin install pyaudio
```

**Solution 2: Download Pre-built Wheel**
1. Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Download appropriate wheel file for your Python version
3. Install: `pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl`

**Solution 3: Skip PyAudio (Optional)**
PyAudio is only needed for microphone input. The app works without it for file-based audio.

### Issue: Virtual Environment Not Activating

**Windows PowerShell:**
If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

### Issue: "Permission denied" (macOS/Linux)

**Solution:**
```bash
chmod +x setup_venv.sh
sudo chmod -R 755 venv
```

### Issue: Packages Install Slowly

**Solution:** Use a faster mirror (China):
```batch
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## ✅ Verification Checklist

After setup, verify:

- [ ] Virtual environment created (`venv` folder exists)
- [ ] Virtual environment activated (prompt shows `(venv)`)
- [ ] Python version is 3.8+ (`python --version`)
- [ ] pip is upgraded (`pip --version`)
- [ ] All packages installed (`pip list` shows required packages)
- [ ] Can import packages (`python -c "import streamlit; print('OK')"`)

## 🎯 Using the Virtual Environment

### Activate (Every Time You Work on Project)

**Windows:**
```batch
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Deactivate (When Done)

```batch
deactivate
```

### Run Application

```batch
python run.py
```

Or:
```batch
streamlit run frontend/app.py
```

## 📦 Requirements.txt Contents

```
streamlit>=1.28.0          # Web UI framework
googletrans==4.0.0rc1      # Google Translate API wrapper
openai>=1.0.0              # OpenAI API client
speechrecognition>=3.10.0   # Speech-to-Text library
gtts>=2.4.0                # Google Text-to-Speech
pytesseract>=0.3.10        # OCR wrapper for Tesseract
Pillow>=10.0.0             # Image processing
python-dotenv>=1.0.0       # Environment variable management
pyaudio>=0.2.11            # Audio I/O (optional, may need special install)
```

## 🔒 Best Practices

1. **Always activate virtual environment** before working on the project
2. **Never commit `venv/` folder** to version control (already in `.gitignore`)
3. **Use `requirements.txt`** to track all dependencies
4. **Keep virtual environment isolated** - don't install packages globally
5. **Update requirements.txt** when adding new packages:
   ```batch
   pip freeze > requirements.txt
   ```

## 📚 Additional Resources

- [Python venv Documentation](https://docs.python.org/3/library/venv.html)
- [pip User Guide](https://pip.pypa.io/en/stable/user_guide/)
- [Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)

---

**Need Help?** Check the main [README.md](README.md) for more information.
