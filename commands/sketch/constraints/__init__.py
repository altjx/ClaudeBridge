"""
Sketch geometric constraint commands.

Sub-modules:
- point: Point constraints (midpoint, coincident)
- line: Line orientation constraints (vertical, horizontal)
- query: Constraint queries and deletion
"""

from .point import COMMANDS as POINT_COMMANDS
from .line import COMMANDS as LINE_COMMANDS
from .query import COMMANDS as QUERY_COMMANDS

COMMANDS = {}
COMMANDS.update(POINT_COMMANDS)
COMMANDS.update(LINE_COMMANDS)
COMMANDS.update(QUERY_COMMANDS)
