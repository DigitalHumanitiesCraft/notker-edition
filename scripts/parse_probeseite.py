#!/usr/bin/env python3
"""
parse_probeseite.py — DOCX → Python-Zwischenformat

Parst Probeseite_Notker.docx und erzeugt ein strukturiertes Zwischenformat
(Python-Dicts / dataclasses) für die TEI-XML-Generierung.

Regelbasiert: Farben, Merged Cells, Zeilentypen, Vers-Zuordnung.
"""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import docx
from docx.oxml.ns import qn


# ---------------------------------------------------------------------------
# Dataclasses (Zwischenformat)
# ---------------------------------------------------------------------------

@dataclass
class Run:
    """Ein DOCX-Run mit Text, Farbe und Formatierung."""
    text: str
    color: Optional[str]  # '806000', '00B050', or None (=black)
    bold: bool = False
    italic: bool = False


@dataclass
class Segment:
    """Ein zusammenhängender Textabschnitt gleicher Farbe/Funktion."""
    text: str
    function: str       # 'psalm', 'translation', 'commentary'
    color: Optional[str]
    runs: list = field(default_factory=list)  # Original-Runs für Feinanalyse


@dataclass
class TextLine:
    """Eine Haupttext-Zeile der Probeseite."""
    segments: list       # List[Segment]
    nhd: str = ''        # nhd. Übersetzung (kursiv-Spalte)
    sigles: str = ''     # Siglen-Spalte (z.B. 'G, R')
    line_number: int = 0


@dataclass
class GlossLine:
    """Eine Interlinearglosse."""
    text: str            # ahd./lat. Glossentext
    nhd: str = ''        # nhd. Übersetzung
    sigles: str = ''
    line_number: int = 0


@dataclass
class SourceEntry:
    """Ein Eintrag im Quellenapparat."""
    sigle: str           # 'A', 'C', 'R', 'Br', 'RII', 'N'
    latin: str = ''
    german: str = ''
    bold_spans: list = field(default_factory=list)  # Positionen fetter Wörter


@dataclass
class PsalterWitness:
    """Ein Textzeuge im synoptischen Psaltervergleich."""
    sigle: str           # 'G', 'R', 'H', 'A', 'C'
    name: str = ''       # 'Gallicanum', etc.
    manuscript: str = ''
    text: str = ''


@dataclass
class VerseGroup:
    """Eine Versgruppe (z.B. Verse 1-2) mit allen zugehörigen Daten."""
    verses: str          # Versreferenz, z.B. '1-2'
    verse_numbers: list  # [1, 2]
    lines: list = field(default_factory=list)      # List[TextLine | GlossLine]
    sources: list = field(default_factory=list)     # List[SourceEntry]


@dataclass
class PsalmData:
    """Gesamtdaten für einen Psalm."""
    psalm_number: int = 2
    verse_groups: list = field(default_factory=list)   # List[VerseGroup]
    psalter_witnesses: list = field(default_factory=list)  # List[PsalterWitness]
    wiener_notker: str = ''


# ---------------------------------------------------------------------------
# Farb-Mapping
# ---------------------------------------------------------------------------

COLOR_MAP = {
    '806000': 'psalm',       # olive → Psalmzitation
    '00B050': 'translation',  # grün → ahd. Übersetzung
    None: 'commentary',       # schwarz → Kommentar
}

KNOWN_SIGLES = {'A', 'C', 'R', 'Br', 'RII', 'N'}
# Extended: in the DOCX, "R II" appears as two runs "R " + "II"
SIGLE_PATTERN = re.compile(r'^(A|C|R|Br|RII|R\s*II|N)$')


# ---------------------------------------------------------------------------
# DOCX-Hilfsfunktionen
# ---------------------------------------------------------------------------

def get_run_color(run) -> Optional[str]:
    """Extrahiert die Schriftfarbe eines Runs."""
    rpr = run._element.find(qn('w:rPr'))
    if rpr is not None:
        color_el = rpr.find(qn('w:color'))
        if color_el is not None:
            val = color_el.get(qn('w:val'))
            if val and val.upper() != '000000':
                return val
    return None


