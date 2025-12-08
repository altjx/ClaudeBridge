# ClaudeBridge Architecture

This document describes the architecture of ClaudeBridge, a Fusion 360 add-in that enables Claude to programmatically control Autodesk Fusion 360.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Claude (AI)                                     │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │ writes JSON
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           commands.json                                      │
│                    (File-based IPC mechanism)                               │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │ polls every 1s
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ClaudeBridge Add-in                                  │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────────────────────┐ │
│  │ PollingThread│───▶│ CustomEvent  │───▶│    Command Dispatcher          │ │
│  │ (background) │    │ (main thread)│    │                                 │ │
│  └─────────────┘    └──────────────┘    └────────────┬────────────────────┘ │
│                                                       │                      │
│  ┌───────────────────────────────────────────────────▼────────────────────┐ │
│  │                        Command Registry                                 │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │ │
│  │  │ queries/ │ │ sketch/  │ │features/ │ │timeline/ │ │ export/  │ ... │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘     │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                          │                                   │
│                                          ▼                                   │
│                              ┌───────────────────────┐                       │
│                              │   Fusion 360 API      │                       │
│                              └───────────────────────┘                       │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │ writes result
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           results.json                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
ClaudeBridge/
├── ClaudeBridge.py              # Entry point (add-in lifecycle)
├── config.py                    # File paths, event IDs
├── utils.py                     # JSON read/write utilities
├── CLAUDE.md                    # Quick reference for Claude
│
├── core/                        # Threading & event infrastructure
│   ├── __init__.py
│   ├── polling.py               # Background polling thread
│   └── event_handler.py         # Main thread event handler
│
├── commands/                    # Command implementation (modular)
│   ├── __init__.py              # Command registry
│   ├── dispatcher.py            # Central routing
│   ├── context.py               # Fusion 360 API abstraction
│   │
│   ├── helpers/                 # Shared utilities package
│   │   ├── __init__.py          # Re-exports all helpers
│   │   ├── command_utils.py     # Decorators (@with_sketch, @with_error_handling)
│   │   ├── sketch_curves.py     # Curve accessors (get_line, get_circle, etc.)
│   │   ├── validation.py        # Parameter validation
│   │   └── geometry/            # Geometry helpers package
│   │       ├── __init__.py      # Re-exports all geometry helpers
│   │       ├── components.py    # collect_all_components
│   │       ├── sketches.py      # get_sketch_by_index, get_sketch_by_global_index
│   │       ├── bodies.py        # get_body_by_index
│   │       ├── edges.py         # collect_edges
│   │       ├── faces.py         # find_top_face
│   │       └── planes.py        # get_construction_axis, get_construction_plane
│   │
│   ├── basic.py                 # ping, message
│   ├── parameters.py            # set_parameter
│   │
│   ├── queries/                 # [DEPRECATED] Use export_session instead
│   │   ├── design.py            # get_info, get_full_design
│   │   ├── bodies.py            # get_bodies_detailed
│   │   ├── sketches.py          # get_sketches_detailed, get_sketch_geometry
│   │   └── features.py          # get_features, get_parameters
│   │
│   ├── sketch/                  # Sketch operations
│   │   ├── __init__.py          # Merges all sketch commands
│   │   ├── create.py            # create_sketch, create_sketch_on_face
│   │   ├── primitives.py        # circle, rectangle, line, polygon
│   │   ├── curves.py            # arc, ellipse, spline
│   │   ├── operations.py        # [future] project, offset, mirror
│   │   ├── dimensions.py        # [future] parametric dimensions
│   │   └── constraints/         # Geometric constraints package
│   │       ├── __init__.py      # Merges constraint commands
│   │       ├── point.py         # midpoint, coincident constraints
│   │       ├── line.py          # vertical, horizontal constraints
│   │       └── query.py         # get_sketch_constraints, delete_constraint
│   │
│   ├── features/                # 3D feature creation
│   │   ├── __init__.py          # Merges feature commands
│   │   ├── basic.py             # extrude, revolve, list_profiles
│   │   ├── modify.py            # fillet, chamfer, shell
│   │   ├── advanced.py          # loft, loft_rails
│   │   ├── patterns.py          # [future] rectangular, circular
│   │   └── body_ops.py          # [future] combine, split, move
│   │
│   ├── construction/            # Construction geometry
│   │   ├── __init__.py          # Merges construction commands
│   │   ├── planes.py            # create_offset_plane, create_plane_at_angle
│   │   ├── axes.py              # [future] construction axes
│   │   └── points.py            # [future] construction points
│   │
│   ├── timeline/                # [future] History operations
│   │   └── operations.py        # delete, suppress, rollback
│   │
│   ├── assembly/                # [future] Assembly features
│   │   ├── components.py        # create, ground components
│   │   └── joints.py            # assembly joints
│   │
│   └── export/                  # Export operations
│       ├── __init__.py          # Merges export commands
│       ├── formats.py           # [future] STL, STEP, F3D, IGES
│       ├── file_ops.py          # [future] save, save_as
│       └── session/             # Session export package
│           ├── __init__.py      # export_session command
│           ├── utils.py         # write_json, pt helpers
│           └── collectors/      # Individual data collectors
│               ├── __init__.py  # Re-exports collectors
│               ├── design.py    # export_design_info
│               ├── bodies.py    # export_bodies
│               ├── sketches.py  # export_sketches
│               ├── features.py  # export_features
│               ├── parameters.py # export_parameters
│               └── construction.py # export_construction_planes
│
└── docs/                        # Documentation
    ├── architecture.md          # This file
    └── missing-features.md      # Feature roadmap
