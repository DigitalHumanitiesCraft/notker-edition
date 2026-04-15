#!/usr/bin/env python3
"""
capture_bug_screenshots.py — Playwright-Script fuer BUG-11.1/2/3 Screenshots vorher/nachher.

Startet einen lokalen HTTP-Server, laedt die HTML-Variante (before|after),
fuehrt die drei Test-Szenarien aus und speichert Screenshots.

Variante:
  python scripts/capture_bug_screenshots.py before   # main-Zustand
  python scripts/capture_bug_screenshots.py after    # iteration-2-Zustand
"""

import sys
import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = Path(__file__).parent.parent
VARIANT = sys.argv[1] if len(sys.argv) > 1 else 'after'
SCREENSHOT_DIR = BASE / 'screenshots' / 'iteration-2' / VARIANT
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

PORT = 8765  # wenig konfliktanfaellig


def shot(page, name: str):
    path = SCREENSHOT_DIR / f'{name}.png'
    page.screenshot(path=str(path), full_page=False)
    print(f'  [{VARIANT}] {name}.png')


def capture(page):
    # Seite laden, warten bis JSON geladen
    page.goto(f'http://localhost:{PORT}/docs/')
    page.wait_for_timeout(1500)  # Warte auf async fetch + initialen Render

    # 0. Initial state
    shot(page, '00-initial')

    # BUG-11.1 Split-Toggle
    # Vorher: Toggle hat keinen sichtbaren Effekt. Nachher: zwei Spalten.
    btn_split = page.locator('button[data-toggle="split"]').first
    btn_split.click()
    page.wait_for_timeout(500)
    shot(page, '11-1-split-toggle-active')
    btn_split.click()  # zurueck
    page.wait_for_timeout(300)

    # BUG-11.2 Scroll im Quellen-Panel
    # Auf Vers 3-5 klicken (viele Quellen, inkl. Augustinus 2)
    verse = page.locator('[data-verse="3"]').first
    verse.click()
    page.wait_for_timeout(500)
    shot(page, '11-2-sources-panel-top')
    # Versuch, im sources-panel zu scrollen
    page.evaluate("""
        const panel = document.querySelector('.sources-content');
        if (panel) panel.scrollTop = panel.scrollHeight;
    """)
    page.wait_for_timeout(400)
    shot(page, '11-2-sources-panel-after-scroll')

    # BUG-11.3 × Button
    close_btn = page.locator('.panel-close').first
    close_btn.click()
    page.wait_for_timeout(600)  # fuer Transition
    shot(page, '11-3-sources-collapsed')

    # Re-open fuer Vollbildansicht
    # (Auf main-Branch gibt es kein Re-Open, darum voriges Screenshot zeigt ggf. unveraendert)


def main():
    server = subprocess.Popen(
        [sys.executable, '-m', 'http.server', str(PORT)],
        cwd=str(BASE),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    time.sleep(1.2)
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(viewport={'width': 1400, 'height': 900})
            page = context.new_page()
            capture(page)
            context.close()
            browser.close()
    finally:
        server.terminate()
        try:
            server.wait(timeout=2)
        except subprocess.TimeoutExpired:
            server.kill()

    print(f'\nScreenshots in: {SCREENSHOT_DIR}')


if __name__ == '__main__':
    main()
