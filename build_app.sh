#!/bin/bash

# Build script for creating the Break Reminder.app bundle

echo "🔨 Building Break Reminder.app..."
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./install.sh first"
    exit 1
fi

source venv/bin/activate

# Install py2app if not already installed
echo "📦 Installing build dependencies..."
pip install py2app

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist

# Build the app
echo "🏗️  Building application bundle..."
python setup.py py2app

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📱 Your app is ready at: dist/Break Reminder.app"
    echo ""
    echo "Next steps:"
    echo "  1. Test the app: open 'dist/Break Reminder.app'"
    echo "  2. Move to Applications: cp -r 'dist/Break Reminder.app' /Applications/"
    echo "  3. Add to Login Items:"
    echo "     - Open System Settings/Preferences"
    echo "     - Go to Users & Groups > Login Items"
    echo "     - Click '+' and add 'Break Reminder' from Applications"
    echo ""
    echo "Or run: ./create_dmg.sh to create an installer DMG"
else
    echo ""
    echo "❌ Build failed. Check the error messages above."
    exit 1
fi
