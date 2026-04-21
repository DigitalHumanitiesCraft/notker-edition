---
type: tracking
created: 2026-04-21
updated: 2026-04-21
tags: [notker, bug-tracker, tech-debt]
---

# Offene Korrekturen

Liste offener Fixes und technischer Altlasten, nach Ebene sortiert. Oberflächliche UI-Bugs stehen weiter unten; die tieferen Probleme (TEI-Datenmodell, Pipeline-Heuristiken) zuerst, weil sie nachgelagerte Bugs überhaupt erst ermöglichen.

## 1. TEI-Datenmodell

### 1.1 `<note type="sigle">` auf falscher Granularitäts-Ebene

**Problem.** Siglen (G, H, R, A, C, Br) stehen als Marginalnote am Ende eines `<ab>`-Blocks, nicht am einzelnen `<seg>`. Beispiel ([data/tei/psalm2.xml](../data/tei/psalm2.xml)):

```xml
<ab n="2">
  <seg type="psalm" xml:lang="la">QVARE FREMVERVNT GENTES. </seg>
  <seg type="translation" xml:lang="goh">Ziu grís-</seg>
  <note type="sigle" place="margin">G, R</note>
</ab>
```

Die Sigle „G, R" bezieht sich eigentlich auf das Psalmzitat, nicht auf die Übersetzung. Die aktuelle Kodierung zwingt das Python-Skript `disambiguate_sigles()` ([scripts/tei_to_json.py](../scripts/tei_to_json.py)), die Zuordnung nachträglich über den `section_type` zu rekonstruieren — eine Heuristik, die bei mehrdeutigen Fällen scheitern kann.

**Fix-Richtung.** Siglen als Attribut am `<seg>` statt als Sibling-`<note>`:

```xml
<seg type="psalm" xml:lang="la" wit="#G #R">QVARE FREMVERVNT GENTES. </seg>
<seg type="translation" xml:lang="goh">Ziu grís-</seg>
```

Berührt: `scripts/parse_probeseite.py`, `scripts/build_tei.py`, `scripts/tei_to_json.py`, `tests/`.

**Aufwand.** ca. ½ Tag.

**Priorität.** Mittel. Jetziger Zustand liefert korrekte Frontend-Daten, Refactor ist semantisch sauberer.

---

### 1.2 Fehlende `<listWit>` im `<teiHeader>`

**Problem.** Psalter-Zeugen G, H, R sind nirgends als formale `<witness>`-Elemente deklariert. Dadurch sind `@wit`-Referenzen (→ 1.1) derzeit nicht möglich ohne erst die Witness-Liste zu schaffen.

**Fix-Richtung.** Im `<teiHeader>` ergänzen:

```xml
<sourceDesc>
  <listWit>
    <witness xml:id="G">Gallicanum — Hieronymus, ältere Vulgata-Fassung</witness>
    <witness xml:id="H">Hebraicum — Hieronymus iuxta Hebraeos (Bamberg Ms. 44)</witness>
    <witness xml:id="R">Romanum</witness>
    <witness xml:id="A-psalter">Augustinus-Psalter (St. Gallen Cod. 162)</witness>
    <witness xml:id="C-psalter">Cassiodor-Psalter (St. Gallen Cod. 200)</witness>
  </listWit>
</sourceDesc>
```

**Priorität.** Mittel. Geht Hand in Hand mit 1.1.

---

### 1.3 Vermischung zweier semantischer Systeme in einer Sigle-Note

**Problem.** Ein `<note type="sigle">G, R, A</note>` kann gleichzeitig Psalter-Zeugen (G) und Kommentarquellen (A) enthalten. Die Disambiguierung erfolgt erst im JSON-Export. TEI-seitig ist nicht erkennbar, welche Sigle welche Rolle spielt.

**Fix-Richtung.** Getrennte Attribute am `<seg>`:

