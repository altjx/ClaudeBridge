"""
Line orientation constraint commands.

Commands for constraining lines to be vertical, horizontal, parallel, perpendicular, etc.
"""

from ....utils import write_result
from ...helpers import get_sketch_by_global_index


def add_constraint_vertical(command_id, params, ctx):
    """
    Add a vertical constraint to a line.

    Params:
        sketch_index: Sketch index (default: last sketch)
        line_index: Index of the line to make vertical

    Example:
        {"action": "add_constraint_vertical", "params": {"line_index": 5}}
    """
    root = ctx.root
    sketch_index = params.get("sketch_index", -1)
    line_index = params.get("line_index", 0)

    sketch, comp, error = get_sketch_by_global_index(root, sketch_index)
    if error:
        return write_result(command_id, False, None, error)

    lines = sketch.sketchCurves.sketchLines
    if line_index < 0 or line_index >= lines.count:
        return write_result(
            command_id, False, None,
            f"Invalid line index {line_index}. Sketch has {lines.count} lines."
        )

    line = lines.item(line_index)

    try:
        constraints = sketch.geometricConstraints
        constraints.addVertical(line)

        write_result(command_id, True, {
            "message": f"Vertical constraint added to line {line_index}",
            "sketch_name": sketch.name,
            "component": comp.name
        })
    except Exception as e:
        write_result(command_id, False, None, f"Failed to add vertical constraint: {str(e)}")


def add_constraint_horizontal(command_id, params, ctx):
    """
    Add a horizontal constraint to a line.

    Params:
        sketch_index: Sketch index (default: last sketch)
        line_index: Index of the line to make horizontal

    Example:
        {"action": "add_constraint_horizontal", "params": {"line_index": 5}}
    """
    root = ctx.root
    sketch_index = params.get("sketch_index", -1)
    line_index = params.get("line_index", 0)

    sketch, comp, error = get_sketch_by_global_index(root, sketch_index)
    if error:
        return write_result(command_id, False, None, error)

    lines = sketch.sketchCurves.sketchLines
    if line_index < 0 or line_index >= lines.count:
        return write_result(
            command_id, False, None,
            f"Invalid line index {line_index}. Sketch has {lines.count} lines."
        )

    line = lines.item(line_index)

    try:
        constraints = sketch.geometricConstraints
        constraints.addHorizontal(line)

        write_result(command_id, True, {
            "message": f"Horizontal constraint added to line {line_index}",
            "sketch_name": sketch.name,
            "component": comp.name
        })
    except Exception as e:
        write_result(command_id, False, None, f"Failed to add horizontal constraint: {str(e)}")


# Future commands:
# - add_constraint_parallel: Parallel lines
# - add_constraint_perpendicular: Perpendicular lines
# - add_constraint_tangent: Tangent curves
# - add_constraint_equal: Equal lengths

COMMANDS = {
    "add_constraint_vertical": add_constraint_vertical,
    "add_constraint_horizontal": add_constraint_horizontal,
}
