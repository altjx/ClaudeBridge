"""
Body-related query commands.
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


def _get_body_info(body, index, component_name=None):
    """Extract detailed information from a body."""
    bbox = body.boundingBox

    # Count face types
    face_types = {}
    for face in body.faces:
        ft = face.geometry.surfaceType
        type_names = {
            0: "Plane", 1: "Cylinder", 2: "Cone", 3: "Sphere",
            4: "Torus", 5: "EllipticalCylinder", 6: "EllipticalCone", 7: "NURBS"
        }
        type_name = type_names.get(ft, "Other")
        face_types[type_name] = face_types.get(type_name, 0) + 1

    info = {
        "name": body.name,
        "index": index,
        "is_solid": body.isSolid,
        "volume_cm3": round(body.volume, 4) if body.volume else None,
        "area_cm2": round(body.area, 4) if body.area else None,
        "face_count": body.faces.count,
        "edge_count": body.edges.count,
        "vertex_count": body.vertices.count,
        "face_types": face_types,
        "bounding_box": {
            "min": [round(bbox.minPoint.x, 4), round(bbox.minPoint.y, 4), round(bbox.minPoint.z, 4)],
            "max": [round(bbox.maxPoint.x, 4), round(bbox.maxPoint.y, 4), round(bbox.maxPoint.z, 4)],
            "size": [
                round(bbox.maxPoint.x - bbox.minPoint.x, 4),
                round(bbox.maxPoint.y - bbox.minPoint.y, 4),
                round(bbox.maxPoint.z - bbox.minPoint.z, 4)
            ]
        }
    }
    if component_name:
        info["component"] = component_name
    return info


def get_bodies_detailed(command_id, params, ctx):
    """Get comprehensive body information including geometry details.

    Traverses all components in the design hierarchy to find all bodies.
    """
    root = ctx.root

    # Collect all components recursively
    all_components = _collect_all_components(root)

    bodies = []
    global_index = 0

    for comp in all_components:
        for i in range(comp.bRepBodies.count):
            body = comp.bRepBodies.item(i)
            body_info = _get_body_info(body, global_index, comp.name)
            bodies.append(body_info)
            global_index += 1

    write_result(command_id, True, {"bodies": bodies, "count": len(bodies)})


COMMANDS = {
    "get_bodies_detailed": get_bodies_detailed,
}
