"""
Construction geometry commands.

Sub-modules:
- planes: Construction plane creation [placeholder]
- axes: Construction axis creation [placeholder]
- points: Construction point creation [placeholder]

See: docs/missing-features.md - Construction Geometry section
"""

try:
    from .planes import COMMANDS as PLANE_COMMANDS
except ImportError:
    PLANE_COMMANDS = {}

try:
    from .axes import COMMANDS as AXIS_COMMANDS
except ImportError:
    AXIS_COMMANDS = {}

try:
    from .points import COMMANDS as POINT_COMMANDS
except ImportError:
    POINT_COMMANDS = {}

# Merge all construction commands
COMMANDS = {}
COMMANDS.update(PLANE_COMMANDS)
COMMANDS.update(AXIS_COMMANDS)
COMMANDS.update(POINT_COMMANDS)
