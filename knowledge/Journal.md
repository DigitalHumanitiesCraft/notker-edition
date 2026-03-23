---
type: journal
created: 2026-02-24
updated: 2026-03-23
tags: [notker, project-log]
---

# Journal: Notker Psalmenkommentar Prototyp

## 2026-02-24 – Erstgespräch und Exploration

Erstes Gespräch (Videokonferenz) mit Dr. Philipp Pfeifer (Germanistik, Uni Graz). Kontakt über [[Georg Vogeler]] und [[Bernhard Bauer]] (ZIM Graz). Ziel: Testseite als Proof of Concept für Drittmittelantrag.

**Vision Auftraggeber:** Haupttext (ahd./lat. gemischt) mit selektiv einblendbaren Sekundärquellen (Augustinus, Cassiodor u.a.), Toggle für lat./dt. Trennung, Quellenverlinkung auf Satzebene, nhd. Übersetzung daneben. Nutzer/in wählt selbst, was sichtbar sein soll.

**Datenlage:**
- Haupttext: gedruckte Editionen (1970er), kaum OCR-fähig; digital im Referenzkorpus Altdeutsch (ReA) auf ANNIS (167.583 Tokens, scrapebar)
- Sekundärquellen: nur Buch/PDF, Zuordnung über Psalm + Vers, Liste unvollständig

**Unsere Einschätzung:** Interface ist klassisches TEI-Projekt; Kernproblem ist Datenaufbereitung/-modellierung. TEI-XML als Single Source of Truth empfohlen. Budget-Hausnummer: 4.000–5.000 € für Prototyp.

**Vereinbart:** Auftraggeber liefert Requirements-Dokument, Psalm-Auswahl und PDF mit Sekundärquellen + Zuordnungserklärung. Wir liefern dann Kostenvoranschlag.

**Offene Punkte (historisch):** Förderlinie/Geldgeber unklar; Absprache mit ReA-Team (Karin Donhauser, HU Berlin) nötig; Urheberrecht an Textgestalt der 1970er-Edition klären.

**Entscheidungen:**
- Psalm 2 als Demonstrationsobjekt
- Statische Seite statt Backend
- JSON statt TEI-XML für den Prototyp *(später revidiert, siehe 23.03.)*

Vollständige Gesprächsnotiz war zuvor in eigenem Dokument; konsolidiert am 23.03.2026.

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
- Research Vault in `knowledge/` konsolidiert (10 → 8 Dokumente)
- Probeseite ist Primärdatenquelle

## 2026-03-23 – Architekturentscheidung: TEI-XML kanonisch

**Revidierte Entscheidung vom 24.02.:** TEI-XML ersetzt JSON als kanonisches Format. JSON wird aus TEI abgeleitet.

**Begründung:** TEI ermöglicht Sprachwechsel-Annotation (`<foreign>`), zeilenübergreifende Segmentverkettung (`@part`/`@next`/`@prev`), Silbentrennung (`<lb break="no"/>`), textkritischen Apparat (`<app>`/`<rdg>`) und akademische Zitierfähigkeit. Für das Gesamtprojekt (150 Psalmen) ist TEI ohnehin vorgesehen.

**Umgesetzt:**
- Pipeline: `parse_probeseite.py` → `classify_layers.py` → `build_tei.py`
- Output: `data/tei/psalm2.xml` (~780 Zeilen, alle 13 Verse, vollständiger Apparat)
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

Vault-Struktur: **8 Dokumente**, keine Redundanzen.

## 2026-03-23 – Pipeline komplett, UI mit echten Daten

