"""
Face selection and analysis helpers for Fusion 360.
"""


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
