#!/usr/bin/env python3
"""
tei_to_json.py — TEI-XML → JSON für die Web-UI

Liest data/tei/psalm2.xml und erzeugt data/processed/psalm2.json
im Schema, das docs/index.html erwartet (Interface-Vertrag Z. 15–70).

Kernaufgabe: Zeilen-basierte TEI-Struktur (<ab>-Elemente) zu vers-basierten
JSON-Sections aggregieren. Verkettete Segmente (@part/@next/@prev) werden
zusammengeführt, Silbentrennungen aufgelöst.
"""

import json
import re
import sys
from pathlib import Path
from lxml import etree

TEI_NS = 'http://www.tei-c.org/ns/1.0'
XML_NS = 'http://www.w3.org/XML/1998/namespace'
NS = {'tei': TEI_NS}


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def text_content(el) -> str:
    """Extrahiert den gesamten Textinhalt eines Elements (inkl. Kinder)."""
    return ''.join(el.itertext())


def get_lang(el) -> str:
    """Liest xml:lang eines Elements."""
    return el.get(f'{{{XML_NS}}}lang', '')


def get_xml_id(el) -> str:
    """Liest xml:id eines Elements."""
    return el.get(f'{{{XML_NS}}}id', '')


def has_foreign(el) -> bool:
    """Prüft ob das Element <foreign>-Kinder hat."""
    return el.find(f'{{{TEI_NS}}}foreign') is not None


def tei_type_to_json_type(seg_type: str) -> str:
    """Mappt TEI seg@type auf JSON section.type."""
    return {
        'psalm': 'psalm_citation',
        'translation': 'translation',
        'commentary': 'commentary',
    }.get(seg_type, seg_type)


def tei_lang_to_json_lang(lang: str, has_foreign_spans: bool) -> str:
    """Mappt TEI xml:lang auf JSON section.language."""
    if has_foreign_spans:
        return 'ahd_lat_mixed'
    return {
        'la': 'lat',
        'goh': 'ahd',
        'de': 'de',
    }.get(lang, lang)


