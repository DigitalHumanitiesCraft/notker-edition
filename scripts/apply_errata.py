#!/usr/bin/env python3
"""
apply_errata.py — Errata-Layer zwischen TEI-Build und JSON-Ableitung.

Zweck:
  Textkorrekturen (z.B. Pfeifer-Review-Feedback) werden als YAML-Regeln
  gepflegt und idempotent auf das generierte TEI angewendet. Damit koennen
  Korrekturen re-runbar sein: wird die DOCX erneut geparst, greifen die
  Errata automatisch wieder.

Vorgehen:
  1. Lade YAML-Regeln via load_rules()
  2. Wende apply_errata() an: jede Regel matcht mit Kontext (eindeutig),
     ersetzt die Zielstelle und wird auf Ambiguitaet geprueft.
  3. Idempotenz: Ist der neue Text bereits vorhanden und der alte nicht,
     wird die Regel ueberspringen (kein Fehler).

Schnittstelle:
  ErrataRule, ErrataError, apply_errata, load_rules

Verwendung als CLI:
  python scripts/apply_errata.py data/tei/psalm2.xml data/errata.yaml

Testabdeckung: tests/test_errata.py
"""

import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Datenmodell
# ---------------------------------------------------------------------------

@dataclass
class ErrataRule:
    """Eine einzelne Errata-Regel.

    Fields:
      id: eindeutiger Regel-Bezeichner (z.B. 'pfeifer-01')
      rationale: Begruendung + Quelle (Konvention: "Pfeifer <Datum> Review, Quelle: <Zitat>")
      context_before: unmittelbar vorangehender Text (disambiguiert Mehrfach-Matches)
      find: der zu ersetzende Text
      replace: der neue Text
      context_after: unmittelbar nachfolgender Text
      expected_count: erwartete Anzahl Matches (typ. 1). Ambiguitaet -> Fehler.
    """
    id: str
    rationale: str
    context_before: str
    find: str
    replace: str
    context_after: str
    expected_count: int = 1

    @property
    def full_pattern(self) -> str:
        return self.context_before + self.find + self.context_after

    @property
    def full_replacement(self) -> str:
        return self.context_before + self.replace + self.context_after

    @property
    def post_pattern(self) -> str:
        """Pattern nach erfolgter Anwendung (fuer Idempotenz-Check)."""
        return self.context_before + self.replace + self.context_after


class ErrataError(Exception):
    """Fehler bei der Errata-Anwendung."""


# ---------------------------------------------------------------------------
# Lade- und Validierungslogik
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = ('id', 'rationale', 'context_before', 'find', 'replace', 'context_after')


