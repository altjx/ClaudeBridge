# Fusion 360 Bridge API Reference

Complete reference for all available commands.

## Connection Commands

### ping
Test the bridge connection.
```json
{"id": 1, "action": "ping", "params": {}}
```

### message
Display a message box in Fusion 360.
```json
{"id": 2, "action": "message", "params": {"text": "Hello!"}}
```

---

## Read Commands (Inspect Design)

### get_info
Basic design information.
```json
{"id": 3, "action": "get_info", "params": {}}
```

### get_full_design
**Complete design snapshot** - bodies, sketches, features, and parameters.
```json
{"id": 4, "action": "get_full_design", "params": {}}
```
**Response includes:**
- All bodies with names, volumes, sizes
- All sketches with profile/curve counts
- All features in timeline order
- All user parameters

### get_bodies_detailed
Comprehensive body information with geometry details.
```json
{"id": 5, "action": "get_bodies_detailed", "params": {}}
```
**Response includes per body:**
- `name`, `index`
- `is_solid`, `volume_cm3`, `area_cm2`
- `face_count`, `edge_count`, `vertex_count`
- `face_types`: {"Plane": 6, "Cylinder": 2, ...}
- `bounding_box`: {min, max, size}

### get_sketches_detailed
All sketches with curve information.
```json
{"id": 6, "action": "get_sketches_detailed", "params": {}}
```
**Response includes per sketch:**
- `name`, `index`, `profile_count`, `is_visible`
- `curves`: {lines, circles, arcs, ellipses, splines, total}

### get_features
Feature timeline history.
```json
{"id": 7, "action": "get_features", "params": {}}
```
**Response per feature:**
- `name`, `index`, `type` (Extrude, Fillet, Shell, etc.)
- `is_suppressed`, `is_valid`

### get_parameters
User-defined parameters only.
```json
{"id": 8, "action": "get_parameters", "params": {}}
```

### get_all_parameters
**All parameters** including model parameters (sketch dimensions, feature values).
```json
{"id": 9, "action": "get_all_parameters", "params": {}}
```
**Response includes:**
- `user_parameters`: Explicitly created parameters
- `model_parameters`: Auto-generated from sketches/features (d1, d2, Extrude1_Height, etc.)
  - `name`: Parameter name (e.g., "d1", "Revolve1_Angle")
  - `expression`: The expression/value as entered
  - `value`: Numeric value in internal units
  - `unit`: Unit type
  - `role`: Parameter role (if available)
  - `created_by`: Which sketch/feature created this parameter
- `counts`: Total counts of each type

### get_sketch_geometry
**Full geometry coordinates** for all curves in a sketch.
```json
{"id": 9, "action": "get_sketch_geometry", "params": {"sketch_index": 0}}
```
**Response includes:**
- `circles`: center [x,y,z], radius, diameter, is_construction
- `lines`: start [x,y,z], end [x,y,z], length, is_construction
- `arcs`: center, radius, start_point, end_point, start_angle_deg, end_angle_deg
- `ellipses`: center, major_radius, minor_radius

### list_profiles
List profiles in a sketch (for extrusion).
```json
{"id": 10, "action": "list_profiles", "params": {"sketch_index": 0}}
```

---

## Construction Geometry

