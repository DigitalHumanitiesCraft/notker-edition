#!/usr/bin/env python3
"""
sync_vault.py — knowledge/*.md -> docs/vault/*.md

Kopiert die Research-Vault-Dokumente in den docs-Unterordner, damit die
vault.html-Seite sie per fetch laden kann. GitHub Pages serviert nur docs/.

Index-Format (docs/vault/index.json):
    {
      "files": ["Journal.md", ...],
      "commit": "abc1234",            # optional, wenn git verfuegbar
      "generated": "2026-04-16T15:30"  # ISO-Timestamp
    }
"""

import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def get_git_commit(repo_root: Path) -> str | None:
    """Liest den aktuellen Git-Commit-Hash. None, wenn kein Git-Repo."""
    try:
        result = subprocess.run(
            ['git', '-C', str(repo_root), 'rev-parse', 'HEAD'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def main():
    root = Path(__file__).parent.parent
    src_dir = root / 'knowledge'
    dst_dir = root / 'docs' / 'vault'

    if not src_dir.is_dir():
        print(f'knowledge/ nicht gefunden: {src_dir}', file=sys.stderr)
        sys.exit(1)

    dst_dir.mkdir(parents=True, exist_ok=True)

    # Alle vorhandenen .md im Ziel entfernen (wenn eine Quelle umbenannt wurde)
    for old in dst_dir.glob('*.md'):
        old.unlink()

    # Mail-Entwuerfe sind interne Arbeitsdokumente und gehoeren nicht in den
    # oeffentlichen Vault. Alle Dateien mit Prefix "Pfeifer-Mail-" oder generell
    # "_"-Prefix werden uebersprungen.
    files = []
    for md in sorted(src_dir.glob('*.md')):
        if md.name.startswith('Pfeifer-Mail-') or md.name.startswith('_'):
            print(f'  skip:   {md.name} (intern)')
            continue
        dst = dst_dir / md.name
        shutil.copy2(md, dst)
        files.append(md.name)
        print(f'  copied: {md.name}')

    # Index-Datei fuer das Frontend
    index = {
        'files': files,
        'generated': datetime.now().strftime('%Y-%m-%dT%H:%M'),
    }
    commit = get_git_commit(root)
    if commit:
        index['commit'] = commit

    (dst_dir / 'index.json').write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    print(f'\n{len(files)} Dokumente synchronisiert nach {dst_dir}')
    if commit:
        print(f'  commit: {commit[:7]}')
    print(f'  generated: {index["generated"]}')


if __name__ == '__main__':
    main()