`tei_to_json.py` gefixt (Vers-Gruppierung, Silbentrennung-Merge), regeneriert: 79 Sections, 14 Glossen, 31 Quellen. UI auf async Fetch umgestellt (Fallback auf eingebettete Demo-Daten für file://).

URL-Persistenz implementiert: Zustand als Hash-Fragment kodiert. Gutachter können Deep Links auf bestimmte Verse mit bestimmter Toggle-Konfiguration teilen.

EVT-Abgrenzung als Kommentarblock im HTML dokumentiert (orthogonale Schichtentrennung, persistentes Quellen-Panel, Single-File).

**Hinweis für Übergabe:** Alvite-Díez (2025), *Int. J. Digital Humanities*, schlägt einen Evaluationsrahmen für UI-Qualität digitaler Editionen vor (Dimensionen: Informationsarchitektur, Navigation, Interaktion, visuelle Gestaltung, Zugänglichkeit). Nützlich als Checkliste vor der Übergabe an Philipp.

## 2026-03-23 – UI-Bugs gefixt, Features ergänzt, Doku synchronisiert

8 UI-Fixes: Glossen-Positionierung (nach Sections statt Heuristik), Farbkontrast Kommentar/Übersetzung erhöht, Psalm-Navigation minimalistisch (1, [2], 3, ···, 50, 100, 150), Facsimile-Button beschriftet ("Handschrift ▶"), Quellen-Panel Vers-Gruppen-Label, Scroll-Indikator.

2 neue Features: Psalmtext-Vergleich als Tab (5 Zeugen tabellarisch), Wiener Notker als Tab (Paralleltext).

Dokumentation gegen Code-Stand synchronisiert: CLAUDE.md (komplett neu, 11 Docs + Dateistruktur), ReadMe.md (Architektur, lokale Nutzung, Erweiterbarkeit), Research Plan (alle Phasen 1–3 ✓), Technik.md (offene Fragen aktualisiert).

## 2026-03-23 – Pipeline-Verbesserungen, Design-Overhaul, IIIF-Fix

Umfassende Review und Überarbeitung:

**Pipeline-Fixes (tei_to_json.py):**
- Siglen-Parsing: Klammernotation `G [A, C]` wird korrekt als `["G", "A", "C"]` geparst
- Bold-Preservation: `<hi rend="bold">` in Quellenzitaten wird als `<b>`-Tags im JSON erhalten (23 Stellen)
- Gloss-Interleaving: 14 Glossen werden an ihrer korrekten Position im Textfluss in die Sections-Liste eingefügt (nicht mehr am Versende)
- nhd.-Übersetzungen in TEI bereinigt (Glossen-Leak aus DOCX-Parsing entfernt)

**TEI-Korrekturen (psalm2.xml):**
- `<facsimile>` auf 4 Surfaces erweitert (Seiten 11–14)
- nhd.-Übersetzungsblöcke von eingesickertem Glossentext bereinigt

**UI/Design:**
- "Handschrift ▶"-Button Positionierung gefixt (`right: 0` statt `left: -22px`)
- Facsimile per Default geöffnet (Gutachter sehen sofort Text + Handschrift)
- IIIF-Seitenzuordnung korrigiert: Canvas-Offset +4 für Vorsatzblätter (Seite 11 = Canvas 14)
- Kommentar-Farbe von `hsl(0,0%,52%)` auf `hsl(0,0%,35%)` verdunkelt (Notkers Stimme lesbar)
- Glossen im Split-View: spannen beide Spalten (`grid-column: 1/-1`)
- Split-View: `ahd_lat_mixed` nur in Ahd-Spalte (keine Duplikation)
- Quellenapparat: Sigle-Chips mit Farbe, Trennlinie lat./dt., Bold-Rendering via `safeBoldHtml()`
- Intro-Text gekürzt mit Handlungsanweisung für Gutachter
- Vers-Active-State: Terracotta-Akzentlinie links
- Footer: Zitierformat nach Konvention
- Psalm-Nav: Kontrast erhöht
- Unterseiten `richtlinien.html` und `methode.html` synchronisiert

**Dokumentation:** CLAUDE.md, Design.md, ReadMe.md, Journal.md aktualisiert.

## Offene Punkte

### Nächste Schritte
- [ ] Push auf GitHub
- [ ] GitHub Pages aktivieren
- [ ] Übergabe an Philipp

### Bekannte Limitationen
- ~~Vers→Seite-Mapping vorläufig~~ → **Gelöst** (Canvas-Offset +4, gegen Manifest verifiziert)
- Trailing Hyphen V7 `irgân-` (Versgrenze, TEI-Strukturproblem)
- Farbüberlagerung Textschicht × Quellenfilter (D-11, am Bildschirm testen)
- `relates_to` in Glossen leer (TEI-Pipeline setzt kein `@target`)

### Mit Philipp zu klären
- [ ] Querverweise auf Bibelstellen: welche Daten existieren?
- [ ] SAP-Bestellnummer

## Verknüpfungen

- [[Research Plan]] — Gesamtplan
- [[Probeseite Analyse]] — Quellenanalyse
- [[Technik]] — Pipeline und Datenmodell
