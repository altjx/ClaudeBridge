# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ClaudeBridge is a Fusion 360 add-in that enables Claude to programmatically control Autodesk Fusion 360. It implements a file-based IPC architecture where Claude writes JSON commands to `commands.json`, the add-in polls and executes them, and results are written to `results.json`.

## Running the Add-in

1. Place the add-in in Fusion 360's AddIns directory:
   - macOS: `~/Library/Application Support/Autodesk/Fusion 360/API/AddIns/ClaudeBridge`
   - Windows: `C:\Users\<user>\AppData\Roaming\Autodesk\Fusion 360\API\AddIns\ClaudeBridge`
2. Open Fusion 360 and create/open a design
3. Shift+S → Add-Ins → ClaudeBridge → Run

## Architecture

> **Full details**: See `docs/architecture.md` for comprehensive architecture documentation.

```
ClaudeBridge.py              # Entry point (run/stop lifecycle)
config.py                    # File paths, event IDs
utils.py                     # JSON read/write utilities
core/
  polling.py                 # Background thread fires custom events every 1s
  event_handler.py           # Handles events on main thread, dispatches commands
commands/
  __init__.py                # Command registry (merges all COMMANDS dicts)
  dispatcher.py              # execute_command() - central dispatch
  context.py                 # CommandContext - abstracts F360 API objects
  helpers/                   # Shared utilities (geometry, validation)
  basic.py                   # ping, message
  parameters.py              # set_parameter
  queries/                   # get_info, get_full_design, get_bodies_detailed, etc.
  sketch/                    # create_sketch, draw_circle, draw_rectangle, draw_line
  features/                  # extrude, revolve, fillet, chamfer, shell, list_profiles
  construction/              # [future] offset planes, axes, points
  timeline/                  # [future] delete, suppress, rollback
  assembly/                  # [future] components, joints
  export/                    # [future] STL, STEP, save
```

**Key pattern**: Background polling thread fires custom Fusion 360 events. Event handler runs on Fusion 360's main thread (required for API calls). Command ID sequencing prevents duplicate execution.

## Adding New Commands

1. Choose the appropriate sub-module:
   - `queries/` - Design information retrieval
   - `sketch/` - 2D sketch operations
   - `features/` - 3D feature creation
   - `construction/` - Construction geometry
   - `timeline/` - Delete/edit operations
   - `assembly/` - Components and joints
   - `export/` - File export

2. Create handler function in the appropriate file:
```python
from ...utils import write_result
from ..helpers import get_sketch_by_index

def my_command(command_id, params, ctx):
    """Description of what this command does."""
    # Implementation...
    write_result(command_id, True, {"message": "Success"})

COMMANDS = {
    "my_command": my_command,
}
```

3. The registry in `commands/__init__.py` automatically merges all COMMANDS dicts.

**Handler signature**: `def handler(command_id: int, params: dict, ctx: CommandContext) -> None`

## Command Structure

```json
{
  "id": <incrementing_int>,
  "action": "<command_name>",
  "params": { ... }
}
```

The `id` must be higher than the previous command or it will be ignored.

## Important Details

- **Units**: All dimensions in centimeters (Fusion 360 internal unit). For 50mm use `5`.
- **Planes**: `"xy"`, `"xz"`, `"yz"` (lowercase)
- **Extrude operations**: `"new"` (new body), `"join"` (add to existing), `"cut"` (subtract)
- **Revolve axis**: `"x"`, `"y"`, `"z"` for construction axes, or `"line"` with `axis_line_index` for sketch line
- **Revolve angle**: Degrees (default 360 for full revolution)
- **Defaults**: sketch_index defaults to last created sketch; body_index defaults to 0

## Shared Helpers

Use helpers from `commands/helpers/` for common operations:

```python
from ..helpers import (
    get_body_by_index,       # Safe body lookup with error handling
    get_sketch_by_index,     # Safe sketch lookup
    collect_edges,           # Collect edges for fillet/chamfer
    find_top_face,           # Find topmost face of body
    get_construction_axis,   # Get X/Y/Z axis
    get_construction_plane,  # Get XY/XZ/YZ plane
    get_operation_type,      # Convert "new"/"join"/"cut" to enum
)
```

## File Paths

Files are stored in the add-in directory (see `config.py`):
- `commands.json` - Claude writes commands here
- `results.json` - Bridge writes execution results here
- `bridge_status.json` - Current bridge status

## Documentation

- `docs/architecture.md` - Full architecture documentation
- `docs/missing-features.md` - Feature roadmap with API references

## Debugging

VS Code launch.json is configured for Python attach debugging on port 9000.
