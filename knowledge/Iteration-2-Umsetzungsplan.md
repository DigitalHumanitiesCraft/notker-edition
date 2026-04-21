---
type: implementation-plan
created: 2026-04-15
updated: 2026-04-16
tags: [notker, implementation, iteration-2]
iteration: 2
baseline: "[[Anforderungen-Iteration-2]]"
status: done
---

# Iteration 2 — Umsetzungsplan und Stand

Begleitdokument zu [[Anforderungen-Iteration-2]]. Hält den geplanten Umsetzungspfad, die Pipeline-Teststrategie und den abschließenden Status pro User Story. Inhaltlich abgeschlossen mit Branch `iteration-2-pfeifer-review`.

## Phasenplan

Drei Phasen, jeweils releasbar. Nach jeder Phase kurze Rücksprache mit dem Auftraggeber statt großem Endreview.

### Phase A — Korrektur (P1)

Ziel: alle Blocker fix, das Review kann vollständig durchgeführt werden.

**Methodische Entscheidung (2026-04-15):** Textkorrekturen werden *nicht* händisch in `data/tei/psalm2.xml` gepatcht — ein Re-Parse der DOCX würde sie überschreiben. Stattdessen Errata-Layer zwischen TEI-Build und JSON-Ableitung, jede Korrektur als YAML-Regel mit Kontext-basiertem Matching, idempotent und auditierbar. *(Im Verlauf der Iteration 2b zugunsten einer einfacheren `PFEIFER_CORRECTIONS`-Liste in `parse_probeseite.py` wieder aufgegeben — siehe Status unten.)*

Schritte:
- **A.0 Test-Infrastruktur:** `tests/test_errata.py`, `tests/test_gloss_classification.py`, Acceptance-Tests in `scripts/test_pipeline.py`. Ground-Truth-Fixtures pro Korrektur (±20 Zeichen Kontext). Alle neuen Tests laufen initial rot.
- **A.1 Errata-Mechanismus:** `data/errata.yaml` + `scripts/apply_errata.py`. Pipeline: `build_tei.py → apply_errata.py → tei_to_json.py`. Ambiguitäts-Check gegen falsches Matching.
- **A.2 Parser-Fix V6 Glossen-Heuristik:** Ursachenanalyse in `classify_layers.py`, Regel-Logik-Review, Counter-Beispiele in Test-Suite.
- **A.3 CSS-Bugfixes:** BUG-11.2 Scroll, BUG-11.3 ×-Button, BUG-11.1 Split-Toggle. Screenshot-Vergleich als Abnahme-Artefakt.
- **A.4 End-to-End + PR:** alle Toggle-Kombinationen (4 Layer × nhd × split = 32 States), URL-Hash-Reload, Regression Iteration 1.

### Phase B — Lesbarkeit (P2)

Niedrigrisiko, Darstellungsqualität.
- BUG-11.4 Kontrast-Fade entfernen bzw. an Scroll-Indikator binden.
- BUG-11.5 Kursiv-Differenzierung nach Entscheidung 3 (kursiv für Lat.-Übersetzungen, aufrecht für Ahd.-Übersetzungen). TEI-Pipeline um `source.source_language` aus `@xml:lang` erweitern.
- US-1.3-Erweiterung: nhd.-Toggle wirkt auch auf Quellen-Panel.
- Release als Iteration 2b.

### Phase C — Struktur (P3, P4, P5)

Vision des Auftraggebers realisieren, benötigt Architekturentscheidung im Videocall.
1. Entscheidungsgespräch: Dropdown-Modell vs. Toggle-Gruppen-Erweiterung, Zeilensynopse über `<lb/>` oder Koordinaten-Annotation, Siglen-Semantik G/R/H.
2. US-9.2 (TEI-`<lb/>`, `lines[]` im JSON, Pipeline-Tests).
3. US-9.1 + US-9.3: Zeilen-Synopse-Layout mit Fließtext-Toggle.
4. US-8.1 + US-8.3: Panel-Registry, Dropdowns, CSS-Grid-Layout.
5. US-8.2: Schließen + Wiederherstellen.
6. US-10.1 + US-10.2: G/R/H als Layer.

### Abhängigkeitsgraph

```
US-12.* ──┐
BUG-11.* ─┤── Phase A (releasbar)
          │
BUG-11.4/5 ── Phase B (releasbar)
US-1.3-Ext ─┘

US-10.2 ── US-10.1 ───────┐
                          │
US-9.2 ── US-9.1 ── US-9.3┤── Phase C (gemeinsam releasen)
                          │
US-8.3 ── US-8.1 ── US-8.2┘
```

## Teststrategie

Pyramide, angewandt vor allem in Phase A:

