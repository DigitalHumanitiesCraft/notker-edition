---
title: "INDEX — Navigation und Begriffslexikon"
project:
  name: "notker-edition"
  repository: "https://github.com/DigitalHumanitiesCraft/notker-edition"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/excellence/blog/Promptotyping"
status: active
version: "0.2"
created: 2026-05-09
updated: 2026-05-09
language: de
authors:
  - "Christopher Pollin"
generated-with: "Claude (Anthropic)"
---

# INDEX — Navigation und Begriffslexikon

Einstiegspunkt für den `knowledge/`-Vault des Notker-Edition-Prototyps. Erste Hälfte: Navigation in einer empfohlenen Lesereihenfolge mit Funktion und Triggerkriterium pro Dokument. Zweite Hälfte: Begriffslexikon der konstitutiven Termini.

## Lesereihenfolge

Einstiegssequenz für eine neue Session, die das Projekt aus dem Stand verstehen muss.

1. [[project]] — Was ist dieses Projekt, wer ist beteiligt, was leistet es bewusst nicht, in welcher Phase ist es.
2. [[data]] — Welches Material verarbeitet die Edition: Domäne (Notker, Handschrift, Textschichten), Datenquellen (Probeseite, ReA, Facsimile, Editionen), Siglen-System, Probeseite-Strukturanalyse.
3. [[specification]] — Was soll das System tun und warum: Anforderungen Iteration 1 und 2, getroffene Entscheidungen mit Begründung, Phasenplan und Stand pro Story, Iteration-2c-Follow-up.
4. [[design]] — Wie sieht das Editionsinterface aus, welche Designhaltung trägt es, welches Slot-System, welche Toggles, welches Farbsystem.
5. [[architecture]] — Wie ist die Pipeline gebaut: DOCX-Parser, Schichtenklassifikation, TEI-Generierung, JSON-Ableitung, Web-Stack, IIIF-Integration, JSON-Schema.
6. [[editorial-guidelines]] — TEI-Kodierungsregeln pro Textphänomen (Schichten, Sprachwechsel, Glossen, Quellenapparat, Fußnoten, Psaltervergleich).
7. [[journal]] — Chronologie der Entscheidungen, falls die Genese eines Befundes fraglich ist.
8. [[offene-korrekturen]] — Aktuell offene Tech-Debt-Items pro Ebene (TEI-Datenmodell, Pipeline, UI).

## Funktionen pro Dokument

| Dokument | Funktion (Konvention) | Wann hier nachlesen |
|---|---|---|
| [[INDEX]] | Navigation + Begriffslexikon | Wenn ein Begriff unklar ist oder die Lesereihenfolge gesucht wird |
| [[project]] | Identität | Wenn der Projektkontext oder die Projektphase unklar ist |
| [[data]] | Material | Wenn Datenfelder, Siglen oder Beispiele falsch verwendet wurden |
| [[specification]] | Substanz (formal + Entscheidungen + Stand) | Wenn ein Akzeptanzkriterium ignoriert oder eine frühere Entscheidung revidiert wurde |
| [[design]] | Gestalt | Wenn UI-Inkonsistenz besteht oder das Designsystem gebrochen wirkt |
| [[architecture]] | Bauweise | Wenn falsche Annahmen über Komponenten, Datenfluss oder Schichtgrenzen entstehen |
| [[editorial-guidelines]] | Bauweise (TEI-Spezialisierung) | Wenn TEI-Kodierung uneinheitlich oder ein Textphänomen falsch ausgezeichnet ist |
| [[journal]] | Genese | Wenn die Entscheidungslogik unklar ist oder eine frühere Sackgasse droht |
| [[offene-korrekturen]] | Process (Tech-Debt-Tracker) | Wenn ein bekannter Bug umgangen werden soll oder eine Korrektur priorisiert wird |

`CLAUDE.md` im Repo-Root ist das Action-Dokument der Wissensbasis: imperative Regeln, die auf die deklarativen Knowledge-Dokumente hier verweisen.

## Begriffslexikon

Die konstitutiven Termini des Projekts, alphabetisch sortiert. Wo eine Begriffsklärung in einem Knowledge-Dokument vertieft ist, verweist der Eintrag dorthin.

