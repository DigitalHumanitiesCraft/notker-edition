---
title: "Journal — Notker Psalmenkommentar Prototyp"
project:
  name: "notker-edition"
  repository: "https://github.com/DigitalHumanitiesCraft/notker-edition"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/excellence/blog/Promptotyping"
status: draft
version: "0.2"
created: 2026-02-24
updated: 2026-05-09
language: de
authors:
  - "Christopher Pollin"
generated-with: "Claude (Anthropic)"
related:
  - "[[INDEX]]"
  - "[[project]]"
  - "[[specification]]"
  - "[[offene-korrekturen]]"
---

# Journal — Notker Psalmenkommentar Prototyp

## 2026-02-24 — Erstgespräch und Exploration

Erstgespräch (Videokonferenz) mit dem Auftraggeber (Institut für Germanistik, Universität Graz). Kontakt über ZIM Graz. Ziel: Testseite als Proof of Concept für Drittmittelantrag.

**Vision Auftraggeber:** Haupttext (ahd./lat. gemischt) mit selektiv einblendbaren Sekundärquellen (Augustinus, Cassiodor u.a.), Toggle für lat./dt. Trennung, Quellenverlinkung auf Satzebene, nhd. Übersetzung daneben. Nutzer/in wählt selbst, was sichtbar sein soll.

**Datenlage:**
- Haupttext: gedruckte Editionen (1970er), kaum OCR-fähig; digital im Referenzkorpus Altdeutsch (ReA) auf ANNIS
- Sekundärquellen: nur Buch/PDF, Zuordnung über Psalm + Vers, Liste unvollständig

**Einschätzung Digital Humanities Craft:** Interface ist klassisches TEI-Projekt; Kernproblem ist Datenaufbereitung/-modellierung. TEI-XML als Single Source of Truth empfohlen.

**Vereinbart:** Auftraggeber liefert Requirements-Dokument, Psalm-Auswahl und PDF mit Sekundärquellen + Zuordnungserklärung. Digital Humanities Craft liefert dann Kostenvoranschlag.

**Entscheidungen:**
- Psalm 2 als Demonstrationsobjekt
- Statische Seite statt Backend
- JSON statt TEI-XML für den Prototyp (später revidiert, siehe 2026-03-23)

## 2026-02-27 — Angebot versendet

Pauschal-Angebot, drei Arbeitspakete, Leistungszeitraum 2–3 Wochen nach Dateneingang.

## 2026-03-21 — Datenlieferung

Finale Datenlieferung. Die früheren Materialien (ANNIS-Scrape, PDFs) waren Vorablieferungen.

Die Lieferung enthielt: `Probeseite_Notker.docx` (vollständige Aufbereitung Psalm 2), Feature-Wünsche (drei Toggles, Querverweise, Farbsemantik), Facsimile-Einstieg bestätigt (CSg 0021, Seite 11). Probeseite war für physische Publikation gedacht — erklärt die hohe Qualität.

## 2026-03-23 — Bestandsanalyse und Vault-Konsolidierung

Probeseite erstmals vollständig maschinell geparst (python-docx, Run-Level-Farbanalyse).

**Zentrale Befunde:**
1. Farbcodierung = Textfunktion, nicht Sprache (olive/grün/schwarz = Psalmzitat/Übersetzung/Kommentar)
2. Interlinearglossen im Textfluss identifiziert
3. Siglen-Doppelbelegung komplexer als angenommen (G, R auch in Haupttext-Siglen)
4. Drei überlagernde Farblogiken (Handschrift / Probeseite / UI)
5. Tabellen in drei funktionalen Gruppen entschlüsselt

**Entscheidungen:** Research Vault in `knowledge/` konsolidiert; Probeseite ist Primärdatenquelle.

## 2026-03-23 — Architekturentscheidung: TEI-XML kanonisch

Revidierte Entscheidung vom 2026-02-24: TEI-XML ersetzt JSON als kanonisches Format. JSON wird aus TEI abgeleitet.

