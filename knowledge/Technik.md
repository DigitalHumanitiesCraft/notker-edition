---
type: technical
created: 2026-02-27
updated: 2026-03-23
tags: [notker, technical, tei, pipeline]
---

# Technik: Notker Psalmenkommentar Prototyp

## Architekturprinzip

**TEI-XML ist die kanonische Datenquelle.** JSON ist ein abgeleitetes Format für die Web-UI. Die Pipeline verläuft:

```
Probeseite_Notker.docx
        │
        ▼
┌─────────────────────────┐
│  parse_probeseite.py     │  DOCX → Python-Zwischenformat
│  Regelbasiert: Farben,   │  (Dataclasses: Run, Segment,
│  Merged Cells, Zeilen-   │   TextLine, GlossLine, SourceEntry)
│  typen, Vers-Zuordnung   │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│  classify_layers.py      │  Anreicherung
│  Sprachwechsel (<foreign>)│  Regelbasiert + Heuristik
│  Segment-Verkettung      │  (LLM-Stub für Kommentar)
│  Glossen-Validierung     │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│  build_tei.py            │  → data/tei/psalm2.xml
│  lxml.etree              │  Kanonisches Format
│  TEI-All RelaxNG         │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│  tei_to_json.py          │  → data/processed/psalm2.json
│  TEI → JSON für Web-UI   │  Abgeleitetes Format
│  (noch nicht gebaut)     │
└────────────┬────────────┘
             ▼
         docs/index.html
```

## Web-Stack

| Komponente | Technologie | Begründung |
|---|---|---|
| Frontend | Vanilla JS + HTML/CSS | Kein Build-Step, keine Dependencies, Langlebigkeit |
| Typografie | Gentium Book Plus (Google Fonts), Inter (UI) | Ahd.-Sonderzeichen, akademische Ästhetik |
| IIIF-Viewer | OpenSeadragon 4.1 (CDN) | Standard für Handschriftendigitalisate |
| Deployment | GitHub Pages (`/docs`) | Kostenlos, kein Server-Setup |
| Datenaufbereitung | Python (python-docx, lxml) | DOCX-Parsing, TEI-Generierung |

Single-File-Prinzip: `docs/index.html` enthält CSS und JS eingebettet.

## TEI-XML-Modell

### Dokumentstruktur

```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="goh">
  <teiHeader>
    <!-- Taxonomien: #fn-psalm, #fn-transl, #fn-comm, #fn-gloss -->
    <!-- Quellen: #src-A, #src-C, #src-R, #src-Br, #src-RII, #src-N -->
    <!-- Psalter-Zeugen: #wit-G, #wit-R, #wit-H, #wit-A-psa, #wit-C-psa -->
  </teiHeader>
  <facsimile><!-- IIIF-Surfaces --></facsimile>
  <text>
    <front><div type="introduction"/></front>
    <body>
      <div type="psalm" n="2">
        <!-- 8 × <div type="verse"> mit <ab>-Zeilen -->
      </div>
    </body>
    <back>
      <div type="psalm_comparison"><!-- 5 Zeugen als <app>/<rdg> --></div>
      <div type="parallel_tradition"><!-- Wiener Notker --></div>
    </back>
  </text>
</TEI>
```

### Encoding-Entscheidungen

| DOCX-Element | TEI-Element | Methode |
|---|---|---|
| Olive Runs (`#806000`) | `<seg type="psalm" ana="#fn-psalm" xml:lang="la">` | Regel (Farbe) |
| Grüne Runs (`#00B050`) | `<seg type="translation" ana="#fn-transl" xml:lang="goh">` | Regel (Farbe) |
| Schwarze Runs | `<seg type="commentary" ana="#fn-comm">` + `<foreign>` | Regel + Heuristik |
| Glossen-Zeile | `<ab ana="#fn-gloss"><gloss>` | Heuristik (Zeilenlänge) |
| Quellenapparat-Zeile | `<cit ana="#src-X"><quote>` + `<note type="translation">` | Regel (Sigle in Spalte 0) |
| Siglen-Spalte | `<note type="sigle" place="margin" cert="low">` | Regel |
| Silbentrennung | `<lb break="no"/>` | Regel (Zeilenende mit `-`) |
| Zeilenübergreifend | `@part`/`@next`/`@prev` auf `<seg>` | Regel |
| Psaltervergleich | `<app><rdg wit="#...">` | Struktur (T11, T12) |
| Wiener Notker | `<div type="parallel_tradition">` Rohtext | Struktur (T13) |

**Warum `<seg>` statt `<quote>` für Psalmzitate?** Notker paraphrasiert gelegentlich. `<seg type="psalm">` ist ehrlicher.

**Warum `<cit>` statt `<app>` für Quellen?** Die Quellen sind Notkers Vorlagen, keine textkritischen Varianten. `<app>` wird nur im Psaltervergleich verwendet.

### Ungeklärte Siglen

RII und N mit `@cert="low"` in der Taxonomie. Im Text: `<note type="editorial">ungeklärt</note>`.

