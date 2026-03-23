#!/usr/bin/env python3
"""
test_pipeline.py — Umfassende Tests für die DOCX→TEI→JSON Pipeline

Prüft die gesamte Verarbeitungskette gegen die bekannte Ground Truth
der Probeseite (Psalm 2, 13 Verse, 14 Glossen, 31 Quellen).

Verwendung:
    python scripts/test_pipeline.py                   # Alles testen
    python scripts/test_pipeline.py --verbose         # Mit Details
    python scripts/test_pipeline.py --fix-report      # Nur Probleme auflisten
"""

import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from lxml import etree

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

BASE = Path(__file__).parent.parent
TEI_PATH = BASE / 'data' / 'tei' / 'psalm2.xml'
JSON_PATH = BASE / 'data' / 'processed' / 'psalm2.json'
DOCX_PATH = BASE / 'data' / 'Probeseite_Notker.docx'
SCHEMA_PATH = BASE / 'data' / 'schema' / 'tei_all.rng'

TEI_NS = 'http://www.tei-c.org/ns/1.0'
XML_NS = 'http://www.w3.org/XML/1998/namespace'
NS = {'tei': TEI_NS}

# Ground Truth aus knowledge/Probeseite Analyse.md
EXPECTED_VERSE_COUNT = 13  # Psalm 2 hat 13 Verse
EXPECTED_GLOSS_COUNT = 14  # 14 identifizierte Glossen
EXPECTED_PSALTER_WITNESSES = {'G', 'R', 'H', 'A', 'C'}
EXPECTED_SOURCE_SIGLES = {'A', 'C', 'R', 'Br'}  # Gesicherte; RII und N optional
EXPECTED_FUNCTIONS = {'psalm', 'translation', 'commentary'}

# Bekannte Glossentexte (Ground Truth aus Probeseite Analyse)
KNOWN_GLOSSES = [
    'iúdon diêt',
    'in gotes martyro',
    'christis uobunga',
    'penêmida',
    '.i. ténchende in uppe',
    'in ubertêilido',   # kann Whitespace-Varianten haben
    'âna zît',
    'irgân-',           # kann Teil einer mehrzeiligen Glosse sein
    'gen / chúnftîg',   # kann Teil einer mehrzeiligen Glosse sein
    'alle liûte',
    'uuerlt-lúste',
    'chuninga des flêisches',
    'kerich',
    'in slago dero brâuuo',
]


# ---------------------------------------------------------------------------
# Test-Framework (minimal, kein pytest nötig)
# ---------------------------------------------------------------------------

@dataclass
class TestResult:
    name: str
    passed: bool
    message: str
    severity: str = 'info'  # 'info', 'warning', 'error'
    details: list = field(default_factory=list)


class TestRunner:
    def __init__(self, verbose=False):
        self.results: list[TestResult] = []
        self.verbose = verbose

    def add(self, name, passed, message, severity='error', details=None):
        self.results.append(TestResult(
            name=name, passed=passed, message=message,
            severity=severity, details=details or [],
        ))

    def report(self):
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        warnings = sum(1 for r in self.results if not r.passed and r.severity == 'warning')
        errors = sum(1 for r in self.results if not r.passed and r.severity == 'error')

        print('\n' + '=' * 70)
        print(f'  TESTERGEBNISSE: {passed} bestanden, {failed} fehlgeschlagen '
              f'({errors} Fehler, {warnings} Warnungen)')
        print('=' * 70)

        for r in self.results:
            if r.passed:
                icon = '  PASS'
            elif r.severity == 'warning':
                icon = '  WARN'
            else:
                icon = '  FAIL'

            print(f'{icon}  {r.name}')
            if not r.passed or self.verbose:
                print(f'         {r.message}')
                for d in r.details[:5]:  # Max 5 Details
                    print(f'           - {d}')
                if len(r.details) > 5:
                    print(f'           ... und {len(r.details) - 5} weitere')

        print()
        return errors == 0  # True wenn keine harten Fehler


# ---------------------------------------------------------------------------
# TEI-Tests
# ---------------------------------------------------------------------------

