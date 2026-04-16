#!/usr/bin/env python3
"""
build_tei.py — Zwischenformat → TEI-XML

Generiert ein sauberes, publikationsfähiges TEI-XML aus dem angereicherten
Zwischenformat von classify_layers.py.
"""

import sys
from pathlib import Path

from lxml import etree

from parse_probeseite import parse_probeseite, PsalmData, SourceEntry, apply_corrections
from classify_layers import (
    classify_and_enrich, EnrichedVerseGroup, EnrichedLine, EnrichedSegment
)


# ---------------------------------------------------------------------------
# Namespaces
# ---------------------------------------------------------------------------

TEI_NS = 'http://www.tei-c.org/ns/1.0'
XML_NS = 'http://www.w3.org/XML/1998/namespace'
NSMAP = {None: TEI_NS, 'xml': XML_NS}


def E(tag, **attrib):
    """Erstellt ein TEI-Element."""
    return etree.Element(f'{{{TEI_NS}}}{tag}', nsmap=NSMAP, **attrib)


def SE(parent, tag, **attrib):
    """Erstellt ein TEI-Subelement."""
    return etree.SubElement(parent, f'{{{TEI_NS}}}{tag}', **attrib)


def set_xml_attr(el, attr, val):
    """Setzt ein xml:-Attribut (z.B. xml:lang, xml:id)."""
    el.set(f'{{{XML_NS}}}{attr}', val)


# ---------------------------------------------------------------------------
# TEI-Header
# ---------------------------------------------------------------------------

