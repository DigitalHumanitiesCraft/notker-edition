---
type: requirements
created: 2026-04-15
tags: [notker, requirements, iteration-2]
iteration: 2
baseline: "[[Anforderungen]]"
feedback-source: "Pfeifer 15.04.2026 (Mail + Google Doc)"
---

# Anforderungen: Notker Psalmenkommentar — Iteration 2

## Kontext

Iteration 1 live unter dhcraft.org/notker-edition, Übergabe-Briefing 23.03.2026. Auftraggeber-Review durch Philipp Pfeifer am 15.04.2026 mit strukturiertem Feedback (Architekturwünsche, Bugs, Textkorrekturen). Iteration 2 setzt das Review um, bevor das gesamte Konvolut an die Gutachter geht.

Iteration 1 definiert die Baseline: [[Anforderungen]] (Epics 1–7, US-1.1 bis US-7.1). Iteration 2 ergänzt Epics 8–11, erweitert US-1.2, US-1.3, US-2.2 und dokumentiert die Bug- und Korrektur-Backlogs.

## Epic 8 – Panel-Flexibilisierung (neu)

Pfeifer wünscht freie Belegung der drei Hauptbereiche (links, Mitte, rechts) aus einem Pool verfügbarer Inhalte statt der festen Rollenzuordnung Quellenapparat | Edition | Facsimile. Das bricht mit dem aktuellen Layout und ist die strukturell größte Änderung der Iteration.

**US-8.1** Als Forscher will ich pro Panel über ein Dropdown auswählen, welchen Inhalt ich dort sehe, damit ich meine Arbeitsansicht frei konfigurieren kann.

Akzeptanzkriterien:
- Drei Dropdowns im Panel-Header (links, Mitte, rechts).
- Inhaltstypen im Pool: Quellenapparat, Notkers Text (Edition), Nhd. Übersetzung, Wiener Notker, Psalter G, Psalter R, Psalter H, Handschrift Notker (Facsimile), Anmerkungen.
- Dropdown-Zustand in URL-Hash persistiert (`p=left:sources,center:edition,right:facsimile`).
- Default nach Erstaufruf entspricht Iteration-1-Layout (Quellen | Edition | Facsimile).
- Dropdown ist erweiterbar: Pool-Einträge werden deklarativ in einer Registry definiert, nicht im Markup hartkodiert.

**US-8.2** Als Forscher will ich einzelne Panels schließen und wieder öffnen können, damit ich zwei- oder einspaltig arbeiten kann.

Akzeptanzkriterien:
- Schließen-Button (×) pro Panel; geschlossenes Panel ist über eine Wiederherstellungs-Leiste reaktivierbar.
- Bei geschlossenem Panel verteilt sich die Breite auf die verbleibenden Panels.
- Zustand in URL persistiert.

**US-8.3** Als Entwickler will ich neue Inhaltstypen ergänzen können, ohne das Panel-System umzubauen (z. B. Quellen-Handschriften, weitere Überlieferungen).

Akzeptanzkriterien:
- Inhaltstyp ist ein Objekt mit `id`, `label`, `render(containerEl)`, optional `icon`.
- Registrierung über `registerPanelContent(typeDef)`.
- Rendering erfolgt in einen generischen Panel-Container, nicht in fixe DOM-Knoten.

**Scope-Notiz:** Bricht `main-container` mit drei festen `<aside>`/`<main>`/`<aside>`-Elementen auf. Erfordert Umbau des Layouts auf CSS-Grid mit dynamischer Kindermenge. Alle Render-Funktionen (`updateSourcesPanel`, `renderVerses`, `initOSD`) werden entkoppelt und in `render(containerEl)`-Hooks gekapselt.

## Epic 9 – Zeilengetreue Synopse (neu)

Pfeifer hat die Übersetzung zeilengetreu erstellt (daher die Bindestriche als Zeilenumbruch-Marker), um sie rechts neben dem Grundtext zu spiegeln. Die aktuelle Darstellung ignoriert die Zeilengrenzen und setzt die Übersetzung als Fließtext unter den Vers, was die Bindestriche zu Störartefakten macht.

**US-9.1** Als Gutachter will ich Grundtext und nhd. Übersetzung zeilengetreu nebeneinander sehen, damit ich die Entsprechung pro Zeile nachvollziehen kann.

