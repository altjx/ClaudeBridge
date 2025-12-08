"""
Utility functions for file I/O operations.
"""

import json
import time

from .config import RESULTS_FILE


def write_json(filepath, data):
    """Write JSON to file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def write_result(command_id, success, result, error=None):
    """Write command result."""
    write_json(RESULTS_FILE, {
        "command_id": command_id,
        "success": success,
        "result": result,
        "error": error,
        "timestamp": time.time()
    })
