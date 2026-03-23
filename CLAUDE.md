# CLAUDE.md – notker-edition

## Projekt

Digitale Edition von Notkers Psalmenkommentar (Notker III. von St. Gallen, ca. 950–1022). Prototyp für einen Drittmittelantrag, Psalm 2 als Demonstrationsobjekt. Auftraggeber ist Dr. Philipp Pfeifer (Institut für Germanistik, Universität Graz). Kooperationspartner sind Georg Vogeler und Bernhard Bauer (ZIM Graz). Auftragnehmer ist Digital Humanities Craft OG.

Repository: https://github.com/DigitalHumanitiesCraft/notker-edition

## Methode

Das Projekt folgt der *Promptotyping*-Methode. Alle Designentscheidungen, Domänenwissen und Implementierungsdetails sind in einem Obsidian-basierten Research Vault unter `knowledge/` erfasst. Lies die Wissensdokumente, bevor du Code schreibst.

## Wissensdokumente

| Dokument | Inhalt |
|---|---|
| `knowledge/Research Plan.md` | Gesamtplan, Scope-Bewertung, Arbeitsphasen |
| `knowledge/Domänenwissen.md` | Notkers Psalmenkommentar, Textschichten, Datenquellen |
| `knowledge/Probeseite Analyse.md` | DOCX-Struktur, Farbcodierung, 14 Glossen, Siglen |
| `knowledge/Anforderungen.md` | 7 Epics, 13 User Stories, Priorisierung |
| `knowledge/Design.md` | Editionsinterface, Toggles, Farbsystem, Informationshierarchie |
| `knowledge/Technik.md` | Pipeline (DOCX→TEI→JSON), JSON-Schema, Web-Stack, IIIF |
| `knowledge/implementation.md` | TEI-XML-Modell im Detail, Encoding-Entscheidungen, DOCX→TEI-Mapping |
| `knowledge/Editionsrichtlinien.md` | Editorische Richtlinien für die TEI-Codierung |
| `knowledge/Journal.md` | Projektchronologie, Entscheidungen, offene Fragen |
| `knowledge/2026-02-24 Erstgespräch.md` | Gesprächsnotiz Erstgespräch |
| `knowledge/Referenzkorpus Altdeutsch.md` | ReA/DDD-Korpus, Annotationsebenen |

## Architektur

**TEI-XML ist die kanonische Datenquelle.** JSON wird daraus abgeleitet.

```
Probeseite_Notker.docx → parse_probeseite.py → classify_layers.py → build_tei.py → psalm2.xml
                                                                                        ↓
                                                                                  tei_to_json.py
                                                                                        ↓
                                                                                  psalm2.json → docs/index.html
```

Web-Stack: Vanilla JS + HTML/CSS, Gentium Book Plus (Google Fonts), OpenSeadragon (CDN), GitHub Pages. Single-File-Prinzip: `docs/index.html` enthält alles.

## Dateistruktur

```
notker-edition/
├── CLAUDE.md
├── ReadMe.md
├── index.html                             # Root-Redirect → docs/index.html (GitHub Pages)
├── .gitignore
├── knowledge/                             # Research Vault (11 Obsidian-Dokumente)
├── data/
│   ├── Probeseite_Notker.docx             # Primärdatenquelle
│   ├── tei/
│   │   └── psalm2.xml                     # Kanonisches TEI-XML
│   ├── processed/
│   │   └── psalm2.json                    # Abgeleitetes JSON für Web-UI
│   └── schema/
│       └── tei_all.rng                    # TEI RelaxNG Schema
├── scripts/
│   ├── parse_probeseite.py                # DOCX → Python-Zwischenformat
│   ├── classify_layers.py                 # Sprachwechsel, Segment-Verkettung
│   ├── build_tei.py                       # → psalm2.xml
│   ├── tei_to_json.py                     # → psalm2.json
│   └── validate_tei.py                    # TEI-Validierung gegen RelaxNG
└── docs/
    └── index.html                         # Single-File-Webanwendung
```

## Regeln

1. **TEI ist kanonisch.** Bei Widersprüchen zwischen JSON und TEI gilt das TEI.
2. **Probeseite ist Ground Truth.** Bei Widersprüchen zwischen Dokumenten und der Probeseite gilt die Probeseite.
3. **Keine ungeklärten Siglen erfinden.** RII, N und H (als Quellen-Sigle) sind ungeklärt. Kennzeichne sie als solche.
4. **Single-File-Prinzip.** Die Webanwendung ist eine HTML-Datei. CSS und JS eingebettet.
5. **Drei Textschichten.** Psalmzitation (olive), Übersetzung (grün), Kommentar (schwarz). Funktionale Klassifikation, nicht sprachbasiert. Im TEI als `<seg type="psalm|translation|commentary">`, im JSON als `section.type`.
