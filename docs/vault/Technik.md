---
type: technical
created: 2026-02-27
updated: 2026-04-16
tags: [notker, technical, tei, pipeline]
---

# Technik: Notker Psalmenkommentar Prototyp

Technische Referenz für Pipeline, TEI-Modell, JSON-Schema und Web-Stack. Für editorische Kodierungsregeln siehe [[Editionsrichtlinien]].

## 1. Pipeline

**TEI-XML ist die kanonische Datenquelle.** JSON wird daraus für die Web-UI abgeleitet.

```
Probeseite_Notker.docx
  → parse_probeseite.py     DOCX → Python (Dataclasses)        Regelbasiert
  → classify_layers.py      Sprachwechsel, @part-Verkettung    Regel + Heuristik
  → build_tei.py            → data/tei/psalm2.xml              lxml, TEI-All RNG
       Schritt 1: TEI seriell aus PsalmData
       Schritt 2: apply_corrections (PFEIFER_CORRECTIONS)      Pipeline-Normalisierung
       Schritt 3: normalize_whitespace_in_text_nodes           DOCX-Artefakte
       Schritt 4: chain_cross_verse_hyphens                    @part="I"/"F" + @next/@prev
  → tei_to_json.py          → data/processed/psalm2.json
       collect_segments inkl. line_n + disambiguate_sigles
       merge_cross_verse_hyphens (textliche Zusammenführung für UI)
  → docs/index.html         Single-File-Webanwendung mit Slot-System
```

Ehemaliger Errata-Layer (`apply_errata.py` + `errata.yaml` + `tests/test_errata.py`)
in Iteration 2 entfernt — die 21 Pfeifer-Korrekturen leben jetzt als
`PFEIFER_CORRECTIONS: list[tuple[str, str]]` in `parse_probeseite.py` und werden
über `apply_corrections()` einmal auf den fertigen TEI-String angewendet.

### 1.1 DOCX-Parsing (`parse_probeseite.py`)

13 Tabellen in 3 Gruppen (Details in [[Probeseite Analyse]]):

| Gruppe | Tables | Erkennung |
|---|---|---|
| Haupttext + Quellen | T1, T3, T4, T7, T11 | Cols 0–2 identisch, ≥4 Spalten |
| Nur Haupttext | T2, T5, T8, T10 | Cols 0–2 identisch, 3 Spalten |
| Eigenständig | T6, T9, T12, T13 | Verschiedene Strukturen |

**Farbextraktion** auf Run-Ebene (nicht Paragraph):
```python
COLOR_MAP = {
    '806000': 'psalm',       # olive → Psalmzitation
    '00B050': 'translation',  # grün → Übersetzung
    None: 'commentary',       # schwarz → Kommentar
}
```

**Vers-Zuordnung** aus Paragraphen zwischen Tabellen (Regex `2,\d+`).

### 1.2 Schichtenklassifikation (`classify_layers.py`)

| Methode | Aufgabe | Genauigkeit |
|---|---|---|
| Regelbasiert | Farbe → Funktion, Siglen, Bold | Sicher |
| Heuristik | Glossen-Erkennung (≤5 Wörter, schwarz, kurze nhd) | Mittel |
| Regelbasiert | Sprachwechsel in Übersetzung/Kommentar (Wörterbuch + Morphologie) | >95% |
| Regelbasiert | Segment-Verkettung (`@part` bei Farb-Kontinuität + Silbentrennung) | Sicher |

### 1.3 TEI-Generierung (`build_tei.py`)

`lxml.etree`, Validierung gegen TEI-All RelaxNG nach Generierung.

### 1.4 TEI→JSON (`tei_to_json.py`)

Traversiert TEI, aggregiert `<ab>`-Zeilen zu Vers-Sections, löst `@part`-Ketten und Silbentrennungen auf. Interface-Vertrag mit der UI.