### create_offset_plane
Create a construction plane offset from a base plane. Essential for creating geometry at different Z heights.
```json
{"id": 10, "action": "create_offset_plane", "params": {
  "plane": "xy",
  "offset": 5.0
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| plane | string | "xy" | Base plane (`"xy"`, `"xz"`, `"yz"`) |
| offset | float | 1.0 | Distance in cm (positive = along normal) |
| name | string | auto | Optional custom name |

**Returns:** `plane_index` for use with `create_sketch`

### create_plane_at_angle
Create a construction plane at an angle from a base plane.
```json
{"id": 11, "action": "create_plane_at_angle", "params": {
  "plane": "xy",
  "axis": "x",
  "angle": 45
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| plane | string | "xy" | Base plane |
| axis | string | "x" | Rotation axis (`"x"`, `"y"`, `"z"`) |
| angle | float | 45 | Angle in degrees |
| name | string | auto | Optional custom name |

### get_construction_planes
List all construction planes in the design.
```json
{"id": 12, "action": "get_construction_planes", "params": {}}
```

---

## Sketch Commands

### create_sketch
Create a new sketch on a construction plane or offset plane.
```json
{"id": 10, "action": "create_sketch", "params": {"plane": "xy"}}
```
**Or on an offset plane:**
```json
{"id": 11, "action": "create_sketch", "params": {"plane_index": 0}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| plane | string | "xy" | Base plane (`"xy"`, `"xz"`, `"yz"`) - used if plane_index not set |
| plane_index | int | null | Index of construction plane (from `create_offset_plane`) |

### create_sketch_on_face
Create a sketch on an existing body face. Useful for adding cuts or features to existing geometry.
```json
{"id": 12, "action": "create_sketch_on_face", "params": {
  "body_index": 0,
  "use_top_face": true
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| body_index | int | 0 | Which body |
| face_index | int | 0 | Which face (if use_top_face is false) |
| use_top_face | bool | false | Auto-find topmost planar face |

**Example workflow for cutting into top of a body:**
```json
// 1. Create sketch on top face
{"id": 1, "action": "create_sketch_on_face", "params": {"body_index": 0, "use_top_face": true}}
// 2. Draw shape to cut
{"id": 2, "action": "draw_circle", "params": {"x": 0, "y": 0, "radius": 1}}
// 3. Cut through body
{"id": 3, "action": "extrude", "params": {"height": -2, "operation": "cut"}}
```

### draw_circle
```json
{"id": 11, "action": "draw_circle", "params": {
  "sketch_index": 0, "x": 0, "y": 0, "radius": 2.5
}}
```

### draw_rectangle
```json
{"id": 12, "action": "draw_rectangle", "params": {
  "sketch_index": 0, "x": 0, "y": 0, "width": 4, "height": 3
}}
```

### draw_line
```json
{"id": 13, "action": "draw_line", "params": {
  "sketch_index": 0, "x1": 0, "y1": 0, "x2": 5, "y2": 3
}}
```

### draw_arc
Draw an arc defined by center, start point, and end point. Arc is drawn counter-clockwise from start to end.
```json
{"id": 14, "action": "draw_arc", "params": {
  "sketch_index": 0,
  "center_x": 0, "center_y": 0,
  "start_x": 2, "start_y": 0,
  "end_x": 0, "end_y": 2
}}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| sketch_index | int | last | Which sketch |
| center_x, center_y | float | 0, 0 | Center point |
| start_x, start_y | float | 1, 0 | Start point (defines radius) |
| end_x, end_y | float | 0, 1 | End point |

### draw_arc_three_points
Draw an arc passing through three points.
```json
{"id": 15, "action": "draw_arc_three_points", "params": {
  "sketch_index": 0,
  "start_x": 0, "start_y": 0,
  "mid_x": 1, "mid_y": 1,
  "end_x": 2, "end_y": 0
}}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| sketch_index | int | last | Which sketch |
| start_x, start_y | float | 0, 0 | Start point of arc |
| mid_x, mid_y | float | 0.5, 0.5 | Point along the arc (determines curvature) |
| end_x, end_y | float | 1, 0 | End point of arc |

### draw_arc_sweep
Draw an arc defined by center, start point, and sweep angle.
```json
{"id": 16, "action": "draw_arc_sweep", "params": {
  "sketch_index": 0,
  "center_x": 0, "center_y": 0,
  "start_x": 2, "start_y": 0,
  "sweep_angle": 90
}}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| sketch_index | int | last | Which sketch |
| center_x, center_y | float | 0, 0 | Center point |
| start_x, start_y | float | 1, 0 | Start point (defines radius) |
| sweep_angle | float | 90 | Sweep angle in degrees (positive = counter-clockwise) |

**Arc Examples:**
```json
// Quarter circle (90°) - use draw_arc_sweep
{"id": 1, "action": "draw_arc_sweep", "params": {
  "center_x": 0, "center_y": 0, "start_x": 3, "start_y": 0, "sweep_angle": 90
}}

// Semicircle (180°)
{"id": 2, "action": "draw_arc_sweep", "params": {
  "center_x": 0, "center_y": 0, "start_x": 3, "start_y": 0, "sweep_angle": 180
}}

// Arc connecting two points with specific curvature - use draw_arc_three_points
{"id": 3, "action": "draw_arc_three_points", "params": {
  "start_x": -2, "start_y": 0, "mid_x": 0, "mid_y": 1.5, "end_x": 2, "end_y": 0
}}
```

---

## 3D Operations

### extrude
Extrude a sketch profile.
```json
{"id": 14, "action": "extrude", "params": {
  "sketch_index": 0,
  "profile_index": 0,
  "height": 5,
  "operation": "new"
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| sketch_index | int | last | Sketch containing profile |
| profile_index | int | 0 | Which profile (use `list_profiles`) |
| height | float | 1 | Height in cm |
| operation | string | "new" | `"new"`, `"join"`, `"cut"` |

### revolve
Revolve a sketch profile around an axis to create rotational geometry.
```json
{"id": 15, "action": "revolve", "params": {
  "sketch_index": 0,
  "profile_index": 0,
  "axis": "x",
  "angle": 360,
  "operation": "new"
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| sketch_index | int | last | Sketch containing profile |
| profile_index | int | 0 | Which profile (use `list_profiles`) |
| axis | string | "x" | `"x"`, `"y"`, `"z"` for construction axes, or `"line"` for sketch line |
| axis_line_index | int | 0 | Index of sketch line to use as axis (when axis="line") |
| angle | float | 360 | Degrees to revolve (360 = full revolution) |
| operation | string | "new" | `"new"`, `"join"`, `"cut"` |

**Example: Create a sphere by revolving a semicircle**
```json
// 1. Create sketch on XZ plane
{"id": 1, "action": "create_sketch", "params": {"plane": "xz"}}
// 2. Draw a semicircle profile (half circle + line for axis)
// 3. Revolve around the line
{"id": 3, "action": "revolve", "params": {"axis": "line", "axis_line_index": 0}}
```

### fillet
Round edges of a body.
```json
{"id": 15, "action": "fillet", "params": {
  "body_index": 0,
  "radius": 0.2,
  "edge_indices": [0, 1, 2]
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| body_index | int | 0 | Which body |
| radius | float | 0.1 | Fillet radius (cm) |
| edge_indices | array | all | Specific edges (or omit for all) |

### chamfer
Bevel edges of a body.
```json
{"id": 16, "action": "chamfer", "params": {
  "body_index": 0,
  "distance": 0.1,
  "edge_indices": [0, 1]
}}
```

### shell
Hollow out a body.
```json
{"id": 17, "action": "shell", "params": {
  "body_index": 0,
  "thickness": 0.2,
  "remove_top": true
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| body_index | int | 0 | Which body |
| thickness | float | 0.1 | Wall thickness (cm) |
| face_index | int | null | Specific face to remove |
| remove_top | bool | true | Auto-find top face if face_index not set |

---

## Parameters

### set_parameter
Create or update a user parameter.
```json
{"id": 18, "action": "set_parameter", "params": {
  "name": "WallThickness",
  "value": 2,
  "unit": "mm"
}}
```

---

## Units

All dimensions are in **centimeters** (Fusion 360's internal unit):
- 1 cm = 10 mm
- For 50mm, use `5` (cm)
- For 2mm, use `0.2` (cm)

---

## Workflow: Modifying Existing Design

1. **Read current state:**
   ```json
   {"id": 1, "action": "get_full_design", "params": {}}
   ```

2. **Analyze the response** to understand:
   - What bodies exist and their sizes
   - What features have been applied
   - Available sketches

3. **Make modifications:**
   - Add fillet/chamfer to existing bodies
   - Create new sketch and cut holes
   - Shell to hollow out
   - Add new features

4. **Verify changes:**
   ```json
   {"id": 99, "action": "get_bodies_detailed", "params": {}}
   ```

---

## File Paths

| File | Purpose |
|------|---------|
| `~/Documents/scripts/fusion_360/ClaudeBridge/commands.json` | Write commands |
| `~/Documents/scripts/fusion_360/ClaudeBridge/results.json` | Read results |
