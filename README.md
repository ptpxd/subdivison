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
   **Butterfly** módszert. Pozitív iterációszámnál a módszer kiválasztása
   azonnal újraszámolja a hálót a betöltött alapmeshből, az aktuális
   iterációszámmal.
4. A jobb oldali **Selected iterations** csúszka 0-ról indul, és 0–4 között
   választhatsz. Az 1–4 közötti értékek kiválasztásakor a háló automatikusan
   frissül; a `+` és `-` billentyűkkel is azonnal alkalmazhatod a módosított
   iterációszámot. A 0 kiválasztása nem változtatja meg a jelenlegi hálót, és
   nem helyettesíti a visszaállítást. Egy iteráció a teljes hálót egyszer
   finomítja. Az `N` billentyű vagy a **Mesh → Subdivide mesh** művelet
   továbbra is használható az aktuális pozitív érték újbóli alkalmazására.
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
