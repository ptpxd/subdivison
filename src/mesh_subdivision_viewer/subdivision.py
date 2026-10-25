from __future__ import annotations

from enum import Enum

from .mesh import HalfEdgeMesh


class SubdivisionScheme(str, Enum):
    LOOP = "loop"
    BUTTERFLY = "butterfly"


def subdivide_mesh(
    mesh: HalfEdgeMesh,
    scheme: SubdivisionScheme | str,
) -> HalfEdgeMesh:
    try:
        selected_scheme = SubdivisionScheme(scheme)
    except ValueError as exc:
        raise ValueError(f"Unsupported subdivision scheme: {scheme}") from exc

    results = []
    for component in mesh.components:
        component_mesh = _component_mesh(mesh, component)
        results.append(
            component_mesh.to_polydata().subdivide(
                1,
                subfilter=selected_scheme.value,
            )
        )

    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int]] = []
    for result in results:
        component_result = HalfEdgeMesh.from_polydata(result)
        offset = len(vertices)
        vertices.extend(component_result.vertices)
        faces.extend(
            (first + offset, second + offset, third + offset)
            for first, second, third in component_result.faces
        )

    return HalfEdgeMesh.build(vertices, faces, revision=mesh.revision + 1)


def _component_mesh(
    mesh: HalfEdgeMesh,
    face_indices: tuple[int, ...],
) -> HalfEdgeMesh:
    vertex_indices = sorted(
        {
            vertex
            for face_index in face_indices
            for vertex in mesh.faces[face_index]
        }
    )
    remap = {old: new for new, old in enumerate(vertex_indices)}
    vertices = [mesh.vertices[index] for index in vertex_indices]
    faces = [
        tuple(remap[index] for index in mesh.faces[face_index])
        for face_index in face_indices
    ]
    return HalfEdgeMesh.build(vertices, faces, revision=mesh.revision)
