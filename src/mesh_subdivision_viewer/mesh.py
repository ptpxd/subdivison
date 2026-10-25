from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
import math
from pathlib import Path
from typing import Iterable, Sequence

Point = tuple[float, float, float]
Triangle = tuple[int, int, int]


class MeshValidationError(ValueError):
    """Raised when mesh geometry or connectivity is invalid."""


class MeshLoadError(ValueError):
    """Raised when an input file cannot be converted to a supported mesh."""


@dataclass(frozen=True, slots=True)
class HalfEdge:
    origin: int
    face: int
    next: int
    twin: int | None


@dataclass(frozen=True, slots=True)
class Face:
    half_edge: int


@dataclass(frozen=True, slots=True)
class HalfEdgeMesh:
    vertices: tuple[Point, ...]
    faces: tuple[Triangle, ...]
    face_records: tuple[Face, ...]
    half_edges: tuple[HalfEdge, ...]
    components: tuple[tuple[int, ...], ...]
    revision: int = 0

    @classmethod
    def build(
        cls,
        vertices: Iterable[Sequence[float]],
        faces: Iterable[Sequence[int]],
        *,
        revision: int = 0,
    ) -> HalfEdgeMesh:
        if revision < 0:
            raise MeshValidationError("Mesh revision cannot be negative.")
        points = tuple(_validate_point(point) for point in vertices)
        triangles = tuple(_validate_triangle(face, len(points)) for face in faces)
        if not points or not triangles:
            raise MeshValidationError("Mesh must contain vertices and faces.")

        edge_faces: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
        directed_edges: set[tuple[int, int]] = set()
        has_duplicate_directed_edge = False
        for face_index, triangle in enumerate(triangles):
            for index, origin in enumerate(triangle):
                destination = triangle[(index + 1) % 3]
                directed = (origin, destination)
                if directed in directed_edges:
                    has_duplicate_directed_edge = True
                directed_edges.add(directed)
                edge_faces[tuple(sorted(directed))].append((face_index, index))

        if any(len(incident) > 2 for incident in edge_faces.values()):
            raise MeshValidationError(
                "Mesh is non-manifold: an edge has more than two incident faces."
            )
        if has_duplicate_directed_edge:
            raise MeshValidationError(
                "Mesh contains a duplicate directed edge; face winding must be consistent."
            )

        face_neighbors: list[set[int]] = [set() for _ in triangles]
        for incident in edge_faces.values():
            if len(incident) == 2:
                first_face, first_index = incident[0]
                second_face, second_index = incident[1]
                first = triangles[first_face]
                second = triangles[second_face]
                if (
                    first[first_index] != second[(second_index + 1) % 3]
                    or first[(first_index + 1) % 3] != second[second_index]
                ):
                    raise MeshValidationError(
                        "Mesh has inconsistent face winding along a shared edge."
                    )
                face_neighbors[first_face].add(second_face)
                face_neighbors[second_face].add(first_face)

        _validate_vertex_manifoldness(triangles, edge_faces, len(points))

        edge_indices: dict[tuple[int, int], int] = {}
        for face_index in range(len(triangles)):
            for local_index in range(3):
                edge_indices[(face_index, local_index)] = face_index * 3 + local_index

        half_edges: list[HalfEdge] = []
        for face_index, triangle in enumerate(triangles):
            for local_index, origin in enumerate(triangle):
                destination = triangle[(local_index + 1) % 3]
                incident = edge_faces[tuple(sorted((origin, destination)))]
                twin: int | None = None
                if len(incident) == 2:
                    twin_face, twin_local_index = next(
                        edge for edge in incident if edge[0] != face_index
                    )
                    twin = edge_indices[(twin_face, twin_local_index)]
                half_edges.append(
                    HalfEdge(
                        origin=origin,
                        face=face_index,
                        next=face_index * 3 + (local_index + 1) % 3,
                        twin=twin,
                    )
                )

        components = _connected_components(face_neighbors)
        face_records = tuple(Face(half_edge=index * 3) for index in range(len(triangles)))
        return cls(points, triangles, face_records, tuple(half_edges), components, revision)

    @classmethod
    def from_polydata(cls, polydata: object) -> HalfEdgeMesh:
        points = getattr(polydata, "points", None)
        cells = getattr(polydata, "faces", None)
        if points is None or cells is None:
            raise MeshValidationError("Input does not contain polygonal mesh data.")
        raw_cells = tuple(int(value) for value in cells)
        triangles: list[Triangle] = []
        offset = 0
        while offset < len(raw_cells):
            count = raw_cells[offset]
            offset += 1
            cell = raw_cells[offset : offset + count]
            if len(cell) != count:
                raise MeshValidationError("Mesh contains an incomplete face.")
            if count != 3:
                raise MeshValidationError("Mesh must be triangulated before conversion.")
            triangles.append((cell[0], cell[1], cell[2]))
            offset += count
        return cls.build(points, triangles)

    def to_polydata(self) -> object:
        try:
            import pyvista as pv
        except ImportError as exc:
            raise RuntimeError("PyVista is required to display or subdivide meshes.") from exc

        face_cells = [value for face in self.faces for value in (3, *face)]
        points = [list(vertex) for vertex in self.vertices]
        return pv.PolyData(points, face_cells)


