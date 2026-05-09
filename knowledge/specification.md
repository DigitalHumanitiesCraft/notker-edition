---
title: "Specification — Anforderungen, Entscheidungen, Stand"
project:
  name: "notker-edition"
  repository: "https://github.com/DigitalHumanitiesCraft/notker-edition"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/excellence/blog/Promptotyping"
status: active
version: "0.2"
created: 2026-02-27
updated: 2026-05-09
language: de
authors:
  - "Christopher Pollin"
generated-with: "Claude (Anthropic)"
topics:
  - "[[Requirements Engineering]]"
  - "[[User Stories]]"
  - "[[Decision Records]]"
related:
  - "[[INDEX]]"
  - "[[project]]"
  - "[[design]]"
  - "[[architecture]]"
  - "[[journal]]"
  - "[[offene-korrekturen]]"
---

# Specification — Anforderungen, Entscheidungen, Stand

Konsolidierte Substanz-Dokumentation für den Notker-Edition-Prototyp. Konsolidiert die Anforderungen aus Iteration 1, die Erweiterungen und Bugfixes aus Iteration 2 (Pfeifer-Review), die getroffenen Entscheidungen, die Phasenstruktur der Umsetzung und den abschließenden Stand pro Story einschließlich der Iteration-2c-Follow-ups. Das Dokument ist nicht chronologisch organisiert (das ist Aufgabe von [[journal]]), sondern nach Substanz-Schichten: zuerst Anforderungen pro Iteration, dann Entscheidungen, dann Umsetzungsstand.

## Kontext

Prototyp für einen Drittmittelantrag. Zielgruppe: Gutachter, die die Vision einer digitalen Edition verstehen sollen. Der Prototyp muss nicht produktionsreif sein, aber funktional und visuell überzeugend. Demonstrationsobjekt: Psalm 2 (13 Verse) aus Notkers Psalmenkommentar.

Iteration 1 wurde am 2026-03-23 ausgeliefert. Auftraggeber-Review am 2026-04-15 (Mail + Google Doc) lieferte Architekturwünsche, Bugs und Textkorrekturen. Iteration 2 (mit Sub-Iterationen 2b und 2c) setzt das Review um, bevor das gesamte Konvolut an die Antrags-Gutachter geht.

## Iteration 1 — Baseline (2026-03-23)

### Epic 1 — Textdarstellung

**US-1.1** Als Gutachter will ich Notkers Text für Psalm 2 vollständig lesen können.

Akzeptanzkriterien: Alle Verse des Psalms dargestellt, Vers- und Zeilenreferenzen sichtbar, Seitenumbrüche der Edition (R10–R13) markiert.

**US-1.2** Als Gutachter will ich den verschränkten lat./ahd. Text sehen und per Toggle in zwei Spalten trennen können.