def build_header():
    """Erstellt den vollständigen teiHeader."""
    header = E('teiHeader')

    # fileDesc
    fd = SE(header, 'fileDesc')

    # titleStmt
    ts = SE(fd, 'titleStmt')
    title = SE(ts, 'title')
    title.text = 'Notkers Psalmenkommentar – Psalm 2 (Digitale Edition, Prototyp)'
    author = SE(ts, 'author')
    author.text = 'Notker III. von St. Gallen (ca. 950–1022)'
    editor = SE(ts, 'editor')
    set_xml_attr(editor, 'id', 'pfeifer')
    editor.text = 'Philipp Pfeifer'
    resp = SE(ts, 'respStmt')
    resp_el = SE(resp, 'resp')
    resp_el.text = 'Digitale Aufbereitung'
    org = SE(resp, 'orgName')
    org.text = 'Digital Humanities Craft OG'

    # publicationStmt — TEI erfordert <authority> oder <publisher> vor <availability>
    ps = SE(fd, 'publicationStmt')
    SE(ps, 'authority').text = 'Digital Humanities Craft OG'
    avail = SE(ps, 'availability')
    lic = SE(avail, 'licence', target='https://creativecommons.org/licenses/by-nc-sa/4.0/')
    lic.text = 'CC-BY-NC-SA 4.0'

    # sourceDesc
    sd = SE(fd, 'sourceDesc')

    # Handschrift
    ms = SE(sd, 'msDesc')
    set_xml_attr(ms, 'id', 'csg0021')
    msid = SE(ms, 'msIdentifier')
    SE(msid, 'settlement').text = 'St. Gallen'
    SE(msid, 'repository').text = 'Stiftsbibliothek'
    SE(msid, 'idno').text = 'CSg 0021'

    # Bibliographien
    bib1 = SE(sd, 'bibl')
    set_xml_attr(bib1, 'id', 'tax_sehrt')
    bib1.text = 'Tax, Petrus W. / Sehrt, Edward H.: Notker der Deutsche – Der Psalter (1979), S. R10–R13'

    bib2 = SE(sd, 'bibl')
    set_xml_attr(bib2, 'id', 'wiener_notker')
    bib2.text = 'Wiener Notker: ÖNB Cod. 2681, Edition Heinzle & Scherrer'

    bib3 = SE(sd, 'bibl')
    set_xml_attr(bib3, 'id', 'rea_corpus')
    bib3.text = 'Referenzkorpus Altdeutsch (DDD), DOI: 10.34644/laudatio-dev-MiXVDnMB7CArCQ9CABmW'

    # Fix 4: <listWit> für Psalter-Zeugen und <listBibl> für Kommentarquellen
    # TEI P5 Kap. 13: Textzeugen gehören als <listWit> in <sourceDesc>
    lw = SE(sd, 'listWit')
    SE(lw, 'head').text = 'Psalter-Textzeugen (synoptischer Vergleich)'
    for wit_id, desc in [
        ('wit-G', 'Gallicanum'),
        ('wit-R', 'Romanum'),
        ('wit-H', 'Hebraicum (iuxta Hebraeos), Staatsbibliothek Bamberg Ms. 44'),
        ('wit-A-psa', 'Augustinus-Psalter, St. Gallen Cod. 162'),
        ('wit-C-psa', 'Cassiodor-Psalter, St. Gallen Cod. 200'),
    ]:
        wit = SE(lw, 'witness')
        set_xml_attr(wit, 'id', wit_id)
        wit.text = desc

    # Kommentarquellen als <listBibl> (Werke, nicht Textzeugen)
    lb = SE(sd, 'listBibl')
    SE(lb, 'head').text = 'Kommentarquellen (Notkers Vorlagen)'
    for bib_id, author, title, cert in [
        ('src-A', 'Augustinus', 'Enarrationes in Psalmos', None),
        ('src-C', 'Cassiodor', 'Expositio Psalmorum', None),
        ('src-R', 'Remigius', None, None),
        ('src-Br', None, 'Breviarium', None),
        ('src-RII', None, 'RII', 'low'),
        ('src-N', None, 'N', 'low'),
    ]:
        bibl = SE(lb, 'bibl')
        set_xml_attr(bibl, 'id', bib_id)
        if cert:
            bibl.set('cert', cert)
        if author:
            SE(bibl, 'author').text = author
        if title:
            SE(bibl, 'title').text = title

    # encodingDesc
    enc = SE(header, 'encodingDesc')

    # Fix 5: <variantEncoding> — TEI P5 fordert dies bei <app>/<rdg>-Verwendung
    SE(enc, 'variantEncoding', method='parallel-segmentation', location='internal')

    cd = SE(enc, 'classDecl')

    # Taxonomy: Textfunktionen
    tax_fn = SE(cd, 'taxonomy')
    set_xml_attr(tax_fn, 'id', 'textfunction')
    for cat_id, desc in [
        ('fn-psalm', 'Psalmzitation: Lateinischer Vulgata-Text, wie Notker ihn zitiert'),
        ('fn-transl', 'Übersetzung: Althochdeutsche Wiedergabe der Psalmzitate'),
        ('fn-comm', 'Kommentar: Notkers Exegese (ahd. und lat. gemischt)'),
        ('fn-gloss', 'Interlinearglosse: Einzelwort- oder Kurzübersetzung'),
    ]:
        cat = SE(tax_fn, 'category')
        set_xml_attr(cat, 'id', cat_id)
        SE(cat, 'catDesc').text = desc

    # editorialDecl > segmentation — TEI P5: <segmentation> ist Kind von <editorialDecl>
    ed = SE(enc, 'editorialDecl')
    segmentation = SE(ed, 'segmentation')
    SE(segmentation, 'p').text = (
        'Der Text ist in funktionale Schichten segmentiert, '
        'die auf der Farbcodierung der handschriftlichen Vorlage und der Probeseite basieren. '
        'Drei Schichttypen: Psalmzitation (lateinischer Vulgata-Text, wie Notker ihn zitiert), '
        'Übersetzung (althochdeutsche Wiedergabe der Psalmzitate) und '
        'Kommentar (Notkers Exegese, ahd. und lat. gemischt). '
        'Interlinearglossen bilden einen vierten Annotationstyp. '
        'Die Segmentierung folgt dem Farbwechsel auf Run-Ebene im DOCX der Probeseite: '
        'olive (#806000) = Psalmzitation, grün (#00B050) = Übersetzung, schwarz = Kommentar.'
    )

    # projectDesc
    pd = SE(enc, 'projectDesc')
    SE(pd, 'p').text = ('Prototyp für einen Drittmittelantrag. '
                        'Nur Psalm 2 (13 Verse). '
                        'Auftraggeber: Dr. Philipp Pfeifer, Universität Graz.')

    # profileDesc
    prof = SE(header, 'profileDesc')
    lu = SE(prof, 'langUsage')
    for ident, name in [('goh', 'Althochdeutsch'), ('la', 'Latein'),
                        ('de', 'Neuhochdeutsch')]:
        lang = SE(lu, 'language', ident=ident)
        lang.text = name

    return header


