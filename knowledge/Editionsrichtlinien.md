---
type: encoding-guidelines
created: 2026-03-23
updated: 2026-04-16
status: active
tags: [notker, tei, encoding, guidelines]
---

# Editionsrichtlinien: Notkers Psalmenkommentar

Kodierungsrichtlinien für die digitale Edition von Notkers Psalmenkommentar in TEI-XML. Dieses Dokument beschreibt alle Textphänomene, die in der Probeseite vorkommen, und legt fest, wie sie kodiert werden. Es dient als Referenz für die manuelle Nachbearbeitung, die Erweiterung auf alle 150 Psalmen und die Kommunikation mit dem Auftraggeber.

---

## 1. Textphänomene und ihre Kodierung

### 1.1 Funktionale Textschichten

Notkers Text ist ein Geflecht aus drei funktionalen Schichten, die in der Handschrift CSg 0021 verschränkt sind und sich durch Farbcodierung (Handschrift: rot/schwarz, Probeseite: olive/grün/schwarz) unterscheiden.

**Kodierung:** Jede Schicht wird als `<seg>` mit `@type` und `@ana` (Verweis auf die Taxonomie im Header) kodiert.

#### 1.1.1 Psalmzitation

Notker zitiert den lateinischen Psalmvers (Vulgata). In der Handschrift rot, in der Probeseite olive (#806000). Typischerweise in Majuskeln (z.B. `QVARE FREMVERVNT GENTES`), aber auch in Normalschrift innerhalb des Textflusses.

```xml
<seg type="psalm" ana="#fn-psalm" xml:lang="la">QVARE FREMVERVNT GENTES.</seg>
```

- `@type="psalm"` — Textfunktion
- `@ana="#fn-psalm"` — Verweis auf Taxonomie `textfunction` im Header
- `@xml:lang="la"` — Immer Latein

**Abgrenzung:** Nicht immer wörtliches Vulgata-Zitat. Notker paraphrasiert gelegentlich. Deshalb `<seg>` statt `<quote>`. Wo die Vulgata wörtlich zitiert wird, kann zusätzlich `<cit>` gesetzt werden (im Prototyp nicht umgesetzt).

#### 1.1.2 Übersetzung

Notkers althochdeutsche Wiedergabe der Psalmzitate. In der Handschrift schwarz, in der Probeseite grün (#00B050). Folgt dem Psalmtext zeilenweise.

```xml
<seg type="translation" ana="#fn-transl" xml:lang="goh">Ziu grís-<lb break="no"/></seg>
```

- `@type="translation"` — Textfunktion
- `@xml:lang="goh"` — Althochdeutsch (ISO 639-3)

**Sprachmischung:** Die Übersetzungsschicht enthält lateinische Einsprengsel, wenn Notker Begriffe im Original belässt (z.B. `cramoton an christum ebraicȩ gentes?`). Diese werden mit `<foreign xml:lang="la">` markiert (siehe 1.2).

#### 1.1.3 Kommentar

Notkers exegetische Erläuterung. In der Handschrift schwarz, in der Probeseite schwarz (default). Enthält sowohl ahd. als auch lat. Passagen frei gemischt. Die Farbe markiert die rhetorische Funktion (Exegese), nicht die Sprache.

```xml
<seg type="commentary" ana="#fn-comm" xml:lang="goh">
  <foreign xml:lang="la">idest</foreign> frustura?
</seg>
```

- `@type="commentary"` — Textfunktion
- `@xml:lang="goh"` — Default-Sprache (ahd. überwiegt im Kommentar)
- Lateinische Passagen innerhalb als `<foreign xml:lang="la">`

**Entscheidung:** `xml:lang="goh"` als Default für den Kommentar, weil Althochdeutsch statistisch häufiger ist. Rein lateinische Kommentarsegmente erhalten `xml:lang="la"` auf dem `<seg>` selbst.

### 1.2 Sprachwechsel (Code-Switching)

Notkers Text wechselt ständig zwischen Althochdeutsch und Latein, oft mitten im Satz. Dies ist ein Kernmerkmal seiner Schreibpraxis und muss kodiert werden.

**Kodierung:** `<foreign xml:lang="...">` innerhalb jedes `<seg>`, das Wörter der jeweils anderen Sprache enthält.

```xml
<!-- Ahd. Übersetzung mit lat. Einsprengseln -->
<seg type="translation" ana="#fn-transl" xml:lang="goh">
  cramoton an <foreign xml:lang="la">christum ebraicȩ gentes</foreign>?
</seg>

<!-- Ahd. Kommentar mit lat. Fachterminus -->
<seg type="commentary" ana="#fn-comm" xml:lang="goh">
  daz sie sîna <foreign xml:lang="la">prȩdistinationem</foreign> dâhton ze iruuendenne.
</seg>

<!-- Lat. Kommentar (selten, kein <foreign> nötig) -->
<seg type="commentary" ana="#fn-comm" xml:lang="la">idest sine tempore.</seg>
```

**Prinzip:** Die Default-Sprache des `<seg>` bestimmt, was *nicht* getaggt wird. Nur die jeweils fremde Sprache bekommt `<foreign>`. Wenn ein ganzes Segment in der anderen Sprache steht, wird `@xml:lang` auf dem `<seg>` selbst gesetzt.

**Grenzfälle:**
- Integrierte Lehnwörter (z.B. `christum` in ahd. Kontext): werden mit `<foreign>` getaggt, weil sie morphologisch lat. sind
- Ahd. Funktionswörter in lat. Kontext (z.B. `in` als Präposition): werden *nicht* getaggt, wenn sie in beiden Sprachen identisch sind und der Kontext eindeutig lat. ist
- Eigennamen (z.B. `herodes`, `ierusalem`): werden nicht mit `<foreign>` getaggt, da sprachlich neutral

### 1.3 Interlinearglossen

Einzelwort- oder Kurzübersetzungen, die im Textfluss als eigene Zeilen erscheinen. 14 Stück in Psalm 2. Übersetzen typischerweise einen lateinischen Fachterminus ins Althochdeutsche.

**Kodierung:** Eigene `<ab>` mit `@ana="#fn-gloss"`, darin `<gloss>`.

```xml
<ab ana="#fn-gloss" n="3">
  <gloss xml:lang="goh">iúdon diêt</gloss>
  <note type="translation_gloss" xml:lang="de">Juden Volk</note>
</ab>
```

**Erkennungsmerkmale im DOCX:**
- Kurze Zeile (≤ 5 Wörter)
- Nur schwarze Runs (keine olive/grüne Farbe)
- nhd-Spalte hat ebenfalls kurze Übersetzung
- Kein Satzschlusszeichen, keine Klammern

**Nicht kodiert:** Das Bezugswort (lat. Terminus, den die Glosse übersetzt) wird im Prototyp nicht explizit verknüpft, da die Zuordnung in der Probeseite positionsbasiert (Zeile), nicht tokenbasiert ist. Für das Gesamtprojekt wäre `@target` auf `<gloss>` mit Verweis auf eine `@xml:id` im Haupttext die saubere Lösung.

### 1.4 Neuhochdeutsche Übersetzung

Arbeitsübersetzung des Auftraggebers zum gesamten Notker-Text. Zeilenweise in der Probeseite (kursiv, keine Farbe). Ist nicht Teil der Edition im engeren Sinn, sondern philologische Arbeitsgrundlage.

**Kodierung:** Pro Versgruppe als `<note type="translation_nhd" resp="#pfeifer" xml:lang="de">`
mit zwei parallelen Repräsentationen — Fließtext und zeilengetreue Aufteilung:

```xml
<note type="translation_nhd" resp="#pfeifer" xml:lang="de">
  <p>WARUM LÄRMTEN DIE VÖLKER. Warum wüteten an Christus ...</p>
  <lg type="line-faithful">
    <l>Der Herr sagte zu mir: Mein Sohn bist du, ich habe</l>
    <l>dich heute geboren, d.h. ohne Zeit. Mein Vater sagte zu mir,</l>
    <l>mein Sohn bist du, heute gebar ich dich. Gott nicht ist keine Zeit ver-</l>
    <l>gangen noh zukünftig...</l>
  </lg>
</note>
```

- `@resp="#pfeifer"` — Attribution an den Übersetzer (deklariert im Header als `<editor>`)
- Im `<note>`, nicht als `<seg>`, weil es kein Teil von Notkers Text ist
- `<p>` ist Lese-Ansicht (Fließtext, Review-Korrekturen einschließlich Cross-Line-Patterns)
- `<lg type="line-faithful">` mit `<l>` pro Zeile bildet die zeilengetreue
  Aufteilung ab. Trailing-Bindestriche bleiben (markieren Zeilen-Trennung wie in der Druckedition).
- Iteration 2 / US-9: Frontend rendert Edition zeilengenau, Pool nhd. als Fließtext mit aufgelösten Bindestrichen.

### 1.5 Quellenapparat

Patristische Quellentexte (Augustinus, Cassiodor, Remigius, Breviarium), auf die sich Notker bezieht. In der Probeseite als eigene Tabellenzeilen mit Sigle, lat. Original und dt. Übersetzung.

**Kodierung:** Pro Vers als `<note type="sources">` mit `<cit>`-Elementen.

```xml
<note type="sources">
  <cit ana="#src-C">
    <bibl>Cassiodor</bibl>
    <quote xml:lang="la">Quattuor membris psalmi huius species
      decora formata est. [...] cum <hi rend="bold">causas
      iracundiae</hi> non haberent.</quote>
    <note type="translation" resp="#pfeifer" xml:lang="de">
      In vier Teilen ist dieses Psalms schöne Gestalt geformt. [...]
    </note>
  </cit>
</note>
```

- `@ana="#src-C"` → Verweis auf `<bibl xml:id="src-C">` im `<sourceDesc>/<listBibl>`
- `<bibl>` → Kurzname der Quelle
- `<quote xml:lang="la">` → Lateinischer Originaltext
- `<hi rend="bold">` → Hervorgehobene Begriffe (aus DOCX-Bold)
- `<note type="translation">` → dt. Arbeitsübersetzung der Quelle

**Warum `<cit>` statt `<app>`?** Die Quellen sind Notkers Vorlagen (Zitate), keine textkritischen Varianten. `<app>` wird nur im Psaltervergleich verwendet (siehe 1.7).

### 1.6 Siglen am Zeilenrand

In der Probeseite steht in der letzten Spalte jeder Haupttext-Zeile eine oder mehrere Siglen (z.B. „G, R", „A", „C, R"). Ihre genaue Semantik ist ungeklärt.

**Kodierung:**

```xml
<note type="sigle" place="margin">G, R</note>
```

**Offene Frage (mit dem Auftraggeber zu klären):** Bezeichnen G und R in der Haupttext-Spalte die Psalmtext-Version, der die Zeile textlich folgt (textkritische Angabe)? Oder markieren sie, welche Kommentarquelle Notker an dieser Stelle benutzt? Die Siglen A und C erscheinen sowohl als Kommentarquellen (im Quellenapparat) als auch in der Haupttext-Siglen-Spalte — die Kontexte sind verschieden.

Bis zur Klärung: keine semantische Auszeichnung über `<note>` hinaus.

### 1.7 Psaltervergleich

Fünf Psalmtext-Versionen synoptisch (Gallicanum, Romanum, Hebraicum, Augustinus-Psalter, Cassiodor-Psalter). In der Probeseite als eigene Tabellen am Ende.

**Kodierung:** Im `<back>` als `<div type="psalm_comparison">` mit `<app>/<rdg>`.

```xml
<div type="psalm_comparison">
  <app>
    <rdg wit="#wit-G">Quare fremuerunt gentes...</rdg>
    <rdg wit="#wit-H">Quare turbabuntur gentes...</rdg>
  </app>
</div>
```

- `@wit` verweist auf `<witness>` in `<sourceDesc>/<listWit>`
- Im `<back>`, nicht `<body>` (nicht Teil von Notkers Text)
- `<variantEncoding method="parallel-segmentation" location="internal"/>` im Header deklariert

### 1.8 Wiener Notker

Paralleltext zu Psalm 2 aus ÖNB Cod. 2681 (Edition Heinzle & Scherrer). Zeigt eine spätere/andere Überlieferungsstufe desselben Textes.

**Kodierung:** Im `<back>` als Rohtext.

```xml
<div type="parallel_tradition" source="#wiener_notker">
  <head>Wiener Notker (ÖNB Cod. 2681)</head>
  <ab>1Quare fremuerunt gentes, et populi meditati sunt inania? [...]</ab>
</div>
```

Keine Feincodierung (Schichten, Sprachtrennung) im Prototyp. Das Gesamtprojekt kann den Wiener Notker separat aufbereiten.

---

## 2. Physische vs. logische Struktur

### 2.1 Zeilenstruktur

Jede Tabellenzeile der Probeseite wird als `<ab>` (anonymous block) abgebildet. Das bewahrt die physische Struktur 1:1.

```xml
<ab n="4">
  <seg type="translation" ...>cramoton an christum ...</seg>
  <seg type="psalm" ... part="I">Et populi medi-<lb break="no"/></seg>
  <note type="sigle" place="margin">C</note>
</ab>
```

### 2.2 Zeilenübergreifende Segmente

Wenn ein Segment über die Zeilengrenze hinausgeht (z.B. durch Silbentrennung), wird `@part` verwendet:

- `@part="I"` (Initial) — Segment beginnt hier, wird fortgesetzt
- `@part="M"` (Medial) — Segment-Fortsetzung, wird weiter fortgesetzt
- `@part="F"` (Final) — Letztes Teilsegment

```xml
<ab n="4">
  <seg type="psalm" ana="#fn-psalm" xml:lang="la" part="I">Et populi medi-<lb break="no"/></seg>
</ab>
<ab n="5">
  <seg type="psalm" ana="#fn-psalm" xml:lang="la" part="F">tati sunt inania.</seg>
</ab>
```

**Entscheidung:** Innerhalb eines Verses nur `@part`, nicht `@next`/`@prev`. TEI P5 dokumentiert beide als äquivalent. `@part` ist kompakter und die Reihenfolge im Dokument ist implizit.

**Cross-Verse-Verkettung (Iteration 2):** Wenn ein Wort über die Vers-Grenze geteilt
ist (z.B. V1-2 endet mit „han-" und V3-5 beginnt mit „gta"), reicht `@part` allein
nicht — die Reihenfolge ist über die Vers-Grenze hinweg nicht implizit. Daher
zusätzlich `@xml:id="seg-cross-N-i"`/`-f"` mit `@next`/`@prev`-Verweisen:

```xml
<!-- Vers 1-2 letzte Zeile -->
<seg type="commentary" xml:lang="goh" part="I" xml:id="seg-cross-1-i" next="#seg-cross-1-f">
  ...uuolta ín slâhen . anderer han-
</seg>

<!-- Vers 3-5 erste Zeile -->
<seg type="commentary" xml:lang="goh" part="F" xml:id="seg-cross-1-f" prev="#seg-cross-1-i">
  gta iz. Pedíu gât ín ter uuíllo...
</seg>
```

Implementiert in `chain_cross_verse_hyphens()` (`build_tei.py`). Die textliche
Zusammenführung („han-" + „gta" → „hangta") erfolgt im JSON via
`merge_cross_verse_hyphens()` für die UI-Lese-Ansicht.

### 2.3 Silbentrennung

Wörter, die am Zeilenende getrennt werden, werden mit `<lb break="no"/>` markiert.

```xml
<seg ...>Ziu grís-<lb break="no"/></seg>
```

**Achtung:** Althochdeutsche Komposita mit Bindestrich (z.B. `lánt-chuninga`, `ne-lâzen`) sind *keine* Silbentrennungen. Der Bindestrich gehört zum Wort. Der Parser unterscheidet: Trennung nur am Zeilenende, wenn die nächste Zeile mit dem gleichen Segmenttyp fortfährt (`@part`).

### 2.4 Akzentzeichen

Notkers Text verwendet Akzentzeichen (z.B. `grís`, `dâhton`, `hêiligen`). Diese werden als Unicode-Zeichen bewahrt, nicht normalisiert. Sie sind Teil der Edition.

---

## 3. Header-Deklarationen

### 3.1 Taxonomie der Textfunktionen

Im `<encodingDesc>/<classDecl>/<taxonomy xml:id="textfunction">`:

| ID | Beschreibung |
|---|---|
| `fn-psalm` | Psalmzitation: Lateinischer Vulgata-Text, wie Notker ihn zitiert |
| `fn-transl` | Übersetzung: Althochdeutsche Wiedergabe der Psalmzitate |
| `fn-comm` | Kommentar: Notkers Exegese (ahd. und lat. gemischt) |
| `fn-gloss` | Interlinearglosse: Einzelwort- oder Kurzübersetzung |

### 3.2 Quellendeklaration

**Textzeugen** (Psalter-Handschriften) in `<sourceDesc>/<listWit>`:

| ID | Zeuge | Handschrift |
|---|---|---|
| `wit-G` | Gallicanum | — |
| `wit-R` | Romanum | — |
| `wit-H` | Hebraicum | Bamberg Ms. 44 |
| `wit-A-psa` | Augustinus-Psalter | St. Gallen Cod. 162 |
| `wit-C-psa` | Cassiodor-Psalter | St. Gallen Cod. 200 |

**Kommentarquellen** (Werke) in `<sourceDesc>/<listBibl>`:

| ID | Autor | Werk | Status |
|---|---|---|---|
| `src-A` | Augustinus | Enarrationes in Psalmos | gesichert |
| `src-C` | Cassiodor | Expositio Psalmorum | gesichert |
| `src-R` | Remigius | — | gesichert (Sigle teilt sich mit `wit-R` Romanum-Psalter) |
| `src-Br` | — | Breviarium | gesichert |
| `src-RII` | — | RII | ungeklärt (`cert="low"`) |
| `src-N` | — | N | ungeklärt (`cert="low"`) |

**R-Disambiguierung (Iteration 2):** Die Sigle „R" ist im Datenmodell ambig: sie
bezeichnet sowohl das Romanum (`wit-R`, Psalter-Zeuge) als auch Remigius (`src-R`,
patristische Quelle). Die JSON-Pipeline (`disambiguate_sigles()` in
`tei_to_json.py`) löst das per Section-Type-Heuristik:

- R-Marginnote auf einer Section vom Typ `psalm_citation` → Romanum (Psalter)
- R-Marginnote auf einer Section vom Typ `commentary`/`translation`/`gloss` → Remigius (Patristik)

Begründung: Wenn Notker einen Psalmtext zitiert und am Rand „R" steht, verweist
das auf den Wortlaut der Romanum-Psalter-Tradition. Steht „R" neben einem
Kommentar-Segment, ist es eine Quellen-Referenz auf Remigius' Auslegung. Die
Heuristik ist plausibel und konsistent mit der Notations-Praxis in der
Probeseite, wartet aber auf finale Bestätigung.

JSON-Output pro Section: `sigles_psalter` und `sigles_sources` als zwei getrennte
Listen. Frontend-Filter wirkt mit Präfix-Keys (`psa:R` vs. `src:R`).

### 3.3 Segmentierungsbeschreibung

Im `<encodingDesc>/<segmentation>`: Beschreibung der funktionalen Textschichten-Segmentierung, basierend auf der Farbcodierung der Probeseite.

### 3.4 Variantenkodierung

`<variantEncoding method="parallel-segmentation" location="internal"/>` — deklariert die Methode für `<app>/<rdg>` im Psaltervergleich.

---

## 4. Ungeklärte Phänomene

| Phänomen | Status | Auswirkung auf Kodierung |
|---|---|---|
| Siglen G, R in Haupttext-Spalte | Mit Auftraggeber klären | `<note type="sigle">` ohne semantische Typisierung |
| Sigle H im Haupttext | Mit Auftraggeber klären | Psalter-Zeuge oder Kommentarquelle? |
| Siglen RII, N | Mit Auftraggeber klären | `<bibl cert="low">` mit `<note type="editorial">` |
| Querverweise auf Bibelstellen | Daten fehlen | Nicht kodiert, im Datenmodell vorbereitet |
| Versgrenze 12/13 | DOCX hat nur „2,12" | Vers 13 als Stub, Daten in Vers 12 |

---

## 5. Konventionen für das Gesamtprojekt

### 5.1 Erweiterung auf weitere Psalmen

Die Kodierung ist für Psalm 2 entwickelt, aber auf alle 150 Psalmen skalierbar:

- Pro Psalm ein `<div type="psalm" n="X">` im `<body>`
- Versgruppen und Einzelverse als `<div type="verse" n="...">`
- Quellenapparat pro Vers
- Psaltervergleich und Wiener Notker im `<back>` (psalm-übergreifend)

### 5.2 Referenzprojekte

- **BIBLINDEX** (biblindex.org): Patristische Bibelzitate, `<cit>`-Konvention
- **Patristic Text Archive** (pta.bbaw.de): Encoding-Guidelines für patristische Kommentare, EpiDoc + CapiTainS
- **TEI P5 Guidelines**: Kap. 12 (Critical Apparatus), Kap. 13 (Names, Dates, People, Places), Kap. 16 (Linking), Kap. 17 (Simple Analytic Mechanisms)

### 5.3 Sprach-Codes

| Code | Sprache | ISO |
|---|---|---|
| `goh` | Althochdeutsch | ISO 639-3 |
| `la` | Latein | ISO 639-1 |
| `de` | Neuhochdeutsch | ISO 639-1 |

---

## Verknüpfungen

- [[Probeseite Analyse]] — Empirische Grundlage (Tabellenstruktur, Farben, Glossen)
- [[Domänenwissen]] — Textschichten, Siglen, Referenzsysteme
- [[Technik]] — Pipeline, TEI-Modell, JSON-Schema und Web-Stack
