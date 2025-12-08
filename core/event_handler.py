"""
Custom event handler for processing commands from the worker thread.
"""

import adsk.core
import json
import os

from ..config import COMMANDS_FILE


class ThreadEventHandler(adsk.core.CustomEventHandler):
    """Handle events fired from the worker thread."""

    def __init__(self, command_executor):
        """
        Initialize the event handler.

        Args:
            command_executor: Callable that takes a command dict and returns
                              the command_id that was processed
        """
        super().__init__()
        self.command_executor = command_executor
        self.last_command_id = 0

    def notify(self, args):
        """Called when a custom event is fired."""
        try:
            event_args = json.loads(args.additionalInfo)
            if event_args.get("check_commands"):
                self._check_and_execute_commands()
        except:
            pass  # Ignore parse errors

    def _check_and_execute_commands(self):
        """Check for new commands and execute them."""
        if os.path.exists(COMMANDS_FILE):
            with open(COMMANDS_FILE, 'r') as f:
                content = f.read().strip()
                if content:
                    cmd = json.loads(content)
                    cmd_id = cmd.get("id", 0)
                    if cmd_id > self.last_command_id:
                        self.last_command_id = self.command_executor(cmd)
