"""
Shared helper utilities for command handlers.
"""

from .geometry import (
    get_body_by_index,
    get_sketch_by_index,
    collect_edges,
    find_top_face,
    get_construction_axis,
    get_construction_plane,
)
from .validation import require_param, get_operation_type