## JSON-Schema (Interface-Vertrag mit UI)

Das JSON wird aus dem TEI abgeleitet (`tei_to_json.py`, noch nicht gebaut). Die Web-UI erwartet:

```json
{
  "psalm": 2,
  "metadata": {
    "title": "Psalm 2",
    "manuscript": "CSg 0021",
    "iiif_manifest": "https://www.e-codices.unifr.ch/metadata/iiif/csg-0021/manifest.json",
    "facsimile_start_canvas": "...canvas/csg-0021_011.json",
    "edition_pages": "R10–R13"
  },
  "verses": [
    {
      "number": 1,
      "edition_page": "R10",
      "sections": [
        {
          "type": "psalm_citation | translation | commentary",
          "text": "...",
          "language": "lat | ahd | ahd_lat_mixed",
          "source_sigles": ["G", "R"]
        }
      ],
      "glosses": [
        { "text": "iúdon diêt", "translation_nhd": "Juden Volk", "relates_to": "gentes" }
      ],
      "translation_nhd": "...",
      "sources": [
        { "sigle": "C", "name": "Cassiodor, ...", "latin_text": "...", "german_translation": "..." }
      ]
    }
  ],
  "psalm_text_comparison": { "witnesses": [...] },
  "wiener_notker": { "text": "..." }
}
```

### TEI → JSON Mapping

| TEI-Element | JSON-Feld |
|---|---|
| `<div type="verse" n="X">` | `verses[].number` |
| `<seg type="psalm">` | `sections[].type: "psalm_citation"` |
| `<seg type="translation">` | `sections[].type: "translation"` |
| `<seg type="commentary">` | `sections[].type: "commentary"` |
| `<ab ana="#fn-gloss"><gloss>` | `glosses[]` |
| `<cit ana="#src-X">` | `sources[]` |
| `<note type="translation_nhd">` | `translation_nhd` |
| `<app>/<rdg>` | `psalm_text_comparison.witnesses[]` |

Silbentrennungen (`<lb break="no"/>`) werden im JSON aufgelöst (zusammengeführt). Die Zeilenstruktur der Probeseite bleibt nur im TEI erhalten.

## IIIF-Integration

| Eigenschaft | Wert |
|---|---|
| Manifest | `https://www.e-codices.unifr.ch/metadata/iiif/csg-0021/manifest.json` |
| API-Version | IIIF Presentation 2.0 |
| Label | St. Gallen, Stiftsbibliothek, Cod. Sang. 21 |
| Psalm 2 Start | Seite 11 (Canvas-Index 10, 0-basiert) |
| Canvas-Pattern | `csg-0021_011.json`, `csg-0021_012.json` etc. |
| Text-Bild-Synopse | Seiten-Ebene: Vers-Klick navigiert zum korrekten Canvas |

Vers→Seite-Mapping (vorläufig, gegen Facsimile zu verifizieren):

| Verse | MS-Seite | Canvas-Index |
|---|---|---|
| 1–3 | 11 | 10 |
| 4–6 | 12 | 11 |
| 7–9 | 13 | 12 |
| 10–13 | 14 | 13 |

## Dateistruktur (Ist-Stand)

```
notker-edition/
├── CLAUDE.md                          # Projektprompt
├── ReadMe.md
├── knowledge/                         # Research Vault (Obsidian)
│   ├── Research Plan.md
│   ├── Domänenwissen.md
│   ├── Probeseite Analyse.md
│   ├── Anforderungen.md
│   ├── Design.md
│   ├── Technik.md                     # ← dieses Dokument
│   ├── Journal.md
│   ├── 2026-02-24 Erstgespräch.md
│   └── Referenzkorpus Altdeutsch.md
├── data/
│   ├── Probeseite_Notker.docx         # Primärdatenquelle
│   └── tei/
│       └── psalm2.xml                 # Kanonisches TEI-XML (764 Zeilen)
├── scripts/
│   ├── parse_probeseite.py            # DOCX → Zwischenformat (717 Z.)
│   ├── classify_layers.py             # Anreicherung (371 Z.)
│   └── build_tei.py                   # Zwischenformat → TEI-XML (577 Z.)
└── docs/
    └── index.html                     # Single-File-Webanwendung (GitHub Pages)
```

## Offene technische Fragen

- [ ] `tei_to_json.py` schreiben (Brücke TEI → JSON → UI)
- [ ] Vers→Seite-Mapping gegen Facsimile verifizieren
- [ ] Silbentrennungen im JSON auflösen
- [ ] Glossen-Erkennung: Schwellwert für Zeilenlänge kalibrieren
- [x] ~~IIIF-Manifest-URL verifizieren~~ → funktioniert (Presentation v2)

## Verknüpfungen

- [[Design]] — UI-Konzept, Toggle-System, Farbsystem
- [[Probeseite Analyse]] — DOCX-Struktur und Parsing-Implikationen
- [[Research Plan]] — Arbeitsphasen und Abhängigkeiten
