---
type: plan
created: 2026-03-23
updated: 2026-04-16
status: active
tags: [digital-humanities, notker, research-plan]
---

# Research Plan: Notker Psalmenkommentar – Digitaler Prototyp

## Projektkontext

Prototyp einer digitalen Edition von Notkers Psalmenkommentar. Psalm 2 (13 Verse). Proof of Concept für Drittmittelantrag.

| Rolle | Person / Organisation |
|---|---|
| Auftraggeber | Dr. Philipp Pfeifer, Universität Graz |
| Kooperation | Georg Vogeler, Bernhard Bauer (ZIM Graz) |
| Auftragnehmer | Digital Humanities Craft OG |
| Operative Kommunikation | Christian Steiner (office@dhcraft.org) |

Budget: 2.000 € netto pauschal. SAP-Bestellnummer per 21.03. noch offen.

## Arbeitsphasen

### Phase 1 – Dokumentation & Klärung ✓

- [x] Probeseite vollständig analysiert (13 Tabellen, 3 Farben, 14 Glossen)
- [x] Research Vault aufgebaut (11 Dokumente)
- [x] Architekturentscheidung: TEI-XML kanonisch, JSON abgeleitet

### Phase 2 – Datenaufbereitung (AP1) ✓

- [x] `parse_probeseite.py`: DOCX → Python-Zwischenformat
- [x] `classify_layers.py`: Sprachwechsel, Segment-Verkettung
- [x] `build_tei.py`: → `data/tei/psalm2.xml` (770 Zeilen)
- [x] `tei_to_json.py`: → `data/processed/psalm2.json` (1.211 Zeilen, 92 Sections inkl. 14 inline Glossen)
- [x] `validate_tei.py`: TEI-Validierung gegen RelaxNG

### Phase 3 – Interface (AP2) ✓

- [x] 3-Panel-Layout (Quellen | Haupttext | Facsimile)
- [x] 6 Toggles + Keyboard-Shortcuts
- [x] Quellenapparat mit Sigle-Filtern
- [x] IIIF-Viewer mit Text-Bild-Synopse (Seiten-Ebene)
- [x] Psalmtext-Vergleich (5 Zeugen) als Tab
- [x] Wiener Notker als Tab
- [x] URL-Persistenz (Hash-Fragment für Deep Links)
- [x] Async JSON-Fetch mit file://-Fallback

### Phase 4 – Übergabe Iteration 1 ✓

- [x] ReadMe.md geschrieben
- [x] Knowledge Vault synchronisiert
- [x] Push auf GitHub und GitHub Pages aktiviert
- [x] Übergabe an Philipp (Briefing 23.03.2026)

### Phase 5 – Iteration 2 (Pfeifer-Review) ✓

Nach Pfeifer-Review (15.04.2026) mit ~20 Textkorrekturen, 6 Bugs und 4
Architektur-Wünschen:

- [x] **Errata-Refactor**: Korrekturen als Pipeline-Normalisierung statt YAML-Layer
  (`PFEIFER_CORRECTIONS` in `parse_probeseite.py`, 779 Zeilen Layer-Code entfernt)
- [x] **Slot-System (US-8)**: drei konfigurierbare Slots, 10-Eintrag-Pool,
  Schließen + Wiederherstellen, URL-Hash mit `slots=A:sources,B:edition,C:facsimile`
- [x] **Zeilengetreue nhd. Übersetzung (US-9)**: TEI `<lg type="line-faithful">`,
  Edition zeigt nhd. zeilengenau, Pool nhd. zeigt Fließtext mit aufgelösten
  Bindestrichen
- [x] **Psalter-Filter (US-10)** mit R-Disambiguierung: G/R/H als Filter-Layer,
  R semantisch separiert (Romanum vs. Remigius nach Section-Type)
- [x] **Datenqualität**: Cross-Verse-Hyphen via `@part`-Verkettung, Whitespace-
  Normalisierung, `line_n` pro Section
- [x] 29/29 Pipeline-Tests grün, 0 Warnings, 0 Errors

Vollständig in [[Anforderungen-Iteration-2]] dokumentiert, Branch
`iteration-2-pfeifer-review` (10 Commits ahead von origin), nicht gepusht.

### Phase 6 – Übergabe Iteration 2 ← aktuell

- [ ] Push + PR gegen `main`
- [ ] Pfeifer-Mail (Draft in [[Pfeifer-Mail-Iteration-2a]])
- [ ] Videocall: Augustinus-2-Nachreichungen V3-5/V6, R-Disambiguierung
  bestätigen, Handschriften-Zeilenumbrüche der CSg 0021

## Offene Punkte (niedrige Priorität)

| Frage | Status |
|---|---|
| Querverweise auf Bibelstellen (US-7.1) | Daten fehlen, Platzhalter im Datenmodell |
| SAP-Bestellnummer | Administrativ, kein Entwicklungsblocker |
| Vers→Seite-Mapping verifizieren | Vorläufig, gegen Facsimile prüfen |
| Echte Handschriften-Zeilenumbrüche der CSg 0021 | Aktuell nur über DOCX-Tabellenzeilen abgeleitet |

## Verknüpfungen

- [[Probeseite Analyse]] — Quellenanalyse
- [[Domänenwissen]] — Textschichten, Siglen
- [[Anforderungen]] — User Stories
- [[Design]] — UI-Konzept
- [[Technik]] — Pipeline, TEI-Modell, JSON-Schema
- [[Journal]] — Chronologie
