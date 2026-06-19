---
title: "Datengrundlage — Notker Psalmenkommentar"
project:
  name: "notker-edition"
  repository: "https://github.com/DigitalHumanitiesCraft/notker-edition"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/excellence/blog/Promptotyping"
status: complete
version: "0.2"
created: 2026-02-24
updated: 2026-05-09
language: de
authors:
  - "Christopher Pollin"
generated-with: "Claude (Anthropic)"
topics:
  - "[[TEI]]"
  - "[[Old High German]]"
  - "[[Reference Corpus]]"
  - "[[IIIF]]"
related:
  - "[[INDEX]]"
  - "[[project]]"
  - "[[architecture]]"
  - "[[editorial-guidelines]]"
knowledge-sources:
  institutions:
    - label: "Stiftsbibliothek St. Gallen"
      uri: "https://www.stibi.ch/"
    - label: "Humboldt-Universität zu Berlin (DDD)"
      uri: "https://korpling.german.hu-berlin.de/"
  standards:
    - label: "TEI P5"
      uri: "https://tei-c.org/release/doc/tei-p5-doc/"
    - label: "IIIF Presentation API 2.0"
      uri: "https://iiif.io/api/presentation/2.0/"
    - label: "ISO 639-3 (goh — Old High German)"
      uri: "https://iso639-3.sil.org/code/goh"
  vocabularies:
    - label: "Codices Sangallenses 0021 (e-codices)"
      uri: "https://www.e-codices.unifr.ch/de/list/one/csg/0021"
    - label: "IIIF-Manifest CSg 0021"
      uri: "https://www.e-codices.unifr.ch/metadata/iiif/csg-0021/manifest.json"
    - label: "Referenzkorpus Altdeutsch ReA"
      uri: "https://doi.org/10.34644/laudatio-dev-MiXVDnMB7CArCQ9CABmW"
    - label: "Tax/Sehrt — Quellenliste De Gruyter"
      uri: "https://www.degruyterbrill.com/document/doi/10.1515/9783110935332/html"
    - label: "Tax/Sehrt — Edition De Gruyter"
      uri: "https://www.degruyterbrill.com/document/doi/10.1515/9783110967500/html"
---

# Datengrundlage — Notker Psalmenkommentar

## Gegenstand

Notker III. von St. Gallen (ca. 950–1022), genannt Notker Labeo oder Notker der Deutsche, verfasste einen Psalmenkommentar, in dem lateinischer Psalmtext und althochdeutsche Übersetzung/Kommentar verschränkt sind. Der Text ist mehrschichtig: Notker übersetzt nicht nur, sondern kompiliert und kommentiert auf Basis patristischer Quellen (Augustinus, Cassiodor u.a.). Die bisherigen kritischen Editionen (Tax/Sehrt, 1970er) trennen diese Schichten nicht sauber auf.

Die Handschrift CSg 0021 (Stiftsbibliothek St. Gallen) unterscheidet lateinische und althochdeutsche Passagen visuell durch rot/schwarz-Schreibung. Lateinisch ist rot, althochdeutsch ist schwarz.

Prototyp-Scope: Psalm 2 (13 Verse). Nur dieser Psalm.

## Textfunktionale Schichten

Die Analyse der Probeseite hat gezeigt, dass Notkers Text drei funktionale Schichten enthält, die über Farbcodierung im DOCX unterschieden werden.

### 1. Psalmzitation (`#806000`, olive)

Die Vulgata-Verse, wie Notker sie in seinen Text einbettet. Typischerweise in Großbuchstaben (z.B. `QVARE FREMVERVNT GENTES`), aber auch in Normalschrift innerhalb des Textflusses (z.B. `Astiterunt reges terrȩ . et principes conuenerunt in unum`). Diese Schicht ist rein lateinisch.

### 2. Übersetzung (`#00B050`, grün)

Notkers althochdeutsche Wiedergabe der Psalmzitate. Direkte Übersetzung, die dem Psalmtext zeilenweise folgt. Kann lateinische Einsprengsel enthalten, wenn Notker einzelne Begriffe im Original belässt (z.B. `cramoton an christum ebraicȩ gentes?` — ahd. Verb + lat. Objekt).

### 3. Kommentar (schwarz)