def load_mesh(path: str | Path) -> HalfEdgeMesh:
    file_path = Path(path)
    if file_path.suffix.lower() not in {".stl", ".obj"}:
        raise MeshLoadError("Only STL and OBJ files are supported.")
    if not file_path.is_file():
        raise MeshLoadError(f"File does not exist or cannot be read: {file_path}")

    try:
        import pyvista as pv

        data = pv.read(file_path)
        if not isinstance(data, pv.PolyData):
            raise MeshLoadError("The selected file does not contain a single polygon mesh.")
        triangulated = data.triangulate()
        if triangulated.n_cells != triangulated.n_faces:
            raise MeshLoadError("The selected file contains unsupported non-surface cells.")
        return HalfEdgeMesh.from_polydata(triangulated)
    except MeshLoadError:
        raise
    except (OSError, ValueError, RuntimeError, ImportError) as exc:
        raise MeshLoadError(f"Could not load mesh '{file_path}': {exc}") from exc


def _validate_point(point: Sequence[float]) -> Point:
    if len(point) != 3:
        raise MeshValidationError("Each vertex must have exactly three coordinates.")
    try:
        coordinates = tuple(float(value) for value in point)
    except (TypeError, ValueError) as exc:
        raise MeshValidationError("Vertex coordinates must be numeric.") from exc
    if not all(math.isfinite(value) for value in coordinates):
        raise MeshValidationError("Vertex coordinates must be finite.")
    return (coordinates[0], coordinates[1], coordinates[2])


def _validate_triangle(face: Sequence[int], vertex_count: int) -> Triangle:
    if len(face) != 3:
        raise MeshValidationError("Each face must reference exactly three vertices.")
    if any(type(index) is not int for index in face):
        raise MeshValidationError("Face indices must be integers.")
    triangle = (face[0], face[1], face[2])
    if len(set(triangle)) != 3:
        raise MeshValidationError("A face cannot reference the same vertex more than once.")
    if any(index < 0 or index >= vertex_count for index in triangle):
        raise MeshValidationError("Face references a vertex index outside the mesh.")
    return triangle


def _connected_components(neighbors: list[set[int]]) -> tuple[tuple[int, ...], ...]:
    unseen = set(range(len(neighbors)))
    components: list[tuple[int, ...]] = []
    while unseen:
        start = unseen.pop()
        component = [start]
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbor in neighbors[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.append(neighbor)
                    queue.append(neighbor)
        components.append(tuple(sorted(component)))
    return tuple(components)


def _validate_vertex_manifoldness(
    triangles: tuple[Triangle, ...],
    edge_faces: dict[tuple[int, int], list[tuple[int, int]]],
    vertex_count: int,
) -> None:
    incident_faces_by_vertex: list[set[int]] = [
        set() for _ in range(vertex_count)
    ]
    incident_edges_by_vertex: list[
        list[tuple[tuple[int, int], list[tuple[int, int]]]]
    ] = [[] for _ in range(vertex_count)]
    for face_index, triangle in enumerate(triangles):
        for vertex in triangle:
            incident_faces_by_vertex[vertex].add(face_index)
    for edge, incident in edge_faces.items():
        for vertex in edge:
            incident_edges_by_vertex[vertex].append((edge, incident))

    for vertex in range(vertex_count):
        incident_faces = incident_faces_by_vertex[vertex]
        if not incident_faces:
            continue

        neighbors = {face_index: set() for face_index in incident_faces}
        boundary_edges = 0
        for _, incident in incident_edges_by_vertex[vertex]:
            if len(incident) == 1:
                boundary_edges += 1
            elif len(incident) == 2:
                first, second = incident[0][0], incident[1][0]
                neighbors[first].add(second)
                neighbors[second].add(first)

        if len(_connected_components_from_neighbors(neighbors)) != 1:
            raise MeshValidationError(
                "Mesh is non-manifold: incident faces at a vertex are disconnected."
            )
        if boundary_edges not in (0, 2):
            raise MeshValidationError(
                "Mesh is non-manifold: a vertex has an invalid number of boundary edges."
            )


def _connected_components_from_neighbors(
    neighbors: dict[int, set[int]],
) -> tuple[tuple[int, ...], ...]:
    unseen = set(neighbors)
    components: list[tuple[int, ...]] = []
    while unseen:
        start = unseen.pop()
        component = [start]
        queue = deque([start])
        while queue:
            for neighbor in neighbors[queue.popleft()]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.append(neighbor)
                    queue.append(neighbor)
        components.append(tuple(component))
    return tuple(components)