| Ebene | Zweck | Scope |
|---|---|---|
| Unit | Einzelregel-Anwendung, Idempotenz (2. Lauf = identischer Output), Ambiguitäts-Erkennung (Regel matcht mehrfach → Fehler statt silent), Parser-Heuristik an DOCX-Paragraph-Fixtures | klein, schnell |
| Integration | End-to-End DOCX → TEI → (Errata) → TEI-final → JSON, Ground-Truth-Vergleich pro Korrektur | mittel |
| Regression | Eine Acceptance pro Review-Korrektur: `alt` nicht vorhanden + `neu` vorhanden an Position X | ein Test pro Korrektur |
| Invarianten | RelaxNG-Validierung, Glossenzähler 13, 7 Vers-`<div>`, keine leeren `<seg>`, keine orphan `<lb/>` | global |

CSS-Bugs werden nicht automatisiert getestet — stattdessen Screenshot-Vergleich als Abnahme.

## Datei-Eingriffe pro Phase

**Phase A:**
- TEI über Pipeline regenerieren (keine manuellen Edits).
- CSS-Fixes in `docs/index.html` vor Zeile 867: `.sources-content { overflow-y: auto; min-height: 0; }`, `.sources-panel.collapsed { width: 0; overflow: hidden; border: none; }`, Split-View-Regeln entkoppeln.
- Manuelle End-to-End-Prüfung aller 32 Toggle-Kombinationen.

**Phase B:**
- BUG-11.4: `mask-image`/`linear-gradient` auf `.sources-content` entfernen.
- BUG-11.5: `.source-german` per `[data-source-language]` stylen, Pipeline-Feld `source_language` aus `<quote xml:lang>` extrahieren.
- US-1.3-Ext: `toggleNhd()` toggelt zusätzlich Klasse auf `#sources-panel`.

**Phase C:**
- US-9.2: `<lb/>`-Elemente im TEI, Parser erkennt DOCX-Zeilenumbrüche (Soft- vs. Hard-Return).
- US-9.1: `renderVerses()` um Zeilen-Modus erweitern, CSS-Grid-Row pro Zeile, Bindestriche am Zeilenende aus Daten entfernen.
- US-8.1: Panel-Registry (`registerPanelContent(def)` mit `id`, `label`, `render(containerEl)`), `main-container` auf CSS-Grid, State `panelAssignment`, URL-Hash-Persistenz erweitern.
- US-10.1: Siglen-Pool um G/R/H als eigene Gruppe, `updateSourceHighlights()` nutzt vorhandene Sigle-Datenstruktur.

## Umsetzungs-Status (Stand 2026-04-16)

Stand nach Auslieferung Iteration 2b auf Branch `iteration-2-pfeifer-review`.

| Story | Phase | Status | Nachweis |
|---|---|---|---|
| US-12.1 Quellen-Übersetzungen (11 Korrekturen) | A | done | `PFEIFER_CORRECTIONS` in `parse_probeseite.py` |
| US-12.2 Haupttext + nhd. (10 Korrekturen) | A | done | `PFEIFER_CORRECTIONS` |
| US-12.3 V6-Glossen-Reklassifikation | A | done | Parser-Heuristik, Glossen 14 → 13 |
| BUG-11.1 Split-Toggle | A | done | `efd7422` |
| BUG-11.2 Sources-Panel-Scroll | A | done | `efd7422` |
| BUG-11.3 ×-Button | A | done | `efd7422`, Iteration 2 ersetzt durch Slot-System |
| BUG-11.4 Kontrast-Fade | B | done | `f2eb99d`, `mask-image` entfernt |
| BUG-11.5 Kursiv nach Sprache | B | done | `f2eb99d`, Pipeline `source_language`, CSS-Regeln |
| US-1.3-Erweiterung Quellen-Toggle | B | done | `f2eb99d`, Taste Q, Default an, URL-Hash `qnhd` |
| US-8.1 Panel-Dropdown pro Feld | C | done | `53de31f`, Slot-System mit 9-Eintrag-Pool |
| US-8.2 Schließen + Wiederherstellen | C | done | `53de31f`, × pro Slot + Restore-Bar |
| US-8.3 Content-Registry | C | done | `53de31f`, `POOL`-Objekt, deklarativ erweiterbar |
| US-9.1 Zeilengetreue nhd.-Übersetzung | C | done | TEI `<lg type="line-faithful">`, Edition rendert `.nhd-line` pro Zeile |
| US-9.2 TEI-Zeilenstruktur Grundtext | C | done | `<ab n="X">` pro Notker-Zeile, `line_n` in JSON, `data-line` im Frontend. Echte Handschriften-Zeilenumbrüche der CSg 0021 weiterhin nur via DOCX abgeleitet |
| US-9.3 Vers-Anker für nhd.-Zeilen | C | done | Zeilen pro Vers extrahiert, kein Vers-Drift |
| US-10.1 Psalter-Filter | C | done | G + R + H als eigene Filter-Gruppe |
| US-10.2 Siglen-Semantik (R-Disambiguierung) | C | done | `disambiguate_sigles()` in `tei_to_json.py` (R in `psalm_citation` → Romanum, sonst → Remigius). Bestätigung durch Auftraggeber offen |
| Cross-Verse-Hyphen im TEI verkettet | — | done | `chain_cross_verse_hyphens()` in `build_tei.py`, V1–2 `han-` + V3–5 `gta` mit `@part`/`@next`/`@prev` |
| Whitespace-Normalisierung | — | done | `normalize_whitespace_in_text_nodes()` in `parse_probeseite.py` |
| Errata-Layer entfernt (Refactor) | — | done | `f49ff58`, 779 Zeilen weg, Korrekturen jetzt in `PFEIFER_CORRECTIONS` |

