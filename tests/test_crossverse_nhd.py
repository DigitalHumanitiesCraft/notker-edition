#!/usr/bin/env python3
"""
test_crossverse_nhd.py — Regression-Test fuer redistribute_crossverse_nhd.

Pfeifer 2026-04-15: "manche Uebersetzungsanfaenge [sind] beim falschen Vers
(bspw. 'erlaubte es' bei V. 3 statt 1-2)".

Der Fix in build_tei.redistribute_crossverse_nhd verschiebt die nhd.-Zeile
einer Cross-Verse-Fortsetzung an das Ende des Vorgaenger-Verses. Heuristik:
Vorgaenger endet auf "-" UND aktueller Anfang kleingeschrieben.

Verwendung:
    PYTHONIOENCODING=utf-8 python tests/test_crossverse_nhd.py
"""

import sys
from dataclasses import dataclass, field
from pathlib import Path

BASE = Path(__file__).parent.parent
sys.path.insert(0, str(BASE / 'scripts'))

from build_tei import redistribute_crossverse_nhd


@dataclass
class StubSeg:
    text: str
    part: str | None = None


@dataclass
class StubLine:
    segments: list = field(default_factory=list)
    nhd: str = ''
    is_gloss: bool = False


@dataclass
class StubGroup:
    verses: str
    lines: list = field(default_factory=list)


RESULTS = []


def case(name, ok, msg=''):
    RESULTS.append((name, ok, msg))


def test_driftcase_v1_v3():
    """Silbentrennung han- / gta iz -> 'erlaubte es' gehoert zu V1-2."""
    v12 = StubGroup('1-2')
    v12.lines.append(StubLine(
        segments=[StubSeg(text='Êin herodes uuolta ín slâhen . anderer han-')],
        nhd='Ein Herodes wollte ihn erschlagen, (ein) anderer'
    ))
    v35 = StubGroup('3-5')
    v35.lines.append(StubLine(
        segments=[StubSeg(text='gta iz. Pedíu gât ín ter uuíllo.')],
        nhd='erlaubte es. Deshalb geht ihnen der Wille'
    ))
    v35.lines.append(StubLine(
        segments=[StubSeg(text='Reissen wir ihre Stricke.')],
        nhd='Reissen wir ihre Stricke.'
    ))

    redistribute_crossverse_nhd([v12, v35])

    v12_nhd = v12.lines[-1].nhd
    v35_first_nhd = v35.lines[0].nhd
    v35_second_nhd = v35.lines[1].nhd

    if 'erlaubte es' not in v12_nhd:
        case('Drift V1-2 absorbiert "erlaubte es"', False,
             f'V1-2-nhd nicht aktualisiert: {v12_nhd!r}')
        return
    if v35_first_nhd != '':
        case('V3-5 erste Zeile nhd geleert', False,
             f'V3-5-Zeile-1 nicht geleert: {v35_first_nhd!r}')
        return
    if 'Reissen' not in v35_second_nhd:
        case('V3-5 spaetere Zeilen unveraendert', False,
             f'V3-5-Zeile-2 unerwartet: {v35_second_nhd!r}')
        return
    case('Drift V1-2 -> V3-5 korrekt umverteilt', True,
         f'V1-2 endet jetzt mit: {v12_nhd[-30:]!r}')


def test_no_drift_when_prev_ends_cleanly():
    """Kein Trailing-Hyphen im Vorgaenger: keine Umverteilung."""
    v1 = StubGroup('1')
    v1.lines.append(StubLine(
        segments=[StubSeg(text='ganzer Satz.')],
        nhd='ganzer Satz.'
    ))
    v2 = StubGroup('2')
    v2.lines.append(StubLine(
        segments=[StubSeg(text='neuer Satz.')],
        nhd='neuer Satz.'
    ))
    redistribute_crossverse_nhd([v1, v2])
    if v2.lines[0].nhd == 'neuer Satz.' and v1.lines[0].nhd == 'ganzer Satz.':
        case('Kein Drift ohne Trailing-Hyphen', True)
    else:
        case('Kein Drift ohne Trailing-Hyphen', False,
             f'v1={v1.lines[0].nhd!r}, v2={v2.lines[0].nhd!r}')


def test_no_drift_when_next_starts_with_capital():
    """Vorgaenger endet auf "-", aber aktueller Anfang ist Grossbuchstabe."""
    v1 = StubGroup('1')
    v1.lines.append(StubLine(
        segments=[StubSeg(text='Wort ueber-')],
        nhd='Wort ueber-'
    ))
    v2 = StubGroup('2')
    v2.lines.append(StubLine(
        segments=[StubSeg(text='Neuer Satz.')],  # Grossbuchstabe
        nhd='Neuer Satz.'
    ))
    redistribute_crossverse_nhd([v1, v2])
    if v2.lines[0].nhd == 'Neuer Satz.' and v1.lines[0].nhd == 'Wort ueber-':
        case('Kein Drift bei Grossbuchstaben-Anfang', True)
    else:
        case('Kein Drift bei Grossbuchstaben-Anfang', False,
             f'v1={v1.lines[0].nhd!r}, v2={v2.lines[0].nhd!r}')


def test_gloss_line_skipped():
    """Glossen-Zeilen zaehlen nicht als erste Text-Zeile."""
    v1 = StubGroup('1')
    v1.lines.append(StubLine(
        segments=[StubSeg(text='Text endet mit-')],
        nhd='Text endet mit-'
    ))
    v2 = StubGroup('2')
    v2.lines.append(StubLine(is_gloss=True, nhd='glossen-nhd'))
    v2.lines.append(StubLine(
        segments=[StubSeg(text='fortsetzung hier.')],
        nhd='fortsetzung hier.'
    ))
    redistribute_crossverse_nhd([v1, v2])
    if 'fortsetzung' in v1.lines[0].nhd and v2.lines[1].nhd == '':
        case('Glossen-Zeile wird uebersprungen', True)
    else:
        case('Glossen-Zeile wird uebersprungen', False,
             f'v1={v1.lines[0].nhd!r}, v2[1]={v2.lines[1].nhd!r}')


def main():
    print('=' * 70)
    print('  Cross-Verse nhd-Drift Tests')
    print('=' * 70)

    test_driftcase_v1_v3()
    test_no_drift_when_prev_ends_cleanly()
    test_no_drift_when_next_starts_with_capital()
    test_gloss_line_skipped()

    passed = sum(1 for _, ok, _ in RESULTS if ok)
    failed = len(RESULTS) - passed
    for name, ok, msg in RESULTS:
        status = 'PASS' if ok else 'FAIL'
        print(f'  {status}  {name}' + (f'  - {msg}' if msg else ''))
    print('=' * 70)
    print(f'  {passed} passed, {failed} failed')
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