```

## Key Design Principles

### 1. Modular Command Organization

Commands are organized into **domain-specific packages** rather than monolithic files:

| Package | Purpose | Target Size |
|---------|---------|-------------|
| `queries/` | Design information retrieval | ~100 lines/file |
| `sketch/` | 2D sketch operations | ~100 lines/file |
| `features/` | 3D feature creation | ~100 lines/file |
| `construction/` | Construction geometry | ~50 lines/file |
| `timeline/` | History manipulation | ~100 lines/file |
| `assembly/` | Component & joints | ~100 lines/file |
| `export/` | File export operations | ~50 lines/file |

**Goal**: Keep individual files under **200 lines** for maintainability.

### 2. Centralized Command Registry

All commands are automatically merged into a single registry:

```python
# In commands/__init__.py
COMMAND_REGISTRY = {}
COMMAND_REGISTRY.update(BASIC_COMMANDS)
COMMAND_REGISTRY.update(QUERY_COMMANDS)
COMMAND_REGISTRY.update(SKETCH_COMMANDS)
# ... etc
```

To add a new command:
1. Create handler in appropriate sub-module
2. Add to that module's `COMMANDS` dict
3. Registry auto-merges on import

### 3. Shared Helpers

Common patterns are extracted to `helpers/` with a clean package structure:

```python
# helpers/geometry/ - Geometry-related helpers
from ..helpers import (
    collect_all_components,         # Traverse component hierarchy
    get_body_by_index,              # Safe body lookup
    get_sketch_by_index,            # Safe sketch lookup
    get_sketch_by_global_index,     # Global sketch lookup across components
    collect_edges,                  # Edge collection for fillets
    find_top_face,                  # Find topmost face
    get_construction_axis,          # Get X/Y/Z axis
    get_construction_plane,         # Get XY/XZ/YZ plane
)

# helpers/sketch_curves.py - Sketch curve accessors
from ..helpers import (
    get_line,                       # Safe line lookup
    get_circle,                     # Safe circle lookup
    get_arc,                        # Safe arc lookup
    get_line_endpoint,              # Get start/end point of line
    get_circle_center,              # Get center of circle
    get_constraint,                 # Safe constraint lookup
)

