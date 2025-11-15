#!/bin/bash

# Create a DMG installer for Break Reminder

echo "📦 Creating DMG installer..."
echo ""

# Make sure the app exists
if [ ! -d "dist/Break Reminder.app" ]; then
    echo "❌ App not found. Please run ./build_app.sh first"
    exit 1
fi

# Create a temporary directory for DMG contents
DMG_DIR="dmg_temp"
rm -rf "$DMG_DIR"
mkdir -p "$DMG_DIR"

# Copy the app to temp directory
echo "📋 Copying app..."
cp -r "dist/Break Reminder.app" "$DMG_DIR/"

# Create a symbolic link to Applications folder
echo "🔗 Creating Applications link..."
ln -s /Applications "$DMG_DIR/Applications"

# Create the DMG
DMG_NAME="BreakReminder-Installer.dmg"
echo "🗜️  Creating DMG..."

# Remove old DMG if it exists
rm -f "$DMG_NAME"

# Create DMG using hdiutil (built into macOS)
hdiutil create -volname "Break Reminder" \
    -srcfolder "$DMG_DIR" \
    -ov -format UDZO \
    "$DMG_NAME"

# Clean up temp directory
rm -rf "$DMG_DIR"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ DMG created successfully!"
    echo ""
    echo "📦 Installer: $DMG_NAME"
    echo ""
    echo "To install:"
    echo "  1. Double-click $DMG_NAME"
    echo "  2. Drag 'Break Reminder' to the Applications folder"
    echo "  3. Eject the disk image"
    echo "  4. Open Break Reminder from Applications"
    echo "  5. Add to Login Items in System Settings/Preferences"
else
    echo ""
    echo "❌ DMG creation failed"
    exit 1
fi
