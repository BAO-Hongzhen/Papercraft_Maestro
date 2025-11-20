#!/bin/bash
################################################################################
# Syntax Roulette - macOS Run Script
# Starts the application in the virtual environment
################################################################################

echo ""
echo "========================================================================"
echo "  Syntax Roulette - Starting Application"
echo "========================================================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo ""
    echo "Please run './setup_macos.sh' first to set up the environment."
    echo ""
    exit 1
fi

# Activate virtual environment
echo "[1/2] Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment!"
    echo "Please run './setup_macos.sh' again."
    echo ""
    exit 1
fi
echo ""

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "[ERROR] main.py not found!"
    echo "Make sure you're in the correct directory."
    echo ""
    exit 1
fi

echo "[2/2] Launching Syntax Roulette..."
echo ""
echo "========================================================================"
echo "  Application is starting..."
echo "  Please wait, this may take a moment..."
echo ""
echo "  The web interface will open automatically in your browser."
echo "  If it doesn't, open: http://localhost:7860"
echo ""
echo "  To stop the application, press Ctrl+C"
echo "========================================================================"
echo ""

# Run the application
python main.py

# If we get here, the application has stopped
echo ""
echo "========================================================================"
echo "  Application stopped."
echo "========================================================================"

