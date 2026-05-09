---
title: "Editionsinterface — Designhaltung und Designsystem"
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
  - "[[Information Visualisation]]"
  - "[[Scholar-Centered Design]]"
  - "[[Synoptic Edition]]"
related:
  - "[[INDEX]]"
  - "[[project]]"
  - "[[specification]]"
  - "[[data]]"
  - "[[architecture]]"
---

# Editionsinterface — Designhaltung und Designsystem

> **Stand:** Dieses Dokument beschreibt das Design nach Iteration 2 (Slot-System, Panel-Dropdown, zeilengetreue Synopse, Parallel-Layout Haupttext | nhd.). Die Iterations-Geschichte und die getroffenen Designentscheidungen pro Iteration sind in [[specification]] dokumentiert; der aktuelle Umsetzungsstand pro Story ebenfalls dort.

## Leitgedanke

Der Prototyp vermittelt Gutachtern eines Drittmittelantrags: *Diese digitale Edition löst ein reales philologisches Problem — die Schichtentrennung in Notkers Psalmenkommentar — auf eine Weise, die gedruckte Editionen nicht können.* Jede Designentscheidung dient diesem Demonstrationszweck.

Die zentrale editorische Leistung ist die Sichtbarmachung von Informationsschichten, die in der Handschrift verschränkt, in der Probeseite farbcodiert und in bisherigen Druckeditionen unaufgelöst geblieben sind. Das Interface trennt nach Textfunktion (Zitat/Übersetzung/Kommentar), nicht nach Sprache (lat./ahd.) — das ist die philologisch bedeutsamere Unterscheidung und der Kern der editorischen Entscheidung. Sprachbasierte Trennung wird als sekundäre Ansicht angeboten.

## 1. Synoptische Darstellung