**Cross-Verse-Verkettung.** Wenn ein Wort über die Versgrenze geteilt ist („han-" am Ende von V1–2, „gta" am Anfang von V3–5), reicht die TEI-`@part`-Verkettung allein nicht — die Reihenfolge ist über die Vers-Grenze hinweg nicht implizit. Lösung: `@xml:id`/`@next`/`@prev` zusätzlich zu `@part="I"`/`"F"`. Implementiert in `chain_cross_verse_hyphens()`. Siehe [[editorial-guidelines#2.2 Zeilenübergreifende Segmente]].

**Disambiguierungs-Heuristik (R-Sigle).** Die Sigle „R" kann Romanum-Psalter (Textzeuge) oder Remigius (Kommentarquelle) bedeuten. Die Pipeline löst sie nach Section-Type auf: R in `psalm_citation` → Romanum, R in `commentary`/`translation`/`gloss` → Remigius. G und H sind eindeutig Psalter, A/C/Br/RII/N eindeutig Patristik. Bestätigung durch den Auftraggeber steht aus. Siehe [[data#Disambiguierungs-Heuristik (Iteration 2)]].

**Edition (Tax/Sehrt).** Die kritische Druckedition von Notkers Psalmenkommentar (De Gruyter, 1970er). Im Prototyp referenziert über die Editions-Seitenangaben R10 bis R13.

**Errata-Layer (historisch).** Eine in Iteration 2 zwischenzeitlich eingeführte YAML-basierte Korrektur-Pipeline. In Iteration 2b zugunsten einer einfachen `PFEIFER_CORRECTIONS`-Liste in `parse_probeseite.py` wieder aufgegeben. 779 Zeilen entfernt. Siehe [[journal#2026-04-16 — Iteration 2b]].

**Facsimile.** Hochauflösendes Bild der Handschriftenseite. Im Prototyp via IIIF aus dem Manifest der Stiftsbibliothek St. Gallen für CSg 0021 eingebunden, Viewer ist OpenSeadragon.

**Funktionale Textschichten.** Drei Schichten in Notkers Text: Psalmzitation (lat. Vulgata-Zitat), Übersetzung (ahd. Wiedergabe), Kommentar (exegetische Erläuterung, ahd. + lat.). Plus zwei zusätzliche Annotationstypen: Interlinearglossen und neuhochdeutsche Arbeitsübersetzung. In der Probeseite per Farbcodierung, im TEI als `<seg type="...">`. Siehe [[data#Textfunktionale Schichten]].

**Glosse (Interlinearglosse).** Einzelwort- oder Kurzübersetzung im Textfluss. 13 Stück in Psalm 2. Erkennungsmerkmale: kurze Zeilen (≤ 5 Wörter), keine Quellen-Sigle, Übersetzungsverhältnis 1:1, keine `[...]`-Auslassung. Im TEI als `<ab ana="#fn-gloss"><gloss>`. Siehe [[data#Interlinearglossen-Inventar]].

**Iteration-Logik.** Das Repo trägt drei Substanz-Iterationen: Iteration 1 (Erstauslieferung 2026-03-23), Iteration 2 (Pfeifer-Review 2026-04-15, Stories Epic 8–12, Bugfixes), Iteration 2c (Follow-up 2026-04-16). Alle in [[specification]] konsolidiert.

**Kanonisches Format.** TEI-XML ist die Source of Truth, JSON wird daraus abgeleitet. Bei Widersprüchen zwischen TEI und JSON gilt das TEI. Architekturentscheidung 2026-03-23.

**Knowledge-Vault.** Der `knowledge/`-Ordner als Promptotyping-Wissensbasis. Folgt der [[Konvention Promptotyping Documents]]. Pflichtkern-Frontmatter, Iterations-Geschichte, knowledge-sources als verschachteltes URI-Mapping.

**Pool / Slot-System.** UI-Architektur seit Iteration 2: Drei generische Slots (A, B, C) mit Auswahl-Dropdown und Schließen-Button. Pool aus 9 Inhaltstypen (Quellen, Edition, nhd. Übersetzung, Wiener Notker, Psalter G/R/H, Facsimile, Anmerkungen, Psalmtext-Vergleich). Single-Instance — Auto-Swap, wenn ein Eintrag in mehreren Slots gewählt wird. URL-Hash-persistent. Siehe [[design#3.1 Gesamtlayout (Slot-System)]].

**Probeseite.** Word-Dokument (`data/Probeseite_Notker.docx`), die maßgebliche Primärdatenquelle. 13 Tabellen in 3 Gruppen, mit Farbcodierung der Textschichten, Quellenapparat, nhd. Arbeitsübersetzung. Finale Lieferung 2026-03-21. Siehe [[data#Probeseiten-Strukturanalyse]].

**Psalter-Zeugen.** Fünf Textversionen des Psalmtextes, die in Notkers Edition synoptisch vergleichbar sind: Gallicanum (G), Romanum (R), Hebraicum (H), Augustinus-Psalter (A-Psalter), Cassiodor-Psalter (C-Psalter). Im TEI als `<witness>` in `<sourceDesc>/<listWit>`, im Apparat als `<rdg wit="#wit-...">`.

**Quellenapparat.** Patristische Quellentexte (Augustinus, Cassiodor, Remigius, Breviarium), auf die Notker zurückgreift. Im TEI als `<note type="sources"><cit>` mit `<bibl>`, `<quote>`, dt. Übersetzung. Pro Vers im Quellenapparat-Panel im UI.

**Section-Type.** Klassifikation einer JSON-Section nach Textfunktion: `psalm_citation`, `translation`, `commentary`, `gloss`. Steuert Render-Modus im Frontend, Layer-Toggles und R-Disambiguierung.

**Slot.** Ein generischer UI-Container im Drei-Slot-Layout (siehe Pool / Slot-System).

**Verification Milestone.** Konzept aus der Promptotyping-Methode für definierte Checkpoints, an denen Domänenexpertise systematisch angewendet wird. Im Notker-Repo nicht explizit instanziiert, aber konzeptuell verwandt mit den Auftraggeber-Reviews zwischen Iteration 1, 2 und 2c.

## Verknüpfungen

- [[project]]
- [[data]]
- [[specification]]
- [[design]]
- [[architecture]]
- [[editorial-guidelines]]
- [[journal]]
- [[offene-korrekturen]]
