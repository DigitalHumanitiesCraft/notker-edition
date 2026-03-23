---
type: plan
created: 2026-03-23
updated: 2026-03-23
status: active
tags: [digital-humanities, notker, research-plan]
---

# Research Plan: Notker Psalmenkommentar – Digitaler Prototyp

## Projektkontext

Prototyp einer digitalen Edition von Notkers Psalmenkommentar (Notker III. von St. Gallen, ca. 950–1022). Demonstrationsobjekt: Psalm 2 (13 Verse). Zweck: funktionsfähiger Proof of Concept für Gutachter eines Drittmittelantrags.

| Rolle | Person / Organisation |
|---|---|
| Auftraggeber | Dr. Philipp Pfeifer, Institut für Germanistik, Universität Graz |
| Kooperation | Georg Vogeler, Bernhard Bauer (ZIM Graz) |
| Auftragnehmer | Digital Humanities Craft OG |
| Operative Kommunikation | Christian Steiner (office@dhcraft.org) |

Budget: 2.000 € netto pauschal (Angebot Nr. 11/26). Geschätzter Aufwand: 11–16 Stunden.
Abrechnung: SAP-Bestellung über Dekanat Uni Graz — SAP-Nummer per 21.03. noch offen.

## Stand des Wissens

Siehe [[Probeseite Analyse]] für die vollständige Quellenanalyse.

### Gesicherte Erkenntnisse

1. **Primärdatenquelle:** Philipps Probeseite enthält alle 13 Verse vollständig aufbereitet.
2. **Dreischichtiges Textmodell.** Psalmzitation / Übersetzung / Kommentar (funktional, nicht sprachbasiert).
3. **TEI-XML ist kanonisch.** Vollständige TEI-Edition liegt vor (`data/tei/psalm2.xml`, 764 Zeilen). JSON wird daraus abgeleitet.
4. **Quellenapparat vollständig.** 4 gesicherte + 2 ungeklärte Siglen. Lat. + dt. Übersetzung.
5. **IIIF verifiziert.** Manifest v2 funktioniert. Seite 11 = Beginn Psalm 2.
6. **UI steht.** Editions-Interface mit 6 Toggles, Quellenapparat, IIIF-Viewer, Text-Bild-Synopse.

### Ungeklärte Fragen

| Frage | Priorität | Selbst lösbar? |
|---|---|---|
| Siglen RII, N | Niedrig | Ja — als "ungeklärt" markiert, für Prototyp ausreichend |
| H in Siglen-Spalte | Niedrig | Ja — textkritische Zuordnung (Hebraicum), ableitbar aus Psalmtext-Vergleich |
| G, R in Siglen-Spalte | Niedrig | Ja — markieren Psalmtext-Version, ableitbar |
| Querverweise auf Bibelstellen | Mittel | Nein — Daten fehlen, Platzhalter im UI |
| SAP-Bestellnummer | Administrativ | Irrelevant für Entwicklung |

## Arbeitsphasen

### Phase 1 – Dokumentation & Klärung ✓

- [x] Probeseite vollständig analysiert
- [x] Research Vault aufgebaut (9 Dokumente)
- [x] Repository-Struktur bereinigt
- [x] Architekturentscheidung: TEI-XML kanonisch

### Phase 2 – Datenaufbereitung (AP1) ✓

- [x] `parse_probeseite.py` (717 Z.): DOCX → Zwischenformat
- [x] `classify_layers.py` (371 Z.): Sprachwechsel, Segment-Verkettung
- [x] `build_tei.py` (577 Z.): → `data/tei/psalm2.xml` (764 Z.)
- [x] Alle 13 Verse, Quellen, Glossen, Psalmtext-Vergleich, Wiener Notker
- [ ] `tei_to_json.py`: TEI → JSON für Web-UI (fehlt)

### Phase 3 – Interface (AP2) ← aktuell

- [x] Multi-Panel-Layout (Quellen | Haupttext | Facsimile)
- [x] 6 Toggles (Psalmzitat, Übersetzung, Kommentar, Glossen, nhd., lat./ahd.-Split)
- [x] Quellenapparat mit Sigle-Filtern und farbigen Seitenstreifen
- [x] IIIF-Viewer (OpenSeadragon, Manifest eingebunden)
- [x] Text-Bild-Synopse (Vers-Klick → korrekte MS-Seite)
- [x] Keyboard-Shortcuts, Drag-to-Resize, Responsive Breakpoints
- [ ] Echte Daten laden (Verse 4–13 sind Stubs, warten auf `tei_to_json.py`)
- [ ] Feinschliff: Psalmtext-Vergleich als Tab, Wiener Notker als Tab

### Phase 4 – Übergabe (AP3)

- [x] ReadMe.md geschrieben
- [ ] Deployment auf GitHub Pages aktivieren
- [ ] Push auf Remote
- [ ] Übergabe an Philipp

## Kritischer Pfad

```
tei_to_json.py (fehlt) ──→ Echte Daten im UI ──→ Feinschliff ──→ Deploy ──→ Übergabe
```

## Verknüpfungen

- [[Probeseite Analyse]] — Quellenanalyse
- [[Domänenwissen]] — Textschichten, Siglen
- [[Anforderungen]] — User Stories
- [[Design]] — UI-Konzept
- [[Technik]] — Pipeline, TEI-Modell, JSON-Schema
- [[Journal]] — Chronologie
