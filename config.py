"""
Configuration and global state for Claude Bridge add-in.
"""

import os

# File paths - JSON files are stored in this add-in's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMMANDS_FILE = os.path.join(BASE_DIR, "commands.json")
RESULTS_FILE = os.path.join(BASE_DIR, "results.json")
STATUS_FILE = os.path.join(BASE_DIR, "bridge_status.json")

# Custom event identifier
CUSTOM_EVENT_ID = "ClaudeBridgeEvent"
