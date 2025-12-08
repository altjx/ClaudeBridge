"""
Parameter validation helpers.
"""

import adsk.fusion


def require_param(params, name, default=None):
    """
    Get a required parameter, returning default if not provided.

    Args:
        params: Parameters dictionary
        name: Parameter name
        default: Default value if not provided

    Returns:
        The parameter value or default
    """
    return params.get(name, default)


def get_operation_type(operation_name):
    """
    Convert operation name string to Fusion 360 FeatureOperation enum.

    Args:
        operation_name: "new", "join", or "cut"

    Returns:
        tuple: (FeatureOperation, error_message)
    """
    operations = {
        "new": adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
        "join": adsk.fusion.FeatureOperations.JoinFeatureOperation,
        "cut": adsk.fusion.FeatureOperations.CutFeatureOperation,
        "intersect": adsk.fusion.FeatureOperations.IntersectFeatureOperation,
    }

    op_lower = operation_name.lower() if operation_name else "new"

    if op_lower not in operations:
        return None, f"Unknown operation: {operation_name}. Use 'new', 'join', 'cut', or 'intersect'."

    return operations[op_lower], None