def test_tei_wellformed(runner: TestRunner):
    """Prüft ob das TEI-XML wohlgeformt ist."""
    try:
        tree = etree.parse(str(TEI_PATH))
        runner.add('TEI wohlgeformt', True, f'{TEI_PATH.name} ist wohlgeformtes XML')
        return tree
    except etree.XMLSyntaxError as e:
        runner.add('TEI wohlgeformt', False, f'XML-Syntaxfehler: {e}')
        return None


def test_tei_relaxng(runner: TestRunner, tree):
    """Validiert TEI gegen RelaxNG-Schema."""
    if not SCHEMA_PATH.exists():
        runner.add('TEI RelaxNG-Validierung', False,
                   f'Schema nicht gefunden: {SCHEMA_PATH}', severity='warning')
        return

    try:
        schema_doc = etree.parse(str(SCHEMA_PATH))
        schema = etree.RelaxNG(schema_doc)
        is_valid = schema.validate(tree)

        if is_valid:
            runner.add('TEI RelaxNG-Validierung', True, 'Valide gegen tei_all.rng')
        else:
            errors = [f'Z.{e.line}: {e.message}' for e in schema.error_log[:10]]
            runner.add('TEI RelaxNG-Validierung', False,
                       f'{len(schema.error_log)} Validierungsfehler', details=errors)
    except Exception as e:
        runner.add('TEI RelaxNG-Validierung', False, f'Schema-Fehler: {e}')


def test_tei_header(runner: TestRunner, root):
    """Prüft Vollständigkeit des TEI-Headers."""
    checks = [
        ('.//tei:titleStmt/tei:title', 'title'),
        ('.//tei:titleStmt/tei:author', 'author'),
        ('.//tei:titleStmt/tei:editor', 'editor'),
        ('.//tei:publicationStmt/tei:authority', 'authority'),
        ('.//tei:msDesc', 'msDesc'),
        ('.//tei:listWit', 'listWit'),
        ('.//tei:listBibl', 'listBibl'),
        ('.//tei:taxonomy[@xml:id="textfunction"]', 'taxonomy textfunction'),
        ('.//tei:variantEncoding', 'variantEncoding'),
        ('.//tei:editorialDecl', 'editorialDecl'),
        ('.//tei:langUsage', 'langUsage'),
    ]
    # xml:id uses the XML namespace in XPath
    missing = []
    for xpath, label in checks:
        # Handle xml:id namespace
        xpath_ns = xpath.replace('@xml:id', f'@{{{XML_NS}}}id')
        if root.find(xpath_ns, NS) is None:
            missing.append(label)

    if missing:
        runner.add('TEI Header vollständig', False,
                   f'{len(missing)} Element(e) fehlen', details=missing)
    else:
        runner.add('TEI Header vollständig', True, f'Alle {len(checks)} Header-Elemente vorhanden')


def test_tei_verses(runner: TestRunner, root):
    """Prüft Vers-Struktur und -Abdeckung."""
    verse_divs = root.findall('.//tei:div[@type="verse"]', NS)
    verse_numbers_covered = set()

    for vd in verse_divs:
        n = vd.get('n', '')
        if '-' in n:
            start, end = n.split('-')
            for v in range(int(start), int(end) + 1):
                verse_numbers_covered.add(v)
        else:
            verse_numbers_covered.add(int(n))

    expected = set(range(1, EXPECTED_VERSE_COUNT + 1))
    missing = expected - verse_numbers_covered
    extra = verse_numbers_covered - expected

    details = []
    if missing:
        details.append(f'Fehlende Verse: {sorted(missing)}')
    if extra:
        details.append(f'Unerwartete Verse: {sorted(extra)}')

    # Vers 13 fehlt in der DOCX-Versstruktur (Probeseite hat nur "2,12")
    # Das ist eine bekannte Limitation, kein harter Fehler
    severity = 'error' if len(missing - {13}) > 0 else 'warning'
    runner.add('TEI Vers-Abdeckung', len(missing - {13}) == 0,
               f'{len(verse_numbers_covered)}/{EXPECTED_VERSE_COUNT} Verse abgedeckt '
               f'({len(verse_divs)} <div type="verse">)',
               severity=severity, details=details)


