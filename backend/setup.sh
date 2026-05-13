#!/bin/bash

echo "=================================================="
echo "AI Creator Studio - Setup Script (Linux/macOS)"
echo "=================================================="

# Validate Python installation
if ! command -v python3 &> /dev/null
then
    echo "[ERROR] Python3 is not installed or not in PATH."
    exit 1
fi

# Validate Pip installation
if ! command -v pip3 &> /dev/null
then
    echo "[ERROR] Pip3 is not installed or not in PATH."
    exit 1
fi

# Create Virtual Environment
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv venv
else
    echo "[INFO] Virtual environment already exists."
fi

# Activate Virtual Environment
source venv/bin/activate

# Install Dependencies
echo "[INFO] Installing dependencies..."
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# Create necessary folders
echo "[INFO] Ensuring folder structure exists..."
mkdir -p uploads generated logs

# Initialize .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "[INFO] Initializing .env from .env.example..."
    cp .env.example .env
fi

echo "=================================================="
echo "Setup Complete!"
echo "Starting AI Creator Studio..."
echo "=================================================="

streamlit run app.py
