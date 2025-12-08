"""
Command utility decorators and helpers for reducing boilerplate.
"""

from functools import wraps
from ...utils import write_result


def with_sketch(fn):
    """
    Decorator that handles sketch retrieval and error checking.

    Injects `sketch` and `comp` keyword arguments into the decorated function.
    Expects `params` dict to have optional `sketch_index` (defaults to -1 for last).

    Usage:
        @with_sketch
        def my_command(command_id, params, ctx, sketch=None, comp=None):
            # sketch and comp are guaranteed to be valid here
            pass
    """
    @wraps(fn)
    def wrapper(command_id, params, ctx):
        from .geometry import get_sketch_by_global_index
        sketch_index = params.get("sketch_index", -1)
        sketch, comp, error = get_sketch_by_global_index(ctx.root, sketch_index)
        if error:
            return write_result(command_id, False, None, error)
        return fn(command_id, params, ctx, sketch=sketch, comp=comp)
    return wrapper


def with_error_handling(action_name):
    """
    Decorator for consistent try/except error handling.

    Usage:
        @with_error_handling("add vertical constraint")
        def add_constraint_vertical(command_id, params, ctx):
            # If exception raised, returns write_result with error message
            pass
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(command_id, *args, **kwargs):
            try:
                return fn(command_id, *args, **kwargs)
            except Exception as e:
                return write_result(command_id, False, None, f"Failed to {action_name}: {str(e)}")
        return wrapper
    return decorator