Akzeptanzkriterien:
- Pro Grundtext-Zeile eine Übersetzungs-Zeile an identischer vertikaler Position.
- Bindestriche am Zeilenende in der Übersetzung entfallen (weder in Daten noch im DOM).
- Der Grundtext folgt den Zeilenumbrüchen der Handschrift (bislang als Fließtext gesetzt).
- Toggle zwischen „zeilengetreu" und „Fließtext" (für Lesefluss).

**US-9.2** Als Editor will ich Zeilengrenzen im TEI explizit modellieren, damit die Zeilenansicht automatisch abgeleitet werden kann.

Akzeptanzkriterien:
- TEI enthält `<lb/>` an allen Zeilenumbrüchen der Handschrift (Grundtext) und der Übersetzung.
- Die JSON-Ableitung gruppiert Sections in `lines: [{segments: [...]}]`.
- Bestehende Schichtklassifikation (`psalm_citation`, `translation`, `commentary`, `glosses`) bleibt pro Segment erhalten.

**US-9.3** Als Gutachter will ich, dass Übersetzungsanfänge am richtigen Vers erscheinen, auch wenn die zeilengetreue Aufteilung verschoben wurde.

Akzeptanzkriterien:
- Keine Übersetzungsfragmente am falschen Vers (aktuell z. B. „erlaubte es" bei V3 statt V1–2).
- Vers-Grenzen werden vor Zeilen-Grenzen respektiert: Zeilen schließen an Vers-Grenzen ab.

**Scope-Notiz:** US-9.1 löst die Datenanmerkungen zu Bindestrichen und Vers-Zuordnung auf. US-9.2 ist Voraussetzung für beliebige Zeilensynopse-Layouts (auch lat./ahd., Grundtext/Quellen). US-9.3 ist die Qualitätsprüfung für 9.1/9.2.

## Epic 10 – Psalter-Zeugen als verlinkbare Layer (neu, erweitert Epic 2/6)

Pfeifer möchte die Psalmen-Zeugen G, R, H analog zu den patristischen Quellen als Hervorhebungs-Layer nutzen: „an welchen Stellen verwendet Notker den G-Psalter?".

**US-10.1** Als Forscher will ich G, R, H wie Quellen filtern, um zu sehen, welche Textstellen auf welchen Psalter-Zeugen zurückgehen.

Akzeptanzkriterien:
- G, R, H erscheinen im Source-Filter-Bereich (visuell als eigene Gruppe, nicht vermischt mit patristischen Siglen).
- Klick auf G/R/H hebt die zugehörigen Sections im Haupttext hervor.
- Die Semantik der Siglen (textkritisch vs. Kommentarquellen-Referenz) ist im TEI mit `@cert` und `@type` expliziert.

**US-10.2** Als Editor will ich die Siglen-Semantik dokumentiert haben, damit die Zuordnung nicht geraten werden muss.

Akzeptanzkriterien:
- Klärung mit Pfeifer: sind G/R/H textkritische Varianten oder Referenzen auf den verwendeten Psalter?
- Entscheidung im TEI mit `<respStmt>` und `@cert="high|low"` fixiert.
- Im UI erscheint ein Info-Tooltip pro Sigle mit der Semantik.

**Scope-Notiz:** US-10.2 blockiert US-10.1 nur, wenn die Semantik-Entscheidung den Render-Modus beeinflusst. Mit `@cert="low"`-Markierung (Status-quo) kann US-10.1 auch vorläufig umgesetzt werden.

## Epic 11 – Bugfixes Iteration 1 (neu)

Pfeifers Bug-Liste aus dem Review. Alle verifiziert im aktuellen `docs/index.html`.

**BUG-11.1** Toggle „lat./ahd. trennen" zeigt keinen Effekt.

Ursache: `toggleSplit()` in `docs/index.html:2682–2693` setzt `.hidden-by-split` auf `.verse-interleaved` und `.visible` auf `.verse-split`. Die CSS-Regeln für diese Klassen greifen nicht in allen Konfigurationen (vermutlich Spezifitätskonflikt mit `.hidden` aus `toggleLayer`). Zu prüfen in der CSS-Sektion oberhalb von Zeile 867.

Akzeptanzkriterium: Toggle zeigt in allen Kombinationen mit Layer-Toggles und nhd-Toggle die Split-Ansicht.

**BUG-11.2** Linkes Panel (Quellenapparat) ist nicht scrollbar.

Ursache: `.sources-content` hat keine `overflow-y: auto` / feste Höhe; bei mehr Quellen als Viewport-Höhe wird der untere Teil abgeschnitten, ohne dass die Panel-Scrollbar erscheint. Pfeifer konnte dadurch Augustinus 2 (V3–5, V6) nicht gegenprüfen.

Akzeptanzkriterium: Panel scrollt unabhängig vom Hauptbereich, Scrollposition bleibt beim Verse-Wechsel erhalten.

**BUG-11.3** Schließen-Button (×) an Quellen- und Facsimile-Panel ohne Wirkung.

Ursache: `togglePanel('sources')` in `docs/index.html:2760–2773` toggelt `.collapsed`. CSS-Regel für `.sources-panel.collapsed` setzt vermutlich nur `width: 0` ohne `display: none` oder ohne `overflow: hidden`; der Panel-Inhalt bleibt sichtbar. Zu bestätigen in CSS-Block.

Akzeptanzkriterium: × schließt das Panel vollständig; Reaktivierung über Wiederherstellungs-Leiste (siehe US-8.2).

**BUG-11.4** Schrift in Quellen-Übersetzungen wird nach unten hin schwächer.

Ursache: Wahrscheinlich CSS-Gradient/Mask-Image auf `.sources-content` als Scroll-Fade-Indikator, oder `opacity`-Abstufung auf späten `.source-german`. Zu verifizieren.

Akzeptanzkriterium: Alle Quellen-Übersetzungen im gleichen Kontrast; kein Fade am Panel-Rand (oder Fade nur im Scroll-Kontext).

**BUG-11.5** Kursivierung der gesamten Übersetzung verdeckt die Herkunft (Latein vs. Althochdeutsch).

Ursache: `.source-german` oder `.nhd-translation` erhält global `font-style: italic`. Es fehlt die typografische Differenzierung, welcher Abschnitt lat. und welcher ahd. übersetzt.

Akzeptanzkriterium: Visuelle Unterscheidung zwischen Übersetzung-von-Latein und Übersetzung-von-Althochdeutsch (z. B. Kursiv nur für lat.-Quelle, aufrecht für ahd.-Quelle; oder kleiner Sigel-Präfix). Entscheidung gemeinsam mit Pfeifer.

## Epic 12 – Textkorrekturen (neu)

Pfeifers Datenkorrekturen. Alle punktuell in TEI-XML patchbar. Jede Korrektur ist atomar, per Testfall prüfbar, und beeinflusst nur `data/tei/psalm2.xml` (und abgeleitet `data/processed/psalm2.json`).

**US-12.1** Korrekturen in patristischen Quellen-Übersetzungen.

| Vers | Quelle | alt → neu |
|------|--------|-----------|
| V1–2 | Cassiodor | „Grüde" → „Gründe" |
| V1–2 | Cassiodor | „Teilen" → „Teile" |
| V1–2 | Remigius | „die Welt der Erde" → „das Universum der Welt" |
| V3–5 | Augustinus | „verplfichtet" → „verpflichtet" |
| V3–5 | Augustinus | „damit uns nicht" → „damit wir nicht" |
| V7 | Cassiodor | nach `[...]` fehlt Abstand |
| V7 | Augustinus | nach „weil" vor „was" fehlt Komma |
| V7 | Augustinus 2 | „womit er das" → „womit das" |
| V8–9 | Augustinus | nach `[...]` fehlt Komma |
| V8–9 | Cassiodor | „unerlegenden" → „unterlegenen" |
| V12–13 | Cassiodor | Komma nach „das heißt" entfernen |

Augustinus 2 zu V3–5 und V6 von Pfeifer nicht kontrolliert (blockiert durch BUG-11.2). Nach Bugfix nachreichen.

**US-12.2** Korrekturen in nhd. Übersetzung.

| Vers | alt → neu |
|------|-----------|
| V12–13 | „abgleitet" → „ableitet" |
| V10–11 | „Köper" → „Körper" |
| V3–5 | „chádensie" → „cháden sie" |
| V8–9 | Punkt fehlt zwischen „Erbe" und „Welches" |
| V8–9 | „Stab. das ist" → „Stab, das ist"; Komma zwischen „Stab" und „das heißt" |
| V7 | Komma fehlt zwischen „mir" und „mein" |
| V2 | Komma zwischen „Wille" und „gleichermaßen" entfernen |
| V3–5 | Komma fehlt zwischen „Himmel" und „wird" |
| V3–5 | „spottenswert war, das" → „spottenswert war, dass" |

**US-12.3** Fehlklassifikation Glosse → Haupttext.

V6: „ze_gótes sélbes ána-sihte. [...] → zu Gottes eigenem Angesicht. [...]" ist aktuell als Glosse markiert, gehört aber zum Haupttext.

Akzeptanzkriterium: Segment wird in TEI von `<gloss>` zu regulärem `<seg type="commentary|translation">` reklassifiziert (Typ-Entscheidung nach Prüfung der Probeseite). Glossenzähler sinkt von 14 auf 13 — Tests in `test_pipeline.py` anpassen.

## Erweiterung bestehender User Stories

**US-1.3 (erweitert)** nhd. Übersetzung als separater Toggle *auch im Quellenapparat*.

Pfeifer: „Vielleicht könnte man auch hier einen Toggle Button für die nhd. Übersetzung haben." Bezieht sich auf die Quellen-Panel-Übersetzungen (`source-german`). Aktuell immer sichtbar.

Akzeptanzkriterium: Ein Toggle steuert nhd. Übersetzung im Hauptbereich und im Quellenapparat gleichzeitig; optional zweiter Toggle nur für Quellen.

**US-2.2 (erweitert)** Psalter-Zeugen im Source-Filter (siehe US-10.1).

**US-1.2 (ersetzt durch US-9.1)** Die lat./ahd.-Trennung der Iteration 1 wird durch die zeilengetreue Synopse (Epic 9) abgelöst. BUG-11.1 bleibt gültig, solange US-1.2 existiert; nach US-9.1-Release entfällt der alte Split-Toggle.

## Priorisierung Iteration 2

| Priorität | Stories | Begründung |
|-----------|---------|------------|
| P1 — Blocker für Review | BUG-11.1, BUG-11.2, BUG-11.3, US-12.1, US-12.2, US-12.3 | Alle verhindern entweder Prüfung oder verfälschen Inhalt. Ohne Fix kein zweites Review. |
| P2 — sichtbare Qualität | BUG-11.4, BUG-11.5, US-1.3-Erweiterung | Kosmetik und Lesbarkeit, schnell umsetzbar. |
| P3 — Architektur | US-8.1, US-8.2, US-8.3 | Strukturell größte Änderung, gemeinsam mit Pfeifer abzustimmen. |
| P4 — Synopse | US-9.1, US-9.2, US-9.3 | Abhängig von Datenmodell-Erweiterung, mittelgroßer Aufwand. |
| P5 — Layer-Erweiterung | US-10.1, US-10.2 | Hängt von Siglen-Klärung (US-10.2) ab. |

## Umsetzungsplan

Drei Phasen, jeweils releasbar. Nach jeder Phase kurze Rücksprache mit Pfeifer (statt großem Endreview).

### Phase A — Korrektur (P1)

Ziel: alle Blocker fix, Pfeifer kann Review vollständig durchführen.

1. Epic 12 umsetzen: TEI-Patches (US-12.1, 12.2, 12.3), JSON regenerieren, Pipeline-Tests erweitern.
2. BUG-11.2 (Scroll): `overflow-y: auto` auf `.sources-content`, `max-height: calc(100vh - ...)`.
3. BUG-11.3 (×): `.collapsed`-CSS vervollständigen (`display: none` auf Inhaltscontainer oder Breite 0 + overflow hidden + opacity 0).
4. BUG-11.1 (Split): Spezifitätskonflikt zwischen `.hidden` und `.hidden-by-split` auflösen; Testfälle mit allen Toggle-Kombinationen.
5. Release als Iteration 2a, Pfeifer prüft nach, liefert Augustinus-2-Korrekturen V3–5 / V6 nach.

### Phase B — Lesbarkeit (P2)

Ziel: Darstellungsqualität, niedrigrisiko.

6. BUG-11.4 (Kontrast): Fade entfernen oder an Scroll-Indikator binden.
7. BUG-11.5 (Kursiv): Entscheidung mit Pfeifer, dann typografische Differenzierung.
8. US-1.3-Erweiterung: nhd.-Toggle wirkt auch auf Quellen-Panel.
9. Release als Iteration 2b.

### Phase C — Struktur (P3, P4, P5)

Ziel: Pfeifers Vision realisieren. Benötigt Architekturentscheidung.

10. **Entscheidungsgespräch mit Pfeifer (Videokonferenz):**
    - Dropdown-Modell (US-8) vs. Erweiterung der bestehenden Toggle-Gruppen (kleiner Umbau)?
    - Zeilensynopse (US-9) über TEI-`<lb/>` oder über Koordinaten-Annotation pro Zeile?
    - Siglen-Semantik G/R/H (US-10.2).
11. US-9.2 umsetzen: `<lb/>` in TEI, `lines[]` im JSON. Pipeline-Tests.
12. US-9.1 + US-9.3: Zeilen-Synopse-Layout, Fließtext-Toggle.
13. US-8.1 + US-8.3: Panel-Registry, Dropdowns, CSS-Grid-Layout.
14. US-8.2: Schließen + Wiederherstellen.
15. US-10.1 + US-10.2: G/R/H als Layer.
16. Release als Iteration 3 (neue Gesamtversion für Antragseinreichung).

### Abhängigkeiten

```
US-12.* ──┐
BUG-11.* ─┤── Phase A (releasbar)
          │
BUG-11.4/5 ── Phase B (releasbar)
US-1.3-Ext ─┘

US-10.2 ── US-10.1 ───────┐
                          │
US-9.2 ── US-9.1 ── US-9.3┤── Phase C (gemeinsam releasen)
                          │
US-8.3 ── US-8.1 ── US-8.2┘
```

## Implementierungsvorschlag

### Phase A — Dateieingriffe

**TEI (`data/tei/psalm2.xml`):** Direkte String-Ersetzungen pro Korrektur aus US-12.1 und US-12.2. Jede Korrektur als atomarer Commit (`git log` nachvollziehbar). Glossen-Reklassifikation V6: `<gloss>…</gloss>` → `<seg type="commentary">…</seg>` (oder entsprechender Typ).

**JSON-Regeneration:** `python scripts/tei_to_json.py data/tei/psalm2.xml data/processed/psalm2.json` nach jedem Commit. `python scripts/test_pipeline.py` — 25 Tests laufen durch, Glossenzähler auf 13 anpassen.

**CSS-Fixes:** In `docs/index.html` vor Zeile 867:
- `.sources-content { overflow-y: auto; min-height: 0; }` (flexbox-Kontext erlaubt `min-height:0` erst korrektes Scrollen).
- `.sources-panel.collapsed { width: 0; overflow: hidden; border: none; }` (statt nur `display:none` auf children).
- `.verse-interleaved.hidden-by-split { display: none; }`, `.verse-split { display: none; }`, `.verse-split.visible { display: grid; }` — statt konkurrierender `.hidden`-Selektor.

**Test:** Manuell alle Toggle-Kombinationen (4 Layer × nhd × split = 32 States) durchschalten. Keyboard-Shortcuts 1–4, N, L. URL-Hash-Persistenz.

### Phase B — Dateieingriffe

**Kontrast (BUG-11.4):** CSS-Property `mask-image` oder `background: linear-gradient(...)` auf `.sources-content` entfernen oder nur an `scroll-timeline` binden.

**Kursiv (BUG-11.5):** `.source-german` aufteilen: `.source-german.lang-lat` kursiv, `.source-german.lang-ahd` aufrecht (oder gemeinsam mit Pfeifer festgelegte Lösung). Pipeline erweitern: `source.source_language` als Feld im JSON (aus TEI-`@xml:lang`).

**nhd.-Toggle auf Quellen (US-1.3-Ext):** `toggleNhd()` zusätzlich Klasse `.hide-source-nhd` auf `#sources-panel` toggeln; CSS `.hide-source-nhd .source-german { display: none; }`.

### Phase C — Dateieingriffe

**US-9.2 — TEI-Erweiterung:** `<lb/>`-Elemente an Zeilenumbrüchen. `scripts/parse_probeseite.py` muss DOCX-Zeilenumbrüche erkennen (Soft-Return vs. Hard-Return). Fallback: Pfeifer liefert Zeilenumbruch-Markierungen explizit in der DOCX.

**US-9.1 — Zeilen-Layout:** Renderer `renderVerses()` erweitern um Modus „lines": Pro `verse.lines[]` ein CSS-Grid-Row mit zwei Spalten (Grundtext links, nhd. rechts). Grundtext verwendet `<br>` oder CSS `white-space: pre-line` auf Zeilenbasis. Bindestriche am Zeilenende aus Daten entfernen.

**US-8.1 — Panel-Registry:** Neue Datei `docs/panels.js` (oder Block in `index.html`):
```js
const PANEL_CONTENT = new Map();
function registerPanelContent(def) { PANEL_CONTENT.set(def.id, def); }
registerPanelContent({ id: 'sources', label: 'Quellenapparat',
  render: (el) => { /* moves updateSourcesPanel() logic here */ } });
registerPanelContent({ id: 'edition', label: 'Notkers Text',
  render: (el) => { /* moves renderVerses() logic here */ } });
// ...facsimile, wiener, psalter-g, psalter-r, psalter-h, nhd, annotations
```
`main-container` wird zu CSS-Grid mit `grid-template-columns: var(--col-widths)`. Drei Panel-Container (`#panel-left`, `#panel-center`, `#panel-right`) mit Dropdown-Header. State erweitert um `state.panelAssignment = { left: 'sources', center: 'edition', right: 'facsimile' }`. URL-Hash-Persistenz erweitert.

**US-10.1 — G/R/H als Layer:** Siglen-Pool in `renderSourceFilters()` um `['G','R','H']` erweitern, visuell als eigene Gruppe (separate `<div class="source-filters-group" data-group="psalter">`). `updateSourceHighlights()` braucht keine Änderung — prüft bereits `@data-sigles`.

### Testmatrix

Manuelle End-to-End-Prüfung nach jeder Phase:
- Alle 13 Verse: Quellen, Glossen, Übersetzungen vollständig dargestellt.
- Alle Toggle-Kombinationen, Keyboard-Shortcuts, URL-Hash-Reload.
- Scroll in allen Panels unabhängig.
- Panel schließen/öffnen; Dropdown-Wechsel in jedem Panel (Phase C).
- Regression-Check Iteration 1: Facsimile-Sync, Source-Filter, Tab-Wechsel.

## Getroffene Entscheidungen

Diese Entscheidungen sind DHCraft-seitig getroffen und gehen in den Videocall mit Pfeifer als Vorschlag ein. Punkt 4 bleibt bis Pfeifer-Bestätigung provisorisch.

### 1. Panel-Modell (US-8) — Dropdown nur rechts, Mitte fix

**Entscheidung.** Rechtes Panel: Dropdown mit Facsimile (Default) | Wiener Notker | Psalter G | Psalter R | Psalter H | Anmerkungen. Linkes Panel: Quellenapparat Default, optional zweiter Dropdown-Eintrag für Anmerkungen. Mittleres Panel: Edition fix, ohne Dropdown.

**Begründung.** Pfeifer wünscht Dropdowns in allen drei Feldern, hat aber im gleichen Feedback das bestehende Drei-Spalten-Layout als „sehr gelungen" bezeichnet. Drei volle Dropdowns würden die visuelle Klarheit und die Minuten-zum-Eindruck-Wirkung für Gutachter gefährden — sie müssten erst konfigurieren, bevor sie sehen. Sein inhaltliches Kernziel (Notker neben G/R/H oder Wiener Notker vergleichen) wird bereits vollständig erfüllt, wenn nur das rechte Panel wechselbar ist. Der Umbau halbiert sich (eine Registry statt drei, CSS-Grid nicht zwingend), das Risiko einer leeren Zentralspalte entfällt.

**Implikation.** US-8.1 und US-8.3 bleiben bestehen, werden aber auf ein Panel fokussiert. US-8.2 (Schließen/Wiederherstellen) bleibt für alle Panels relevant. Falls Pfeifer im Videocall auf volle Dropdown-Flexibilität besteht, ist die Skalierung auf drei Panels trivial, weil die Registry schon steht.

### 2. Zeilensynopse (US-9) — TEI-`<lb/>` aus Bindestrichen geparst

**Entscheidung.** `scripts/parse_probeseite.py` erweitern: Bindestriche am Zeilenende in der DOCX-Übersetzung (`wort-\nwort2`) werden als Zeilenumbruch-Signal konsumiert — Bindestrich verschwindet aus dem Text, stattdessen `<lb/>` im TEI. JSON-Ableitung gruppiert Segments in `lines[]`. Der Grundtext benötigt analoge Zeilenumbruch-Markierung, Quelle klärt der Videocall (DOCX der Probeseite oder Tax/Sehrt-Vorlage).

**Begründung.** Die Alternative (CSS-Grid ohne Datenänderung) scheidet aus — wir haben ohne die Bindestriche keine Information, wo Pfeifers Zeilen sind. Die gewählte Lösung konsumiert die Artefakte als Daten, statt sie als Störung zu behandeln. Skaliert auf die übrigen 149 Psalmen. Kein zusätzliches Liefer-Ping an Pfeifer für die Übersetzung.

**Offene Nachfrage im Videocall.** Quelle für die Grundtext-Zeilenumbrüche der Handschrift.

### 3. Kursiv-Semantik (BUG-11.5) — Kursiv nur für Übersetzungen aus dem Lateinischen

**Entscheidung.** Pipeline erweitert um `source.source_language` aus TEI-`@xml:lang`. CSS: `.source-german.lang-lat { font-style: italic }`, `.source-german.lang-ahd { font-style: normal }`.

**Begründung.** Entspricht editorischer Konvention (Kursiv für „aus anderer Sprache übertragen"). Alternativen (Sigel-Präfix, Farbkodierung) sind visuell lauter oder kollidieren mit dem bestehenden Farbsystem. Minimaler Umsetzungsaufwand: ein Datenfeld, zwei CSS-Regeln.

### 4. Siglen-Semantik G/R/H (US-10.2) — provisorisch als Psalter-Zeugen, Filter-Layer

**Entscheidung.** G = Gallicanum, R = Romanum, H = Hebraicum werden als Psalter-Zeugen modelliert (`@type="psalter_witness"`), nicht als Varianten-Apparat. Visualisierung als eigene Filter-Gruppe im Quellen-Panel, analog patristischer Quellen. `@cert="low"` bis Pfeifer-Bestätigung. Nicht-blockierend für US-10.1.

**Begründung.** Die Filter-Layer-Darstellung beantwortet Pfeifers explizite Frage („an welchen Stellen verwendet Notker den G-Psalter?") direkt. Ein Varianten-Apparat wäre eine andere Story. **Sigelkonflikt:** „R" ist doppelt belegt (Remigius patristisch und Romanum-Psalter) — im UI mit unterschiedlichen Chip-Farben oder Prefix disambiguieren, im TEI über `@type` trennbar.

### 5. Research-Vault-Zugriff (Pfeifers Zusatzfrage) — kein Repo-Zugriff, Methoden-Paket

**Entscheidung.** Kein Repo-Zugriff für Pfeifers Antragskollegen. Stattdessen: (a) `docs/methode.html` als öffentliche, verlinkbare Methodenseite ausbauen und stabilisieren (existiert bereits als Gerüst); (b) konsolidiertes PDF „Methodik Notker-Edition-Prototyp v1" als zitierbaren Antrags-Stand; (c) bei Bedarf für Pfeifer persönlich ein Read-only-Snapshot-Branch.

**Begründung.** Antragskollegen brauchen zitierbaren stabilen Stand, nicht Live-Repo. DHCraft behält Qualitätskontrolle über die Methodendarstellung (Kernprofil). Antworten-Mail an Pfeifer als separate L2-Nebentask.

## Verknüpfungen

- [[Anforderungen]] — Iteration-1-Baseline
- [[Design]] — Design-Entscheidungen (ggf. in Phase C zu aktualisieren)
- [[Technik]] — Pipeline und Datenmodell (Erweiterung in US-9.2)
- [[Probeseite Analyse]] — Original-Datenquelle
- [[Journal]] — Chronik (wird nach Phase A fortgeschrieben)
