---
type: plan
created: 2026-03-23
updated: 2026-03-23
status: draft
tags: [digital-humanities, notker, research-plan]
---

# Research Plan: Notker Psalmenkommentar – Digitaler Prototyp

## Projektkontext

Prototyp einer digitalen Edition von Notkers Psalmenkommentar (Notker III. von St. Gallen, ca. 950–1022). Demonstrationsobjekt: Psalm 2 (13 Verse). Zweck: funktionsfähiger Proof of Concept für Gutachter eines Drittmittelantrags.

| Rolle | Person / Organisation |
|---|---|
| Auftraggeber | Dr. Philipp Pfeifer, Institut für Germanistik, Universität Graz |
| Kooperation | Georg Vogeler, Bernhard Bauer (ZIM Graz) |
| Auftragnehmer | Digital Humanities Craft OG |
| Operative Kommunikation | Christian Steiner (office@dhcraft.org) |

Budget: 2.000 € netto pauschal (Angebot Nr. 11/26). Geschätzter Aufwand: 11–16 Stunden.
Abrechnung: SAP-Bestellung über Dekanat Uni Graz — SAP-Nummer per 21.03. noch offen.

## Stand des Wissens

Siehe [[Probeseite Analyse]] für die vollständige Quellenanalyse.

### Gesicherte Erkenntnisse

1. **Primärdatenquelle:** Philipps Probeseite (`data/Probeseite_Notker.docx`) enthält alle 13 Verse vollständig: Haupttext, nhd. Übersetzung, Quellenapparat, 14 Interlinearglossen, synoptischen Psalmtext-Vergleich (5 Zeugen) und Wiener Notker als Paralleltext. Finale Lieferung: 21.03.2026.

2. **Dreischichtiges Textmodell.** Die Farbcodierung der Probeseite codiert **Textfunktion**, nicht Sprache:
   - **Psalmzitation** (`#806000`, olive): Lateinische Psalmverse, wie Notker sie zitiert
   - **Übersetzung** (`#00B050`, grün): Ahd. Wiedergabe der Psalmzitate
   - **Kommentar** (schwarz): Notkers Exegese (ahd. UND lat. gemischt)

3. **Drei überlagernde Farblogiken:**
   - Handschrift CSg 0021: rot = Latein, schwarz = Althochdeutsch (Sprache)
   - Probeseite: olive/grün/schwarz = Psalmzitat/Übersetzung/Kommentar (Funktion)
   - Prototyp-UI: noch zu definieren

4. **Quellenapparat vollständig.** Vier gesicherte Siglen: A (Augustinus), C (Cassiodor), R (Remigius), Br (Breviarium). Jede Quelle mit lat. Original und dt. Übersetzung.

5. **Facsimile:** Seite 11 von CSg 0021 = Beginn Psalm 2 (von Philipp bestätigt). URL: `https://www.e-codices.unifr.ch/de/csg/0021/11/0/`

