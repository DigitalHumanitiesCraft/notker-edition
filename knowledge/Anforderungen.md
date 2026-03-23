---
type: requirements
created: 2026-02-27
updated: 2026-03-23
tags: [notker, requirements]
---

# Anforderungen: Notker Psalmenkommentar Prototyp

## Kontext

Prototyp für Drittmittelantrag. Zielgruppe: Gutachter, die die Vision einer digitalen Edition verstehen sollen. Der Prototyp muss nicht produktionsreif sein, aber funktional und visuell überzeugend.

## Epic 1 – Textdarstellung (must-have)

**US-1.1** Als Gutachter will ich Notkers Text für Psalm 2 vollständig lesen können.

Akzeptanzkriterien:
- Alle 13 Verse dargestellt
- Vers- und Zeilenreferenzen sichtbar
- Seitenumbrüche der Edition (R10–R13) markiert

**US-1.2** Als Gutachter will ich den verschränkten lat./ahd. Text sehen und per Toggle in zwei Spalten trennen können.

Akzeptanzkriterien:
- Standardansicht: verschränkter Text (wie in der Handschrift)
- Toggle-Ansicht: Latein links, Althochdeutsch rechts, synchron gescrollt
- Farbliche Unterscheidung (siehe [[Design#Farbkonzept]])

**US-1.3** Als Gutachter will ich die nhd. Übersetzung neben dem Haupttext sehen können.

Akzeptanzkriterien:
- nhd. Übersetzung einblendbar (Toggle)
- Zuordnung auf Vers-/Abschnittsebene
- Datengrundlage: Philipps Übersetzung aus der Probeseite

## Epic 2 – Quellenapparat (must-have)

**US-2.1** Als Gutachter will ich bei Klick auf einen Vers die patristischen Quellen sehen.

Akzeptanzkriterien:
- Klick auf Vers öffnet/aktualisiert Quellen-Panel
- Quellen-Panel zeigt: Sigle, Quellenname, lat. Text, dt. Übersetzung
- Alle 13 Verse abgedeckt

**US-2.2** Als Forscher will ich nach einzelnen Quellen filtern können.

Akzeptanzkriterien:
- Checkboxen pro Quellen-Sigle (A, C, Br, R etc.)
- Filter hebt zugehörige Stellen im Haupttext hervor
- Quellen-Panel zeigt nur gefilterte Einträge

## Epic 3 – Facsimile (must-have)

**US-3.1** Als Gutachter will ich das Handschriftendigitalisat neben dem Text sehen.

Akzeptanzkriterien:
- IIIF-Viewer eingebettet (e-codices, CSg 0021, ab Seite 11)
- Mindestens die relevanten Seiten für Psalm 2 navigierbar
- Zoom und Pan funktionieren

## Epic 4 – Funktionale Textschichten (neu, aus E-Mail 21.03.)

**US-4.1** Als Gutachter will ich Übersetzung und Kommentar unabhängig voneinander ein-/ausblenden können, damit ich die verschiedenen Textfunktionen gezielt betrachten kann.

Akzeptanzkriterien:
- Drei unabhängige Toggles: Psalmzitation / Übersetzung / Kommentar
- Psalmzitation visuell unterscheidbar (olive/warm, angelehnt an Probeseite)
- Übersetzung visuell unterscheidbar (grün)
- Kommentar als Standard sichtbar, ausblendbar

**US-4.2** Als Gutachter will ich Interlinearglossen separat ein-/ausblenden können.

Akzeptanzkriterien:
- Toggle für Glossen (unabhängig von den drei Textschichten)
- Glossen visuell als Annotation erkennbar (kleinere Schrift, eigene Farbe)
- 14 Glossen in Psalm 2

**Anmerkung:** US-4.1 und US-4.2 sind Philipps explizite Wünsche vom 21.03. Sie gehen über das ursprüngliche Toggle-Konzept (nur lat./ahd.) hinaus und erfordern die dreigliedrige Textfunktions-Klassifikation aus der [[Probeseite Analyse]].

## Epic 5 – Gesamteindruck (must-have)

**US-5.1** Als Gutachter will ich eine visuell ansprechende, professionelle Oberfläche sehen.

Akzeptanzkriterien:
- Responsives Layout (Laptop-Bildschirm)
- Klare visuelle Hierarchie
- Kein "Baustellen"-Eindruck

**US-5.2** Als Gutachter will ich verstehen, dass dies ein Prototyp ist und die Vision skaliert.

Akzeptanzkriterien:
- Kurzer Einleitungstext erklärt Kontext und Vision
- Navigation deutet weitere Psalmen an (ausgegraut)

## Epic 6 – Psalmtext-Vergleich (scope offen)

**US-6.1** Als Gutachter will ich die Psalmtext-Versionen synoptisch vergleichen können.

Akzeptanzkriterien:
- Synoptische Darstellung der fünf Textzeugen (G, R, H, A-Psalter, C-Psalter)
- Varianten visuell hervorgehoben
- Umschaltbar oder als eigener Tab

**US-6.2** Als Gutachter will ich den Wiener Notker als Paralleltext sehen.

Akzeptanzkriterien:
- Wiener Notker (ÖNB Cod. 2681) als einblendbarer Paralleltext
- Zuordnung auf Versebene

**Anmerkung:** Daten für US-6.1 und US-6.2 liegen vollständig in der Probeseite vor. Budget-Klärung mit Philipp ausstehend.

## Epic 7 – Querverweise (scope offen, Daten fehlen)

**US-7.1** Als Forscher will ich Querverweise auf andere Bibelstellen sehen, die Notker zitiert.

Akzeptanzkriterien:
- Eigener Reiter/Panel für Bibelstellen-Querverweise
- Zuordnung auf Versebene

**Anmerkung:** Philipps Wunsch vom 21.03. Datengrundlage existiert noch nicht. Nicht im Prototyp umsetzbar, aber im Datenmodell vorbereiten.

## Priorisierung

| Priorität | User Stories | Status |
|---|---|---|
| P1 (Kern) | US-1.1, US-1.2, US-2.1, US-5.1 | Vereinbart, im Budget |
| P2 (wichtig) | US-1.3, US-2.2, US-3.1, US-5.2 | Im Budget |
| P3 (Mehraufwand) | US-4.1, US-4.2 | Neu (21.03.), ~2–3h Mehraufwand |
| P4 (scope offen) | US-6.1, US-6.2 | Daten vorhanden, Budget klären |
| P5 (nicht im Prototyp) | US-7.1 | Daten fehlen |

## Verknüpfungen

- [[Research Plan]] — Gesamtplan und Scope-Bewertung
- [[Design]] — Wie die Anforderungen umgesetzt werden
- [[Probeseite Analyse]] — Datengrundlage für die Anforderungen
