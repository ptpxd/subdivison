from pathlib import Path

import pytest

from mesh_subdivision_viewer.mesh import MeshLoadError, load_mesh

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    "filename",
    [
        "tetrahedron_ascii.stl",
        "tetrahedron_binary.stl",
        "triangle_mesh.obj",
        "polygon_mesh.obj",
    ],
)
def test_loads_stl_and_obj_meshes(filename):
    mesh = load_mesh(FIXTURES / filename)

    assert mesh.vertices
    assert mesh.faces
    assert all(len(face) == 3 for face in mesh.faces)


def test_triangulates_obj_polygon():
    mesh = load_mesh(FIXTURES / "polygon_mesh.obj")

    assert len(mesh.faces) == 2


@pytest.mark.parametrize(
    ("filename", "content", "suffix", "message"),
    [
        ("empty.obj", "", ".obj", "Could not load"),
        ("malformed.obj", "not a mesh", ".obj", "Could not load"),
        ("invalid.txt", "mesh", ".txt", "Only STL and OBJ"),
        ("nonmanifold.obj", "v 0 0 0\nv 1 0 0\nv 0 1 0\nv 0 -1 0\nv 0 0 1\n"
         "f 1 2 3\nf 2 1 4\nf 1 2 5\n", ".obj", "non-manifold"),
    ],
)
def test_reports_invalid_input(tmp_path, filename, content, suffix, message):
    path = tmp_path / filename
    path.write_text(content, encoding="utf-8")

    with pytest.raises(MeshLoadError, match=message):
        load_mesh(path)


def test_reports_unreadable_path(tmp_path):
    path = tmp_path / "missing.obj"

    with pytest.raises(MeshLoadError, match="does not exist"):
        load_mesh(path)
