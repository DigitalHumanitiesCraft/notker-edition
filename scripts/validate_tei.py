#!/usr/bin/env python3
"""
validate_tei.py — Validiert psalm2.xml gegen das TEI-All RelaxNG-Schema.

Verwendung:
    python scripts/validate_tei.py
    python scripts/validate_tei.py data/tei/psalm2.xml
    python scripts/validate_tei.py data/tei/psalm2.xml data/schema/tei_all.rng
"""

import sys
import urllib.request
from pathlib import Path

from lxml import etree


def download_schema(schema_path: Path) -> bool:
    """Lädt das TEI-All RelaxNG-Schema herunter, falls nicht vorhanden."""
    if schema_path.exists():
        return True

    url = 'http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng'
    print(f'Schema nicht gefunden. Lade herunter von {url} ...')
    try:
        schema_path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, str(schema_path))
        print(f'  Heruntergeladen: {schema_path.stat().st_size:,} Bytes')
        return True
    except Exception as e:
        print(f'  FEHLER beim Download: {e}')
        return False


def validate(xml_path: Path, schema_path: Path) -> bool:
    """Validiert eine TEI-XML-Datei gegen ein RelaxNG-Schema."""

    print(f'XML:    {xml_path}')
    print(f'Schema: {schema_path}')
    print()

    # Schema laden
    try:
        schema_doc = etree.parse(str(schema_path))
        schema = etree.RelaxNG(schema_doc)
    except Exception as e:
        print(f'FEHLER beim Laden des Schemas: {e}')
        return False

    # XML laden
    try:
        doc = etree.parse(str(xml_path))
    except etree.XMLSyntaxError as e:
        print(f'XML-SYNTAXFEHLER: {e}')
        return False

    # Validieren
    is_valid = schema.validate(doc)

    if is_valid:
        print('ERGEBNIS: VALIDE')
    else:
        print(f'ERGEBNIS: NICHT VALIDE ({len(schema.error_log)} Fehler)')
        print()
        for i, error in enumerate(schema.error_log):
            if i >= 20:
                print(f'  ... und {len(schema.error_log) - 20} weitere Fehler')
                break
            print(f'  Zeile {error.line}: {error.message}')

    # Statistik
    print()
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    root = doc.getroot()
    print('STATISTIK:')
    for label, xpath in [
        ('Verse', './/tei:div[@type="verse"]'),
        ('<ab>', './/tei:ab'),
        ('<seg>', './/tei:seg'),
        ('<gloss>', './/tei:gloss'),
        ('<foreign>', './/tei:foreign'),
        ('<cit>', './/tei:cit'),
        ('<app>', './/tei:app'),
        ('@part', './/*[@part]'),
    ]:
        count = len(root.findall(xpath, ns))
        print(f'  {label}: {count}')

    return is_valid


def main():
    # Defaults
    base = Path(__file__).parent.parent
    xml_path = base / 'data' / 'tei' / 'psalm2.xml'
    schema_path = base / 'data' / 'schema' / 'tei_all.rng'

    # CLI-Argumente
    if len(sys.argv) >= 2:
        xml_path = Path(sys.argv[1])
    if len(sys.argv) >= 3:
        schema_path = Path(sys.argv[2])

    if not xml_path.exists():
        print(f'FEHLER: {xml_path} nicht gefunden')
        sys.exit(1)

    if not download_schema(schema_path):
        sys.exit(1)

    is_valid = validate(xml_path, schema_path)
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