def load_rules(yaml_path: Path) -> list[ErrataRule]:
    """Laedt und validiert Regeln aus einer YAML-Datei.

    Wirft ErrataError bei Schemafehlern (fehlende Pflichtfelder, falscher Typ).
    """
    yaml_path = Path(yaml_path)
    if not yaml_path.exists():
        raise ErrataError(f'YAML-Datei nicht gefunden: {yaml_path}')

    with open(yaml_path, encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if data is None:
        return []
    if not isinstance(data, list):
        raise ErrataError(f'YAML-Root muss eine Liste sein, ist {type(data).__name__}')

    rules: list[ErrataRule] = []
    seen_ids: set[str] = set()

    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            raise ErrataError(f'Eintrag #{i}: muss ein Dict sein, ist {type(entry).__name__}')

        for field_name in REQUIRED_FIELDS:
            if field_name not in entry:
                raise ErrataError(f'Eintrag #{i} ({entry.get("id", "?")}): Pflichtfeld "{field_name}" fehlt')

        rule_id = str(entry['id'])
        if rule_id in seen_ids:
            raise ErrataError(f'Doppelter id: {rule_id}')
        seen_ids.add(rule_id)

        rules.append(ErrataRule(
            id=rule_id,
            rationale=str(entry['rationale']),
            context_before=str(entry['context_before']),
            find=str(entry['find']),
            replace=str(entry['replace']),
            context_after=str(entry['context_after']),
            expected_count=int(entry.get('expected_count', 1)),
        ))

    return rules


# ---------------------------------------------------------------------------
# Anwendungslogik
# ---------------------------------------------------------------------------

def apply_rule(text: str, rule: ErrataRule) -> tuple[str, str]:
    """Wendet eine einzelne Regel an.

    Returns (neuer_text, status).
    Status: 'applied' | 'idempotent' | 'not_found' | 'ambiguous'
    Wirft ErrataError bei unerwartetem Zustand.
    """
    find_count = text.count(rule.full_pattern)
    already_applied_count = text.count(rule.post_pattern) if rule.find != rule.replace else 0

    # Sonderfall: find == post_pattern (replace == find) -> Regel ist No-Op
    if rule.full_pattern == rule.full_replacement:
        return text, 'noop'

    if find_count == 0 and already_applied_count >= rule.expected_count:
        # Bereits angewendet -> idempotent, kein Fehler
        return text, 'idempotent'

    if find_count == 0:
        raise ErrataError(
            f'{rule.id}: Pattern nicht gefunden. '
            f'context_before="{rule.context_before[:30]}..." '
            f'find="{rule.find[:30]}..." '
            f'context_after="{rule.context_after[:30]}..."'
        )

    if find_count != rule.expected_count:
        raise ErrataError(
            f'{rule.id}: Erwartete {rule.expected_count} Matches, gefunden: {find_count}. '
            f'Regel ambiguous oder context ungenau. '
            f'Pattern: "{rule.full_pattern[:80]}..."'
        )

    new_text = text.replace(rule.full_pattern, rule.full_replacement, rule.expected_count)
    return new_text, 'applied'


def apply_errata(text: str, rules: list[ErrataRule]) -> str:
    """Wendet alle Regeln sequenziell an.

    Wirft ErrataError bei unerwartetem Zustand (siehe apply_rule).
    """
    current = text
    for rule in rules:
        current, _status = apply_rule(current, rule)
    return current


def apply_errata_with_report(text: str, rules: list[ErrataRule]) -> tuple[str, dict]:
    """Wie apply_errata, gibt zusaetzlich einen Status-Report zurueck."""
    current = text
    report = {'applied': [], 'idempotent': [], 'noop': []}
    for rule in rules:
        current, status = apply_rule(current, rule)
        report.setdefault(status, []).append(rule.id)
    return current, report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print('Usage: python scripts/apply_errata.py <tei_path> <yaml_path> [--dry-run]')
        print('  TEI wird in-place modifiziert (ausser bei --dry-run).')
        sys.exit(2)

    tei_path = Path(sys.argv[1])
    yaml_path = Path(sys.argv[2])
    dry_run = '--dry-run' in sys.argv

    if not tei_path.exists():
        print(f'FEHLER: TEI-Datei nicht gefunden: {tei_path}')
        sys.exit(1)

    try:
        rules = load_rules(yaml_path)
    except ErrataError as e:
        print(f'FEHLER beim Laden von {yaml_path}: {e}')
        sys.exit(1)

    print(f'{len(rules)} Regeln geladen aus {yaml_path}')

    with open(tei_path, encoding='utf-8') as f:
        text = f.read()

    try:
        new_text, report = apply_errata_with_report(text, rules)
    except ErrataError as e:
        print(f'FEHLER bei Regel-Anwendung: {e}')
        sys.exit(1)

    print(f'  applied:    {len(report.get("applied", []))}')
    print(f'  idempotent: {len(report.get("idempotent", []))}')
    print(f'  noop:       {len(report.get("noop", []))}')

    if dry_run:
        print('(dry-run: keine Aenderungen geschrieben)')
        sys.exit(0)

    if new_text == text:
        print('Keine Aenderungen noetig.')
        sys.exit(0)

    with open(tei_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_text)

    print(f'{tei_path} aktualisiert.')


if __name__ == '__main__':
    main()
