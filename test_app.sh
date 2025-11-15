#!/bin/bash

# Test the built app and show detailed error messages

echo "🔍 Testing Break Reminder.app..."
echo ""

if [ ! -d "dist/Break Reminder.app" ]; then
    echo "❌ App not found at dist/Break Reminder.app"
    echo "Please run ./build_app.sh first"
    exit 1
fi

echo "📂 Checking app structure..."
echo ""

# Show what's in the MacOS directory
if [ -d "dist/Break Reminder.app/Contents/MacOS" ]; then
    echo "Contents of MacOS directory:"
    ls -la "dist/Break Reminder.app/Contents/MacOS/"
    echo ""

    # Find the executable (usually the first file)
    EXECUTABLE=$(find "dist/Break Reminder.app/Contents/MacOS/" -type f -perm +111 | head -n 1)

    if [ -n "$EXECUTABLE" ]; then
        echo "Found executable: $EXECUTABLE"
        echo ""
        echo "Running app with verbose output..."
        echo "Press Ctrl+C to stop"
        echo ""
        echo "==== App Output ===="
        "$EXECUTABLE"
    else
        echo "❌ No executable found in MacOS directory"
        echo ""
        echo "Try rebuilding with: ./build_app.sh"
    fi
else
    echo "❌ MacOS directory not found"
    echo ""
    echo "App structure:"
    ls -lR "dist/Break Reminder.app/" | head -30
fi
