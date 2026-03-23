---
type: implementation
created: 2026-02-27
updated: 2026-03-23
tags: [notker, technical]
---

# Technik: Notker Psalmenkommentar Prototyp

## Stack

| Komponente | Technologie | Begründung |
|---|---|---|
| Frontend | Vanilla JS + HTML/CSS | Kein Build-Step, keine Dependencies, maximale Langlebigkeit |
| Styling | Tailwind CSS (CDN) | Schnelles Prototyping, konsistentes Design |
| Datenmodell | JSON | Statisch, kein Server nötig |
| IIIF-Viewer | OpenSeadragon (CDN) | Standard für Handschriftendigitalisate |
| Deployment | GitHub Pages oder lokale Datei | Kostenlos, kein Server-Setup |
| Datenaufbereitung | Python (python-docx) | DOCX-Parsing inkl. Farbextraktion |

Bewusst kein Framework. Single-File-Prinzip: eine HTML-Datei mit eingebettetem JS/CSS.

## JSON-Datenmodell (revidiert 23.03.)

Schema revidiert nach [[Probeseite Analyse]]. Zentrale Änderung: `section.type` ist jetzt dreigliedrig (psalm_citation, translation, commentary) statt zweigliedrig.

```json
{
  "psalm": 2,
  "metadata": {
    "title": "Psalm 2",
    "edition": "Tax/Sehrt (1970er)",
    "manuscript": "CSg 0021",
    "iiif_manifest": "https://www.e-codices.unifr.ch/metadata/iiif/csg-0021/manifest.json",
    "facsimile_start": "https://www.e-codices.unifr.ch/de/csg/0021/11/0/",
    "edition_pages": "R10–R13",
    "source_editions": {
      "quellenliste": "https://www.degruyterbrill.com/document/doi/10.1515/9783110935332/html",
      "edition": "https://www.degruyterbrill.com/document/doi/10.1515/9783110967500/html"
    }
  },
  "verses": [
    {
      "number": 1,
      "edition_lines": "21–27",
      "sections": [
        {
          "type": "psalm_citation",
          "text": "QVARE FREMVERVNT GENTES.",
          "language": "lat",
          "translation_nhd": "WARUM LÄRMTEN DIE VÖLKER.",
          "source_sigles": ["G", "R"]
        },
        {
          "type": "translation",
          "text": "Ziu grís-cramoton an christum ebraicȩ gentes?",
          "language": "ahd_lat_mixed",
          "translation_nhd": "Warum wüteten an Christus die hebräischen Völker?",
          "source_sigles": ["C"]
        },
        {
          "type": "commentary",
          "text": "des ín ubelo spuên solta.",
          "language": "ahd",
          "translation_nhd": "dessen, (das) ihnen übel bekommen sollte.",
          "source_sigles": []
        }
      ],
      "glosses": [
        {
          "position": "nach Row 1",
          "text": "iúdon diêt",
          "translation_nhd": "Juden Volk",
          "relates_to": "gentes"
        }
      ],
      "sources": [
        {
          "sigle": "C",
          "name": "Cassiodor, Expositio Psalmorum",
          "latin_text": "Quattuor membris psalmi huius species decora formata est...",
          "german_translation": "In vier Teilen ist dieses Psalms schöne Gestalt geformt...",
          "edition_reference": null
        }
      ],
      "bible_references": []
    }
  ],
  "psalm_text_comparison": {
    "witnesses": [
      {
        "sigle": "G",
        "name": "Gallicanum",
        "manuscript": null,
        "verses": {}
      },
      {
        "sigle": "H",
        "name": "Hebraicum (iuxta Hebraeos)",
        "manuscript": "Bamberg Ms. 44",
        "verses": {}
      }
    ]
  },
  "wiener_notker": {
    "manuscript": "ÖNB Cod. 2681",
    "edition": "Heinzle & Scherrer",
    "text": ""
  }
}
```

### Modellierungsentscheidungen

