"""
Utility functions for session export.
"""

import json


def write_json(filepath, data):
    """Write JSON to file with pretty formatting."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def pt(point):
    """Round point coordinates."""
    return [round(point.x, 4), round(point.y, 4), round(point.z, 4)]