# helpers/command_utils.py - Decorators for reducing boilerplate
from ..helpers import with_sketch, with_error_handling

@with_sketch                        # Auto-retrieves sketch, handles errors
@with_error_handling("add fillet")  # Wraps in try/except
def my_command(command_id, params, ctx, sketch=None, comp=None):
    ...

# helpers/validation.py - Parameter validation
from ..helpers import get_operation_type  # "new"/"join"/"cut" → enum
```

### 4. Command Context Abstraction

`CommandContext` provides a clean interface to Fusion 360 objects:

```python
class CommandContext:
    @property design    # Active design (auto-refreshed)
    @property root      # Root component
    @property sketches  # Sketches collection
    @property extrudes  # Extrude features
    def require_design() # Validate design exists
```

### 5. Threading Model

Fusion 360 requires API calls on the main thread:

```
Background Thread              Main Thread
┌─────────────┐               ┌─────────────────────┐
│PollingThread│──fireEvent───▶│ThreadEventHandler   │
│ (1s loop)   │               │ ↓                   │
└─────────────┘               │ execute_command()   │
                              │ ↓                   │
                              │ Fusion 360 API      │
                              └─────────────────────┘
```

## Command Structure

### Request Format
```json
{
  "id": 42,
  "action": "extrude",
  "params": {
    "sketch_index": 0,
    "height": 5,
    "operation": "new"
  }
}
```

### Response Format
```json
{
  "id": 42,
  "success": true,
  "result": {"message": "Extruded 5cm"},
  "error": null
}
```

### Handler Signature
```python
def handler(command_id: int, params: dict, ctx: CommandContext) -> None:
    # Process command
    # ...
    write_result(command_id, success=True, result={...})
```

## Adding New Features

### Step 1: Choose the Right Module

| Feature Type | Module |
|-------------|--------|
| Query/inspection | `queries/` |
| 2D drawing | `sketch/` |
| 3D creation | `features/` |
| Modify existing | `features/modify.py` |
| Patterns/mirrors | `features/patterns.py` |
| Construction | `construction/` |
| Delete/edit | `timeline/` |
| Components | `assembly/` |
| Export | `export/` |

### Step 2: Create the Handler

```python
# features/advanced.py
from ...utils import write_result
from ..helpers import get_sketch_by_index, get_operation_type

def sweep(command_id, params, ctx):
    """Sweep a profile along a path."""
    # Implementation...
    write_result(command_id, True, {"message": "Sweep created"})

COMMANDS = {
    "sweep": sweep,
}
```

### Step 3: Update Module's `__init__.py` (if needed)

If creating a new file, ensure it's imported in the package's `__init__.py`:

```python
# features/__init__.py
from .advanced import COMMANDS as ADVANCED_COMMANDS
COMMANDS.update(ADVANCED_COMMANDS)
```

## File Size Guidelines

| Situation | Recommendation |
|-----------|----------------|
| File > 200 lines | Split into sub-modules |
| Related functions | Group in same file |
| Shared logic | Extract to `helpers/` |
| Single complex command | Own file is OK |

## Current Command Count

| Package | Commands | Status |
|---------|----------|--------|
| basic | 2 | Complete |
| parameters | 1 | Complete |
| queries | 8 | Deprecated (use export_session) |
| sketch/create | 2 | Complete |
| sketch/primitives | 4 | Complete |
| sketch/curves | 3 | Complete (arcs) |
| sketch/constraints | 7 | Partial (more planned) |
| features/basic | 3 | Complete |
| features/modify | 3 | Complete |
| features/advanced | 2 | Complete (loft) |
| construction | 2 | Partial |
| timeline | 0 | Placeholder |
| assembly | 0 | Placeholder |
| export/session | 1 | Complete |
| **Total** | **~38** | |

See `docs/missing-features.md` for the complete roadmap of planned commands.
