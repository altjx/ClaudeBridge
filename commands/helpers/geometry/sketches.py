"""
Sketch selection and retrieval helpers for Fusion 360.
"""

from .components import collect_all_components


def get_all_sketches(root):
    """
    Get all sketches across all components with global indexing.

    Args:
        root: Root component

    Returns:
        List of tuples: (sketch, global_index, component)
    """
    all_components = collect_all_components(root)
    sketches = []
    global_index = 0

    for comp in all_components:
        for i in range(comp.sketches.count):
            sketch = comp.sketches.item(i)
            sketches.append((sketch, global_index, comp))
            global_index += 1

    return sketches


def get_sketch_by_global_index(root, index):
    """
    Get a sketch by global index across all components.

    Args:
        root: Root component
        index: Global sketch index (or -1/None for last sketch)

    Returns:
        tuple: (sketch, component, error_message)
    """
    all_sketches = get_all_sketches(root)

    if not all_sketches:
        return None, None, "No sketches in design"

    if index is None or index == -1:
        index = len(all_sketches) - 1

    if index < 0 or index >= len(all_sketches):
        return None, None, f"Invalid sketch index {index}. Design has {len(all_sketches)} sketches."

    sketch, _, comp = all_sketches[index]
    return sketch, comp, None


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