def get_cell_runs(cell) -> list[Run]:
    """Extrahiert alle Runs einer Zelle mit Farbe und Formatierung."""
    runs = []
    for para in cell.paragraphs:
        for run in para.runs:
            if run.text:  # auch Leerzeichen bewahren
                runs.append(Run(
                    text=run.text,
                    color=get_run_color(run),
                    bold=bool(run.bold),
                    italic=bool(run.italic),
                ))
    return runs


def cell_text(cell) -> str:
    """Gesamttext einer Zelle."""
    return ''.join(p.text for p in cell.paragraphs).strip()


def is_merged_row(row) -> bool:
    """Prüft ob Cols 0-2 identisch sind (merged cells)."""
    cells = row.cells
    if len(cells) < 3:
        return False
    t0 = cell_text(cells[0])
    t1 = cell_text(cells[1])
    t2 = cell_text(cells[2])
    # Alle drei gleich und nicht-leer
    return t0 == t1 == t2 and t0 != ''


def is_empty_row(row) -> bool:
    """Prüft ob alle Zellen leer sind."""
    return all(cell_text(c) == '' for c in row.cells)


# ---------------------------------------------------------------------------
# Runs → Segmente (Farb-basiert zusammenführen)
# ---------------------------------------------------------------------------

def runs_to_segments(runs: list[Run]) -> list[Segment]:
    """Fasst aufeinanderfolgende Runs gleicher Farbe zu Segmenten zusammen."""
    if not runs:
        return []

    segments = []
    current_color = runs[0].color
    current_runs = [runs[0]]
    current_texts = [runs[0].text]

    for run in runs[1:]:
        if run.color == current_color:
            current_runs.append(run)
            current_texts.append(run.text)
        else:
            fn = COLOR_MAP.get(current_color, 'commentary')
            segments.append(Segment(
                text=''.join(current_texts),
                function=fn,
                color=current_color,
                runs=list(current_runs),
            ))
            current_color = run.color
            current_runs = [run]
            current_texts = [run.text]

    # Letztes Segment
    fn = COLOR_MAP.get(current_color, 'commentary')
    segments.append(Segment(
        text=''.join(current_texts),
        function=fn,
        color=current_color,
        runs=list(current_runs),
    ))

    return segments


# ---------------------------------------------------------------------------
# Zeilentyp-Erkennung
# ---------------------------------------------------------------------------

def detect_source_row(row) -> Optional[SourceEntry]:
    """Erkennt eine Quellenapparat-Zeile: Col 0 = einzelne Sigle."""
    cells = row.cells
    col0_text = cell_text(cells[0]).strip()

    # Normalisierung: "R II" → "RII"
    normalized = col0_text.replace(' ', '')

    if not SIGLE_PATTERN.match(normalized):
        return None

    # Sicherheitscheck: Col 1 muss substantiellen Text haben
    if len(cells) < 2:
        return None
    col1_text = cell_text(cells[1]).strip()
    if len(col1_text) < 5:
        return None

    # Latin-Text: Col 1 (Runs ohne Formatierung, aber Bold bewahren)
    latin_text = col1_text

    # Bold-Spans in Col 1 extrahieren
    bold_spans = []
    col1_runs = get_cell_runs(cells[1])
    pos = 0
    for r in col1_runs:
        if r.bold and r.text.strip():
            bold_spans.append((pos, pos + len(r.text), r.text))
        pos += len(r.text)

    # German translation: Col 2+ (kursiv)
    german = ''
    for ci in range(2, len(cells)):
        ct = cell_text(cells[ci]).strip()
        if ct and ct != col1_text:  # Nicht dupliziert
            german = ct
            break

    return SourceEntry(
        sigle=normalized,
        latin=latin_text,
        german=german,
        bold_spans=bold_spans,
    )


