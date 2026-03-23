---
type: technical
created: 2026-03-23
updated: 2026-03-23
status: decided
tags: [notker, tei, implementation, pipeline]
---

# Implementation: TEI-Modell und DOCX→TEI-Pipeline

Dieses Dokument beschreibt (1) das TEI-XML-Modell für die digitale Edition von Notkers Psalmenkommentar, (2) die Python-Pipeline DOCX → TEI-XML und (3) offene technische Entscheidungen. Es basiert auf der maschinellen Analyse der Probeseite (`data/Probeseite_Notker.docx`) und synthetisiert [[Probeseite Analyse]], [[Domänenwissen]] und [[Anforderungen]].

**Grundsatz:** Das TEI-XML ist die Single Source of Truth. Nachgelagerte Formate (JSON für Web-UI) werden daraus abgeleitet. Siehe [[Technik]] für das JSON-Schema und den Web-Stack.

---

## 1. TEI-XML-Modell

### 1.1 Dokumentstruktur

```xml
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="goh">
  <teiHeader><!-- 1.2 --></teiHeader>
  <facsimile><!-- IIIF-Surfaces --></facsimile>
  <text>
    <front>
      <div type="introduction"><!-- Einleitungstext für Gutachter --></div>
    </front>
    <body>
      <div type="psalm" n="2">
        <head>Psalm 2</head>
        <!-- 13 × <div type="verse">, siehe 1.3 -->
      </div>
    </body>
    <back>
      <div type="psalm_comparison"><!-- Synoptischer Psaltervergleich, 1.7 --></div>
      <div type="parallel_tradition" source="#wiener_notker"><!-- 1.8 --></div>
    </back>
  </text>
</TEI>
```

`xml:lang="goh"` (ISO 639-3 Althochdeutsch) als Default, weil der Großteil von Notkers eigenem Text ahd. ist. Lat. Passagen lokal mit `xml:lang="la"` überschrieben.

### 1.2 teiHeader (Kurzfassung)

```xml
<teiHeader>
  <fileDesc>
    <titleStmt>
      <title>Notkers Psalmenkommentar – Psalm 2 (Prototyp)</title>
      <author>Notker III. von St. Gallen</author>
      <editor xml:id="pfeifer">Philipp Pfeifer</editor>
      <respStmt>
        <resp>Digitale Aufbereitung</resp>
        <orgName>Digital Humanities Craft OG</orgName>
      </respStmt>
    </titleStmt>
    <sourceDesc>
      <msDesc xml:id="csg0021">
        <msIdentifier>
          <settlement>St. Gallen</settlement>
          <repository>Stiftsbibliothek</repository>
          <idno>CSg 0021</idno>
        </msIdentifier>
      </msDesc>
      <bibl xml:id="tax_sehrt">Tax/Sehrt, Der Psalter (1979), S. R10–R13</bibl>
      <bibl xml:id="wiener_notker">ÖNB Cod. 2681, Ed. Heinzle &amp; Scherrer</bibl>
      <bibl xml:id="rea_corpus">ReA/DDD, DOI:10.34644/laudatio-dev-MiXVDnMB7CArCQ9CABmW</bibl>
    </sourceDesc>
  </fileDesc>
  <encodingDesc>
    <classDecl>
      <!-- Funktionale Textschichten -->
      <taxonomy xml:id="textfunction">
        <category xml:id="fn-psalm">
          <catDesc>Psalmzitation (lat. Vulgata, wie Notker zitiert)</catDesc>
        </category>
        <category xml:id="fn-transl">
          <catDesc>Übersetzung (ahd. Wiedergabe der Psalmzitate)</catDesc>
        </category>
        <category xml:id="fn-comm">
          <catDesc>Kommentar (Notkers Exegese, ahd./lat. gemischt)</catDesc>
        </category>
        <category xml:id="fn-gloss">
          <catDesc>Interlinearglosse</catDesc>
        </category>
      </taxonomy>
      <!-- Quellen-Siglen -->
      <taxonomy xml:id="sources">
        <category xml:id="src-A"><catDesc>Augustinus, Enarrationes in Psalmos</catDesc></category>
        <category xml:id="src-C"><catDesc>Cassiodor, Expositio Psalmorum</catDesc></category>
        <category xml:id="src-R"><catDesc>Remigius</catDesc></category>
        <category xml:id="src-Br"><catDesc>Breviarium</catDesc></category>
        <category xml:id="src-RII" cert="low"><catDesc>RII – ungeklärt</catDesc></category>
        <category xml:id="src-N" cert="low"><catDesc>N – ungeklärt</catDesc></category>
      </taxonomy>
      <!-- Psalter-Zeugen -->
      <taxonomy xml:id="psalter_witnesses">
        <category xml:id="wit-G"><catDesc>Gallicanum</catDesc></category>
        <category xml:id="wit-R"><catDesc>Romanum</catDesc></category>
        <category xml:id="wit-H"><catDesc>Hebraicum, Bamberg Ms. 44</catDesc></category>
        <category xml:id="wit-A-psa"><catDesc>Augustinus-Psalter, Cod. 162</catDesc></category>
        <category xml:id="wit-C-psa"><catDesc>Cassiodor-Psalter, Cod. 200</catDesc></category>
      </taxonomy>
    </classDecl>
  </encodingDesc>
  <profileDesc>
    <langUsage>
      <language ident="goh">Althochdeutsch</language>
      <language ident="la">Latein</language>
      <language ident="de">Neuhochdeutsch</language>
    </langUsage>
  </profileDesc>
</teiHeader>
```

