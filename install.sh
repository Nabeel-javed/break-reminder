#!/bin/bash

# Installation script for 20/20/20 Break Reminder

echo "🔧 Installing 20/20/20 Break Reminder..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Installation complete!"
echo ""
echo "To run the app:"
echo "  1. source venv/bin/activate"
echo "  2. python break_reminder.py"
echo ""
echo "To enable auto-start on login, run:"
echo "  ./setup_autostart.sh"