# ---------------------------------------------------------------------------
# Facsimile
# ---------------------------------------------------------------------------

def build_facsimile():
    """Erstellt das facsimile-Element mit IIIF-Referenzen."""
    facs = E('facsimile')
    # Seite 11 = Beginn Psalm 2 (von Philipp bestätigt)
    surf = SE(facs, 'surface')
    set_xml_attr(surf, 'id', 'facs-p11')
    surf.set('source', 'https://www.e-codices.unifr.ch/de/csg/0021/11/0/')
    graphic = SE(surf, 'graphic',
                 url='https://www.e-codices.unifr.ch/loris/csg/csg-0021/csg-0021_011.jp2/full/max/0/default.jpg')
    return facs


# ---------------------------------------------------------------------------
# Text-Body: Verse
# ---------------------------------------------------------------------------

FUNCTION_TO_ANA = {
    'psalm': '#fn-psalm',
    'translation': '#fn-transl',
    'commentary': '#fn-comm',
}


def build_mixed_content(parent_el, text: str, spans: list, make_element):
    """
    Generische Mixed-Content-Erzeugung: Text mit Inline-Elementen.

    Args:
        parent_el: Das übergeordnete XML-Element
        text: Der Gesamttext
        spans: Liste von (start, end, data)-Tupeln, sortiert nach Position
        make_element: Callable(parent, data) → erzeugt das Inline-Element und gibt es zurück
    """
    if not spans:
        parent_el.text = text
        return

    pos = 0
    last_el = None
    for start, end, data in sorted(spans, key=lambda s: s[0]):
        if start >= len(text) or end > len(text):
            continue

        pre_text = text[pos:start]
        if last_el is None:
            parent_el.text = (parent_el.text or '') + pre_text
        else:
            last_el.tail = (last_el.tail or '') + pre_text

        inline_el = make_element(parent_el, data)
        inline_el.text = text[start:end]
        last_el = inline_el
        pos = end

    if pos < len(text):
        if last_el is not None:
            last_el.tail = (last_el.tail or '') + text[pos:]
        else:
            parent_el.text = (parent_el.text or '') + text[pos:]


def build_text_with_foreign(parent_el, seg: EnrichedSegment):
    """Baut Text mit <foreign>-Elementen für Sprachwechsel."""
    def make_foreign(parent, span_data):
        el = SE(parent, 'foreign')
        set_xml_attr(el, 'lang', span_data.lang)
        return el

    spans = [(s.start, s.end, s) for s in seg.foreign_spans]
    build_mixed_content(parent_el, seg.text, spans, make_foreign)