```xml
<seg type="psalm" xml:lang="la" wit="#G #R">…</seg>        <!-- Textzeugen -->
<seg type="commentary" xml:lang="goh" source="#bibl-A">…</seg>  <!-- Quellenbezug -->
```

Entfernt die Disambiguierungs-Heuristik aus `tei_to_json.py` vollständig.

**Priorität.** Mittel (zusammen mit 1.1, 1.2).

---

### 1.4 R-Disambiguierung noch nicht durch Auftraggeber bestätigt

**Problem.** Der Heuristik-Regel „R in `psalm_citation` = Romanum, R in `commentary`/`translation` = Remigius" (siehe [Domänenwissen#Disambiguierungs-Heuristik](Domänenwissen.md)) fehlt die Bestätigung von Pfeifer. Wenn die Regel falsch ist, sind die `sigles_psalter` / `sigles_sources`-Felder im JSON teilweise falsch zugeordnet.

**Fix-Richtung.** Im nächsten Gespräch mit Pfeifer abklären. Idealerweise liefert er konkrete Textbeispiele zur Verifikation.

**Priorität.** Hoch (für TEI-Refactor-Entscheidung).

---

### 1.5 Ungeklärte Siglen N und RII

**Problem.** N (einmalig Table 4 Row 5) und RII (einmalig Table 4 Row 15) sind in der Probeseite belegt, aber ihre Quelle ist unklar (siehe [Domänenwissen#Kommentarquellen-ungeklärt](Domänenwissen.md)).

**Aktueller Umgang.** `disambiguate_sigles()` packt Unbekanntes als Fallback in `sigles_sources`.

**Fix-Richtung.** Mit Pfeifer klären.

**Priorität.** Niedrig (Einzelfälle, affektieren das Gesamtbild nicht).

---

## 2. Pipeline-Ebene

### 2.1 Zeilengenauigkeit des Notker-Grundtextes (Bug 7)

**Problem.** Der Notker-Grundtext im Frontend folgt nicht zeilentreu der Druckedition. Zeilenumbrüche werden im Parser vermutlich zu einem durchgängigen Fließtext zusammengefasst.

**Zu prüfen.** `parse_probeseite.py` — wie werden `<w:br>`-Elemente aus DOCX übernommen? Werden sie als `<lb/>` nach TEI übertragen? Wenn ja, wertet `tei_to_json.py` sie korrekt aus?

**Berührt.** `parse_probeseite.py`, `tei_to_json.py`, ggf. `docs/index.html` (Renderer).

**Priorität.** Hoch (direkter User-Bug).

---

### 2.2 Kursivierung ahd. vs. lat. in nhd.-Übersetzung (Bug 8)

**Problem.** Die nhd. Arbeitsübersetzung differenziert nicht visuell zwischen ahd. und lat. Grundtext. In der Probeseite sind lat. Passagen in der nhd. Spalte kursiv gesetzt; diese Information wird im Parser/Export verloren.

**Zu prüfen.** Nimmt `parse_probeseite.py` Italic-Runs in der nhd.-Spalte wahr? Werden sie in TEI als `<hi rend="italic">` oder `<foreign>` übertragen? Kommen sie im JSON-`translation_nhd` an?

**Berührt.** `parse_probeseite.py`, `tei_to_json.py`, `docs/index.html` (CSS + Renderer).

**Priorität.** Hoch (direkter User-Bug).

---

### 2.3 Zahlendarstellung in Wiener Notker und Psalterien (Bug 5)

**Problem.** Zahlen > 9 werden in den synoptischen Psaltertext-Ansichten getrennt dargestellt (z.B. „1 0" statt „10"). Ursache vermutlich im Vers-Splitting: das Regex `splitIntoVerses()` in [docs/index.html:3703](../docs/index.html#L3703) matcht `\d{1,2}[A-Z\[]`, aber wenn der Text „10I" enthält, wird evtl. „1" als Versnummer und „0I" als Text interpretiert.

**Zu prüfen.** Funktioniert die Regex bei zweistelligen Versnummern? Testfall mit Vers 10+ durchspielen.

**Berührt.** `docs/index.html` — `splitIntoVerses()`.

**Priorität.** Mittel.

---

## 3. UI-Ebene

### 3.1 Latein/Deutsch-Trennung: „nebeneinander" vs. „untereinander" (Bug 2)

**Status.** Offen, Kunden-Rücksprache nötig.

**Kern.** Der `lat./ahd.`-Toggle rendert bereits zwei Spalten ([docs/index.html:3261-3296](../docs/index.html#L3261-L3296)), aber jedes `<seg>` bekommt eine eigene Grid-Zeile und füllt nur eine der zwei Spalten — visuell entsteht ein Treppen-Effekt. Drei mögliche Lesarten des Bugs:

1. Echte Parallelstellung mit Pairing-Logik (aufwändig, editorisch kompliziert).
2. Zwei-Spalten-Fluss ohne Zeilensprünge (CSS-Flip).
3. Aktueller Zustand ist korrekt.

**Priorität.** Hoch, blockiert von Pfeifer-Rückfrage.

---

### 3.2 Fenster-Vergrößerung (Bug 1) — UX-Abnahme

**Status.** Technisch refactored (symmetrischer Drag, Reset-Button in Top-Nav, `min-width: 240px`, kein 800px-Cap). Abnahme durch Auftraggeber steht aus.

**Priorität.** Niedrig (funktioniert, aber UX-Geschmack ist subjektiv).

---

### 3.3 Geschlossene Panels wiederöffnen (Bug 6)

**Status.** Funktioniert bereits über:
- Restore-Bar am unteren Bildschirmrand (erscheint wenn Slots geschlossen sind)
- „Ansicht zurücksetzen"-Button in der Top-Nav (öffnet alle + setzt Breiten zurück)

**Offen.** UX-Abnahme: ist die Restore-Bar entdeckbar genug? Ggf. visueller Hinweis nötig („↓ unten auf der Seite erscheint eine Leiste zum Wiederöffnen").

**Priorität.** Niedrig.

---

---

## 4. Erledigt in diesem Durchgang

- **Bug 3** (Psalter-Buttons G/H/R ohne Wirkung): CSS-Variablen `--color-psa-G/H/R` ergänzt, Chip-Styling pro Sigle scoped by group (R-Kollision weg), Highlight-Rendering auf linear-gradient umgestellt.
- **Bug 4** (Mehrfachauswahl Psalterien): `break;` in `updateSourceHighlights()` entfernt, alle Matches werden gesammelt und als gestapelte 3px-Streifen am linken Rand gerendert.
- **2.4 Word-Fußnoten integriert.** Parser liest `word/footnotes.xml` und attachiert jede Referenz an den Anker-Run. TEI-Kodierung als `<note type="editorial" n="N" resp="#pfeifer"><label>anchor</label>body</note>` am `<ab>` (RelaxNG-valide — `@corresp` ist auf `<note>` nicht erlaubt, `<label>`-Kind ist es). JSON-Feld `verse.footnotes: [{n, anchor, body, line_n}]` plus `source.footnotes` für Quellen-interne Fußnoten. Frontend rendert eine Fußnoten-Liste unterhalb jedes Vers-Grids und unter betreffenden Quelleneinträgen (Nummer-Chip, Anker-Wort, Body). 56 von 58 Fußnoten aus der DOCX jetzt sichtbar; die verbleibenden zwei liegen in Positionen, die der aktuelle Parser nicht abdeckt (z. B. Psalter-Header-Zeilen).

## 5. Verknüpfungen

- [Domänenwissen](Domänenwissen.md) — Siglen-System, Disambiguierungs-Heuristik
- [Technik](Technik.md) — Pipeline, TEI-Modell
- [Editionsrichtlinien](Editionsrichtlinien.md) — TEI-Kodierungsregeln
- [Journal](Journal.md) — Chronologie der Entscheidungen
