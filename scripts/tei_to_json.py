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


def rich_text_content(el) -> str:
    """Extrahiert Text mit <b>-Tags für <hi rend='bold'> Elemente.

    Nur <hi rend="bold"> wird erhalten, alle anderen Tags werden als
    reiner Text extrahiert. Ergebnis ist sicheres HTML (kein XSS-Risiko,
    da nur <b>-Tags erzeugt werden).
    """
    parts = []
    if el.text:
        parts.append(el.text)
    for child in el:
        local = etree.QName(child.tag).localname if isinstance(child.tag, str) else ''
        if local == 'hi' and child.get('rend') == 'bold':
            inner = text_content(child)
            parts.append(f'<b>{inner}</b>')
        else:
            # Rekursiv: <hi> kann in <quote> verschachtelt sein
            parts.append(rich_text_content(child))
        if child.tail:
            parts.append(child.tail)
    return ''.join(parts)


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


def parse_sigles(text: str) -> list[str]:
    """
    Parst Siglen-Text aus TEI <note type="sigle">.

    Unterstützt Formate wie:
      'G, R'          → ['G', 'R']
      'G [A, C]'      → ['G', 'A', 'C']
      'C,G,R,H'       → ['C', 'G', 'R', 'H']
      'G, A, C'       → ['G', 'A', 'C']

    Extrahiert alle bekannten Siglen-Muster (Großbuchstabe + optionaler
    Kleinbuchstabe oder II-Suffix) und ignoriert Klammern/Kommas.
    """
    return list(dict.fromkeys(re.findall(r'[A-Z][a-z]*(?:II)?(?:-psa)?', text)))


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
    Sammelt alle <seg>- und <gloss>-Elemente eines Vers-divs und führt
    verkettete Segmente zusammen. Glossen werden als type="gloss" Einträge
    an ihrer korrekten Position im Textfluss beibehalten.
    """
    # Phase 1: Alle Segmente sammeln (inkl. Glossen als Marker)
    raw_segments = []

    for ab in verse_div.findall(f'{{{TEI_NS}}}ab'):
        sigle_note = ab.find(f'{{{TEI_NS}}}note[@type="sigle"]')
        line_sigles = []
        if sigle_note is not None and sigle_note.text:
            line_sigles = parse_sigles(sigle_note.text)
        # Iteration 2 / US-9.2: Notker-Zeilennummer aus <ab n="X">.
        try:
            line_n = int(ab.get('n', '0'))
        except (TypeError, ValueError):
            line_n = 0

        if ab.get('ana') == '#fn-gloss':
            # Glosse als Marker in den Segment-Stream einfügen
            gloss_el = ab.find(f'{{{TEI_NS}}}gloss')
            nhd_note = ab.find(f'{{{TEI_NS}}}note[@type="translation_gloss"]')
            if gloss_el is not None:
                raw_segments.append({
                    'text': clean_text(text_content(gloss_el)),
                    'type': '_gloss',
                    'lang': get_lang(gloss_el),
                    'part': '',
                    'has_foreign': False,
                    'sigles': [],
                    'line_n': line_n,
                    '_gloss_nhd': clean_text(text_content(nhd_note)) if nhd_note is not None else '',
                    '_gloss_target': gloss_el.get('target', '').lstrip('#'),
                })
            continue

        for seg in ab.findall(f'{{{TEI_NS}}}seg'):
            raw_segments.append({
                'text': text_content(seg),
                'type': seg.get('type', ''),
                'lang': get_lang(seg),
                'part': seg.get('part', ''),
                'has_foreign': has_foreign(seg),
                'sigles': list(line_sigles),
                'line_n': line_n,
            })

    # Phase 2: Verkettete Segmente zusammenführen
    # @part="I" beginnt eine Kette, "M" setzt fort, "F" beendet.
    # Aufeinanderfolgende Segmente gleichen Typs mit I→M→...→F werden zusammengeführt.
    # Gloss-Marker (_gloss) werden unverändert durchgereicht.
    merged = []
    i = 0
    while i < len(raw_segments):
        seg = raw_segments[i]

        # Gloss-Marker direkt durchreichen (mit Schema-konformen Feldern)
        if seg['type'] == '_gloss':
            merged.append({
                'type': 'gloss',
                'text': seg['text'],
                'language': tei_lang_to_json_lang(seg.get('lang', 'goh'), False),
                'source_sigles': [],
                'line_n': seg.get('line_n', 0),
                'translation_nhd': seg.get('_gloss_nhd', ''),
                'relates_to': seg.get('_gloss_target', ''),
            })
            i += 1
            continue

        if seg['part'] == 'I':
            # Kette sammeln: I → (M →)* F
            chain_text = seg['text']
            chain_sigles = list(seg['sigles'])
            chain_has_foreign = seg['has_foreign']
            j = i + 1
            while j < len(raw_segments):
                nxt = raw_segments[j]
                # Gloss-Marker in Ketten überspringen (werden separat gehandhabt)
                if nxt['type'] == '_gloss':
                    j += 1
                    continue
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
                'line_n': seg.get('line_n', 0),
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
                    'line_n': seg.get('line_n', 0),
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
    # Gloss-Marker werden bei der Hyphen-Suche übersprungen, da Glossen
    # keine Wörter unterbrechen (z.B. "grís-" [Glosse] "cramoton")
    result = []
    for sec in merged:
        if sec['type'] == 'gloss':
            # Gloss-Marker temporär behalten für korrekte Hyphen-Logik
            result.append(sec)
            continue

        # Finde den letzten Nicht-Gloss-Eintrag für Hyphen-Merge
        prev = None
        for r in reversed(result):
            if r['type'] != 'gloss':
                prev = r
                break

        if (prev is not None
                and prev['type'] == sec['type']
                and prev['text'].endswith('-')):
            prev['text'] = merge_hyphenated(prev['text'], sec['text'])
            for s in sec['source_sigles']:
                if s not in prev['source_sigles']:
                    prev['source_sigles'].append(s)
        else:
            result.append(sec)

    # Phase 4: Disambiguierung der Sigles in Psalter-Zeugen vs. patristische
    # Quellen (R ist ambig: Romanum bei psalm_citation, sonst Remigius).
    for sec in result:
        psa, src = disambiguate_sigles(sec['type'], sec.get('source_sigles', []))
        sec['sigles_psalter'] = psa
        sec['sigles_sources'] = src

    # Gloss-Einträge bleiben in sections[] an ihrer korrekten Position
    # Die UI rendert type="gloss" Sections inline im Textfluss
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
    """Sammelt die nhd. Übersetzung eines Vers-divs als Fließtext."""
    nhd_note = verse_div.find(f'{{{TEI_NS}}}note[@type="translation_nhd"]')
    if nhd_note is None:
        return ''
    p = nhd_note.find(f'{{{TEI_NS}}}p')
    if p is not None:
        return clean_text(text_content(p))
    return clean_text(text_content(nhd_note))


PSALTER_SIGLES = {'G', 'H'}        # eindeutig Psalter-Zeugen
SOURCE_SIGLES = {'A', 'C', 'Br', 'RII', 'N'}  # eindeutig patristische Quellen
# 'R' ist ambig:
#   - in psalm_citation-Sections: R = Romanum-Psalter
#   - in commentary/translation/gloss-Sections: R = Remigius (patristic)


def disambiguate_sigles(section_type: str, sigles: list[str]) -> tuple[list[str], list[str]]:
    """Teilt eine Sigles-Liste in (psalter_sigles, source_sigles).

    Disambiguierung anhand des Section-Types fuer R (Romanum vs. Remigius).
    Fuer alle anderen Sigles ist die Zuordnung eindeutig.
    """
    psalter, sources = [], []
    for s in sigles:
        if s in PSALTER_SIGLES:
            psalter.append(s)
        elif s in SOURCE_SIGLES:
            sources.append(s)
        elif s == 'R':
            if section_type == 'psalm_citation':
                psalter.append(s)
            else:
                sources.append(s)
        else:
            sources.append(s)  # Unbekannte Sigle vorsichtshalber als Quelle
    return psalter, sources


def collect_nhd_lines(verse_div) -> list[str]:
    """Sammelt die zeilengetreue nhd. Übersetzung als Liste (Iteration 2 / US-9).

    Liest die <l>-Elemente unter <note type="translation_nhd"><lg type="line-faithful">.
    Fallback: leere Liste, wenn keine line-faithful-Daten vorhanden.
    """
    nhd_note = verse_div.find(f'{{{TEI_NS}}}note[@type="translation_nhd"]')
    if nhd_note is None:
        return []
    lg = nhd_note.find(f'{{{TEI_NS}}}lg[@type="line-faithful"]')
    if lg is None:
        return []
    return [clean_text(text_content(l)) for l in lg.findall(f'{{{TEI_NS}}}l') if text_content(l).strip()]


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
        latin = clean_text(rich_text_content(quote)) if quote is not None else ''
        # Iteration 2 / BUG-11.5: source language from quote's xml:lang.
        # Ermöglicht typografische Differenzierung im UI (kursiv fuer lat.,
        # aufrecht fuer ahd.).
        source_language = get_lang(quote) if quote is not None else 'la'

        tr_note = cit.find(f'{{{TEI_NS}}}note[@type="translation"]')
        german = clean_text(text_content(tr_note)) if tr_note is not None else ''

        sources.append({
            'sigle': sigle,
            'name': name,
            'latin_text': latin,
            'german_translation': german,
            'source_language': source_language or 'la',
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

    # Witness-Definitionen aus dem Header (<listWit> in <sourceDesc>)
    wit_names = {}
    for wit_el in tei_root.findall(f'.//{{{TEI_NS}}}listWit/{{{TEI_NS}}}witness'):
        wit_id = get_xml_id(wit_el)
        wit_names[f'#{wit_id}'] = text_content(wit_el).strip()

    # Sigle → voller Name + Handschrift
    sigle_info = {
        'G':     ('Gallicanum', None),
        'R':     ('Romanum', None),
        'H':     ('Hebraicum (iuxta Hebraeos)', 'Bamberg Ms. 44'),
        'A-psa': ('Augustinus-Psalter', 'St. Gallen Cod. 162'),
        'C-psa': ('Cassiodor-Psalter', 'St. Gallen Cod. 200'),
    }

    # Readings
    for rdg in comp_div.findall(f'.//{{{TEI_NS}}}rdg'):
        wit_ref = rdg.get('wit', '')
        sigle = wit_ref.replace('#wit-', '')
        info = sigle_info.get(sigle, (wit_names.get(wit_ref, sigle), None))

        witnesses.append({
            'sigle': sigle,
            'name': info[0],
            'manuscript': info[1],
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
# Cross-verse hyphenation fix
# ---------------------------------------------------------------------------

def fix_cross_verse_hyphens(verses: list[dict]):
    """
    Löst Silbentrennungen an Versgruppen-Grenzen auf.
    Wenn der letzte Section-Text eines Verses mit '-' endet und der
    nächste Vers (mit Daten) eine erste Section gleichen Typs hat,
    werden die Texte zusammengeführt.
    """
    real_verses = [v for v in verses if v.get('sections')]
    for i in range(len(real_verses) - 1):
        curr = real_verses[i]
        nxt = real_verses[i + 1]

        if not curr['sections'] or not nxt['sections']:
            continue

        last_sec = curr['sections'][-1]
        first_sec = nxt['sections'][0]

        if last_sec['text'].rstrip().endswith('-') and last_sec['type'] == first_sec['type']:
            # Merge: "han-" + "gta iz..." → "hangta iz..."
            merged = merge_hyphenated(last_sec['text'], first_sec['text'])
            last_sec['text'] = merged
            # Sigles zusammenführen
            for s in first_sec.get('source_sigles', []):
                if s not in last_sec.get('source_sigles', []):
                    last_sec.setdefault('source_sigles', []).append(s)
            # Erste Section des nächsten Verses entfernen
            nxt['sections'] = nxt['sections'][1:]


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
        nhd_lines = collect_nhd_lines(verse_div)
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
                    'translation_nhd_lines': nhd_lines,
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
                    'translation_nhd_lines': [],
                    'sources': [],
                })

    # Post-Processing: Silbentrennungen an Versgruppen-Grenzen auflösen
    # z.B. V1-2 endet "han-", V3-5 beginnt "gta iz" → "hangta iz"
    fix_cross_verse_hyphens(result['verses'])

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
