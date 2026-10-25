# Mesh Subdivision Viewer

Egyszerű Python asztali alkalmazás háromszögelt STL és OBJ modellek
megtekintésére és finomítására. A program Loop és Butterfly subdivisiont,
forgatást, nagyítást, dróthálós és flat shading megjelenítést támogat.

## Szükséges programok

- Python 3.11 vagy újabb
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Asztali környezet, amely támogatja a Qt ablakok megjelenítését

## Telepítés és indítás

Nyiss terminált a projekt gyökérmappájában, majd futtasd:

```powershell
uv sync --extra dev
uv run python -m mesh_subdivision_viewer
```

Az első parancs létrehozza a virtuális környezetet, és telepíti a szükséges
csomagokat. Ezután a második elindítja a programot.

## Használat

1. A **File → Open mesh...** menüpontban válassz egy `.stl` vagy `.obj` fájlt.
2. Az egér húzásával forgasd a modellt, az egérgörgővel nagyíts vagy kicsinyíts.
3. A **Mesh → Subdivision scheme** menüben válaszd ki a **Loop** vagy
   **Butterfly** módszert.
4. Nyomd meg az `N` billentyűt egy finomítási iteráció elindításához.
5. Nyomd meg a `W` billentyűt a flat shading és a dróthálós nézet közötti
   váltáshoz.

Ha a fájl nem olvasható vagy a háló topológiája nem támogatott, a program
hibaüzenetet jelenít meg, és nyitva marad.

## Tesztek futtatása

```powershell
uv run python -m pytest
```

## További dokumentáció

- [Részletes quickstart és ellenőrzési lépések](specs/001-mesh-subdivision-viewer/quickstart.md)
