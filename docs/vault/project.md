---
title: "Notker Psalmenkommentar — Digitaler Prototyp"
project:
  name: "notker-edition"
  repository: "https://github.com/DigitalHumanitiesCraft/notker-edition"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/excellence/blog/Promptotyping"
status: active
version: "0.2"
created: 2026-03-23
updated: 2026-05-09
language: de
authors:
  - "Christopher Pollin"
generated-with: "Claude (Anthropic)"
topics:
  - "[[Promptotyping]]"
  - "[[Scholar-Centered Design]]"
  - "[[Digital Edition]]"
related:
  - "[[INDEX]]"
  - "[[data]]"
  - "[[specification]]"
  - "[[design]]"
  - "[[architecture]]"
  - "[[editorial-guidelines]]"
  - "[[journal]]"
knowledge-sources:
  institutions:
    - label: "Universität Graz, Institut für Germanistik"
      uri: "https://germanistik.uni-graz.at/"
    - label: "ZIM Graz — Zentrum für Informationsmodellierung"
      uri: "https://informationsmodellierung.uni-graz.at/"
    - label: "Digital Humanities Craft OG"
      uri: "https://dhcraft.org/"
  methods:
    - label: "Promptotyping"
      uri: "https://dhcraft.org/excellence/blog/Promptotyping"
    - label: "Scholar-Centered Design"
      uri: "https://informationsmodellierung.uni-graz.at/"
---

# Notker Psalmenkommentar — Digitaler Prototyp

## Identität

Prototyp einer digitalen Edition von Notkers Psalmenkommentar (Notker III. von St. Gallen, ca. 950–1022). Demonstrationsobjekt: Psalm 2 (13 Verse). Proof of Concept für einen Drittmittelantrag.

| Rolle | Person / Organisation |
|---|---|
| Auftraggeber | Institut für Germanistik, Universität Graz |
| Kooperation | ZIM Graz |
| Umsetzung | Digital Humanities Craft OG |

## Was der Prototyp leistet

Notkers Text verschränkt lateinischen Psalmtext, althochdeutsche Übersetzung und exegetischen Kommentar in einem Textfluss. Die digitale Edition macht diese Schichten einzeln sichtbar — drei funktionale Textschichten farblich unterschieden (Psalmzitat, Übersetzung, Kommentar), Parallel-Layout mit zeilengetreuer nhd. Übersetzung, Toggles für jede Schicht, Quellenapparat mit patristischen Autoren (Augustinus, Cassiodor, Remigius, Breviarium), Psalter-Filter mit Section-Type-Disambiguierung der Sigle „R", Interlinearglossen inline, Facsimile der Handschrift CSg 0021 via IIIF (e-codices), konfigurierbares Drei-Slot-Layout, synoptischer Psalmtext-Vergleich von fünf Textzeugen, Wiener Notker als Paralleltext, URL-persistente Deep Links für Gutachter.

Alle Schicht-, Filter- und Layout-Entscheidungen sind in [[design]] dokumentiert; die TEI- und Pipeline-Architektur in [[architecture]]; die Anforderungs- und Iterations-Geschichte in [[specification]].

## Was der Prototyp bewusst nicht leistet

- Keine Vollabdeckung aller 150 Psalmen. Psalm 2 demonstriert das Prinzip; die Pipeline ist multi-psalm-ready, aber der Antragsstand zeigt eine Edition.
- Kein editorisches Backend. Die Edition ist statisch ausgeliefert; Korrekturen laufen über `PFEIFER_CORRECTIONS` in `parse_probeseite.py`.
- Keine Querverweise auf Bibelstellen. Der Auftraggeber hat den Wunsch geäußert, die Datenbasis fehlt aber.
- Keine zeilengenaue Bild-Text-Synopse. Vers→Seite-Mapping ist umgesetzt, Vers→Zeile-Koordinaten würden manuelle Annotation erfordern und übersteigen das Prototyp-Budget.
- Kein Mobile-Layout. Zielgröße ist Laptop (1280–1440 px); kleinere Viewports werden funktional unterstützt, aber nicht primär gestaltet.

## Substanzherkunft

