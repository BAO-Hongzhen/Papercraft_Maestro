#!/bin/bash
################################################################################
# Syntax Roulette - macOS Setup Script
# This script sets up the virtual environment and installs dependencies
################################################################################

echo ""
echo "========================================================================"
echo "  Syntax Roulette - Setup for macOS"
echo "========================================================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  Option 1 (Recommended): brew install python@3.10"
    echo "  Option 2: Download from https://www.python.org/downloads/"
    echo ""
    exit 1
fi

echo "[1/6] Checking Python installation..."
python3 --version
echo ""

# Check Python version (at least 3.8)
python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"
if [ $? -ne 0 ]; then
    echo "[ERROR] Python 3.8 or higher is required!"
    echo "Please upgrade your Python installation."
    echo ""
    exit 1
fi

echo "[2/6] Checking system information..."
echo "Platform: $(uname -m)"
if [[ $(uname -m) == 'arm64' ]]; then
    echo "✅ Apple Silicon detected - MPS acceleration will be available"
else
    echo "⚠️  Intel Mac detected - will use CPU mode (slower)"
fi
echo ""

echo "[3/6] Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "Virtual environment already exists. Removing old one..."
    rm -rf .venv
fi

python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create virtual environment!"
    echo ""
    exit 1
fi
echo "Virtual environment created successfully!"
echo ""

echo "[4/6] Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment!"
    echo ""
    exit 1
fi
echo ""

echo "[5/6] Upgrading pip..."
python -m pip install --upgrade pip
echo ""

echo "[6/6] Installing dependencies..."
echo "This may take several minutes on first run..."
echo ""

pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies!"
    echo ""
    echo "Troubleshooting tips:"
    echo "- Check your internet connection"
    echo "- Make sure you have Xcode Command Line Tools: xcode-select --install"
    echo "- Try: pip install --upgrade pip setuptools wheel"
    echo ""
    exit 1
fi

echo ""
echo "========================================================================"
echo "  Setup completed successfully!"
echo "========================================================================"
echo ""
echo "Next steps:"
echo "  1. Run './run_macos.sh' to start the application"
echo "  2. Wait for the browser to open automatically"
echo "  3. Start creating amazing images!"
echo ""
echo "Note: First run will download AI models (~4GB, one-time only)"
echo "This may take 5-15 minutes depending on your internet connection."
echo ""
if [[ $(uname -m) == 'arm64' ]]; then
    echo "🚀 Your Apple Silicon Mac will use GPU acceleration (MPS) for fast generation!"
else
    echo "⚠️  CPU mode will be used (slower). Consider using an Apple Silicon Mac for better performance."
fi
echo ""
echo "========================================================================"

