# Notker Psalmenkommentar – Digitale Edition (Prototyp)

Prototyp einer digitalen Edition von Notkers Psalmenkommentar (Notker III. von St. Gallen, ca. 950–1022). Demonstrationsobjekt: **Psalm 2** (13 Verse). Proof of Concept für einen Drittmittelantrag.

| Rolle | Person / Organisation |
|---|---|
| Auftraggeber | Dr. Philipp Pfeifer, Institut für Germanistik, Universität Graz |
| Kooperation | Georg Vogeler, Bernhard Bauer (ZIM Graz) |
| Umsetzung | [Digital Humanities Craft OG](https://dhcraft.org) |

## Was der Prototyp zeigt

Notkers Psalmenkommentar verschränkt lateinischen Psalmtext, althochdeutsche Übersetzung und exegetischen Kommentar in einem Textfluss. Das Interface macht diese Schichten einzeln sichtbar:

- **Drei funktionale Textschichten** farblich unterschieden (Psalmzitat / Übersetzung / Kommentar)
- **Sechs unabhängige Toggles** (Schichten, nhd. Übersetzung, lat./ahd.-Trennung)
- **Quellenapparat** mit patristischen Quellen (Augustinus, Cassiodor, Remigius, Breviarium)
- **14 Interlinearglossen** inline dargestellt
- **Facsimile** der Handschrift CSg 0021 via IIIF (e-codices)
- **Synoptischer Psalmtext-Vergleich** (5 Textzeugen)
- **Wiener Notker** als Paralleltext (ÖNB Cod. 2681)
- **URL-Persistenz** — Deep Links für Gutachter
- **Quellentext-Betonungen** — Schlüsselbegriffe in patristischen Zitaten fett hervorgehoben

## Architektur

TEI-XML ist die kanonische Datenquelle. JSON wird daraus für die Web-UI abgeleitet.

```
Probeseite_Notker.docx → Pipeline (4 Python-Scripts) → psalm{N}.xml → psalm{N}.json → index.html
```

Kein Framework, kein Build-Step — maximale Langlebigkeit.

## Lokale Nutzung

```bash
# Pipeline ausführen (regeneriert TEI + JSON für Psalm 2)
python scripts/build_tei.py
python scripts/tei_to_json.py

# Alle vorhandenen Psalmen (wenn mehrere TEI-Dateien existieren)
python scripts/tei_to_json.py

# Lokaler Server (für JSON-Fetch + IIIF-Viewer)
python -m http.server
# → http://localhost:8000/docs/index.html

# Oder: docs/index.html direkt als Datei öffnen (Fallback auf eingebettete Daten)
```

`docs/index.html` funktioniert auch direkt als Datei (Fallback auf eingebettete Demo-Daten).

## Neuen Psalm hinzufügen

Das System ist auf Multi-Psalm-Skalierung ausgelegt. Wenn eine neue DOCX vorliegt:

```bash
python scripts/build_tei.py 3 --docx data/Psalm3.docx   # → data/tei/psalm3.xml
python scripts/tei_to_json.py 3                         # → data/processed/psalm3.json
```

`data/tei/index.json` und `data/processed/index.json` werden automatisch aktualisiert.
Das Frontend liest diese Indices und macht den neuen Psalm in der Navigation klickbar —
kein Code-Change in `docs/index.html` nötig. Deep-Link per URL-Hash: `#psalm=3`.

## Erweiterbarkeit

Drei Ausbaustufen der Text-Bild-Verknüpfung:

1. **Seiten-Synopse (implementiert):** Vers-Klick navigiert zur Handschriftenseite.
2. **Zeilen-Synopse (nächste Stufe):** Vers-Klick zoomt auf die exakte Zeile (~4–8h Annotation).
3. **Token-Synopse (Gesamtprojekt):** Mouse-Over hebt korrespondierende Stelle hervor.

**Slot-System** (Panel-Registry): neue Pool-Einträge (Quellen-Handschriften, weitere Überlieferungen) lassen sich deklarativ in `docs/index.html` als `POOL`-Eintrag ergänzen, ohne das Layout umzubauen.

## Zitierhinweis

Haupttext-Daten basieren auf dem [Referenzkorpus Altdeutsch (ReA/DDD)](https://korpling.german.hu-berlin.de/annis/ddd):

> Zeige, L. E.; Schnelle, G.; Klotz, M.; Donhauser, K.; Gippert, J.; Lühr, R. (2022). Deutsch Diachron Digital. Referenzkorpus Altdeutsch. Humboldt-Universität zu Berlin. DOI: [10.34644/laudatio-dev-MiXVDnMB7CArCQ9CABmW](https://doi.org/10.34644/laudatio-dev-MiXVDnMB7CArCQ9CABmW)

Facsimile: [e-codices, CSg 0021](https://www.e-codices.unifr.ch/de/csg/0021/11/0/)

## Lizenz

Quellcode: MIT. Textdaten und Übersetzungen: Rechte beim jeweiligen Urheber.