def detect_gloss_line(text_runs: list[Run], nhd: str, sigles: str) -> bool:
    """
    Heuristik: Ist diese Zeile eine Interlinearglosse?
    Kriterien:
    - Kurzer Text (≤ 5 Wörter)
    - Nur schwarze Runs (keine olive/grüne Farbe)
    - nhd-Spalte hat ebenfalls kurzen Text
    - Kein Satzzeichen am Ende (Glossen enden nicht mit '.')
    - Keine Klammern (Bibliographische Angaben)
    - Keine Verben im Vollsatzformat
    """
    if not text_runs:
        return False

    full_text = ''.join(r.text for r in text_runs).strip()
    words = full_text.split()

    if len(words) > 5:
        return False

    # Keine farbigen Runs (olive oder grün → keine Glosse)
    if any(r.color in ('806000', '00B050') for r in text_runs):
        return False

    # nhd-Spalte sollte auch kurz sein (Glosse hat kurze Übersetzung)
    nhd_words = nhd.strip().split() if nhd else []
    if len(nhd_words) > 5:
        return False

    # Leerer Text → keine Glosse
    if len(full_text) < 2:
        return False

    # Klammern → bibliographische Angabe, nicht Glosse
    if '(' in full_text or ')' in full_text:
        return False

    # Text mit Punkt am Ende → eher Kommentar als Glosse
    # (Ausnahme: ".i." = id est, das ist eine Glosse)
    if full_text.endswith('.') and not full_text.startswith('.i.'):
        return False

    # Vollständige Sätze mit Verb → Kommentar
    # Heuristik: enthält ein konjugiertes Verb-Muster (ahd. endet oft auf -t, -n)
    # Aber viele Glossen enthalten auch "-" (Silbentrennung) → das ist OK
    # Strenger: wenn nhd leer, dann eher keine nützliche Glosse
    # (außer es ist ein Verweis wie "kerich" → "Gericht?")

    return True


# ---------------------------------------------------------------------------
# Vers-Referenz parsen
# ---------------------------------------------------------------------------

def parse_verse_ref(text: str) -> Optional[tuple[str, list[int]]]:
    """
    Parst Vers-Referenzen wie '2,1-2', '2,3-2,5', '2,6'.
    Text kommt oft verdreifacht aus Merged Cells (z.B. '2,1-22,1-22,1-2').
    Gibt (ref_string, [verse_numbers]) zurück.
    """
    text = text.strip()
    if not text:
        return None

    # Brute-Force: Probiere alle gültigen Vers-Referenzen für Psalm 2 (Verse 1-13)
    # und prüfe ob sie als Substring vorkommen mit Grenzprüfung (kein Digit danach).
    # Das umgeht das Problem mit zusammengeklebten Merged-Cell-Texten.
    candidates = []

    def has_boundary_match(pattern: str) -> bool:
        """Prüft ob pattern als Substring mit nicht-Digit-Grenze vorkommt."""
        start = 0
        while True:
            idx = text.find(pattern, start)
            if idx == -1:
                return False
            end_idx = idx + len(pattern)
            # Nach dem Match darf kein Digit folgen
            if end_idx >= len(text) or not text[end_idx].isdigit():
                return True
            start = idx + 1

    # Ranges (Psalm,Start-Psalm,End)
    for s in range(1, 14):
        for e in range(s + 1, 14):
            pattern = f'2,{s}-2,{e}'
            if has_boundary_match(pattern):
                candidates.append((f'{s}-{e}', list(range(s, e + 1))))

    # Ranges (Psalm,Start-End)
    for s in range(1, 14):
        for e in range(s + 1, 14):
            pattern = f'2,{s}-{e}'
            if has_boundary_match(pattern):
                candidates.append((f'{s}-{e}', list(range(s, e + 1))))

    # Einzelverse (Psalm,Vers)
    for v in range(1, 14):
        pattern = f'2,{v}'
        if has_boundary_match(pattern):
            candidates.append((str(v), [v]))

    if not candidates:
        return None

    # Bevorzuge Ranges über Einzelverse (spezifischste = längste Versliste)
    # Bei Gleichstand: kürzere Textform bevorzugen
    candidates.sort(key=lambda c: (-len(c[1]), len(c[0])))
    return candidates[0]
    # 2,3-2,5 (Psalm.Vers - Psalm.Vers)
    m = re.match(r'^(\d+),(\d+)\s*-\s*\d+,(\d+)$', text)
    if m:
        start, end = int(m.group(2)), int(m.group(3))
        return f'{start}-{end}', list(range(start, end + 1))

    # 2,1-2 (Psalm, VerseStart-VerseEnd)
    m = re.match(r'^(\d+),(\d+)\s*-\s*(\d+)$', text)
    if m:
        start, end = int(m.group(2)), int(m.group(3))
        return f'{start}-{end}', list(range(start, end + 1))

    # 2,6 (Psalm, Vers)
    m = re.match(r'^(\d+),(\d+)$', text)
    if m:
        v = int(m.group(2))
        return str(v), [v]

    # Fallback: versuche aus dem verdreifachten Text das erste gültige Muster
    for pat, ngroups in [
        (r'(\d+),(\d+)\s*-\s*\d+,(\d+)', 3),
        (r'(\d+),(\d+)\s*-\s*(\d+)', 3),
        (r'(\d+),(\d+)', 2),
    ]:
        m = re.search(pat, text)
        if m:
            if ngroups == 3:
                start, end = int(m.group(2)), int(m.group(3))
                if end < 20 and start <= end:  # Plausibilitätscheck
                    return f'{start}-{end}', list(range(start, end + 1))
            elif ngroups == 2:
                v = int(m.group(2))
                if v < 20:
                    return str(v), [v]

    return None


