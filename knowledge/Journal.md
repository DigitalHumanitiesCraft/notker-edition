---
type: journal
created: 2026-02-24
updated: 2026-03-23
tags: [notker, project-log]
---

# Journal: Notker Psalmenkommentar Prototyp

## 2026-02-24 – Erstgespräch und Exploration

Philipp Pfeifer (Germanistik, Uni Graz) hat uns via Georg Vogeler und Bernhard Bauer (ZIM Graz) kontaktiert. Ziel: funktionsfähiger Prototyp für Gutachter.

Siehe [[2026-02-24 Erstgespräch]] für die vollständige Gesprächsnotiz.

**Entscheidungen:**
- Psalm 2 als Demonstrationsobjekt
- Statische Seite statt Backend
- JSON statt TEI-XML für den Prototyp *(später revidiert, siehe 23.03.)*

## 2026-02-27 – Angebot versendet

Angebot Nr. 11/26: 2.000 € netto pauschal. Drei Arbeitspakete. Leistungszeitraum 2–3 Wochen nach Dateneingang.

## 2026-03-21 – Datenlieferung durch Philipp

**Korrektur:** Finale Datenlieferung war 21.03., nicht 27.02. Die früheren Materialien (ANNIS-Scrape, PDFs) waren Vorablieferungen.

Philipps E-Mail enthielt:
- `Probeseite_Notker.docx` — vollständige Aufbereitung Psalm 2
- Feature-Wünsche: drei Toggles, Querverweise, Farbsemantik
- Facsimile-Einstieg bestätigt: CSg 0021, Seite 11
- Probeseite war für physische Publikation gedacht (erklärt hohe Qualität)

## 2026-03-23 – Bestandsanalyse und Vault-Konsolidierung

Probeseite erstmals vollständig maschinell geparst (python-docx, Run-Level-Farbanalyse).

**Zentrale Befunde:**
1. Farbcodierung = **Textfunktion**, nicht Sprache (olive/grün/schwarz = Psalmzitat/Übersetzung/Kommentar)
2. **14 Interlinearglossen** identifiziert
3. Siglen-Doppelbelegung komplexer als angenommen (G, R auch in Haupttext-Siglen)
4. Drei überlagernde Farblogiken (Handschrift / Probeseite / UI)
5. 13 Tabellen in drei funktionalen Gruppen entschlüsselt

**Entscheidungen:**
- Research Vault in `knowledge/` konsolidiert (10 → 9 Dokumente)
- Probeseite ist Primärdatenquelle

## 2026-03-23 – Architekturentscheidung: TEI-XML kanonisch

**Revidierte Entscheidung vom 24.02.:** TEI-XML ersetzt JSON als kanonisches Format. JSON wird aus TEI abgeleitet.

**Begründung:** TEI ermöglicht Sprachwechsel-Annotation (`<foreign>`), zeilenübergreifende Segmentverkettung (`@part`/`@next`/`@prev`), Silbentrennung (`<lb break="no"/>`), textkritischen Apparat (`<app>`/`<rdg>`) und akademische Zitierfähigkeit. Für das Gesamtprojekt (150 Psalmen) ist TEI ohnehin vorgesehen.

**Umgesetzt:**
- Pipeline: `parse_probeseite.py` → `classify_layers.py` → `build_tei.py`
- Output: `data/tei/psalm2.xml` (764 Zeilen, alle 13 Verse, vollständiger Apparat)
- Legacy JSON-Pipeline entfernt

## 2026-03-23 – Editions-Interface gebaut

`docs/index.html` (1.242 Zeilen), Single-File für GitHub Pages.

**Umgesetzt:**
- 3-Panel-Layout (Quellen | Haupttext | Facsimile) mit Drag-to-Resize
- 6 Toggles mit Keyboard-Shortcuts (1–4, N, L)
- Quellenapparat mit farbigen Sigle-Filtern
- IIIF-Viewer (OpenSeadragon, Manifest verifiziert)
- Text-Bild-Synopse: Vers-Klick navigiert Facsimile zur MS-Seite
- Psalm-Navigationsleiste (1–150)
- Designentscheidungen D-1 bis D-4 gelöst (Inline-Glossen, nhd. unterhalb, individuelle Quellenfarben, Gentium Book Plus)

**Offen:** Echte Daten für Verse 4–13 (warten auf `tei_to_json.py`)

## 2026-03-23 – Knowledge Vault Refactoring

`Technik.md` und `implementation.md` zu einem Dokument zusammengeführt (TEI + JSON + Pipeline + Web-Stack). Broken Link in Anforderungen.md gefixt. Research Plan auf aktuellen Stand gebracht. Journal aktualisiert.

Vault-Struktur: **9 Dokumente**, keine Redundanzen.

## 2026-03-23 – Pipeline komplett, UI mit echten Daten

`tei_to_json.py` gefixt (Vers-Gruppierung, Silbentrennung-Merge), regeneriert: 79 Sections, 14 Glossen, 31 Quellen. UI auf async Fetch umgestellt (Fallback auf eingebettete Demo-Daten für file://).

URL-Persistenz implementiert: Zustand als Hash-Fragment kodiert. Gutachter können Deep Links auf bestimmte Verse mit bestimmter Toggle-Konfiguration teilen.

EVT-Abgrenzung als Kommentarblock im HTML dokumentiert (orthogonale Schichtentrennung, persistentes Quellen-Panel, Single-File).

**Hinweis für Übergabe:** Alvite-Díez (2025), *Int. J. Digital Humanities*, schlägt einen Evaluationsrahmen für UI-Qualität digitaler Editionen vor (Dimensionen: Informationsarchitektur, Navigation, Interaktion, visuelle Gestaltung, Zugänglichkeit). Nützlich als Checkliste vor der Übergabe an Philipp.

## Offene Fragen

### Nächste Schritte
- [x] ~~`tei_to_json.py` schreiben~~ → fertig, Vers-Gruppen + Hyphenation gefixt
- [x] ~~Echte Daten ins UI laden~~ → async Fetch mit Fallback
- [x] ~~URL-Persistenz~~ → Hash-Fragment-Encoding
- [ ] Vers→Seite-Mapping gegen Facsimile verifizieren
- [ ] GitHub Pages aktivieren und deployen
- [ ] Übergabe an Philipp

### Mit Philipp zu klären (niedrige Priorität)
- [ ] Querverweise auf Bibelstellen: welche Daten existieren?
- [ ] SAP-Bestellnummer

## Verknüpfungen

- [[Research Plan]] — Gesamtplan
- [[Probeseite Analyse]] — Quellenanalyse
- [[Technik]] — Pipeline und Datenmodell
