"""
Basic 3D feature commands: extrude, revolve, list_profiles.
"""

import math

import adsk.core
import adsk.fusion

from ...utils import write_result
from ..helpers import get_sketch_by_index, get_construction_axis, get_operation_type


def extrude(command_id, params, ctx):
    """Extrude a sketch profile to create a 3D body."""
    sketches = ctx.sketches
    extrudes = ctx.extrudes

    idx = params.get("sketch_index", sketches.count - 1)
    profile_idx = params.get("profile_index", 0)
    height = params.get("height", 1)
    op = params.get("operation", "new")

    sketch, error = get_sketch_by_index(sketches, idx)
    if error:
        return write_result(command_id, False, None, error)

    if profile_idx >= sketch.profiles.count:
        return write_result(command_id, False, None,
                            f"Invalid profile. Has {sketch.profiles.count}")

    profile = sketch.profiles.item(profile_idx)

    operation, error = get_operation_type(op)
    if error:
        return write_result(command_id, False, None, error)

    ext_input = extrudes.createInput(profile, operation)
    ext_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(height))
    extrudes.add(ext_input)

    write_result(command_id, True, {"message": f"Extruded {height}cm"})


def revolve(command_id, params, ctx):
    """
    Revolve a sketch profile around an axis to create a 3D body.

    Params:
        sketch_index: Index of sketch (default: last sketch)
        profile_index: Index of profile in sketch (default: 0)
        angle: Angle in degrees (default: 360 for full revolution)
        axis: "x", "y", "z" for construction axes, or "line" for sketch line
        axis_line_index: Index of sketch line to use as axis (when axis="line")
        operation: "new", "join", or "cut" (default: "new")
    """
    sketches = ctx.sketches
    root = ctx.root

    sketch_index = params.get("sketch_index", sketches.count - 1)
    profile_index = params.get("profile_index", 0)
    angle = params.get("angle", 360)
    axis = params.get("axis", "x")
    axis_line_index = params.get("axis_line_index", 0)
    operation = params.get("operation", "new")

    sketch, error = get_sketch_by_index(sketches, sketch_index)
    if error:
        return write_result(command_id, False, None, error)

    if profile_index >= sketch.profiles.count:
        return write_result(command_id, False, None,
                            f"Invalid profile. Has {sketch.profiles.count}")

    profile = sketch.profiles.item(profile_index)

    # Get the axis
    axis_lower = axis.lower()
    if axis_lower in ("x", "y", "z"):
        axis_obj, error = get_construction_axis(root, axis_lower)
        if error:
            return write_result(command_id, False, None, error)
    elif axis_lower == "line":
        # Use a sketch line as axis
        if axis_line_index >= sketch.sketchCurves.sketchLines.count:
            return write_result(command_id, False, None,
                                f"Invalid axis line index. Has {sketch.sketchCurves.sketchLines.count} lines")
        axis_obj = sketch.sketchCurves.sketchLines.item(axis_line_index)
    else:
        return write_result(command_id, False, None, f"Unknown axis: {axis}")

    # Convert angle to radians
    angle_rad = math.radians(angle)

    # Get operation type
    op, error = get_operation_type(operation)
    if error:
        return write_result(command_id, False, None, error)

    revolves = root.features.revolveFeatures
    rev_input = revolves.createInput(profile, axis_obj, op)

    # Set the angle extent
    angle_value = adsk.core.ValueInput.createByReal(angle_rad)
    rev_input.setAngleExtent(False, angle_value)

    revolves.add(rev_input)

    write_result(command_id, True, {"message": f"Revolved {angle}° around {axis} axis"})


def list_profiles(command_id, params, ctx):
    """List all profiles in a sketch with their areas."""
    sketches = ctx.sketches

    idx = params.get("sketch_index", sketches.count - 1)

    sketch, error = get_sketch_by_index(sketches, idx)
    if error:
        return write_result(command_id, False, None, error)

    profiles = [
        {"index": i, "area": round(sketch.profiles.item(i).areaProperties().area, 4)}
        for i in range(sketch.profiles.count)
    ]

    write_result(command_id, True, {"profiles": profiles})


COMMANDS = {
    "extrude": extrude,
    "revolve": revolve,
    "list_profiles": list_profiles,
}
