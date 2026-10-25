import pytest

from mesh_subdivision_viewer.mesh import HalfEdgeMesh
from mesh_subdivision_viewer.subdivision import SubdivisionScheme, subdivide_mesh


@pytest.fixture
def tetrahedron():
    return HalfEdgeMesh.build(
        [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)],
        [(0, 2, 1), (0, 1, 3), (0, 3, 2), (1, 2, 3)],
    )


@pytest.mark.parametrize(
    "scheme",
    [SubdivisionScheme.LOOP, SubdivisionScheme.BUTTERFLY],
)
def test_applies_one_subdivision_iteration(tetrahedron, scheme):
    result = subdivide_mesh(tetrahedron, scheme)

    assert len(result.faces) == len(tetrahedron.faces) * 4
    assert result.revision == tetrahedron.revision + 1
    assert result.components
    assert all(edge.next // 3 == edge.face for edge in result.half_edges)


def test_repeated_iteration_uses_previous_result(tetrahedron):
    once = subdivide_mesh(tetrahedron, SubdivisionScheme.LOOP)
    twice = subdivide_mesh(once, SubdivisionScheme.LOOP)

    assert len(once.faces) == 16
    assert len(twice.faces) == 64
    assert twice.revision == 2


def test_subdivides_disconnected_components_independently():
    vertices = [
        (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (3, 0, 0), (4, 0, 0), (3, 1, 0), (3, 0, 1),
    ]
    faces = [
        (0, 2, 1), (0, 1, 3), (0, 3, 2), (1, 2, 3),
        (4, 6, 5), (4, 5, 7), (4, 7, 6), (5, 6, 7),
    ]
    mesh = HalfEdgeMesh.build(vertices, faces)

    result = subdivide_mesh(mesh, SubdivisionScheme.BUTTERFLY)

    assert len(result.components) == 2
    assert len(result.faces) == 32


def test_rejects_unknown_scheme_without_mutating_mesh(tetrahedron):
    with pytest.raises(ValueError, match="Unsupported subdivision scheme"):
        subdivide_mesh(tetrahedron, "invalid")

    assert len(tetrahedron.faces) == 4
    assert tetrahedron.revision == 0
