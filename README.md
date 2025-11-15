# 👁️ 20/20/20 Break Reminder

A macOS menu bar app that helps you remember the 20/20/20 rule to reduce eye strain from screen time.

## What is the 20/20/20 Rule?

Every **20 minutes** of screen time, take a **20-second** break and look at something **20 feet** (6 meters) away.

This simple practice helps:
- Reduce eye strain and fatigue
- Prevent dry eyes
- Minimize headaches
- Improve focus and productivity

## Features

✅ **Menu Bar Integration** - Sits quietly in your menu bar with easy access to settings
✅ **Smart Notifications** - Starts with a pop-up, escalates to fullscreen if ignored
✅ **Fullscreen Break Timer** - Beautiful 20-second countdown with instructions and tips
✅ **Configurable Settings** - Customize work duration, snooze time, and notification style
✅ **Snooze Function** - Need a few more minutes? Snooze the reminder
✅ **Sound Alerts** - Audio notification when it's break time (can be disabled)
✅ **Idle Detection** - Automatically pauses timer when your Mac is locked or idle
✅ **Auto-start** - Launches automatically when you log in to your Mac

## Installation

### Requirements
- macOS 10.14 or later
- Python 3.8 or later

### Option 1: Standalone App (Recommended - No Terminal Required!)

This creates a proper macOS `.app` that you can install once and forget about.

1. **Clone or download this repository**
   ```bash
   cd ~/Desktop
   git clone <repository-url>
   cd break-reminder
   ```

2. **Run the installation script**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Build the standalone app**
   ```bash
   chmod +x build_app.sh
   ./build_app.sh
   ```

4. **Install to Applications**
   ```bash
   cp -r "dist/Break Reminder.app" /Applications/
   ```

5. **Launch the app**
   - Open from Applications folder or Spotlight (Cmd+Space, type "Break Reminder")
   - You'll see 👁️ in your menu bar
   - The app will ask if you want to enable auto-start - click "Yes, Auto-Start"!
   - That's it! No Terminal needed anymore!

#### Optional: Create a DMG Installer

To create a distributable DMG file:
```bash
chmod +x create_dmg.sh
./create_dmg.sh
```

This creates `BreakReminder-Installer.dmg` that you can share or reinstall later.

### Option 2: Run from Terminal (For Development)

1. **Clone or download this repository**
   ```bash
   cd ~/Downloads
   git clone <repository-url>
   cd break-reminder
   ```

2. **Run the installation script**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Start the app**
   ```bash
   source venv/bin/activate
   python break_reminder.py
   ```

4. **Enable auto-start (Optional)**
   ```bash
   chmod +x setup_autostart.sh
   ./setup_autostart.sh
   ```

## Usage

### First Launch

When you first launch the app, you'll see the 👁️ icon in your menu bar. Click it to access:

- **Time until break** - See how much time remains
- **Pause/Resume Timer** - Temporarily stop the timer
- **Take Break Now** - Manually trigger a break
- **Reset Timer** - Restart the 20-minute countdown
- **Settings** - Customize your preferences
- **About** - Learn more about the app
- **Quit** - Close the application

### Taking a Break

When it's time for a break:

1. **Pop-up notification** appears first (if that's your setting)
2. If ignored for 10 seconds, a **fullscreen overlay** appears
3. The overlay shows:
   - 20-second countdown timer
   - Instructions on what to look at
   - Tips for healthy eye habits
4. Choose **Done** when finished, or **Snooze** for a few more minutes

### Keyboard Shortcuts (During Break)

- `ESC` or `Space` - Complete break and reset timer
- Click **Done** button - Same as ESC
- Click **Snooze** button - Postpone break by configured duration

## Settings

### Work Duration
Choose how long to work before a break reminder:
- 15 minutes
- **20 minutes** (default, recommended)
- 25 minutes
- 30 minutes

### Snooze Duration
Set how long to postpone when you snooze:
- 2 minutes
- **5 minutes** (default)
- 10 minutes
- 15 minutes

### Notification Style
- **Pop-up (escalates to fullscreen)** - Gentle reminder that becomes more insistent (default)
- **Fullscreen Only** - Immediately shows fullscreen break timer

### Sound Alerts
- **Enabled** (default) - Plays a sound when break time arrives
- **Disabled** - Silent notifications only

### Pause When Idle
- **Enabled** (default) - Timer pauses when your Mac is locked or you're away
- **Disabled** - Timer continues running regardless of activity

## Configuration File

Settings are saved in `~/.break_reminder_config.json`

Default configuration:
```json
{
  "work_duration": 1200,        // 20 minutes in seconds
  "break_duration": 20,          // 20 seconds
  "snooze_duration": 300,        // 5 minutes in seconds
  "notification_type": "popup",  // "popup" or "fullscreen"
  "sound_enabled": true,
  "pause_on_idle": true,
  "idle_threshold": 60           // seconds before considered idle
}
```

## Troubleshooting

### App doesn't start
- Make sure you activated the virtual environment: `source venv/bin/activate`
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify Python 3 is installed: `python3 --version`

### No fullscreen overlay
- The app requires Tkinter (usually included with Python)
- Install Tkinter: `brew install python-tk@3.11` (adjust version as needed)

### Auto-start doesn't work
- Check if the LaunchAgent is loaded: `launchctl list | grep breakreminder`
- View logs: `cat ~/Library/Logs/BreakReminder.log`
- Ensure the path in the plist file is correct

### Timer doesn't pause when idle
- This feature uses macOS's IOKit framework
- Make sure "Pause When Idle" is enabled in Settings
- Idle threshold is 60 seconds by default

## Uninstallation

### Remove auto-start
```bash
launchctl unload ~/Library/LaunchAgents/com.breakreminder.app.plist
rm ~/Library/LaunchAgents/com.breakreminder.app.plist
```

### Remove the app
```bash
rm -rf ~/path/to/break-reminder
rm ~/.break_reminder_config.json
```

## Why This Matters

**Digital eye strain** affects 50-90% of people who work at computers. Symptoms include:
- Dry, irritated eyes
- Blurred vision
- Eye fatigue
- Headaches
- Neck and shoulder pain

The 20/20/20 rule is recommended by optometrists and eye health professionals as a simple, effective way to reduce these symptoms.

## Tips for Best Results

1. **Position matters** - Look out a window or across a large room
2. **Actually look away** - Don't just unfocus your eyes, look at distant objects
3. **Blink frequently** - Helps keep eyes moist
4. **Adjust screen brightness** - Match your environment
5. **Consider blue light** - Use Night Shift or f.lux in evenings
6. **Regular eye exams** - See an optometrist annually

## License

MIT License - Feel free to use, modify, and distribute

## Contributing

Contributions welcome! Feel free to submit issues and pull requests.

## Support

If you encounter any issues or have suggestions, please open an issue on the repository.

---

**Remember:** This app is a helpful reminder tool, but listen to your body. If your eyes feel strained, take a break even if the timer hasn't gone off yet! 👁️✨
