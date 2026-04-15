#!/usr/bin/env python3
"""
test_errata.py — Unit-Tests fuer den Errata-Mechanismus.

Ziel der Errata-Schicht (scripts/apply_errata.py):
- Textkorrekturen idempotent und re-runbar zwischen TEI-Build und JSON-Ableitung
- Matching erfolgt mit Kontext (eindeutig), nicht mit globalem find/replace
- Ambiguitaets-Check: matcht eine Regel mehr/weniger als erwartet -> Fehler, kein silent miss

Verwendung:
    PYTHONIOENCODING=utf-8 python tests/test_errata.py
"""

import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
sys.path.insert(0, str(BASE / 'scripts'))

# Diese Imports schlagen fehl in A.0 (rot). In A.1 werden sie gruen.
try:
    from apply_errata import (
        ErrataRule,
        ErrataError,
        apply_errata,
        load_rules,
    )
    MODULE_AVAILABLE = True
except ImportError as e:
    MODULE_AVAILABLE = False
    IMPORT_ERROR = str(e)


# ---------------------------------------------------------------------------
# Test-Framework (minimal)
# ---------------------------------------------------------------------------

class TestCase:
    def __init__(self, name):
        self.name = name
        self.passed = False
        self.message = ''

    def ok(self, message=''):
        self.passed = True
        self.message = message

    def fail(self, message):
        self.passed = False
        self.message = message


RESULTS = []


def case(name):
    tc = TestCase(name)
    RESULTS.append(tc)
    return tc


# ---------------------------------------------------------------------------
# Tests: Rule-Anwendung
# ---------------------------------------------------------------------------

def test_single_rule_applies():
    tc = case('Einzelregel wird angewendet')
    if not MODULE_AVAILABLE:
        tc.fail(f'Modul apply_errata nicht importierbar: {IMPORT_ERROR}')
        return

    rule = ErrataRule(
        id='t-001',
        rationale='Test',
        context_before='als sie ',
        find='Grüde',
        replace='Gründe',
        context_after=' des Zorns',
        expected_count=1,
    )
    text = 'Es schilt die Völker, als sie Grüde des Zorns nicht hatten.'
    result = apply_errata(text, [rule])
    expected = 'Es schilt die Völker, als sie Gründe des Zorns nicht hatten.'
    if result == expected:
        tc.ok(f'Korrekte Ersetzung: Grüde -> Gründe')
    else:
        tc.fail(f'Unerwartet: {result!r}')


def test_idempotent():
    tc = case('Idempotenz: zweiter Lauf = identischer Output')
    if not MODULE_AVAILABLE:
        tc.fail(f'Modul apply_errata nicht importierbar: {IMPORT_ERROR}')
        return

    rule = ErrataRule(
        id='t-002',
        rationale='Test',
        context_before='über ',
        find='die Welt der Erde',
        replace='das Universum der Welt',
        context_after=' ausgebreitet',
        expected_count=1,
    )
    text = 'ist dieser über die Welt der Erde ausgebreitet.'
    first = apply_errata(text, [rule])

    # Zweiter Lauf: erwartet 0 Matches (alt schon weg) -> aber Regel expected_count=1
    # -> muss separat laufen mit expected_count=0 oder Regel-Flag "optional_after_apply"
    # Alternative: expected_count kann als range definiert sein. Spezifikation:
    # Nach Anwendung sollte die Regel ohne Fehler ueberspringen (idempotent).
    # Das heisst: apply_errata muss erkennen "find fehlt, replace vorhanden" = bereits angewendet.
    second = apply_errata(first, [rule])
    if first == second:
        tc.ok('Erster und zweiter Lauf identisch')
    else:
        tc.fail(f'Nicht idempotent: first={first!r}, second={second!r}')


def test_ambiguous_match_fails():
    tc = case('Ambiguitaets-Fehler: mehr Matches als erwartet')
    if not MODULE_AVAILABLE:
        tc.fail(f'Modul apply_errata nicht importierbar: {IMPORT_ERROR}')
        return

    rule = ErrataRule(
        id='t-003',
        rationale='Test',
        context_before='',
        find='Kirche',
        replace='Gemeinde',
        context_after='',
        expected_count=1,
    )
    text = 'Die Kirche ist die Kirche der Glaeubigen.'
    try:
        apply_errata(text, [rule])
        tc.fail('Erwartete ErrataError, aber keine geworfen')
    except ErrataError as e:
        if 'ambig' in str(e).lower() or 'expected' in str(e).lower() or '2' in str(e):
            tc.ok(f'ErrataError korrekt geworfen: {e}')
        else:
            tc.fail(f'ErrataError geworfen, aber Message unklar: {e}')


def test_no_match_fails_when_expected():
    tc = case('Fehler wenn Regel keine Anwendung findet')
    if not MODULE_AVAILABLE:
        tc.fail(f'Modul apply_errata nicht importierbar: {IMPORT_ERROR}')
        return

    rule = ErrataRule(
        id='t-004',
        rationale='Test',
        context_before='xyz ',
        find='nonexistent',
        replace='ersetzt',
        context_after=' abc',
        expected_count=1,
    )
    text = 'Hier kommt xyz nicht vor in diesem Text.'
    try:
        apply_errata(text, [rule])
        tc.fail('Erwartete ErrataError, aber keine geworfen')
    except ErrataError as e:
        tc.ok(f'ErrataError korrekt geworfen: {e}')


