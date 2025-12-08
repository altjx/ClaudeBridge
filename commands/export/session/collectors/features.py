"""
Feature information collector for session export.
"""

import os
from ..utils import write_json


def export_features(root, all_components, session_dir):
    """
    Export feature timeline information.

    Collects information about all features in the design including
    their type, suppression status, and validity.

    Args:
        root: Root component
        all_components: List of all components in the design
        session_dir: Directory to write output files

    Returns:
        int: Number of features exported
    """
    features = []
    global_index = 0

    for comp in all_components:
        for i in range(comp.features.count):
            feat = comp.features.item(i)
            features.append({
                "name": feat.name,
                "index": global_index,
                "component": comp.name,
                "type": feat.objectType.split("::")[-1].replace("Feature", ""),
                "is_suppressed": feat.isSuppressed,
                "is_valid": feat.isValid
            })
            global_index += 1

    write_json(os.path.join(session_dir, "features.json"), {
        "features": features,
        "count": len(features)
    })
    return len(features)
