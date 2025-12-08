"""
Command dispatcher - routes commands to appropriate handlers.
"""

from ..utils import write_result
from .context import CommandContext
from . import get_handler


def execute_command(cmd, app, ui):
    """
    Execute a command from Claude.

    Args:
        cmd: Command dictionary with 'id', 'action', and 'params'
        app: Fusion 360 Application object
        ui: Fusion 360 UserInterface object

    Returns:
        int: The command_id that was processed
    """
    command_id = cmd.get("id", 0)
    action = cmd.get("action", "")
    params = cmd.get("params", {})

    try:
        # Create context for this command
        ctx = CommandContext(app, ui)

        # Check if design is required (all commands except ping and message)
        if action not in ("ping", "message"):
            success, error = ctx.require_design()
            if not success:
                write_result(command_id, False, None, error)
                return command_id

        # Get the handler for this action
        handler = get_handler(action)

        if handler:
            handler(command_id, params, ctx)
        else:
            write_result(command_id, False, None, f"Unknown action: {action}")

    except Exception as e:
        write_result(command_id, False, None, str(e))

    return command_id
