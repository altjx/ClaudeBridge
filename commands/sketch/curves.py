"""
Advanced sketch curve commands: arc, ellipse, spline, slot.
"""

import math

import adsk.core

from ...utils import write_result
from ..helpers import get_sketch_by_index


def draw_arc(command_id, params, ctx):
    """
    Draw an arc defined by center point, start point, and end point.

    The arc is drawn counter-clockwise from start to end around the center.

    Params:
        sketch_index: Index of sketch (default: last sketch)
        center_x, center_y: Center point coordinates
        start_x, start_y: Start point coordinates
        end_x, end_y: End point coordinates
    """
    sketches = ctx.sketches

    idx = params.get("sketch_index", sketches.count - 1)
    center_x = params.get("center_x", 0)
    center_y = params.get("center_y", 0)
    start_x = params.get("start_x", 1)
    start_y = params.get("start_y", 0)
    end_x = params.get("end_x", 0)
    end_y = params.get("end_y", 1)

    sketch, error = get_sketch_by_index(sketches, idx)
    if error:
        return write_result(command_id, False, None, error)

    center = adsk.core.Point3D.create(center_x, center_y, 0)
    start = adsk.core.Point3D.create(start_x, start_y, 0)
    end = adsk.core.Point3D.create(end_x, end_y, 0)

    arc = sketch.sketchCurves.sketchArcs.addByCenterStartEnd(center, start, end)

    write_result(command_id, True, {
        "message": f"Arc from ({start_x},{start_y}) to ({end_x},{end_y}) around ({center_x},{center_y})",
        "radius": round(arc.radius, 4)
    })


def draw_arc_three_points(command_id, params, ctx):
    """
    Draw an arc passing through three points.

    Params:
        sketch_index: Index of sketch (default: last sketch)
        start_x, start_y: Start point of arc
        mid_x, mid_y: Point along the arc (determines curvature)
        end_x, end_y: End point of arc
    """
    sketches = ctx.sketches

    idx = params.get("sketch_index", sketches.count - 1)
    start_x = params.get("start_x", 0)
    start_y = params.get("start_y", 0)
    mid_x = params.get("mid_x", 0.5)
    mid_y = params.get("mid_y", 0.5)
    end_x = params.get("end_x", 1)
    end_y = params.get("end_y", 0)

    sketch, error = get_sketch_by_index(sketches, idx)
    if error:
        return write_result(command_id, False, None, error)

    start = adsk.core.Point3D.create(start_x, start_y, 0)
    mid = adsk.core.Point3D.create(mid_x, mid_y, 0)
    end = adsk.core.Point3D.create(end_x, end_y, 0)

    arc = sketch.sketchCurves.sketchArcs.addByThreePoints(start, mid, end)

    write_result(command_id, True, {
        "message": f"Arc through ({start_x},{start_y}), ({mid_x},{mid_y}), ({end_x},{end_y})",
        "radius": round(arc.radius, 4),
        "center": [
            round(arc.centerSketchPoint.geometry.x, 4),
            round(arc.centerSketchPoint.geometry.y, 4)
        ]
    })


def draw_arc_sweep(command_id, params, ctx):
    """
    Draw an arc defined by center, start point, and sweep angle.

    Params:
        sketch_index: Index of sketch (default: last sketch)
        center_x, center_y: Center point coordinates
        start_x, start_y: Start point coordinates (also defines radius)
        sweep_angle: Sweep angle in degrees (positive = counter-clockwise)
    """
    sketches = ctx.sketches

    idx = params.get("sketch_index", sketches.count - 1)
    center_x = params.get("center_x", 0)
    center_y = params.get("center_y", 0)
    start_x = params.get("start_x", 1)
    start_y = params.get("start_y", 0)
    sweep_angle = params.get("sweep_angle", 90)

    sketch, error = get_sketch_by_index(sketches, idx)
    if error:
        return write_result(command_id, False, None, error)

    center = adsk.core.Point3D.create(center_x, center_y, 0)
    start = adsk.core.Point3D.create(start_x, start_y, 0)
    sweep_rad = math.radians(sweep_angle)

    arc = sketch.sketchCurves.sketchArcs.addByCenterStartSweep(center, start, sweep_rad)

    # Calculate radius from center to start
    radius = math.sqrt((start_x - center_x)**2 + (start_y - center_y)**2)

    write_result(command_id, True, {
        "message": f"Arc {sweep_angle}° from ({start_x},{start_y}) around ({center_x},{center_y})",
        "radius": round(radius, 4),
        "sweep_angle": sweep_angle
    })


# Future commands:
# - draw_ellipse: Draw ellipse
# - draw_spline: Spline through points
# - draw_slot: Slot shapes

COMMANDS = {
    "draw_arc": draw_arc,
    "draw_arc_three_points": draw_arc_three_points,
    "draw_arc_sweep": draw_arc_sweep,
}
