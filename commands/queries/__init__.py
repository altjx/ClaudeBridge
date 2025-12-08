"""
Query commands for retrieving design information.

Sub-modules:
- design: Overall design queries (get_info, get_full_design)
- bodies: Body-related queries (get_bodies_detailed)
- sketches: Sketch-related queries (get_sketches_detailed, get_sketch_geometry)
- features: Feature and parameter queries (get_features, get_parameters, get_all_parameters)
"""

from .design import COMMANDS as DESIGN_COMMANDS
from .bodies import COMMANDS as BODY_COMMANDS
from .sketches import COMMANDS as SKETCH_COMMANDS
from .features import COMMANDS as FEATURE_COMMANDS

# Merge all query commands
COMMANDS = {}
COMMANDS.update(DESIGN_COMMANDS)
COMMANDS.update(BODY_COMMANDS)
COMMANDS.update(SKETCH_COMMANDS)
COMMANDS.update(FEATURE_COMMANDS)
