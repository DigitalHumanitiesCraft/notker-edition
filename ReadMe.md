# Notker Psalmenkommentar – Digitale Edition (Prototyp)

Prototyp einer digitalen Edition von Notkers Psalmenkommentar (Notker III. von St. Gallen, ca. 950–1022). Demonstrationsobjekt: **Psalm 2** (13 Verse). Erstellt als Proof of Concept für einen Drittmittelantrag.

## Projektkontext

| Rolle | Person / Organisation |
|---|---|
| Auftraggeber | Dr. Philipp Pfeifer, Institut für Germanistik, Universität Graz |
| Kooperation | Georg Vogeler, Bernhard Bauer (ZIM Graz) |
| Umsetzung | [Digital Humanities Craft OG](https://dhcraft.org) |

## Was der Prototyp zeigt

Notkers Psalmenkommentar verschränkt **lateinischen Psalmtext**, **althochdeutsche Übersetzung** und **exegetischen Kommentar** in einem einzigen Textfluss. Bisherige Druckeditionen lösen diese Schichten nicht auf. Der Prototyp macht sie sichtbar:

- **Drei funktionale Textschichten** farblich unterschieden (Psalmzitat / Übersetzung / Kommentar)
- **Sechs unabhängige Toggles** zum Ein-/Ausblenden von Schichten, nhd. Übersetzung und lat./ahd.-Trennung
- **Quellenapparat** mit patristischen Quellen (Augustinus, Cassiodor, Remigius, Breviarium) – lateinisch und deutsch
- **14 Interlinearglossen** inline dargestellt
- **Facsimile** der Handschrift CSg 0021 via IIIF (e-codices)
- **Synoptischer Psalmtext-Vergleich** (5 Textzeugen) und Wiener Notker als Paralleltext

## Datengrundlage

Die maßgebliche Primärdatenquelle ist Philipps Probeseite (`data/Probeseite_Notker.docx`), eine tabellarische Aufbereitung von Psalm 2 mit Farbcodierung der Textschichten. Das Python-Script `scripts/parse_probeseite.py` extrahiert daraus das strukturierte JSON-Datenmodell (`data/processed/psalm2.json`).

## Struktur

```
notker-edition/
├── CLAUDE.md              # Projektprompt für Claude Code
├── ReadMe.md
├── knowledge/             # Research Vault (Obsidian-kompatibel)
│   ├── Research Plan.md   # Gesamtplan, Scope, Arbeitsphasen
│   ├── Domänenwissen.md   # Notker, Textschichten, Siglen
│   ├── Probeseite Analyse.md  # DOCX-Analyse: Tabellen, Farben, Glossen
│   ├── Anforderungen.md   # 7 Epics, 13 User Stories
│   ├── Design.md          # Editionsinterface, Typografie, Toggles
│   ├── Technik.md         # JSON-Schema, Web-Stack, Parsing
│   ├── implementation.md  # TEI-XML-Modell, DOCX→TEI-Pipeline
│   ├── Journal.md         # Projektchronologie
│   ├── 2026-02-24 Erstgespräch.md
│   └── Referenzkorpus Altdeutsch.md
├── data/
│   ├── Probeseite_Notker.docx      # Primärdatenquelle
│   └── processed/
│       └── psalm2.json             # Aufbereitetes Datenmodell
├── scripts/
│   └── parse_probeseite.py         # DOCX → JSON
└── app/
    └── index.html                  # Single-File-Webanwendung (in Arbeit)
```

## Technologie

- **Frontend:** Vanilla JS + HTML/CSS, Tailwind CSS (CDN), OpenSeadragon (CDN)
- **Datenmodell:** JSON (kein Backend, kein Server)
- **Datenaufbereitung:** Python (python-docx)
- **Deployment:** GitHub Pages oder lokale HTML-Datei

Bewusst kein Framework — maximale Langlebigkeit. Der Prototyp muss in zwei Jahren noch funktionieren, ohne dass jemand `npm install` ausführt.

## Methode

Das Projekt folgt der [Promptotyping](https://dhcraft.org)-Methode. Alle Designentscheidungen und Domänenwissen sind in den Wissensdokumenten unter `knowledge/` dokumentiert.

## Zitierhinweis

Haupttext-Daten basieren auf dem [Referenzkorpus Altdeutsch (ReA/DDD)](https://korpling.german.hu-berlin.de/annis/ddd):

> Zeige, L. E.; Schnelle, G.; Klotz, M.; Donhauser, K.; Gippert, J.; Lühr, R. (2022). Deutsch Diachron Digital. Referenzkorpus Altdeutsch. Humboldt-Universität zu Berlin. DOI: [10.34644/laudatio-dev-MiXVDnMB7CArCQ9CABmW](https://doi.org/10.34644/laudatio-dev-MiXVDnMB7CArCQ9CABmW)

Facsimile: [e-codices, CSg 0021](https://www.e-codices.unifr.ch/de/csg/0021/11/0/)

## Lizenz

Quellcode: MIT. Textdaten und Übersetzungen: Rechte beim jeweiligen Urheber.
