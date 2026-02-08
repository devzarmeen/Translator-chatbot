# 🐍 Virtual Environment Quick Reference

Quick command reference for managing the virtual environment.

## 📋 Setup Commands

### Create Virtual Environment

**Windows:**
```batch
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

### Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```batch
.\venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Verification:** Prompt should show `(venv)` prefix.

### Deactivate Virtual Environment

```batch
deactivate
```

Works on all platforms.

## 📦 Package Management

### Install All Requirements

```batch
pip install -r requirements.txt
```

### Upgrade pip

```batch
python -m pip install --upgrade pip
```

### List Installed Packages

```batch
pip list
```

### Check Specific Package

```batch
pip show streamlit
```

### Install Single Package

```batch
pip install package_name
```

### Uninstall Package

```batch
pip uninstall package_name
```

### Update Requirements File

```batch
pip freeze > requirements.txt
```

## ✅ Verification

### Check Python Version

```batch
python --version
```

Should show Python 3.8 or higher.

### Check if in Virtual Environment

**Windows:**
```batch
where python
```

Should show path to `venv\Scripts\python.exe`

**macOS/Linux:**
```bash
which python
```

Should show path to `venv/bin/python`

### Run Verification Script

```batch
python verify_venv.py
```

## 🚀 Running Application

### With Virtual Environment Active

```batch
python run.py
```

Or:

```batch
streamlit run frontend/app.py
```

### Without Activating (Windows)

```batch
.\venv\Scripts\python.exe run.py
```

### Without Activating (macOS/Linux)

```bash
./venv/bin/python run.py
```

## 🔧 Troubleshooting Commands

### Recreate Virtual Environment

**Windows:**
```batch
rmdir /s /q venv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Fix Permission Issues (macOS/Linux)

```bash
chmod -R 755 venv
```

### Clear pip Cache

```batch
pip cache purge
```

## 📝 Common Workflow

1. **Activate virtual environment**
   ```batch
   .\venv\Scripts\activate
   ```

2. **Work on project**
   - Edit code
   - Run application
   - Test features

3. **Install new package** (if needed)
   ```batch
   pip install new_package
   pip freeze > requirements.txt
   ```

4. **Deactivate when done**
   ```batch
   deactivate
   ```

---

**Remember:** Always activate the virtual environment before working on the project!
