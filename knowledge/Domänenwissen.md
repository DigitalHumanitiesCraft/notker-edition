---
type: knowledge
created: 2026-02-24
updated: 2026-03-23
tags: [notker, medieval-studies, domain-knowledge]
---

# Domänenwissen: Notker Psalmenkommentar

## Gegenstand

Notker III. von St. Gallen (ca. 950–1022), genannt Notker Labeo oder Notker der Deutsche, verfasste einen Psalmenkommentar, in dem lateinischer Psalmtext und althochdeutsche Übersetzung/Kommentar verschränkt sind. Der Text ist mehrschichtig: Notker übersetzt nicht nur, sondern kompiliert und kommentiert auf Basis patristischer Quellen (Augustinus, Cassiodor u.a.). Die bisherigen kritischen Editionen (Tax/Sehrt, 1970er) trennen diese Schichten nicht sauber auf.

Die Handschrift CSg 0021 (Stiftsbibliothek St. Gallen) unterscheidet lateinische und althochdeutsche Passagen visuell durch rot/schwarz-Schreibung. Lateinisch ist rot, althochdeutsch ist schwarz.

## Textfunktionale Schichten

Die Analyse der [[Probeseite Analyse|Probeseite]] hat gezeigt, dass Notkers Text drei **funktionale Schichten** enthält, die über Farbcodierung im DOCX unterschieden werden:

### 1. Psalmzitation (`#806000`, olive)

Die Vulgata-Verse, wie Notker sie in seinen Text einbettet. Typischerweise in Großbuchstaben (z.B. `QVARE FREMVERVNT GENTES`), aber auch in Normalschrift innerhalb des Textflusses (z.B. `Astiterunt reges terrȩ . et principes conuenerunt in unum`). Diese Schicht ist **rein lateinisch**.

### 2. Übersetzung (`#00B050`, grün)

Notkers althochdeutsche Wiedergabe der Psalmzitate. Direkte Übersetzung, die dem Psalmtext zeilenweise folgt. Kann lateinische Einsprengsel enthalten, wenn Notker einzelne Begriffe im Original belässt (z.B. `cramoton an christum ebraicȩ gentes?` — ahd. Verb + lat. Objekt).

### 3. Kommentar (schwarz)

Notkers exegetischer Kommentar. Enthält SOWOHL althochdeutsche als AUCH lateinische Passagen (z.B. `idest frustura` = lat., `des ín ubelo spuên solta` = ahd.). Die Farbe markiert die **rhetorische Funktion** (Exegese), nicht die Sprache. Hier verarbeitet Notker die patristischen Quellen und fügt eigene Erklärungen hinzu.

### 4. Interlinearglossen (eigener Annotationstyp)

