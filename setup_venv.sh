#!/bin/bash
# Virtual Environment Setup Script for AI Translator Chatbot (macOS/Linux)
# This script creates and configures a Python virtual environment for the project.

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_NAME="venv"
VENV_PATH="${PROJECT_ROOT}/${VENV_NAME}"
REQUIREMENTS_FILE="${PROJECT_ROOT}/requirements.txt"

echo "============================================================"
echo "AI TRANSLATOR CHATBOT - Virtual Environment Setup"
echo "============================================================"
echo "Project root: ${PROJECT_ROOT}"
echo ""

# Step 1: Check Python version
echo "============================================================"
echo "STEP 1: Checking Python Version"
echo "============================================================"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ ERROR: Python 3 is not installed!${NC}"
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Python version: ${PYTHON_VERSION}"
echo -e "${GREEN}✅ Python version check passed${NC}"
echo ""

# Step 2: Create virtual environment
echo "============================================================"
echo "STEP 2: Creating Virtual Environment"
echo "============================================================"
if [ -d "${VENV_PATH}" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists at: ${VENV_PATH}${NC}"
    read -p "Do you want to recreate it? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing virtual environment..."
        rm -rf "${VENV_PATH}"
    else
        echo "Using existing virtual environment."
    fi
fi

if [ ! -d "${VENV_PATH}" ]; then
    echo "Creating virtual environment at: ${VENV_PATH}"
    python3 -m venv "${VENV_PATH}"
    echo -e "${GREEN}✅ Virtual environment created successfully!${NC}"
else
    echo -e "${GREEN}✅ Using existing virtual environment${NC}"
fi
echo ""

# Step 3: Verify virtual environment
echo "============================================================"
echo "STEP 3: Verifying Virtual Environment"
echo "============================================================"
if [ ! -f "${VENV_PATH}/bin/python" ]; then
    echo -e "${RED}❌ ERROR: Python executable not found in virtual environment!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Virtual environment verified successfully!${NC}"
echo "   Python: ${VENV_PATH}/bin/python"
echo ""

# Step 4: Upgrade pip
echo "============================================================"
echo "STEP 4: Upgrading pip"
echo "============================================================"
"${VENV_PATH}/bin/python" -m pip install --upgrade pip --quiet
echo -e "${GREEN}✅ pip upgraded successfully!${NC}"
echo ""

# Step 5: Install requirements
echo "============================================================"
echo "STEP 5: Installing Required Packages"
echo "============================================================"
if [ ! -f "${REQUIREMENTS_FILE}" ]; then
    echo -e "${RED}❌ ERROR: requirements.txt not found at: ${REQUIREMENTS_FILE}${NC}"
    exit 1
fi

echo "Installing packages from: ${REQUIREMENTS_FILE}"
echo "This may take a few minutes..."
"${VENV_PATH}/bin/pip" install -r "${REQUIREMENTS_FILE}"
echo -e "${GREEN}✅ All packages installed successfully!${NC}"
echo ""

# Step 6: Verify installations
echo "============================================================"
echo "STEP 6: Verifying Package Installations"
echo "============================================================"
"${VENV_PATH}/bin/pip" list | grep -E "(streamlit|googletrans|openai|speechrecognition|gtts|pytesseract|Pillow|python-dotenv)" || true
echo -e "${GREEN}✅ Key packages verified!${NC}"
echo ""

# Step 7: Print instructions
echo "============================================================"
echo "SETUP COMPLETE!"
echo "============================================================"
echo ""
echo "📋 To activate the virtual environment:"
echo "   source ${VENV_PATH}/bin/activate"
echo "   OR"
echo "   source venv/bin/activate"
echo ""
echo "📋 To deactivate the virtual environment:"
echo "   deactivate"
echo ""
echo "📋 To run the application:"
echo "   python run.py"
echo "   OR"
echo "   streamlit run frontend/app.py"
echo ""
echo "📋 To verify virtual environment is active:"
echo "   which python  # Should show venv path"
echo "   pip list      # Should show installed packages"
echo ""
echo "============================================================"
