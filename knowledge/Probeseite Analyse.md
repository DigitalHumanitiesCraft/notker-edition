---
type: analysis
created: 2026-03-23
status: complete
tags: [data-analysis, probeseite, notker]
---

# Probeseite Analyse

Systematische Analyse von `data/Probeseite_Notker.docx` — der maßgeblichen Primärdatenquelle für den Prototyp. Die Probeseite wurde ursprünglich für eine physische Publikation erstellt, nicht für den Prototyp. Das erklärt die hohe philologische Qualität. Finale Lieferung: 21.03.2026.

## Tabellenstruktur

13 Tabellen in drei funktionalen Gruppen:

### Gruppe 1: Haupttext + eingebetteter Quellenapparat

| Tabelle | Rows × Cols | Verse | Bemerkung |
|---|---|---|---|
| Table 1 | 18 × 5 | 1–2 | Rows 0–12: Haupttext. Rows 13–17: Quellen (C, A, R, C, C) |
| Table 3 | 13 × 5 | 5–6 | Rows 0–3: Haupttext. Rows 4–8: Quellen (C, A, Br, A, C). Rows 9–12: leer |
| Table 4 | 16 × 4 | 6–7 | Rows 0–8: Haupttext. Rows 9–15: Quellen (A, C, A, A, C, C, RII) |
| Table 7 | 21 × 6 | 8–9 | Rows 0–12: Haupttext. Rows 13–16: Quellen (A, C, A, A). Rows 17–20: leer |
| Table 11 | 7 × 5 | 12–13 | Rows 0–1: Quellen (C, A). Rows 2–3: leer. Rows 4–6: **Psalmtext-Vergleich** (G, R, H) |

### Gruppe 2: Nur Haupttext (ohne eingebettete Quellen)

| Tabelle | Rows × Cols | Verse |
|---|---|---|
| Table 2 | 13 × 3 | 3–4 (Fortsetzung von V. 2) |
| Table 5 | 9 × 3 | 7 |
| Table 8 | 9 × 3 | 10–11 |
| Table 10 | 11 × 3 | 12 |

### Gruppe 3: Eigenständige Datenbereiche

| Tabelle | Rows × Cols | Inhalt |
|---|---|---|
| Table 6 | 3 × 3 | Quellenapparat zu Vers 7 (C, A) |
| Table 9 | 6 × 3 | Quellenapparat zu Vers 10–11 (C, A, C, A, Br, C) |
| Table 12 | 2 × 2 | Psalter-Vergleich: A-Psalter (Cod. 162) und C-Psalter (Cod. 200) |
| Table 13 | 2 × 1 | Wiener Notker (ÖNB Cod. 2681), Volltext Psalm 2 |

## Spaltenstruktur

Die Haupttext-Tabellen haben **scheinbar** 3–6 Spalten, tatsächlich aber nur 3 semantische Spalten. Spalten 0–2 enthalten **identischen Text** (merged cells in Word, von python-docx als separate Zellen gelesen).

**Tatsächliche Spalten:**

| Spalte | Inhalt | Formatierung |
|---|---|---|
| Haupttext (merged) | Notkers Text mit Farbcodierung | olive/grün/schwarz |
| nhd. Übersetzung | Philipps Arbeitsübersetzung | kursiv, keine Farbe |
| Siglen | Quellen-Siglen pro Zeile | keine Formatierung |

**Quellenapparat-Zeilen** (eingebettet in Haupttext-Tabellen):

| Spalte | Inhalt |
|---|---|
| Spalte 0 | Sigle (C, A, R, Br, RII, N) |
| Spalte 1 | Lateinischer Originaltext |
| Spalte 2+ | Deutsche Übersetzung (teils dupliziert über restliche Spalten) |

## Farbcodierung

Drei Farben mit **funktionaler** Semantik (NICHT sprachbasiert):

### `#806000` (Olive/Gelb) — Psalmzitation (290 Runs)

Lateinische Psalmverse, wie Notker sie in seinem Text zitiert. Das ist Notkers eigene Wiedergabe der Vulgata, eingebettet in den Kommentarfluss.

Beispiele:
- `PSALVS DAVID.`
- `QVARE FREMVERVNT GENTES.`
- `Astiterunt reges terrȩ . et principes conuenerunt in unum aduersus dominum et aduersus christum eivs.`
- `Disrumpamus uincula eorum . et proiciamus a nobis iugum ipsorum .`
- `Qui habitat in celis irridebit eos . et dominus subsannabit eos.`
- `Dominus dixit ad me . filius meus es tu . ego hodie genui te .`
- `Postula a me`

### `#00B050` (Grün) — Übersetzung (524 Runs)

Althochdeutsche Wiedergabe der Psalmzitate. Kann lateinische Einsprengsel enthalten (z.B. `cramoton an christum ebraicȩ gentes?` ist grün, obwohl teils lateinisch).

Beispiele:
- `Ziu grís-cramoton an christum ebraicȩ gentes?`
- `Vnde ziu dâhton sîne liûte ardingun . ín ze irloschenne?`
- `Tie lánt-chuninga uuâren gágenuuerte in passione domini`
- `Prechen cháden sie íro gebénde . unde uuerfen ába uns íro ioch.`
- `Ter in hímile bûet . der spóttot íro . unde násesnûdet an_sîe.`
- `Min fáter chád ze mír . mîn sun bist du . hiûto gebár ih tih.`

### Schwarz (Default) — Kommentar (3702 Runs)

Notkers exegetischer Kommentar. Enthält SOWOHL ahd. als AUCH lat. Passagen. Die Farbe codiert die Textfunktion "Kommentar/Exegese", nicht die Sprache.

