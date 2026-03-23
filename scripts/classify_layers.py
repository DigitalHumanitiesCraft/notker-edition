#!/usr/bin/env python3
"""
classify_layers.py — Schichtenklassifikation und Anreicherung

Nimmt das Zwischenformat von parse_probeseite.py und reichert es an:
- Glossen-Validierung
- Zeilenübergreifende Segment-Verkettung (@part/@next/@prev)
- Sprachwechsel-Annotation (regelbasiert, LLM-Stub für Kommentar)
"""

import re
from dataclasses import dataclass, field
from typing import Optional

from parse_probeseite import (
    PsalmData, VerseGroup, TextLine, GlossLine, Segment
)


# ---------------------------------------------------------------------------
# Enriched Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ForeignSpan:
    """Ein Sprachwechsel innerhalb eines Segments."""
    start: int       # Zeichenposition im Segment-Text
    end: int
    lang: str        # 'la' oder 'goh'
    text: str


@dataclass
class EnrichedSegment:
    """Ein angereichertes Segment mit Sprachwechsel und Verkettung."""
    text: str
    function: str         # 'psalm', 'translation', 'commentary'
    lang: str             # Default-Sprache: 'la' oder 'goh'
    foreign_spans: list = field(default_factory=list)  # List[ForeignSpan]
    # Zeilenübergreifende Verkettung
    xml_id: Optional[str] = None
    part: Optional[str] = None    # 'I', 'M', 'F'
    next_id: Optional[str] = None
    prev_id: Optional[str] = None
    # Original-Segment für Rückverfolgung
    original: Optional[Segment] = None


@dataclass
class EnrichedLine:
    """Eine angereicherte Textzeile."""
    segments: list       # List[EnrichedSegment]
    nhd: str = ''
    sigles: str = ''
    line_number: int = 0
    is_gloss: bool = False
    gloss_text: str = ''
    gloss_nhd: str = ''


@dataclass
class EnrichedVerseGroup:
    """Eine angereicherte Versgruppe."""
    verses: str
    verse_numbers: list
    lines: list = field(default_factory=list)   # List[EnrichedLine]
    sources: list = field(default_factory=list)  # unverändert von parse_probeseite


# ---------------------------------------------------------------------------
# Sprachwechsel-Erkennung (regelbasiert)
# ---------------------------------------------------------------------------

# Einfaches ahd. Wörterbuch (häufige Funktionswörter und Formen)
AHD_MARKERS = {
    'ziu', 'unde', 'daz', 'diu', 'der', 'die', 'des', 'den', 'dem',
    'ist', 'sint', 'uuas', 'uuâren', 'uuolta', 'neist',
    'nube', 'nals', 'noh', 'ioh', 'ába', 'ána', 'fóne', 'umbe',
    'sih', 'ín', 'ír', 'ímo', 'sie', 'er', 'iz', 'mír', 'tir',
    'mit', 'ze', 'in', 'an', 'uber', 'uuider',
    'chît', 'hêizzet', 'stât', 'kân', 'mag', 'sol', 'tûe',
    'pedíu', 'pedîu', 'uuánda', 'uuanda', 'samoso',
    'góte', 'got', 'gotes', 'christvs',
    'so', 'al', 'al', 'dâr', 'tanne', 'denne',
    'nehéue', 'ne-lâzen', 'ne-mag',
}

# Lateinische Marker (Funktionswörter, Konjunktionen)
LAT_MARKERS = {
    'idest', 'id', 'est', 'et', 'in', 'non', 'sed', 'quia', 'quod',
    'qui', 'quae', 'cum', 'ad', 'de', 'ex', 'per', 'pro', 'super',
    'dominus', 'dominum', 'domini', 'deus', 'dei', 'deo',
    'christum', 'christi', 'christo',
    'ecclesiam', 'ecclesia', 'ȩcclesiam', 'ȩcclesia',
    'iudicio', 'retributio', 'peccatorum',
    'prȩdistinationem', 'prȩteritum', 'futurum',
    'euangelium', 'religionem', 'christianam',
    'specula', 'latine',
    'meditantes', 'inania', 'sine', 'tempore',
    'passione', 'reges', 'principes', 'sacerdotum',
    'vincula', 'iugum', 'uindicta',
    'terrenas', 'concupiscentias',
    'ictu', 'oculi',
}