### 1.3 Versstruktur (Kernmodell)

Jeder Vers = `<div type="verse">`. Pro DOCX-Tabellenzeile ein `<ab>` (physische Struktur, 1:1-Abbildung). Innerhalb: `<seg>` mit `@type` und `@ana` für die funktionalen Schichten. Segmente, die über Zeilengrenzen hinausgehen, werden mit `@part` + `@next`/`@prev` verkettet (logische Struktur). Sprachwechsel innerhalb aller Schichten werden mit `<foreign>` kodiert.

**Designprinzip: Verlustfreie Kodierung.** Physische und logische Struktur koexistieren. Man kann immer aggregieren (Zeilen → Sinneinheiten, `<foreign>` ignorieren), aber nie disaggregieren. Diese Granularität ermöglicht die Skalierung auf 150 Psalmen und korpuslinguistische Auswertung.

```xml
<div type="verse" n="1">
  <!-- Zeile 1: Psalmzitat + Übersetzungsbeginn (zeilenübergreifend) -->
  <ab n="1">
    <seg type="psalm" ana="#fn-psalm" xml:lang="la"
         >QVARE FREMVERVNT GENTES.</seg>
    <seg type="translation" ana="#fn-transl" xml:lang="goh"
         xml:id="v1-tr1" part="I" next="#v1-tr1b"
         >Ziu grís<lb break="no"/></seg>
    <note type="sigle" place="margin">G, R</note>
  </ab>

  <!-- Zeile 2: Interlinearglosse -->
  <ab n="2" ana="#fn-gloss">
    <gloss xml:lang="goh" target="#gentes-v1">iúdon diêt</gloss>
    <note type="sigle" place="margin">C</note>
  </ab>

  <!-- Zeile 3: Übersetzung (Fortsetzung von Z.1) + neues Psalmzitat -->
  <ab n="3">
    <seg type="translation" ana="#fn-transl" xml:lang="goh"
         xml:id="v1-tr1b" part="F" prev="#v1-tr1"
         >cramoton an <foreign xml:lang="la">christum ebraicȩ
         gentes</foreign>?</seg>
    <seg type="psalm" ana="#fn-psalm" xml:lang="la"
         xml:id="v1-ps2" part="I" next="#v1-ps2b"
         >Et populi medi<lb break="no"/></seg>
    <note type="sigle" place="margin">C</note>
  </ab>

  <!-- Zeile 4: Psalmzitat-Ende + Kommentar + Übersetzung -->
  <ab n="4">
    <seg type="psalm" ana="#fn-psalm" xml:lang="la"
         xml:id="v1-ps2b" part="F" prev="#v1-ps2"
         >tati sunt inania.</seg>
    <seg type="commentary" ana="#fn-comm" xml:lang="goh"
         ><foreign xml:lang="la">idest frustura</foreign>?</seg>
    <seg type="translation" ana="#fn-transl" xml:lang="goh"
         xml:id="v1-tr2" part="I" next="#v1-tr2b"
         >Vnde ziu dâh<lb break="no"/></seg>
    <note type="sigle" place="margin">G, R, A</note>
  </ab>

  <!-- Zeile 5: Übersetzung-Ende + Kommentar -->
  <ab n="5">
    <seg type="translation" ana="#fn-transl" xml:lang="goh"
         xml:id="v1-tr2b" part="F" prev="#v1-tr2"
         >ton sîne liûte ardingun . ín ze irloschenne?</seg>
    <seg type="commentary" ana="#fn-comm" xml:lang="goh"
         xml:id="v1-co1" part="I" next="#v1-co1b"
         >Sie dâhton</seg>
    <note type="sigle" place="margin">A</note>
  </ab>

  <!-- Zeile 6: Kommentar-Ende + neues Psalmzitat -->
  <ab n="6">
    <seg type="commentary" ana="#fn-comm" xml:lang="goh"
         xml:id="v1-co1b" part="F" prev="#v1-co1"
         >des ín ubelo spuên solta.</seg>
    <seg type="psalm" ana="#fn-psalm" xml:lang="la"
         xml:id="v1-ps3" part="I" next="#v1-ps3b"
         ><foreign xml:lang="la">Astiterunt reges terrȩ . et
         principes</foreign></seg>
    <note type="sigle" place="margin">G, R</note>
  </ab>

  <!-- ... weitere Zeilen ... -->

  <!-- nhd. Übersetzung (Pfeifer) -->
  <note type="translation_nhd" resp="#pfeifer" xml:lang="de">
    <p>WARUM LÄRMTEN DIE VÖLKER. Warum wüteten an Christus die
    hebräischen Völker? Und (warum) sind die Völker vorbereitet
    sinnlos, das heißt vergeblich? Und warum dachten seine Leute
    grundlos, ihn auszulöschen? Sie gedachten dessen, (das)
    ihnen übel bekommen sollte.</p>
  </note>

  <!-- Quellenapparat -->
  <note type="sources">
    <cit ana="#src-C">
      <bibl>Cassiodor</bibl>
      <quote xml:lang="la">Quattuor membris psalmi huius species
      decora formata est. In primo loquitur propheta de Iudaeis
      propter passionem Christi. [...] Corripit enim populos
      propheta, cur fremuerint contra Dominum Saluatorem, cum
      <hi rend="bold">causas iracundiae</hi> non haberent.</quote>
      <note type="translation" resp="#pfeifer" xml:lang="de">
        In vier Teilen ist dieses Psalms schöne Gestalt geformt. [...]
      </note>
    </cit>
    <cit ana="#src-A">
      <bibl>Augustinus</bibl>
      <quote xml:lang="la">Pro eo dictum est utquid, ac si diceretur:
      <hi rend="bold">frustra</hi>; non enim impleuerunt quod
      uoluerunt, ut Christus exstingueretur.</quote>
      <note type="translation" resp="#pfeifer" xml:lang="de">
        Dafür wurde gesagt „was denn", als ob gesagt worden
        wäre „vergeblich" [...]
      </note>
    </cit>
    <!-- R, C, C -->
  </note>
</div>
```