Die maßgebliche Primärdatenquelle ist eine DOCX-Probeseite des Auftraggebers (`data/Probeseite_Notker.docx`, finale Lieferung 2026-03-21), tabellarisch aufgebaut, mit Farbcodierung der Textschichten, Quellenapparat und nhd. Arbeitsübersetzung. Sekundärquelle ist das Referenzkorpus Altdeutsch (ReA / DDD-AD-Z-Notker-Psalmen_1.2, HU Berlin) als ANNIS-HTML-Scrape zur Validierung. Facsimile-Bilder über das IIIF-Manifest der Stiftsbibliothek St. Gallen (CSg 0021, e-codices). Quelleneditionen referenzieren Tax/Sehrt (De Gruyter, 1970er). Vollständige Beschreibung in [[data]].

## Methodische Verortung

Das Repo folgt der Promptotyping-Methode: Der `knowledge/`-Ordner ist die Source of Truth, Code wird daraus iterativ abgeleitet, der Critical Expert (Auftraggeber-Review) validiert pro Iteration. Iteration 1 (Erstauslieferung 2026-03-23) wurde durch ein strukturiertes Review (Mail + Google Doc, 2026-04-15) zu Iteration 2 erweitert; Iteration 2c (2026-04-16) reagiert auf Befunde der 2b-Auslieferung. Die Iterations-Logik ist in [[specification]] dokumentiert.

Knowledge/Process/Action-Klassifikation folgt der Lese-Heuristik der Konvention: Knowledge-Dokumente liegen in `knowledge/`, das Action-Dokument `CLAUDE.md` im Repo-Root verweist auf sie und übersetzt deklaratives Wissen in imperative Anweisungen für den Coding-Agenten.

## Arbeitsphasen

| Phase | Inhalt | Stand |
|---|---|---|
| 1 — Dokumentation und Klärung | Probeseite analysiert, Vault aufgebaut, TEI-XML als kanonisch entschieden | abgeschlossen |
| 2 — Datenaufbereitung (AP1) | Pipeline DOCX → TEI → JSON, RelaxNG-validiert | abgeschlossen |
| 3 — Interface (AP2) | 3-Panel-Layout, Toggles, Quellenapparat, IIIF, Psalmtext-Vergleich, URL-Persistenz | abgeschlossen |
| 4 — Übergabe Iteration 1 | ReadMe, Vault-Sync, GitHub Pages, Übergabe an Auftraggeber | abgeschlossen |
| 5 — Iteration 2 (Review-Einarbeitung) | Errata-Refactor, Slot-System, zeilengetreue nhd., Psalter-Filter, R-Disambiguierung, Multi-Psalm-Pipeline, Vault öffentlich | abgeschlossen |
| 6 — Abnahme Iteration 2 | Auftraggeber-Review auf deployter Seite, Augustinus-2-Nachreichungen V3-5/V6, R-Disambiguierungs-Bestätigung, CSg-0021-Zeilenumbrüche klären | offen |

## Offene Punkte (niedrige Priorität)

| Frage | Status |
|---|---|
| Querverweise auf Bibelstellen (US-7.1) | Daten fehlen, Platzhalter im Datenmodell |
| Vers→Seite-Mapping verifizieren | Vorläufig, gegen Facsimile prüfen |
| Echte Handschriften-Zeilenumbrüche der CSg 0021 | Aktuell nur über DOCX-Tabellenzeilen abgeleitet |

## Verknüpfungen

- [[INDEX]] — Navigation und Begriffslexikon
- [[data]] — Primärdatenquelle, ReA-Korpus, Siglen-System, Probeseite-Strukturanalyse
- [[specification]] — Anforderungen Iteration 1 und 2, Entscheidungen, Stand pro Story
- [[design]] — Editionsinterface, Slot-System, Toggles, Farbsystem
- [[architecture]] — Pipeline, TEI-Modell, JSON-Schema, Web-Stack, IIIF
- [[editorial-guidelines]] — TEI-Kodierungsregeln für alle Textphänomene
- [[journal]] — Chronologie und Entscheidungen
- [[offene-korrekturen]] — Tech-Debt-Tracker