def classify_language(word: str) -> Optional[str]:
    """
    Klassifiziert ein einzelnes Wort als 'la' oder 'goh'.
    Gibt None zurück wenn unsicher.
    """
    clean = word.lower().strip('.,;:!?()[]')
    if not clean:
        return None

    if clean in AHD_MARKERS:
        return 'goh'
    if clean in LAT_MARKERS:
        return 'la'

    # Heuristiken basierend auf Morphologie
    # Ahd. Akzentzeichen (á, é, í, ó, ú, â, ê, î, ô, û)
    if re.search(r'[áéíóúâêîôû]', clean):
        return 'goh'

    # Ahd. typische Endungen
    if re.search(r'(ent|ont|ost|est|ota|oton|aht|eht|iht)$', clean):
        return 'goh'

    # Ahd. typische Anfänge (uu = w)
    if clean.startswith('uu') or clean.startswith('ch'):
        return 'goh'

    # Lat. typische Endungen
    if re.search(r'(orum|arum|ibus|orum|tion|ment|alis|ilis|atus|itus)$', clean):
        return 'la'

    # Lat. typische Endungen (kürzere)
    if re.search(r'(um|us|is|em|am|ae|os|as)$', clean) and len(clean) > 3:
        return 'la'

    return None


def detect_foreign_spans(text: str, default_lang: str) -> list[ForeignSpan]:
    """
    Erkennt Sprachwechsel innerhalb eines Textsegments.
    Regelbasiert für häufige Fälle, markiert unsichere Stellen.

    Psalmzitate (default_lang='la') erhalten keine <foreign>-Annotation,
    da sie per Definition rein lateinisch sind.
    """
    # Psalmzitate sind rein lateinisch — kein Sprachwechsel nötig
    if default_lang == 'la':
        return []

    words = re.findall(r'\S+', text)
    if not words:
        return []

    spans = []
    current_lang = default_lang
    current_start = 0
    foreign_start = None

    for word in words:
        word_start = text.find(word, current_start)
        word_end = word_start + len(word)
        lang = classify_language(word)

        if lang and lang != default_lang:
            # Fremdsprachiges Wort gefunden
            if foreign_start is None:
                foreign_start = word_start
            foreign_end = word_end
        else:
            # Zurück zur Default-Sprache oder unsicher
            if foreign_start is not None:
                # Foreign-Span abschließen
                span_text = text[foreign_start:foreign_end].strip()
                if span_text:
                    other_lang = 'la' if default_lang == 'goh' else 'goh'
                    spans.append(ForeignSpan(
                        start=foreign_start,
                        end=foreign_end,
                        lang=other_lang,
                        text=span_text,
                    ))
                foreign_start = None

        current_start = word_end

    # Offenen Span am Ende abschließen
    if foreign_start is not None:
        span_text = text[foreign_start:foreign_end].strip()
        if span_text:
            other_lang = 'la' if default_lang == 'goh' else 'goh'
            spans.append(ForeignSpan(
                start=foreign_start,
                end=foreign_end,
                lang=other_lang,
                text=span_text,
            ))

    return spans


# ---------------------------------------------------------------------------
# Segment-Verkettung (@part/@next/@prev)
# ---------------------------------------------------------------------------

def detect_line_continuations(lines: list[EnrichedLine], verse_id: str):
    """
    Erkennt zeilenübergreifende Segmente und setzt @part/@next/@prev.
    Ein Segment geht über die Zeile hinaus, wenn:
    - Es am Zeilenende mit Bindestrich (Silbentrennung) oder
      ohne Satzzeichen endet
    - Die nächste Zeile mit einem Segment gleichen Typs beginnt
    """
    seg_counter = 0

    for i in range(len(lines) - 1):
        line = lines[i]
        next_line = lines[i + 1]

        if line.is_gloss or next_line.is_gloss:
            continue
        if not line.segments or not next_line.segments:
            continue

        last_seg = line.segments[-1]
        first_seg = next_line.segments[0]

        # Prüfe ob letztes Segment der Zeile → erstes Segment der nächsten Zeile
        # gleichen Typ hat (Fortsetzung)
        if last_seg.function == first_seg.function:
            text = last_seg.text.rstrip()
            # Silbentrennung am Zeilenende
            ends_with_hyphen = text.endswith('-')
            # Oder: Text endet ohne Satzschlusszeichen
            ends_mid_sentence = not text.endswith(('.', '?', '!'))

            if ends_with_hyphen or ends_mid_sentence:
                seg_counter += 1
                # IDs vergeben
                id_a = f'{verse_id}-seg{seg_counter}a'
                id_b = f'{verse_id}-seg{seg_counter}b'

                if last_seg.part is None:
                    # Neues Kettensegment beginnen
                    last_seg.part = 'I'
                    last_seg.xml_id = id_a
                    last_seg.next_id = id_b
                else:
                    # Bereits Teil einer Kette → erweitern
                    last_seg.part = 'M'
                    last_seg.next_id = id_b

                first_seg.part = 'F'
                first_seg.xml_id = id_b
                first_seg.prev_id = last_seg.xml_id