### 1.4 Encoding-Entscheidungen

#### Textschichten: `<seg>` mit `@ana`

| DOCX-Farbe | `@type` | `@ana` | Default `@xml:lang` |
|---|---|---|---|
| `#806000` (olive) | `psalm` | `#fn-psalm` | `la` |
| `#00B050` (grün) | `translation` | `#fn-transl` | `goh` |
| schwarz (default) | `commentary` | `#fn-comm` | `goh` |

**Warum `<seg>` statt `<quote>` für Psalmzitate?** Notker paraphrasiert gelegentlich. `<seg type="psalm">` ist ehrlicher. Für wörtliche Vulgata-Zitate kann zusätzlich `<cit>` gesetzt werden.

**Warum `@ana`?** Verweist auf die deklarierte Taxonomie im Header. Ermöglicht maschinelles Auslesen der Schicht-Zugehörigkeit.

#### Sprachwechsel: `<foreign>` in allen Schichten (entschieden)

**Entscheidung (23.03.):** Sprachwechsel werden in **allen drei Schichten** mit `<foreign xml:lang="...">` kodiert – verlustfrei. Die Information ist in der Probeseite vorhanden (Handschrift: rot/schwarz = Sprache) und muss bewahrt werden, weil das Gesamtprojekt (150 Psalmen) korpuslinguistische Auswertung braucht (z.B. Latein-Anteil pro Schicht, Verteilung lat. Einsprengsel).

**Warum nicht nur die funktionale Kodierung?** Man kann `<foreign>` immer ignorieren (CSS/XSLT überspringt es), aber nachträglich hinzufügen erfordert Neuanalyse aller 150 Psalmen. Granular kodieren ist strikt flexibler.

```xml
<!-- Grüne Übersetzung mit lat. Einsprengseln -->
<seg type="translation" ana="#fn-transl" xml:lang="goh">
  cramoton an <foreign xml:lang="la">christum ebraicȩ gentes</foreign>?
</seg>

<!-- Schwarzer Kommentar: lat. Fachterminus -->
<seg type="commentary" ana="#fn-comm" xml:lang="goh">
  <foreign xml:lang="la">idest frustura</foreign>?
</seg>

<!-- Kommentar, der in ein neues Psalmzitat übergeht -->
<seg type="commentary" ana="#fn-comm" xml:lang="goh">
  des ín ubelo spuên solta.
</seg>
<seg type="psalm" ana="#fn-psalm" xml:lang="la">
  Astiterunt reges terrȩ . et principes
</seg>
```

