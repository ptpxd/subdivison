import math

import pytest

from mesh_subdivision_viewer.mesh import HalfEdgeMesh, MeshValidationError


def test_builds_face_loops_and_shared_edge_twins():
    mesh = HalfEdgeMesh.build(
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
        [(0, 1, 2), (0, 2, 3)],
    )

    assert len(mesh.half_edges) == 6
    assert all(edge.next // 3 == edge.face for edge in mesh.half_edges)
    assert mesh.half_edges[2].twin == 3
    assert mesh.half_edges[3].twin == 2
    assert mesh.components == ((0, 1),)
    assert tuple(face.half_edge for face in mesh.face_records) == (0, 3)


def test_preserves_boundary_edges_without_twins():
    mesh = HalfEdgeMesh.build(
        [(0, 0, 0), (1, 0, 0), (0, 1, 0)],
        [(0, 1, 2)],
    )

    assert all(edge.twin is None for edge in mesh.half_edges)


def test_finds_disconnected_components():
    mesh = HalfEdgeMesh.build(
        [
            (0, 0, 0), (1, 0, 0), (0, 1, 0),
            (3, 0, 0), (4, 0, 0), (3, 1, 0),
        ],
        [(0, 1, 2), (3, 4, 5)],
    )

    assert mesh.components == ((0,), (1,))


@pytest.mark.parametrize(
    ("vertices", "faces", "message"),
    [
        ([(0, 0, 0)], [], "vertices and faces"),
        ([(0, 0)], [(0, 0, 0)], "three coordinates"),
        ([(math.nan, 0, 0), (1, 0, 0), (0, 1, 0)], [(0, 1, 2)], "finite"),
        ([(0, 0, 0), (1, 0, 0), (0, 1, 0)], [(0, 1)], "exactly three"),
        ([(0, 0, 0), (1, 0, 0), (0, 1, 0)], [(0, 1, 3)], "outside"),
        ([(0, 0, 0), (1, 0, 0), (0, 1, 0)], [(0, 1, 1)], "same vertex"),
    ],
)
def test_rejects_invalid_meshes(vertices, faces, message):
    with pytest.raises(MeshValidationError, match=message):
        HalfEdgeMesh.build(vertices, faces)


def test_rejects_duplicate_directed_edge():
    with pytest.raises(MeshValidationError, match="duplicate directed edge"):
        HalfEdgeMesh.build(
            [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)],
            [(0, 1, 2), (0, 1, 3)],
        )


def test_rejects_non_manifold_edge():
    with pytest.raises(MeshValidationError, match="more than two"):
        HalfEdgeMesh.build(
            [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1)],
            [(0, 1, 2), (1, 0, 3), (0, 1, 4)],
        )


def test_rejects_inconsistent_shared_edge_winding():
    with pytest.raises(
        MeshValidationError,
        match="duplicate directed edge|inconsistent face winding",
    ):
        HalfEdgeMesh.build(
            [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
            [(0, 1, 2), (0, 3, 2)],
        )


def test_rejects_disconnected_face_fans_at_shared_vertex():
    with pytest.raises(MeshValidationError, match="faces at a vertex are disconnected"):
        HalfEdgeMesh.build(
            [
                (0, 0, 0), (-1, 0, 0), (0, 1, 0),
                (1, 0, 0), (0, -1, 0),
            ],
            [(0, 1, 2), (0, 3, 4)],
        )
