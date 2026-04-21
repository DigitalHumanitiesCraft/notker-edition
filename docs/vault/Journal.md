---
type: journal
created: 2026-02-24
updated: 2026-04-16
tags: [notker, project-log]
---

# Journal: Notker Psalmenkommentar Prototyp

## 2026-02-24 – Erstgespräch und Exploration

Erstgespräch (Videokonferenz) mit dem Auftraggeber (Institut für Germanistik, Universität Graz). Kontakt über ZIM Graz. Ziel: Testseite als Proof of Concept für Drittmittelantrag.

**Vision Auftraggeber:** Haupttext (ahd./lat. gemischt) mit selektiv einblendbaren Sekundärquellen (Augustinus, Cassiodor u.a.), Toggle für lat./dt. Trennung, Quellenverlinkung auf Satzebene, nhd. Übersetzung daneben. Nutzer/in wählt selbst, was sichtbar sein soll.

**Datenlage:**
- Haupttext: gedruckte Editionen (1970er), kaum OCR-fähig; digital im Referenzkorpus Altdeutsch (ReA) auf ANNIS
- Sekundärquellen: nur Buch/PDF, Zuordnung über Psalm + Vers, Liste unvollständig

**Einschätzung Digital Humanities Craft:** Interface ist klassisches TEI-Projekt; Kernproblem ist Datenaufbereitung/-modellierung. TEI-XML als Single Source of Truth empfohlen.

**Vereinbart:** Auftraggeber liefert Requirements-Dokument, Psalm-Auswahl und PDF mit Sekundärquellen + Zuordnungserklärung. Digital Humanities Craft liefert dann Kostenvoranschlag.

**Offene Punkte (historisch):** Förderlinie/Geldgeber unklar; Absprache mit ReA-Team (HU Berlin) nötig; Urheberrecht an Textgestalt der 1970er-Edition klären.

**Entscheidungen:**
- Psalm 2 als Demonstrationsobjekt
- Statische Seite statt Backend
- JSON statt TEI-XML für den Prototyp *(später revidiert, siehe 23.03.)*

## 2026-02-27 – Angebot versendet

Pauschal-Angebot, drei Arbeitspakete, Leistungszeitraum 2–3 Wochen nach Dateneingang.

## 2026-03-21 – Datenlieferung

**Korrektur:** Finale Datenlieferung war 21.03., nicht 27.02. Die früheren Materialien (ANNIS-Scrape, PDFs) waren Vorablieferungen.

Die Lieferung enthielt:
- `Probeseite_Notker.docx` — vollständige Aufbereitung Psalm 2
- Feature-Wünsche: drei Toggles, Querverweise, Farbsemantik
- Facsimile-Einstieg bestätigt: CSg 0021, Seite 11
- Probeseite war für physische Publikation gedacht (erklärt hohe Qualität)

## 2026-03-23 – Bestandsanalyse und Vault-Konsolidierung

Probeseite erstmals vollständig maschinell geparst (python-docx, Run-Level-Farbanalyse).

**Zentrale Befunde:**
1. Farbcodierung = **Textfunktion**, nicht Sprache (olive/grün/schwarz = Psalmzitat/Übersetzung/Kommentar)
2. Interlinearglossen im Textfluss identifiziert
3. Siglen-Doppelbelegung komplexer als angenommen (G, R auch in Haupttext-Siglen)
4. Drei überlagernde Farblogiken (Handschrift / Probeseite / UI)
5. Tabellen in drei funktionalen Gruppen entschlüsselt

**Entscheidungen:**
- Research Vault in `knowledge/` konsolidiert
- Probeseite ist Primärdatenquelle

## 2026-03-23 – Architekturentscheidung: TEI-XML kanonisch

**Revidierte Entscheidung vom 24.02.:** TEI-XML ersetzt JSON als kanonisches Format. JSON wird aus TEI abgeleitet.

