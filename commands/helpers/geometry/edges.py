"""
Edge selection and collection helpers for Fusion 360.
"""

import adsk.core


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
