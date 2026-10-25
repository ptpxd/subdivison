# Data Model: Mesh Subdivision Viewer

## Mesh

Represents one loaded or subdivided surface.

- **vertices**: 3D positions indexed by stable integer identifiers for the
  current mesh revision.
- **faces**: triangular faces, each referencing three valid vertices.
- **half-edges**: directed edge records used to express face loops and
  neighboring faces.
- **components**: connected surface parts; each part is independently passed to
  the subdivision filter and then recombined for display.
- **revision**: current mesh state after loading or a completed iteration.

Validation:

- Every face references exactly three existing vertices.
- Each face has a closed three-half-edge loop.
- Each undirected edge has one or two incident faces; more than two is
  non-manifold and rejected.
- Oppositely directed half-edges on a shared edge are twins.
- A boundary half-edge has no twin; it is retained as a boundary edge.
- Vertex coordinates and generated subdivision output must be finite.
- Empty meshes, invalid indices, duplicate directed edges, and inconsistent
  connectivity are rejected with a load/refinement error.

## Half-edge

Represents one directed side of a mesh edge.

- **origin**: identifier of the start vertex.
- **face**: incident face identifier.
- **next**: next half-edge in the face's oriented loop.
- **twin**: oppositely directed half-edge on the same shared edge, or absent
  for a boundary edge.

Half-edges are rebuilt and validated when a mesh is loaded and after each
subdivision result is converted back from VTK.

## Subdivision scheme

The user-selected rule for the next refinement.

- **value**: `Loop` or `Butterfly`.
- **default**: `Loop`.

Changing the scheme affects later iterations only.

## Iteration

One subdivision operation on the current mesh.

- **input revision**: the mesh revision immediately before the operation.
- **scheme**: the selected Loop or Butterfly rule at key-press time.
- **output revision**: the newly refined and validated mesh.

Each iteration-key press triggers at most one operation. Failed operations
leave the current mesh unchanged and report an error.

## Display mode

Controls how the current mesh is drawn.

- **value**: `Wireframe` or `FlatShaded`.
- **default**: `FlatShaded` when a mesh is loaded.

Changing the display mode does not alter mesh topology or subdivision state.

## Viewer state

The desktop application holds the current optional mesh, selected scheme,
display mode, and active file path. Subdivision is available only while a valid
mesh is loaded. A failed file open leaves the previously displayed mesh intact.