def clean_text(text: str) -> str:
    """Bereinigt Text: Whitespace normalisieren, Zeilenumbrüche entfernen."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def merge_hyphenated(text_a: str, text_b: str) -> str:
    """
    Führt zwei Texte zusammen, die durch Silbentrennung getrennt sind.
    'dâh-' + 'ton' → 'dâhton'
    'medi-' + 'tati' → 'meditati'
    Aber: 'lánt-chuninga' bleibt (Kompositum, kein Zeilenumbruch).
    """
    a = text_a.rstrip()
    if a.endswith('-'):
        return a[:-1] + text_b.lstrip()
    return a + ' ' + text_b.lstrip()


# ---------------------------------------------------------------------------
# Segment-Zusammenführung
# ---------------------------------------------------------------------------

def collect_segments(verse_div) -> list[dict]:
    """
    Sammelt alle <seg>-Elemente eines Vers-divs und führt verkettete
    Segmente zusammen. Gibt eine Liste von Section-Dicts zurück.
    """
    # Phase 1: Alle Segmente sammeln
    raw_segments = []

    for ab in verse_div.findall(f'{{{TEI_NS}}}ab'):
        sigle_note = ab.find(f'{{{TEI_NS}}}note[@type="sigle"]')
        line_sigles = []
        if sigle_note is not None and sigle_note.text:
            line_sigles = [s.strip() for s in sigle_note.text.split(',') if s.strip()]

        if ab.get('ana') == '#fn-gloss':
            continue

        for seg in ab.findall(f'{{{TEI_NS}}}seg'):
            raw_segments.append({
                'text': text_content(seg),
                'type': seg.get('type', ''),
                'lang': get_lang(seg),
                'part': seg.get('part', ''),
                'has_foreign': has_foreign(seg),
                'sigles': list(line_sigles),
            })

    # Phase 2: Verkettete Segmente zusammenführen
    # @part="I" beginnt eine Kette, "M" setzt fort, "F" beendet.
    # Aufeinanderfolgende Segmente gleichen Typs mit I→M→...→F werden zusammengeführt.
    merged = []
    i = 0
    while i < len(raw_segments):
        seg = raw_segments[i]

        if seg['part'] == 'I':
            # Kette sammeln: I → (M →)* F
            chain_text = seg['text']
            chain_sigles = list(seg['sigles'])
            chain_has_foreign = seg['has_foreign']
            j = i + 1
            while j < len(raw_segments):
                nxt = raw_segments[j]
                if nxt['type'] == seg['type'] and nxt['part'] in ('M', 'F'):
                    chain_text = merge_hyphenated(chain_text, nxt['text'])
                    chain_sigles.extend(nxt['sigles'])
                    chain_has_foreign = chain_has_foreign or nxt['has_foreign']
                    if nxt['part'] == 'F':
                        j += 1
                        break
                    j += 1
                else:
                    break  # Kette unterbrochen

            merged.append({
                'type': tei_type_to_json_type(seg['type']),
                'text': clean_text(chain_text),
                'language': tei_lang_to_json_lang(seg['lang'], chain_has_foreign),
                'source_sigles': list(dict.fromkeys(chain_sigles)),
            })
            i = j

        elif seg['part'] in ('', None):
            # Eigenständiges Segment
            text = clean_text(seg['text'])
            if text:
                merged.append({
                    'type': tei_type_to_json_type(seg['type']),
                    'text': text,
                    'language': tei_lang_to_json_lang(seg['lang'], seg['has_foreign']),
                    'source_sigles': list(seg['sigles']),
                })
            i += 1

        else:
            # Verwaiste M/F-Segmente (sollte nicht vorkommen)
            text = clean_text(seg['text'])
            if text:
                merged.append({
                    'type': tei_type_to_json_type(seg['type']),
                    'text': text,
                    'language': tei_lang_to_json_lang(seg['lang'], seg['has_foreign']),
                    'source_sigles': list(seg['sigles']),
                })
            i += 1

    # Phase 3: Unchained trailing hyphens zusammenführen
    # Wenn aufeinanderfolgende Sections gleichen Typs enden/beginnen mit Trennung
    result = []
    for sec in merged:
        if result and result[-1]['type'] == sec['type'] and result[-1]['text'].endswith('-'):
            result[-1]['text'] = merge_hyphenated(result[-1]['text'], sec['text'])
            for s in sec['source_sigles']:
                if s not in result[-1]['source_sigles']:
                    result[-1]['source_sigles'].append(s)
        else:
            result.append(sec)

    return result


def collect_glosses(verse_div) -> list[dict]:
    """Sammelt alle Glossen eines Vers-divs."""
    glosses = []
    for ab in verse_div.findall(f'{{{TEI_NS}}}ab'):
        if ab.get('ana') != '#fn-gloss':
            continue
        gloss_el = ab.find(f'{{{TEI_NS}}}gloss')
        nhd_note = ab.find(f'{{{TEI_NS}}}note[@type="translation_gloss"]')

        if gloss_el is not None:
            glosses.append({
                'text': clean_text(text_content(gloss_el)),
                'translation_nhd': clean_text(text_content(nhd_note)) if nhd_note is not None else '',
                'relates_to': gloss_el.get('target', '').lstrip('#'),
            })
    return glosses


def collect_nhd(verse_div) -> str:
    """Sammelt die nhd. Übersetzung eines Vers-divs."""
    nhd_note = verse_div.find(f'{{{TEI_NS}}}note[@type="translation_nhd"]')
    if nhd_note is not None:
        return clean_text(text_content(nhd_note))
    return ''


def collect_sources(verse_div) -> list[dict]:
    """Sammelt den Quellenapparat eines Vers-divs."""
    sources = []
    src_note = verse_div.find(f'{{{TEI_NS}}}note[@type="sources"]')
    if src_note is None:
        return sources

    sigle_to_name = {
        'src-A': ('A', 'Augustinus, Enarrationes in Psalmos'),
        'src-C': ('C', 'Cassiodor, Expositio Psalmorum'),
        'src-R': ('R', 'Remigius'),
        'src-Br': ('Br', 'Breviarium'),
        'src-RII': ('RII', 'RII (ungeklärt)'),
        'src-N': ('N', 'N (ungeklärt)'),
    }

    for cit in src_note.findall(f'{{{TEI_NS}}}cit'):
        ana = cit.get('ana', '').lstrip('#')
        sigle, name = sigle_to_name.get(ana, (ana, ana))

        quote = cit.find(f'{{{TEI_NS}}}quote')
        latin = clean_text(text_content(quote)) if quote is not None else ''

        tr_note = cit.find(f'{{{TEI_NS}}}note[@type="translation"]')
        german = clean_text(text_content(tr_note)) if tr_note is not None else ''

        sources.append({
            'sigle': sigle,
            'name': name,
            'latin_text': latin,
            'german_translation': german,
        })

    return sources


# ---------------------------------------------------------------------------
# Psaltervergleich & Wiener Notker
# ---------------------------------------------------------------------------

def collect_psalm_comparison(tei_root) -> dict:
    """Sammelt den synoptischen Psaltervergleich."""
    comp_div = tei_root.find(f'.//{{{TEI_NS}}}div[@type="psalm_comparison"]')
    if comp_div is None:
        return {'witnesses': []}

    witnesses = []
    # Witness-Liste
    wit_names = {}
    for wit_el in comp_div.findall(f'.//{{{TEI_NS}}}witness'):
        wit_id = get_xml_id(wit_el)
        wit_names[f'#{wit_id}'] = text_content(wit_el).strip()

    # Readings
    for rdg in comp_div.findall(f'.//{{{TEI_NS}}}rdg'):
        wit_ref = rdg.get('wit', '')
        sigle = wit_ref.replace('#wit-', '').replace('-full', '')
        name = wit_names.get(wit_ref, sigle)

        # Manuscript aus den Witness-Namen extrahieren
        manuscript = None
        if 'Bamberg' in name:
            manuscript = 'Bamberg Ms. 44'
        elif 'Cod. 162' in name:
            manuscript = 'St. Gallen Cod. 162'
        elif 'Cod. 200' in name:
            manuscript = 'St. Gallen Cod. 200'

        witnesses.append({
            'sigle': sigle,
            'name': name,
            'manuscript': manuscript,
            'text': clean_text(text_content(rdg)),
        })

    return {'witnesses': witnesses}


def collect_wiener_notker(tei_root) -> dict:
    """Sammelt den Wiener Notker."""
    wn_div = tei_root.find(f'.//{{{TEI_NS}}}div[@type="parallel_tradition"]')
    if wn_div is None:
        return {'manuscript': '', 'edition': '', 'text': ''}

    ab = wn_div.find(f'{{{TEI_NS}}}ab')
    text = clean_text(text_content(ab)) if ab is not None else ''

    return {
        'manuscript': 'ÖNB Cod. 2681',
        'edition': 'Heinzle & Scherrer',
        'text': text,
    }


# ---------------------------------------------------------------------------
# Hauptfunktion
# ---------------------------------------------------------------------------

def tei_to_json(tei_path: str) -> dict:
    """Konvertiert TEI-XML in das JSON-Schema für die Web-UI."""
    tree = etree.parse(tei_path)
    root = tree.getroot()

    # Metadata
    result = {
        'psalm': 2,
        'metadata': {
            'title': 'Psalm 2',
            'edition': 'Tax/Sehrt (1970er)',
            'manuscript': 'CSg 0021',
            'iiif_manifest': 'https://www.e-codices.unifr.ch/metadata/iiif/csg-0021/manifest.json',
            'facsimile_start_canvas': 'https://www.e-codices.unifr.ch/metadata/iiif/csg-0021/canvas/csg-0021_011.json',
            'edition_pages': 'R10–R13',
        },
        'verses': [],
        'psalm_text_comparison': collect_psalm_comparison(root),
        'wiener_notker': collect_wiener_notker(root),
    }

    # Verse
    verse_page_map = {
        '1': 'R10', '2': 'R10', '3': 'R10', '4': 'R11',
        '5': 'R11', '6': 'R11', '7': 'R12', '8': 'R12',
        '9': 'R12', '10': 'R13', '11': 'R13', '12': 'R13', '13': 'R13',
    }

    for verse_div in root.findall(f'.//{{{TEI_NS}}}div[@type="verse"]'):
        verse_n = verse_div.get('n', '')

        # Versgruppen wie "1-2" → einzelne Verse auflösen
        if '-' in verse_n:
            start, end = verse_n.split('-')
            verse_numbers = list(range(int(start), int(end) + 1))
        else:
            verse_numbers = [int(verse_n)]

        sections = collect_segments(verse_div)
        glosses = collect_glosses(verse_div)
        nhd = collect_nhd(verse_div)
        sources = collect_sources(verse_div)

        # Für Versgruppen: alle Daten unter der ersten Versnummer,
        # zusätzliche Versnummern als leere Einträge
        for i, vn in enumerate(verse_numbers):
            if i == 0:
                result['verses'].append({
                    'number': vn,
                    'edition_page': verse_page_map.get(str(vn), ''),
                    'sections': sections,
                    'glosses': glosses,
                    'translation_nhd': nhd,
                    'sources': sources,
                })
            else:
                # Zusätzliche Verse in der Gruppe: Verweis auf Hauptvers
                result['verses'].append({
                    'number': vn,
                    'included_in': verse_numbers[0],
                    'edition_page': verse_page_map.get(str(vn), ''),
                    'sections': [],
                    'glosses': [],
                    'translation_nhd': '',
                    'sources': [],
                })

    # Vers 13 fehlt in der DOCX-Versstruktur (Probeseite hat nur "2,12" als
    # Überschrift, aber der Text deckt Verse 12 und 13 ab). Vers 13 ergänzen.
    existing_numbers = {v['number'] for v in result['verses']}
    if 13 not in existing_numbers:
        result['verses'].append({
            'number': 13,
            'included_in': 12,
            'edition_page': verse_page_map.get('13', ''),
            'sections': [],
            'glosses': [],
            'translation_nhd': '',
            'sources': [],
        })

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    tei_path = Path(__file__).parent.parent / 'data' / 'tei' / 'psalm2.xml'
    output_path = Path(__file__).parent.parent / 'data' / 'processed' / 'psalm2.json'

    if not tei_path.exists():
        print(f'FEHLER: {tei_path} nicht gefunden')
        sys.exit(1)

    print(f'Lese TEI: {tei_path}')
    result = tei_to_json(str(tei_path))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f'JSON geschrieben: {output_path}')
    print(f'  Verse: {len(result["verses"])}')
    total_sections = sum(len(v["sections"]) for v in result["verses"])
    total_glosses = sum(len(v["glosses"]) for v in result["verses"])
    total_sources = sum(len(v["sources"]) for v in result["verses"])
    print(f'  Sections: {total_sections}')
    print(f'  Glossen: {total_glosses}')
    print(f'  Quellen: {total_sources}')
    print(f'  Psalter-Zeugen: {len(result["psalm_text_comparison"]["witnesses"])}')
    print(f'  Wiener Notker: {len(result["wiener_notker"]["text"])} Zeichen')


if __name__ == '__main__':
    main()
