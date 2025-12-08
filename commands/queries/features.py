"""
Feature and parameter query commands.
"""

from ...utils import write_result


def get_features(command_id, params, ctx):
    """Get feature timeline information."""
    root = ctx.root

    features = []
    for i in range(root.features.count):
        feat = root.features.item(i)
        features.append({
            "name": feat.name,
            "index": i,
            "type": feat.objectType.split("::")[-1].replace("Feature", ""),
            "is_suppressed": feat.isSuppressed,
            "is_valid": feat.isValid
        })

    write_result(command_id, True, {"features": features, "count": len(features)})


def get_parameters(command_id, params, ctx):
    """Get user parameters."""
    design = ctx.design

    params_list = []
    for i in range(design.userParameters.count):
        param = design.userParameters.item(i)
        params_list.append({
            "name": param.name,
            "expression": param.expression,
            "value": param.value,
            "unit": param.unit,
            "comment": param.comment
        })

    write_result(command_id, True, {"parameters": params_list, "count": len(params_list)})


def get_all_parameters(command_id, params, ctx):
    """Get all parameters including model parameters (sketch dimensions, feature values)."""
    design = ctx.design

    user_params = []
    for i in range(design.userParameters.count):
        param = design.userParameters.item(i)
        user_params.append({
            "name": param.name,
            "expression": param.expression,
            "value": round(param.value, 6),
            "unit": param.unit,
            "comment": param.comment
        })

    model_params = []
    for i in range(design.allParameters.count):
        param = design.allParameters.item(i)
        # Skip user parameters (already captured above)
        if param.objectType == "adsk::fusion::UserParameter":
            continue

        # Get the parent/role info if available
        role = ""
        try:
            if hasattr(param, 'role'):
                role = param.role
        except:
            pass

        # Get created by (which feature/sketch created this parameter)
        created_by = ""
        try:
            if hasattr(param, 'createdBy') and param.createdBy:
                created_by = param.createdBy.name
        except:
            pass

        model_params.append({
            "name": param.name,
            "expression": param.expression,
            "value": round(param.value, 6),
            "unit": param.unit,
            "role": role,
            "created_by": created_by
        })

    write_result(command_id, True, {
        "user_parameters": user_params,
        "model_parameters": model_params,
        "counts": {
            "user": len(user_params),
            "model": len(model_params),
            "total": len(user_params) + len(model_params)
        }
    })


COMMANDS = {
    "get_features": get_features,
    "get_parameters": get_parameters,
    "get_all_parameters": get_all_parameters,
}