Beispiele:
- `idest frustura?` (lat. Kommentar)
- `des ín ubelo spuên solta.` (ahd. Kommentar)
- `in gotes martyro` (Interlinearglosse)
- `Nals taz got mit munde unde mit násun dehêinen hûoh tûe . nube daz iz huôhlîch uuas` (ahd. Kommentar)
- `Góte neist nehêin zît prȩteritum noh futurum.` (ahd./lat. gemischter Kommentar)

### Zusätzliche Formatierungen

| Formatierung | Runs | Bedeutung |
|---|---|---|
| Kursiv (default) | 628 | nhd. Übersetzung (Spalte 3/4) |
| Fett (default) | 94 | Hervorgehobene Begriffe in Quellentexten |
| Fett+Kursiv | 7 | Hervorgehobene Begriffe in dt. Quellenübersetzung |

## Interlinearglossen

14 identifizierte Glossen. Erkennungsmuster: kurze Zeilen (2–5 Wörter), keine Quellen-Sigle, Übersetzungsverhältnis 1:1.

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

**Anmerkung:** Manche Glossen erstrecken sich über mehrere Zeilen (z.B. T3R2 hat drei Glossierungen in einer Zeile, T5R3+R5 sind eine zerteilte Glosse). Die Positionierung im Haupttext ist zeilenbasiert, nicht tokenbasiert.

## Quellen-Siglen: Vollständiges Inventar

### In Quellenapparat-Zeilen (Kommentarquellen)

| Sigle | Quelle | Vorkommen (Tables) | Häufigkeit |
|---|---|---|---|
| C | Cassiodor, Expositio Psalmorum | 1, 2, 3, 4, 6, 7, 8, 9, 11 | Sehr häufig |
| A | Augustinus, Enarrationes in Psalmos | 1, 3, 4, 5, 6, 7, 9, 11 | Sehr häufig |
| R | Remigius | 1, 8 | Gelegentlich |
| Br | Breviarium | 3, 9 | Selten |
| RII | Unbekannt (zweite Remigius-Quelle?) | 4 (Row 15, einmalig) | Einmal |
| N | Unbekannt | 4 (Row 5, einmalig) | Einmal |

### In Siglen-Spalte der Haupttext-Zeilen

| Sigle(n) | Bedeutung | Vorkommen |
|---|---|---|
| G, R | Vermutlich: Zeile folgt Gallicanum/Romanum-Textgestalt | Häufig (Tables 1–8, 10) |
| A | Kontext: Augustinus als Kommentarquelle (NICHT Psalter-Zeuge) | Tables 1, 4, 5, 7, 8 |
| C | Kontext: Cassiodor als Kommentarquelle (NICHT Psalter-Zeuge) | Tables 1, 2, 4, 7, 8 |
| H | Unklar: Hebraicum-Psalter oder Kommentarquelle? | Tables 2, 5, 7 |

**Offenes Problem:** G und R in der Siglen-Spalte könnten anzeigen, welcher Psalmtext-Version die Zeile textlich folgt (= textkritische Angabe), oder sie könnten Kommentarquellen markieren. Dies ist mit Philipp zu klären.

### Im Psalmtext-Vergleich (Table 11 Rows 4–6 + Table 12)

| Sigle | Zeuge | Handschrift |
|---|---|---|
| G | Gallicanum | nicht angegeben |
| R | Romanum | nicht angegeben |
| H | Hebraicum (iuxta Hebraeos) | Staatsbibliothek Bamberg Ms. 44 |
| A | Augustinus-Psalter | St. Gallen Cod. 162 |
| C | Cassiodor-Psalter | St. Gallen Cod. 200 |

## Psalmtext-Vergleich: Ausgewählte Varianten

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

## Parsing-Implikationen

### Erkennungsheuristiken für den Parser

| Zeilentyp | Erkennungsmerkmal |
|---|---|
| Haupttext | Spalte 0–2 identisch, Farbe (olive/grün/schwarz), nhd. in vorletzter Spalte |
| Quellenapparat | Spalte 0 = einzelne Sigle (C, A, R, Br, RII, N), Spalte 1 = lat. Text |
| Interlinearglosse | Kurze Zeile (< 30 Zeichen?), keine Sigle, kein Psalmzitat (keine olive Farbe) |
| Leerzeile | Alle Spalten leer |

### Technische Herausforderungen

1. **Merged Cells:** Spalten 0–2 sind in Word gemerged; python-docx liest sie als separate, identische Zellen. Parser muss dies erkennen und deduplizieren.
2. **Variable Spaltenanzahl:** Tables haben 3–6 Spalten. Die semantische Struktur (Haupttext | nhd. | Siglen) ist stabil, die physische Spaltenanzahl nicht.
3. **Zeilenumbrüche:** Text ist zeilenweise auf Tabellenzeilen verteilt, nicht nach semantischen Einheiten. Wörter werden am Zeilenende getrennt (z.B. `grís-` / `cramoton`).
4. **Farbextraktion:** Run-Level-Analyse nötig (nicht Paragraph-Level). Ein Paragraph kann Runs in verschiedenen Farben enthalten.
5. **Glossen-Erkennung:** Keine explizite Markierung im DOCX. Heuristik basiert auf Zeilenlänge und Kontext.
6. **Vers-Zuordnung:** Nicht explizit in den Tabellen. Muss aus den Paragraphen-Überschriften zwischen den Tabellen abgeleitet werden (z.B. `P0: 2,1-2`, `P2: 2,3-2,5`).

## Verknüpfungen

- [[Research Plan]] — Gesamtplan und Phasen
- [[Domänenwissen]] — Informationsschichten und Siglen
- [[Technik]] — JSON-Schema und Parsing-Strategie
