"""
Constraint query and deletion commands.

Commands for listing constraints and deleting them.
"""

from ....utils import write_result
from ...helpers import get_sketch_by_global_index


def get_sketch_constraints(command_id, params, ctx):
    """
    Get all geometric constraints in a sketch.

    Params:
        sketch_index: Sketch index (default: last sketch)

    Returns list of constraints with their types and connected entities.
    """
    root = ctx.root
    sketch_index = params.get("sketch_index", -1)

    # Get the sketch
    sketch, comp, error = get_sketch_by_global_index(root, sketch_index)
    if error:
        return write_result(command_id, False, None, error)

    constraints = sketch.geometricConstraints
    constraint_list = []

    # Constraint type mapping
    constraint_types = {
        0: "Coincident",
        1: "Collinear",
        2: "Concentric",
        3: "Equal",
        4: "Fix",
        5: "Horizontal",
        6: "HorizontalPoints",
        7: "MidPoint",
        8: "Parallel",
        9: "Perpendicular",
        10: "Smooth",
        11: "Symmetry",
        12: "Tangent",
        13: "Vertical",
        14: "VerticalPoints",
        15: "CircularPattern",
        16: "RectangularPattern",
        17: "Offset",
        18: "Mirror"
    }

    for i in range(constraints.count):
        constraint = constraints.item(i)
        c_type = constraint_types.get(constraint.objectType, str(constraint.objectType))

        # Try to get more details about what the constraint connects
        constraint_info = {
            "index": i,
            "type": c_type,
            "is_deletable": constraint.isDeletable if hasattr(constraint, 'isDeletable') else None,
        }

        # Try to identify connected entities based on constraint type
        try:
            # Different constraints have different properties
            if hasattr(constraint, 'point'):
                pt = constraint.point
                constraint_info["point"] = [round(pt.geometry.x, 4), round(pt.geometry.y, 4)]
            if hasattr(constraint, 'line'):
                line = constraint.line
                constraint_info["line_start"] = [round(line.startSketchPoint.geometry.x, 4),
                                                  round(line.startSketchPoint.geometry.y, 4)]
                constraint_info["line_end"] = [round(line.endSketchPoint.geometry.x, 4),
                                                round(line.endSketchPoint.geometry.y, 4)]
            if hasattr(constraint, 'entityOne'):
                constraint_info["entity_one"] = str(constraint.entityOne.objectType)
            if hasattr(constraint, 'entityTwo'):
                constraint_info["entity_two"] = str(constraint.entityTwo.objectType)
        except:
            pass

        constraint_list.append(constraint_info)

    write_result(command_id, True, {
        "sketch_name": sketch.name,
        "component": comp.name,
        "constraint_count": len(constraint_list),
        "constraints": constraint_list
    })


def delete_constraint(command_id, params, ctx):
    """
    Delete a geometric constraint by index.

    Params:
        sketch_index: Sketch index (default: last sketch)
        constraint_index: Index of the constraint to delete

    Example:
        {"action": "delete_constraint", "params": {"constraint_index": 14}}
    """
    root = ctx.root
    sketch_index = params.get("sketch_index", -1)
    constraint_index = params.get("constraint_index", 0)

    sketch, comp, error = get_sketch_by_global_index(root, sketch_index)
    if error:
        return write_result(command_id, False, None, error)

    constraints = sketch.geometricConstraints

    if constraint_index < 0 or constraint_index >= constraints.count:
        return write_result(
            command_id, False, None,
            f"Invalid constraint index {constraint_index}. Sketch has {constraints.count} constraints."
        )

    constraint = constraints.item(constraint_index)

    if not constraint.isDeletable:
        return write_result(
            command_id, False, None,
            f"Constraint {constraint_index} is not deletable."
        )

    try:
        constraint.deleteMe()

        write_result(command_id, True, {
            "message": f"Constraint {constraint_index} deleted",
            "sketch_name": sketch.name,
            "component": comp.name
        })
    except Exception as e:
        write_result(command_id, False, None, f"Failed to delete constraint: {str(e)}")


COMMANDS = {
    "get_sketch_constraints": get_sketch_constraints,
    "delete_constraint": delete_constraint,
}
