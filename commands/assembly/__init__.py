"""
Component and assembly commands.

Sub-modules:
- components: Component management [placeholder]
- joints: Assembly joints [placeholder]

See: docs/missing-features.md - Components & Assembly section
"""

try:
    from .components import COMMANDS as COMPONENT_COMMANDS
except ImportError:
    COMPONENT_COMMANDS = {}

try:
    from .joints import COMMANDS as JOINT_COMMANDS
except ImportError:
    JOINT_COMMANDS = {}

# Merge all assembly commands
COMMANDS = {}
COMMANDS.update(COMPONENT_COMMANDS)
COMMANDS.update(JOINT_COMMANDS)
