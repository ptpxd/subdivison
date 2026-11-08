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
   **Butterfly** módszert. A módszer kiválasztása nem módosítja az aktuális
   hálót, és nem törli a kiválasztott iterációszámot. A következő alkalmazás az
   új módszerrel, a betöltött alapmeshből számolja újra az eredményt.
4. A jobb oldali **Selected iterations** csúszka 0-ról indul, és 0–4 között
   választhatsz. A 0 azt jelenti, hogy nincs kiválasztva iteráció; az 1–4 a
   következő felosztás iterációinak számát adja meg. A `+` és `-` billentyűkkel
   egyesével növelheted vagy csökkentheted a számot. A csúszka és a billentyűk
   csak a kijelölést változtatják; a **Mesh → Subdivide mesh** művelet vagy az
   `N` billentyű alkalmazza a kiválasztott iterációszámot. Egy iteráció a teljes
   aktuális hálót egyszer finomítja.
5. Nyomd meg az `R` billentyűt a háló legutóbbi betöltött állapotának
   visszaállításához. Ez törli az előző művelet eredmény-összegzését, nullázza
   az elvégzett iterációkat, és megtartja a kiválasztott iterációszámot és
   subdivision módszert.
6. Nyomd meg a `W` billentyűt a flat shading és a dróthálós nézet közötti
   váltáshoz.

A sikeres finomítás összegzése megmutatja a választott módszert, az alkalmazott
iterációk számát, valamint a háló oldallapjainak számát a művelet előtt és után. Az
összegzés külön mezőben marad látható akkor is, ha másik beállítást választasz;
új háló betöltése vagy visszaállítása törli, mert új alapállapotot ad meg.

Ha a fájl nem olvasható vagy a háló topológiája nem támogatott, a program
hibaüzenetet jelenít meg, és nyitva marad.

## Tesztek futtatása

```powershell
uv run python -m pytest
```

## További dokumentáció

- [Részletes quickstart és ellenőrzési lépések](specs/001-mesh-subdivision-viewer/quickstart.md)
