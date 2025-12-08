"""
Component hierarchy helpers for Fusion 360.
"""


def collect_all_components(root):
    """
    Recursively collect all components in the design hierarchy.

    Args:
        root: Root component

    Returns:
        List of all components (including root)
    """
    components = [root]

    def traverse_occurrences(occurrences):
        for i in range(occurrences.count):
            occ = occurrences.item(i)
            comp = occ.component
            components.append(comp)
            if comp.occurrences.count > 0:
                traverse_occurrences(comp.occurrences)

    traverse_occurrences(root.occurrences)
    return components