**Parser-Implikation:**
- **Olive/Grün:** Sprache durch Farbe determiniert. `<foreign>` innerhalb grüner Segmente erfordert Wörterbuch-Lookup oder LLM, aber nur ~524 grüne Runs.
- **Schwarz (Kommentar):** LLM unverzichtbar, weil kein Farbsignal. Aber ahd./lat. morphologisch sehr verschieden → >95% Genauigkeit realistisch.
- **Ablauf:** Regelbasierter Pass (Farbe → `<seg>`) → LLM-Batch für `<foreign>`-Annotation → manuelles Review.

#### Zeilenübergreifende Segmente: `@part` + `@next`/`@prev` (entschieden)

**Entscheidung (23.03.):** Physische Struktur (Zeilen) und logische Struktur (Sinneinheiten) werden **parallel** kodiert. `<ab>` = DOCX-Tabellenzeile (1:1, verlustfrei). `@part` + `@next`/`@prev` verkettet Segmente, die über Zeilengrenzen gehen.

| Attribut | Wert | Bedeutung |
|---|---|---|
| `@part="I"` | Initial | Segment beginnt hier, geht in nächster Zeile weiter |
| `@part="M"` | Medial | Segment-Fortsetzung, geht noch weiter |
| `@part="F"` | Final | Letztes Teilsegment |
| `@next` | `#xml:id` | Verweis auf nächstes Teilsegment |
| `@prev` | `#xml:id` | Verweis auf vorheriges Teilsegment |

**Warum beides?**
- Die UI kann wahlweise zeilenbasiert (Faksimile-Synchronisation) oder sinneinheitenbasiert (Leseansicht) rendern
- Für 150 Psalmen kann ein späterer Pass die Ketten automatisch auflösen
- `<ab>` bewahrt die Verbindung zur Handschriftenzeile (Alignment mit IIIF)
- `@part`-Ketten ermöglichen semantische Suche über Zeilengrenzen

**Wo setzt der Parser `@part`?**
- Wenn ein `<seg>` am Zeilenende mit `<lb break="no"/>` endet UND die nächste Zeile mit einem `<seg>` gleichen `@type` und `@ana` beginnt → Verkettung
- Wenn ein Farbwechsel (olive → grün → schwarz) mitten in einer Zeile stattfindet → kein `@part`, sondern neues `<seg>` in derselben `<ab>`

#### Interlinearglossen: `<gloss>`

14 Glossen in Psalm 2. Als eigene `<ab>` mit `@ana="#fn-gloss"`:

```xml
<ab ana="#fn-gloss">
  <gloss xml:lang="goh" target="#term-gentes">iúdon diêt</gloss>
</ab>
```

nhd. Übersetzung der Glosse steht in Pfeifers Übersetzungsspalte (wird über `<note type="translation_nhd">` des Verses abgebildet).

#### Quellenapparat: `<cit>`

**Warum `<cit>` statt `<app>`?** Die Quellen sind Notkers Vorlagen, keine textkritischen Varianten. `<cit>` (Zitat mit Quellenangabe) passt besser. `<app>` wird im Psaltervergleich verwendet (dort liegen echte Varianten vor).

Struktur pro Quelleneintrag:
- `@ana` → `#src-A`, `#src-C` etc.
- `<bibl>` → Kurzreferenz
- `<quote xml:lang="la">` → Lateinischer Originaltext, `<hi rend="bold">` für Hervorhebungen
- `<note type="translation" resp="#pfeifer" xml:lang="de">` → Dt. Übersetzung

#### Ungeklärte Siglen

Mit `@cert="low"` in der Taxonomie. Im Text mit `<note type="editorial">`:

```xml
<cit ana="#src-RII">
  <note type="editorial">Sigle RII ungeklärt. Vermutlich zweite Remigius-Quelle.</note>
  <bibl>RII</bibl>
  <quote xml:lang="la">Sion autem arx est altissima in Ierusalem...</quote>
</cit>
```

#### Siglen am Zeilenrand

```xml
<note type="sigle" place="margin" cert="low">G, R</note>
```

`@cert="low"`, weil die Semantik der Haupttext-Siglen (Psalmtext-Zuordnung vs. Quellenmarkierung) ungeklärt ist.

#### Zeilenumbrüche

```xml
<seg type="translation" ana="#fn-transl" xml:lang="goh">Ziu grís<lb break="no"/></seg>
```

`<lb break="no"/>` bewahrt die Zeilenstruktur der Probeseite und markiert Silbentrennung. Zusammenführung erst bei der JSON-Ableitung für die UI.

### 1.5 Synoptischer Psaltervergleich

Fünf Psalmtext-Zeugen mit `<app>` / `<rdg>`:

```xml
<div type="psalm_comparison">
  <listWit>
    <witness xml:id="wit-G-full">Gallicanum</witness>
    <witness xml:id="wit-R-full">Romanum</witness>
    <witness xml:id="wit-H-full">Hebraicum, Bamberg Ms. 44</witness>
    <witness xml:id="wit-A-full">Augustinus-Psalter, Cod. 162</witness>
    <witness xml:id="wit-C-full">Cassiodor-Psalter, Cod. 200</witness>
  </listWit>
  <ab n="1">
    <app>
      <rdg wit="#wit-G-full">Quare fremuerunt gentes. et populi meditati sunt inania.</rdg>
      <rdg wit="#wit-H-full">Quare turbabuntur gentes. et tribus meditabuntur inania.</rdg>
      <!-- etc. -->
    </app>
  </ab>
</div>
```

Im `<back>`, nicht `<body>` (kein Teil von Notkers Text).

### 1.6 Wiener Notker

```xml
<div type="parallel_tradition" source="#wiener_notker">
  <head>Wiener Notker (ÖNB Cod. 2681)</head>
  <ab n="1">Quare fremuerunt gentes, et populi meditati sunt inania? [...]
  Unde zuuiu dahton sine liute aruungen in zerlesgenne?</ab>
</div>
```

Keine Feincodierung (Schichten, Sprachtrennung) im Prototyp. Rohtext.

---

## 2. Python-Pipeline DOCX → TEI-XML

### 2.1 Architektur

```
Probeseite_Notker.docx
        │
        ▼
┌─────────────────────────┐
│  parse_probeseite.py     │  DOCX → Python-Dicts (Zwischenformat)
│  - Tabellen iterieren    │  Regelbasiert
│  - Merged Cells dedup    │
│  - Run-Farben extrahieren│
│  - Zeilentypen erkennen  │
└────────────┬────────────┘
             │  List[VerseData]
             ▼
┌─────────────────────────┐
│  classify_layers.py      │  Schichten zuweisen + anreichern
│  - Farbe → Funktion      │  Regelbasiert + Heuristik + LLM
│  - Glossen erkennen      │
│  - Sprachwechsel taggen   │
└────────────┬────────────┘
             │  List[VerseData] (enriched)
             ▼
┌─────────────────────────┐
│  build_tei.py            │  TEI-XML generieren
│  - lxml.etree            │  Regelbasiert
│  - Schema-Validierung    │
└────────────┬────────────┘
             │  psalm2.xml
             ▼
┌─────────────────────────┐
│  tei_to_json.py          │  TEI → JSON (für Web-UI)
│  - lxml-Traversal        │  Regelbasiert
│  - Flaches JSON          │
└────────────┬────────────┘
             │  psalm2.json
```

### 2.2 Schritt 1: DOCX parsen

#### Tabellenerkennung

13 Tabellen in 3 funktionalen Gruppen (aus [[Probeseite Analyse]]):

| Gruppe | Tables | Erkennung | Inhalt |
|---|---|---|---|
| Haupttext + Quellen | 0, 2, 3, 6 (T7 im DOCX) | Cols 0–2 identisch, ≥ 4 Spalten | Notkers Text + eingebetteter Apparat |
| Nur Haupttext | 1, 4, 7, 9 (T2, T5, T8, T10) | Cols 0–2 identisch, 3 Spalten | Notkers Text ohne Apparat |
| Eigenständig | 5, 8, 10, 11, 12 (T6, T9, T11, T12, T13) | Verschiedene Strukturen | Quellen, Psaltervergleich, Wiener Notker |

#### DOCX-Strukturen → Zwischenformat

| DOCX-Element | Erkennung | Zwischenformat |
|---|---|---|
| Paragraph zwischen Tabellen | `w:p`, Text ≈ `\d+,\d+` | Vers-Zuordnung (steuert Gruppierung) |
| Haupttext-Zeile | Cols 0–2 identisch (merged) | `Row(type='text', segments=[...], nhd, sigles)` |
| Quellenapparat-Zeile | Col 0 = einzelne Sigle (A, C, R, Br, RII, N) | `Row(type='source', sigle, latin, german)` |
| Interlinearglosse | Kurze Zeile (≤ 5 Wörter), schwarz, keine Sigle | `Row(type='gloss', text, nhd)` |
| Psaltervergleich | T10 R4–6 + T11: Siglen-Header + Volltext | `PsalterWitness(sigle, text)` |
| Wiener Notker | T12: Header „Wiener Notker" | `WienerNotker(text)` |

#### Merged-Cell-Deduplizierung

```python
def deduplicate_merged(row):
    """Cols 0-2 identisch → nur Col 0 verwenden."""
    texts = [cell.text.strip() for cell in row.cells[:min(3, len(row.cells))]]
    if len(set(texts)) == 1:
        return row.cells[0]  # merged → eine Zelle reicht
    return None  # nicht gemerged, Row-Typ anders
```

#### Run-Level-Farbextraktion