def build_verse_div(vg: EnrichedVerseGroup, parent):
    """Erstellt ein <div type="verse"> für eine Versgruppe."""
    div = SE(parent, 'div', type='verse')
    div.set('n', vg.verses)

    # Textzeilen
    for line in vg.lines:
        if line.is_gloss:
            # <ab ana="#fn-gloss">
            ab = SE(div, 'ab')
            ab.set('ana', '#fn-gloss')
            ab.set('n', str(line.line_number))
            gloss = SE(ab, 'gloss')
            set_xml_attr(gloss, 'lang', 'goh')
            gloss.text = line.gloss_text
            if line.gloss_nhd:
                note = SE(ab, 'note', type='translation_gloss')
                set_xml_attr(note, 'lang', 'de')
                note.text = line.gloss_nhd
        else:
            # <ab> mit <seg>-Elementen
            ab = SE(div, 'ab')
            ab.set('n', str(line.line_number))

            for seg in line.segments:
                # Leere Segmente überspringen
                if not seg.text.strip():
                    continue

                seg_el = SE(ab, 'seg')
                seg_el.set('type', seg.function)
                seg_el.set('ana', FUNCTION_TO_ANA.get(seg.function, '#fn-comm'))
                set_xml_attr(seg_el, 'lang', seg.lang)

                # Fix 2: Nur @part (I/M/F) für Verkettung, nicht @next/@prev
                # TEI P5: Beide Methoden sind äquivalent, @part ist kompakter
                if seg.part:
                    seg_el.set('part', seg.part)

                # Text mit <foreign>-Spans
                build_text_with_foreign(seg_el, seg)

                # <lb break="no"/> am Ende wenn Silbentrennung
                if seg.text.rstrip().endswith('-'):
                    SE(seg_el, 'lb', **{'break': 'no'})

            # Siglen
            if line.sigles:
                note = SE(ab, 'note', type='sigle', place='margin')
                note.text = line.sigles

        # nhd. Übersetzung als Attribut auf <ab> (oder eigenes Element)
        if not line.is_gloss and line.nhd:
            # Wir sammeln nhd pro Vers, nicht pro Zeile (siehe unten)
            pass

    # nhd. Übersetzung gesammelt pro Versgruppe (ohne Glossen-nhd)
    nhd_parts = []
    for line in vg.lines:
        if not line.is_gloss and line.nhd:
            # Whitespace normalisieren (DOCX-Artefakte)
            clean_nhd = ' '.join(line.nhd.split())
            if clean_nhd:
                nhd_parts.append(clean_nhd)
    if nhd_parts:
        nhd_note = SE(div, 'note', type='translation_nhd', resp='#pfeifer')
        set_xml_attr(nhd_note, 'lang', 'de')
        p = SE(nhd_note, 'p')
        p.text = ' '.join(nhd_parts)

    # Quellenapparat
    if vg.sources:
        src_note = SE(div, 'note', type='sources')
        for src in vg.sources:
            build_source_entry(src, src_note)


def build_source_entry(src: SourceEntry, parent):
    """Erstellt ein <cit>-Element für einen Quelleneintrag."""
    cit = SE(parent, 'cit')

    # Sigle → @ana
    sigle_norm = src.sigle.replace(' ', '')
    ana_map = {
        'A': '#src-A', 'C': '#src-C', 'R': '#src-R',
        'Br': '#src-Br', 'RII': '#src-RII', 'N': '#src-N',
    }
    ana = ana_map.get(sigle_norm, f'#src-{sigle_norm}')
    cit.set('ana', ana)

    # <bibl>
    bibl = SE(cit, 'bibl')
    name_map = {
        'A': 'Augustinus', 'C': 'Cassiodor', 'R': 'Remigius',
        'Br': 'Breviarium', 'RII': 'RII', 'N': 'N',
    }
    bibl.text = name_map.get(sigle_norm, sigle_norm)

    # Editorial note für ungeklärte Siglen
    if sigle_norm in ('RII', 'N'):
        ed_note = SE(cit, 'note', type='editorial')
        ed_note.text = f'Sigle {sigle_norm} ist ungeklärt.'

    # <quote> mit lat. Text
    if src.latin:
        quote = SE(cit, 'quote')
        set_xml_attr(quote, 'lang', 'la')

        # Bold-Spans einbauen
        if src.bold_spans:
            build_text_with_bold(quote, src.latin, src.bold_spans)
        else:
            quote.text = src.latin

    # <note type="translation"> mit dt. Übersetzung
    if src.german:
        tr_note = SE(cit, 'note', type='translation', resp='#pfeifer')
        set_xml_attr(tr_note, 'lang', 'de')
        tr_note.text = src.german


