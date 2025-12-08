"""
3D feature creation commands.

Sub-modules:
- basic: Basic features (extrude, revolve, list_profiles)
- modify: Modification features (fillet, chamfer, shell, draft)
- advanced: Advanced features (sweep, loft, hole, thread) [placeholder]
- patterns: Pattern features (rectangular, circular, mirror, path) [placeholder]
- body_ops: Body operations (combine, split, move, copy, scale) [placeholder]
"""

from .basic import COMMANDS as BASIC_COMMANDS
from .modify import COMMANDS as MODIFY_COMMANDS

# Import placeholder modules if they have commands
try:
    from .advanced import COMMANDS as ADVANCED_COMMANDS
except ImportError:
    ADVANCED_COMMANDS = {}

try:
    from .patterns import COMMANDS as PATTERN_COMMANDS
except ImportError:
    PATTERN_COMMANDS = {}

try:
    from .body_ops import COMMANDS as BODY_OPS_COMMANDS
except ImportError:
    BODY_OPS_COMMANDS = {}

# Merge all feature commands
COMMANDS = {}
COMMANDS.update(BASIC_COMMANDS)
COMMANDS.update(MODIFY_COMMANDS)
COMMANDS.update(ADVANCED_COMMANDS)
COMMANDS.update(PATTERN_COMMANDS)
COMMANDS.update(BODY_OPS_COMMANDS)