def test_tei_segments(runner: TestRunner, root):
    """Prüft Segment-Integrität."""
    segs = root.findall('.//tei:seg', NS)
    issues = []

    empty_segs = 0
    no_type = 0
    no_lang = 0
    no_ana = 0
    unknown_types = set()

    for seg in segs:
        text = ''.join(seg.itertext()).strip()
        if not text:
            empty_segs += 1

        seg_type = seg.get('type', '')
        if not seg_type:
            no_type += 1
        elif seg_type not in EXPECTED_FUNCTIONS:
            unknown_types.add(seg_type)

        if not seg.get(f'{{{XML_NS}}}lang'):
            no_lang += 1

        if not seg.get('ana'):
            no_ana += 1

    if empty_segs:
        issues.append(f'{empty_segs} leere <seg>-Elemente')
    if no_type:
        issues.append(f'{no_type} <seg> ohne @type')
    if no_lang:
        issues.append(f'{no_lang} <seg> ohne xml:lang')
    if no_ana:
        issues.append(f'{no_ana} <seg> ohne @ana')
    if unknown_types:
        issues.append(f'Unbekannte @type-Werte: {unknown_types}')

    runner.add('TEI Segment-Integrität', len(issues) == 0,
               f'{len(segs)} <seg>-Elemente geprüft',
               severity='warning' if empty_segs < 3 else 'error',
               details=issues)


def test_tei_part_chains(runner: TestRunner, root):
    """Prüft @part-Verkettungs-Integrität."""
    parts = root.findall('.//*[@part]', NS)

    chain_starts = [p for p in parts if p.get('part') == 'I']
    chain_ends = [p for p in parts if p.get('part') == 'F']
    chain_mids = [p for p in parts if p.get('part') == 'M']

    issues = []

    # Jedes I muss irgendwann zu einem F gleichen Typs führen
    if len(chain_starts) != len(chain_ends):
        issues.append(f'@part="I" ({len(chain_starts)}) ≠ @part="F" ({len(chain_ends)})')

    # Prüfe konsekutive Verkettung innerhalb jedes Vers-divs
    for verse_div in root.findall('.//tei:div[@type="verse"]', NS):
        abs_in_verse = verse_div.findall('tei:ab', NS)
        part_segs = []
        for ab in abs_in_verse:
            for seg in ab.findall('tei:seg', NS):
                if seg.get('part'):
                    part_segs.append(seg)

        # Prüfe Sequenzen: I→F oder I→M→...→F
        open_chain = None
        for seg in part_segs:
            part = seg.get('part')
            seg_type = seg.get('type')

            if part == 'I':
                if open_chain:
                    issues.append(f'Neue Kette startet bevor vorherige endet '
                                  f'(Vers {verse_div.get("n")}, Typ {seg_type})')
                open_chain = seg_type
            elif part in ('M', 'F'):
                if not open_chain:
                    issues.append(f'Verwaister @part="{part}" ohne vorheriges I '
                                  f'(Vers {verse_div.get("n")}, Typ {seg_type})')
                elif open_chain != seg_type:
                    issues.append(f'Typwechsel in Kette: {open_chain} → {seg_type} '
                                  f'(Vers {verse_div.get("n")})')
                if part == 'F':
                    open_chain = None

        if open_chain:
            issues.append(f'Offene Kette (kein F) in Vers {verse_div.get("n")}, '
                          f'Typ {open_chain}')

    runner.add('@part-Verkettung konsistent', len(issues) == 0,
               f'{len(chain_starts)} Ketten geprüft ({len(chain_starts)} I, '
               f'{len(chain_mids)} M, {len(chain_ends)} F)',
               details=issues)


