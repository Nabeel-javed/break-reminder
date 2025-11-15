#!/bin/bash

# Test the built app and show detailed error messages

echo "🔍 Testing Break Reminder.app..."
echo ""

if [ ! -d "dist/Break Reminder.app" ]; then
    echo "❌ App not found at dist/Break Reminder.app"
    echo "Please run ./build_app.sh first"
    exit 1
fi

echo "Running app with verbose output..."
echo "Press Ctrl+C to stop"
echo ""
echo "==== App Output ===="

# Run the app directly from its executable to see error messages
"dist/Break Reminder.app/Contents/MacOS/BreakReminder"
