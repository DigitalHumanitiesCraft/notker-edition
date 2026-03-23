---
type: journal
created: 2026-02-24
updated: 2026-03-23
tags: [notker, project-log]
---

# Journal: Notker Psalmenkommentar Prototyp

## 2026-02-24 – Erstgespräch und Exploration

Philipp Pfeifer (Germanistik, Uni Graz) hat uns via Georg Vogeler und Bernhard Bauer (ZIM Graz) kontaktiert. Er plant einen Drittmittelantrag für eine digitale Edition von Notkers Psalmenkommentar und braucht einen funktionsfähigen Prototyp für die Gutachter.

Siehe [[2026-02-24 Erstgespräch]] für die vollständige Gesprächsnotiz.

**Entscheidungen:**
- Psalm 2 als Demonstrationsobjekt (13 Verse, überschaubar, quellenreich)
- Statische Seite statt Backend (Langlebigkeit, Portabilität)
- JSON statt TEI-XML für den Prototyp (TEI kommt im Gesamtprojekt)

## 2026-02-27 – Angebot versendet

Angebot Nr. 11/26: 2.000 € netto pauschal für Prototyp Psalm 2. Drei Arbeitspakete (AP1: Daten 4–6h, AP2: UI 5–7h, AP3: Übergabe 2–3h). Leistungszeitraum 2–3 Wochen nach Dateneingang.

Promptotyping-Dokumente aufgesetzt: knowledge, requirements, design, implementation, journal.

## 2026-03-21 – Datenlieferung durch Philipp

**Korrektur:** Die finale Datenlieferung erfolgte am 21.03.2026, nicht am 27.02. wie in einer früheren Version dieses Journals vermerkt. Die Materialien vom 27.02. waren Vorablieferungen (ANNIS-Scrape, PDFs, Interface-Skizze). Die Probeseite als Word-Dokument kam erst am 21.03.

Philipps E-Mail vom 21.03. enthielt:
- `Probeseite_Notker.docx` — vollständige tabellarische Aufbereitung von Psalm 2
- Explizite Feature-Wünsche (drei Toggles, Querverweise, Farbsemantik)
- Bestätigung: Facsimile-Einstieg = CSg 0021, Seite 11
- Kontextinfo: Probeseite war für physische Publikation gedacht, nicht für Prototyp

**Neue Feature-Wünsche:**
1. Drei separate Toggles: Übersetzung / Kommentar / Interlinearglossen
2. Querverweise auf Bibelstellen als eigener Reiter
3. Farbcodierung mit Semantik (Psalmzitat / Übersetzung / Kommentar)

**Zusätzlich geklärt:**
- Operative Kommunikation läuft über Christian Steiner (office@dhcraft.org)
- Abrechnung über SAP-Bestellung Dekanat Uni Graz (SAP-Nummer noch offen)
- Quelleneditionen identifiziert: De Gruyter (Quellenliste + Edition)

## 2026-03-23 – Bestandsanalyse und Vault-Konsolidierung

Systematische Analyse aller Projektmaterialien. Probeseite erstmals vollständig maschinell geparst.

**Zentrale Befunde:**

1. **Die Probeseite codiert Textfunktion über Farbe.** Drei Farben: olive (#806000) = Psalmzitation, grün (#00B050) = Übersetzung, schwarz = Kommentar. Das ist keine Sprachunterscheidung, sondern eine funktionale Klassifikation. Der Kommentar enthält sowohl ahd. als auch lat. Passagen.

2. **14 Interlinearglossen identifiziert** (statt der wenigen Beispiele in der bisherigen Dokumentation).

3. **Siglen-Doppelbelegung ist komplexer als angenommen.** G und R erscheinen nicht nur als Psalmtext-Zeugen, sondern auch in der Siglen-Spalte der Haupttext-Tabellen. Ihre Funktion dort ist unklar.

4. **Drei überlagernde Farblogiken** erkannt: Handschrift (Sprache), Probeseite (Textfunktion), UI (noch zu definieren).

5. **Tabellenstruktur entschlüsselt.** 13 Tabellen in drei funktionalen Gruppen. Merged Cells verursachen Duplikation in Spalten 0–2. Variable Spaltenanzahl (3–6), aber stabile semantische Struktur.

**Entscheidungen:**
- Alle Wissensdokumente in Research Vault (`knowledge/`) konsolidiert
- Probeseite bleibt Primärdatenquelle
- JSON-Schema muss `section.type` dreigliedrig modellieren: `psalm_citation`, `translation`, `commentary`

**Korrektur früherer Annahmen:**
- ~~Datenlieferung 27.02.~~ → Finale Lieferung 21.03.
- ~~Farbkonzept = Sprachunterscheidung~~ → Farbkonzept = Textfunktion
- ~~4 Informationstypen im Haupttext~~ → 3 funktionale Schichten + Interlinearglossen als Annotationstyp
- ~~Wenige Interlinearglossen~~ → 14 Stück identifiziert

## Offene Fragen

### Mit Philipp zu klären
- [ ] Siglen RII, N, H (als Quellen-Sigle)
- [ ] G, R in Siglen-Spalte: Psalmtext-Zuordnung oder Kommentarquelle?
- [ ] Querverweise auf Bibelstellen: welche Daten existieren?
- [ ] SAP-Bestellnummer
- [ ] Scope: Psalmtext-Vergleich und Wiener Notker im Prototyp?

### Technisch zu klären
- [ ] IIIF-Manifest-URL verifizieren
- [ ] Seiten-Range CSg 0021 für Psalm 2
- [ ] ANNIS-Datenmodell: Sprach-Annotationsebene vorhanden?

## Verknüpfungen

- [[Research Plan]] — Gesamtplan
- [[Probeseite Analyse]] — Detaillierte Quellenanalyse
