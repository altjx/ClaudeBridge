"""
Background polling thread for command checking.
"""

import threading
import json

from ..config import CUSTOM_EVENT_ID


class PollingThread(threading.Thread):
    """Background thread that fires events to check for commands."""

    def __init__(self, stop_event, app):
        """
        Initialize the polling thread.

        Args:
            stop_event: threading.Event to signal when to stop
            app: Fusion 360 Application object
        """
        threading.Thread.__init__(self)
        self.stopped = stop_event
        self.app = app

    def run(self):
        """Fire event every second to check for commands."""
        while not self.stopped.wait(1.0):
            try:
                self.app.fireCustomEvent(CUSTOM_EVENT_ID, json.dumps({"check_commands": True}))
            except:
                pass  # App might be shutting down
