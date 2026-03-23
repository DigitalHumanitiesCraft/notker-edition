---
type: concept
created: 2026-02-24
updated: 2026-03-23
tags: [digital-humanities, medieval-studies]
status: reviewed
---

# Referenzkorpus Altdeutsch

## Definition

Das Referenzkorpus Altdeutsch (ReA) ist ein tiefenannotiertes Mehrebenenkorpus aller althochdeutschen und altniederdeutschen Texte (ca. 750–1050). Es ist Teil des Verbunds "Deutsch Diachron Digital" (DDD) und wird über die Such- und Visualisierungsplattform ANNIS bereitgestellt.

## Eckdaten

| Eigenschaft | Wert |
|:---|:---|
| Umfang | ca. 650.000 Textwörter (ca. 535.000 Tokens) |
| Zeitraum | 750–1050 |
| Lizenz | CC-BY-NC-SA |
| Version | 1.2 (Oktober 2022) |
| Zugang ANNIS4 | https://korpling.german.hu-berlin.de/annis/ddd |
| Projektwebseite | https://www.deutschdiachrondigital.de/rea/ |
| Förderung | DFG-Sachbeihilfe 2008–2015 |

## Verantwortliche

Karin Donhauser (HU Berlin), Jost Gippert (Goethe-Universität Frankfurt), Rosemarie Lühr (Universität Jena). Aktuelle Betreuung in Berlin.

## Zitierhinweis

Zeige, Lars Erik; Schnelle, Gohar; Klotz, Martin; Donhauser, Karin; Gippert, Jost; Lühr, Rosemarie. 2022. Deutsch Diachron Digital. Referenzkorpus Altdeutsch. Humboldt-Universität zu Berlin. DOI: https://doi.org/10.34644/laudatio-dev-MiXVDnMB7CArCQ9CABmW

## Annotationsebenen

- **Primärtext** ("edition"): handschriftengetreue Wiedergabe
- **Normalisierung** ("text"): segmentierte Schreibung
- **POS-Tagging:** nach DDDTS, kompatibel mit STTS
- **Morphologie:** Kasus, Numerus, Genus, Tempus, Modus etc.
- **Lemmatisierung** und **Übersetzung**
- **Satzstruktur** (Satzspannen)
- **Metadaten:** Entstehungszeit, Sprachraum, Überlieferungskontext

## Notker im ReA

Notkers Gesamtwerk umfasst ca. 350.000 Wortformen und macht damit mehr als die Hälfte der gesamten altdeutschen Textüberlieferung aus. Im ANNIS-Korpus:

- `DDD-AD-Z-Notker-Psalmen_1.2` (167.583 Tokens) – Psalmenkommentar
- `DDD-AD-Z-Notker-Boethiu...` – Boethius-Übersetzung
- `DDD-AD-Z-Notker-Cantica...` – Cantica

Die lateinischen Vorlagen sind mit aufgenommen, annotiert und mit den ahd. Daten aligniert.

## Technischer Zugang

Weltweit kostenfrei, ohne Anmeldung über ANNIS. Daten im HTML scrapebar (Token als `textval`-Attribute in `<span>`-Elementen).

## Verknüpfungen

- [[Domänenwissen]] — Notker im Projektkontext
- [[Technik]] — Parsing-Strategie für ANNIS-Daten
