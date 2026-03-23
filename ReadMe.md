# Notker Psalmenkommentar – Digitale Edition (Prototyp)

Prototyp einer digitalen Edition von Notkers Psalmenkommentar (Notker III. von St. Gallen, ca. 950–1022). Demonstrationsobjekt: **Psalm 2** (13 Verse). Erstellt als Proof of Concept für einen Drittmittelantrag.

## Projektkontext

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
- **Facsimile** der Handschrift CSg 0021 via IIIF (e-codices) mit Seiten-Synopse
- **Synoptischer Psalmtext-Vergleich** (5 Textzeugen: Gallicanum, Romanum, Hebraicum, A-Psalter, C-Psalter)
- **Wiener Notker** als Paralleltext (ÖNB Cod. 2681)
- **URL-Persistenz** — Deep Links für Gutachter auf bestimmte Verse mit Toggle-Konfiguration

## Architektur

TEI-XML ist die kanonische Datenquelle. JSON wird daraus für die Web-UI abgeleitet.

```
Probeseite_Notker.docx
  → parse_probeseite.py → classify_layers.py → build_tei.py
  → data/tei/psalm2.xml (kanonisch)
  → tei_to_json.py → data/processed/psalm2.json (abgeleitet)
  → docs/index.html (Single-File-UI)
```

## Struktur

```
notker-edition/
├── knowledge/                         # Research Vault (11 Obsidian-Dokumente)
├── data/
│   ├── Probeseite_Notker.docx         # Primärdatenquelle (Philipp Pfeifer)
│   ├── tei/psalm2.xml                 # Kanonisches TEI-XML
│   ├── processed/psalm2.json          # JSON für Web-UI
│   └── schema/tei_all.rng             # TEI RelaxNG Schema
├── scripts/
│   ├── parse_probeseite.py            # DOCX → Python-Zwischenformat
│   ├── classify_layers.py             # Sprachwechsel, Segment-Verkettung
│   ├── build_tei.py                   # → TEI-XML
│   ├── tei_to_json.py                 # TEI → JSON
│   └── validate_tei.py                # TEI-Validierung
└── docs/
    └── index.html                     # Single-File-Webanwendung (GitHub Pages)
```

## Technologie

- **Frontend:** Vanilla JS + HTML/CSS, Gentium Book Plus + Inter (Google Fonts), OpenSeadragon (IIIF)
- **Datenmodell:** TEI-XML (kanonisch) → JSON (abgeleitet)
- **Datenaufbereitung:** Python (python-docx, lxml)
- **Deployment:** GitHub Pages (statisch, kein Server)

Kein Framework, kein Build-Step — maximale Langlebigkeit.

## Lokale Nutzung

```bash
# Pipeline ausführen (regeneriert TEI + JSON)
python scripts/build_tei.py
python scripts/tei_to_json.py

# Lokaler Server (für JSON-Fetch)
python -m http.server
# → http://localhost:8000/docs/index.html

# Oder: docs/index.html direkt als Datei öffnen (Fallback auf eingebettete Demo-Daten)
```

## Erweiterbarkeit

Drei Ausbaustufen der Text-Bild-Verknüpfung:

1. **Seiten-Synopse (implementiert):** Vers-Klick navigiert IIIF-Viewer zur korrekten Handschriftenseite.
2. **Zeilen-Synopse (nächste Stufe):** Vers-Klick zoomt auf die exakte Zeile. Erfordert Koordinaten-Annotation (~4–8h pro Psalm).
3. **Token-Synopse (Gesamtprojekt):** Mouse-Over hebt korrespondierende Stelle im Digitalisat hervor (Elwood-Viewer-Methode).

Das Toggle-System skaliert auf alle 150 Psalmen. Die Pipeline braucht nur neue Probeseite-Daten als Input.

## Zitierhinweis

Haupttext-Daten basieren auf dem [Referenzkorpus Altdeutsch (ReA/DDD)](https://korpling.german.hu-berlin.de/annis/ddd):

> Zeige, L. E.; Schnelle, G.; Klotz, M.; Donhauser, K.; Gippert, J.; Lühr, R. (2022). Deutsch Diachron Digital. Referenzkorpus Altdeutsch. Humboldt-Universität zu Berlin. DOI: [10.34644/laudatio-dev-MiXVDnMB7CArCQ9CABmW](https://doi.org/10.34644/laudatio-dev-MiXVDnMB7CArCQ9CABmW)

Facsimile: [e-codices, CSg 0021](https://www.e-codices.unifr.ch/de/csg/0021/11/0/)

## Lizenz

Quellcode: MIT. Textdaten und Übersetzungen: Rechte beim jeweiligen Urheber.