# ---------------------------------------------------------------------------
# Hauptparser
# ---------------------------------------------------------------------------

def parse_probeseite(docx_path: str) -> PsalmData:
    """Parst die Probeseite und gibt das strukturierte Zwischenformat zurück."""

    doc = docx.Document(docx_path)
    psalm = PsalmData()

    # Phase 1: Dokument-Elemente in Reihenfolge durchgehen
    # und Paragraphen (Vers-Überschriften) von Tabellen trennen
    elements = []
    body = doc.element.body
    table_index = 0

    para_index = 0
    all_paragraphs = doc.paragraphs

    for elem in body:
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'p':
            # Text über python-docx Paragraph extrahieren (sauberer als XML-Iteration)
            if para_index < len(all_paragraphs):
                para_text = all_paragraphs[para_index].text.strip()
                if para_text:
                    elements.append(('paragraph', para_text))
            para_index += 1
        elif tag == 'tbl':
            if table_index < len(doc.tables):
                elements.append(('table', doc.tables[table_index]))
                table_index += 1

    # Phase 2: Vers-Gruppen bilden
    current_group = None
    groups = []

    for etype, edata in elements:
        if etype == 'paragraph':
            ref = parse_verse_ref(edata)
            if ref:
                ref_str, verse_nums = ref
                current_group = VerseGroup(
                    verses=ref_str,
                    verse_numbers=verse_nums,
                )
                groups.append(current_group)

        elif etype == 'table' and current_group is not None:
            parse_table(edata, current_group, psalm)

    psalm.verse_groups = groups

    # Zeilennummern vergeben
    for group in psalm.verse_groups:
        for i, line in enumerate(group.lines):
            line.line_number = i + 1

    return psalm


def parse_table(table, group: VerseGroup, psalm: PsalmData):
    """Parst eine einzelne Tabelle und fügt Daten zur VerseGroup/PsalmData hinzu."""

    rows = list(table.rows)
    if not rows:
        return

    ncols = max(len(r.cells) for r in rows)

    # Sonderfall: Wiener Notker (1 Spalte, Header enthält "Wiener")
    if ncols <= 2:
        first_cell_text = cell_text(rows[0].cells[0])
        if 'Wiener' in first_cell_text or 'ÖNB' in first_cell_text:
            if len(rows) > 1:
                psalm.wiener_notker = cell_text(rows[1].cells[0])
            return

        # Sonderfall: Psalter-Vergleich (2 Spalten, Header mit Cod.)
        if 'Cod.' in first_cell_text or 'Psalter' in first_cell_text.lower():
            parse_psalter_table(table, psalm)
            return

    for row in rows:
        if is_empty_row(row):
            continue

        cells = row.cells

        # Prüfe auf Quellenapparat-Zeile
        source = detect_source_row(row)
        if source:
            group.sources.append(source)
            continue

        # Prüfe auf Psaltervergleich-Zeilen (Siglen-Header mit G, R, H)
        if is_psalter_header_row(row, ncols):
            parse_psalter_inline(table, rows, row, psalm)
            return  # Rest der Tabelle ist Psaltervergleich

        # Haupttext-Zeilen (Merged Cells)
        if is_merged_row(row):
            parse_haupttext_row(row, group, ncols)
        elif ncols >= 3:
            # Nicht-gemergte Zeile mit ≥3 Spalten: könnte auch Haupttext sein
            # wenn Col 0 substantiellen Text hat
            col0 = cell_text(cells[0])
            if len(col0) > 3 and not SIGLE_PATTERN.match(col0.strip().replace(' ', '')):
                parse_haupttext_row(row, group, ncols)