**Test-Bilanz:**
- `tests/test_gloss_classification.py`: 6 / 6 grün
- `scripts/test_pipeline.py`: 29 / 29 grün, 0 Warnings
- Browser-Smoke-Test (Playwright): 0 JS-Errors, R-Disambiguierung verifiziert (`src:R` → 16 Patristik-Sections, `psa:R` → 13 Psalter-Sections, keine Überlappung)

**Offen für Iteration 3:**
- Echte Handschriften-Zeilenumbrüche der CSg 0021 (bislang aus DOCX-Tabellenzeilen abgeleitet). Mit Tax/Sehrt-Markierung oder Facsimile-Ableitung verfeinerbar.
- R-Disambiguierung: Bestätigung der Best-Effort-Heuristik durch den Auftraggeber.
- Augustinus-2-Korrekturen V3–5 / V6: wegen BUG-11.2 in Iteration 1 nicht prüfbar, Nachreichung erwartet.

## Iteration 2c — Follow-up (2026-04-16)

Befunde aus der Iteration-2b-Auslieferung, alle ohne neue Stories adressierbar und direkt umgesetzt.

| Befund | Status | Nachweis |
|---|---|---|
| Quellen-Filter doppelt gerendert nach Slot-Re-Mount | done | `renderSourceFilters()` leert Container |
| Pool-Templates mit festen Pixel-Breiten (Iteration-1-Altlast) | done | `width: 100%; height: 100%` |
| `<th>` im Psalmtext-Vergleich überlagert Content beim Scrollen | done | `z-index: 2` + Box-Shadow |
| OSD-Viewer leer nach Slot-Swap | done | `onMount` ruft `viewport.applyConstraints` |
| Toggle „Quellen-Übersetzung" im falschen Kontext | done | verschoben in Quellen-Panel-Header |
| Schichten-Toggle wirkt nicht bei geschlossenem Edition-Slot | done | `ensurePoolVisible('edition')` |
| Quellen-nhd-Toggle wirkt nicht bei geschlossenem Quellen-Slot | done | `ensurePoolVisible('sources')` |
| Quellen-/Psalter-Filter untereinander statt nebeneinander | done | `flex-direction: row`, `.source-filter-group` |
| Redundante Zeilen im Quellen-Header | done | Merge zu einer Zeile, Aktion via `margin-left: auto` |
| Toolbar-Gruppenlabels verschwenden Platz | done | entfernt, Padding/Font reduziert |
| Fünf `<l>`-Zeilen-Korrekturen griffen nicht (Fließtext-Replace) | done | Patterns für beide Kontexte in `PFEIFER_CORRECTIONS` |
| Cross-Verse-Drift: „erlaubte es" bei V3 statt V1–2 | done | `redistribute_crossverse_nhd()` in `build_tei.py` |
| Psalm-Nav 1/3/50/100/150 wirkt begehbar | done | `.disabled`-Class + `cursor: not-allowed` |
| Diagnose meldet Glossenzahl 13/14 als Problem | done | Erwartung auf 13 korrigiert |
| Diagnose meldet V7 „irgân-" als Problem (bekannte Limitation) | done | aus Warn-Liste gefiltert |
| Leeres Verses-Panel bei 0 aktiven Schichten verwirrt | done | Info-Block + „Alle Schichten einblenden"-Button |
| Promptotyping-Vault nicht öffentlich zugänglich | done | `docs/vault.html` + `scripts/sync_vault.py` |

**Tests:** 29 / 29 Pipeline-Tests grün, Pipeline idempotent.

## Verknüpfungen

- [[Anforderungen-Iteration-2]] — Stories, Priorisierung und Entscheidungen
- [[Journal]] — chronologische Fortschreibung und Iteration-2c-Notizen
- [[Technik]] — Pipeline und Datenmodell
