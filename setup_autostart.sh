#!/bin/bash

# Setup auto-start for 20/20/20 Break Reminder on macOS

APP_NAME="BreakReminder"
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/break_reminder.py"
VENV_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/venv"
PLIST_PATH="$HOME/Library/LaunchAgents/com.breakreminder.app.plist"

echo "🔧 Setting up auto-start for Break Reminder..."

# Create LaunchAgent plist
cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.breakreminder.app</string>
    <key>ProgramArguments</key>
    <array>
        <string>$VENV_PATH/bin/python</string>
        <string>$SCRIPT_PATH</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$HOME/Library/Logs/BreakReminder.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/Library/Logs/BreakReminder.error.log</string>
</dict>
</plist>
EOF

# Make script executable
chmod +x "$SCRIPT_PATH"

# Load the launch agent
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"

echo "✅ Auto-start enabled!"
echo "The app will now start automatically when you log in."
echo ""
echo "To disable auto-start:"
echo "  launchctl unload $PLIST_PATH"
echo "  rm $PLIST_PATH"