def parse_haupttext_row(row, group: VerseGroup, ncols: int):
    """Parst eine Haupttext-Zeile (gemergete oder nicht-gemergte)."""
    cells = row.cells

    # Haupttext: Col 0 (bei merged: Col 0 = Col 1 = Col 2)
    text_runs = get_cell_runs(cells[0])
    if not text_runs:
        return

    segments = runs_to_segments(text_runs)

    # nhd-Spalte: vorletzte oder letzte nicht-identische Spalte
    nhd = ''
    sigles = ''

    if ncols >= 4:
        # Bei 5-Spalten-Tabellen: Col 3 = nhd, Col 4 = Siglen
        # Bei 3-Spalten-Tabellen (nicht merged): Col 1 = nhd, Col 2 = Siglen
        nhd_col = min(3, ncols - 2) if ncols >= 5 else 1
        sigles_col = min(4, ncols - 1) if ncols >= 5 else 2

        nhd_candidate = cell_text(cells[nhd_col])
        sigles_candidate = cell_text(cells[sigles_col])

        # Validierung: nhd sollte länger sein, Siglen kurz
        if len(sigles_candidate) <= 15:
            sigles = sigles_candidate
        if nhd_candidate != cell_text(cells[0]):  # Nicht identisch mit Haupttext
            nhd = nhd_candidate
    elif ncols == 3:
        # 3-Spalten: Col 1 = nhd, Col 2 = Siglen (wenn nicht merged)
        if not is_merged_row(row):
            nhd = cell_text(cells[1])
            sigles = cell_text(cells[2])
        else:
            # Merged 3-Spalten: keine nhd/Siglen-Spalte sichtbar
            pass
    elif ncols >= 5:
        nhd = cell_text(cells[3])
        sigles = cell_text(cells[4])

    # Glossen-Erkennung
    if detect_gloss_line(text_runs, nhd, sigles):
        full_text = ''.join(r.text for r in text_runs).strip()
        group.lines.append(GlossLine(
            text=full_text,
            nhd=nhd,
            sigles=sigles,
        ))
    else:
        group.lines.append(TextLine(
            segments=segments,
            nhd=nhd,
            sigles=sigles,
        ))


def is_psalter_header_row(row, ncols: int) -> bool:
    """Erkennt die Sigle-Header-Zeile des Psaltervergleichs."""
    if ncols < 3:
        return False
    cells = row.cells
    texts = [cell_text(c).strip() for c in cells[:min(5, ncols)]]
    # Psaltervergleich: Zeile mit nur Siglen (G, R, H)
    sigles_found = sum(1 for t in texts if t in ('G', 'R', 'H', 'A', 'C'))
    return sigles_found >= 3


def parse_psalter_inline(table, rows, header_row, psalm: PsalmData):
    """Parst den Psaltervergleich aus einer Tabelle mit Siglen-Header."""
    cells = header_row.cells
    ncols = len(cells)

    # Sigle pro Spalte
    sigles = [cell_text(c).strip() for c in cells[:ncols]]

    # Nächste Zeile(n) enthalten den Text
    header_idx = rows.index(header_row)
    for row in rows[header_idx + 1:]:
        if is_empty_row(row):
            continue
        for ci in range(min(ncols, len(row.cells))):
            if ci < len(sigles) and sigles[ci]:
                text = cell_text(row.cells[ci]).strip()
                if text and len(text) > 10:
                    psalm.psalter_witnesses.append(PsalterWitness(
                        sigle=sigles[ci],
                        text=text,
                    ))
        break  # Nur eine Textzeile erwartet


