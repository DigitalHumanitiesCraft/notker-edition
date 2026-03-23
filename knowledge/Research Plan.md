---
type: plan
created: 2026-03-23
updated: 2026-03-23
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

### Phase 4 – Übergabe (AP3) ← aktuell

- [x] ReadMe.md geschrieben
- [x] Knowledge Vault synchronisiert
- [ ] Push auf GitHub
- [ ] GitHub Pages aktivieren (Settings → Pages → Source: main, Folder: /)
- [ ] Übergabe an Philipp

## Offene Punkte (niedrige Priorität)

| Frage | Status |
|---|---|
| Querverweise auf Bibelstellen | Daten fehlen, Platzhalter im Datenmodell |
| SAP-Bestellnummer | Administrativ, kein Entwicklungsblocker |
| Vers→Seite-Mapping verifizieren | Vorläufig, gegen Facsimile prüfen |
| Trailing Hyphen an Vers-Grenze (V1 sec[12]) | Bekannte Limitation, TEI-Strukturproblem |
| Farbüberlagerung Textschicht × Quellenfilter (D-11) | Am Bildschirm zu testen |

## Verknüpfungen

- [[Probeseite Analyse]] — Quellenanalyse
- [[Domänenwissen]] — Textschichten, Siglen
- [[Anforderungen]] — User Stories
- [[Design]] — UI-Konzept
- [[Technik]] — Pipeline, TEI-Modell, JSON-Schema
- [[Journal]] — Chronologie
