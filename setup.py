"""
Setup script for building the Break Reminder macOS app with py2app
"""

from setuptools import setup
import sys

APP = ['break_reminder.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': None,  # You can add an .icns file later if you want a custom icon
    'plist': {
        'CFBundleName': 'Break Reminder',
        'CFBundleDisplayName': 'Break Reminder',
        'CFBundleGetInfoString': "20/20/20 Eye Break Reminder",
        'CFBundleIdentifier': 'com.breakreminder.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2024',
        'LSUIElement': True,  # This makes it a menu bar app (no dock icon)
        'NSAppleEventsUsageDescription': 'This app needs to access System Events to add itself to Login Items.',
    },
    'packages': ['rumps', 'tkinter', 'PIL'],
    'includes': [
        'subprocess',
        'json',
        'time',
        'threading',
        'pathlib',
        'os',
        'datetime',
    ],
    'frameworks': [],
    'excludes': ['numpy', 'matplotlib'],  # Exclude unused heavy packages
    'semi_standalone': False,
    'site_packages': True,
}

setup(
    name='BreakReminder',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