**Begründung:** TEI ermöglicht Sprachwechsel-Annotation (`<foreign>`), zeilenübergreifende Segmentverkettung (`@part`/`@next`/`@prev`), Silbentrennung (`<lb break="no"/>`), textkritischen Apparat (`<app>`/`<rdg>`) und akademische Zitierfähigkeit. Für das Gesamtprojekt (150 Psalmen) ist TEI ohnehin vorgesehen.

**Umgesetzt:**
- Pipeline: `parse_probeseite.py` → `classify_layers.py` → `build_tei.py`
- Output: `data/tei/psalm2.xml` (alle 13 Verse, vollständiger Apparat)
- Legacy JSON-Pipeline entfernt

## 2026-03-23 – Editions-Interface gebaut

`docs/index.html`, Single-File für GitHub Pages.

**Umgesetzt:**
- 3-Panel-Layout (Quellen | Haupttext | Facsimile) mit Drag-to-Resize
- Toggles mit Keyboard-Shortcuts (1–4, N, L)
- Quellenapparat mit farbigen Sigle-Filtern
- IIIF-Viewer (OpenSeadragon, Manifest verifiziert)
- Text-Bild-Synopse: Vers-Klick navigiert Facsimile zur MS-Seite
- Psalm-Navigationsleiste (1–150)
- Designentscheidungen D-1 bis D-4 gelöst (Inline-Glossen, nhd. unterhalb, individuelle Quellenfarben, Gentium Book Plus)

**Offen:** Echte Daten für Verse 4–13 (warten auf `tei_to_json.py`)

## 2026-03-23 – Knowledge Vault Refactoring

`Technik.md` und `implementation.md` zu einem Dokument zusammengeführt (TEI + JSON + Pipeline + Web-Stack). Broken Link in Anforderungen.md gefixt. Research Plan auf aktuellen Stand gebracht. Journal aktualisiert.

## 2026-03-23 – Pipeline komplett, UI mit echten Daten

