# Research: Mesh Subdivision Viewer

## Python mesh I/O, rendering, and subdivision

- **Decision**: Use PyVista and its VTK-backed `PolyData` operations for STL/OBJ
  loading, rendering, triangulation, and Loop/Butterfly subdivision.
- **Rationale**: PyVista exposes both subdivision schemes in Python. VTK
  provides readers for STL and Wavefront OBJ. OBJ polygons can be triangulated
  before processing. This avoids writing and maintaining two subdivision
  algorithms.
- **Alternatives considered**: Implement subdivision directly; rejected as
  more code and algorithmic risk than the feature requires. OpenSubdiv; rejected
  because its documented schemes include Loop but not Butterfly and the
  project does not provide a straightforward first-party Python binding.
- **Sources**:
  - [PyVista subdivision API](https://docs.pyvista.org/api/core/_autosummary/pyvista.polydatafilters.subdivide.html)
  - [PyVista read API](https://docs.pyvista.org/api/readers/_autosummary/pyvista.read.html)
  - [PyVista triangulate API](https://docs.pyvista.org/api/core/_autosummary/pyvista.polydatafilters.triangulate.html)
  - [VTK STL reader](https://vtk.org/doc/nightly/html/classvtkSTLReader.html)
  - [VTK OBJ reader](https://vtk.org/doc/nightly/html/classvtkOBJReader.html)
  - [OpenSubdiv scheme definitions](https://raw.githubusercontent.com/PixarAnimationStudios/OpenSubdiv/release/opensubdiv/sdc/types.h)
  - [OpenSubdiv introduction](https://opensubdiv.org/docs/intro.html)

## Edge-based mesh representation

- **Decision**: Maintain an explicit half-edge mesh representation for each
  loaded and subdivided surface. Convert to PyVista/VTK data only at the
  import, subdivision, and rendering boundaries, rebuilding and validating
  half-edge connectivity after each subdivision.
- **Rationale**: The user explicitly requires an edge-based structure and the
  half-edge representation is the simpler requested option. Keeping conversion
  at clear boundaries avoids reimplementing VTK subdivision algorithms while
  still making the application's mesh connectivity explicit and checkable.
- **Alternatives considered**: Rely only on VTK `PolyData`; rejected because it
  does not fulfill the explicit half-edge requirement. Implement the
  subdivision algorithms on the half-edge structure; rejected to avoid
  unnecessary custom algorithm complexity.

## Desktop UI and interaction

- **Decision**: Use PyVistaQt's `QtInteractor` in a small PySide6 desktop window.
- **Rationale**: The interactor embeds the PyVista rendering view in a Qt
  application; Qt provides the required menu and keyboard actions without
  introducing a separate rendering/UI stack.
- **Sources**:
  - [PyVista Qt plotting](https://docs.pyvista.org/api/plotting/qt_plotting.html)
  - [PyVistaQt usage](https://qt.pyvista.org/usage.html)
  - [Qt for Python getting started](https://doc.qt.io/qtforpython-6/gettingstarted.html)

## Mesh connectivity and input constraints

- **Decision**: Triangulate polygonal faces at load. Validate manifold
  connectivity in the half-edge model. Process disconnected components
  individually for subdivision and combine the results for display.
- **Rationale**: PyVista documents that subdivision expects a single connected
  mesh and may fail on multi-part input. Per-component processing preserves
  ordinary multi-part files without adding another subdivision implementation.
  Invalid or non-manifold topology is rejected with a useful message, as
  required by the specification.
- **Source**: [PyVista subdivision API](https://docs.pyvista.org/api/core/_autosummary/pyvista.polydatafilters.subdivide.html)

## Dependencies and platform

- **Decision**: Use Python 3.11+, PyVista, PyVistaQt, and PySide6; use pytest as
  a development dependency.
- **Rationale**: PyVista and PyVistaQt document pip installation; PyVistaQt
  supports Qt bindings including PySide6. This is a direct, conventional Python
  desktop path.
- **Trade-offs**: VTK is a sizable native dependency and packaged application
  size may be substantial. Keep the initial deliverable as a Python
  application, not a bundled installer.
- **Sources**:
  - [PyVista installation](https://docs.pyvista.org/getting-started/installation)
  - [PyVistaQt repository](https://github.com/pyvista/pyvistaqt)
  - [VTK on PyPI](https://pypi.org/project/vtk/)
  - [Qt for Python licensing](https://doc.qt.io/qtforpython-6/licenses.html)
