# CLAUDE.md – notker-edition

## Projekt

Digitale Edition von Notkers Psalmenkommentar (Notker III. von St. Gallen, ca. 950–1022). Prototyp für einen Drittmittelantrag, Psalm 2 als Demonstrationsobjekt. Auftraggeber ist Dr. Philipp Pfeifer (Institut für Germanistik, Universität Graz). Kooperationspartner sind Georg Vogeler und Bernhard Bauer (ZIM Graz). Auftragnehmer ist Digital Humanities Craft OG.

Repository: https://github.com/DigitalHumanitiesCraft/notker-edition

## Methode

Das Projekt folgt der *Promptotyping*-Methode. Alle Designentscheidungen, Domänenwissen und Implementierungsdetails sind in einem Obsidian-basierten Research Vault unter `knowledge/` erfasst. Diese Dokumente sind der *Context Stream*, also die maßgebliche Wissensgrundlage für jede Arbeitseinheit. Lies sie vollständig, bevor du Code schreibst oder Entscheidungen triffst.

## Wissensdokumente

| Dokument | Lies zuerst, wenn du ... |
|---|---|
| `knowledge/Research Plan.md` | ... den Gesamtplan, Scope-Bewertung und aktuelle Arbeitsphasen sehen willst |
| `knowledge/Domänenwissen.md` | ... verstehen willst, was Notkers Psalmenkommentar ist, welche Textschichten und Datenquellen existieren |
| `knowledge/Probeseite Analyse.md` | ... die Tabellenstruktur, Farbcodierung und Parsing-Implikationen der Primärdatenquelle nachschlagen willst |
| `knowledge/Anforderungen.md` | ... wissen willst, was der Prototyp können muss und wie die Features priorisiert sind |
| `knowledge/Design.md` | ... nachvollziehen willst, wie das Interface aufgebaut ist, welche Toggles es gibt und wie das Farbkonzept funktioniert |
| `knowledge/Technik.md` | ... den technischen Stack, das JSON-Datenmodell und die Parsing-Strategie verstehen willst |
| `knowledge/implementation.md` | ... das TEI-XML-Modell, die DOCX→TEI-Pipeline und Encoding-Entscheidungen verstehen willst |
| `knowledge/Journal.md` | ... die Projektchronologie, Entscheidungen und offenen Fragen nachschlagen willst |

## Stack

- Vanilla JS + HTML/CSS (kein Framework, kein Build-Step)
- Tailwind CSS via CDN
- OpenSeadragon via CDN (IIIF-Viewer)
- JSON als Datenmodell (kein Backend, kein Server)
- Deployment auf GitHub Pages oder als lokale HTML-Datei
- Datenaufbereitung in Python (python-docx)

Die bewusste Entscheidung gegen Frameworks folgt dem Prinzip maximaler Langlebigkeit. Der Prototyp muss in zwei Jahren noch funktionieren, ohne dass jemand `npm install` ausführt.

## Dateistruktur

```
notker-edition/
├── CLAUDE.md                          # Projektprompt für Claude Code
├── README.md
├── knowledge/                         # Research Vault (Obsidian)
│   ├── Research Plan.md
│   ├── Domänenwissen.md
│   ├── Probeseite Analyse.md
│   ├── Anforderungen.md
│   ├── Design.md
│   ├── Technik.md
│   ├── implementation.md
│   ├── Journal.md
│   ├── 2026-02-24 Erstgespräch.md
│   └── Referenzkorpus Altdeutsch.md
├── data/
│   ├── Probeseite_Notker.docx         # Primärdatenquelle
│   └── processed/
│       └── psalm2.json                # Aufbereitetes Datenmodell
├── scripts/
│   ├── parse_probeseite.py            # Probeseite → JSON
│   └── parse_annis.py                 # ANNIS-HTML → Rohtext (optional)
└── docs/
    └── index.html                     # Single-File-Anwendung (GitHub Pages)
```

## Arbeitspakete

**AP1 – Datenaufbereitung (4–6h).** Probeseite parsen (Farbcodierung extrahieren, Textschichten klassifizieren, Glossen und Quellenapparat trennen), JSON aufbauen. Die Probeseite (`data/Probeseite_Notker.docx`) ist die maßgebliche Ground Truth.

**AP2 – Weboberfläche (5–7h).** Multi-Panel-Interface mit Haupttext, Quellen-Panel und IIIF-Viewer. Kernfeatures: sechs Toggles (Psalmzitat/Übersetzung/Kommentar/Glossen/nhd./lat.-ahd.-Trennung), Quellenfilter, Facsimile.

**AP3 – Dokumentation und Übergabe (2–3h).** README, Zitierhinweise, Übergabe an Philipp.

## Regeln

1. **Analyse vor Produktion.** Lies die Wissensdokumente in `knowledge/`, bevor du Code schreibst. Wenn dir Informationen fehlen, frag nach, statt Annahmen zu treffen.
2. **Probeseite ist Ground Truth.** Bei Widersprüchen zwischen Dokumenten und der Probeseite gilt die Probeseite.
3. **Keine ungeklärten Siglen erfinden.** Die Siglen RII, N und H (als Quellen-Sigle) sind noch nicht abschließend geklärt. Modelliere sie im Datenmodell, aber kennzeichne sie als ungeklärt.
4. **Single-File-Prinzip.** Die Webanwendung ist eine HTML-Datei. CSS und JS sind eingebettet, nicht ausgelagert.
5. **Wissensdokumente aktuell halten.** Wenn du eine Designentscheidung triffst oder ein Problem löst, trage es in das zuständige Dokument in `knowledge/` ein.
6. **Drei Textschichten beachten.** Der Haupttext hat drei funktionale Schichten: Psalmzitation (olive), Übersetzung (grün), Kommentar (schwarz). Diese Klassifikation basiert auf der Farbcodierung der Probeseite und ist im JSON als `section.type` modelliert.
