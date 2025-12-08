"""
Construction plane commands.
"""

import adsk.core
import adsk.fusion

from ...utils import write_result
from ..helpers import get_construction_plane


def create_offset_plane(command_id, params, ctx):
    """
    Create a construction plane offset from an existing plane.

    Params:
        plane: Base plane ("xy", "xz", or "yz")
        offset: Distance in cm (positive = along normal direction)
        name: Optional name for the plane

    Returns:
        plane_name: Name of the created plane
        plane_index: Index of the created plane
    """
    root = ctx.root

    plane_name = params.get("plane", "xy")
    offset = params.get("offset", 1.0)
    custom_name = params.get("name", None)

    # Get the base construction plane
    base_plane, error = get_construction_plane(root, plane_name)
    if error:
        return write_result(command_id, False, None, error)

    try:
        # Create the offset plane
        planes = root.constructionPlanes
        plane_input = planes.createInput()

        # Set offset from base plane
        offset_value = adsk.core.ValueInput.createByReal(offset)
        plane_input.setByOffset(base_plane, offset_value)

        # Create the plane
        new_plane = planes.add(plane_input)

        # Optionally rename
        if custom_name:
            new_plane.name = custom_name

        write_result(command_id, True, {
            "plane_name": new_plane.name,
            "plane_index": planes.count - 1,
            "offset": offset,
            "base_plane": plane_name
        })

    except Exception as e:
        write_result(command_id, False, None, f"Failed to create offset plane: {str(e)}")


def create_plane_at_angle(command_id, params, ctx):
    """
    Create a construction plane at an angle from an existing plane.

    Params:
        plane: Base plane ("xy", "xz", or "yz")
        axis: Axis to rotate around ("x", "y", or "z")
        angle: Angle in degrees
        name: Optional name for the plane

    Returns:
        plane_name: Name of the created plane
        plane_index: Index of the created plane
    """
    root = ctx.root

    plane_name = params.get("plane", "xy")
    axis_name = params.get("axis", "x")
    angle = params.get("angle", 45.0)
    custom_name = params.get("name", None)

    # Get the base construction plane
    base_plane, error = get_construction_plane(root, plane_name)
    if error:
        return write_result(command_id, False, None, error)

    # Get the axis
    from ..helpers import get_construction_axis
    axis, error = get_construction_axis(root, axis_name)
    if error:
        return write_result(command_id, False, None, error)

    try:
        import math

        # Create the angled plane
        planes = root.constructionPlanes
        plane_input = planes.createInput()

        # Convert angle to radians
        angle_rad = math.radians(angle)
        angle_value = adsk.core.ValueInput.createByReal(angle_rad)

        # Set by angle from base plane around axis
        plane_input.setByAngle(axis, angle_value, base_plane)

        # Create the plane
        new_plane = planes.add(plane_input)

        # Optionally rename
        if custom_name:
            new_plane.name = custom_name

        write_result(command_id, True, {
            "plane_name": new_plane.name,
            "plane_index": planes.count - 1,
            "angle_degrees": angle,
            "base_plane": plane_name,
            "axis": axis_name
        })

    except Exception as e:
        write_result(command_id, False, None, f"Failed to create angled plane: {str(e)}")


COMMANDS = {
    "create_offset_plane": create_offset_plane,
    "create_plane_at_angle": create_plane_at_angle,
}
