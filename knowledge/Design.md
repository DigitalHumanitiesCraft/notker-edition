---
type: design
created: 2026-02-27
updated: 2026-03-23
status: draft
tags: [notker, ui-design, edition-interface]
---

# Design: Notker Psalmenkommentar – Editionsinterface

## Leitgedanke

Der Prototyp muss Gutachtern eines Drittmittelantrags in wenigen Minuten vermitteln: *Diese digitale Edition löst ein reales philologisches Problem — die Schichtentrennung in Notkers Psalmenkommentar — auf eine Weise, die gedruckte Editionen nicht können.* Jede Designentscheidung dient diesem Demonstrationszweck.

Die zentrale editorische Leistung ist nicht die Textpräsentation allein, sondern die **Sichtbarmachung von Informationsschichten**, die in der Handschrift verschränkt, in der Probeseite farbcodiert und in bisherigen Druckeditionen unaufgelöst geblieben sind.

---

## 1. Editionsinterface-Konzept

### 1.1 Synoptische Darstellung

Notkers Text ist ein **Geflecht aus drei funktionalen Schichten** (vgl. [[Probeseite Analyse#Farbcodierung]]):

| Schicht | Funktion | In der Handschrift | In der Probeseite |
|---|---|---|---|
| Psalmzitation | Notker zitiert den lat. Psalmvers | Rot (= Latein) | Olive (#806000) |
| Übersetzung | Notker überträgt den Psalmvers ins Ahd. | Schwarz (= Deutsch) | Grün (#00B050) |
| Kommentar | Notker kommentiert exegetisch (ahd. + lat.) | Schwarz (= Deutsch) | Schwarz (default) |

Die Handschrift trennt nach **Sprache** (rot/schwarz). Die Probeseite trennt nach **Textfunktion** (Zitat/Übersetzung/Kommentar). Das UI muss die funktionale Logik umsetzen, weil sie die philologisch bedeutsamere Unterscheidung ist. Sprachbasierte Trennung (lat./ahd.) wird als sekundäre Ansicht angeboten.

**Standardansicht (verschränkt):** Alle drei Schichten sind sichtbar, farblich differenziert, in der Reihenfolge des Originaltextes. So liest man Notker, wie er geschrieben hat — ein Vers entfaltet sich als Psalmzitat → Übersetzung → Kommentar. Der Gutachter sieht sofort die Komplexität und Mehrschichtigkeit.

**Gefilterte Ansichten (per Toggle):** Jede Schicht einzeln ab- oder zuschaltbar. Ein Gutachter, der nur wissen will, *was* Notker aus dem Psalm macht, blendet den Kommentar aus und sieht nur Zitat + Übersetzung. Ein Forscher, der die Exegese untersucht, blendet die Psalmzitation aus und sieht nur Kommentar.

**Zweispaltige Ansicht (lat./ahd.-Split):** Orthogonal zu den Schicht-Toggles. Trennt den sichtbaren Text nach Sprache in zwei synchron scrollende Spalten. Funktioniert unabhängig davon, welche Schichten aktiv sind. Das ist das "Killer-Feature" für Gutachter: ein Klick verwandelt den verschränkten Text in ein übersichtliches Nebeneinander.

### 1.2 Glossierung

14 Interlinearglossen in Psalm 2 (vgl. [[Probeseite Analyse#Interlinearglossen]]). Sie stehen zwischen Token und Kommentar: Kurzübersetzungen einzelner lateinischer Fachtermini.

**Darstellungsprinzip:** Glossen erscheinen **inline** an der Position, an der sie im Textfluss stehen. Sie sind visuell als Annotationstyp erkennbar — nicht als Haupttext, nicht als Fußnote, sondern als "dritte Ebene" zwischen Zeile und Rand.

**Konkrete Umsetzung:**

```
[Haupttextzeile]
  penêmida → Vorherbestimmung          ← Glosse, eingerückt, kleinere Schrift
[nächste Haupttextzeile mit prȩdistinationem]
```

Die Glosse zeigt: ahd. Glossenwort, Pfeil, nhd. Übersetzung. Der lateinische Bezugsbegriff ist im Haupttext an der darüber- oder darunterliegenden Stelle erkennbar. Eine explizite Verbindungslinie wäre visuell überladen.

**Toggle:** Glossen sind separat ein-/ausblendbar ([[Anforderungen#Epic 4|US-4.2]]). Standard: AN. Wenn ausgeblendet, fließt der Haupttext ohne Unterbrechung.

### 1.3 Navigation

**Versnavigation:** 13 Verse, nummeriert am linken Rand. Klick auf eine Versnummer scrollt den Vers in den sichtbaren Bereich und aktualisiert das Quellen-Panel. Der aktive Vers erhält einen subtilen Hintergrund-Highlight.

**Psalmnavigation (Skalierbarkeit):** Im Header eine horizontale Leiste mit Psalm-Nummern 1–150. Nur Psalm 2 ist aktiv, alle anderen sind ausgegraut. Das signalisiert Gutachtern: die Vision skaliert. Kein funktionaler Aufwand, nur visuelles Signal.

**Editions-Seitenumbrüche:** Die Seitenreferenzen R10–R13 (Tax/Sehrt-Edition) werden als dezente Randnotiz an der entsprechenden Stelle im Text markiert, damit Forscher von der digitalen Edition in die gedruckte springen können.

### 1.4 Quellenapparat

**Sidebar-Prinzip:** Quellen werden nicht als Popup oder Tooltip gezeigt, sondern in einem persistenten Panel links vom Haupttext. Begründung: Gutachter und Forscher wollen Quelle und Text **gleichzeitig** lesen, nicht flüchtig einblenden.

**Aufbau des Quellen-Panels:**
1. **Filterbereich** (oben): Checkboxen pro Quellen-Sigle (A, C, R, Br). Aktive Filter heben die zugehörigen Stellen im Haupttext farblich hervor.
2. **Quelleneinträge** (darunter): Pro aktiver Quelle zum ausgewählten Vers ein Block mit:
   - Sigle und vollständiger Quellenname (z.B. "C — Cassiodor, Expositio Psalmorum")
   - Lateinischer Originaltext
   - Deutsche Übersetzung (Philipps Arbeit)

**Quellen-Highlight im Haupttext:** Wenn ein Quellenfilter aktiv ist, werden die Haupttext-Zeilen, die mit dieser Quelle assoziiert sind (über `source_sigles`), mit einem dezenten farbigen Seitenstreifen markiert. Farbzuordnung pro Quelle:

| Sigle | Farbe (Vorschlag) |
|---|---|
| A (Augustinus) | Blau |
| C (Cassiodor) | Grün |
| R (Remigius) | Orange |
| Br (Breviarium) | Violett |

### 1.5 Facsimile-Anbindung

**Panel rechts**, ein-/ausklappbar. Zeigt das Digitalisat von CSg 0021 (e-codices) via IIIF-Viewer. Standardmäßig **eingeklappt**, um auf Laptop-Bildschirmen Platz für Text und Quellen zu lassen. Ein Gutachter, der die Handschrift sehen will, klappt es auf — das ist ein bewusster Akt, kein Default.

Zoom und Pan über den eingebetteten Viewer. Navigation zwischen den relevanten Seiten (ab Seite 11). Keine Verknüpfung auf Zeilenebene im Prototyp (wäre wünschenswert, aber Aufwand übersteigt Budget).

### 1.6 Neuhochdeutsche Übersetzung

Philipps nhd. Arbeitsübersetzung ist einblendbar per Toggle. Darstellung: **unterhalb jedes Verses** als kursiver Block in gedämpftem Grauton. Nicht als eigene Spalte (zu viel Platz), nicht als Tooltip (zu flüchtig).

Standard: AUS. Gutachter ohne Althochdeutsch-Kenntnisse können sie bei Bedarf zuschalten.

---

## 2. UI-Architektur und Designsystem

### 2.1 Gesamtlayout

Dreispaltiges Grundraster mit flexiblen Proportionen:

```
┌─────────────────────────────────────────────────────────┐
│  HEADER                                                  │
│  Projekttitel · Psalm-Leiste [1 ··· 2 ··· 150]          │
├───────────┬───────────────────────────┬─────────────────┤
│           │                           │                 │
│  QUELLEN  │      HAUPTTEXT            │   FACSIMILE     │
│  ~25%     │      ~50%                 │   ~25%          │
│           │                           │   (einklappbar) │
│           │  ┌─────────────────────┐  │                 │
│           │  │ Toggle-Toolbar      │  │                 │
│           │  ├─────────────────────┤  │                 │
│           │  │ Vers 1              │  │                 │
│           │  │ Vers 2              │  │                 │
│           │  │ ...                 │  │                 │
│           │  └─────────────────────┘  │                 │
│           │                           │                 │
├───────────┴───────────────────────────┴─────────────────┤
│  FOOTER                                                  │
│  Zitierhinweis · Projektkontext · Lizenz                 │
└─────────────────────────────────────────────────────────┘
```

Panels sind durch verschiebbare Trenner getrennt (Drag-to-resize). Quellen-Panel und Facsimile-Panel können unabhängig ein-/ausgeklappt werden. Wenn beide eingeklappt sind, nimmt der Haupttext die volle Breite ein.

### 2.2 Typografie

**Editionstext (Haupttext):** Serifen-Schrift. Akademische Konvention, erhöht Lesbarkeit langer Textpassagen. Muss altgermanistische Sonderzeichen unterstützen: ȩ, û, ô, î, ê, â, é, á, ó, í. Kandidaten: Junicode, Gentium Plus, oder ein systemnaher Fallback (Georgia, Palatino).

**Psalmzitation:** Gleiche Serifenschrift, etwas größerer Schriftgrad oder Kapitälchen für VERSALIEN-Psalmzitate. Farblich abgesetzt (warm-rötlich).

**Interlinearglossen:** Gleiche Serifenschrift, um ~20% reduzierter Schriftgrad. Einrückung, visuell als Annotation erkennbar.

**Quellenapparat:** Gleiche Serifenschrift wie Editionstext. Lateinischer Text und deutsche Übersetzung visuell getrennt (lat. regulär, dt. kursiv oder umgekehrt).

**nhd. Übersetzung:** Kursiv, gedämpfter Grauton. Gleiche Serifenschrift.

**UI-Elemente (Toggles, Filter, Navigation):** Serifenlose Schrift. Klein, funktional, soll nicht vom Editionstext ablenken. Labels in Deutsch.

**Schriftgrößen-Hierarchie:**

| Ebene | Relativ | Verwendung |
|---|---|---|
| H1 | 1.5rem | Projekttitel (nur Header) |
| Psalmzitat (Versalien) | 1.1rem | QVARE FREMVERVNT GENTES |
| Haupttext | 1.0rem (Basis) | Übersetzung, Kommentar |
| Glossen | 0.85rem | Interlinearglossen |
| nhd. Übersetzung | 0.9rem | Philipps Arbeitsübersetzung |
| UI-Labels | 0.8rem | Toggles, Filter, Fußzeile |

### 2.3 Farbsystem

Drei Farblogiken existieren im Projekt (vgl. [[Domänenwissen#Drei überlagernde Farblogiken]]). Das UI definiert die dritte:

**Primärfarben (Textschichten):**

| Schicht | Farbe | HSL-Bereich | Begründung |
|---|---|---|---|
| Psalmzitation | Terracotta / warmes Rot | hsl(15, 60%, 40%) | Reminiszenz an die rote Tinte der Handschrift |
| Übersetzung | Dunkles Schwarzbraun | hsl(30, 20%, 15%) | Reminiszenz an die schwarze Tinte; visuell "Hauptstimme" |
| Kommentar | Mittelgrau | hsl(0, 0%, 45%) | Tritt zurück, dominiert nicht |
| Interlinearglossen | Gedämpftes Blaugrau | hsl(210, 20%, 50%) | Eigene Farbe, klar abgesetzt vom Textfluss |

**Sekundärfarben (Quellen-Highlighting):**

| Sigle | Farbe | Verwendung |
|---|---|---|
| A (Augustinus) | Blau, dezent | Seitenstreifen im Haupttext bei aktivem Filter |
| C (Cassiodor) | Grün, dezent | dto. |
| R (Remigius) | Orange, dezent | dto. |
| Br (Breviarium) | Violett, dezent | dto. |

**Funktionsfarben:**

| Element | Farbe |
|---|---|
| Aktiver Vers (Hintergrund) | Sehr helles Warmgrau, hsl(40, 10%, 96%) |
| nhd. Übersetzung | Hellgrau, hsl(0, 0%, 55%) |
| Hintergrund Hauptfläche | Weiß |
| Hintergrund Quellen-Panel | Sehr helles Grau, hsl(0, 0%, 97%) |
| Hintergrund Facsimile-Panel | Schwarz (IIIF-Viewer-Konvention) |

**Gesamtästhetik:** Seriös-akademisch. Neutrale Basis, Farbe ausschließlich funktional. Kein Dekor, keine Illustrationen, keine Gradienten. Das Interface soll wie ein philologisches Werkzeug aussehen, nicht wie eine App.

### 2.4 Responsivität

**Primäre Zielgröße:** Laptop-Bildschirm (1280–1440px Breite). Der Prototyp wird Gutachtern auf einem Laptop oder großen Monitor präsentiert, nicht auf Mobilgeräten.

**Breakpoints:**

| Breite | Layout |
|---|---|
| ≥ 1200px | Drei Panels nebeneinander (Standard) |
| 900–1199px | Zwei Panels (Quellen oder Facsimile eingeklappt) |
| < 900px | Einzelpanel mit Tab-Navigation (Haupttext / Quellen / Facsimile) |

Mobile-Optimierung ist für den Prototyp kein Ziel. Die schmalen Breakpoints sind ein Fallback, kein Feature.

---

## 3. Informationshierarchie

Die Edition hat **sechs Informationstypen** (vgl. [[Domänenwissen#Textfunktionale Schichten]]). Sie sind hierarchisch geordnet nach visueller Prominenz:

```
Ebene 1 (immer sichtbar, Zentrum)
  └── Haupttext: Psalmzitation + Übersetzung + Kommentar
        │
        ├── 1a. Psalmzitation (farblich hervorgehoben, Versalien)
        ├── 1b. Übersetzung (farblich hervorgehoben, Fließtext)
        └── 1c. Kommentar (zurückgenommen, Fließtext)

Ebene 2 (eingebettet, abschaltbar)
  └── Interlinearglossen (inline, kleiner, eigene Farbe)

Ebene 3 (flankierend, persistent)
  └── Quellenapparat (Sidebar links, aktualisiert bei Vers-Klick)

Ebene 4 (optional, zuschaltbar)
  ├── nhd. Übersetzung (unterhalb der Verse, per Toggle)
  └── Facsimile (Panel rechts, ein-/ausklappbar)

Ebene 5 (Kontext, statisch)
  └── Editions-Seitenumbrüche, Zitierhinweise, Einleitungstext
```

**Prinzip: Progressive Disclosure.** Der Standardzustand zeigt Ebene 1–3. Ebene 4 wird aktiv zugeschaltet. So sieht ein Gutachter beim ersten Laden ein lesbares Interface, nicht ein überfrachtetes. Die Komplexität entfaltet sich bei Interaktion.

### Visueller Rhythmus innerhalb eines Verses

Ein einzelner Vers ist die atomare Einheit der Edition. So baut er sich visuell auf:

```
┌─────────────────────────────────────────┐
│ 1  ← Versnummer (Randnotiz)             │
│                                          │
│ QVARE FREMVERVNT GENTES.               │ ← Psalmzitation (Terracotta)
│ Ziu grís-cramoton an christum ebraicȩ   │ ← Übersetzung (Schwarzbraun)
│ gentes?                                  │
│   iúdon diêt → Juden Volk              │ ← Glosse (Blaugrau, eingerückt)
│ Et populi meditati sunt inania.         │ ← Psalmzitation
│ Vnde ziu dâhton sîne liûte ardingun.   │ ← Übersetzung
│ ín ze irloschenne? Sie dâhton           │
│ des ín ubelo spuên solta.              │ ← Kommentar (Mittelgrau)
│                                          │
│ Warum wüteten an Christus die           │ ← nhd. Übersetzung (optional,
│ hebräischen Völker? ...                  │    hellgrau kursiv)
│                                     R10 │ ← Editions-Seitenreferenz
└─────────────────────────────────────────┘
```

---

## 4. Interaktionskonzept

### 4.1 Toggle-System

Sechs Toggles, gruppiert in einer Toolbar über dem Haupttext:

**Gruppe A — Textschichten (Was sehe ich?)**

| Toggle | Initialzustand | Tastenkürzel |
|---|---|---|
| Psalmzitation | ● AN | 1 |
| Übersetzung | ● AN | 2 |
| Kommentar | ● AN | 3 |
| Interlinearglossen | ● AN | 4 |

**Gruppe B — Darstellung (Wie sehe ich es?)**

| Toggle | Initialzustand | Tastenkürzel |
|---|---|---|
| nhd. Übersetzung | ○ AUS | N |
| lat./ahd. trennen | ○ AUS | L |

**Verhalten:** Die Toggles der Gruppe A und B sind orthogonal. Beispielkombinationen:

| Szenario | Gruppe A | Gruppe B | Ergebnis |
|---|---|---|---|
| Erstbesuch | Alle AN | Alle AUS | Volltext, verschränkt, ohne nhd. |
| "Nur den Psalm zeigen" | Nur Psalmzitat AN | — | Nur die lat. Psalmverse sichtbar |
| "Zweisprachig" | Psalmzitat + Übersetzung AN | lat./ahd. trennen AN | Zwei Spalten: lat. Psalm links, ahd. Übersetzung rechts |
| "Ich verstehe kein Ahd." | Alle AN | nhd. AN | Volltext mit nhd. Übersetzung unter jedem Vers |

**Visuelles Feedback:** Aktive Toggles sind farblich gefüllt (Pillbutton-Stil). Beim Umschalten animiert der Text sanft (Opacity-Übergang, kein hartes Erscheinen/Verschwinden).

### 4.2 Vers-Interaktion

| Aktion | Auslöser | Wirkung |
|---|---|---|
| Vers auswählen | Klick auf Versnummer oder Textbereich | Quellen-Panel aktualisiert sich, Vers erhält Hintergrund-Highlight |
| Quellenfilter setzen | Checkbox im Quellen-Panel | Gefilterte Quellen angezeigt, zugehörige Haupttext-Zeilen markiert |
| Quellenfilter löschen | Checkbox erneut klicken oder "Alle"-Button | Filter entfernt, Markierung entfernt |

### 4.3 Panel-Interaktion

| Aktion | Auslöser | Wirkung |
|---|---|---|
| Quellen-Panel ein/aus | Klick auf Panel-Rand oder Shortcut | Panel klappt ein/aus, Haupttext nimmt den Platz ein |
| Facsimile ein/aus | Klick auf Panel-Rand oder Shortcut | dto. |
| Panel-Breite ändern | Drag am Trenner | Proportionen verschieben sich |

### 4.4 Zustandsmodell

Der gesamte UI-Zustand ist durch wenige Variablen beschrieben:

- `activeVerse: number` (1–13)
- `visibleLayers: Set<'psalm_citation' | 'translation' | 'commentary' | 'glosses'>`
- `showNhd: boolean`
- `splitLanguages: boolean`
- `sourceFilter: Set<string>` (Siglen)
- `panelState: { sources: 'open' | 'closed', facsimile: 'open' | 'closed' }`

**URL-Persistenz (nice-to-have):** Zustand in URL-Fragment kodiert, damit ein Gutachter einen bestimmten Vers mit bestimmter Toggle-Kombination als Link teilen kann.

---

## 5. Offene Designentscheidungen

### Entscheidung nötig vor Implementierung

| Nr. | Frage | Optionen | Empfehlung | Abhängigkeit |
|---|---|---|---|---|
| D-1 | Glossen: Inline oder Tooltip? | (a) Inline eingerückt, (b) Tooltip bei Hover, (c) Randnotiz | (a) Inline — sichtbarer, ehrlicher gegenüber dem Textcharakter | Philipps Feedback |
| D-2 | nhd. Übersetzung: Unter dem Vers oder als Spalte? | (a) Unterhalb, (b) Schmale Spalte rechts | (a) Unterhalb — platzsparender bei 3-Panel-Layout | Keiner |
| D-3 | Quellenfilter: Farbe pro Sigle oder einheitliche Hervorhebung? | (a) Individuelle Sigle-Farben, (b) Einheitlicher Highlight-Streifen | (a) Individuelle Farben — ermöglicht mehrere Filter gleichzeitig | Keiner |
| D-4 | Serifenschrift: Welche konkret? | Junicode, Gentium Plus, Palatino, Georgia | Gentium Plus (frei, gute ahd.-Zeichenabdeckung) — Fallback testen | Font-Rendering im Browser |

### Entscheidung abhängig von Scope-Klärung mit Philipp

| Nr. | Frage | Abhängigkeit |
|---|---|---|
| D-5 | Psalmtext-Vergleich: Eigener Tab oder Unter-Panel? | Scope/Budget-Entscheidung |
| D-6 | Wiener Notker: Paralleltext neben Haupttext oder eigener Tab? | Scope/Budget-Entscheidung |
| D-7 | Querverweise auf Bibelstellen: Eigener Reiter? Wo im Layout? | Daten fehlen; Philipps Lieferung abwarten |

### Entscheidung erst bei Implementierung

| Nr. | Frage | Grund |
|---|---|---|
| D-8 | Exakte Farbwerte für Textschichten | Muss am Bildschirm getestet werden (Kontrastverhältnisse, Barrierefreiheit) |
| D-9 | Animation bei Toggle-Umschaltung: Dauer und Art | Muss sich im Prototyp "richtig anfühlen" |
| D-10 | Facsimile-Panel: Standardbreite und -zustand | Abhängig von tatsächlicher Bildqualität des IIIF-Streams |

---

## Verknüpfungen

- [[Anforderungen]] — User Stories, die dieses Design umsetzt
- [[Probeseite Analyse]] — Datengrundlage für Farblogik und Glosseninventar
- [[Domänenwissen]] — Textschichten und Farblogiken
- [[Research Plan]] — Arbeitsphasen und Scope-Bewertung
- [[Technik]] — Paralleles Dokument für Stack, Datenmodell, Pipeline
