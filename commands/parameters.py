"""
Parameter management commands.
"""

import adsk.core

from ..utils import write_result


def set_parameter(command_id, params, ctx):
    """Create or update a user parameter."""
    design = ctx.design

    name = params.get("name")
    value = params.get("value")
    unit = params.get("unit", "cm")

    if not name or value is None:
        return write_result(command_id, False, None, "Name and value required")

    existing = design.userParameters.itemByName(name)
    if existing:
        existing.expression = f"{value} {unit}"
        write_result(command_id, True, {"message": f"Updated {name} = {value} {unit}"})
    else:
        design.userParameters.add(
            name,
            adsk.core.ValueInput.createByString(f"{value} {unit}"),
            unit,
            ""
        )
        write_result(command_id, True, {"message": f"Created {name} = {value} {unit}"})


# Command registry for this module
COMMANDS = {
    "set_parameter": set_parameter,
}
