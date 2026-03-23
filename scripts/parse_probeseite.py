"""
parse_probeseite.py — Probeseite_Notker.docx → psalm2.json

Parses Philipp's Word document (the authoritative primary data source)
into a structured JSON model. Extracts:
  - Main text with functional layer classification (psalm_citation / translation / commentary)
  - Interlinear glosses
  - Source apparatus (patristic sources with Latin + German)
  - NHD translation
  - Source sigles per line
  - Psalm text comparison (5 witnesses)
  - Wiener Notker parallel text

Color mapping (from DOCX run-level formatting):
  #806000 (olive)  → psalm_citation
  #00B050 (green)  → translation
  default (black)  → commentary

See knowledge/Probeseite Analyse.md for full structural documentation.
"""

import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from docx import Document
from docx.oxml.ns import qn

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DOCX_PATH = Path(__file__).parent.parent / "data" / "Probeseite_Notker.docx"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "processed" / "psalm2.json"

COLOR_PSALM_CITATION = "806000"
COLOR_TRANSLATION = "00B050"

# Known source sigles that appear in column 0 of apparatus rows
KNOWN_SIGLES = {"A", "C", "R", "Br", "RII", "N"}

# Max character length for a line to be considered a potential gloss
GLOSS_MAX_LENGTH = 45

# Verse ranges derived from paragraph headings between tables in the DOCX.
VERSE_RANGES = {
    0: (1, 2),    # Table 1:  "2,1-2"
    1: (3, 4),    # Table 2:  continuation / "2,3-2,5"
    2: (5, 6),    # Table 3:  "2,5-6"
    3: (6, 7),    # Table 4:  "2,6-7" (overlaps with 6)
    4: (7, 7),    # Table 5:  "2,7" continuation
    5: (7, 7),    # Table 6:  sources for verse 7
    6: (8, 9),    # Table 7:  "2,8-9"
    7: (10, 11),  # Table 8:  "2,10-11"
    8: (10, 11),  # Table 9:  sources for 10-11
    9: (12, 13),  # Table 10: "2,12-13" (V13 starts mid-table with "Cum exarserit")
    10: (12, 13), # Table 11: "2,12-13" + psalm text comparison
    11: None,     # Table 12: Psalter comparison (A, C)
    12: None,     # Table 13: Wiener Notker
}

