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

| Rolle | Institution |
|---|---|
| Auftraggeber | Institut für Germanistik, Universität Graz |
| Kooperation | ZIM Graz |
| Umsetzung | Digital Humanities Craft |

## Arbeitsphasen

### Phase 1 – Dokumentation & Klärung

- [x] Probeseite vollständig analysiert (Farbcodierung, Glossen, Tabellenstruktur)
- [x] Research Vault aufgebaut
- [x] Architekturentscheidung: TEI-XML kanonisch, JSON abgeleitet

### Phase 2 – Datenaufbereitung (AP1)

- [x] `parse_probeseite.py`: DOCX → Python-Zwischenformat
- [x] `classify_layers.py`: Sprachwechsel, Segment-Verkettung
- [x] `build_tei.py` → `data/tei/psalm2.xml`
- [x] `tei_to_json.py` → `data/processed/psalm2.json`
- [x] `validate_tei.py`: TEI-Validierung gegen RelaxNG

### Phase 3 – Interface (AP2)

- [x] 3-Panel-Layout (Quellen | Haupttext | Facsimile)
- [x] Textschicht-Toggles + Keyboard-Shortcuts
- [x] Quellenapparat mit Sigle-Filtern
- [x] IIIF-Viewer mit Text-Bild-Synopse (Seiten-Ebene)
- [x] Psalmtext-Vergleich (5 Zeugen) als Tab
- [x] Wiener Notker als Tab
- [x] URL-Persistenz (Hash-Fragment für Deep Links)
- [x] Async JSON-Fetch mit file://-Fallback

### Phase 4 – Übergabe Iteration 1

- [x] ReadMe.md geschrieben
- [x] Knowledge Vault synchronisiert
- [x] Push auf GitHub und GitHub Pages aktiviert
- [x] Übergabe an Auftraggeber

### Phase 5 – Iteration 2 (Review-Einarbeitung)

Nach Review mit Textkorrekturen, Bugs und Architektur-Wünschen:

- [x] **Errata-Refactor**: Korrekturen als Pipeline-Normalisierung direkt im
  Parser (`PFEIFER_CORRECTIONS`), idempotent
- [x] **Slot-System**: drei konfigurierbare Slots mit Inhalts-Pool,
  Schließen + Wiederherstellen, URL-Hash-persistent
- [x] **Zeilengetreue nhd. Übersetzung**: TEI `<lg type="line-faithful">`,
  Edition zeigt nhd. zeilengenau, Pool nhd. zeigt Fließtext mit aufgelösten
  Bindestrichen
- [x] **Psalter-Filter** mit R-Disambiguierung: G/R/H als Filter-Layer,
  R semantisch separiert (Romanum vs. Remigius nach Section-Type)
- [x] **Datenqualität**: Cross-Verse-Hyphen via `@part`-Verkettung, Whitespace-
  Normalisierung, `line_n` pro Section
- [x] Multi-Psalm-Pipeline: Psalm-Parameter in Build-Scripts, Indices, Frontend-Hash
- [x] Research Vault öffentlich unter `/vault.html`

Branch gepusht, PR gegen `main` gemergt, auf GitHub Pages deployt.

### Phase 6 – Abnahme Iteration 2

- [ ] Review durch Auftraggeber auf der deployten Seite
- [ ] Augustinus-2-Nachreichungen V3-5/V6
- [ ] Bestätigung der R-Disambiguierungs-Heuristik
- [ ] Handschriften-Zeilenumbrüche der CSg 0021 klären (zeilengenauer Grundtext)

## Offene Punkte (niedrige Priorität)

| Frage | Status |
|---|---|
| Querverweise auf Bibelstellen (US-7.1) | Daten fehlen, Platzhalter im Datenmodell |
| Vers→Seite-Mapping verifizieren | Vorläufig, gegen Facsimile prüfen |
| Echte Handschriften-Zeilenumbrüche der CSg 0021 | Aktuell nur über DOCX-Tabellenzeilen abgeleitet |

## Verknüpfungen

- [[Probeseite Analyse]] — Quellenanalyse
- [[Domänenwissen]] — Textschichten, Siglen
- [[Anforderungen]] — User Stories
- [[Design]] — UI-Konzept
- [[Technik]] — Pipeline, TEI-Modell, JSON-Schema
- [[Journal]] — Chronologie