**Begründung:** TEI ermöglicht Sprachwechsel-Annotation (`<foreign>`), zeilenübergreifende Segmentverkettung (`@part`/`@next`/`@prev`), Silbentrennung (`<lb break="no"/>`), textkritischen Apparat (`<app>`/`<rdg>`) und akademische Zitierfähigkeit. Für das Gesamtprojekt (150 Psalmen) ist TEI ohnehin vorgesehen.

Umgesetzt: Pipeline `parse_probeseite.py` → `classify_layers.py` → `build_tei.py`; Output `data/tei/psalm2.xml` (alle 13 Verse, vollständiger Apparat); Legacy-JSON-Pipeline entfernt.

## 2026-03-23 — Editions-Interface gebaut

`docs/index.html`, Single-File für GitHub Pages. 3-Panel-Layout (Quellen | Haupttext | Facsimile) mit Drag-to-Resize, Toggles mit Keyboard-Shortcuts (1–4, N, L), Quellenapparat mit farbigen Sigle-Filtern, IIIF-Viewer (OpenSeadragon, Manifest verifiziert), Text-Bild-Synopse (Vers-Klick navigiert Facsimile zur MS-Seite), Psalm-Navigationsleiste (1–150). Designentscheidungen D-1 bis D-4 gelöst (Inline-Glossen, nhd. unterhalb, individuelle Quellenfarben, Gentium Book Plus).

## 2026-03-23 — Pipeline komplett, UI mit echten Daten

