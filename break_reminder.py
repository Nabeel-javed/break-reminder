#!/usr/bin/env python3
"""
20/20/20 Break Reminder - Menu Bar App for macOS
Reminds you to take eye breaks every 20 minutes by looking at something 20 feet away for 20 seconds
"""

import rumps
import time
import threading
import subprocess
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Try to import Tkinter for fullscreen overlay
try:
    import tkinter as tk
    from tkinter import ttk
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False


class BreakReminderApp(rumps.App):
    """Main application class for the 20/20/20 Break Reminder"""

    def __init__(self):
        super(BreakReminderApp, self).__init__(
            name="BreakReminder",
            title="👁️",
            quit_button=None
        )

        # Load configuration
        self.config_file = Path.home() / '.break_reminder_config.json'
        self.load_config()

        # Timer state
        self.work_duration = self.config.get('work_duration', 20 * 60)  # 20 minutes in seconds
        self.break_duration = self.config.get('break_duration', 20)  # 20 seconds
        self.snooze_duration = self.config.get('snooze_duration', 5 * 60)  # 5 minutes default
        self.notification_type = self.config.get('notification_type', 'popup')  # 'popup' or 'fullscreen'
        self.sound_enabled = self.config.get('sound_enabled', True)
        self.pause_on_idle = self.config.get('pause_on_idle', True)
        self.idle_threshold = self.config.get('idle_threshold', 60)  # seconds

        # Runtime state
        self.timer_running = True
        self.time_remaining = self.work_duration
        self.last_update = time.time()
        self.notification_shown = False
        self.notification_escalated = False
        self.fullscreen_window = None

        # Build menu
        self.build_menu()

        # Start timer using rumps.Timer (runs on main thread)
        self.update_timer = rumps.Timer(self.run_timer, 1)
        self.update_timer.start()

        # Check if first launch and prompt for auto-start
        if self.config.get('first_launch', True):
            self.prompt_auto_start()

    def load_config(self):
        """Load configuration from file"""
        default_config = {
            'work_duration': 20 * 60,
            'break_duration': 20,
            'snooze_duration': 5 * 60,
            'notification_type': 'popup',
            'sound_enabled': True,
            'pause_on_idle': True,
            'idle_threshold': 60,
            'first_launch': True
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = {**default_config, **json.load(f)}
            except Exception as e:
                print(f"Error loading config: {e}")
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def build_menu(self):
        """Build the menu bar menu"""
        self.menu = [
            rumps.MenuItem('Time until break: --:--', callback=None),
            rumps.separator,
            rumps.MenuItem('Pause Timer', callback=self.toggle_timer),
            rumps.MenuItem('Take Break Now', callback=self.take_break_now),
            rumps.MenuItem('Reset Timer', callback=self.reset_timer),
            rumps.separator,
            self.build_settings_menu(),
            rumps.separator,
            rumps.MenuItem('About', callback=self.show_about),
            rumps.MenuItem('Quit', callback=self.quit_app)
        ]

    def build_settings_menu(self):
        """Build settings submenu"""
        settings_menu = rumps.MenuItem('Settings')

        # Work duration options
        work_duration_menu = rumps.MenuItem('Work Duration')
        for minutes in [15, 20, 25, 30]:
            item = rumps.MenuItem(
                f'{minutes} minutes',
                callback=lambda sender, m=minutes: self.set_work_duration(m)
            )
            if minutes * 60 == self.work_duration:
                item.state = True
            work_duration_menu.add(item)

        # Snooze duration options
        snooze_menu = rumps.MenuItem('Snooze Duration')
        for minutes in [2, 5, 10, 15]:
            item = rumps.MenuItem(
                f'{minutes} minutes',
                callback=lambda sender, m=minutes: self.set_snooze_duration(m)
            )
            if minutes * 60 == self.snooze_duration:
                item.state = True
            snooze_menu.add(item)

        # Notification type
        notification_menu = rumps.MenuItem('Notification Style')
        popup_item = rumps.MenuItem(
            'Pop-up (escalates to fullscreen)',
            callback=lambda _: self.set_notification_type('popup')
        )
        fullscreen_item = rumps.MenuItem(
            'Fullscreen Only',
            callback=lambda _: self.set_notification_type('fullscreen')
        )
        if self.notification_type == 'popup':
            popup_item.state = True
        else:
            fullscreen_item.state = True
        notification_menu.add(popup_item)
        notification_menu.add(fullscreen_item)

        # Sound toggle
        sound_item = rumps.MenuItem(
            'Sound Alerts',
            callback=self.toggle_sound
        )
        sound_item.state = self.sound_enabled

        # Pause on idle toggle
        idle_item = rumps.MenuItem(
            'Pause When Idle',
            callback=self.toggle_pause_on_idle
        )
        idle_item.state = self.pause_on_idle

        settings_menu.add(work_duration_menu)
        settings_menu.add(snooze_menu)
        settings_menu.add(notification_menu)
        settings_menu.add(sound_item)
        settings_menu.add(idle_item)

        return settings_menu

    def set_work_duration(self, minutes):
        """Set work duration in minutes"""
        self.work_duration = minutes * 60
        self.config['work_duration'] = self.work_duration
        self.save_config()
        self.reset_timer(None)
        self.build_menu()
        rumps.notification(
            title='Settings Updated',
            subtitle='',
            message=f'Work duration set to {minutes} minutes'
        )

    def set_snooze_duration(self, minutes):
        """Set snooze duration in minutes"""
        self.snooze_duration = minutes * 60
        self.config['snooze_duration'] = self.snooze_duration
        self.save_config()
        self.build_menu()
        rumps.notification(
            title='Settings Updated',
            subtitle='',
            message=f'Snooze duration set to {minutes} minutes'
        )

    def set_notification_type(self, notif_type):
        """Set notification type"""
        self.notification_type = notif_type
        self.config['notification_type'] = notif_type
        self.save_config()
        self.build_menu()

    def toggle_sound(self, sender):
        """Toggle sound alerts"""
        self.sound_enabled = not self.sound_enabled
        sender.state = self.sound_enabled
        self.config['sound_enabled'] = self.sound_enabled
        self.save_config()

    def toggle_pause_on_idle(self, sender):
        """Toggle pause on idle"""
        self.pause_on_idle = not self.pause_on_idle
        sender.state = self.pause_on_idle
        self.config['pause_on_idle'] = self.pause_on_idle
        self.save_config()

    def toggle_timer(self, sender):
        """Pause/Resume the timer"""
        self.timer_running = not self.timer_running
        if self.timer_running:
            sender.title = 'Pause Timer'
            self.last_update = time.time()
        else:
            sender.title = 'Resume Timer'

    def take_break_now(self, _):
        """Manually trigger a break"""
        self.show_break_notification()

    def reset_timer(self, _):
        """Reset the timer to full duration"""
        self.time_remaining = self.work_duration
        self.last_update = time.time()
        self.notification_shown = False
        self.notification_escalated = False

    def snooze_break(self):
        """Snooze the break reminder"""
        self.time_remaining = self.snooze_duration
        self.last_update = time.time()
        self.notification_shown = False
        self.notification_escalated = False
        if self.fullscreen_window:
            self.fullscreen_window.destroy()
            self.fullscreen_window = None

    def get_idle_time(self):
        """Get system idle time in seconds (macOS)"""
        try:
            result = subprocess.run(
                ['ioreg', '-c', 'IOHIDSystem'],
                capture_output=True,
                text=True,
                timeout=1
            )
            for line in result.stdout.split('\n'):
                if 'HIDIdleTime' in line:
                    # Extract the idle time in nanoseconds and convert to seconds
                    idle_ns = int(line.split('=')[1].strip())
                    return idle_ns / 1_000_000_000
        except Exception as e:
            print(f"Error getting idle time: {e}")
        return 0

    def run_timer(self, _):
        """Main timer callback - called every second by rumps.Timer"""
        try:
            if self.timer_running:
                # Check if system is idle
                if self.pause_on_idle:
                    idle_time = self.get_idle_time()
                    if idle_time > self.idle_threshold:
                        # System is idle, don't decrement timer
                        self.last_update = time.time()
                        return

                # Update timer
                current_time = time.time()
                elapsed = current_time - self.last_update
                self.last_update = current_time

                self.time_remaining -= elapsed

                # Update menu title and menu bar display
                if self.time_remaining <= 0:
                    # Break time - show message instead of negative numbers
                    self.menu['Time until break: --:--'].title = 'Break Time! 👁️'
                    self.title = '👁️ Break Time!'
                else:
                    # Normal countdown
                    minutes = int(self.time_remaining // 60)
                    seconds = int(self.time_remaining % 60)
                    self.menu['Time until break: --:--'].title = f'Time until break: {minutes:02d}:{seconds:02d}'
                    self.title = f'👁️ {minutes:02d}:{seconds:02d}'

                # Check if it's time for a break
                if self.time_remaining <= 0 and not self.notification_shown:
                    self.show_break_notification()
                    self.notification_shown = True

                # Escalate to fullscreen if popup ignored for 10 seconds
                elif self.time_remaining <= -10 and self.notification_shown and not self.notification_escalated:
                    if self.notification_type == 'popup':
                        self.show_fullscreen_break()
                        self.notification_escalated = True

        except Exception as e:
            print(f"Timer error: {e}")

    def play_sound(self):
        """Play notification sound"""
        if self.sound_enabled:
            try:
                # Use macOS system sound
                subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'], check=False)
            except Exception as e:
                print(f"Error playing sound: {e}")

    def show_break_notification(self):
        """Show initial break notification"""
        self.play_sound()

        if self.notification_type == 'fullscreen':
            self.show_fullscreen_break()
        else:
            # Show macOS notification
            response = rumps.notification(
                title='Time for a break! 👁️',
                subtitle='20/20/20 Rule',
                message='Look at something 20 feet away for 20 seconds to rest your eyes.',
                sound=False  # We already played our custom sound
            )

            # Schedule fullscreen escalation check
            threading.Timer(10, self.check_escalation).start()

    def check_escalation(self):
        """Check if we need to escalate to fullscreen"""
        if self.notification_shown and not self.notification_escalated and self.time_remaining < -5:
            self.show_fullscreen_break()
            self.notification_escalated = True

    def show_fullscreen_break(self):
        """Show fullscreen break window"""
        if not HAS_TKINTER:
            print("Tkinter not available, cannot show fullscreen window")
            return

        if self.fullscreen_window:
            return  # Already showing

        self.play_sound()

        # Create fullscreen window
        self.fullscreen_window = tk.Tk()
        self.fullscreen_window.title("Break Time")
        self.fullscreen_window.attributes('-fullscreen', True)
        self.fullscreen_window.attributes('-topmost', True)
        self.fullscreen_window.configure(bg='#2C3E50')

        # Main container
        container = tk.Frame(self.fullscreen_window, bg='#2C3E50')
        container.place(relx=0.5, rely=0.5, anchor='center')

        # Title
        title = tk.Label(
            container,
            text="👁️ Time for a Break! 👁️",
            font=('Helvetica', 48, 'bold'),
            fg='#ECF0F1',
            bg='#2C3E50'
        )
        title.pack(pady=20)

        # Countdown
        self.countdown_label = tk.Label(
            container,
            text="20",
            font=('Helvetica', 120, 'bold'),
            fg='#3498DB',
            bg='#2C3E50'
        )
        self.countdown_label.pack(pady=30)

        # Instructions
        instructions_frame = tk.Frame(container, bg='#2C3E50')
        instructions_frame.pack(pady=20)

        instruction_text = "Look at something 20 feet (6 meters) away"
        instruction = tk.Label(
            instructions_frame,
            text=instruction_text,
            font=('Helvetica', 24),
            fg='#ECF0F1',
            bg='#2C3E50'
        )
        instruction.pack()

        # Tips
        tips = [
            "💡 Focus on a distant object like a tree or building",
            "💡 Let your eyes relax and blink naturally",
            "💡 This helps prevent eye strain and fatigue",
            "💡 Regular breaks improve focus and productivity"
        ]

        tips_frame = tk.Frame(container, bg='#34495E', padx=30, pady=20)
        tips_frame.pack(pady=30)

        for tip in tips:
            tip_label = tk.Label(
                tips_frame,
                text=tip,
                font=('Helvetica', 16),
                fg='#ECF0F1',
                bg='#34495E',
                anchor='w'
            )
            tip_label.pack(anchor='w', pady=5)

        # Buttons
        button_frame = tk.Frame(container, bg='#2C3E50')
        button_frame.pack(pady=30)

        done_button = tk.Button(
            button_frame,
            text="Done (ESC)",
            command=lambda: self.finish_break(True),
            font=('Helvetica', 18, 'bold'),
            bg='#27AE60',
            fg='white',
            padx=30,
            pady=15,
            relief='flat',
            cursor='hand2'
        )
        done_button.pack(side='left', padx=10)

        snooze_button = tk.Button(
            button_frame,
            text=f"Snooze {self.snooze_duration // 60} min",
            command=lambda: self.finish_break(False),
            font=('Helvetica', 18),
            bg='#E67E22',
            fg='white',
            padx=30,
            pady=15,
            relief='flat',
            cursor='hand2'
        )
        snooze_button.pack(side='left', padx=10)

        # Keyboard bindings
        self.fullscreen_window.bind('<Escape>', lambda e: self.finish_break(True))
        self.fullscreen_window.bind('<space>', lambda e: self.finish_break(True))

        # Start countdown
        self.break_countdown(self.break_duration)

        self.fullscreen_window.mainloop()

    def break_countdown(self, seconds):
        """Countdown timer for break"""
        if not self.fullscreen_window:
            return

        try:
            if seconds > 0:
                self.countdown_label.config(text=str(seconds))
                self.fullscreen_window.after(1000, lambda: self.break_countdown(seconds - 1))
            else:
                self.countdown_label.config(text="✓", fg='#27AE60')
        except Exception as e:
            print(f"Countdown error: {e}")

    def finish_break(self, reset=True):
        """Finish the break"""
        if self.fullscreen_window:
            self.fullscreen_window.destroy()
            self.fullscreen_window = None

        if reset:
            self.reset_timer(None)
        else:
            self.snooze_break()

    def show_about(self, _):
        """Show about dialog"""
        rumps.alert(
            title='20/20/20 Break Reminder',
            message='Version 1.0\n\n'
                    'Reminds you to follow the 20/20/20 rule:\n'
                    'Every 20 minutes, take a 20-second break\n'
                    'and look at something 20 feet away.\n\n'
                    'This helps reduce eye strain from screen time.',
            ok='OK'
        )

    def check_is_in_login_items(self):
        """Check if app is already in Login Items"""
        try:
            # Get the app bundle path
            result = subprocess.run(
                ['osascript', '-e', 'tell application "System Events" to get the name of every login item'],
                capture_output=True,
                text=True,
                timeout=5
            )
            login_items = result.stdout.strip()
            # Check if "Break Reminder" or "BreakReminder" is in login items
            return 'Break Reminder' in login_items or 'BreakReminder' in login_items
        except Exception as e:
            print(f"Error checking login items: {e}")
            return False

    def add_to_login_items(self):
        """Add app to Login Items using AppleScript"""
        try:
            # Get the path to the running app
            app_path = os.path.abspath(__file__)

            # If running as .app bundle, get the bundle path
            if '.app/Contents/' in app_path:
                # Extract path to .app bundle
                bundle_path = app_path.split('.app/Contents/')[0] + '.app'
            else:
                # Running from Python directly - can't add to Login Items
                rumps.alert(
                    title='Cannot Add to Login Items',
                    message='Auto-start only works when running as a standalone .app bundle.\n\n'
                            'To enable auto-start:\n'
                            '1. Build the app: ./build_app.sh\n'
                            '2. Install to Applications\n'
                            '3. Relaunch from Applications\n\n'
                            'See README for details.',
                    ok='OK'
                )
                return False

            # Use AppleScript to add to Login Items
            script = f'''
                tell application "System Events"
                    make new login item at end with properties {{path:"{bundle_path}", hidden:false}}
                end tell
            '''

            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                return True
            else:
                print(f"Error adding to login items: {result.stderr}")
                return False

        except Exception as e:
            print(f"Error adding to login items: {e}")
            return False

    def prompt_auto_start(self):
        """Prompt user to enable auto-start on first launch"""
        # Mark as no longer first launch
        self.config['first_launch'] = False
        self.save_config()

        # Check if already in login items
        if self.check_is_in_login_items():
            return

        # Show prompt
        response = rumps.alert(
            title='Welcome to Break Reminder! 👁️',
            message='Would you like Break Reminder to start automatically when you log in?\n\n'
                    'This ensures you never forget to take eye breaks!',
            ok='Yes, Auto-Start',
            cancel='No Thanks'
        )

        if response == 1:  # User clicked "Yes, Auto-Start"
            success = self.add_to_login_items()
            if success:
                rumps.notification(
                    title='Auto-Start Enabled! ✅',
                    subtitle='',
                    message='Break Reminder will now start automatically when you log in.'
                )

    def quit_app(self, _):
        """Quit the application"""
        if self.fullscreen_window:
            self.fullscreen_window.destroy()
        rumps.quit_application()


if __name__ == '__main__':
    app = BreakReminderApp()
    app.run()