`tei_to_json.py` gefixt (Vers-Gruppierung, Silbentrennung-Merge). UI auf async Fetch umgestellt (Fallback auf eingebettete Demo-Daten für file://).

URL-Persistenz implementiert: Zustand als Hash-Fragment kodiert. Gutachter können Deep Links auf bestimmte Verse mit bestimmter Toggle-Konfiguration teilen.

EVT-Abgrenzung als Kommentarblock im HTML dokumentiert (orthogonale Schichtentrennung, persistentes Quellen-Panel, Single-File).

**Hinweis für Übergabe:** Alvite-Díez (2025), *Int. J. Digital Humanities*, schlägt einen Evaluationsrahmen für UI-Qualität digitaler Editionen vor (Dimensionen: Informationsarchitektur, Navigation, Interaktion, visuelle Gestaltung, Zugänglichkeit). Nützlich als Checkliste vor der Übergabe an den Auftraggeber.

## 2026-03-23 – UI-Bugs gefixt, Features ergänzt, Doku synchronisiert

UI-Fixes: Glossen-Positionierung (nach Sections statt Heuristik), Farbkontrast Kommentar/Übersetzung erhöht, Psalm-Navigation minimalistisch (1, [2], 3, ···, 50, 100, 150), Facsimile-Button beschriftet („Handschrift ▶"), Quellen-Panel Vers-Gruppen-Label, Scroll-Indikator.

Neue Features: Psalmtext-Vergleich als Tab (5 Zeugen tabellarisch), Wiener Notker als Tab (Paralleltext).

Dokumentation gegen Code-Stand synchronisiert: CLAUDE.md, ReadMe.md, Research Plan, Technik.md.

## 2026-03-23 – Pipeline-Verbesserungen, Design-Overhaul, IIIF-Fix

Umfassende Review und Überarbeitung:

**Pipeline-Fixes (tei_to_json.py):**
- Siglen-Parsing: Klammernotation `G [A, C]` wird korrekt als `["G", "A", "C"]` geparst
- Bold-Preservation: `<hi rend="bold">` in Quellenzitaten wird als `<b>`-Tags im JSON erhalten
- Gloss-Interleaving: Glossen werden an ihrer korrekten Position im Textfluss in die Sections-Liste eingefügt (nicht mehr am Versende)
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

## 2026-04-15 – Iteration 2 (Review-Einarbeitung)

Review durch den Auftraggeber mit Textkorrekturen, Glossen-Fehlklassifikation V6, drei Bugs
(Split-Toggle, Scroll, ×-Button) und vier Architektur-Wünschen (Dropdown-Panels,
Zeilensynopse, Psalter-Layer, Kursiv-Konvention). Umsetzung auf Branch
`iteration-2-pfeifer-review`.

**Methodischer Wechsel:** Manuelle TEI-Edits wären strukturelle Anti-Pattern (Re-Parse
überschreibt sie). Phase A restrukturiert: testgetrieben.

**Phase A: Datenkorrektur und Blocker**
- Textkorrekturen als YAML-Errata-Layer (`data/errata.yaml`, `scripts/apply_errata.py`).
  Idempotent, re-runbar, audit-fähig mit Rationale-Konvention pro Regel.
- V6-Glossen-Reklassifikation via Heuristik-Erweiterung in `detect_gloss_line()`:
  Text mit `[...]` ist Haupttext, nicht Glosse. Generisch, nicht V6-Spezialfall.
- BUG-11.1 Split-Toggle: `renderVerses()` setzte State-Klassen bei DOM-Rebuild nicht —
  jetzt `state.splitLanguages` am Element-Konstruktor.
- BUG-11.2 Scroll: `.sources-panel` fehlte Flex-Container-Kontext für `.sources-content`-
  Scroll.
- BUG-11.3 ×-Button: `.panel.collapsed` griff nie (Markup hat keine `.panel`-Klasse);
  dedizierte `.sources-panel.collapsed` + vervollständigte `.facsimile-panel.collapsed`.
- Test-Infrastruktur ausgebaut: Unit-Tests für Errata und Gloss-Heuristik;
  `scripts/test_pipeline.py` um Akzeptanz-Tests erweitert.
- Screenshots vorher/nachher via Playwright.

**Phase B: Lesbarkeit**
- BUG-11.4 Kontrast-Fade: `.sources-content` `mask-image` entfernt (Review-Befund:
  „Schrift schwächer bei V12–13"). Native Scrollbar als Indikator.
- BUG-11.5 Kursiv-Konvention: Pipeline extrahiert `source_language` aus `<quote xml:lang>`.
  CSS `[data-source-language="la"]` → kursiv, `[data-source-language="goh"]` → aufrecht.
  In Psalm 2 alle Quellen `la` — Konvention für spätere ahd.-Quellen dokumentiert.
- US-1.3-Erweiterung: Toggle „Quellen-Übersetzung" (Taste Q, Default an) im Toolbar.
  Blendet `.source-german` im Quellenapparat aus. URL-Hash `qnhd=0`.

**Phase C.1: Psalter-Layer**
- US-10.1: Filter-Gruppe „Psalter" mit G und H unter der existierenden „Quellen"-Gruppe.
  Visuell differenziert (gestrichelter Rahmen, grau-blaue Farbe).
- R in Psalter-Gruppe weggelassen wegen Sigel-Konflikt mit Remigius (patristisch) —
  wartet auf Klärung durch den Auftraggeber.

**Offen aus Iteration 2:**
- US-9 Zeilensynopse: **hart blockiert** durch fehlende Grundtext-Zeilenumbrüche der
  Handschrift. Input benötigt (Tax/Sehrt-Markierung oder Facsimile-Ableitung).
- Augustinus-2-Korrekturen V3–5/V6: konnten wegen BUG-11.2 nicht geprüft werden.
  Nach Phase-A-Merge kann nachgescrollt werden.

**Entscheidungen dokumentiert in** `knowledge/Anforderungen-Iteration-2.md`:
1. Panel-Modell Kompromiss (nur rechts Dropdown, Mitte fix)
2. Zeilensynopse via TEI-`<lb/>` aus DOCX-Bindestrichen geparst
3. Kursiv-Konvention (kursiv für lat., aufrecht für ahd.)
4. Siglen G/R/H provisorisch als Psalter-Zeugen mit `@cert="low"`
5. Research-Vault-Zugriff: kein Repo-Zugriff, Methoden-HTML/PDF als Ersatz

## 2026-04-16 – Iteration 2b: Errata-Refactor, Slot-System, US-9 Zeilensynopse

Auslieferung der drei verbleibenden Architektur-Stories in einem Rutsch:

**Errata-Refactor:** Das gesamte Errata-System entfernt. Statt YAML + dataclass + Loader + Tests
eine einfache Liste `PFEIFER_CORRECTIONS: list[tuple[str, str]]`
in `parse_probeseite.py` und ein Aufruf von `apply_corrections()`
auf den fertigen TEI-String in `build_tei.py`. Pipeline ist jetzt linear:
DOCX → parse → classify → build → normalize → write. Alle Korrekturen
weiterhin im finalen TEI; Tests grün.

**US-8 Panel-Dropdowns:** Drei feste Panels durch konfigurierbare
Slots ersetzt. Pool-Registry mit wählbaren Inhalten (sources, edition, nhd, wiener,
psalter G/R/H, facsimile, notes, comparison). DOM-Knoten werden zwischen
Slots verschoben (single-instance pool, Auto-Swap). Restore-Bar am unteren
Rand für geschlossene Slots. URL-Hash `slots=A:nhd,B:edition,C:psalter_g&closed=`.

**Cleanup:** Edition-Tabs (Edition/Comparison/Wiener) aus dem Editor entfernt —
Wiener Notker und Psalmtext-Vergleich sind jetzt eigenständige Pool-Einträge,
keine Tabs mehr nötig. switchTab() und renderWiener() weg.

**US-9 Zeilensynopse (nhd):** Pipeline schreibt zusätzlich `<lg type="line-faithful">`
mit `<l>` pro line.nhd ins TEI; tei_to_json.py liefert `translation_nhd_lines: [str]`.
Edition rendert die nhd. Übersetzung jetzt zeilengetreu (Trailing-Bindestriche
bleiben als Trennungsmarkierung). Pool-Eintrag „Nhd. Übersetzung" rendert
denselben Inhalt als Fließtext mit aufgelösten Bindestrichen
(„ver- gegangen" → „vergegangen"). Cross-line-Korrekturen (z. B. „mir, mein Sohn")
greifen via TEI-String-Normalize.

**US-10.1 R-Sigle:** R im Psalter-Filter ergänzt mit explizitem Disambiguierungs-
Tooltip („Sigle teilt sich mit Remigius im Quellenapparat"). Provisorisch
bis zur Klärung durch den Auftraggeber.

**Browser-Walkthrough mit Playwright:** alle Slot-Operationen,
Layer-Toggles, Vers-Klick-Sync, URL-Deep-Link, Cap-auf-2-geschlossene-Slots,
Pool-Swap A↔C grün.

**Stand der Branch `iteration-2-pfeifer-review`:** alle aus dem Review
adressierbaren Punkte umgesetzt. Offen nur, was extern blockiert ist
(Grundtext-Zeilenumbrüche der Handschrift, R-Disambiguierung-Klärung,
Augustinus-2-Nachreichungen V3–5/V6).

## 2026-04-16 – Iteration 2c: Follow-up-Screenshots

**UI-Sauberkeit**
- Doppelter Render der Quellen-Filter-Gruppen (Container wurde bei Re-Mount
  des sources-Pool nicht geleert). Fix in `renderSourceFilters()`.
- Pool-Templates (`sources-panel`, `facsimile-panel`, `text-panel`) hatten
  noch feste Pixel-Breiten aus Iteration 1 (`width:300px`, `max-width:450px`).
  Seit dem Slot-System von Iteration 2 sollten sie ihre Slot-Breite voll
  ausfüllen. Fix: `width:100%; height:100%`.
- `<th>` im Psalmtext-Vergleich bekam `z-index:2` + Box-Shadow, damit
  beim Scrollen keine Überlagerung mit Content entsteht.
- OSD-Viewer bekam beim Re-Mount `viewport.applyConstraints(true)`, damit
  die Handschrift nach einem Slot-Swap wieder rendert.

**Toolbar / Subheader**
- Toggle „Quellen-Übersetzung" (Taste Q) aus zentraler Toolbar in den
  Quellen-Panel-Header verschoben. Dort kontextuell sinnvoll.
- `ensurePoolVisible()`-Helper eingeführt: `toggleLayer()` öffnet den
  Edition-Slot wieder, `toggleSourceNhd()` öffnet den Quellen-Slot.
- Filter-Gruppen (`Quellen` + `Psalter`) stehen jetzt nebeneinander statt
  untereinander. `.sources-subheader` mit `.source-filters` zu einer
  einzigen Zeile gemerged. Aktions-Button via `margin-left:auto` rechts.
- Toolbar-Labels „SCHICHTEN"/„ANZEIGE" entfernt, Button-Padding/Font
  reduziert (0.72rem, 0.15/0.5rem padding).

**Datenkorrekturen aus dem Review**
- `<l>`-Zeilen-Korrekturen, die der Fließtext-Replace-Layer nicht
  erreichte: V7 „Mein Vater sagte zu mir," / V8–9 „dein Erbe." + „Stab,
  das ist" + „mit eisernem Stab," + „den Körper." Muster matchen jetzt
  sowohl `<p>` als auch `<l>`-Kontexte. `PFEIFER_CORRECTIONS` entsprechend
  erweitert.
- `redistribute_crossverse_nhd()` in `build_tei.py`: wenn die erste Zeile
  einer Versgruppe ein Cross-Verse-Fortsetzungs-Fragment ist (Heuristik:
  Vorgänger endet auf „-", aktueller Anfang kleingeschrieben), wandert
  die nhd-Übersetzung an das Ende der letzten nhd-Zeile des Vorgängers.
  Löst den Review-Befund „erlaubte es" erscheint bei V3 statt V1–2.

**Navigation / Diagnose**
- Psalm-Nav-Einträge außer 2 sind `disabled` (grau, `cursor:not-allowed`,
  Tooltip „noch nicht verfügbar").
- Diagnose-Konsole: Glossen-Erwartungswert an V6-Reklassifikation angepasst,
  bekannte V7-„irgân-"-Silbentrennung aus Warn-Liste gefiltert.
- Leer-Hinweis im Verses-Panel, wenn alle Schichten ausgeblendet
  sind, mit „Alle Schichten einblenden"-Button.

**Promptotyping-Vault**
- Neue `docs/vault.html` rendert alle knowledge-Dokumente mit
  `marked.js` client-seitig. Sidebar mit sortierter Dokumentliste,
  YAML-Frontmatter + Obsidian-Wikilinks werden beim Rendern bereinigt.
  Deep-Link via `?doc=Filename.md`. `scripts/sync_vault.py` kopiert
  `knowledge/*.md` → `docs/vault/*.md` + `index.json`.
- Links in Hauptnavigation und Footer ergänzt.

## 2026-04-21 – UI-Feinschliff und Vault-Refactor

Arbeit in zwei Strängen parallel: Frontend-Bugs aus laufender Review plus eine Aufräumrunde im Research Vault.

**UI-Fixes** (`docs/index.html`):
- Restore-Bar für geschlossene Slots aus dem fixierten Unterrand in die Top-Nav verschoben und mit „Ansicht zurücksetzen" zu einer `.header-view-controls`-Gruppe rechts geclustert.
- `resetLayout()` setzt jetzt den vollständigen Startzustand wieder her (State vor DOM, keine doppelten Renders): Slot-Zuweisung, Breiten, Layer-Toggles, nhd/Quellen-Übersetzung, Filter, aktiver Vers.
- Slot-Verhältnis auf 3 : 4 : 3 gesetzt — Notkers Text im Default breiter als die Flanken.
- Psalter-Pool-Templates getrennt (`pool-psalter-G/R/H`), damit mehrere Psalter-Zeugen gleichzeitig in verschiedenen Slots angezeigt werden können. Der gemeinsame Template-Knoten hatte das vorher verhindert.
- Quellen-Panel: permanenter Header „Quellen zu Vers N" plus Hinweiszeile zur Klick-Synchronisation. Empty-State zeigt, in welchen Versen eine gefilterte Sigle tatsächlich vorkommt (klickbare Sprünge).
- Sigle-Chip CSS-Bug behoben: `color: inherit` statt `color: #fff` auf `.sigle-chip`, damit `background: currentColor` die Farbe vom Kontext erbt (Elternteil oder Inline-Style) statt Weiß-auf-Weiß zu rendern.
- Vers-Nummern: kleineres Font + `white-space: nowrap`, damit Gruppen wie „12–13" nicht mehr umbrechen.
- Intro-Details-Block („Psalm 2 · Einführung · Bedienung") entfernt — war statisches HTML aus Iteration 1, kam nicht aus der Pipeline und stand seit dem Slot-System ohne Bezug im Notkers-Text-Panel.

**Vault-Refactor** (`knowledge/`):
- Siglen-Tabellen vereinheitlicht: `Domänenwissen.md` ist Single Source of Truth. `Editionsrichtlinien.md` führt jetzt nur die TEI-IDs, `Probeseite Analyse.md` nur das empirische Vorkommen; beide verweisen auf das Domänenwissen.
- Domänenwissen-Siglen klar in „gesichert" (A, C, Br, R; G, H, A-Psalter, C-Psalter) und „in Klärung" (RII, N, Haupttext-Spalte, R-Disambiguierung) geteilt.
- `Anforderungen-Iteration-2.md` von 461 auf 243 Zeilen gekürzt; Umsetzungsplan, Teststrategie und Stand pro Story in neue Datei `Iteration-2-Umsetzungsplan.md` ausgelagert.
- Pfeifer-Mail-Entwürfe nach `knowledge/_drafts/` verschoben (werden von `sync_vault.py` nicht mehr in den öffentlichen Vault kopiert).
- `Technik.md` um Begründungs-Sätze pro Pipeline-Schritt angereichert: warum vier Skripte, warum Farbextraktion auf Run-Ebene, warum zwei Datenformate nebeneinander, warum `<seg>` statt `<quote>` etc.
- `CLAUDE.md` mit den tatsächlichen Dokumenten im Vault synchronisiert, Hinweis auf `_drafts/` ergänzt.

**Neuer Befund (Offene Korrekturen 2.4):** Die DOCX enthält **58 inhaltliche Fußnoten** (Textzeugen-Varianten, Quellenzuschreibungen, Übersetzungsentscheidungen), die aktuell von `parse_probeseite.py` nicht ausgelesen werden und entsprechend weder im TEI noch im JSON noch in der UI erscheinen. Beispiel FN#1: „Der Zusatz PSALMVS DAVID, der in G und R in rot geschrieben ist, fehlt in H." Priorität hoch — inhaltlich genau die Art philologischer Annotation, die eine digitale Edition von einer DOCX-Abschrift unterscheidet.

**Seiten-Mapping um −1 korrigiert (am selben Tag):** UI-Beobachtung, dass Tax/Sehrt-R10 und Handschriftenseite 11 um eins auseinander lagen. Das frühere Mapping (Psalm-2-Beginn = HS-Seite 11) war mit der Edition-Seitenangabe R10 inkonsistent. Vers→Seite jetzt: V1–3 = S. 10, V4–6 = S. 11, V7–9 = S. 12, V10–13 = S. 13. Angepasst: `docs/index.html` (`VERSE_TO_PAGE`, Schema-Block, Demo-Fallback), `scripts/tei_to_json.py` (Metadata-URL), `scripts/build_tei.py` (`<facsimile>`-IIIF-URL), `knowledge/Domänenwissen.md`, `knowledge/Technik.md`, `docs/methode.html`. Pipeline regeneriert, Tests grün.

**Fußnoten-Integration (nachträglich am selben Tag):** Parser, TEI-Emission, JSON-Ableitung und Frontend-Darstellung komplett durchgezogen.

- Neuer Run-Feld `footnote_refs`, neue Dataclass `Footnote` mit `n`, `body`, `anchor_text`.
- `load_footnotes()` liest `word/footnotes.xml`, `get_cell_runs()` hängt leere Referenz-Runs an den vorhergehenden Anker-Run.
- TEI-Emission als `<note type="editorial" n="N" resp="#pfeifer"><label>anchor</label>body</note>` innerhalb des betreffenden `<ab>` bzw. `<cit>`. Erste Fassung mit `@corresp` schlug an RelaxNG an (nicht erlaubt auf `<note>`) — `<label>`-Kind ist die Schema-konforme Alternative.
- JSON: `verse.footnotes: [{n, anchor, body, line_n}]` und `source.footnotes` für Quellen-interne Anmerkungen.
- UI: Fußnoten-Liste unterhalb des Vers-Grids und unter den betreffenden Quelleneinträgen, je mit Nummer-Chip, Anker-Wort und Fließtext-Body. Stil bewusst unaufdringlich, damit das Haupttext-Grid nicht unterbrochen wird.
- Bilanz: 53 von 58 Fußnoten landen an Haupttext-Zeilen, 3 an Quelleneinträgen; 2 hängen in Strukturen, die der aktuelle Parser nicht abdeckt (Psalter-Header o. ä.) — gutartig, nicht blockierend.
- 29 / 29 Pipeline-Tests grün.

## Offene Punkte

### Nächste Schritte
- [ ] Augustinus-2-Korrekturen V3–5/V6 gegenprüfen lassen (Scroll-Bug ist gefixt)
- [ ] Videocall mit Auftraggeber: R-Sigle endgültig (Remigius vs. Romanum),
      Grundtext-Zeilenumbrüche der Handschrift (Daten oder Quelle dafür)
- [ ] Methoden-Paket (docs/methode.html stabilisieren + zitierbares PDF) für Antrag

### Bekannte Limitationen (Stand Iteration 2)
- Trailing Hyphen V7 `irgân-` (Versgrenze, TEI-Strukturproblem — unverändert seit
  Iteration 1, Low-Prio)
- `relates_to` in Glossen leer (TEI-Pipeline setzt kein `@target` — unverändert)
- Pre-existing TEI-Warnings in Pipeline: Versgrenzen-Silbentrennung + ein doppeltes
  Leerzeichen in Remigius V1–2 (nicht in der Review-Korrektur-Liste)

### Mit dem Auftraggeber zu klären
- [ ] Grundtext-Zeilenumbrüche der Handschrift (für US-9 Zeilensynopse)
- [ ] Siglen-Semantik G/R/H: textkritische Varianten oder Psalter-Quellen?
- [ ] R-Konflikt: Remigius vs. Romanum — wie im TEI disambiguiert?
- [ ] Kursiv-Konvention bestätigen
- [ ] Querverweise auf Bibelstellen: welche Daten existieren?

## Verknüpfungen

- [[Research Plan]] — Gesamtplan
- [[Probeseite Analyse]] — Quellenanalyse
- [[Technik]] — Pipeline und Datenmodell
- [[Anforderungen-Iteration-2]] — Iteration 2 Backlog, Entscheidungen, TDD-Plan