6. **Quelleneditionen:** De Gruyter — [Quellenliste S. 4–5](https://www.degruyterbrill.com/document/doi/10.1515/9783110935332/html), [Edition S. 11](https://www.degruyterbrill.com/document/doi/10.1515/9783110967500/html).

### Ungeklärte Fragen

| Frage | Priorität | Klärung durch |
|---|---|---|
| Siglen RII, N, H (als Quellen-Sigle im Haupttext) | Hoch | Philipp |
| G, R in Siglen-Spalte: Psalmtext-Zuordnung oder Kommentarquelle? | Hoch | Philipp |
| Querverweise auf Bibelstellen: welche Daten existieren? | Hoch | Philipp |
| SAP-Bestellnummer | Mittel | Philipp / Dekanat |
| IIIF-Manifest-URL verifizieren | Niedrig | Technisch |
| Seiten-Range von CSg 0021 für Psalm 2 (ab S. 11, bis wohin?) | Niedrig | Facsimile prüfen |

## Philipps Feature-Wünsche (E-Mail 21.03.2026)

Vier explizite Wünsche über die vereinbarten [[Anforderungen]] hinaus:

1. **Drei separate Toggles:** Übersetzung, Kommentar und Interlinearglossen unabhängig ein-/ausblendbar
2. **Dreischichtige Farbcodierung** im UI (Psalmzitat / Übersetzung / Kommentar)
3. **Querverweise auf Bibelstellen** als eigener Reiter
4. **Toggle für Interlinearglossen** separat

### Scope-Bewertung

| Feature | Budget (2.000 €) | Mehraufwand | Außerhalb Prototyp |
|---|---|---|---|
| Haupttext + lat./ahd.-Toggle | ✓ | | |
| Quellenapparat mit Filter | ✓ | | |
| nhd. Übersetzung (Toggle) | ✓ | | |
| Facsimile (IIIF-Viewer) | ✓ | | |
| Interlinearglossen inline | ✓ | | |
| Professioneller Gesamteindruck | ✓ | | |
| Drei-Farb-Semantik im UI | | ~2h | |
| Separate Toggles (Übers./Komm./Glossen) | | ~2–3h | |
| Psalmtext-Vergleich (synoptisch) | | ~2h | |
| Querverweise Bibelstellen | | | ✗ (Daten fehlen) |
| Wiener Notker als Paralleltext | | | ✗ (Scope) |

**Empfehlung:** Kernfeatures im Budget umsetzen. Drei-Farb-Semantik und separate Toggles sind machbar, wenn die Farbklassifikation automatisch aus dem DOCX extrahiert werden kann (was unsere Analyse bestätigt). Querverweise nicht im Prototyp, da Datengrundlage fehlt.

## Arbeitsphasen

### Phase 1 – Dokumentation & Klärung ← aktuell

- [x] Probeseite vollständig analysiert (Struktur, Farben, Glossen, Siglen)
- [x] Wissensdokumente in Research Vault konsolidiert
- [ ] Scope-Abstimmung mit Philipp (via Christian)
- [ ] Offene Siglen klären (RII, N, H, G/R-Doppelbelegung)
- [ ] Repository-Struktur bereinigen (Obsidian-Files aus Root entfernen)

### Phase 2 – Datenaufbereitung (AP1, ~4–6h)

- [ ] `parse_probeseite.py`: Word-Tabellen → JSON
  - Farbcodierung aus DOCX-Runs extrahieren → `section.type`
  - Interlinearglossen als eigenen Typ erkennen (Heuristik: kurze Zeilen ohne Sigle)
  - Quellenapparat-Zeilen erkennen (Heuristik: Sigle in Spalte 0)
  - Merged Cells korrekt behandeln (Spalten 0–2 identisch)
- [ ] JSON-Schema validieren gegen alle 13 Verse
- [ ] Optional: `parse_annis.py` für Handschriftenzeilen (Sekundärquelle)
- [ ] Referenzsysteme verknüpfen (Editionszeilen ↔ Handschriftenzeilen)

### Phase 3 – Interface (AP2, ~5–7h)

- [ ] Multi-Panel-Layout: Haupttext (Mitte), Quellen (links), Facsimile (rechts)
- [ ] Drei-Farb-Darstellung: Psalmzitat / Übersetzung / Kommentar
- [ ] Toggle-System: lat./ahd.-Trennung, Übersetzung, Kommentar, Glossen
- [ ] Quellenfilter: Checkboxen pro Sigle mit Highlight im Haupttext
- [ ] nhd. Übersetzung einblendbar (unter Versen oder als Spalte)
- [ ] IIIF-Viewer (OpenSeadragon via CDN)
- [ ] Einleitungstext + Navigation (angedeutete weitere Psalmen)
- [ ] Responsive Layout, seriös-akademische Ästhetik

### Phase 4 – Übergabe (AP3, ~2–3h)

- [ ] README mit Projektbeschreibung
- [ ] Zitierhinweise (Korpus, Edition, Facsimile)
- [ ] Deployment auf GitHub Pages
- [ ] Übergabe an Philipp

## Abhängigkeiten

```
Phase 1 (Klärung) ───→ Phase 2 (Daten) ───→ Phase 3 (UI) ───→ Phase 4 (Übergabe)
       ↑                      ↑
  Siglen-Klärung        Scope-Entscheidung
  (Philipp)             (Drei-Farb, Toggles, Vergleich)
```

Phase 2 kann mit der Kernstruktur sofort beginnen. Scope-abhängige Features (Psalmtext-Vergleich, Querverweise) werden im JSON vorbereitet, aber erst nach Klärung implementiert.

## Verknüpfungen

- [[Probeseite Analyse]] — Vollständige Analyse der Primärdatenquelle
- [[Domänenwissen]] — Notkers Psalmenkommentar, Informationsschichten, Siglen
- [[Anforderungen]] — User Stories und Priorisierung
- [[Design]] — Layout, Farben, Interaktion
- [[Technik]] — Stack, JSON-Schema, Parsing-Strategie
- [[Journal]] — Projektchronologie