def parse_psalter_table(table, psalm: PsalmData):
    """Parst eine eigenständige Psalter-Vergleichstabelle (T11)."""
    for row in table.rows:
        cells = row.cells
        if len(cells) >= 2:
            for cell in cells:
                ct = cell_text(cell).strip()
                if 'Cod. 162' in ct:
                    psalm.psalter_witnesses.append(PsalterWitness(
                        sigle='A',
                        name='Augustinus-Psalter',
                        manuscript='St. Gallen Cod. 162',
                    ))
                elif 'Cod. 200' in ct:
                    psalm.psalter_witnesses.append(PsalterWitness(
                        sigle='C',
                        name='Cassiodor-Psalter',
                        manuscript='St. Gallen Cod. 200',
                    ))
        # Text-Zeile (2. Reihe)
        if len(cells) >= 2:
            for i, wit in enumerate(psalm.psalter_witnesses):
                if wit.sigle in ('A', 'C') and not wit.text:
                    # Versuche den Text aus der nächsten Zeile zu holen
                    pass

    # Zweite Zeile hat den eigentlichen Text
    if len(table.rows) > 1:
        text_row = table.rows[1]
        for ci, cell in enumerate(text_row.cells):
            ct = cell_text(cell).strip()
            if ct and len(ct) > 20:
                # Zuordnung über Position
                for wit in psalm.psalter_witnesses:
                    if wit.sigle in ('A', 'C') and not wit.text:
                        wit.text = ct
                        break


# ---------------------------------------------------------------------------
# Ausgabe / Debug
# ---------------------------------------------------------------------------

def print_summary(psalm: PsalmData):
    """Gibt eine Zusammenfassung des geparsten Psalms aus."""
    print(f'=== Psalm {psalm.psalm_number} ===')
    print(f'Versgruppen: {len(psalm.verse_groups)}')

    total_text = 0
    total_gloss = 0
    total_sources = 0

    for vg in psalm.verse_groups:
        text_lines = [l for l in vg.lines if isinstance(l, TextLine)]
        gloss_lines = [l for l in vg.lines if isinstance(l, GlossLine)]
        total_text += len(text_lines)
        total_gloss += len(gloss_lines)
        total_sources += len(vg.sources)

        print(f'\n--- Verse {vg.verses} (V. {vg.verse_numbers}) ---')
        print(f'  Textzeilen: {len(text_lines)}, Glossen: {len(gloss_lines)}, '
              f'Quellen: {len(vg.sources)}')

        for line in vg.lines:
            if isinstance(line, TextLine):
                seg_summary = ' | '.join(
                    f'[{s.function}] {s.text[:50]}' for s in line.segments
                )
                print(f'  L{line.line_number}: {seg_summary}')
                if line.nhd:
                    print(f'    nhd: {line.nhd[:60]}')
                if line.sigles:
                    print(f'    sigles: {line.sigles}')
            elif isinstance(line, GlossLine):
                print(f'  G{line.line_number}: GLOSSE "{line.text}" → "{line.nhd}"')

        for src in vg.sources:
            print(f'  SRC [{src.sigle}]: {src.latin[:60]}...')
            if src.german:
                print(f'    de: {src.german[:60]}...')

    print(f'\n=== Summe: {total_text} Textzeilen, {total_gloss} Glossen, '
          f'{total_sources} Quelleneinträge ===')

    print(f'\nPsalter-Zeugen: {len(psalm.psalter_witnesses)}')
    for wit in psalm.psalter_witnesses:
        print(f'  [{wit.sigle}] {wit.name or "(Name fehlt)"}: '
              f'{wit.text[:60] if wit.text else "(Text fehlt)"}...')

    print(f'\nWiener Notker: {"Ja" if psalm.wiener_notker else "Nein"} '
          f'({len(psalm.wiener_notker)} Zeichen)')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    docx_path = Path(__file__).parent.parent / 'data' / 'Probeseite_Notker.docx'
    if not docx_path.exists():
        print(f'FEHLER: {docx_path} nicht gefunden')
        sys.exit(1)

    psalm = parse_probeseite(str(docx_path))
    print_summary(psalm)
    return psalm


if __name__ == '__main__':
    main()
