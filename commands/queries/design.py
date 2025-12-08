"""
Design-level query commands.
"""

from ...utils import write_result


def _collect_all_components(root):
    """Recursively collect all components in the design hierarchy."""
    components = [root]

    def traverse_occurrences(occurrences):
        for i in range(occurrences.count):
            occ = occurrences.item(i)
            comp = occ.component
            components.append(comp)
            # Recursively traverse nested occurrences
            if comp.occurrences.count > 0:
                traverse_occurrences(comp.occurrences)

    traverse_occurrences(root.occurrences)
    return components


def get_info(command_id, params, ctx):
    """Get basic design information.

    Traverses all components in the design hierarchy.
    """
    root = ctx.root
    design = ctx.design

    # Collect all components recursively
    all_components = _collect_all_components(root)

    bodies = []
    global_index = 0
    for comp in all_components:
        for i in range(comp.bRepBodies.count):
            b = comp.bRepBodies.item(i)
            bodies.append({
                "name": b.name,
                "index": global_index,
                "faces": b.faces.count,
                "component": comp.name
            })
            global_index += 1

    # Count sketches across all components
    total_sketches = sum(comp.sketches.count for comp in all_components)

    write_result(command_id, True, {
        "name": design.rootComponent.name,
        "bodies": bodies,
        "sketch_count": total_sketches,
        "component_count": len(all_components)
    })


def get_full_design(command_id, params, ctx):
    """Get complete design snapshot with bodies, sketches, features, and parameters.

    Traverses all components in the design hierarchy.
    """
    root = ctx.root
    design = ctx.design

    # Collect all components recursively
    all_components = _collect_all_components(root)

    # Bodies summary (across all components)
    bodies = []
    global_body_index = 0
    for comp in all_components:
        for i in range(comp.bRepBodies.count):
            body = comp.bRepBodies.item(i)
            bbox = body.boundingBox
            bodies.append({
                "name": body.name,
                "index": global_body_index,
                "component": comp.name,
                "volume_cm3": round(body.volume, 4) if body.volume else None,
                "face_count": body.faces.count,
                "size": [
                    round(bbox.maxPoint.x - bbox.minPoint.x, 4),
                    round(bbox.maxPoint.y - bbox.minPoint.y, 4),
                    round(bbox.maxPoint.z - bbox.minPoint.z, 4)
                ]
            })
            global_body_index += 1

    # Sketches summary (across all components)
    sketch_list = []
    global_sketch_index = 0
    for comp in all_components:
        for i in range(comp.sketches.count):
            sketch = comp.sketches.item(i)
            sketch_list.append({
                "name": sketch.name,
                "index": global_sketch_index,
                "component": comp.name,
                "profiles": sketch.profiles.count,
                "curves": sketch.sketchCurves.count
            })
            global_sketch_index += 1

    # Features summary (across all components)
    features = []
    global_feature_index = 0
    for comp in all_components:
        for i in range(comp.features.count):
            feat = comp.features.item(i)
            features.append({
                "name": feat.name,
                "index": global_feature_index,
                "component": comp.name,
                "type": feat.objectType.split("::")[-1].replace("Feature", "")
            })
            global_feature_index += 1

    # Components summary
    components = []
    for comp in all_components:
        components.append({
            "name": comp.name,
            "bodies": comp.bRepBodies.count,
            "sketches": comp.sketches.count,
            "features": comp.features.count
        })

    # Parameters (design-level)
    params_list = []
    for i in range(design.userParameters.count):
        param = design.userParameters.item(i)
        params_list.append({
            "name": param.name,
            "value": f"{param.expression} ({param.value} {param.unit})"
        })

    write_result(command_id, True, {
        "name": design.rootComponent.name,
        "components": components,
        "bodies": bodies,
        "sketches": sketch_list,
        "features": features,
        "parameters": params_list,
        "summary": {
            "component_count": len(all_components),
            "body_count": len(bodies),
            "sketch_count": len(sketch_list),
            "feature_count": len(features),
            "parameter_count": len(params_list)
        }
    })


COMMANDS = {
    "get_info": get_info,
    "get_full_design": get_full_design,
}
