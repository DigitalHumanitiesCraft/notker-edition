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
| `knowledge/Offene Korrekturen.md` | Bug-Tracker auf tieferer Ebene (TEI, Pipeline, UI) |

## Architektur

**TEI-XML ist die kanonische Datenquelle.** JSON wird daraus abgeleitet.

```
Probeseite_Notker.docx → parse_probeseite.py → classify_layers.py → build_tei.py → psalm{N}.xml
                                                                          ↓
                                                                    tei_to_json.py
                                                                          ↓
                                                                    psalm{N}.json → docs/index.html
```

Textkorrekturen (z.B. Pfeifer-Review-Feedback) sind als zwei Listen in
`parse_probeseite.py` deklariert:
- `PFEIFER_CORRECTIONS` — Fließtext-Patterns, via `apply_corrections()`
- `PFEIFER_LINE_CORRECTIONS` — zeilenbezogene Patterns, via `apply_line_corrections()` pro `<l>`

Beide sind idempotent (str.replace findet nichts, wenn die Korrekturen bereits in
einer aktualisierten DOCX enthalten sind).

**Multi-Psalm-ready:**
- `python scripts/build_tei.py [N]` erzeugt `data/tei/psalm{N}.xml` (Default: 2)
- `python scripts/tei_to_json.py [N]` erzeugt `data/processed/psalm{N}.json` (oder alle)
- `data/tei/index.json` und `data/processed/index.json` listen alle verfügbaren Psalmen
- Frontend liest den JSON-Index dynamisch und rendert die Psalm-Nav. Aktiver Psalm via URL-Hash `#psalm=N`
- `build_tei.py` ruft am Ende `sync_vault.py` auf (kopiert `knowledge/*.md` → `docs/vault/`)

Web-Stack: Vanilla JS + HTML/CSS, Gentium Book Plus, OpenSeadragon (CDN), GitHub Pages. Single-File-Prinzip: `docs/index.html` enthält alles.

## Dateistruktur

```
notker-edition/
├── CLAUDE.md
├── ReadMe.md
├── index.html                             # Root-Redirect → docs/index.html
├── knowledge/                             # Research Vault (Markdown-Dokumente)
├── data/
│   ├── Probeseite_Notker.docx             # Primärdatenquelle
│   ├── tei/psalm{N}.xml                   # Kanonisches TEI-XML (normalisiert)
│   ├── tei/index.json                     # Liste verfügbarer Psalmen (TEI)
│   ├── processed/psalm{N}.json            # Abgeleitetes JSON für Web-UI
│   ├── processed/index.json               # Liste verfügbarer Psalmen (JSON)
│   └── schema/tei_all.rng                 # TEI RelaxNG Schema
├── scripts/
│   ├── parse_probeseite.py                # DOCX → Zwischenformat (+ PFEIFER_CORRECTIONS, PFEIFER_LINE_CORRECTIONS)
│   ├── classify_layers.py                 # Sprachwechsel, Segment-Verkettung
│   ├── build_tei.py                       # → psalm{N}.xml (akzeptiert psalm_number als CLI-Arg)
│   ├── tei_to_json.py                     # → psalm{N}.json (single oder alle)
│   ├── sync_vault.py                      # knowledge/*.md → docs/vault/ (mit Git-Hash)
│   ├── test_pipeline.py                   # Integration/Regression-Tests
│   └── validate_tei.py                    # TEI-Validierung gegen RelaxNG
├── tests/
│   ├── test_gloss_classification.py       # Unit-Tests Glossen-Heuristik
│   └── test_crossverse_nhd.py             # Unit-Tests Cross-Verse-nhd-Drift
└── docs/
    ├── index.html                         # Single-File-Webanwendung
    ├── richtlinien.html                   # Editionsrichtlinien (Unterseite)
    ├── methode.html                       # Methode und technischer Aufbau (Unterseite)
    ├── vault.html                         # Research-Vault-Viewer (rendert knowledge/*.md)
    └── vault/                             # Synchronisierte Kopie von knowledge/ + index.json
```

## Neuen Psalm hinzufügen

Wenn Pfeifer eine DOCX für einen weiteren Psalm liefert:
1. DOCX nach `data/{Psalm-Name}.docx` legen
2. `python scripts/build_tei.py N --docx data/{Psalm-Name}.docx` — erzeugt `data/tei/psalmN.xml` + aktualisiert Index
3. `python scripts/tei_to_json.py N` — erzeugt `data/processed/psalmN.json` + aktualisiert Index
4. Frontend erkennt den neuen Psalm automatisch (Reload genügt). Psalm-Nav macht ihn klickbar.

Keine Code-Änderung in `docs/index.html` nötig.

## Regeln

1. **TEI ist kanonisch.** Bei Widersprüchen zwischen JSON und TEI gilt das TEI.
2. **Probeseite ist Ground Truth.** Bei Widersprüchen zwischen Dokumenten und der Probeseite gilt die Probeseite.
3. **Keine ungeklärten Siglen erfinden.** RII, N und H (als Quellen-Sigle) sind ungeklärt.
4. **Single-File-Prinzip.** Die Webanwendung ist eine HTML-Datei. CSS und JS eingebettet.
5. **Drei Textschichten.** Psalmzitation (olive), Übersetzung (grün), Kommentar (schwarz). Funktionale Klassifikation, nicht sprachbasiert. Im TEI als `<seg type="psalm|translation|commentary">`.
6. **Tests laufen lassen.** `python scripts/test_pipeline.py` nach Pipeline-Änderungen.