def build_text_with_bold(parent_el, text, bold_spans):
    """Baut Text mit <hi rend="bold">-Elementen."""
    def make_bold(parent, _data):
        return SE(parent, 'hi', rend='bold')

    build_mixed_content(parent_el, text, bold_spans, make_bold)


# ---------------------------------------------------------------------------
# Back-Matter: Psaltervergleich + Wiener Notker
# ---------------------------------------------------------------------------

def build_back(psalm: PsalmData, parent):
    """Erstellt den <back>-Bereich mit Psaltervergleich und Wiener Notker."""

    # Psaltervergleich — Zeugen sind in <sourceDesc>/<listWit> deklariert,
    # hier nur die Readings als <app>/<rdg> mit Verweis auf die Header-IDs
    if psalm.psalter_witnesses:
        div = SE(parent, 'div', type='psalm_comparison')
        head = SE(div, 'head')
        head.text = 'Synoptischer Vergleich der Psalmtext-Versionen'

        app = SE(div, 'app')
        seen = set()
        for wit in psalm.psalter_witnesses:
            if wit.sigle in seen or not wit.text:
                continue
            seen.add(wit.sigle)
            # Sigle → Header-ID Mapping
            wit_id_map = {
                'G': 'wit-G', 'R': 'wit-R', 'H': 'wit-H',
                'A': 'wit-A-psa', 'C': 'wit-C-psa',
            }
            wit_id = wit_id_map.get(wit.sigle, f'wit-{wit.sigle}')
            rdg = SE(app, 'rdg', wit=f'#{wit_id}')
            set_xml_attr(rdg, 'lang', 'la')
            rdg.text = wit.text

    # Wiener Notker
    if psalm.wiener_notker:
        div = SE(parent, 'div', type='parallel_tradition', source='#wiener_notker')
        head = SE(div, 'head')
        head.text = 'Wiener Notker (ÖNB Cod. 2681, Edition Heinzle & Scherrer)'
        ab = SE(div, 'ab')
        ab.text = psalm.wiener_notker


# ---------------------------------------------------------------------------
# Hauptfunktion
# ---------------------------------------------------------------------------

def build_tei(psalm: PsalmData, enriched_groups: list[EnrichedVerseGroup]) -> etree._Element:
    """Baut den vollständigen TEI-Baum."""

    tei = E('TEI')
    set_xml_attr(tei, 'lang', 'goh')

    # Header
    tei.append(build_header())

    # Facsimile
    tei.append(build_facsimile())

    # Text
    text = SE(tei, 'text')

    # Front
    front = SE(text, 'front')
    intro = SE(front, 'div', type='introduction')
    p = SE(intro, 'p')
    p.text = ('Diese digitale Edition zeigt Psalm 2 aus Notkers Psalmenkommentar '
              'als Prototyp für eine vollständige Edition aller 150 Psalmen. '
              'Der Text basiert auf der Handschrift CSg 0021 (Stiftsbibliothek St. Gallen) '
              'und der kritischen Edition von Tax/Sehrt (1979).')

    # Body
    body = SE(text, 'body')
    psalm_div = SE(body, 'div', type='psalm', n='2')
    head = SE(psalm_div, 'head')
    head.text = 'Psalm 2'

    for vg in enriched_groups:
        build_verse_div(vg, psalm_div)

    # Back
    back = SE(text, 'back')
    build_back(psalm, back)

    return tei


# ---------------------------------------------------------------------------
# Serialisierung & Validierung
# ---------------------------------------------------------------------------

