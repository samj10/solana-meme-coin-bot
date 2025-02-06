#!/bin/bash
set -e  # Exit on error

# Check for virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate and install requirements
echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

# Set paper trading mode
export PAPER_TRADING="true"
export SAFETY_MAX_SOL="0.0"

# Run the bot
echo "Starting in PAPER TRADING mode..."
python src/bot.py