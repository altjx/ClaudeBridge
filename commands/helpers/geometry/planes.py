"""
Construction plane and axis helpers for Fusion 360.
"""


def get_construction_axis(root, axis_name):
    """
    Get a construction axis from the root component.

    Args:
        root: Root component
        axis_name: "x", "y", or "z"

    Returns:
        tuple: (axis_object, error_message)
    """
    axis_name = axis_name.lower()
    axes = {
        "x": root.xConstructionAxis,
        "y": root.yConstructionAxis,
        "z": root.zConstructionAxis,
    }

    if axis_name not in axes:
        return None, f"Unknown axis: {axis_name}. Use 'x', 'y', or 'z'."

    return axes[axis_name], None


def get_construction_plane(root, plane_name):
    """
    Get a construction plane from the root component.

    Args:
        root: Root component
        plane_name: "xy", "xz", or "yz"

    Returns:
        tuple: (plane_object, error_message)
    """
    plane_name = plane_name.lower()
    planes = {
        "xy": root.xYConstructionPlane,
        "xz": root.xZConstructionPlane,
        "yz": root.yZConstructionPlane,
    }

    if plane_name not in planes:
        return None, f"Unknown plane: {plane_name}. Use 'xy', 'xz', or 'yz'."

    return planes[plane_name], None