Akzeptanzkriterien: Standardansicht zeigt verschränkten Text (wie in der Handschrift); Toggle-Ansicht zeigt Latein links, Althochdeutsch rechts, synchron gescrollt; farbliche Unterscheidung gemäß [[design#3.3 Farbsystem]].

**US-1.3** Als Gutachter will ich die nhd. Übersetzung neben dem Haupttext sehen können.

Akzeptanzkriterien: nhd. Übersetzung einblendbar (Toggle), Zuordnung auf Vers-/Abschnittsebene, Datengrundlage ist die Arbeitsübersetzung des Auftraggebers aus der Probeseite.

### Epic 2 — Quellenapparat

**US-2.1** Als Gutachter will ich bei Klick auf einen Vers die patristischen Quellen sehen.

Akzeptanzkriterien: Klick auf Vers öffnet/aktualisiert Quellen-Panel; Quellen-Panel zeigt Sigle, Quellenname, lat. Text, dt. Übersetzung; alle Verse des Psalms abgedeckt.

**US-2.2** Als Forscher will ich nach einzelnen Quellen filtern können.

Akzeptanzkriterien: Checkboxen pro Quellen-Sigle (A, C, Br, R etc.); Filter hebt zugehörige Stellen im Haupttext hervor; Quellen-Panel zeigt nur gefilterte Einträge.

### Epic 3 — Facsimile

**US-3.1** Als Gutachter will ich das Handschriftendigitalisat neben dem Text sehen.

Akzeptanzkriterien: IIIF-Viewer eingebettet (e-codices, CSg 0021, ab Seite 11); mindestens die relevanten Seiten für Psalm 2 navigierbar; Zoom und Pan funktionieren.

### Epic 4 — Funktionale Textschichten

**US-4.1** Als Gutachter will ich Übersetzung und Kommentar unabhängig voneinander ein-/ausblenden können, damit ich die verschiedenen Textfunktionen gezielt betrachten kann.

Akzeptanzkriterien: Drei unabhängige Toggles (Psalmzitation / Übersetzung / Kommentar); Psalmzitation visuell unterscheidbar (olive/warm, angelehnt an Probeseite); Übersetzung visuell unterscheidbar (grün); Kommentar als Standard sichtbar, ausblendbar.

**US-4.2** Als Gutachter will ich Interlinearglossen separat ein-/ausblenden können.

Akzeptanzkriterien: Toggle für Glossen (unabhängig von den drei Textschichten); Glossen visuell als Annotation erkennbar (kleinere Schrift, eigene Farbe).

US-4.1 und US-4.2 sind explizite Wünsche des Auftraggebers. Sie gehen über das ursprüngliche Toggle-Konzept (nur lat./ahd.) hinaus und erfordern die dreigliedrige Textfunktions-Klassifikation aus [[data#Probeseiten-Strukturanalyse]].

### Epic 5 — Gesamteindruck

**US-5.1** Als Gutachter will ich eine visuell ansprechende, professionelle Oberfläche sehen.

Akzeptanzkriterien: Responsives Layout (Laptop-Bildschirm); klare visuelle Hierarchie; kein „Baustellen"-Eindruck.

**US-5.2** Als Gutachter will ich verstehen, dass dies ein Prototyp ist und die Vision skaliert.

Akzeptanzkriterien: Kurzer Einleitungstext erklärt Kontext und Vision; Navigation deutet weitere Psalmen an (ausgegraut).

### Epic 6 — Psalmtext-Vergleich

**US-6.1** Als Gutachter will ich die Psalmtext-Versionen synoptisch vergleichen können.

Akzeptanzkriterien: Synoptische Darstellung der fünf Textzeugen (G, R, H, A-Psalter, C-Psalter); Varianten visuell hervorgehoben; umschaltbar oder als eigener Tab.

**US-6.2** Als Gutachter will ich den Wiener Notker als Paralleltext sehen.

Akzeptanzkriterien: Wiener Notker (ÖNB Cod. 2681) als einblendbarer Paralleltext; Zuordnung auf Versebene.

Daten für US-6.1 und US-6.2 liegen vollständig in der Probeseite vor.

### Epic 7 — Querverweise

**US-7.1** Als Forscher will ich Querverweise auf andere Bibelstellen sehen, die Notker zitiert.

Akzeptanzkriterien: Eigener Reiter/Panel für Bibelstellen-Querverweise; Zuordnung auf Versebene.

Wunsch des Auftraggebers. Datengrundlage existiert noch nicht. Nicht im Prototyp umsetzbar, aber im Datenmodell vorbereiten.

### Priorisierung Iteration 1

| Priorität | User Stories | Status |
|---|---|---|
| P1 (Kern) | US-1.1, US-1.2, US-2.1, US-5.1 | done |
| P2 (wichtig) | US-1.3, US-2.2, US-3.1, US-5.2 | done |
| P3 (Mehraufwand) | US-4.1, US-4.2 | done |
| P4 (scope offen) | US-6.1, US-6.2 | done |
| P5 (nicht im Prototyp) | US-7.1 | nicht umgesetzt (Datenfehlen) |

## Iteration 2 — Pfeifer-Review (2026-04-15 bis 2026-04-16)

Iteration 2 ergänzt die Iteration-1-Baseline um Epics 8–12, erweitert US-1.2, US-1.3 und US-2.2 und dokumentiert die Bug- und Korrektur-Backlogs.

### Epic 8 — Panel-Flexibilisierung

Der Auftraggeber wünscht freie Belegung der drei Hauptbereiche (links, Mitte, rechts) aus einem Pool verfügbarer Inhalte statt der festen Rollenzuordnung Quellenapparat | Edition | Facsimile. Das bricht mit dem aktuellen Layout und ist die strukturell größte Änderung der Iteration.

**US-8.1** Als Forscher will ich pro Panel über ein Dropdown auswählen, welchen Inhalt ich dort sehe, damit ich meine Arbeitsansicht frei konfigurieren kann.

Akzeptanzkriterien: Drei Dropdowns im Panel-Header (links, Mitte, rechts); Inhaltstypen im Pool (Quellenapparat, Notkers Text, Nhd. Übersetzung, Wiener Notker, Psalter G, Psalter R, Psalter H, Handschrift Notker, Anmerkungen); Dropdown-Zustand in URL-Hash persistiert (`p=left:sources,center:edition,right:facsimile`); Default nach Erstaufruf entspricht Iteration-1-Layout; Dropdown ist erweiterbar (Pool-Einträge deklarativ in einer Registry, nicht im Markup hartkodiert).

**US-8.2** Als Forscher will ich einzelne Panels schließen und wieder öffnen können, damit ich zwei- oder einspaltig arbeiten kann.

Akzeptanzkriterien: Schließen-Button (×) pro Panel; geschlossenes Panel über Wiederherstellungs-Leiste reaktivierbar; bei geschlossenem Panel verteilt sich die Breite auf die verbleibenden; Zustand in URL persistiert.

**US-8.3** Als Entwickler will ich neue Inhaltstypen ergänzen können, ohne das Panel-System umzubauen (z. B. Quellen-Handschriften, weitere Überlieferungen).

Akzeptanzkriterien: Inhaltstyp ist ein Objekt mit `id`, `label`, `render(containerEl)`, optional `icon`; Registrierung über `registerPanelContent(typeDef)`; Rendering erfolgt in einen generischen Panel-Container, nicht in fixe DOM-Knoten.

Scope-Notiz: Bricht `main-container` mit drei festen `<aside>`/`<main>`/`<aside>`-Elementen auf. Erfordert Umbau des Layouts auf CSS-Grid mit dynamischer Kindermenge. Alle Render-Funktionen (`updateSourcesPanel`, `renderVerses`, `initOSD`) werden entkoppelt und in `render(containerEl)`-Hooks gekapselt.

### Epic 9 — Zeilengetreue Synopse

Der Auftraggeber hat die Übersetzung zeilengetreu erstellt (daher die Bindestriche als Zeilenumbruch-Marker), um sie rechts neben dem Grundtext zu spiegeln. Die Iteration-1-Darstellung ignorierte die Zeilengrenzen und setzte die Übersetzung als Fließtext unter den Vers, was die Bindestriche zu Störartefakten machte.

**US-9.1** Als Gutachter will ich Grundtext und nhd. Übersetzung zeilengetreu nebeneinander sehen, damit ich die Entsprechung pro Zeile nachvollziehen kann.

Akzeptanzkriterien: Pro Grundtext-Zeile eine Übersetzungs-Zeile an identischer vertikaler Position; Bindestriche am Zeilenende in der Übersetzung entfallen; Grundtext folgt den Zeilenumbrüchen der Handschrift; Toggle zwischen „zeilengetreu" und „Fließtext".

**US-9.2** Als Editor will ich Zeilengrenzen im TEI explizit modellieren, damit die Zeilenansicht automatisch abgeleitet werden kann.

Akzeptanzkriterien: TEI enthält `<lb/>` an allen Zeilenumbrüchen der Handschrift (Grundtext) und der Übersetzung; JSON-Ableitung gruppiert Sections in `lines: [{segments: [...]}]`; bestehende Schichtklassifikation bleibt pro Segment erhalten.

**US-9.3** Als Gutachter will ich, dass Übersetzungsanfänge am richtigen Vers erscheinen, auch wenn die zeilengetreue Aufteilung verschoben wurde.

Akzeptanzkriterien: Keine Übersetzungsfragmente am falschen Vers (Iteration-1-Bug: „erlaubte es" bei V3 statt V1–2); Vers-Grenzen werden vor Zeilen-Grenzen respektiert.

Scope-Notiz: US-9.1 löst die Datenanmerkungen zu Bindestrichen und Vers-Zuordnung auf. US-9.2 ist Voraussetzung für beliebige Zeilensynopse-Layouts. US-9.3 ist die Qualitätsprüfung für 9.1/9.2.

### Epic 10 — Psalter-Zeugen als verlinkbare Layer

Der Auftraggeber möchte die Psalmen-Zeugen G, R, H analog zu den patristischen Quellen als Hervorhebungs-Layer nutzen: „an welchen Stellen verwendet Notker den G-Psalter?".

**US-10.1** Als Forscher will ich G, R, H wie Quellen filtern, um zu sehen, welche Textstellen auf welchen Psalter-Zeugen zurückgehen.

Akzeptanzkriterien: G, R, H erscheinen im Source-Filter-Bereich (visuell als eigene Gruppe, nicht vermischt mit patristischen Siglen); Klick auf G/R/H hebt die zugehörigen Sections im Haupttext hervor; Semantik der Siglen (textkritisch vs. Kommentarquellen-Referenz) ist im TEI mit `@cert` und `@type` expliziert.

**US-10.2** Als Editor will ich die Siglen-Semantik dokumentiert haben, damit die Zuordnung nicht geraten werden muss.

Akzeptanzkriterien: Klärung mit dem Auftraggeber, ob G/R/H textkritische Varianten oder Referenzen auf den verwendeten Psalter sind; Entscheidung im TEI mit `<respStmt>` und `@cert="high|low"` fixiert; Info-Tooltip pro Sigle im UI.

Scope-Notiz: US-10.2 blockiert US-10.1 nur, wenn die Semantik-Entscheidung den Render-Modus beeinflusst. Mit `@cert="low"`-Markierung kann US-10.1 vorläufig umgesetzt werden.

### Epic 11 — Bugfixes Iteration 1

Bug-Liste aus dem Review. Alle verifiziert im Iteration-1-`docs/index.html`.

**BUG-11.1** Toggle „lat./ahd. trennen" zeigt keinen Effekt. Ursache: `toggleSplit()` in `docs/index.html:2682–2693` setzt `.hidden-by-split` auf `.verse-interleaved` und `.visible` auf `.verse-split`. CSS-Regeln für diese Klassen greifen nicht in allen Konfigurationen (Spezifitätskonflikt mit `.hidden` aus `toggleLayer`). Akzeptanz: Toggle zeigt in allen Kombinationen mit Layer-Toggles und nhd-Toggle die Split-Ansicht.

**BUG-11.2** Linkes Panel (Quellenapparat) ist nicht scrollbar. Ursache: `.sources-content` hat keine `overflow-y: auto` / feste Höhe. Akzeptanz: Panel scrollt unabhängig vom Hauptbereich; Scrollposition bleibt beim Verse-Wechsel erhalten.

**BUG-11.3** Schließen-Button (×) an Quellen- und Facsimile-Panel ohne Wirkung. Ursache: `togglePanel('sources')` in `docs/index.html:2760–2773` toggelt `.collapsed`; CSS-Regel für `.sources-panel.collapsed` setzt nur `width: 0` ohne `display: none` oder `overflow: hidden`. Akzeptanz: × schließt das Panel vollständig; Reaktivierung über Wiederherstellungs-Leiste (siehe US-8.2).

**BUG-11.4** Schrift in Quellen-Übersetzungen wird nach unten hin schwächer. Ursache: vermutlich CSS-Gradient/Mask-Image auf `.sources-content` als Scroll-Fade-Indikator. Akzeptanz: Alle Quellen-Übersetzungen im gleichen Kontrast; kein Fade am Panel-Rand.

**BUG-11.5** Kursivierung der gesamten Übersetzung verdeckt die Herkunft (Latein vs. Althochdeutsch). Ursache: `.source-german` oder `.nhd-translation` erhält global `font-style: italic`. Akzeptanz: Visuelle Unterscheidung zwischen Übersetzung-von-Latein und Übersetzung-von-Althochdeutsch (Entscheidung gemeinsam mit dem Auftraggeber).

### Epic 12 — Textkorrekturen

Datenkorrekturen aus dem Review. Alle punktuell in TEI-XML patchbar. Jede Korrektur ist atomar, per Testfall prüfbar, und beeinflusst nur `data/tei/psalm2.xml` (und abgeleitet `data/processed/psalm2.json`).

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

Augustinus 2 zu V3–5 und V6 wurde in Iteration 1 nicht kontrolliert (blockiert durch BUG-11.2). Nach Bugfix nachreichen.

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

V6: „ze_gótes sélbes ána-sihte. [...] → zu Gottes eigenem Angesicht. [...]" ist in Iteration 1 als Glosse markiert, gehört aber zum Haupttext.

Akzeptanz: Segment wird in TEI von `<gloss>` zu regulärem `<seg type="commentary|translation">` reklassifiziert (Typ-Entscheidung nach Prüfung der Probeseite). Glossenzähler sinkt von 14 auf 13 — Tests in `test_pipeline.py` anpassen.

### Erweiterung bestehender User Stories

**US-1.3 (erweitert)** nhd. Übersetzung als separater Toggle auch im Quellenapparat. Bezieht sich auf die Quellen-Panel-Übersetzungen (`source-german`); Iteration 1 hatte sie immer sichtbar. Akzeptanz: Ein Toggle steuert nhd. Übersetzung im Hauptbereich und im Quellenapparat gleichzeitig; optional zweiter Toggle nur für Quellen.

**US-2.2 (erweitert)** Psalter-Zeugen im Source-Filter (siehe US-10.1).

**US-1.2 (ersetzt durch US-9.1)** Die lat./ahd.-Trennung der Iteration 1 wird durch die zeilengetreue Synopse (Epic 9) abgelöst. BUG-11.1 bleibt gültig, solange US-1.2 existiert; nach US-9.1-Release entfällt der alte Split-Toggle.

### Priorisierung Iteration 2

| Priorität | Stories | Begründung |
|-----------|---------|------------|
| P1 — Blocker für Review | BUG-11.1, BUG-11.2, BUG-11.3, US-12.1, US-12.2, US-12.3 | Alle verhindern entweder Prüfung oder verfälschen Inhalt |
| P2 — sichtbare Qualität | BUG-11.4, BUG-11.5, US-1.3-Erweiterung | Kosmetik und Lesbarkeit, schnell umsetzbar |
| P3 — Architektur | US-8.1, US-8.2, US-8.3 | Strukturell größte Änderung, gemeinsam mit Auftraggeber abzustimmen |
| P4 — Synopse | US-9.1, US-9.2, US-9.3 | Abhängig von Datenmodell-Erweiterung, mittelgroßer Aufwand |
| P5 — Layer-Erweiterung | US-10.1, US-10.2 | Hängt von Siglen-Klärung (US-10.2) ab |

## Getroffene Entscheidungen

Diese Entscheidungen sind seitens Digital Humanities Craft getroffen und gehen in den Videocall mit dem Auftraggeber als Vorschlag ein. D-9 bleibt bis zur Bestätigung durch den Auftraggeber provisorisch.

### Vor Implementierung Iteration 1 entschieden

| Nr. | Frage | Entscheidung |
|---|---|---|
| D-1 | Glossen-Darstellung | Inline eingerückt (sichtbarer als Tooltip, ehrlicher gegenüber dem Textcharakter) |
| D-2 | nhd. Übersetzung Position | Iteration 1: unterhalb des Verses (revidiert in D-2-Iter2: parallele Spalte) |
| D-3 | Quellenfilter-Farbe | Individuelle Sigle-Farben, damit mehrere Filter gleichzeitig lesbar bleiben |
| D-4 | Serifenschrift | Gentium Book Plus (frei, gute ahd.-Zeichenabdeckung) |

### In Iteration 2 entschieden

**D-5 — Panel-Modell (US-8): Dropdown nur rechts, Mitte fix.** Rechtes Panel: Dropdown mit Facsimile (Default) | Wiener Notker | Psalter G | Psalter R | Psalter H | Anmerkungen. Linkes Panel: Quellenapparat Default, optional zweiter Dropdown-Eintrag für Anmerkungen. Mittleres Panel: Edition fix, ohne Dropdown.

Begründung: Der Auftraggeber wünscht Dropdowns in allen drei Feldern, hat aber im gleichen Feedback das bestehende Drei-Spalten-Layout als „sehr gelungen" bezeichnet. Drei volle Dropdowns würden die visuelle Klarheit und die Minuten-zum-Eindruck-Wirkung für Gutachter gefährden. Das inhaltliche Kernziel (Notker neben G/R/H oder Wiener Notker vergleichen) wird bereits vollständig erfüllt, wenn nur das rechte Panel wechselbar ist. Der Umbau halbiert sich, das Risiko einer leeren Zentralspalte entfällt.

Implikation: US-8.1 und US-8.3 bleiben bestehen, werden aber auf ein Panel fokussiert. US-8.2 (Schließen/Wiederherstellen) bleibt für alle Panels relevant. Die Skalierung auf drei Panels ist später trivial, weil die Registry schon steht.

**D-6 — Zeilensynopse (US-9): TEI-`<lb/>` aus Bindestrichen geparst.** `scripts/parse_probeseite.py` erweitern: Bindestriche am Zeilenende in der DOCX-Übersetzung (`wort-\nwort2`) werden als Zeilenumbruch-Signal konsumiert — Bindestrich verschwindet aus dem Text, stattdessen `<lb/>` im TEI. JSON-Ableitung gruppiert Segments in `lines[]`. Der Grundtext benötigt analoge Zeilenumbruch-Markierung, Quelle klärt der Videocall.

Begründung: Die Alternative (CSS-Grid ohne Datenänderung) scheidet aus — ohne die Bindestriche fehlt die Information, wo die Zeilen des Auftraggebers liegen. Die gewählte Lösung konsumiert die Artefakte als Daten, statt sie als Störung zu behandeln. Skaliert auf die übrigen 149 Psalmen.

**D-7 — Kursiv-Semantik (BUG-11.5): Kursiv nur für Übersetzungen aus dem Lateinischen.** Pipeline erweitert um `source.source_language` aus TEI-`@xml:lang`. CSS: `.source-german.lang-lat { font-style: italic }`, `.source-german.lang-ahd { font-style: normal }`.

Begründung: Entspricht editorischer Konvention. Alternativen (Sigel-Präfix, Farbkodierung) sind visuell lauter oder kollidieren mit dem bestehenden Farbsystem.

**D-8 — Psalmtext-Vergleich.** Eigener Pool-Eintrag im Slot-System, als synoptische Tabelle aller fünf Zeugen.

**D-9 — Siglen-Semantik G/R/H (US-10.2): provisorisch als Psalter-Zeugen, Filter-Layer.** G = Gallicanum, R = Romanum, H = Hebraicum werden als Psalter-Zeugen modelliert (`@type="psalter_witness"`), nicht als Varianten-Apparat. Visualisierung als eigene Filter-Gruppe im Quellen-Panel, analog patristischer Quellen. `@cert="low"` bis zur Bestätigung durch den Auftraggeber. Nicht-blockierend für US-10.1.

Begründung: Die Filter-Layer-Darstellung beantwortet die explizite Frage des Auftraggebers direkt. Sigelkonflikt: „R" ist doppelt belegt (Remigius patristisch und Romanum-Psalter) — im UI mit unterschiedlichen Chip-Farben oder Prefix disambiguieren, im TEI über `@type` trennbar.

**D-10 — Facsimile-Panel.** Standardmäßig offen im rechten Slot; Breite 3 : 4 : 3 (Quellen : Edition : Handschrift).

**D-11 — Farbüberlagerung Schicht × Filter.** Schichtfarbe für den Text, Filterfarbe als Seiten-Stripe auf der `.verse-line`; mehrere Filter stapeln sich als 4px-Streifen mit 1px-Abstand.

**D-12 — Wiener Notker.** Eigener Pool-Eintrag, als Paralleltext.

**D-13 — Research-Vault-Zugriff: öffentliche Vault-Seite statt Repo-Zugriff.** Kein Repo-Zugriff für die Antragskollegen. Stattdessen `docs/vault.html` rendert alle Wissensdokumente öffentlich und verlinkbar; `docs/methode.html` als stabile Methodenseite; konsolidiertes PDF „Methodik Notker-Edition-Prototyp v1" als zitierbarer Antrags-Stand. Begründung: Antragskollegen brauchen zitierbaren stabilen Stand, nicht Live-Repo. Digital Humanities Craft behält Qualitätskontrolle über die Methodendarstellung.

### Offen

| Nr. | Frage |
|---|---|
| D-14 | Querverweise auf Bibelstellen — wo im Layout? Daten liegen noch nicht vor |
| D-15 | Barrierefreiheits-Review (Kontrastverhältnisse über alle Farbkombinationen) |
| D-16 | Toggle-Animation: aktuell hart, ggf. sanfter Fade |

## Umsetzung und Stand

### Phasenplan

Drei Phasen, jeweils releasbar. Nach jeder Phase kurze Rücksprache mit dem Auftraggeber statt großem Endreview.

**Phase A — Korrektur (P1).** Ziel: alle Blocker fix, das Review kann vollständig durchgeführt werden.

Methodische Notiz: Textkorrekturen werden nicht händisch in `data/tei/psalm2.xml` gepatcht — ein Re-Parse der DOCX würde sie überschreiben. Initial als Errata-Layer geplant (YAML-Regeln + `apply_errata.py`); im Verlauf der Iteration 2b zugunsten einer einfacheren `PFEIFER_CORRECTIONS`-Liste in `parse_probeseite.py` aufgegeben.

Schritte: Test-Infrastruktur (Ground-Truth-Fixtures pro Korrektur ±20 Zeichen Kontext, Tests laufen initial rot); Errata-Mechanismus (später durch `PFEIFER_CORRECTIONS` ersetzt); Parser-Fix V6 Glossen-Heuristik; CSS-Bugfixes (BUG-11.2 Scroll, BUG-11.3 ×-Button, BUG-11.1 Split-Toggle); End-to-End-Verifikation aller 32 Toggle-States.

**Phase B — Lesbarkeit (P2).** Niedrigrisiko, Darstellungsqualität. BUG-11.4 Kontrast-Fade entfernen bzw. an Scroll-Indikator binden; BUG-11.5 Kursiv-Differenzierung nach D-7; US-1.3-Erweiterung (nhd.-Toggle wirkt auch auf Quellen-Panel). Release als Iteration 2b.

**Phase C — Struktur (P3, P4, P5).** Vision des Auftraggebers realisieren, benötigt Architekturentscheidung im Videocall.

1. Entscheidungsgespräch: Dropdown-Modell vs. Toggle-Gruppen-Erweiterung, Zeilensynopse über `<lb/>` oder Koordinaten-Annotation, Siglen-Semantik G/R/H.
2. US-9.2 (TEI-`<lb/>`, `lines[]` im JSON, Pipeline-Tests).
3. US-9.1 + US-9.3: Zeilen-Synopse-Layout mit Fließtext-Toggle.
4. US-8.1 + US-8.3: Panel-Registry, Dropdowns, CSS-Grid-Layout.
5. US-8.2: Schließen + Wiederherstellen.
6. US-10.1 + US-10.2: G/R/H als Layer.

### Abhängigkeitsgraph

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

### Teststrategie

Pyramide, angewandt vor allem in Phase A:

| Ebene | Zweck | Scope |
|---|---|---|
| Unit | Einzelregel-Anwendung, Idempotenz, Ambiguitäts-Erkennung, Parser-Heuristik an DOCX-Paragraph-Fixtures | klein, schnell |
| Integration | End-to-End DOCX → TEI → (Errata) → TEI-final → JSON, Ground-Truth-Vergleich pro Korrektur | mittel |
| Regression | Eine Acceptance pro Review-Korrektur: `alt` nicht vorhanden + `neu` vorhanden an Position X | ein Test pro Korrektur |
| Invarianten | RelaxNG-Validierung, Glossenzähler 13, 7 Vers-`<div>`, keine leeren `<seg>`, keine orphan `<lb/>` | global |

CSS-Bugs werden nicht automatisiert getestet — stattdessen Screenshot-Vergleich als Abnahme.

### Datei-Eingriffe pro Phase

**Phase A.** TEI über Pipeline regenerieren (keine manuellen Edits). CSS-Fixes in `docs/index.html` vor Zeile 867: `.sources-content { overflow-y: auto; min-height: 0; }`, `.sources-panel.collapsed { width: 0; overflow: hidden; border: none; }`, Split-View-Regeln entkoppeln. Manuelle End-to-End-Prüfung aller 32 Toggle-Kombinationen.

**Phase B.** BUG-11.4: `mask-image`/`linear-gradient` auf `.sources-content` entfernen. BUG-11.5: `.source-german` per `[data-source-language]` stylen, Pipeline-Feld `source_language` aus `<quote xml:lang>` extrahieren. US-1.3-Ext: `toggleNhd()` toggelt zusätzlich Klasse auf `#sources-panel`.

**Phase C.** US-9.2: `<lb/>`-Elemente im TEI, Parser erkennt DOCX-Zeilenumbrüche. US-9.1: `renderVerses()` um Zeilen-Modus erweitern, CSS-Grid-Row pro Zeile, Bindestriche am Zeilenende aus Daten entfernen. US-8.1: Panel-Registry (`registerPanelContent(def)` mit `id`, `label`, `render(containerEl)`), `main-container` auf CSS-Grid, State `panelAssignment`, URL-Hash-Persistenz erweitern. US-10.1: Siglen-Pool um G/R/H als eigene Gruppe, `updateSourceHighlights()` nutzt vorhandene Sigle-Datenstruktur.

### Stand pro Story (Stand 2026-04-16, Branch `iteration-2-pfeifer-review`)

| Story | Phase | Status | Nachweis |
|---|---|---|---|
| US-12.1 Quellen-Übersetzungen (11 Korrekturen) | A | done | `PFEIFER_CORRECTIONS` in `parse_probeseite.py` |
| US-12.2 Haupttext + nhd. (10 Korrekturen) | A | done | `PFEIFER_CORRECTIONS` |
| US-12.3 V6-Glossen-Reklassifikation | A | done | Parser-Heuristik, Glossen 14 → 13 |
| BUG-11.1 Split-Toggle | A | done | `efd7422` |
| BUG-11.2 Sources-Panel-Scroll | A | done | `efd7422` |
| BUG-11.3 ×-Button | A | done | `efd7422`, Iteration 2 ersetzt durch Slot-System |
| BUG-11.4 Kontrast-Fade | B | done | `f2eb99d`, `mask-image` entfernt |
| BUG-11.5 Kursiv nach Sprache | B | done | `f2eb99d`, Pipeline `source_language`, CSS-Regeln |
| US-1.3-Erweiterung Quellen-Toggle | B | done | `f2eb99d`, Taste Q, Default an, URL-Hash `qnhd` |
| US-8.1 Panel-Dropdown pro Feld | C | done | `53de31f`, Slot-System mit 9-Eintrag-Pool |
| US-8.2 Schließen + Wiederherstellen | C | done | `53de31f`, × pro Slot + Restore-Bar |
| US-8.3 Content-Registry | C | done | `53de31f`, `POOL`-Objekt, deklarativ erweiterbar |
| US-9.1 Zeilengetreue nhd.-Übersetzung | C | done | TEI `<lg type="line-faithful">`, Edition rendert `.nhd-line` pro Zeile |
| US-9.2 TEI-Zeilenstruktur Grundtext | C | done | `<ab n="X">` pro Notker-Zeile, `line_n` in JSON, `data-line` im Frontend; echte Handschriften-Zeilenumbrüche der CSg 0021 weiterhin nur via DOCX abgeleitet |
| US-9.3 Vers-Anker für nhd.-Zeilen | C | done | Zeilen pro Vers extrahiert, kein Vers-Drift |
| US-10.1 Psalter-Filter | C | done | G + R + H als eigene Filter-Gruppe |
| US-10.2 Siglen-Semantik (R-Disambiguierung) | C | done | `disambiguate_sigles()` in `tei_to_json.py`; Bestätigung durch Auftraggeber offen |
| Cross-Verse-Hyphen im TEI verkettet | — | done | `chain_cross_verse_hyphens()` in `build_tei.py`, V1–2 `han-` + V3–5 `gta` mit `@part`/`@next`/`@prev` |
| Whitespace-Normalisierung | — | done | `normalize_whitespace_in_text_nodes()` in `parse_probeseite.py` |
| Errata-Layer entfernt (Refactor) | — | done | `f49ff58`, 779 Zeilen weg, Korrekturen jetzt in `PFEIFER_CORRECTIONS` |

**Test-Bilanz:**

- `tests/test_gloss_classification.py`: 6 / 6 grün
- `scripts/test_pipeline.py`: 29 / 29 grün, 0 Warnings
- Browser-Smoke-Test (Playwright): 0 JS-Errors, R-Disambiguierung verifiziert (`src:R` → 16 Patristik-Sections, `psa:R` → 13 Psalter-Sections, keine Überlappung)

**Offen für Iteration 3:**

- Echte Handschriften-Zeilenumbrüche der CSg 0021 (bislang aus DOCX-Tabellenzeilen abgeleitet); mit Tax/Sehrt-Markierung oder Facsimile-Ableitung verfeinerbar.
- R-Disambiguierung: Bestätigung der Best-Effort-Heuristik durch den Auftraggeber.
- Augustinus-2-Korrekturen V3–5 / V6: wegen BUG-11.2 in Iteration 1 nicht prüfbar, Nachreichung erwartet.

## Iteration 2c — Follow-up (2026-04-16)

Befunde aus der Iteration-2b-Auslieferung, alle ohne neue Stories adressierbar und direkt umgesetzt.

| Befund | Status | Nachweis |
|---|---|---|
| Quellen-Filter doppelt gerendert nach Slot-Re-Mount | done | `renderSourceFilters()` leert Container |
| Pool-Templates mit festen Pixel-Breiten (Iteration-1-Altlast) | done | `width: 100%; height: 100%` |
| `<th>` im Psalmtext-Vergleich überlagert Content beim Scrollen | done | `z-index: 2` + Box-Shadow |
| OSD-Viewer leer nach Slot-Swap | done | `onMount` ruft `viewport.applyConstraints` |
| Toggle „Quellen-Übersetzung" im falschen Kontext | done | verschoben in Quellen-Panel-Header |
| Schichten-Toggle wirkt nicht bei geschlossenem Edition-Slot | done | `ensurePoolVisible('edition')` |
| Quellen-nhd-Toggle wirkt nicht bei geschlossenem Quellen-Slot | done | `ensurePoolVisible('sources')` |
| Quellen-/Psalter-Filter untereinander statt nebeneinander | done | `flex-direction: row`, `.source-filter-group` |
| Redundante Zeilen im Quellen-Header | done | Merge zu einer Zeile, Aktion via `margin-left: auto` |
| Toolbar-Gruppenlabels verschwenden Platz | done | entfernt, Padding/Font reduziert |
| Fünf `<l>`-Zeilen-Korrekturen griffen nicht (Fließtext-Replace) | done | Patterns für beide Kontexte in `PFEIFER_CORRECTIONS` |
| Cross-Verse-Drift: „erlaubte es" bei V3 statt V1–2 | done | `redistribute_crossverse_nhd()` in `build_tei.py` |
| Psalm-Nav 1/3/50/100/150 wirkt begehbar | done | `.disabled`-Class + `cursor: not-allowed` |
| Diagnose meldet Glossenzahl 13/14 als Problem | done | Erwartung auf 13 korrigiert |
| Diagnose meldet V7 „irgân-" als Problem (bekannte Limitation) | done | aus Warn-Liste gefiltert |
| Leeres Verses-Panel bei 0 aktiven Schichten verwirrt | done | Info-Block + „Alle Schichten einblenden"-Button |
| Promptotyping-Vault nicht öffentlich zugänglich | done | `docs/vault.html` + `scripts/sync_vault.py` |

Tests: 29 / 29 Pipeline-Tests grün, Pipeline idempotent.

## Verknüpfungen

- [[INDEX]] — Navigation und Begriffslexikon
- [[project]] — Projektidentität, Phasen und Demonstrationszweck
- [[design]] — Design-Entscheidungen, die diese Anforderungen umsetzen
- [[architecture]] — Pipeline und Datenmodell, die diese Stories tragen
- [[journal]] — Chronologie der Sessions
- [[offene-korrekturen]] — Tech-Debt, der über die Iteration-2-Stories hinaus offen blieb