Notkers Text ist ein Geflecht aus drei funktionalen Schichten (vgl. [[data#Textfunktionale Schichten]]):

| Schicht | Funktion | Handschrift | Probeseite |
|---|---|---|---|
| Psalmzitation | Notker zitiert den lat. Psalmvers | Rot | Olive (#806000) |
| Übersetzung | Notker überträgt ins Ahd. | Schwarz | Grün (#00B050) |
| Kommentar | Notker kommentiert exegetisch (ahd. + lat.) | Schwarz | Schwarz |

Drei Ansichtsmodi bauen aufeinander auf:

**Standardansicht (verschränkt).** Alle drei Schichten sichtbar, farblich differenziert, in Originalreihenfolge. Ein Vers entfaltet sich als Psalmzitat → Übersetzung → Kommentar. Der Gutachter sieht sofort die Mehrschichtigkeit.

**Gefilterte Ansichten (per Toggle).** Jede Schicht einzeln ab-/zuschaltbar. Ein Forscher, der die Exegese untersucht, blendet die Psalmzitation aus und sieht nur Kommentar.

**Zweispaltige Ansicht (lat./ahd.-Split).** Orthogonal zu den Schicht-Toggles. Trennt den sichtbaren Text nach Sprache in zwei synchron scrollende Spalten. Das ist das Demonstrationsfeature für Gutachter: ein Klick verwandelt den verschränkten Text in ein übersichtliches Nebeneinander.

## 2. Komponenten

### 2.1 Glossierung

Interlinearglossen aus Psalm 2 (vgl. [[data#Interlinearglossen-Inventar]]). Darstellung inline, eingerückt, in reduziertem Schriftgrad (0.85rem), Blaugrau. Per Toggle abschaltbar (Standard: AN). So erscheinen Glossen als das, was sie sind: eine Annotationsebene zwischen Zeile und Rand, weder Haupttext noch Fußnote.

### 2.2 Quellenapparat

Persistentes Panel links vom Haupttext. Begründung: Gutachter und Forscher lesen Quelle und Text gleichzeitig, nicht flüchtig per Tooltip.

Aufbau: Filterbereich oben (Checkboxen pro Sigle), darunter Quelleneinträge zum ausgewählten Vers mit Sigle, Quellenname, lateinischem Text und deutscher Übersetzung. Aktive Filter markieren zugehörige Haupttext-Zeilen mit farbigem Seitenstreifen.

Quellenfarben: A (Augustinus) = Blau, C (Cassiodor) = Grün, R (Remigius) = Orange, Br (Breviarium) = Violett. Diese Farben sind bewusst als dezente Seitenstreifen umgesetzt, um Interferenz mit den Textschicht-Farben zu minimieren. Das Überlagerungsrisiko bei mehreren gleichzeitig aktiven Filtern bleibt ein offener Testpunkt.

### 2.3 Facsimile-Anbindung

Rechtes Panel, ein-/ausklappbar, standardmäßig geöffnet (Gutachter sehen sofort Text + Handschrift). IIIF-Viewer für CSg 0021 (e-codices). Navigation ab Seite 11.

**Text-Bild-Synopse.** Versklick navigiert den Viewer zur korrekten Handschriftenseite (Seiten-Synopse, nicht Zeilensynopse). Mapping: Vers → Seite.

Einschränkung, die benannt werden muss: Auf einer dicht beschriebenen Handschriftenseite muss der Nutzer den Vers selbst finden. Zeilenverknüpfung wäre wünschenswert, erfordert aber manuelle Koordinaten-Annotation und übersteigt das Prototyp-Budget. Die Seiten-Synopse demonstriert das Prinzip und skaliert.

### 2.4 Neuhochdeutsche Übersetzung

Zwei Darstellungsmodi nebeneinander. In der Edition zeilengenau pro Notker-Zeile auf identischer Höhe (Iteration 2 / US-9). Im Pool als Fließtext-Lese-Ansicht mit aufgelösten Bindestrichen. Toggle steuert Sichtbarkeit auch im Quellenapparat (Iteration 2 / US-1.3-Erweiterung).

### 2.5 Navigation

**Versnavigation.** Verse nummeriert am linken Rand. Klick scrollt und aktualisiert das Quellen-Panel. Aktiver Vers erhält subtilen Hintergrund-Highlight.

**Psalmleiste.** Horizontale Leiste im Header, Psalm 1–150. Nur Psalm 2 aktiv, alle anderen ausgegraut. Rein visuelles Skalierungssignal für Gutachter.

**Editions-Seitenumbrüche.** Referenzen R10–R13 (Tax/Sehrt-Edition) als dezente Randnotiz.

## 3. Layout und Designsystem

### 3.1 Gesamtlayout (Slot-System)

Dreispaltiges Grundraster mit drei generischen Slots A · B · C. Jeder Slot hat einen Auswahl-Dropdown im Header und einen Schließen-Button. Die Default-Belegung entspricht dem Iteration-1-Layout: A=Quellen, B=Notkers Edition, C=Facsimile.

Aus dem Pool kann pro Slot ein Inhaltstyp gewählt werden:

| Pool-Eintrag | Inhalt | Quelle |
|---|---|---|
| Quellen | Patristischer Apparat (A/C/R/Br + Filter) | bestehender Apparat |
| Notkers Text | Edition mit Schichten-Toggles | Haupttext |
| Nhd. Übersetzung | Arbeitsübersetzung als Fließtext-Lese-Ansicht | aufgelöste Bindestriche |
| Wiener Notker | Paralleltext ÖNB Cod. 2681 | NEU als eigener Slot |
| Psalter G | Gallicanum als zusammenhängender Psaltertext | NEU |
| Psalter R | Romanum | NEU |
| Psalter H | Hebraicum | NEU |
| Handschrift Notker | IIIF-Facsimile CSg 0021 | bestehend |
| Anmerkungen | Siglen-Schlüssel + editorische Hinweise | NEU |
| Psalmtext-Vergleich | Synoptische Tabelle aller fünf Zeugen | NEU |

Single-Instance-Pool: jeder Eintrag existiert genau einmal im DOM. Pickt man in Slot B einen Eintrag, der schon in A montiert ist, tauschen die Slots transparent ihren Inhalt. Geschlossene Slots erscheinen als Buttons in einer Wiederherstellungsleiste am unteren Bildschirmrand.

Panels durch verschiebbare Trenner (drag-to-resize). Header mit Projekttitel und Psalmleiste, Footer mit Zitierhinweis, Projektkontext, Lizenz.

Slot-Belegung wird im URL-Hash persistiert: `#slots=A:nhd,B:edition,C:psalter_g&closed=`.

### 3.2 Typografie

Editionstext in Serifenschrift (Gentium Book Plus via Google Fonts, Fallback Palatino → Georgia). Muss altgermanistische Sonderzeichen unterstützen (ȩ, û, ô, î, ê, â, é, á, ó, í). UI-Elemente (Toggles, Filter, Navigation) serifenlos, klein, funktional.

| Ebene | Größe | Verwendung |
|---|---|---|
| H1 | 1.5rem | Projekttitel |
| Psalmzitat | 1.1rem | QVARE FREMVERVNT GENTES |
| Haupttext | 1.0rem | Übersetzung, Kommentar |
| nhd. Übersetzung | 0.9rem | Arbeitsübersetzung des Auftraggebers |
| Glossen | 0.85rem | Interlinearglossen |
| UI-Labels | 0.8rem | Toggles, Filter, Fußzeile |

### 3.3 Farbsystem

Drei Farblogiken existieren im Projekt (vgl. [[data#Drei überlagernde Farblogiken]]). Das UI definiert die dritte.

**Textschicht-Farben:**

| Schicht | Farbe | HSL | Begründung |
|---|---|---|---|
| Psalmzitation | Terracotta | hsl(15, 60%, 40%) | Reminiszenz an rote Tinte der Handschrift |
| Übersetzung | Schwarzbraun | hsl(25, 30%, 18%) | Reminiszenz an schwarze Tinte, visuell Hauptstimme |
| Kommentar | Dunkelgrau | hsl(0, 0%, 35%) | Notkers eigene Stimme, lesbar aber nicht dominant |
| Glossen | Blaugrau | hsl(210, 20%, 50%) | Eigene Farbe, abgesetzt vom Textfluss |

**Funktionsfarben:** Aktiver Vers hsl(40, 15%, 96%) mit Terracotta-Akzentlinie links, nhd. Übersetzung hsl(0, 0%, 55%), Hauptfläche weiß, Quellen-Panel hsl(0, 0%, 97.5%), Facsimile-Panel schwarz.

**Gesamtästhetik.** Seriös-akademisch. Neutrale Basis, Farbe ausschließlich funktional. Kein Dekor, keine Gradienten. Das Interface soll wie ein philologisches Werkzeug aussehen.

### 3.4 Responsivität

Primäre Zielgröße: Laptop (1280–1440 px). ≥1200px drei Panels, 900–1199px zwei Panels, <900px Einzelpanel mit Tabs. Mobile ist kein Ziel.

## 4. Interaktion

### 4.1 Toggle-System

Sechs Toggles in zwei orthogonalen Gruppen.

**Gruppe A — Textschichten:** Psalmzitation (1), Übersetzung (2), Kommentar (3), Glossen (4). Alle initial AN.

**Gruppe B — Darstellung:** nhd. Übersetzung (N), lat./ahd. trennen (L). Beide initial AUS.

Die Gruppen sind frei kombinierbar. Beispielszenarien:

| Ziel | Gruppe A | Gruppe B |
|---|---|---|
| Erstbesuch | Alle AN | Alle AUS |
| Nur den Psalm | Nur Psalmzitat | — |
| Zweisprachig | Psalmzitat + Übersetzung | lat./ahd. Split AN |
| Ohne Ahd.-Kenntnisse | Alle AN | nhd. AN |

Aktive Toggles farblich gefüllt (Pillbutton). Beim Umschalten Opacity-Übergang, kein hartes Erscheinen/Verschwinden.

### 4.2 Zustandsmodell

```
activeVerse: number (1–13)
visibleLayers: Set<'psalm_citation' | 'translation' | 'commentary' | 'glosses'>
showNhd: boolean
splitLanguages: boolean
sourceFilter: Set<string>
panelState: { sources: 'open' | 'closed', facsimile: 'open' | 'closed' }
```

**URL-Persistenz.** Zustand wird in URL-Fragment kodiert. Ermöglicht dem Antragsteller, Gutachter gezielt auf bestimmte Verse mit bestimmter Toggle-Konfiguration zu verlinken. Das ist kein Luxus, sondern direkt relevant für die Begutachtungssituation.

### 4.3 Visueller Rhythmus eines Verses

```
┌─────────────────────────────────────────┐
│ 1                                        │  Versnummer
│ QVARE FREMVERVNT GENTES.               │  Psalmzitation (Terracotta)
│ Ziu grís-cramoton an christum ebraicȩ   │  Übersetzung (Schwarzbraun)
│ gentes?                                  │
│   iúdon diêt → Juden Volk              │  Glosse (Blaugrau, eingerückt)
│ Et populi meditati sunt inania.         │  Psalmzitation
│ Vnde ziu dâhton sîne liûte ardingun.   │  Übersetzung
│ ín ze irloschenne? Sie dâhton           │
│ des ín ubelo spuên solta.              │  Kommentar (Mittelgrau)
│ Warum wüteten an Christus die           │  nhd. (optional, hellgrau kursiv)
│ hebräischen Völker? ...                  │
│                                     R10 │  Editions-Seitenreferenz
└─────────────────────────────────────────┘
```

## 5. Informationshierarchie

Fünf Ebenen, geordnet nach visueller Prominenz. Progressive Disclosure: Standardzustand zeigt Ebene 1–3, Ebene 4 wird aktiv zugeschaltet. Ein Gutachter sieht beim ersten Laden ein lesbares Interface, nicht ein überfrachtetes.

| Ebene | Inhalt | Sichtbarkeit |
|---|---|---|
| 1 | Haupttext (Psalmzitation, Übersetzung, Kommentar) | Immer sichtbar, Zentrum |
| 2 | Interlinearglossen | Eingebettet, abschaltbar |
| 3 | Quellenapparat | Flankierend, persistent |
| 4 | nhd. Übersetzung, Facsimile | Optional, zuschaltbar |
| 5 | Editions-Seitenumbrüche, Zitierhinweise | Kontext, statisch |

## 6. Negative Selbstdefinition

Was die Designhaltung bewusst nicht leistet, gehört zur Identität des Prototyps. Das Interface ist nicht responsive auf Mobile. Es bietet keine zeilengenaue Bild-Text-Synopse (zu hoher Annotationsaufwand). Es vermischt Schichtfarbe und Filterfarbe nicht in einer Hervorhebung — Schichtfarbe trägt den Text, Filterfarbe trägt einen Seiten-Stripe. Es führt keine animierten Übergänge ein, die Lesefluss stören würden. Es zeigt keine Statistik-Sidebar (keine „Zeichenzahl", keine „Schichtverteilung") — das wären Metriken, die vom Lesegegenstand ablenken.

## 7. Anschluss an den Action-Layer

Diese Designhaltung ist deklarativ. Die imperative Übersetzung in Designprinzipien für den Coding-Agenten gehört in `CLAUDE.md` im Repo-Root, das auf dieses Dokument als Wertequelle verweist. Kandidaten für imperative Sätze, die `CLAUDE.md` aus dieser Haltung ableiten könnte: „Generiere CSS, das Schichtfarbe und Filterfarbe trennt." „Wähle bei Layout-Fragen das philologische Werkzeug, nicht das marketing-orientierte Interface." „Nutze Farbe nur funktional, nie dekorativ." Die imperative Form lebt nicht hier.

## Verknüpfungen

- [[INDEX]] — Navigation und Begriffslexikon
- [[project]] — Projektidentität und Demonstrationszweck
- [[specification]] — User Stories, die dieses Design umsetzt; Iterations-Geschichte und Designentscheidungen pro Iteration
- [[data]] — Datengrundlage für Farblogik und Glosseninventar
- [[architecture]] — Stack, Datenmodell, Pipeline