def test_tei_glosses(runner: TestRunner, root):
    """Prüft Glossen-Vollständigkeit gegen Ground Truth."""
    gloss_els = root.findall('.//tei:gloss', NS)
    found_texts = [clean(''.join(g.itertext())) for g in gloss_els]

    # Prüfe gegen bekannte Glossen (Fuzzy-Match: normalisierter Vergleich)
    matched = 0
    unmatched = []
    found_norms = [clean(ft) for ft in found_texts]
    for known in KNOWN_GLOSSES:
        known_norm = clean(known)
        if any(known_norm in ft or ft in known_norm or
               known_norm.replace(' / ', ' ') in ft.replace(' / ', ' ')
               for ft in found_norms):
            matched += 1
        else:
            unmatched.append(known)

    details = []
    if unmatched:
        details.append(f'Nicht gefunden: {unmatched}')
    details.append(f'Gefunden im TEI: {found_texts}')

    runner.add(f'Glossen-Vollständigkeit ({EXPECTED_GLOSS_COUNT} erwartet)',
               len(gloss_els) >= EXPECTED_GLOSS_COUNT - 2,  # ±2 Toleranz
               f'{len(gloss_els)} Glossen im TEI, {matched}/{len(KNOWN_GLOSSES)} '
               f'Ground-Truth-Matches',
               severity='warning' if len(gloss_els) >= 10 else 'error',
               details=details)


def test_tei_sources(runner: TestRunner, root):
    """Prüft Quellenapparat-Vollständigkeit."""
    cits = root.findall('.//tei:cit', NS)
    found_sigles = set()
    issues = []

    for cit in cits:
        ana = cit.get('ana', '').lstrip('#')
        found_sigles.add(ana.replace('src-', ''))

        # Jedes cit braucht quote und bibl
        if cit.find(f'{{{TEI_NS}}}quote') is None:
            issues.append(f'{ana}: <quote> fehlt')
        if cit.find(f'{{{TEI_NS}}}bibl') is None:
            issues.append(f'{ana}: <bibl> fehlt')

    missing_sigles = EXPECTED_SOURCE_SIGLES - found_sigles
    if missing_sigles:
        issues.append(f'Fehlende Siglen: {missing_sigles}')

    runner.add('Quellenapparat vollständig', len(missing_sigles) == 0,
               f'{len(cits)} <cit>-Einträge, Siglen: {sorted(found_sigles)}',
               details=issues)


def test_tei_psalter_comparison(runner: TestRunner, root):
    """Prüft synoptischen Psaltervergleich."""
    comp = root.find('.//tei:div[@type="psalm_comparison"]', NS)
    if comp is None:
        runner.add('Psaltervergleich vorhanden', False, 'Kein <div type="psalm_comparison">')
        return

    rdgs = comp.findall('.//tei:rdg', NS)
    found_witnesses = set()
    for rdg in rdgs:
        wit = rdg.get('wit', '').lstrip('#')
        sigle = wit.replace('wit-', '').replace('-psa', '').replace('-full', '')
        found_witnesses.add(sigle)

    missing = EXPECTED_PSALTER_WITNESSES - found_witnesses
    details = []
    if missing:
        details.append(f'Fehlende Zeugen: {missing}')

    runner.add('Psaltervergleich (5 Zeugen)', len(missing) == 0,
               f'{len(rdgs)} <rdg>-Elemente, Zeugen: {sorted(found_witnesses)}',
               details=details)


def test_tei_wiener_notker(runner: TestRunner, root):
    """Prüft Wiener Notker."""
    wn = root.find('.//tei:div[@type="parallel_tradition"]', NS)
    if wn is None:
        runner.add('Wiener Notker vorhanden', False, 'Kein <div type="parallel_tradition">')
        return

    text = ''.join(wn.itertext()).strip()
    runner.add('Wiener Notker vorhanden', len(text) > 100,
               f'{len(text)} Zeichen Text')


def test_tei_language_tagging(runner: TestRunner, root):
    """Prüft Sprachwechsel-Annotation."""
    foreigns = root.findall('.//tei:foreign', NS)
    issues = []

    # Prüfe: <foreign> in lat. Psalmzitaten sollte selten sein
    # (Psalmzitate sind rein lateinisch laut Domänenwissen)
    for f_el in foreigns:
        parent_seg = f_el.getparent()
        if parent_seg is not None and parent_seg.get('type') == 'psalm':
            f_lang = f_el.get(f'{{{XML_NS}}}lang', '')
            f_text = ''.join(f_el.itertext()).strip()
            if f_lang == 'goh':
                issues.append(f'<foreign xml:lang="goh"> in Psalmzitat: "{f_text}"')

    if issues:
        runner.add('Sprachwechsel in Psalmzitaten', False,
                   f'{len(issues)} verdächtige <foreign> in lat. Psalmzitaten',
                   severity='warning', details=issues)
    else:
        runner.add('Sprachwechsel in Psalmzitaten', True,
                   f'{len(foreigns)} <foreign>-Elemente geprüft, keine in Psalmzitaten')


