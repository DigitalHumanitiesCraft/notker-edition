# CLAUDE.md – notker-edition

## Projekt

Digitale Edition von Notkers Psalmenkommentar (Notker III. von St. Gallen, ca. 950–1022). Prototyp für einen Drittmittelantrag, Psalm 2 als Demonstrationsobjekt.

| Rolle | Person / Organisation |
|---|---|
| Auftraggeber | Dr. Philipp Pfeifer, Universität Graz |
| Kooperation | Georg Vogeler, Bernhard Bauer (ZIM Graz) |
| Auftragnehmer | Digital Humanities Craft OG |

Repository: https://github.com/DigitalHumanitiesCraft/notker-edition

## Methode

*Promptotyping*-Methode. Alle Designentscheidungen und Domänenwissen im Research Vault unter `knowledge/`. Lies die Wissensdokumente, bevor du Code schreibst.

## Wissensdokumente

| Dokument | Inhalt |
|---|---|
| `knowledge/Research Plan.md` | Gesamtplan, Scope, Arbeitsphasen |
| `knowledge/Domänenwissen.md` | Textschichten, Siglen, Datenquellen, ReA-Korpus |
| `knowledge/Probeseite Analyse.md` | DOCX-Struktur, Farbcodierung, 14 Glossen |
| `knowledge/Anforderungen.md` | 7 Epics, 13 User Stories, Priorisierung |
| `knowledge/Design.md` | Editionsinterface, Toggles, Farbsystem |
| `knowledge/Technik.md` | Pipeline, TEI-Modell, JSON-Schema, Web-Stack, IIIF |
| `knowledge/Editionsrichtlinien.md` | TEI-Kodierungsregeln für alle Textphänomene |
| `knowledge/Journal.md` | Projektchronologie, Entscheidungen |

## Architektur

**TEI-XML ist die kanonische Datenquelle.** JSON wird daraus abgeleitet.

```
Probeseite_Notker.docx → parse_probeseite.py → classify_layers.py → build_tei.py → psalm2.xml
                                                                                        ↓
                                                                                  tei_to_json.py
                                                                                        ↓
                                                                                  psalm2.json → docs/index.html
```

Web-Stack: Vanilla JS + HTML/CSS, Gentium Book Plus, OpenSeadragon (CDN), GitHub Pages. Single-File-Prinzip: `docs/index.html` enthält alles.

## Dateistruktur

```
notker-edition/
├── CLAUDE.md
├── ReadMe.md
├── index.html                             # Root-Redirect → docs/index.html
├── knowledge/                             # Research Vault (8 Dokumente)
├── data/
│   ├── Probeseite_Notker.docx             # Primärdatenquelle
│   ├── tei/psalm2.xml                     # Kanonisches TEI-XML
│   ├── processed/psalm2.json              # Abgeleitetes JSON für Web-UI
│   └── schema/tei_all.rng                 # TEI RelaxNG Schema
├── scripts/
│   ├── parse_probeseite.py                # DOCX → Python-Zwischenformat
│   ├── classify_layers.py                 # Sprachwechsel, Segment-Verkettung
│   ├── build_tei.py                       # → psalm2.xml
│   ├── tei_to_json.py                     # → psalm2.json (Bold, Siglen, Gloss-Interleaving)
│   └── validate_tei.py                    # TEI-Validierung gegen RelaxNG
└── docs/
    ├── index.html                         # Single-File-Webanwendung
    ├── richtlinien.html                   # Editionsrichtlinien (Unterseite)
    └── methode.html                       # Methode und technischer Aufbau (Unterseite)
```

## Regeln

1. **TEI ist kanonisch.** Bei Widersprüchen zwischen JSON und TEI gilt das TEI.
2. **Probeseite ist Ground Truth.** Bei Widersprüchen zwischen Dokumenten und der Probeseite gilt die Probeseite.
3. **Keine ungeklärten Siglen erfinden.** RII, N und H (als Quellen-Sigle) sind ungeklärt.
4. **Single-File-Prinzip.** Die Webanwendung ist eine HTML-Datei. CSS und JS eingebettet.
5. **Drei Textschichten.** Psalmzitation (olive), Übersetzung (grün), Kommentar (schwarz). Funktionale Klassifikation, nicht sprachbasiert. Im TEI als `<seg type="psalm|translation|commentary">`.
6. **Tests laufen lassen.** `python scripts/test_pipeline.py` nach Pipeline-Änderungen.
