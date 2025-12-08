"""
Geometry helpers package for Fusion 360.

This package provides utilities for working with Fusion 360 geometry:
- components: Component hierarchy traversal
- sketches: Sketch selection and retrieval
- bodies: Body selection
- edges: Edge collection
- faces: Face selection and analysis
- planes: Construction planes and axes
"""

from .components import collect_all_components
from .sketches import get_all_sketches, get_sketch_by_global_index, get_sketch_by_index
from .bodies import get_body_by_index
from .edges import collect_edges
from .faces import find_top_face
from .planes import get_construction_axis, get_construction_plane

__all__ = [
    'collect_all_components',
    'get_all_sketches',
    'get_sketch_by_global_index',
    'get_sketch_by_index',
    'get_body_by_index',
    'collect_edges',
    'find_top_face',
    'get_construction_axis',
    'get_construction_plane',
]