def serialize_tei(tei: etree._Element, output_path: str):
    """Serialisiert den TEI-Baum als XML-Datei."""
    tree = etree.ElementTree(tei)
    etree.indent(tree, space='  ')

    with open(output_path, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(b'<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" '
                b'type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\n')
        tree.write(f, encoding='unicode' if False else 'UTF-8',
                   xml_declaration=False, pretty_print=True)

    print(f'TEI-XML geschrieben: {output_path}')


def basic_validation(tei: etree._Element):
    """Grundlegende Strukturvalidierung (ohne externes Schema)."""
    errors = []

    # Prüfe Grundstruktur
    ns = {'tei': TEI_NS}
    header = tei.find('tei:teiHeader', ns)
    if header is None:
        errors.append('teiHeader fehlt')

    text = tei.find('tei:text', ns)
    if text is None:
        errors.append('text fehlt')

    body = tei.find('.//tei:body', ns)
    if body is None:
        errors.append('body fehlt')

    # Verse zählen
    verses = tei.findall('.//tei:div[@type="verse"]', ns)
    print(f'  Verse gefunden: {len(verses)}')
    for v in verses:
        n = v.get('n', '?')
        abs_count = len(v.findall('tei:ab', ns))
        segs = v.findall('.//tei:seg', ns)
        glosses = v.findall('.//tei:gloss', ns)
        sources = v.findall('.//tei:cit', ns)
        print(f'    Vers {n}: {abs_count} <ab>, {len(segs)} <seg>, '
              f'{len(glosses)} <gloss>, {len(sources)} <cit>')

    # Verkettungen prüfen
    parts = tei.findall('.//*[@part]', ns)
    print(f'  Verkettete Segmente (@part): {len(parts)}')

    # Foreign-Spans prüfen
    foreigns = tei.findall('.//tei:foreign', ns)
    print(f'  Sprachwechsel (<foreign>): {len(foreigns)}')

    # Back-Matter
    psalter = tei.findall('.//tei:div[@type="psalm_comparison"]', ns)
    wiener = tei.findall('.//tei:div[@type="parallel_tradition"]', ns)
    print(f'  Psaltervergleich: {"ja" if psalter else "nein"}')
    print(f'  Wiener Notker: {"ja" if wiener else "nein"}')

    if errors:
        print(f'\n  FEHLER: {", ".join(errors)}')
        return False

    print('  Validierung: OK (Strukturprüfung bestanden)')
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    docx_path = Path(__file__).parent.parent / 'data' / 'Probeseite_Notker.docx'
    output_path = Path(__file__).parent.parent / 'data' / 'tei' / 'psalm2.xml'

    print('=== Schritt 1: DOCX parsen ===')
    psalm = parse_probeseite(str(docx_path))

    print('\n=== Schritt 2: Schichten klassifizieren ===')
    enriched = classify_and_enrich(psalm)

    print('\n=== Schritt 3: TEI-XML generieren ===')
    tei = build_tei(psalm, enriched)

    print('\n=== Validierung ===')
    basic_validation(tei)

    print('\n=== Serialisierung ===')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    serialize_tei(tei, str(output_path))

    # Pipeline-interne Textnormalisierung (Pfeifer-Korrekturen, vormals Errata-Layer).
    # Wirkt auf den fertigen TEI-String, weil einige Korrekturen Zeilenumbrueche
    # ueberbruecken (Pfeifer hat zeilengetreu uebersetzt, daher Bindestriche).
    with open(output_path, encoding='utf-8') as f:
        tei_text = f.read()
    normalized = apply_corrections(tei_text)
    if normalized != tei_text:
        with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(normalized)
        print(f'  Normalisierung: Pfeifer-Korrekturen angewendet ({len(normalized) - len(tei_text):+d} Zeichen)')

    # Statistik
    xml_str = etree.tostring(tei, encoding='unicode', pretty_print=True)
    print(f'  Dateigröße: {len(xml_str.encode("utf-8")):,} Bytes')
    print(f'  Zeilen: {xml_str.count(chr(10)):,}')

if __name__ == '__main__':
    main()