Notkers exegetischer Kommentar. Enthält sowohl althochdeutsche als auch lateinische Passagen (z.B. `idest frustura` = lat., `des ín ubelo spuên solta` = ahd.). Die Farbe markiert die rhetorische Funktion (Exegese), nicht die Sprache. Hier verarbeitet Notker die patristischen Quellen und fügt eigene Erklärungen hinzu.

### 4. Interlinearglossen (eigener Annotationstyp)

Einzelwort- oder Kurzübersetzungen, die im Textfluss als eigene Zeilen erscheinen. Sie übersetzen lateinische Fachtermini ins Althochdeutsche (z.B. `penêmida` → `Vorherbestimmung`, `uuerlt-lúste` → `Weltlüste`). Vollständiges Inventar weiter unten.

### 5. Patristische Quellentexte

Die Kommentare von Augustinus, Cassiodor, Remigius u.a., auf die sich Notker bezieht. In der Probeseite als eigene Tabellenzeilen mit Sigle, lateinischem Original und deutscher Arbeitsübersetzung.

### 6. Neuhochdeutsche Übersetzung

Arbeitsübersetzung des Auftraggebers, die den gesamten Notker-Text zeilenweise in der Probeseite (kursiv, keine Farbe) wiedergibt.

## Drei überlagernde Farblogiken

