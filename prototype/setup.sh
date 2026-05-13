#!/bin/bash

echo "=========================================="
echo "AI Creator Studio Prototype Setup (Linux/Mac)"
echo "=========================================="

# 1. Create Virtual Environment
echo "[1/4] Creating Virtual Environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Install Dependencies
echo "[2/4] Installing Dependencies..."
pip install -r requirements.txt

# 3. Initialize .env (if not exists)
echo "[3/4] Checking .env file..."
if [ ! -f .env ]; then
    echo "[WARN] .env file not found. Creating a template."
    echo "GEMINI_API_KEY=YOUR_KEY_HERE" > .env
    echo "[IMPORTANT] Please update .env with your GEMINI_API_KEY!"
fi

echo "=========================================="
echo "Setup Complete! Starting Terminal App..."
echo "=========================================="
python3 main.py