Einzelwort- oder Kurzübersetzungen, die im Textfluss als eigene Zeilen erscheinen. 14 Glossen in Psalm 2 identifiziert. Sie übersetzen lateinische Fachtermini ins Althochdeutsche (z.B. `penêmida` → `Vorherbestimmung`, `uuerlt-lúste` → `Weltlüste`). Siehe [[Probeseite Analyse#Interlinearglossen]] für das vollständige Inventar.

### 5. Patristische Quellentexte

Die Kommentare von Augustinus, Cassiodor, Remigius u.a., auf die sich Notker bezieht. In der Probeseite als eigene Tabellenzeilen mit Sigle, lateinischem Original und deutscher Übersetzung (Philipps Arbeit).

### 6. Neuhochdeutsche Übersetzung

Philipps eigene Arbeitsübersetzung des gesamten Notker-Textes, zeilenweise in der Probeseite (kursiv, keine Farbe).

## Drei überlagernde Farblogiken

| System | Logik | Farben |
|---|---|---|
| Handschrift CSg 0021 | **Sprache** | rot = Latein, schwarz = Althochdeutsch |
| Probeseite (DOCX) | **Textfunktion** | olive = Psalmzitat, grün = Übersetzung, schwarz = Kommentar |
| Prototyp-UI | **Noch zu definieren** | Muss beide Logiken berücksichtigen |

## Prototyp-Scope

Psalm 2 (13 Verse). Nur dieser Psalm.

## Datenquellen

### 1. Probeseite – Primärdatenquelle

Word-Dokument (`data/Probeseite_Notker.docx`), tabellarische Aufbereitung. Ursprünglich für physische Publikation erstellt. Finale Lieferung: 21.03.2026.

Inhalt: 13 Tabellen mit Haupttext (inkl. Farbcodierung), nhd. Übersetzung, Quellenapparat, Interlinearglossen, synoptischer Psalmtext-Vergleich (5 Zeugen), Wiener Notker. Siehe [[Probeseite Analyse]] für die vollständige Strukturanalyse.

### 2. ANNIS-HTML-Scrape (Sekundärquelle)

Quelle: Referenzkorpus Altdeutsch (ReA), ein tiefenannotiertes Mehrebenenkorpus aller althochdeutschen und altniederdeutschen Texte (ca. 750–1050), Teil des Verbunds "Deutsch Diachron Digital" (DDD). Ca. 650.000 Textwörter, Version 1.2 (Oktober 2022), Lizenz CC-BY-NC-SA. Zugang weltweit kostenfrei über ANNIS4: https://korpling.german.hu-berlin.de/annis/ddd

**Annotationsebenen:**
- Primärtext ("edition"): handschriftengetreue Wiedergabe
- Normalisierung ("text"): segmentierte Schreibung
- POS-Tagging (DDDTS, kompatibel mit STTS)
- Morphologie (Kasus, Numerus, Genus, Tempus, Modus etc.)
- Lemmatisierung und Übersetzung
- Satzstruktur (Satzspannen)
- Metadaten (Entstehungszeit, Sprachraum, Überlieferungskontext)

**Notker im ReA:** Notkers Gesamtwerk umfasst ca. 350.000 Wortformen — mehr als die Hälfte der gesamten altdeutschen Textüberlieferung. Relevantes Korpus: `DDD-AD-Z-Notker-Psalmen_1.2` (167.583 Tokens). Lateinische Vorlagen sind mit aufgenommen, annotiert und mit den ahd. Daten aligniert.

**Technischer Zugang:** Daten im HTML scrapebar (Token als `textval`-Attribute in `<span>`-Elementen). Liefert Handschriften-Zeilenreferenzen und dient zur Validierung der Textgestalt. Daten noch nicht im Repository (`data/raw/annis_psalm2.html` fehlt).

### 3. Facsimile

e-codices, CSg 0021. IIIF-fähig.
- Einstieg Psalm 2: [Seite 11](https://www.e-codices.unifr.ch/de/csg/0021/11/0/) (von Philipp bestätigt)
- IIIF-Manifest (zu verifizieren): `https://www.e-codices.unifr.ch/metadata/iiif/csg-0021/manifest.json`
- Seiten-Range für Psalm 2: ab S. 11, Ende noch zu klären

### 4. Quelleneditionen (De Gruyter)

- Quellenliste: [Tax/Sehrt, S. 4–5](https://www.degruyterbrill.com/document/doi/10.1515/9783110935332/html)
- Edition: [Tax/Sehrt, S. 11](https://www.degruyterbrill.com/document/doi/10.1515/9783110967500/html)

## Quellen-Siglen

### Kommentarquellen (gesichert)

| Sigle | Quelle | Häufigkeit in Psalm 2 |
|---|---|---|
| A | Augustinus, Enarrationes in Psalmos | Sehr häufig, umfangreichste Quelle |
| C | Cassiodor, Expositio Psalmorum | Sehr häufig, zweitwichtigste Quelle |
| Br | Breviarium | Selten, kurze Einträge |
| R | Remigius | Gelegentlich |

### Kommentarquellen (ungeklärt)

| Sigle | Vermutung | Vorkommen | Klärungsbedarf |
|---|---|---|---|
| RII | Zweite Remigius-Quelle oder -Rezension? | Table 4, Row 15 (einmalig) | Mit Philipp klären |
| N | Unbekannt | Table 4, Row 5 (einmalig) | Mit Philipp klären |

### Siglen in der Haupttext-Spalte (unklar)

G, R, H, A, C erscheinen auch in der **Siglen-Spalte der Haupttext-Zeilen** (nicht in den Quellenapparat-Zeilen). Dort könnten sie bedeuten:
- Welcher Psalmtext-Version die Zeile textlich folgt (textkritisch), ODER
- Welche Kommentarquelle die Zeile inhaltlich beeinflusst hat

Die Funktion von **H** in der Siglen-Spalte ist besonders unklar: Hebraicum-Psalter als Textvorlage? Oder eine eigene Kommentarquelle? Erscheint in Tables 2, 5, 7.

### Psalmtext-Zeugen (synoptischer Vergleich)

| Sigle | Textzeuge | Handschrift |
|---|---|---|
| G | Gallicanum | (nicht angegeben) |
| R | Romanum | (nicht angegeben) |
| H | Hebraicum (iuxta Hebraeos) | Bamberg Ms. 44 |
| A | Augustinus-Psalter | St. Gallen Cod. 162 |
| C | Cassiodor-Psalter | St. Gallen Cod. 200 |

**Siglen-Disambiguation:** A, C, R, H haben je nach Kontext verschiedene Bedeutungen. Im Quellenapparat: Kommentarwerke. Im Psalmtext-Vergleich: Psalter-Handschriften. In der Haupttext-Siglen-Spalte: unklar.

## Referenzsysteme

| System | Granularität | Beispiel |
|---|---|---|
| Psalmverse | Vers 1–13 | P5 = Psalm 2, Vers 5 |
| Editionszeilen | fortlaufend | Zeile 1–n (Tax/Sehrt) |
| Handschriftenzeilen | fortlaufend | Zeilen in CSg 0021 |

Die Quellenzuordnung in der Probeseite referenziert implizit die Editionszeilen. Der ANNIS-Export referenziert Handschriftenzeilen. Die Brücke muss manuell hergestellt werden.

## Zitierhinweis Korpus

Zeige, Lars Erik; Schnelle, Gohar; Klotz, Martin; Donhauser, Karin; Gippert, Jost; Lühr, Rosemarie. 2022. Deutsch Diachron Digital. Referenzkorpus Altdeutsch. Humboldt-Universität zu Berlin. DOI: https://doi.org/10.34644/laudatio-dev-MiXVDnMB7CArCQ9CABmW

## Verknüpfungen

- [[Research Plan]] — Gesamtplan
- [[Probeseite Analyse]] — Detaillierte DOCX-Analyse
- [[Anforderungen]] — Was der Prototyp können muss
