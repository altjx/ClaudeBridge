"""
Body selection and retrieval helpers for Fusion 360.
"""


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
