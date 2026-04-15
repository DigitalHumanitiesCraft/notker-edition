#!/usr/bin/env python3
"""
test_gloss_classification.py — Regression- und Unit-Tests fuer detect_gloss_line().

Zweck: Sicherstellen, dass der V6-Fall "ze_gótes sélbes ána-sihte. [...]" nach
dem Parser-Fix NICHT mehr als Glosse klassifiziert wird, und dass gueltige
Glossen weiterhin korrekt erkannt werden.

Pfeifer 2026-04-15: "V. 6 ... ist als Glosse erwaehnt ist aber Haupttext"

Verwendung:
    PYTHONIOENCODING=utf-8 python tests/test_gloss_classification.py
"""

import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
sys.path.insert(0, str(BASE / 'scripts'))

from parse_probeseite import Run, detect_gloss_line


class TestCase:
    def __init__(self, name):
        self.name = name
        self.passed = False
        self.message = ''

    def ok(self, m=''):
        self.passed = True
        self.message = m

    def fail(self, m):
        self.passed = False
        self.message = m


RESULTS = []


def case(name):
    tc = TestCase(name)
    RESULTS.append(tc)
    return tc


def runs(text: str, color=None) -> list:
    """Baut eine Liste mit einem Run fuer einen Text."""
    return [Run(text=text, color=color)]


# ---------------------------------------------------------------------------
# Regression fuer V6: darf NICHT als Glosse klassifiziert sein
# ---------------------------------------------------------------------------

def test_v6_ze_gotes_not_gloss():
    tc = case('V6 Regression: "ze_gótes sélbes ána-sihte. [...]" ist KEINE Glosse')
    text = 'ze_gótes sélbes ána-sihte. [...]'
    nhd = 'zu Gottes eigenem Angesicht. [...]'
    result = detect_gloss_line(runs(text), nhd, '')
    if result is False:
        tc.ok('Korrekt als Nicht-Glosse klassifiziert')
    else:
        tc.fail(f'FALSCH: detect_gloss_line returned {result} fuer "{text}"')


def test_bracket_ellipsis_signals_main_text():
    tc = case('Heuristik: Text mit "[...]" ist Haupttext, nicht Glosse')
    # Ein Editor-Marker "[...]" signalisiert Auslassung in zusammenhaengendem Text,
    # typisch fuer Kommentar- oder Haupttext-Fortsetzungen - nicht fuer kurze Glossen.
    for text, nhd in [
        ('kurzer text. [...]', 'kurze uebersetzung. [...]'),
        ('[...] end', '[...] ende'),
        ('mid [...] text', 'mitte [...] text'),
    ]:
        result = detect_gloss_line(runs(text), nhd, '')
        if result is not False:
            tc.fail(f'"[...]"-Text {text!r} faelschlich als Glosse klassifiziert')
            return
    tc.ok('Alle "[...]"-Texte korrekt als Nicht-Glosse')


# ---------------------------------------------------------------------------
# Positiv-Tests: echte Glossen bleiben Glossen
# ---------------------------------------------------------------------------

def test_real_glosses_still_detected():
    tc = case('Positiv: echte Glossen werden weiterhin korrekt erkannt')
    real_glosses = [
        ('iúdon diêt', 'Judenvolk'),
        ('christis uobunga', 'Christi Glauben'),
        ('penêmida', 'Vorherbestimmung'),
        ('âna zît', 'ohne Zeit'),
        ('alle liûte', 'alle Völker'),
        ('uuerlt-lúste', 'Weltlüste'),
        ('kerich', 'Gericht?'),
        ('in slago dero brâuuo', 'im Schlag der Brauen'),
    ]
    offenders = []
    for text, nhd in real_glosses:
        if detect_gloss_line(runs(text), nhd, '') is not True:
            offenders.append(text)

    if offenders:
        tc.fail(f'{len(offenders)} echte Glossen nicht als solche erkannt: {offenders}')
    else:
        tc.ok(f'{len(real_glosses)} echte Glossen korrekt erkannt')


def test_long_text_not_gloss():
    tc = case('Langtext (>5 Woerter) ist keine Glosse')
    long_text = 'ein sehr langer Kommentar mit mehr als fuenf Woertern hier'
    if detect_gloss_line(runs(long_text), 'lang', '') is False:
        tc.ok()
    else:
        tc.fail('Langtext faelschlich als Glosse')


def test_colored_text_not_gloss():
    tc = case('Farbiger Text (olive = Psalmzitat, gruen = Uebersetzung) ist keine Glosse')
    for color in ('806000', '00B050'):
        runs_colored = [Run(text='text', color=color)]
        if detect_gloss_line(runs_colored, 'text', '') is not False:
            tc.fail(f'Farbe {color} faelschlich als Glosse')
            return
    tc.ok()


def test_bibliographic_bracket_not_gloss():
    tc = case('Bibliographie-Klammer (Herausgeber 2020) ist keine Glosse')
    # Runde Klammern signalisieren bibliographische Angabe
    result = detect_gloss_line(runs('(Staatsbibliothek Bamberg Ms. 44)'), 'verweis', '')
    if result is False:
        tc.ok()
    else:
        tc.fail('Bibliographische Angabe faelschlich als Glosse')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print('=' * 70)
    print('  Glossen-Klassifikation Tests')
    print('=' * 70)

    test_v6_ze_gotes_not_gloss()
    test_bracket_ellipsis_signals_main_text()
    test_real_glosses_still_detected()
    test_long_text_not_gloss()
    test_colored_text_not_gloss()
    test_bibliographic_bracket_not_gloss()

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