# Known psalm citation openings for Psalm 2 (Vulgata, Gallicanum).
# Used to detect verse boundaries within multi-verse tables.
# Each key is a lowercase prefix of the psalm citation → verse number.
PSALM_VERSE_STARTS = {
    "psalvs david": 0,  # Title, not a verse — ignore for splitting
    "qvare fremvervnt": 1,
    "astiterunt reges": 2,
    "disrumpamus uincula": 3,
    "qui habitat in c": 4,
    "tunc loquetur": 5,
    "ego autem": 6,
    "dominus dixit": 7,
    "postula a me": 8,
    "reges eos in virga": 9,
    "et nunc reges": 10,
    "seruite domino": 11,
    "apprehendite disciplinam": 12,
    "cum exarserit": 13,
    # Also match lowercase versions since not all citations are VERSALIEN
    "vox christi": 6,       # Heading before verse 6 psalm citation
    "vox prophetȩ": 10,     # Heading before verse 10
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class TextRun:
    text: str
    color: str  # "806000", "00B050", or "default"


@dataclass
class Section:
    type: str       # psalm_citation, translation, commentary
    text: str
    language: str   # lat, ahd, ahd_lat_mixed
    translation_nhd: str = ""
    source_sigles: list = field(default_factory=list)


@dataclass
class Gloss:
    position: str
    text: str
    translation_nhd: str = ""
    relates_to: str = ""


@dataclass
class Source:
    sigle: str
    name: str = ""
    latin_text: str = ""
    german_translation: str = ""


@dataclass
class Verse:
    number: int
    sections: list = field(default_factory=list)
    glosses: list = field(default_factory=list)
    sources: list = field(default_factory=list)
    bible_references: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Source name lookup
# ---------------------------------------------------------------------------

SOURCE_NAMES = {
    "A": "Augustinus, Enarrationes in Psalmos",
    "C": "Cassiodor, Expositio Psalmorum",
    "R": "Remigius",
    "Br": "Breviarium",
    "RII": "Unbekannt (zweite Remigius-Quelle?)",
    "N": "Unbekannt",
}


# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------

def get_run_color(run) -> str:
    """Extract the font color from a run. Returns hex string or 'default'."""
    if run.font.color and run.font.color.rgb:
        return str(run.font.color.rgb)
    return "default"


def extract_colored_runs(cell) -> list[TextRun]:
    """Extract all runs from a cell with their colors."""
    runs = []
    for para in cell.paragraphs:
        for run in para.runs:
            text = run.text
            if not text:
                continue
            color = get_run_color(run)
            # Normalize color
            if color not in (COLOR_PSALM_CITATION, COLOR_TRANSLATION):
                color = "default"
            runs.append(TextRun(text=text, color=color))
    return runs


def runs_to_sections(runs: list[TextRun]) -> list[Section]:
    """Group consecutive runs of the same color into Sections."""
    if not runs:
        return []

    sections = []
    current_color = runs[0].color
    current_text_parts = [runs[0].text]

    for run in runs[1:]:
        if run.color == current_color:
            current_text_parts.append(run.text)
        else:
            text = "".join(current_text_parts).strip()
            if text:
                sections.append(_make_section(text, current_color))
            current_color = run.color
            current_text_parts = [run.text]

    # Final group
    text = "".join(current_text_parts).strip()
    if text:
        sections.append(_make_section(text, current_color))

    return sections


def _make_section(text: str, color: str) -> Section:
    """Create a Section from text and its DOCX color."""
    if color == COLOR_PSALM_CITATION:
        return Section(
            type="psalm_citation",
            text=text,
            language="lat",
        )
    elif color == COLOR_TRANSLATION:
        # Translation can contain Latin loanwords; detect mixed
        lang = _detect_language(text)
        return Section(
            type="translation",
            text=text,
            language=lang,
        )
    else:
        lang = _detect_language(text)
        return Section(
            type="commentary",
            text=text,
            language=lang,
        )


def _detect_language(text: str) -> str:
    """
    Simple heuristic for language detection.
    If text contains typical OHG markers (accented vowels, specific words),
    classify as ahd or mixed.
    """
    # Common OHG accent markers
    ahd_markers = set("âêîôûáéíóú")
    has_ahd = any(c in ahd_markers for c in text)

    # Common Latin indicators (but NOT Latin words that appear in OHG context)
    latin_patterns = [
        r'\b(et|in|idest|sunt|eius|dominum|christum|eos)\b',
        r'\b[A-Z]{3,}\b',  # All-caps words (psalm citations in lowercase context)
    ]
    has_latin = any(re.search(p, text) for p in latin_patterns)

    if has_ahd and has_latin:
        return "ahd_lat_mixed"
    elif has_ahd:
        return "ahd"
    elif has_latin:
        return "lat"
    else:
        # Default: if it contains common OHG words, call it ahd
        return "ahd"


def get_cell_text(cell) -> str:
    """Get plain text from a cell, joining paragraphs with spaces."""
    return " ".join(p.text.strip() for p in cell.paragraphs if p.text.strip())


def is_empty_row(row) -> bool:
    """Check if all cells in a row are empty."""
    return all(not get_cell_text(cell) for cell in row.cells)


def is_apparatus_row(row) -> bool:
    """
    Check if this row is a source apparatus entry.
    Apparatus rows have a single known sigle in column 0.
    """
    col0_text = get_cell_text(row.cells[0]).strip()
    return col0_text in KNOWN_SIGLES


def is_gloss_row(row, num_cols: int) -> bool:
    """
    Heuristic: a gloss row has short text, no sigle, and no olive-colored runs.
    """
    # Get text from the main text column (column 0)
    col0_text = get_cell_text(row.cells[0]).strip()

    if not col0_text or len(col0_text) > GLOSS_MAX_LENGTH:
        return False

    # Must not be an apparatus row
    if col0_text in KNOWN_SIGLES:
        return False

    # Check: no olive (psalm_citation) color in column 0
    runs = extract_colored_runs(row.cells[0])
    has_olive = any(r.color == COLOR_PSALM_CITATION for r in runs)
    if has_olive:
        return False

    # Check: last column (sigles) should be empty for glosses
    sigles_text = get_cell_text(row.cells[-1]).strip()
    if sigles_text and any(s in sigles_text for s in KNOWN_SIGLES):
        return False

    # If the text is very short and doesn't look like a text continuation
    # (no sentence-ending punctuation continuation), it's likely a gloss
    if len(col0_text) < GLOSS_MAX_LENGTH:
        # Additional check: glosses typically don't start with lowercase
        # continuation of a previous line (like "tati sunt inania")
        # But some do (like "gen  chúnftîg"). So we keep this loose.
        return True

    return False


def parse_sigles(text: str) -> list[str]:
    """Parse sigles from the sigles column (e.g., 'G, R, A' → ['G', 'R', 'A'])."""
    if not text:
        return []
    # Split by comma, strip whitespace
    parts = [s.strip() for s in text.split(",")]
    return [p for p in parts if p]


# ---------------------------------------------------------------------------
# Table parsing
# ---------------------------------------------------------------------------

def parse_main_text_table(table, verse_range: tuple[int, int]) -> dict[int, Verse]:
    """
    Parse a main text table. Returns a dict of verse_number → Verse.
    Since we can't always determine exact verse boundaries within a table,
    we assign all content to the first verse in the range initially,
    then try to split on psalm citation patterns.
    """
    verses = {}
    for v in range(verse_range[0], verse_range[1] + 1):
        if v not in verses:
            verses[v] = Verse(number=v)

    # We'll collect everything into the range and assign to first verse
    # (refinement can split later based on psalm citation patterns)
    primary_verse = verse_range[0]
    current_verse = primary_verse

    num_cols = len(table.columns)

    for row_idx, row in enumerate(table.rows):
        if is_empty_row(row):
            continue

        if is_apparatus_row(row):
            source = parse_apparatus_row(row, num_cols)
            if source and current_verse in verses:
                verses[current_verse].sources.append(source)
            continue

        if is_gloss_row(row, num_cols):
            col0_text = get_cell_text(row.cells[0]).strip()
            # NHD translation from the translation column
            nhd_col_idx = _get_nhd_column(num_cols)
            nhd_text = get_cell_text(row.cells[nhd_col_idx]).strip() if nhd_col_idx < num_cols else ""

            gloss = Gloss(
                position=f"Table row {row_idx}",
                text=col0_text,
                translation_nhd=nhd_text,
            )
            if current_verse in verses:
                verses[current_verse].glosses.append(gloss)
            continue

        # Main text row
        # Column 0 has the colored text (columns 0-2 are merged/identical, read only 0)
        runs = extract_colored_runs(row.cells[0])
        sections = runs_to_sections(runs)

        # NHD translation from the appropriate column
        nhd_col_idx = _get_nhd_column(num_cols)
        nhd_text = ""
        if nhd_col_idx < num_cols:
            nhd_text = get_cell_text(row.cells[nhd_col_idx]).strip()

        # Sigles from last column
        sigles_text = get_cell_text(row.cells[-1]).strip()
        sigles = parse_sigles(sigles_text)

        # Check if a psalm citation matches a known verse start
        for sec in sections:
            if sec.type == "psalm_citation":
                detected_verse = _detect_verse_from_citation(sec.text)
                if detected_verse and detected_verse != current_verse:
                    if verse_range[0] <= detected_verse <= verse_range[1]:
                        current_verse = detected_verse
                        if current_verse not in verses:
                            verses[current_verse] = Verse(number=current_verse)

        # Assign nhd and sigles to each section
        for sec in sections:
            sec.translation_nhd = nhd_text
            sec.source_sigles = sigles

        if current_verse in verses:
            verses[current_verse].sections.extend(sections)

    return verses


def _detect_verse_from_citation(text: str) -> int | None:
    """
    Check if a psalm citation matches a known verse opening.
    Returns the verse number or None.
    """
    text_lower = text.strip().lower()
    for prefix, verse_num in PSALM_VERSE_STARTS.items():
        if text_lower.startswith(prefix):
            if verse_num == 0:  # Title, not a verse
                return None
            return verse_num
    return None


def _get_nhd_column(num_cols: int) -> int:
    """
    Get the column index for the NHD translation.
    In tables with 3 cols: col 1 is NHD
    In tables with 4 cols: col 2 is NHD (col 0-1 might be merged text)
    In tables with 5 cols: col 3 is NHD (cols 0-2 merged)
    In tables with 6 cols: col 3 is NHD (cols 0-2 merged, col 4-5 other)
    General rule: second-to-last column (last is sigles).
    """
    if num_cols <= 3:
        return 1
    else:
        return num_cols - 2


def parse_apparatus_row(row, num_cols: int) -> Source | None:
    """Parse a source apparatus row."""
    sigle = get_cell_text(row.cells[0]).strip()
    if sigle not in KNOWN_SIGLES:
        return None

    latin_text = ""
    german_translation = ""

    if num_cols >= 3:
        latin_text = get_cell_text(row.cells[1]).strip()
        german_translation = get_cell_text(row.cells[2]).strip()

    # For wider tables, German translation might be in a later column
    # (sometimes duplicated across cols 2+)
    if num_cols >= 4 and not german_translation:
        german_translation = get_cell_text(row.cells[2]).strip()

    return Source(
        sigle=sigle,
        name=SOURCE_NAMES.get(sigle, ""),
        latin_text=latin_text,
        german_translation=german_translation,
    )


# ---------------------------------------------------------------------------
# Psalm text comparison (Tables 11-12)
# ---------------------------------------------------------------------------

def parse_psalm_comparison(doc) -> dict:
    """Parse the synoptic psalm text comparison from Tables 11 and 12."""
    witnesses = []

    # Table 11 (index 10), rows 4-6: G, R, H header + full texts
    table11 = doc.tables[10]
    if len(table11.rows) >= 7:
        # Row 5 has the sigle headers: G, G, R, R, H
        # Row 6 has the full psalm texts
        header_row = table11.rows[5]
        text_row = table11.rows[6]

        # Extract unique witnesses from this table
        seen = set()
        for cell_idx, cell in enumerate(text_row.cells):
            text = get_cell_text(cell).strip()
            if not text:
                continue
            # Get sigle from header row
            sigle = get_cell_text(header_row.cells[cell_idx]).strip()
            if sigle and sigle not in seen:
                seen.add(sigle)
                manuscript = None
                if sigle == "H":
                    manuscript = "Staatsbibliothek Bamberg Ms. 44"
                witnesses.append({
                    "sigle": sigle,
                    "name": _witness_name(sigle),
                    "manuscript": manuscript,
                    "text": text,
                })

    # Table 12 (index 11): A-Psalter and C-Psalter
    table12 = doc.tables[11]
    if len(table12.rows) >= 2:
        header_row = table12.rows[0]
        text_row = table12.rows[1]

        for cell_idx, cell in enumerate(text_row.cells):
            text = get_cell_text(cell).strip()
            header = get_cell_text(header_row.cells[cell_idx]).strip()
            if not text:
                continue

            if "162" in header:  # A-Psalter, Cod. 162
                witnesses.append({
                    "sigle": "A_psalter",
                    "name": "Augustinus-Psalter",
                    "manuscript": "St. Gallen Cod. 162",
                    "text": text,
                })
            elif "200" in header:  # C-Psalter, Cod. 200
                witnesses.append({
                    "sigle": "C_psalter",
                    "name": "Cassiodor-Psalter",
                    "manuscript": "St. Gallen Cod. 200",
                    "text": text,
                })

    return {
        "description": "Synoptischer Vergleich der Psalmtext-Versionen",
        "witnesses": witnesses,
    }


def _witness_name(sigle: str) -> str:
    names = {
        "G": "Gallicanum",
        "R": "Romanum",
        "H": "Hebraicum (iuxta Hebraeos)",
    }
    return names.get(sigle, sigle)


# ---------------------------------------------------------------------------
# Wiener Notker (Table 13)
# ---------------------------------------------------------------------------

def parse_wiener_notker(doc) -> dict:
    """Parse the Wiener Notker parallel text from Table 13."""
    table13 = doc.tables[12]
    header = get_cell_text(table13.rows[0].cells[0]).strip() if table13.rows else ""
    text = get_cell_text(table13.rows[1].cells[0]).strip() if len(table13.rows) > 1 else ""

    return {
        "description": header,
        "manuscript": "ÖNB Cod. 2681",
        "edition": "Heinzle & Scherrer",
        "text": text,
    }


# ---------------------------------------------------------------------------
# Main assembly
# ---------------------------------------------------------------------------

def merge_verses(all_verses: dict[int, Verse]) -> list[dict]:
    """Convert verse dict to sorted list, merging duplicates."""
    result = []
    for num in sorted(all_verses.keys()):
        v = all_verses[num]
        result.append({
            "number": v.number,
            "sections": [asdict(s) for s in v.sections],
            "glosses": [asdict(g) for g in v.glosses],
            "sources": [asdict(s) for s in v.sources],
            "bible_references": v.bible_references,
        })
    return result


def main():
    print(f"Reading {DOCX_PATH}...")
    doc = Document(str(DOCX_PATH))
    print(f"  Found {len(doc.tables)} tables, {len(doc.paragraphs)} paragraphs")

    # Collect verses from all main text tables (0-10)
    all_verses: dict[int, Verse] = {}

    for table_idx, table in enumerate(doc.tables):
        vrange = VERSE_RANGES.get(table_idx)
        if vrange is None:
            continue  # Skip special tables (psalter comparison, Wiener Notker)

        print(f"  Parsing Table {table_idx + 1} (verses {vrange[0]}–{vrange[1]})...")
        table_verses = parse_main_text_table(table, vrange)

        # Merge into global verse collection
        for vnum, verse in table_verses.items():
            if vnum not in all_verses:
                all_verses[vnum] = verse
            else:
                # Append sections, glosses, sources to existing verse
                all_verses[vnum].sections.extend(verse.sections)
                all_verses[vnum].glosses.extend(verse.glosses)
                all_verses[vnum].sources.extend(verse.sources)

    # Parse special sections
    print("  Parsing psalm text comparison...")
    psalm_comparison = parse_psalm_comparison(doc)

    print("  Parsing Wiener Notker...")
    wiener_notker = parse_wiener_notker(doc)

    # Assemble final JSON
    output = {
        "psalm": 2,
        "metadata": {
            "title": "Psalm 2",
            "edition": "Tax/Sehrt (1970er)",
            "manuscript": "CSg 0021",
            "iiif_manifest": "https://www.e-codices.unifr.ch/metadata/iiif/csg-0021/manifest.json",
            "facsimile_start": "https://www.e-codices.unifr.ch/de/csg/0021/11/0/",
            "edition_pages": "R10–R13",
            "source_editions": {
                "quellenliste": "https://www.degruyterbrill.com/document/doi/10.1515/9783110935332/html",
                "edition": "https://www.degruyterbrill.com/document/doi/10.1515/9783110967500/html",
            },
        },
        "verses": merge_verses(all_verses),
        "psalm_text_comparison": psalm_comparison,
        "wiener_notker": wiener_notker,
    }

    # Statistics
    total_sections = sum(len(v["sections"]) for v in output["verses"])
    total_glosses = sum(len(v["glosses"]) for v in output["verses"])
    total_sources = sum(len(v["sources"]) for v in output["verses"])
    type_counts = {}
    for v in output["verses"]:
        for s in v["sections"]:
            type_counts[s["type"]] = type_counts.get(s["type"], 0) + 1

    print(f"\n  Results:")
    print(f"    Verses:   {len(output['verses'])}")
    print(f"    Sections: {total_sections} ({type_counts})")
    print(f"    Glosses:  {total_glosses}")
    print(f"    Sources:  {total_sources}")
    print(f"    Witnesses: {len(psalm_comparison['witnesses'])}")

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n  Written to {OUTPUT_PATH}")
    return output


if __name__ == "__main__":
    main()