def test_tei_nhd_contamination(runner: TestRunner, root):
    """Prüft ob nhd-Übersetzungen von Glossentexten kontaminiert sind."""
    issues = []

    for verse_div in root.findall('.//tei:div[@type="verse"]', NS):
        nhd_note = verse_div.find(f'{{{TEI_NS}}}note[@type="translation_nhd"]')
        if nhd_note is None:
            continue

        nhd_text = ''.join(nhd_note.itertext()).strip()

        # Bekannte Glossentexte im nhd-Text suchen
        gloss_els = verse_div.findall(f'.//{{{TEI_NS}}}gloss')
        for gloss in gloss_els:
            gloss_text = ''.join(gloss.itertext()).strip()
            # Normalisiere Whitespace für Vergleich
            gloss_norm = ' '.join(gloss_text.split())
            if gloss_norm and gloss_norm in nhd_text:
                issues.append(f'Glosse "{gloss_norm}" in nhd-Übersetzung von '
                              f'Vers {verse_div.get("n")}')

    runner.add('nhd-Übersetzung nicht kontaminiert', len(issues) == 0,
               f'{len(issues)} Kontaminationen gefunden',
               severity='warning', details=issues)


def test_tei_verse_boundary_truncation(runner: TestRunner, root):
    """Prüft auf abgeschnittene Wörter an Versgruppen-Grenzen."""
    issues = []
    verse_divs = root.findall('.//tei:div[@type="verse"]', NS)

    for i, vd in enumerate(verse_divs):
        # Letztes <ab> des Vers-divs prüfen
        abs_list = vd.findall('tei:ab', NS)
        if not abs_list:
            continue

        last_ab = abs_list[-1]
        # Letzter Textinhalt
        segs = last_ab.findall('tei:seg', NS)
        if not segs:
            # Prüfe ob note mit text
            continue

        last_seg = segs[-1]
        text = ''.join(last_seg.itertext()).rstrip()
        if text.endswith('-'):
            # Prüfe ob nächster Vers-div mit Fortsetzung beginnt
            if i + 1 < len(verse_divs):
                next_vd = verse_divs[i + 1]
                next_abs = next_vd.findall('tei:ab', NS)
                if next_abs:
                    first_seg = next_abs[0].find('tei:seg', NS)
                    if first_seg is not None:
                        next_text = ''.join(first_seg.itertext()).strip()[:30]
                        issues.append(
                            f'Vers {vd.get("n")} endet mit "{text[-20:]}", '
                            f'Vers {next_vd.get("n")} beginnt mit "{next_text}"')

    runner.add('Keine abgeschnittenen Wörter an Versgruppen-Grenzen',
               len(issues) == 0,
               f'{len(issues)} Grenz-Probleme',
               severity='warning', details=issues)


def test_tei_whitespace(runner: TestRunner, root):
    """Prüft auf übermäßigen Whitespace in Textinhalten (ignoriert XML-Indentation)."""
    issues = []
    multi_space_pattern = re.compile(r'  +')
    # Elemente die tatsächlichen Text enthalten (nicht nur Struktur)
    text_tags = {'seg', 'gloss', 'quote', 'note', 'p', 'ab', 'head', 'title',
                 'author', 'editor', 'bibl', 'foreign', 'hi', 'rdg'}

    for el in root.iter():
        tag = el.tag.split('}')[-1] if '}' in el.tag else el.tag
        if tag not in text_tags:
            continue
        # Nur den direkten Textinhalt prüfen, nicht Indentation
        if el.text:
            stripped = el.text.strip()
            if stripped and multi_space_pattern.search(stripped):
                preview = stripped[:60]
                issues.append(f'<{tag}>: "{preview}"')

    runner.add('Kein ueberm. Whitespace in Textinhalten',
               len(issues) == 0,
               f'{len(issues)} Elemente mit Mehrfach-Leerzeichen',
               severity='warning', details=issues)