**section.type (revidiert).** Drei Typen statt zwei: `psalm_citation` (olive in Probeseite), `translation` (grün), `commentary` (schwarz). Ermöglicht die drei Textschicht-Toggles aus [[Design#Toggle-System]].

**section.language.** Neues Feld. Werte: `lat`, `ahd`, `ahd_lat_mixed`. Ermöglicht den lat./ahd.-Split orthogonal zu den Textschicht-Toggles. Die Sprache ist NICHT identisch mit dem Typ: Kommentar kann `ahd` oder `ahd_lat_mixed` sein.

**bible_references.** Leeres Array pro Vers, vorbereitet für Philipps Querverweise-Wunsch. Daten fehlen noch.

**Siglen-Disambiguation.** Quellenapparat: `sources[].sigle`. Psalmtext-Vergleich: eigener Namespace `psalm_text_comparison.witnesses[].sigle`. Haupttext-Siglen: `sections[].source_sigles` (Bedeutung noch zu klären mit Philipp).

**Interlinearglossen.** Array `glosses[]` pro Vers. Position textuell (Tabellenzeilen-Referenz). Token-basierte Zuordnung wäre präziser, erfordert aber Tokenisierung.

## Datenaufbereitung

### Schritt 1 – Probeseite parsen (Primärquelle)

Python-Script `parse_probeseite.py`. Nutzt python-docx.

Kernlogik:
1. Tabellen iterieren, Paragraphen-Überschriften zwischen Tabellen als Vers-Zuordnung nutzen
2. Pro Tabellenzeile: Zeilentyp erkennen (Haupttext / Quellenapparat / Glosse / Leer)
3. Im Haupttext: Run-Level-Farbanalyse → section.type ableiten
4. Merged Cells deduplizieren (Spalten 0–2 identisch → nur einmal lesen)
5. nhd. Übersetzung aus vorletzter Spalte, Siglen aus letzter Spalte

Heuristiken:
- **Quellenapparat-Zeile:** Spalte 0 enthält eine einzelne Sigle (C, A, R, Br, RII, N)
- **Interlinearglosse:** Kurze Zeile (< ~30 Zeichen), keine olive Farbe, keine Sigle in letzter Spalte
- **Leerzeile:** Alle Spalten leer

### Schritt 2 – ANNIS-HTML parsen (Sekundärquelle)

Python-Script `parse_annis.py`. Extrahiert `<span textval="...">`-Elemente und Zeilennummern aus `<td>`. Liefert Handschriften-Zeilenreferenzen.

**Status:** ANNIS-HTML (`data/raw/annis_psalm2.html`) fehlt noch im Repository.

### Schritt 3 – Referenzsysteme verknüpfen

Manuelle Brücke zwischen Editionszeilen (Probeseite) und Handschriftenzeilen (ANNIS). Einmalig für 13 Verse.

## Dateistruktur (Soll)

```
notker-edition/
├── CLAUDE.md               # Projektprompt
├── README.md
├── knowledge/              # Research Vault (Obsidian)
│   ├── Research Plan.md
│   ├── Domänenwissen.md
│   ├── Probeseite Analyse.md
│   ├── Anforderungen.md
│   ├── Design.md
│   ├── Technik.md
│   ├── Journal.md
│   └── ...
├── data/
│   ├── Probeseite_Notker.docx  # Primärdatenquelle
│   └── processed/
│       └── psalm2.json          # Aufbereitetes Datenmodell
├── scripts/
│   ├── parse_probeseite.py
│   └── parse_annis.py
└── app/
    └── index.html               # Single-File-Anwendung
```

## Offene technische Fragen

- [ ] IIIF-Manifest-URL verifizieren
- [ ] ANNIS-HTML beschaffen oder aus Scope entfernen
- [ ] Sprach-Annotationsebene im ANNIS-Datenmodell?
- [ ] Glossen-Erkennung: Schwellwert für Zeilenlänge kalibrieren
- [ ] Vers-Zuordnung: Paragraphen-Parsing zwischen Tabellen testen

## Verknüpfungen

- [[Design]] — UI-Konzept und Toggle-System
- [[Probeseite Analyse]] — Parsing-Implikationen
- [[Research Plan]] — Arbeitsphasen