```python
from docx.oxml.ns import qn

COLOR_MAP = {
    '806000': 'psalm',      # olive
    '00B050': 'translation', # grün
    None: 'commentary'       # schwarz (default)
}

def get_run_color(run):
    rpr = run._element.find(qn('w:rPr'))
    if rpr is not None:
        color = rpr.find(qn('w:color'))
        if color is not None:
            return color.get(qn('w:val'))
    return None
```

Zusammenhängende Runs gleicher Farbe → ein Segment.

#### Vers-Zuordnung

Paragraphen zwischen Tabellen:

| Text (bereinigt) | Verse | Nachfolgende Tables |
|---|---|---|
| `2,1-2` | 1–2 | T0, T1 |
| `2,3-2,5` | 3–5 | T2, T3 |
| `2,6` | 6 | T4, T5 |
| `2,7` | 7 | T6 |
| `2,8-9` | 8–9 | T7, T8 |
| `2,10-11` | 10–11 | T9, T10 (Zeilen 0–3) |
| `2,12` | 12 | T10 (Zeilen 4–6), T11, T12 |

**Achtung:** Pro Versgruppe folgen oft mehrere Tabellen. Parser sammelt alle Tables bis zur nächsten Vers-Überschrift.

### 2.3 Schritt 2: Schichtenklassifikation

#### Regelbasiert (sicher)

| Regel | Trigger | Ergebnis |
|---|---|---|
| Farbe `#806000` | Run-Farbe | `type='psalm'`, `lang='la'` |
| Farbe `#00B050` | Run-Farbe | `type='translation'`, `lang='goh'` |
| Schwarz + Col 0 = Sigle | Einzelwort-Sigle in Col 0 | `type='source'` |
| Kursiv in nhd-Spalte | Run-Formatting | `type='nhd_translation'` |
| Bold in Quellentext | Run bold | `<hi rend="bold">` |

#### Heuristiken (mittlere Sicherheit)

| Heuristik | Kriterien | Fehlerrisiko |
|---|---|---|
| Glossen-Erkennung | Zeile ≤ 5 Wörter, nur schwarze Runs, keine Sigle, nhd-Spalte hat kurze Übersetzung | Mittel: kurze Kommentarzeilen als false positive |
| Versgrenze in Tabelle | Neues olive-Psalmzitat nach schwarzem Kommentar | Niedrig: Farbwechsel eindeutig |

#### LLM-gestützt (nötig)

| Aufgabe | Grund | Erwartete Genauigkeit |
|---|---|---|
| **Sprachwechsel im Kommentar** (schwarz) | Mischt ahd./lat. frei. Kein Farbsignal. → `<foreign xml:lang="la">` | > 95% (Sprachen morphologisch sehr verschieden) |
| **Sprachwechsel in Übersetzung** (grün) | Lat. Einsprengsel in ahd. Text. → `<foreign xml:lang="la">` | > 95% (Kontext + Wörterbuch) |
| **Glossen-Validierung** | Heuristik-Kandidaten überprüfen: Glosse oder kurzer Kommentar? | Hoch (wenige Beispiele im Prompt reichen) |
| **Silbentrennung auflösen** | `grís-` + `cramoton` = `gríscramoton`. Braucht ahd. Morphologie. | Hoch, manuell überprüfbar |
| **Segment-Verkettung** | Erkennung, ob ein Segment über die Zeile hinausgeht (→ `@part`) | Hoch (Farb-Kontinuität + Silbentrennung als Signal) |
| **Satzgrenzen** | Ahd. Interpunktion unregelmäßig | Mittel |

**Ablauf:** Regelbasierter Pass (Farbe, Merged Cells, Siglen) → LLM-Batch (Claude API) für `<foreign>`-Annotation und `@part`-Verkettung → manuelles Review.

### 2.4 Schritt 3: TEI generieren (`build_tei.py`)

`lxml.etree` für XML-Bau. Kein Template-System (Struktur zu variabel).

Kernfunktionen:

```python
XML_NS = 'http://www.w3.org/XML/1998/namespace'

def build_verse(verse_data, parent):
    div = etree.SubElement(parent, 'div', type='verse', n=str(verse_data.number))

    for line in verse_data.lines:
        ab = etree.SubElement(div, 'ab', n=str(line.number))

        for seg_data in line.segments:
            seg = etree.SubElement(ab, 'seg',
                type=seg_data.function,
                ana=f'#fn-{seg_data.function_key}')
            seg.set(f'{{{XML_NS}}}lang', seg_data.lang)

            # Zeilenübergreifende Verkettung
            if seg_data.part:
                seg.set(f'{{{XML_NS}}}id', seg_data.xml_id)
                seg.set('part', seg_data.part)  # I, M, or F
                if seg_data.next_id:
                    seg.set('next', f'#{seg_data.next_id}')
                if seg_data.prev_id:
                    seg.set('prev', f'#{seg_data.prev_id}')

            # Sprachwechsel: <foreign> innerhalb des Segments
            build_text_with_foreign(seg, seg_data)

        if line.sigles:
            note = etree.SubElement(ab, 'note', type='sigle', place='margin')
            note.text = line.sigles

    # nhd. Übersetzung, Quellenapparat analog

def build_text_with_foreign(parent_el, seg_data):
    """Baut Text mit <foreign>-Elementen für Sprachwechsel."""
    if not seg_data.foreign_spans:
        parent_el.text = seg_data.text
        return
    # Iteriert über Text und foreign-Spans, baut Mixed Content
    pos = 0
    last_el = None
    for span in seg_data.foreign_spans:
        # Text vor dem foreign-Span
        pre_text = seg_data.text[pos:span.start]
        if last_el is None:
            parent_el.text = (parent_el.text or '') + pre_text
        else:
            last_el.tail = (last_el.tail or '') + pre_text
        # <foreign> Element
        foreign = etree.SubElement(parent_el, 'foreign')
        foreign.set(f'{{{XML_NS}}}lang', span.lang)
        foreign.text = seg_data.text[span.start:span.end]
        last_el = foreign
        pos = span.end
    # Restlicher Text nach dem letzten foreign-Span
    if pos < len(seg_data.text):
        if last_el is not None:
            last_el.tail = (last_el.tail or '') + seg_data.text[pos:]
        else:
            parent_el.text = (parent_el.text or '') + seg_data.text[pos:]
```

Validierung gegen TEI-All RelaxNG nach Generierung.

### 2.5 Schritt 4: TEI → JSON

Traversiert TEI-XML, erzeugt das JSON-Schema aus [[Technik]]. Dieses Script ist der **Interface-Vertrag** mit dem parallelen UI-Agenten.

| TEI-Element | JSON-Feld |
|---|---|
| `<div type="verse" n="X">` | `verses[].number` |
| `<seg type="psalm">` | `verses[].sections[].type: 'psalm_citation'` |
| `<seg type="translation">` | `verses[].sections[].type: 'translation'` |
| `<seg type="commentary">` | `verses[].sections[].type: 'commentary'` |
| `<ab ana="#fn-gloss">` / `<gloss>` | `verses[].glosses[]` |
| `<cit ana="#src-X">` | `verses[].sources[]` |
| `<note type="translation_nhd">` | `verses[].translation_nhd` |
| `<app>/<rdg>` | `psalm_text_comparison.witnesses[]` |

---

## 3. Vollständiges Mapping DOCX → TEI

| DOCX-Struktur | Erkennung | TEI-Element | Methode |
|---|---|---|---|
| Vers-Paragraph | Regex `\d+,\d+` zw. Tabellen | Vers-Zuordnung | Regel |
| Olive Runs (`#806000`) | Run-Farbe | `<seg type="psalm" xml:lang="la">` | Regel |
| Grüne Runs (`#00B050`) | Run-Farbe | `<seg type="translation" xml:lang="goh">` + `<foreign>` für lat. Wörter | Regel + LLM |
| Schwarze Runs (default) | Keine Farbe | `<seg type="commentary">` + `<foreign>` für lat. Wörter | Regel + LLM |
| Kursiv in nhd-Spalte | Formatting | `<note type="translation_nhd">` | Regel |
| Siglen-Spalte | Letzte Spalte, kurzer Text | `<note type="sigle" place="margin">` | Regel |
| Quellenapparat-Zeile | Col 0 = Sigle allein | `<cit>` mit `<quote>` + `<note>` | Regel |
| Bold in Quellen | Run bold | `<hi rend="bold">` | Regel |
| Glossen-Zeile | Kurz, schwarz, keine Sigle | `<ab ana="#fn-gloss"><gloss>` | Heuristik + LLM |
| Psaltervergleich | T10 R5–6, T11 | `<app><rdg wit="#...">` | Regel (Struktur) |
| Wiener Notker (T12) | Header-Text | `<div type="parallel_tradition">` | Regel |
| Zeilentrennung `-` | Run endet `-` am Zeilenende | `<lb break="no"/>` | Regel* |
| Zeilenübergreifendes Segment | Gleicher `@type`/`@ana` setzt sich in nächster Zeile fort | `@part="I"/"M"/"F"` + `@next`/`@prev` | Regel + LLM |

*Achtung: ahd. Komposita mit Bindestrich (z.B. `lánt-chuninga`) dürfen nicht als Silbentrennung behandelt werden. Heuristik: Trennung nur am Zeilenende, wenn nächste Zeile mit Kleinbuchstabe beginnt.

### Kodierungsebenen-Zusammenfassung

