"""
Construction plane information collector for session export.
"""

import os
from ..utils import write_json


def export_construction_planes(root, session_dir):
    """
    Export construction plane information.

    Collects information about all construction planes in the root component
    including their names and visibility status.

    Args:
        root: Root component
        session_dir: Directory to write output files

    Returns:
        int: Number of construction planes exported
    """
    planes = root.constructionPlanes
    plane_list = []

    for i in range(planes.count):
        plane = planes.item(i)
        plane_list.append({
            "index": i,
            "name": plane.name,
            "is_visible": plane.isVisible
        })

    write_json(os.path.join(session_dir, "construction_planes.json"), {
        "planes": plane_list,
        "count": planes.count
    })
    return planes.count