# ---------------------------------------------------------------------------
# Hauptfunktion
# ---------------------------------------------------------------------------

def classify_and_enrich(psalm: PsalmData) -> list[EnrichedVerseGroup]:
    """Reichert das geparste Zwischenformat an."""
    enriched_groups = []

    for vg in psalm.verse_groups:
        enriched_lines = []

        for line in vg.lines:
            if isinstance(line, GlossLine):
                enriched_lines.append(EnrichedLine(
                    segments=[],
                    nhd=line.nhd,
                    sigles=line.sigles,
                    line_number=line.line_number,
                    is_gloss=True,
                    gloss_text=line.text,
                    gloss_nhd=line.nhd,
                ))
            elif isinstance(line, TextLine):
                enriched_segs = []
                for seg in line.segments:
                    # Default-Sprache aus Funktion ableiten
                    if seg.function == 'psalm':
                        default_lang = 'la'
                    elif seg.function == 'translation':
                        default_lang = 'goh'
                    else:  # commentary
                        default_lang = 'goh'  # Ahd. ist häufiger im Kommentar

                    # Sprachwechsel erkennen
                    foreign = detect_foreign_spans(seg.text, default_lang)

                    enriched_segs.append(EnrichedSegment(
                        text=seg.text,
                        function=seg.function,
                        lang=default_lang,
                        foreign_spans=foreign,
                        original=seg,
                    ))

                enriched_lines.append(EnrichedLine(
                    segments=enriched_segs,
                    nhd=line.nhd,
                    sigles=line.sigles,
                    line_number=line.line_number,
                ))

        # Segment-Verkettung
        verse_id = f'v{vg.verses.replace("-", "_")}'
        detect_line_continuations(enriched_lines, verse_id)

        enriched_groups.append(EnrichedVerseGroup(
            verses=vg.verses,
            verse_numbers=vg.verse_numbers,
            lines=enriched_lines,
            sources=vg.sources,
        ))

    return enriched_groups


# ---------------------------------------------------------------------------
# Debug-Ausgabe
# ---------------------------------------------------------------------------

def print_enriched(groups: list[EnrichedVerseGroup]):
    """Debug-Ausgabe der angereicherten Daten."""
    for vg in groups:
        print(f'\n--- Verse {vg.verses} ---')
        for line in vg.lines:
            if line.is_gloss:
                print(f'  G{line.line_number}: "{line.gloss_text}" → "{line.gloss_nhd}"')
                continue

            for seg in line.segments:
                part_info = ''
                if seg.part:
                    part_info = f' @part={seg.part}'
                    if seg.next_id:
                        part_info += f' →{seg.next_id}'
                    if seg.prev_id:
                        part_info += f' ←{seg.prev_id}'

                foreign_info = ''
                if seg.foreign_spans:
                    foreign_info = ' FOREIGN: ' + ', '.join(
                        f'[{fs.lang}]{fs.text}' for fs in seg.foreign_spans
                    )

                text_preview = seg.text[:60]
                print(f'  L{line.line_number} [{seg.function}/{seg.lang}]'
                      f'{part_info}: {text_preview}{foreign_info}')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    from parse_probeseite import parse_probeseite
    from pathlib import Path

    docx_path = Path(__file__).parent.parent / 'data' / 'Probeseite_Notker.docx'
    psalm = parse_probeseite(str(docx_path))
    enriched = classify_and_enrich(psalm)
    print_enriched(enriched)
    return enriched


if __name__ == '__main__':
    main()
