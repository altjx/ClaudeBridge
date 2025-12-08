"""
Export and file operation commands.

Sub-modules:
- formats: Export to various formats (STL, STEP, F3D, IGES) [placeholder]
- file_ops: File operations (save, save_as) [placeholder]

See: docs/missing-features.md - Export & File Operations section
"""

try:
    from .formats import COMMANDS as FORMAT_COMMANDS
except ImportError:
    FORMAT_COMMANDS = {}

try:
    from .file_ops import COMMANDS as FILE_OPS_COMMANDS
except ImportError:
    FILE_OPS_COMMANDS = {}

# Merge all export commands
COMMANDS = {}
COMMANDS.update(FORMAT_COMMANDS)
COMMANDS.update(FILE_OPS_COMMANDS)