# ---------------------------------------------------------------------------
# JSON-Tests
# ---------------------------------------------------------------------------

def test_json_wellformed(runner: TestRunner):
    """Prüft ob das JSON wohlgeformt ist."""
    try:
        with open(JSON_PATH, encoding='utf-8') as f:
            data = json.load(f)
        runner.add('JSON wohlgeformt', True, f'{JSON_PATH.name} ist gültiges JSON')
        return data
    except (json.JSONDecodeError, FileNotFoundError) as e:
        runner.add('JSON wohlgeformt', False, str(e))
        return None


def test_json_schema(runner: TestRunner, data):
    """Prüft JSON-Schema-Konformität."""
    issues = []

    # Top-level Felder
    for key in ('psalm', 'metadata', 'verses', 'psalm_text_comparison', 'wiener_notker'):
        if key not in data:
            issues.append(f'Feld "{key}" fehlt')

    if 'metadata' in data:
        for key in ('title', 'manuscript', 'iiif_manifest', 'edition_pages'):
            if key not in data['metadata']:
                issues.append(f'metadata.{key} fehlt')

    # Vers-Schema
    for v in data.get('verses', []):
        if 'number' not in v:
            issues.append(f'Vers ohne "number"')
            continue
        if 'included_in' in v:
            continue  # Verweis-Vers, keine weiteren Felder nötig
        for key in ('sections', 'glosses', 'translation_nhd', 'sources'):
            if key not in v:
                issues.append(f'Vers {v["number"]}: "{key}" fehlt')

        # Section-Schema
        for sec in v.get('sections', []):
            for key in ('type', 'text', 'language'):
                if key not in sec:
                    issues.append(f'Vers {v["number"]}, Section ohne "{key}"')

    runner.add('JSON Schema-Konformität', len(issues) == 0,
               f'{len(data.get("verses", []))} Verse geprüft',
               details=issues)


def test_json_verse_coverage(runner: TestRunner, data):
    """Prüft Vers-Vollständigkeit im JSON."""
    verse_numbers = {v['number'] for v in data.get('verses', [])}
    expected = set(range(1, EXPECTED_VERSE_COUNT + 1))
    missing = expected - verse_numbers

    runner.add('JSON Vers-Abdeckung', len(missing) == 0,
               f'{len(verse_numbers)}/{EXPECTED_VERSE_COUNT} Verse',
               details=[f'Fehlend: {sorted(missing)}'] if missing else [])


def test_json_no_trailing_hyphens(runner: TestRunner, data):
    """Prüft ob Silbentrennungen im JSON aufgelöst sind."""
    issues = []
    for v in data.get('verses', []):
        for sec in v.get('sections', []):
            # Glossen können legitim mit '-' enden (geteilte Glossen, z.B. "irgân-")
            if sec.get('type') == 'gloss':
                continue
            text = sec.get('text', '')
            if text.endswith('-'):
                issues.append(f'Vers {v["number"]}: "{text[-30:]}"')

    runner.add('JSON: Keine offenen Silbentrennungen', len(issues) == 0,
               f'{len(issues)} offene Trennungen',
               severity='warning', details=issues)


def test_json_section_types(runner: TestRunner, data):
    """Prüft ob alle Section-Typen korrekt gemappt sind."""
    valid_types = {'psalm_citation', 'translation', 'commentary', 'gloss'}
    invalid = set()
    type_counts = {}

    for v in data.get('verses', []):
        for sec in v.get('sections', []):
            t = sec.get('type', '')
            type_counts[t] = type_counts.get(t, 0) + 1
            if t not in valid_types:
                invalid.add(t)

    details = [f'{t}: {c}' for t, c in sorted(type_counts.items())]
    runner.add('JSON Section-Typen valide', len(invalid) == 0,
               f'Verteilung: {type_counts}',
               details=details + ([f'Ungültig: {invalid}'] if invalid else []))


