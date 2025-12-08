"""
Basic sketch shape commands: circle, rectangle, line, polygon.
"""

import adsk.core

from ...utils import write_result
from ..helpers import get_sketch_by_index


def draw_circle(command_id, params, ctx):
    """Draw a circle on a sketch."""
    sketches = ctx.sketches

    idx = params.get("sketch_index", sketches.count - 1)
    x = params.get("x", 0)
    y = params.get("y", 0)
    r = params.get("radius", 1)

    sketch, error = get_sketch_by_index(sketches, idx)
    if error:
        return write_result(command_id, False, None, error)

    sketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(x, y, 0), r
    )

    write_result(command_id, True, {"message": f"Circle at ({x},{y}) r={r}"})


def draw_rectangle(command_id, params, ctx):
    """Draw a rectangle on a sketch."""
    sketches = ctx.sketches

    idx = params.get("sketch_index", sketches.count - 1)
    x = params.get("x", 0)
    y = params.get("y", 0)
    w = params.get("width", 1)
    h = params.get("height", 1)

    sketch, error = get_sketch_by_index(sketches, idx)
    if error:
        return write_result(command_id, False, None, error)

    lines = sketch.sketchCurves.sketchLines

    p1 = adsk.core.Point3D.create(x, y, 0)
    p2 = adsk.core.Point3D.create(x + w, y, 0)
    p3 = adsk.core.Point3D.create(x + w, y + h, 0)
    p4 = adsk.core.Point3D.create(x, y + h, 0)

    lines.addByTwoPoints(p1, p2)
    lines.addByTwoPoints(p2, p3)
    lines.addByTwoPoints(p3, p4)
    lines.addByTwoPoints(p4, p1)

    write_result(command_id, True, {"message": f"Rectangle at ({x},{y}) {w}x{h}"})


def draw_line(command_id, params, ctx):
    """Draw a line on a sketch."""
    sketches = ctx.sketches

    idx = params.get("sketch_index", sketches.count - 1)
    x1 = params.get("x1", 0)
    y1 = params.get("y1", 0)
    x2 = params.get("x2", 1)
    y2 = params.get("y2", 1)

    sketch, error = get_sketch_by_index(sketches, idx)
    if error:
        return write_result(command_id, False, None, error)

    sketch.sketchCurves.sketchLines.addByTwoPoints(
        adsk.core.Point3D.create(x1, y1, 0),
        adsk.core.Point3D.create(x2, y2, 0)
    )

    write_result(command_id, True, {"message": f"Line ({x1},{y1})->({x2},{y2})"})


COMMANDS = {
    "draw_circle": draw_circle,
    "draw_rectangle": draw_rectangle,
    "draw_line": draw_line,
}
