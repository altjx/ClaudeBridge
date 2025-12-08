"""
Modification feature commands: fillet, chamfer, shell.
"""

import adsk.core
import adsk.fusion

from ...utils import write_result
from ..helpers import get_body_by_index, collect_edges, find_top_face


def fillet(command_id, params, ctx):
    """Add fillet to edges of a body."""
    root = ctx.root

    body_idx = params.get("body_index", 0)
    radius = params.get("radius", 0.1)
    edge_indices = params.get("edge_indices", None)

    body, error = get_body_by_index(root, body_idx)
    if error:
        return write_result(command_id, False, None, error)

    fillets = root.features.filletFeatures
    fillet_input = fillets.createInput()

    edges = collect_edges(body, edge_indices, max_edges=50)

    if edges.count == 0:
        return write_result(command_id, False, None, "No edges to fillet")

    fillet_input.addConstantRadiusEdgeSet(
        edges, adsk.core.ValueInput.createByReal(radius), True
    )
    fillet_input.isRollingBallCorner = True
    fillets.add(fillet_input)

    write_result(command_id, True, {"message": f"Fillet added, radius {radius}cm"})


def chamfer(command_id, params, ctx):
    """Add chamfer to edges of a body."""
    root = ctx.root

    body_idx = params.get("body_index", 0)
    distance = params.get("distance", 0.1)
    edge_indices = params.get("edge_indices", None)

    body, error = get_body_by_index(root, body_idx)
    if error:
        return write_result(command_id, False, None, error)

    chamfers = root.features.chamferFeatures

    edges = collect_edges(body, edge_indices, max_edges=20)

    if edges.count == 0:
        return write_result(command_id, False, None, "No edges to chamfer")

    chamfer_input = chamfers.createInput2()
    chamfer_input.chamferEdgeSets.addEqualDistanceChamferEdgeSet(
        edges, adsk.core.ValueInput.createByReal(distance), True
    )
    chamfers.add(chamfer_input)

    write_result(command_id, True, {"message": f"Chamfer added, distance {distance}cm"})


def shell(command_id, params, ctx):
    """Hollow out a body by removing faces."""
    root = ctx.root

    body_idx = params.get("body_index", 0)
    thickness = params.get("thickness", 0.1)
    face_index = params.get("face_index", None)
    remove_top = params.get("remove_top", True)

    body, error = get_body_by_index(root, body_idx)
    if error:
        return write_result(command_id, False, None, error)

    shells = root.features.shellFeatures
    faces_to_remove = adsk.core.ObjectCollection.create()

    if face_index is not None:
        if face_index < body.faces.count:
            faces_to_remove.add(body.faces.item(face_index))
    elif remove_top:
        # Find top face (highest Z)
        top_face = find_top_face(body)
        if top_face:
            faces_to_remove.add(top_face)

    shell_input = shells.createInput(faces_to_remove)
    shell_input.insideThickness = adsk.core.ValueInput.createByReal(thickness)
    shells.add(shell_input)

    write_result(command_id, True, {"message": f"Shell created, thickness {thickness}cm"})


COMMANDS = {
    "fillet": fillet,
    "chamfer": chamfer,
    "shell": shell,
}