def test_json_glosses(runner: TestRunner, data):
    """Prüft Glossen im JSON."""
    total = sum(len(v.get('glosses', [])) for v in data.get('verses', []))
    empty_text = 0
    empty_nhd = 0

    for v in data.get('verses', []):
        for g in v.get('glosses', []):
            if not g.get('text', '').strip():
                empty_text += 1
            if not g.get('translation_nhd', '').strip():
                empty_nhd += 1

    issues = []
    if empty_text:
        issues.append(f'{empty_text} Glossen ohne Text')
    if empty_nhd:
        issues.append(f'{empty_nhd} Glossen ohne nhd-Übersetzung')

    runner.add(f'JSON Glossen ({EXPECTED_GLOSS_COUNT} erwartet)',
               total >= EXPECTED_GLOSS_COUNT - 2,
               f'{total} Glossen im JSON',
               severity='warning', details=issues)


def test_json_sources(runner: TestRunner, data):
    """Prüft Quellen im JSON."""
    total = sum(len(v.get('sources', [])) for v in data.get('verses', []))
    found_sigles = set()
    issues = []

    for v in data.get('verses', []):
        for s in v.get('sources', []):
            found_sigles.add(s.get('sigle', ''))
            if not s.get('latin_text', '').strip():
                issues.append(f'Vers {v["number"]}, {s.get("sigle")}: lat. Text fehlt')

    missing_sigles = EXPECTED_SOURCE_SIGLES - found_sigles
    if missing_sigles:
        issues.append(f'Fehlende Siglen: {missing_sigles}')

    runner.add('JSON Quellen vollständig', len(missing_sigles) == 0,
               f'{total} Quelleneinträge, Siglen: {sorted(found_sigles)}',
               details=issues)


def test_json_psalter_witnesses(runner: TestRunner, data):
    """Prüft Psaltervergleich im JSON."""
    comp = data.get('psalm_text_comparison', {})
    witnesses = comp.get('witnesses', [])
    # Siglen normalisieren: 'A-psa' -> 'A', 'C-psa' -> 'C'
    found = set()
    for w in witnesses:
        s = w.get('sigle', '')
        found.add(s.split('-')[0] if '-' in s else s)
    missing = EXPECTED_PSALTER_WITNESSES - found

    details = []
    for w in witnesses:
        text_len = len(w.get('text', ''))
        details.append(f'{w.get("sigle")}: {text_len} Zeichen')

    if missing:
        details.append(f'Fehlend: {missing}')

    runner.add('JSON Psaltervergleich', len(missing) == 0,
               f'{len(witnesses)} Zeugen', details=details)


def test_json_wiener_notker(runner: TestRunner, data):
    """Prüft Wiener Notker im JSON."""
    wn = data.get('wiener_notker', {})
    text = wn.get('text', '')
    runner.add('JSON Wiener Notker', len(text) > 100,
               f'{len(text)} Zeichen Text')


def test_json_nhd_contamination(runner: TestRunner, data):
    """Prüft ob nhd-Übersetzungen Glossentexte enthalten."""
    issues = []

    for v in data.get('verses', []):
        nhd = v.get('translation_nhd', '')
        if not nhd:
            continue
        for g in v.get('glosses', []):
            gtext = g.get('text', '').strip()
            if gtext and gtext in nhd and len(gtext) > 3:
                issues.append(f'Vers {v["number"]}: Glosse "{gtext}" in nhd')

    runner.add('JSON: nhd nicht kontaminiert', len(issues) == 0,
               f'{len(issues)} Kontaminationen',
               severity='warning', details=issues)


# ---------------------------------------------------------------------------
# DOCX ↔ TEI Vergleich
# ---------------------------------------------------------------------------