`tei_to_json.py` gefixt (Vers-Gruppierung, Silbentrennung-Merge). UI auf async Fetch umgestellt (Fallback auf eingebettete Demo-Daten für file://). URL-Persistenz implementiert: Zustand als Hash-Fragment kodiert. Gutachter können Deep Links auf bestimmte Verse mit bestimmter Toggle-Konfiguration teilen. EVT-Abgrenzung als Kommentarblock im HTML dokumentiert (orthogonale Schichtentrennung, persistentes Quellen-Panel, Single-File).

## 2026-03-23 — UI-Bugs gefixt, Features ergänzt, Doku synchronisiert

UI-Fixes: Glossen-Positionierung (nach Sections statt Heuristik), Farbkontrast Kommentar/Übersetzung erhöht, Psalm-Navigation minimalistisch, Facsimile-Button beschriftet, Quellen-Panel Vers-Gruppen-Label, Scroll-Indikator. Neue Features: Psalmtext-Vergleich als Tab (5 Zeugen tabellarisch), Wiener Notker als Tab (Paralleltext). Dokumentation gegen Code-Stand synchronisiert.

## 2026-03-23 — Pipeline-Verbesserungen, Design-Overhaul, IIIF-Fix

Umfassende Review und Überarbeitung.

Pipeline-Fixes (`tei_to_json.py`): Siglen-Parsing (Klammernotation `G [A, C]` korrekt als `["G", "A", "C"]` geparst), Bold-Preservation (`<hi rend="bold">` in Quellenzitaten als `<b>`-Tags im JSON erhalten), Gloss-Interleaving (Glossen an korrekter Position im Textfluss in die Sections-Liste eingefügt), nhd.-Übersetzungen in TEI bereinigt.

TEI-Korrekturen (`psalm2.xml`): `<facsimile>` auf 4 Surfaces erweitert, nhd.-Übersetzungsblöcke von eingesickertem Glossentext bereinigt.

UI/Design: „Handschrift ▶"-Button Positionierung gefixt, Facsimile per Default geöffnet, IIIF-Seitenzuordnung korrigiert (Canvas-Offset +4 für Vorsatzblätter), Kommentar-Farbe verdunkelt, Glossen im Split-View spannen beide Spalten, Quellenapparat mit Sigle-Chips und Trennlinie, Vers-Active-State mit Terracotta-Akzentlinie, Footer-Zitierformat, Psalm-Nav-Kontrast erhöht.

## 2026-04-15 — Iteration 2 (Review-Einarbeitung)

Review durch den Auftraggeber mit Textkorrekturen, Glossen-Fehlklassifikation V6, drei Bugs (Split-Toggle, Scroll, ×-Button) und vier Architektur-Wünschen (Dropdown-Panels, Zeilensynopse, Psalter-Layer, Kursiv-Konvention). Umsetzung auf Branch `iteration-2-pfeifer-review`.

Methodischer Wechsel: Manuelle TEI-Edits wären strukturelle Anti-Pattern (Re-Parse überschreibt sie). Phase A restrukturiert als testgetrieben.

**Phase A — Datenkorrektur und Blocker.** Textkorrekturen als YAML-Errata-Layer (`data/errata.yaml`, `scripts/apply_errata.py`), idempotent und audit-fähig mit Rationale-Konvention pro Regel. V6-Glossen-Reklassifikation via Heuristik-Erweiterung in `detect_gloss_line()`: Text mit `[...]` ist Haupttext, nicht Glosse. BUG-11.1 Split-Toggle: `renderVerses()` setzte State-Klassen bei DOM-Rebuild nicht. BUG-11.2 Scroll: Flex-Container-Kontext für `.sources-content` ergänzt. BUG-11.3 ×-Button: dedizierte `.sources-panel.collapsed`. Test-Infrastruktur ausgebaut.

**Phase B — Lesbarkeit.** BUG-11.4 Kontrast-Fade: `.sources-content`-`mask-image` entfernt. BUG-11.5 Kursiv-Konvention: Pipeline extrahiert `source_language` aus `<quote xml:lang>`, CSS `[data-source-language="la"]` → kursiv. US-1.3-Erweiterung: Toggle „Quellen-Übersetzung" (Taste Q, Default an).

**Phase C.1 — Psalter-Layer.** US-10.1: Filter-Gruppe „Psalter" mit G und H unter der „Quellen"-Gruppe, visuell differenziert. R wegen Sigel-Konflikt mit Remigius vorerst weggelassen.

## 2026-04-16 — Iteration 2b: Errata-Refactor, Slot-System, US-9 Zeilensynopse

Auslieferung der drei verbleibenden Architektur-Stories in einem Rutsch.

**Errata-Refactor.** YAML + Dataclass + Loader + Tests entfernt. Ersetzt durch eine einfache Liste `PFEIFER_CORRECTIONS: list[tuple[str, str]]` in `parse_probeseite.py` und einen Aufruf von `apply_corrections()` auf den fertigen TEI-String in `build_tei.py`. Pipeline jetzt linear: DOCX → parse → classify → build → normalize → write.

**US-8 Panel-Dropdowns.** Drei feste Panels durch konfigurierbare Slots ersetzt. Pool-Registry mit wählbaren Inhalten (sources, edition, nhd, wiener, psalter G/R/H, facsimile, notes, comparison). DOM-Knoten werden zwischen Slots verschoben (single-instance pool, Auto-Swap). Restore-Bar am unteren Rand. URL-Hash `slots=A:nhd,B:edition,C:psalter_g&closed=`.

Cleanup: Edition-Tabs (Edition/Comparison/Wiener) aus dem Editor entfernt — Wiener Notker und Psalmtext-Vergleich sind jetzt eigenständige Pool-Einträge.

**US-9 Zeilensynopse (nhd).** Pipeline schreibt zusätzlich `<lg type="line-faithful">` mit `<l>` pro line.nhd ins TEI; `tei_to_json.py` liefert `translation_nhd_lines: [str]`. Edition rendert die nhd. Übersetzung jetzt zeilengetreu (Trailing-Bindestriche bleiben). Pool-Eintrag „Nhd. Übersetzung" rendert denselben Inhalt als Fließtext mit aufgelösten Bindestrichen. Cross-line-Korrekturen greifen via TEI-String-Normalize.

**US-10.1 R-Sigle.** R im Psalter-Filter ergänzt mit explizitem Disambiguierungs-Tooltip („Sigle teilt sich mit Remigius im Quellenapparat"). Provisorisch bis zur Klärung durch den Auftraggeber.

Browser-Walkthrough mit Playwright: alle Slot-Operationen, Layer-Toggles, Vers-Klick-Sync, URL-Deep-Link, Cap-auf-2-geschlossene-Slots, Pool-Swap A↔C grün.

## 2026-04-16 — Iteration 2c: Follow-up

UI-Sauberkeit: Doppelter Render der Quellen-Filter-Gruppen behoben, Pool-Templates auf `width:100%; height:100%`, `<th>` im Psalmtext-Vergleich mit `z-index:2`, OSD-Viewer Re-Mount mit `viewport.applyConstraints(true)`.

Toolbar/Subheader: „Quellen-Übersetzung"-Toggle in den Quellen-Panel-Header verschoben, `ensurePoolVisible()`-Helper eingeführt, Filter-Gruppen nebeneinander statt untereinander, Toolbar-Labels „SCHICHTEN"/„ANZEIGE" entfernt.

Datenkorrekturen: `<l>`-Zeilen-Korrekturen mit erweiterten Patterns (matchen `<p>` und `<l>`-Kontexte); `redistribute_crossverse_nhd()` löst den Review-Befund „erlaubte es" erscheint bei V3 statt V1–2.

Navigation/Diagnose: Psalm-Nav-Einträge außer 2 als `disabled`; Diagnose-Konsole an V6-Reklassifikation angepasst; Leer-Hinweis im Verses-Panel mit „Alle Schichten einblenden"-Button.

Promptotyping-Vault: Neue `docs/vault.html` rendert alle knowledge-Dokumente client-seitig. `scripts/sync_vault.py` kopiert `knowledge/*.md` → `docs/vault/*.md` + `index.json`.

## 2026-04-21 — UI-Feinschliff und Vault-Refactor

Arbeit in zwei Strängen parallel: Frontend-Bugs aus laufender Review plus eine Aufräumrunde im Research Vault.

UI-Fixes (`docs/index.html`): Restore-Bar für geschlossene Slots aus dem fixierten Unterrand in die Top-Nav verschoben und mit „Ansicht zurücksetzen" zu einer `.header-view-controls`-Gruppe rechts geclustert. `resetLayout()` setzt jetzt den vollständigen Startzustand wieder her. Slot-Verhältnis auf 3 : 4 : 3 gesetzt. Psalter-Pool-Templates getrennt (`pool-psalter-G/R/H`). Quellen-Panel mit permanentem Header „Quellen zu Vers N" plus Hinweiszeile. Sigle-Chip CSS-Bug behoben (`color: inherit` statt `#fff`). Vers-Nummern: kleineres Font + `white-space: nowrap`. Intro-Details-Block aus Iteration 1 entfernt.

Vault-Refactor (`knowledge/`): Siglen-Tabellen vereinheitlicht (Domänenwissen Single Source of Truth, Editorial Guidelines nur TEI-IDs, Probeseite Analyse nur empirisches Vorkommen). Domänenwissen-Siglen klar in „gesichert" und „in Klärung" geteilt. Anforderungen-Iteration-2 von 461 auf 243 Zeilen gekürzt; Umsetzungsplan, Teststrategie und Stand pro Story in neue Datei `Iteration-2-Umsetzungsplan.md` ausgelagert. Pfeifer-Mail-Entwürfe nach `knowledge/_drafts/`. Technik um Begründungs-Sätze pro Pipeline-Schritt angereichert.

Neuer Befund (`offene-korrekturen` 2.4): Die DOCX enthält 58 inhaltliche Fußnoten, die aktuell von `parse_probeseite.py` nicht ausgelesen werden.

Seiten-Mapping um −1 korrigiert: Vers→Seite jetzt V1–3 = S. 10, V4–6 = S. 11, V7–9 = S. 12, V10–13 = S. 13. Angepasst in `docs/index.html`, `scripts/tei_to_json.py`, `scripts/build_tei.py`, mehreren Knowledge-Dokumenten und `docs/methode.html`. Pipeline regeneriert, Tests grün.

Fußnoten-Integration (nachträglich am selben Tag): Parser, TEI-Emission, JSON-Ableitung und Frontend-Darstellung komplett durchgezogen. Neuer Run-Feld `footnote_refs`, neue Dataclass `Footnote`. TEI-Emission als `<note type="editorial" n="N" resp="#pfeifer"><label>anchor</label>body</note>` (`<label>`-Kind ist die Schema-konforme Alternative zu `@corresp`, das auf `<note>` nicht erlaubt ist). JSON: `verse.footnotes: [...]` und `source.footnotes`. UI: Fußnoten-Liste unterhalb des Vers-Grids und unter den betreffenden Quelleneinträgen. Bilanz: 53 von 58 Fußnoten landen an Haupttext-Zeilen, 3 an Quelleneinträgen, 2 in Strukturen, die der aktuelle Parser nicht abdeckt. 29/29 Pipeline-Tests grün.

## 2026-05-09 — Knowledge-Vault-Refactor auf Konvention v0.2

Refactor des `knowledge/`-Ordners auf [[Konvention Promptotyping Documents]] (Stand 2026-05-09 nach HerData `13f9880`). Repo-weite Schema-Version `0.2`.

Datei-Operationen: `Research Plan.md` → `project.md`. `Domänenwissen.md` + `Probeseite Analyse.md` → konsolidiert in `data.md`. `Anforderungen.md` + `Anforderungen-Iteration-2.md` + `Iteration-2-Umsetzungsplan.md` → konsolidiert in `specification.md`. `Design.md` → `design.md`. `Technik.md` → `architecture.md`. `Editionsrichtlinien.md` → `editorial-guidelines.md`. `Journal.md` → `journal.md`. `Offene Korrekturen.md` → `offene-korrekturen.md`. Neu angelegt: `INDEX.md` (Navigation und Begriffslexikon).

Frontmatter-Refactor: Pflichtkern (`title`, `project`, `method`, `status`, `version: 0.2`, `created`, `updated`); Empfehlungen (`language`, `authors`, `generated-with`, `topics` als Wikilinks, `related`); kontextabhängig (`knowledge-sources` als verschachteltes URI-Mapping in `project.md`, `data.md`, `architecture.md`, `editorial-guidelines.md`).

Inhaltlich keine Änderung an Substanz oder Entscheidungen — die Konsolidierungen erhalten die Iterations-Hierarchie und die Detail-Inhalte der Quelldokumente. Alte Cross-Links auf umbenannte Dokumente überall im Vault aktualisiert. `CLAUDE.md` im Repo-Root auf neue Dateinamen synchronisiert.

## Offene Punkte

### Nächste Schritte
- Augustinus-2-Korrekturen V3–5/V6 gegenprüfen lassen (Scroll-Bug ist gefixt)
- Videocall mit Auftraggeber: R-Sigle endgültig (Remigius vs. Romanum), Grundtext-Zeilenumbrüche der Handschrift (Daten oder Quelle dafür)
- Methoden-Paket (`docs/methode.html` stabilisieren + zitierbares PDF) für Antrag

### Bekannte Limitationen (Stand Iteration 2)
- Trailing Hyphen V7 `irgân-` (Versgrenze, TEI-Strukturproblem — unverändert seit Iteration 1, Low-Prio)
- `relates_to` in Glossen leer (TEI-Pipeline setzt kein `@target` — unverändert)
- Pre-existing TEI-Warnings in Pipeline: Versgrenzen-Silbentrennung + ein doppeltes Leerzeichen in Remigius V1–2 (nicht in der Review-Korrektur-Liste)

### Mit dem Auftraggeber zu klären
- Grundtext-Zeilenumbrüche der Handschrift (für US-9 Zeilensynopse)
- Siglen-Semantik G/R/H: textkritische Varianten oder Psalter-Quellen?
- R-Konflikt: Remigius vs. Romanum — wie im TEI disambiguiert?
- Kursiv-Konvention bestätigen
- Querverweise auf Bibelstellen: welche Daten existieren?

## Verknüpfungen

- [[INDEX]] — Navigation und Begriffslexikon
- [[project]] — Gesamtplan und Phasen
- [[data]] — Quellenanalyse und Probeseite-Strukturanalyse
- [[architecture]] — Pipeline und Datenmodell
- [[specification]] — Anforderungen, Entscheidungen und Stand pro Story
- [[offene-korrekturen]] — Tech-Debt-Tracker
