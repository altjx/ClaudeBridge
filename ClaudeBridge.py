"""
Claude Bridge Add-in for Fusion 360
===================================
Uses threading and custom events to poll for commands from Claude.

Based on official Autodesk Custom Event Sample pattern.

This is the main entry point. The actual command handling is organized in:
- config.py: Configuration and constants
- utils.py: File I/O utilities
- core/: Event handling and polling infrastructure
- commands/: Command handlers organized by category
"""

import adsk.core
import adsk.fusion
import traceback
import threading
import os

# Import from our modules
from .config import CUSTOM_EVENT_ID, COMMANDS_FILE, STATUS_FILE
from .utils import write_json
from .core import PollingThread, ThreadEventHandler
from .commands import execute_command

# Global references (required for Fusion 360 add-in lifecycle)
app = None
ui = None
handlers = []
stop_flag = None
custom_event = None


def _create_command_executor():
    """Create a command executor closure that captures app and ui."""
    def executor(cmd):
        return execute_command(cmd, app, ui)
    return executor


def run(context):
    """Called when add-in starts."""
    global app, ui, custom_event, stop_flag, handlers

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Write status
        write_json(STATUS_FILE, {"status": "running", "message": "Bridge active"})

        # Clear old commands
        if os.path.exists(COMMANDS_FILE):
            os.remove(COMMANDS_FILE)

        # Register custom event
        custom_event = app.registerCustomEvent(CUSTOM_EVENT_ID)

        # Create event handler with command executor
        event_handler = ThreadEventHandler(_create_command_executor())
        custom_event.add(event_handler)
        handlers.append(event_handler)

        # Start polling thread
        stop_flag = threading.Event()
        polling_thread = PollingThread(stop_flag, app)
        polling_thread.start()

        ui.messageBox(
            "Claude Bridge is active!\n\n"
            "Commands are checked every second.\n"
            "Claude can now send commands.",
            "Claude Bridge"
        )

    except:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')


def stop(context):
    """Called when add-in stops."""
    global stop_flag, custom_event, handlers

    try:
        # Stop the thread
        if stop_flag:
            stop_flag.set()

        # Unregister event
        if custom_event and handlers:
            custom_event.remove(handlers[0])
        if custom_event:
            app.unregisterCustomEvent(CUSTOM_EVENT_ID)

        handlers = []

        write_json(STATUS_FILE, {"status": "stopped", "message": "Bridge stopped"})

    except:
        pass