| System | Logik | Farben |
|---|---|---|
| Handschrift CSg 0021 | Sprache | rot = Latein, schwarz = Althochdeutsch |
| Probeseite (DOCX) | Textfunktion | olive = Psalmzitat, grün = Übersetzung, schwarz = Kommentar |
| Prototyp-UI | Funktional | siehe [[design#3.3 Farbsystem]] |

## Datenquellen

### 1. Probeseite — Primärdatenquelle

Word-Dokument (`data/Probeseite_Notker.docx`), tabellarische Aufbereitung. Ursprünglich für physische Publikation erstellt. Finale Lieferung: 2026-03-21.

Inhalt: 13 Tabellen mit Haupttext (inkl. Farbcodierung), nhd. Übersetzung, Quellenapparat, Interlinearglossen, synoptischer Psalmtext-Vergleich (5 Zeugen), Wiener Notker. Die DOCX-Strukturanalyse trägt dieses Dokument selbst weiter unten unter „Probeseiten-Strukturanalyse".

### 2. ANNIS-HTML-Scrape (Sekundärquelle)

Quelle: Referenzkorpus Altdeutsch (ReA), ein tiefenannotiertes Mehrebenenkorpus aller althochdeutschen und altniederdeutschen Texte (ca. 750–1050), Teil des Verbunds „Deutsch Diachron Digital" (DDD). Ca. 650.000 Textwörter, Version 1.2 (2022-10), Lizenz CC-BY-NC-SA. Zugang weltweit kostenfrei über ANNIS4: https://korpling.german.hu-berlin.de/annis/ddd

Annotationsebenen: Primärtext (handschriftengetreue Wiedergabe), Normalisierung, POS-Tagging (DDDTS, kompatibel mit STTS), Morphologie, Lemmatisierung und Übersetzung, Satzstruktur, Metadaten.

Notkers Gesamtwerk umfasst im ReA mehr als die Hälfte der gesamten altdeutschen Textüberlieferung. Relevantes Korpus: `DDD-AD-Z-Notker-Psalmen_1.2`. Lateinische Vorlagen sind aufgenommen, annotiert und mit den ahd. Daten aligniert.

Technischer Zugang: Daten im HTML scrapebar (Token als `textval`-Attribute in `<span>`-Elementen). Liefert Handschriften-Zeilenreferenzen und dient zur Validierung der Textgestalt. Daten noch nicht im Repository (`data/raw/annis_psalm2.html` fehlt).

Zitierhinweis: Zeige, Lars Erik; Schnelle, Gohar; Klotz, Martin; Donhauser, Karin; Gippert, Jost; Lühr, Rosemarie. 2022. Deutsch Diachron Digital. Referenzkorpus Altdeutsch. Humboldt-Universität zu Berlin. DOI: https://doi.org/10.34644/laudatio-dev-MiXVDnMB7CArCQ9CABmW

### 3. Facsimile

e-codices, CSg 0021. IIIF-fähig.

- Einstieg Psalm 2: Seite 10 der Handschrift, entsprechend der Tax/Sehrt-Edition-Seite R10 (https://www.e-codices.unifr.ch/de/csg/0021/10/0/)
- IIIF-Manifest: `https://www.e-codices.unifr.ch/metadata/iiif/csg-0021/manifest.json`
- Seiten-Range für Psalm 2: Handschriftenseiten 10–13 (Edition R10–R13)

### 4. Quelleneditionen (De Gruyter)

- Quellenliste: Tax/Sehrt, S. 4–5 (https://www.degruyterbrill.com/document/doi/10.1515/9783110935332/html)
- Edition: Tax/Sehrt, S. 11 (https://www.degruyterbrill.com/document/doi/10.1515/9783110967500/html)

## Quellen-Siglen

Notkers Kommentar nennt an zwei Stellen Siglen: im Quellenapparat (am Ende einer Versgruppe) und in der Marginalspalte jeder Haupttext-Zeile. Je nach Kontext hat dieselbe Sigle verschiedene Bedeutungen — die UI-Filter lösen diese Mehrdeutigkeit über eine Section-Type-Heuristik auf.

### Gesichert: Kommentarquellen (Quellenapparat)

| Sigle | Quelle | Häufigkeit in Psalm 2 |
|---|---|---|
| A | Augustinus, Enarrationes in Psalmos | sehr häufig, umfangreichste Quelle |
| C | Cassiodor, Expositio Psalmorum | sehr häufig, zweitwichtigste Quelle |
| Br | Breviarium in Psalmos (Pseudo-Hieronymus) | selten, kurze Einträge |
| R | Remigius von Auxerre | gelegentlich |

### Gesichert: Psalmtext-Zeugen (synoptischer Vergleich)

| Sigle | Textzeuge | Handschrift |
|---|---|---|
| G | Gallicanum | nicht angegeben |
| R | Romanum | nicht angegeben |
| H | Hebraicum (iuxta Hebraeos) | Bamberg Ms. 44 |
| A | Augustinus-Psalter | St. Gallen Cod. 162 |
| C | Cassiodor-Psalter | St. Gallen Cod. 200 |

### In Klärung: Siglen in der Haupttext-Spalte

G, R, H, A, C erscheinen auch in der Marginalspalte der Haupttext-Zeilen (nicht in den Quellenapparat-Zeilen). Zwei mögliche Lesarten: textkritisch (die Zeile folgt dem Wortlaut eines bestimmten Psalmtext-Zeugen) oder quellenbezogen (die Zeile greift inhaltlich auf eine bestimmte Kommentarquelle zurück).

Die Funktion von H in der Haupttext-Spalte ist besonders offen (Hebraicum als Textvorlage oder eine eigene Kommentarquelle?) — es erscheint in Tables 2, 5, 7. Klärung durch den Auftraggeber ausstehend.

### In Klärung: Einzelvorkommen RII und N

| Sigle | Vermutung | Vorkommen | Klärungsbedarf |
|---|---|---|---|
| RII | zweite Remigius-Quelle oder -Rezension? | Table 4 Row 15, einmalig | mit Auftraggeber klären |
| N | unbekannt | Table 4 Row 5, einmalig | mit Auftraggeber klären |

Im TEI als `@cert="low"` markiert und mit `<note type="editorial">ungeklärt</note>` kommentiert.

### Disambiguierungs-Heuristik (Iteration 2)

Für die UI-Filter wird jede Sigle in der Marginalspalte des Notker-Textes anhand des zugehörigen Section-Types aufgelöst:

| Sigle | bei `psalm_citation` | bei `commentary` / `translation` / `gloss` |
|---|---|---|
| G | Gallicanum (Psalter) | Gallicanum (Psalter) — eindeutig |
| H | Hebraicum (Psalter) | Hebraicum (Psalter) — eindeutig |
| R | Romanum (Psalter) | Remigius (Patristik) |
| A, C, Br | Augustinus-/Cassiodor-/Br-Psalter | Augustinus, Cassiodor, Breviarium (Patristik) |

Begründung für den R-Fall: Steht neben einem Psalmzitat ein „R", verweist das auf den Wortlaut der Romanum-Tradition; neben einem Kommentar-Segment auf Remigius' Auslegung. Die Lesart ist konsistent mit der Notations-Praxis der Probeseite, eine Bestätigung durch den Auftraggeber steht aber noch aus.

Implementiert in `disambiguate_sigles()` (`scripts/tei_to_json.py`). Im JSON stehen die aufgelösten Siglen pro Section in zwei getrennten Listen (`sigles_psalter`, `sigles_sources`); die Frontend-Filter wirken jeweils auf das semantisch passende Feld (`psa:R` vs. `src:R`).

## Referenzsysteme

| System | Granularität | Beispiel |
|---|---|---|
| Psalmverse | Vers 1–13 | P5 = Psalm 2, Vers 5 |
| Editionszeilen | fortlaufend | Zeile 1–n (Tax/Sehrt) |
| Handschriftenzeilen | fortlaufend | Zeilen in CSg 0021 |

Die Quellenzuordnung in der Probeseite referenziert implizit die Editionszeilen. Der ANNIS-Export referenziert Handschriftenzeilen. Die Brücke muss manuell hergestellt werden.

## Probeseiten-Strukturanalyse

Systematische Analyse von `data/Probeseite_Notker.docx` als maßgebliche Primärdatenquelle des Prototyps. Die Probeseite wurde ursprünglich für eine physische Publikation erstellt, nicht für den Prototyp — das erklärt die hohe philologische Qualität und die für die Pipeline herausfordernde Tabellen-Drucksatz-Struktur.

### Tabellenstruktur

13 Tabellen in drei funktionalen Gruppen.

**Gruppe 1 — Haupttext + eingebetteter Quellenapparat:**

| Tabelle | Rows × Cols | Verse | Bemerkung |
|---|---|---|---|
| Table 1 | 18 × 5 | 1–2 | Rows 0–12: Haupttext. Rows 13–17: Quellen (C, A, R, C, C) |
| Table 3 | 13 × 5 | 5–6 | Rows 0–3: Haupttext. Rows 4–8: Quellen (C, A, Br, A, C). Rows 9–12: leer |
| Table 4 | 16 × 4 | 6–7 | Rows 0–8: Haupttext. Rows 9–15: Quellen (A, C, A, A, C, C, RII) |
| Table 7 | 21 × 6 | 8–9 | Rows 0–12: Haupttext. Rows 13–16: Quellen (A, C, A, A). Rows 17–20: leer |
| Table 11 | 7 × 5 | 12–13 | Rows 0–1: Quellen (C, A). Rows 2–3: leer. Rows 4–6: Psalmtext-Vergleich (G, R, H) |

**Gruppe 2 — Nur Haupttext (ohne eingebettete Quellen):**

| Tabelle | Rows × Cols | Verse |
|---|---|---|
| Table 2 | 13 × 3 | 3–4 (Fortsetzung von V. 2) |
| Table 5 | 9 × 3 | 7 |
| Table 8 | 9 × 3 | 10–11 |
| Table 10 | 11 × 3 | 12 |

**Gruppe 3 — Eigenständige Datenbereiche:**

| Tabelle | Rows × Cols | Inhalt |
|---|---|---|
| Table 6 | 3 × 3 | Quellenapparat zu Vers 7 (C, A) |
| Table 9 | 6 × 3 | Quellenapparat zu Vers 10–11 (C, A, C, A, Br, C) |
| Table 12 | 2 × 2 | Psalter-Vergleich: A-Psalter (Cod. 162) und C-Psalter (Cod. 200) |
| Table 13 | 2 × 1 | Wiener Notker (ÖNB Cod. 2681), Volltext Psalm 2 |

### Spaltenstruktur

Die Haupttext-Tabellen haben scheinbar 3–6 Spalten, tatsächlich aber nur 3 semantische Spalten. Spalten 0–2 enthalten identischen Text (merged cells in Word, von python-docx als separate Zellen gelesen).

Tatsächliche Spalten:

| Spalte | Inhalt | Formatierung |
|---|---|---|
| Haupttext (merged) | Notkers Text mit Farbcodierung | olive/grün/schwarz |
| nhd. Übersetzung | Arbeitsübersetzung des Auftraggebers | kursiv, keine Farbe |
| Siglen | Quellen-Siglen pro Zeile | keine Formatierung |

Quellenapparat-Zeilen (eingebettet in Haupttext-Tabellen):

| Spalte | Inhalt |
|---|---|
| Spalte 0 | Sigle (C, A, R, Br, RII, N) |
| Spalte 1 | Lateinischer Originaltext |
| Spalte 2+ | Deutsche Übersetzung (teils dupliziert über restliche Spalten) |

### Farbcodierung im Detail

Drei Farben mit funktionaler Semantik (nicht sprachbasiert).

`#806000` (Olive/Gelb) — Psalmzitation (290 Runs). Lateinische Psalmverse, wie Notker sie in seinem Text zitiert. Beispiele: `PSALVS DAVID.`, `QVARE FREMVERVNT GENTES.`, `Astiterunt reges terrȩ . et principes conuenerunt in unum aduersus dominum et aduersus christum eivs.`, `Disrumpamus uincula eorum . et proiciamus a nobis iugum ipsorum .`, `Qui habitat in celis irridebit eos . et dominus subsannabit eos.`, `Dominus dixit ad me . filius meus es tu . ego hodie genui te .`, `Postula a me`.

`#00B050` (Grün) — Übersetzung (524 Runs). Althochdeutsche Wiedergabe der Psalmzitate. Kann lateinische Einsprengsel enthalten (z.B. `cramoton an christum ebraicȩ gentes?` ist grün, obwohl teils lateinisch). Beispiele: `Ziu grís-cramoton an christum ebraicȩ gentes?`, `Vnde ziu dâhton sîne liûte ardingun . ín ze irloschenne?`, `Tie lánt-chuninga uuâren gágenuuerte in passione domini`, `Prechen cháden sie íro gebénde . unde uuerfen ába uns íro ioch.`, `Ter in hímile bûet . der spóttot íro . unde násesnûdet an_sîe.`, `Min fáter chád ze mír . mîn sun bist du . hiûto gebár ih tih.`.

Schwarz (Default) — Kommentar (3702 Runs). Notkers exegetischer Kommentar. Enthält sowohl ahd. als auch lat. Passagen. Beispiele: `idest frustura?` (lat.), `des ín ubelo spuên solta.` (ahd.), `in gotes martyro` (Glosse), `Nals taz got mit munde unde mit násun dehêinen hûoh tûe . nube daz iz huôhlîch uuas` (ahd.), `Góte neist nehêin zît prȩteritum noh futurum.` (gemischt).

Zusätzliche Formatierungen:

| Formatierung | Runs | Bedeutung |
|---|---|---|
| Kursiv (default) | 628 | nhd. Übersetzung (Spalte 3/4) |
| Fett (default) | 94 | Hervorgehobene Begriffe in Quellentexten |
| Fett+Kursiv | 7 | Hervorgehobene Begriffe in dt. Quellenübersetzung |

### Interlinearglossen-Inventar

13 Glossen (Iteration 2 reklassifiziert: V6 „ze_gótes sélbes ána-sihte. [...]" war ursprünglich als 14. Glosse erkannt, ist aber Haupttext mit `[...]`-Auslassung — Heuristik in `detect_gloss_line()` erweitert: Text mit `[...]` ist Haupttext, nicht Glosse).

Erkennungsmuster: kurze Zeilen (2–5 Wörter), keine Quellen-Sigle, Übersetzungsverhältnis 1:1, keine `[...]`-Auslassung.

| Tabelle | Row | Ahd./Lat. Text | nhd. Übersetzung | Bezug |
|---|---|---|---|---|
| T1 | R2 | iúdon diêt | Juden Volk | gentes |
| T1 | R8 | in gotes martyro | in Gottes Martyrium | passione |
| T2 | R4 | christis uobunga | Christi Glauben | christianam religionem |
| T2 | R9 | penêmida | Vorherbestimmung | prȩdistinationem |
| T2 | R11 | .i. ténchende in uppe | d.h. Denkende vergeblich | meditantes inania |
| T3 | R2 | in ubertêilido / lon / sundon | im Gericht / Lohn / Sünden | iudicio / retributio / peccatorum |
| T5 | R1 | âna zît | ohne Zeit | sine tempore |
| T5 | R3 | irgân- | vergan- | prȩteritum |
| T5 | R5 | gen / chúnftîg | gen / künftig | (Fortsetzung: prȩteritum / futurum) |
| T7 | R2 | alle liûte | alle Völker | gentes |
| T7 | R10 | uuerlt-lúste | Weltlüste | terrenas concupiscentias |
| T8 | R4 | chuninga des flêisches | Könige des Fleisches | reges terrae |
| T10 | R5 | kerich | Gericht? | ? |
| T10 | R7 | in slago dero brâuuo | im Schlag der Brauen | in ictu oculi |

Manche Glossen erstrecken sich über mehrere Zeilen (z.B. T3R2 hat drei Glossierungen in einer Zeile, T5R3+R5 sind eine zerteilte Glosse). Die Positionierung im Haupttext ist zeilenbasiert, nicht tokenbasiert.

### Siglen-Vorkommen (empirisch)

Quellenapparat-Zeilen:

| Sigle | Tables (Vorkommen) | Häufigkeit |
|---|---|---|
| C | 1, 2, 3, 4, 6, 7, 8, 9, 11 | sehr häufig |
| A | 1, 3, 4, 5, 6, 7, 9, 11 | sehr häufig |
| R | 1, 8 | gelegentlich |
| Br | 3, 9 | selten |
| RII | T4 Row 15 | einmalig (ungeklärt) |
| N | T4 Row 5 | einmalig (ungeklärt) |

Siglen-Spalte der Haupttext-Zeilen:

| Sigle(n) | Tables (Vorkommen) |
|---|---|
| G, R | 1–8, 10 (häufig) |
| A | 1, 4, 5, 7, 8 |
| C | 1, 2, 4, 7, 8 |
| H | 2, 5, 7 |

Was diese Rand-Siglen bedeuten (Psalmtext-Version vs. Kommentarquelle), ist nicht eindeutig aus der Probeseite ablesbar — siehe „In Klärung: Siglen in der Haupttext-Spalte" oben.

### Psalmtext-Vergleich: Ausgewählte Varianten

Textuell signifikante Unterschiede zwischen den Zeugen (Vers-Auswahl):

| Vers | G/R | H | Anmerkung |
|---|---|---|---|
| 1 | `fremuerunt` | `turbabuntur` | Komplett anderes Verb |
| 1 | `populi` | `tribus` | Völker vs. Stämme |
| 3 | `proiciamus` (nur A) | `piciamus` (G, R, H, C) | Orthographische Variante |
| 6 | `prȩceptum eius` (G) | `prȩceptum domini` (R, H) | eius vs. domini |
| 9 | `Reges eos` (G, R) | `Pasces eos` (H) | Herrschen vs. Weiden |
| 12 | `Apprehendite disciplinam` (G, R) | `Adorate pure` (H) | Komplett anderer Text |
| 13 | `qui condifunt in eo` (G, R) | `qui sperant in eium` (H) | Vertrauen vs. Hoffen |

Der Hebraicum-Text weicht an mehreren Stellen substantiell ab — besonders Verse 9, 12, 13 zeigen grundlegend andere Lesarten.

### Parsing-Implikationen

Erkennungsheuristiken für den Parser:

| Zeilentyp | Erkennungsmerkmal |
|---|---|
| Haupttext | Spalte 0–2 identisch, Farbe (olive/grün/schwarz), nhd. in vorletzter Spalte |
| Quellenapparat | Spalte 0 = einzelne Sigle (C, A, R, Br, RII, N), Spalte 1 = lat. Text |
| Interlinearglosse | Kurze Zeile (< 30 Zeichen), keine Sigle, kein Psalmzitat (keine olive Farbe) |
| Leerzeile | Alle Spalten leer |

Technische Herausforderungen:

1. Merged Cells. Spalten 0–2 sind in Word gemerged; python-docx liest sie als separate, identische Zellen. Parser muss dies erkennen und deduplizieren.
2. Variable Spaltenanzahl. Tables haben 3–6 Spalten. Die semantische Struktur (Haupttext | nhd. | Siglen) ist stabil, die physische Spaltenanzahl nicht.
3. Zeilenumbrüche. Text ist zeilenweise auf Tabellenzeilen verteilt, nicht nach semantischen Einheiten. Wörter werden am Zeilenende getrennt (z.B. `grís-` / `cramoton`).
4. Farbextraktion. Run-Level-Analyse nötig (nicht Paragraph-Level). Ein Paragraph kann Runs in verschiedenen Farben enthalten.
5. Glossen-Erkennung. Keine explizite Markierung im DOCX. Heuristik basiert auf Zeilenlänge und Kontext.
6. Vers-Zuordnung. Nicht explizit in den Tabellen. Muss aus den Paragraphen-Überschriften zwischen den Tabellen abgeleitet werden (z.B. `P0: 2,1-2`, `P2: 2,3-2,5`).

## Verknüpfungen

- [[INDEX]] — Navigation und Begriffslexikon
- [[project]] — Projektidentität und Phasen
- [[architecture]] — Pipeline und JSON-Schema, die auf diese Daten aufsetzen
- [[editorial-guidelines]] — TEI-Kodierungsregeln pro Textphänomen