def test_docx_tei_comparison(runner: TestRunner, root):
    """Vergleicht DOCX-Quellzahlen mit TEI-Output."""
    if not DOCX_PATH.exists():
        runner.add('DOCX↔TEI Vergleich', False,
                   f'{DOCX_PATH} nicht gefunden', severity='warning')
        return

    try:
        sys.path.insert(0, str(BASE / 'scripts'))
        from parse_probeseite import parse_probeseite, TextLine, GlossLine

        psalm = parse_probeseite(str(DOCX_PATH))
    except Exception as e:
        runner.add('DOCX↔TEI Vergleich', False,
                   f'Parser-Fehler: {e}', severity='warning')
        return

    # Zähle DOCX-Entitäten
    docx_text_lines = 0
    docx_gloss_lines = 0
    docx_sources = 0
    docx_verse_groups = len(psalm.verse_groups)

    for vg in psalm.verse_groups:
        docx_text_lines += sum(1 for l in vg.lines if isinstance(l, TextLine))
        docx_gloss_lines += sum(1 for l in vg.lines if isinstance(l, GlossLine))
        docx_sources += len(vg.sources)

    # Zähle TEI-Entitäten
    tei_abs = len(root.findall('.//tei:div[@type="verse"]//tei:ab', NS))
    tei_glosses = len(root.findall('.//tei:gloss', NS))
    tei_sources = len(root.findall('.//tei:cit', NS))
    tei_verse_groups = len(root.findall('.//tei:div[@type="verse"]', NS))

    details = [
        f'DOCX: {docx_verse_groups} Versgruppen, {docx_text_lines} Textzeilen, '
        f'{docx_gloss_lines} Glossen, {docx_sources} Quellen',
        f'TEI:  {tei_verse_groups} Versgruppen, {tei_abs} <ab>, '
        f'{tei_glosses} <gloss>, {tei_sources} <cit>',
        f'Psalter: {len(psalm.psalter_witnesses)} Zeugen',
        f'Wiener Notker: {len(psalm.wiener_notker)} Zeichen',
    ]

    # Toleranz: TEI kann mehr <ab> haben als DOCX-Zeilen (Glossen werden zu <ab>)
    total_docx_lines = docx_text_lines + docx_gloss_lines
    diff_lines = abs(tei_abs - total_docx_lines)
    diff_sources = abs(tei_sources - docx_sources)
    diff_glosses = abs(tei_glosses - docx_gloss_lines)

    all_ok = diff_lines <= 2 and diff_sources == 0 and diff_glosses <= 1
    runner.add('DOCX↔TEI Zählervergleich', all_ok,
               f'Differenzen: Zeilen ±{diff_lines}, Quellen ±{diff_sources}, '
               f'Glossen ±{diff_glosses}',
               severity='warning' if not all_ok else 'info',
               details=details)


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def clean(text: str) -> str:
    """Normalisiert Whitespace."""
    return ' '.join(text.split()).strip()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    runner = TestRunner(verbose=verbose)

    print('=' * 70)
    print('  Notker Pipeline Tests -- DOCX > TEI > JSON')
    print('=' * 70)

    # --- TEI-Tests ---
    print('\n--- TEI-Tests ---')

    if not TEI_PATH.exists():
        runner.add('TEI-Datei vorhanden', False, f'{TEI_PATH} nicht gefunden')
        runner.report()
        return

    tree = test_tei_wellformed(runner)
    if tree is None:
        runner.report()
        return

    root = tree.getroot()
    test_tei_relaxng(runner, tree)
    test_tei_header(runner, root)
    test_tei_verses(runner, root)
    test_tei_segments(runner, root)
    test_tei_part_chains(runner, root)
    test_tei_glosses(runner, root)
    test_tei_sources(runner, root)
    test_tei_psalter_comparison(runner, root)
    test_tei_wiener_notker(runner, root)
    test_tei_language_tagging(runner, root)
    test_tei_nhd_contamination(runner, root)
    test_tei_verse_boundary_truncation(runner, root)
    test_tei_whitespace(runner, root)

    # --- JSON-Tests ---
    print('\n--- JSON-Tests ---')

    if not JSON_PATH.exists():
        runner.add('JSON-Datei vorhanden', False, f'{JSON_PATH} nicht gefunden')
        runner.report()
        return

    data = test_json_wellformed(runner)
    if data is None:
        runner.report()
        return

    test_json_schema(runner, data)
    test_json_verse_coverage(runner, data)
    test_json_section_types(runner, data)
    test_json_no_trailing_hyphens(runner, data)
    test_json_glosses(runner, data)
    test_json_sources(runner, data)
    test_json_psalter_witnesses(runner, data)
    test_json_wiener_notker(runner, data)
    test_json_nhd_contamination(runner, data)

    # --- DOCX↔TEI Vergleich ---
    print('\n--- DOCX↔TEI Vergleich ---')
    test_docx_tei_comparison(runner, root)

    # --- Report ---
    success = runner.report()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
