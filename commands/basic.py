"""
Basic commands: ping, message
"""

from ..utils import write_result


def ping(command_id, params, ctx):
    """Respond to ping with pong."""
    write_result(command_id, True, {"message": "pong"})


def message(command_id, params, ctx):
    """Display a message box to the user."""
    text = params.get("text", "Hello!")
    ctx.ui.messageBox(text, "Claude")
    write_result(command_id, True, {"message": "displayed"})


# Command registry for this module
COMMANDS = {
    "ping": ping,
    "message": message,
}
