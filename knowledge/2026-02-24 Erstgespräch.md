---
type: log
created: 2026-02-24
tags: [digital-humanities, medieval-studies]
status: reviewed
---

# 2026-02-24 – Erstgespräch Notker Prototyp

## Kontext

Erstes Gespräch mit Dr. Philipp Pfeifer zum Prototyp einer digitalen Edition von Notkers Psalmenkommentar. Kontakt kam über [[Georg Vogeler]] und [[Bernhard Bauer]] (Universität Graz). Ziel: Testseite als Proof of Concept für einen Drittmittelantrag.

## Gegenstand

[[Domänenwissen|Notkers Psalmenkommentar]] ist ein mehrschichtiger Text: lateinische Psalmverse und althochdeutsche Übersetzung/Kommentar sind ineinander verschränkt. Dazu kommen ca. 15–20 Sekundärquellen (Augustinus, Cassiodor u.a.), auf die sich der Kommentar bezieht. Bisherige Editionen (1970er Jahre) lösen diese Schichten nicht sauber auf.

## Vision des Auftraggebers

Interface mit folgenden Funktionen:

- Notkers Haupttext anzeigen (ahd./lat. gemischt)
- Daneben: neue nhd. Übersetzung mit Kommentar (entsteht im Gesamtprojekt)
- Sekundärquellen selektiv einblendbar (Augustinus, Cassiodor etc.)
- Toggle: Latein und Deutsch im Haupttext trennen und nebeneinander zeigen
- Quellenverlinkung auf Satzebene: Klick auf Satz zeigt zugehörige Quellen
- Nutzer/in wählt selbst, was sichtbar sein soll

## Datenlage (besprochen)

### Haupttext

- Gedruckte Editionen aus den 1970ern; Akzente handschriftlich eingetragen, kaum kopierbar/OCR-fähig
- Digital vorhanden im [[Referenzkorpus Altdeutsch]] auf ANNIS: Corpus `DDD-AD-Z-Notker-Psalmen_1.2` (167.583 Tokens)
- ANNIS-Oberfläche umständlich (Vaadin-basiert, Desktop-artig), aber Daten im HTML scrapebar

### Sekundärquellen

- Nur in Buchform/PDF vorhanden
- Gesammelte Quellenliste existiert, aber unvollständig
- Zuordnung zu Notkers Text über Psalm + Vers

## Unsere Einschätzung (im Gespräch mitgeteilt)

- **Interface:** allerkleinste Problem; klassisches TEI-Projekt
- **Kernproblem:** Datenaufbereitung und -modellierung
- **Architektur:** TEI-XML als Single Source of Truth; daraus beliebige Interfaces ableitbar
- **Budget-Einschätzung:** ca. 4.000–5.000 € für Prototyp (Hausnummer)

## Vereinbart

Auftraggeber liefert:
1. Requirements-Dokument (frei formuliert)
2. Psalm-Auswahl für den Prototyp
3. PDF mit Sekundärquellen + Erklärung der Zuordnung

Wir liefern dann Kostenvoranschlag.

## Offene Punkte (historisch)

- ~~Name des Auftraggebers~~ → Dr. Philipp Pfeifer
- Welche Förderlinie / welcher Geldgeber?
- Für Gesamtprojekt: Absprache mit ReA-Team (Karin Donhauser, HU Berlin)
- Rechtliche Klärung: Urheberrecht an der Textgestalt der Edition aus den 1970ern?

## Sources

- Erstgespräch (Videokonferenz), 2026-02-24
- [[Referenzkorpus Altdeutsch]]: https://korpling.german.hu-berlin.de/annis/ddd
- Projektwebseite ReA: https://www.deutschdiachrondigital.de/rea/

## Verknüpfungen

- [[Journal]] — Projektchronologie
- [[Domänenwissen]] — Fachwissen Notker