| Ebene | TEI-Element | Bewahrt | Erweiterbar durch |
|---|---|---|---|
| Physische Zeile | `<ab>` | DOCX-Tabellenstruktur 1:1 | Faksimile-Verlinkung (Zeile → Handschriftenzeile via IIIF) |
| Funktionale Schicht | `<seg @type @ana>` | Farbcodierung der Probeseite | Weitere Schichttypen in späteren Psalmen |
| Logische Einheit | `@part` + `@next/@prev` | Zusammengehörigkeit über Zeilengrenzen | Satzextraktion, semantische Suche |
| Sprachwechsel | `<foreign xml:lang>` | Sprachgrenzen auf Wortebene | Lemmatisierung, POS-Tagging, Sprachstatistik |
| Silbentrennung | `<lb break="no"/>` | Trennstellen der Probeseite | Alignment mit Handschrift/Edition |

---

## 4. Offene technische Entscheidungen

### 4.1 Abhängig vom parallelen UI-Agenten

| Entscheidung | Betrifft | Interface-Vertrag |
|---|---|---|
| JSON-Schema | `tei_to_json.py` | UI-Agent definiert erwartetes JSON. Aktueller Stand in [[Technik]]. |
| Toggle-Granularität | TEI→JSON-Tiefe | Vers-Level oder Run-Level? Bestimmt JSON-Struktur. |
| Glossen-Darstellung | JSON-Struktur | Inline vs. Tooltip → Glossen als eigene Objekte oder Token-Annotationen. |
| Farbmapping | TEI-Taxonomie-IDs | `#fn-psalm`, `#fn-transl`, `#fn-comm` als Vertrag. |

### 4.2 Abhängig von Klärung mit Philipp

| Frage | TEI-Auswirkung | Workaround |
|---|---|---|
| G, R in Haupttext-Siglen | `<note type="textual_witness">` vs. `<note type="source_ref">` | `<note type="sigle" cert="low">` |
| H im Haupttext | Psalter oder Kommentarquelle? | `<note type="sigle" cert="low">` |
| RII, N | `<bibl>`-Inhalt | `<note type="editorial">ungeklärt</note>` |
| Scope Psaltervergleich | Im TEI immer modellieren, im JSON weglassen? | Ja, TEI ist vollständig |
| Bibelstellen-Querverweise | `<ref type="biblical">`? | Nicht modellieren (Daten fehlen) |

### 4.3 Technisch offen

| Entscheidung | Empfehlung | Begründung |
|---|---|---|
| Silbentrennung | `<lb break="no"/>` bewahren, im JSON auflösen | Zeilenstruktur philologisch relevant |
| Akzente | Bewahren (Unicode) | Teil der Edition |
| Token-Boundaries | Fließtext, nicht tokenbasiert | Tokenisierung = ANNIS-Aufgabe |
| TEI → JSON | Python (lxml), nicht XSLT | Flexibler für Prototyp |
| IIIF-Seiten | Seite 11 bestätigt, Ende unklar | `<surface>`-Elemente vorbereiten |

---

## 5. Getroffene Modellierungsentscheidungen (23.03.)

Die folgenden Fragen wurden mit der Orchestration geklärt. Leitprinzip: **Verlustfreie Kodierung** – Information immer bewahren, weil man aggregieren, aber nie disaggregieren kann.

### 5.1 Segmentierung: Beides (entschieden)

Physische Struktur (`<ab>` = DOCX-Zeile) UND logische Struktur (`@part` + `@next`/`@prev` für zeilenübergreifende Segmente) koexistieren. Keine Information geht verloren. Die UI entscheidet, welche Ebene sie rendert.

### 5.2 Sprachmischung: `<foreign>` in allen Schichten (entschieden)

Sprachwechsel werden überall mit `<foreign xml:lang="...">` kodiert – in grünen Übersetzungssegmenten genauso wie im schwarzen Kommentar. Begründung:
- Nachträglich hinzufügen erfordert Neuanalyse aller Psalmen
- Ermöglicht korpuslinguistische Auswertung (Latein-Anteil, Einsprengsel-Verteilung)
- `<foreign>` kann von der UI/XSLT trivial ignoriert werden
- Die Handschrift unterscheidet die Sprachen explizit (rot/schwarz) – wir überführen diese Information in Struktur

---

## Verknüpfungen

- [[Probeseite Analyse]] — Empirische Grundlage für DOCX-Strukturen
- [[Domänenwissen]] — Textschichten, Siglen, Referenzsysteme
- [[Anforderungen]] — Features, die das TEI-Modell bedienen muss
- [[Design]] — UI-Konzept und Toggle-System
- [[Technik]] — JSON-Schema und Web-Stack
- [[Research Plan]] — Phasenplanung
- [[Journal]] — Projektchronologie
