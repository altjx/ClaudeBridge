"""
Geometry selection helpers for Fusion 360 objects.
"""

import adsk.core
import adsk.fusion


def get_body_by_index(root, index):
    """
    Get a body from the root component by index.

    Args:
        root: Root component
        index: Body index

    Returns:
        tuple: (body, error_message) - body is None if error
    """
    if index >= root.bRepBodies.count:
        return None, f"Invalid body index {index}. Design has {root.bRepBodies.count} bodies."
    return root.bRepBodies.item(index), None


def get_sketch_by_index(sketches, index):
    """
    Get a sketch by index, defaulting to last sketch if index is -1 or None.

    Args:
        sketches: Sketches collection
        index: Sketch index (None/-1 for last sketch)

    Returns:
        tuple: (sketch, error_message) - sketch is None if error
    """
    if index is None or index == -1:
        index = sketches.count - 1

    if index < 0 or index >= sketches.count:
        return None, f"Invalid sketch index {index}. Design has {sketches.count} sketches."

    return sketches.item(index), None


def collect_edges(body, edge_indices=None, max_edges=50):
    """
    Collect edges from a body into an ObjectCollection.

    Args:
        body: The body to collect edges from
        edge_indices: List of specific edge indices, or None for all edges
        max_edges: Maximum edges to collect if edge_indices is None

    Returns:
        ObjectCollection of edges
    """
    edges = adsk.core.ObjectCollection.create()

    if edge_indices:
        for idx in edge_indices:
            if idx < body.edges.count:
                edges.add(body.edges.item(idx))
    else:
        for i in range(min(body.edges.count, max_edges)):
            edges.add(body.edges.item(i))

    return edges


def find_top_face(body):
    """
    Find the topmost planar face of a body (highest Z coordinate).

    Args:
        body: The body to search

    Returns:
        The top face, or None if no planar faces found
    """
    top_face = None
    max_z = -9999

    for face in body.faces:
        # Only consider planar faces (surfaceType 0 = Plane)
        if face.geometry.surfaceType == 0:
            bbox = face.boundingBox
            z = (bbox.minPoint.z + bbox.maxPoint.z) / 2
            if z > max_z:
                max_z = z
                top_face = face

    return top_face


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
