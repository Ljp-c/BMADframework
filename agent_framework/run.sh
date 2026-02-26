#!/bin/bash
# ================================================
# AutoGen Framework - Interactive Mode Launcher
# ================================================

echo ""
echo "====================================="
echo "  AutoGen Framework Launcher"
echo "====================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

# Change to script directory
cd "$(dirname "$0")"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found!"
    if [ -f ".env.example" ]; then
        echo "Creating .env from .env.example..."
        cp ".env.example" ".env"
        echo "Created .env file. Please edit it with your API credentials."
    else
        echo "Error: .env.example not found!"
        exit 1
    fi
fi

# Check if required dependencies are installed
echo "Checking dependencies..."
if ! pip3 list | grep -q "pyautogen"; then
    echo ""
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

# Run the framework
echo ""
echo "Starting AutoGen Framework..."
echo ""
python3 main.py

exit_code=$?
if [ $exit_code -ne 0 ]; then
    echo ""
    echo "Error occurred during execution (exit code: $exit_code)"
    exit 1
fi
