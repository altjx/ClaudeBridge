"""Utilities for accessing sketch curves and geometry with consistent error handling.

This module provides safe accessor functions for sketch curves (lines, circles, arcs, ellipses),
their geometric properties (endpoints, centers), and sketch constraints. Each function returns
a tuple of (object, error_message) to enable consistent error handling across constraint and
sketch command handlers.

Pattern:
    curve, error = get_line(sketch, 0)
    if error:
        write_result(command_id, False, {"error": error})
        return
    # Use curve...
"""

def get_line(sketch, index):
    """Get a sketch line by index with error handling.

    Args:
        sketch: The Sketch object
        index: Line index (0-based)

    Returns:
        tuple: (line, error_message) - line is None if error
    """
    lines = sketch.sketchCurves.sketchLines
    if index < 0 or index >= lines.count:
        return None, f"Invalid line index {index}. Sketch has {lines.count} lines."
    return lines.item(index), None


def get_circle(sketch, index):
    """Get a sketch circle by index with error handling.

    Args:
        sketch: The Sketch object
        index: Circle index (0-based)

    Returns:
        tuple: (circle, error_message) - circle is None if error
    """
    circles = sketch.sketchCurves.sketchCircles
    if index < 0 or index >= circles.count:
        return None, f"Invalid circle index {index}. Sketch has {circles.count} circles."
    return circles.item(index), None


def get_arc(sketch, index):
    """Get a sketch arc by index with error handling.

    Args:
        sketch: The Sketch object
        index: Arc index (0-based)

    Returns:
        tuple: (arc, error_message) - arc is None if error
    """
    arcs = sketch.sketchCurves.sketchArcs
    if index < 0 or index >= arcs.count:
        return None, f"Invalid arc index {index}. Sketch has {arcs.count} arcs."
    return arcs.item(index), None


def get_ellipse(sketch, index):
    """Get a sketch ellipse by index with error handling.

    Args:
        sketch: The Sketch object
        index: Ellipse index (0-based)

    Returns:
        tuple: (ellipse, error_message) - ellipse is None if error
    """
    ellipses = sketch.sketchCurves.sketchEllipses
    if index < 0 or index >= ellipses.count:
        return None, f"Invalid ellipse index {index}. Sketch has {ellipses.count} ellipses."
    return ellipses.item(index), None


def get_line_endpoint(sketch, line_index, endpoint="end"):
    """Get a specific endpoint from a sketch line.

    Args:
        sketch: The Sketch object
        line_index: Line index (0-based)
        endpoint: "start" or "end" (default: "end")

    Returns:
        tuple: (point, error_message) - point is None if error
    """
    line, error = get_line(sketch, line_index)
    if error:
        return None, error

    if endpoint not in ["start", "end"]:
        return None, f"Invalid endpoint '{endpoint}'. Must be 'start' or 'end'."

    point = line.startSketchPoint if endpoint == "start" else line.endSketchPoint
    if not point:
        return None, f"Line {line_index} has no {endpoint} point."

    return point, None


def get_circle_center(sketch, circle_index):
    """Get the center point of a sketch circle.

    Args:
        sketch: The Sketch object
        circle_index: Circle index (0-based)

    Returns:
        tuple: (point, error_message) - point is None if error
    """
    circle, error = get_circle(sketch, circle_index)
    if error:
        return None, error

    center = circle.centerSketchPoint
    if not center:
        return None, f"Circle {circle_index} has no center point."

    return center, None


def get_arc_center(sketch, arc_index):
    """Get the center point of a sketch arc.

    Args:
        sketch: The Sketch object
        arc_index: Arc index (0-based)

    Returns:
        tuple: (point, error_message) - point is None if error
    """
    arc, error = get_arc(sketch, arc_index)
    if error:
        return None, error

    center = arc.centerSketchPoint
    if not center:
        return None, f"Arc {arc_index} has no center point."

    return center, None


def get_arc_endpoint(sketch, arc_index, endpoint="end"):
    """Get a specific endpoint from a sketch arc.

    Args:
        sketch: The Sketch object
        arc_index: Arc index (0-based)
        endpoint: "start" or "end" (default: "end")

    Returns:
        tuple: (point, error_message) - point is None if error
    """
    arc, error = get_arc(sketch, arc_index)
    if error:
        return None, error

    if endpoint not in ["start", "end"]:
        return None, f"Invalid endpoint '{endpoint}'. Must be 'start' or 'end'."

    point = arc.startSketchPoint if endpoint == "start" else arc.endSketchPoint
    if not point:
        return None, f"Arc {arc_index} has no {endpoint} point."

    return point, None


def get_constraint(sketch, index):
    """Get a sketch constraint by index with error handling.

    Args:
        sketch: The Sketch object
        index: Constraint index (0-based)

    Returns:
        tuple: (constraint, error_message) - constraint is None if error
    """
    constraints = sketch.geometricConstraints
    if index < 0 or index >= constraints.count:
        return None, f"Invalid constraint index {index}. Sketch has {constraints.count} constraints."
    return constraints.item(index), None


def get_sketch_point(sketch, index):
    """Get a sketch point by index with error handling.

    Args:
        sketch: The Sketch object
        index: Point index (0-based)

    Returns:
        tuple: (point, error_message) - point is None if error
    """
    points = sketch.sketchPoints
    if index < 0 or index >= points.count:
        return None, f"Invalid point index {index}. Sketch has {points.count} points."
    return points.item(index), None
