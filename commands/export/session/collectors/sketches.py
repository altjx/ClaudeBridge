"""
Sketch information collector for session export.
"""

import os
import math
from ..utils import write_json, pt


def export_sketches(root, all_components, session_dir):
    """
    Export sketch overview and individual sketch geometry files.

    Creates a sketches/ subdirectory with overview.json and individual
    sketch_N.json files containing detailed geometry information.

    Args:
        root: Root component
        all_components: List of all components in the design
        session_dir: Directory to write output files

    Returns:
        int: Number of sketches exported
    """
    sketches_dir = os.path.join(session_dir, "sketches")
    os.makedirs(sketches_dir, exist_ok=True)

    # Collect all sketches with global indexing
    all_sketches = []
    global_index = 0
    for comp in all_components:
        for i in range(comp.sketches.count):
            sketch = comp.sketches.item(i)
            all_sketches.append((sketch, global_index, comp))
            global_index += 1

    # Export overview
    overview = []
    for sketch, idx, comp in all_sketches:
        curves = sketch.sketchCurves
        overview.append({
            "name": sketch.name,
            "index": idx,
            "component": comp.name,
            "profile_count": sketch.profiles.count,
            "is_visible": sketch.isVisible,
            "curves": {
                "lines": curves.sketchLines.count,
                "circles": curves.sketchCircles.count,
                "arcs": curves.sketchArcs.count,
                "ellipses": curves.sketchEllipses.count,
                "splines": curves.sketchFittedSplines.count,
                "total": curves.count
            }
        })

    write_json(os.path.join(sketches_dir, "overview.json"), {
        "sketches": overview,
        "count": len(overview)
    })

    # Export individual sketch geometry
    for sketch, idx, comp in all_sketches:
        curves = sketch.sketchCurves

        # Extract circles
        circles = []
        for i in range(curves.sketchCircles.count):
            circle = curves.sketchCircles.item(i)
            circles.append({
                "index": i,
                "center": pt(circle.centerSketchPoint.geometry),
                "radius": round(circle.radius, 4),
                "diameter": round(circle.radius * 2, 4),
                "is_construction": circle.isConstruction
            })

        # Extract lines
        lines = []
        for i in range(curves.sketchLines.count):
            line = curves.sketchLines.item(i)
            lines.append({
                "index": i,
                "start": pt(line.startSketchPoint.geometry),
                "end": pt(line.endSketchPoint.geometry),
                "length": round(line.length, 4),
                "is_construction": line.isConstruction
            })

        # Extract arcs
        arcs = []
        for i in range(curves.sketchArcs.count):
            arc = curves.sketchArcs.item(i)
            arc_data = {
                "index": i,
                "center": pt(arc.centerSketchPoint.geometry),
                "radius": round(arc.radius, 4),
                "start_point": pt(arc.startSketchPoint.geometry),
                "end_point": pt(arc.endSketchPoint.geometry),
                "is_construction": arc.isConstruction
            }
            # Try to get angles from geometry object
            try:
                geom = arc.geometry
                arc_data["start_angle_deg"] = round(math.degrees(geom.startAngle), 2)
                arc_data["end_angle_deg"] = round(math.degrees(geom.endAngle), 2)
            except:
                pass
            arcs.append(arc_data)

        # Extract ellipses
        ellipses = []
        for i in range(curves.sketchEllipses.count):
            ellipse = curves.sketchEllipses.item(i)
            ellipses.append({
                "index": i,
                "center": pt(ellipse.centerSketchPoint.geometry),
                "major_radius": round(ellipse.majorRadius, 4),
                "minor_radius": round(ellipse.minorRadius, 4),
                "is_construction": ellipse.isConstruction
            })

        # Get sketch plane info
        plane_info = {}
        try:
            plane = sketch.referencePlane
            if plane:
                plane_info = {"name": plane.name if hasattr(plane, 'name') else "Custom"}
        except:
            plane_info = {"name": "Unknown"}

        sketch_data = {
            "sketch_name": sketch.name,
            "sketch_index": idx,
            "component": comp.name,
            "plane": plane_info,
            "circles": circles,
            "lines": lines,
            "arcs": arcs,
            "ellipses": ellipses,
            "counts": {
                "circles": len(circles),
                "lines": len(lines),
                "arcs": len(arcs),
                "ellipses": len(ellipses),
                "total": len(circles) + len(lines) + len(arcs) + len(ellipses)
            }
        }

        write_json(os.path.join(sketches_dir, f"sketch_{idx}.json"), sketch_data)

    return len(all_sketches)
