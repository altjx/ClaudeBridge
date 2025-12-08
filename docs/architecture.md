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
├── ClaudeBridge.py          # Entry point (add-in lifecycle)
├── config.py                # File paths, event IDs
├── utils.py                 # JSON read/write utilities
├── CLAUDE.md                # Quick reference for Claude
│
├── core/                    # Threading & event infrastructure
│   ├── __init__.py
│   ├── polling.py           # Background polling thread
│   └── event_handler.py     # Main thread event handler
│
├── commands/                # Command implementation (modular)
│   ├── __init__.py          # Command registry
│   ├── dispatcher.py        # Central routing
│   ├── context.py           # Fusion 360 API abstraction
│   │
│   ├── helpers/             # Shared utilities
│   │   ├── geometry.py      # Body/face/edge selection
│   │   └── validation.py    # Parameter validation
│   │
│   ├── basic.py             # ping, message
│   ├── parameters.py        # set_parameter
│   │
│   ├── queries/             # Design information retrieval
│   │   ├── design.py        # get_info, get_full_design
│   │   ├── bodies.py        # get_bodies_detailed
│   │   ├── sketches.py      # get_sketches_detailed, get_sketch_geometry
│   │   └── features.py      # get_features, get_parameters
│   │
│   ├── sketch/              # Sketch operations
│   │   ├── create.py        # create_sketch
│   │   ├── primitives.py    # circle, rectangle, line
│   │   ├── curves.py        # [future] arc, ellipse, spline
│   │   ├── operations.py    # [future] project, offset, mirror
│   │   ├── constraints.py   # [future] geometric constraints
│   │   └── dimensions.py    # [future] parametric dimensions
│   │
│   ├── features/            # 3D feature creation
│   │   ├── basic.py         # extrude, revolve, list_profiles
│   │   ├── modify.py        # fillet, chamfer, shell
│   │   ├── advanced.py      # [future] sweep, loft, hole
│   │   ├── patterns.py      # [future] rectangular, circular
│   │   └── body_ops.py      # [future] combine, split, move
│   │
│   ├── construction/        # [future] Construction geometry
│   │   ├── planes.py        # offset, angle, 3-point planes
│   │   ├── axes.py          # construction axes
│   │   └── points.py        # construction points
│   │
│   ├── timeline/            # [future] History operations
│   │   └── operations.py    # delete, suppress, rollback
│   │
│   ├── assembly/            # [future] Assembly features
│   │   ├── components.py    # create, ground components
│   │   └── joints.py        # assembly joints
│   │
│   └── export/              # [future] Export operations
│       ├── formats.py       # STL, STEP, F3D, IGES
│       └── file_ops.py      # save, save_as
│
└── docs/                    # Documentation
    ├── architecture.md      # This file
    └── missing-features.md  # Feature roadmap
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

Common patterns are extracted to `helpers/`:

```python
# helpers/geometry.py
get_body_by_index(root, index)      # Safe body lookup
get_sketch_by_index(sketches, idx)  # Safe sketch lookup
collect_edges(body, indices)        # Edge collection for fillets
find_top_face(body)                 # Find topmost face
get_construction_axis(root, name)   # Get X/Y/Z axis
get_construction_plane(root, name)  # Get XY/XZ/YZ plane

# helpers/validation.py
get_operation_type(name)            # "new"/"join"/"cut" → enum
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
| queries | 8 | Complete |
| sketch | 4 | Partial (6+ planned) |
| features | 6 | Partial (15+ planned) |
| construction | 0 | Placeholder |
| timeline | 0 | Placeholder |
| assembly | 0 | Placeholder |
| export | 0 | Placeholder |
| **Total** | **21** | |

See `docs/missing-features.md` for the complete roadmap of planned commands.
