"""
Timeline and edit operation commands.

Sub-modules:
- operations: Timeline operations (delete, suppress, rollback, edit) [placeholder]

See: docs/missing-features.md - Delete & Edit Operations section
"""

try:
    from .operations import COMMANDS as OPERATION_COMMANDS
except ImportError:
    OPERATION_COMMANDS = {}

# Merge all timeline commands
COMMANDS = {}
COMMANDS.update(OPERATION_COMMANDS)