def test_context_disambiguates():
    tc = case('Kontext disambiguiert: gleicher find-String, unterschiedlicher Kontext')
    if not MODULE_AVAILABLE:
        tc.fail(f'Modul apply_errata nicht importierbar: {IMPORT_ERROR}')
        return

    rule = ErrataRule(
        id='t-005',
        rationale='Test',
        context_before='Stab ',
        find='. das ist',
        replace=', das ist',
        context_after=' unbeugsame',
        expected_count=1,
    )
    text = 'Stab . das ist unbeugsame Gerechtigkeit. Stab . das ist ein Exempel.'
    # Nur die erste Instanz hat "unbeugsame" nach ". das ist" - das ist der disambiguierende Anker
    result = apply_errata(text, [rule])
    expected = 'Stab, das ist unbeugsame Gerechtigkeit. Stab . das ist ein Exempel.'
    if result == expected:
        tc.ok('Nur kontext-matchende Instanz ersetzt')
    else:
        tc.fail(f'Unerwartet: {result!r}')


def test_multiple_rules_sequential():
    tc = case('Mehrere Regeln werden sequenziell angewendet')
    if not MODULE_AVAILABLE:
        tc.fail(f'Modul apply_errata nicht importierbar: {IMPORT_ERROR}')
        return

    r1 = ErrataRule(id='t-006a', rationale='Test',
                   context_before='', find='alpha', replace='A',
                   context_after='', expected_count=1)
    r2 = ErrataRule(id='t-006b', rationale='Test',
                   context_before='', find='beta', replace='B',
                   context_after='', expected_count=1)
    text = 'alpha und beta'
    result = apply_errata(text, [r1, r2])
    if result == 'A und B':
        tc.ok('Beide Regeln angewendet')
    else:
        tc.fail(f'Unerwartet: {result!r}')


def test_yaml_schema_loads():
    tc = case('YAML-Schema: load_rules liest valide Datei')
    if not MODULE_AVAILABLE:
        tc.fail(f'Modul apply_errata nicht importierbar: {IMPORT_ERROR}')
        return

    yaml_path = BASE / 'data' / 'errata.yaml'
    if not yaml_path.exists():
        tc.fail(f'errata.yaml nicht vorhanden (wird in A.1 erstellt): {yaml_path}')
        return

    try:
        rules = load_rules(yaml_path)
        if len(rules) < 15:
            tc.fail(f'Erwartet mindestens 15 Regeln (Pfeifer-Korrekturen), gefunden: {len(rules)}')
            return
        tc.ok(f'{len(rules)} Regeln geladen')
    except Exception as e:
        tc.fail(f'load_rules scheiterte: {e}')


def test_yaml_schema_rejects_missing_fields():
    tc = case('YAML-Schema: fehlende Pflichtfelder -> Fehler')
    if not MODULE_AVAILABLE:
        tc.fail(f'Modul apply_errata nicht importierbar: {IMPORT_ERROR}')
        return

    # Schreibe Dummy-YAML mit fehlendem "find"
    import tempfile
    bad_yaml = """
- id: bad-001
  rationale: missing find field
  context_before: "x"
  replace: "y"
  context_after: "z"
  expected_count: 1
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
        f.write(bad_yaml)
        tmp_path = Path(f.name)

    try:
        try:
            load_rules(tmp_path)
            tc.fail('Erwartete Fehler fuer fehlendes "find", aber keiner geworfen')
        except (ErrataError, KeyError, TypeError) as e:
            tc.ok(f'Schema-Fehler korrekt erkannt: {type(e).__name__}')
    finally:
        tmp_path.unlink(missing_ok=True)


def test_rationale_convention():
    tc = case('Rationale-Konvention: Regeln tragen "Pfeifer 2026-04-15 Review, Quelle: X"')
    if not MODULE_AVAILABLE:
        tc.fail(f'Modul apply_errata nicht importierbar: {IMPORT_ERROR}')
        return

    yaml_path = BASE / 'data' / 'errata.yaml'
    if not yaml_path.exists():
        tc.fail(f'errata.yaml nicht vorhanden (wird in A.1 erstellt): {yaml_path}')
        return

    try:
        rules = load_rules(yaml_path)
    except Exception as e:
        tc.fail(f'load_rules scheiterte: {e}')
        return

    # Jede Pfeifer-Regel muss Rationale mit Datum und Quelle enthalten
    pfeifer_rules = [r for r in rules if r.id.startswith('pfeifer-')]
    offenders = []
    for r in pfeifer_rules:
        if 'Pfeifer' not in r.rationale or '2026-04-15' not in r.rationale or 'Quelle' not in r.rationale:
            offenders.append(r.id)

    if offenders:
        tc.fail(f'{len(offenders)} Regeln ohne Konventions-konforme Rationale: {offenders[:3]}...')
    else:
        tc.ok(f'Alle {len(pfeifer_rules)} Pfeifer-Regeln entsprechen der Rationale-Konvention')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print('=' * 70)
    print('  Errata Unit-Tests')
    print('=' * 70)

    if not MODULE_AVAILABLE:
        print(f'\n  Modul nicht verfuegbar: {IMPORT_ERROR}')
        print('  (Erwartet in A.0 - alle Tests laufen ROT bis A.1 fertig)')

    test_single_rule_applies()
    test_idempotent()
    test_ambiguous_match_fails()
    test_no_match_fails_when_expected()
    test_context_disambiguates()
    test_multiple_rules_sequential()
    test_yaml_schema_loads()
    test_yaml_schema_rejects_missing_fields()
    test_rationale_convention()

    passed = sum(1 for r in RESULTS if r.passed)
    failed = sum(1 for r in RESULTS if not r.passed)

    print()
    print('=' * 70)
    print(f'  ERGEBNIS: {passed} bestanden, {failed} fehlgeschlagen')
    print('=' * 70)

    for r in RESULTS:
        icon = '  PASS' if r.passed else '  FAIL'
        print(f'{icon}  {r.name}')
        if not r.passed:
            print(f'         {r.message}')

    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