**Besondere Features:**
- **Siglen-Parsing:** Klammernotation `G [A, C]` wird korrekt als separate Siglen geparst (Regex: `[A-Z][a-z]*(?:II)?`)
- **R-Disambiguierung** (`disambiguate_sigles()`): R ist ambig (Romanum-Psalter vs. Remigius-Patristik). Heuristik anhand Section-Type: R in `psalm_citation` → `sigles_psalter`, sonst → `sigles_sources`. G/H sind eindeutig Psalter, A/C/Br/RII/N eindeutig Patristik.
- **Notker-Zeilennummer**: jede Section trägt `line_n` aus dem `<ab n="X">` (Iteration 2 / US-9.2) — Frontend setzt `data-line` Attribut.
- **nhd. line-faithful**: `collect_nhd_lines()` liest die `<l>`-Elemente unter `<lg type="line-faithful">` als `translation_nhd_lines: [str]`. Frontend rendert Edition zeilengetreu, Pool-View als Fließtext.
- **Bold-Preservation:** `<hi rend="bold">` in `<quote>`-Elementen wird als `<b>`-Tags im JSON erhalten (`rich_text_content()`)
- **Gloss-Interleaving:** Glossen (`<ab ana="#fn-gloss">`) werden als `type: "gloss"` Sections an ihrer korrekten Position im Textfluss eingefügt, nicht separat am Versende
- **Hyphen-Merge über Glossen hinweg:** Silbentrennungen werden auch dann zusammengeführt, wenn eine Glosse dazwischen liegt (z.B. "grís-" [Glosse] "cramoton" → "gríscramoton")
- **Cross-Verse-Hyphen-Merge** (`merge_cross_verse_hyphens()`): textliche Zusammenführung im JSON parallel zur semantischen `@part`-Verkettung im TEI (V1-2 „han-" + V3-5 „gta" → „hangta")

### 1.5 Validierung und Tests

- `validate_tei.py`: RelaxNG-Validierung + Strukturstatistik (auch in test_pipeline integriert)
- `test_pipeline.py`: 29 Tests (DOCX↔TEI↔JSON), Ground-Truth-Vergleich, Pfeifer-Korrekturen
- `tests/test_gloss_classification.py`: 6 Unit-Tests für Glossen-Heuristik

## 2. TEI-XML-Modell

### 2.1 Dokumentstruktur

```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="goh">
  <teiHeader>
    <!-- Taxonomien: #fn-psalm, #fn-transl, #fn-comm, #fn-gloss -->
    <!-- Quellen: #src-A, #src-C, #src-R, #src-Br, #src-RII, #src-N -->
    <!-- Psalter-Zeugen: #wit-G, #wit-R, #wit-H, #wit-A-psa, #wit-C-psa -->
    <!-- variantEncoding method="parallel-segmentation" -->
  </teiHeader>
  <facsimile><!-- IIIF-Surfaces --></facsimile>
  <text>
    <front><div type="introduction"/></front>
    <body>
      <div type="psalm" n="2">
        <!-- 7 × <div type="verse"> mit <ab>-Zeilen -->
      </div>
    </body>
    <back>
      <div type="psalm_comparison"><!-- 5 Zeugen als <app>/<rdg> --></div>
      <div type="parallel_tradition"><!-- Wiener Notker --></div>
    </back>
  </text>
</TEI>
```

### 2.2 Kernmodell: Vers → Zeile → Segment

**Designprinzip: Verlustfreie Kodierung.** Physische und logische Struktur koexistieren — man kann aggregieren, aber nie disaggregieren.

```xml
<div type="verse" n="1-2">
  <ab n="2">
    <seg type="psalm" ana="#fn-psalm" xml:lang="la">QVARE FREMVERVNT GENTES.</seg>
    <seg type="translation" ana="#fn-transl" xml:lang="goh">Ziu grís-<lb break="no"/></seg>
    <note type="sigle" place="margin">G, R</note>
  </ab>
  <ab ana="#fn-gloss" n="3">
    <gloss xml:lang="goh">iúdon diêt</gloss>
    <note type="translation_gloss" xml:lang="de">Juden Volk</note>
  </ab>
  <ab n="4">
    <seg type="translation" ana="#fn-transl" xml:lang="goh"
         >cramoton an <foreign xml:lang="la">christum</foreign> ebraicȩ gentes?</seg>
    <seg type="psalm" ana="#fn-psalm" xml:lang="la" part="I">Et populi medi-<lb break="no"/></seg>
  </ab>
  <ab n="5">
    <seg type="psalm" ana="#fn-psalm" xml:lang="la" part="F">tati sunt inania.</seg>
    <seg type="commentary" ana="#fn-comm" xml:lang="goh">
      <foreign xml:lang="la">idest</foreign> frustura?</seg>
  </ab>
  <!-- nhd. Übersetzung, Quellenapparat -->
</div>
```

### 2.3 Vollständiges DOCX→TEI Mapping

| DOCX-Struktur | Erkennung | TEI-Element | Methode |
|---|---|---|---|
| Vers-Paragraph | Regex `\d+,\d+` | Vers-Zuordnung | Regel |
| Olive Runs (`#806000`) | Run-Farbe | `<seg type="psalm" xml:lang="la">` | Regel |
| Grüne Runs (`#00B050`) | Run-Farbe | `<seg type="translation" xml:lang="goh">` | Regel |
| Schwarze Runs | Default | `<seg type="commentary">` + `<foreign>` | Regel + Heuristik |
| Kursiv in nhd-Spalte | Formatting | `<note type="translation_nhd">` | Regel |
| Siglen-Spalte | Letzte Spalte | `<note type="sigle" place="margin">` | Regel |
| Quellenapparat | Col 0 = Sigle | `<cit>` + `<quote>` + `<note>` | Regel |
| Bold in Quellen | Run bold | `<hi rend="bold">` | Regel |
| Glossen-Zeile | Kurz, schwarz, keine Sigle | `<ab ana="#fn-gloss"><gloss>` | Heuristik |
| Psaltervergleich | T11, T12 | `<app><rdg wit="#...">` | Regel |
| Wiener Notker | T13 | `<div type="parallel_tradition">` | Regel |
| Silbentrennung | `-` am Zeilenende | `<lb break="no"/>` | Regel |
| Zeilenübergreifend | Gleicher Typ fortsetzend | `@part="I"/"M"/"F"` | Regel |

### 2.4 Kodierungsebenen

| Ebene | TEI-Element | Bewahrt | Erweiterbar durch |
|---|---|---|---|
| Physische Zeile | `<ab>` | DOCX-Tabellenstruktur 1:1 | Faksimile-Verlinkung |
| Funktionale Schicht | `<seg @type @ana>` | Farbcodierung Probeseite | Weitere Schichttypen |
| Logische Einheit | `@part` | Zusammengehörigkeit über Zeilengrenzen | Satzextraktion |
| Sprachwechsel | `<foreign xml:lang>` | Sprachgrenzen auf Wortebene | Lemmatisierung, POS |
| Silbentrennung | `<lb break="no"/>` | Trennstellen der Probeseite | Alignment mit HS |

### 2.5 Encoding-Entscheidungen

**`<seg>` statt `<quote>` für Psalmzitate:** Notker paraphrasiert gelegentlich. `<seg type="psalm">` ist ehrlicher.

**`<cit>` statt `<app>` für Quellen:** Die Quellen sind Notkers Vorlagen, keine textkritischen Varianten. `<app>` nur im Psaltervergleich.

**`<foreign>` in allen Schichten:** Verlustfrei — nachträglich hinzufügen erfordert Neuanalyse aller 150 Psalmen. `<foreign>` kann von UI/XSLT trivial ignoriert werden.

**Nur `@part`, nicht `@next`/`@prev`** für Verkettungen *innerhalb* eines Verses: TEI P5 dokumentiert beide als äquivalent. `@part` ist kompakter, Reihenfolge implizit.

**`@part="I"`/`@part="F"` plus `@xml:id`/`@next`/`@prev` für Cross-Verse-Verkettungen:** Wenn ein Wort über die Vers-Grenze geteilt ist (z.B. „han-" / „gta"), reicht `@part` allein nicht (Reihenfolge nicht implizit über Vers-Grenze). Daher zusätzlich `@xml:id="seg-cross-N-i"`/`-f"` mit `@next`/`@prev`-Verweisen. Implementiert in `chain_cross_verse_hyphens()` (`build_tei.py`).

**`<lg type="line-faithful">` für nhd. Übersetzung** (Iteration 2 / US-9): Pfeifer hat zeilengetreu übersetzt. Pro Zeile ein `<l>` unter `<note type="translation_nhd"><lg type="line-faithful">`. Daneben weiterhin `<p>` mit Fließtext für Lese-Ansicht.

**Ungeklärte Siglen:** RII und N mit `@cert="low"` in Taxonomie + `<note type="editorial">ungeklärt</note>`.

## 3. JSON-Schema (Iteration 2)

```json
{
  "psalm": 2,
  "metadata": { "title", "manuscript", "iiif_manifest", "facsimile_start_canvas", "edition_pages" },
  "verses": [{
    "number": 1,
    "edition_page": "R10",
    "sections": [{
      "type": "psalm_citation|translation|commentary|gloss",
      "text": "...",
      "language": "lat|ahd|ahd_lat_mixed",
      "sigles_psalter": ["G", "R"],     // disambiguiert: Psalter-Zeugen (G/H + R bei psalm_citation)
      "sigles_sources": ["A"],          // disambiguiert: Patristik (A/C/Br + R sonst)
      "line_n": 2                       // Notker-Zeile innerhalb des Verses
    }],
    "glosses": [{ "text", "translation_nhd", "relates_to" }],
    "translation_nhd": "...",                      // Fließtext, vollkorrigiert
    "translation_nhd_lines": ["...", "..."],       // zeilengetreu (Iteration 2 / US-9)
    "sources": [{ "sigle", "name", "latin_text", "german_translation" }]
  }],
  "psalm_text_comparison": { "witnesses": [...] },
  "wiener_notker": { "text": "..." }
}
```

Silbentrennungen werden im JSON aufgelöst (sowohl innerhalb eines Verses als
auch über Vers-Grenzen, parallel zur semantischen `@part`-Verkettung im TEI).
Die Zeilenstruktur bleibt im TEI (`<ab n="X">`) und im JSON (`line_n`).

## 4. Web-Stack

| Komponente | Technologie | Begründung |
|---|---|---|
| Frontend | Vanilla JS + HTML/CSS | Kein Build-Step, Langlebigkeit |
| Typografie | Gentium Book Plus, Inter | Ahd.-Sonderzeichen |
| IIIF-Viewer | OpenSeadragon 4.1 (CDN) | Standard für Handschriften |
| Deployment | GitHub Pages (`/docs`) | Kostenlos, statisch |
| Pipeline | Python (python-docx, lxml) | DOCX-Parsing, TEI |

Single-File-Prinzip: `docs/index.html` enthält CSS und JS eingebettet.

## 5. IIIF-Integration

| Eigenschaft | Wert |
|---|---|
| Manifest | `https://www.e-codices.unifr.ch/metadata/iiif/csg-0021/manifest.json` |
| API-Version | IIIF Presentation 2.0 |
| Psalm 2 Start | Seite 11 (Canvas-Index 10, 0-basiert) |
| Text-Bild-Synopse | Seiten-Ebene: Vers-Klick → korrekter Canvas |

Vers→Seite-Mapping (vorläufig):

| Verse | MS-Seite | Canvas-Index |
|---|---|---|
| 1–3 | 11 | 10 |
| 4–6 | 12 | 11 |
| 7–9 | 13 | 12 |
| 10–13 | 14 | 13 |

## 6. Offene technische Fragen

- [ ] Vers→Seite-Mapping gegen Facsimile verifizieren
- [ ] Farbüberlagerung Textschicht × Quellenfilter testen (D-11)

## Verknüpfungen

- [[Editionsrichtlinien]] — Kodierungsregeln für TEI
- [[Design]] — UI-Konzept, Toggle-System, Farbsystem
- [[Probeseite Analyse]] — DOCX-Struktur und Parsing-Implikationen
- [[Research Plan]] — Arbeitsphasen und Abhängigkeiten
