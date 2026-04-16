---
type: mail-draft
created: 2026-04-16
tags: [notker, pfeifer, mail, iteration-2c]
recipient: Philipp Pfeifer
status: draft
---

# Mail-Draft an Philipp Pfeifer — Iteration 2c Auslieferung

**Betreff:** Notker-Prototyp — zweite Review-Runde, drei offene Rückfragen

---

Sehr geehrter Herr Pfeifer,

ich melde mich mit dem Zwischenstand zum Notker-Prototyp. Alle Punkte aus
Ihrem Review vom 15. April sind umgesetzt, die Edition liegt unter
https://dhcraft.org/notker-edition.

## Was seit der letzten Runde neu ist

**Aus Ihrem Feedback direkt umgesetzt**

- Alle rund 20 Textkorrekturen (Quellen-Übersetzungen und neuhochdeutsche
  Übersetzung) sind eingearbeitet — sowohl im Fließtext als auch in der
  zeilengenauen Wiedergabe.
- Die V6-Glosse „ze_gótes sélbes ána-sihte" ist jetzt als Haupttext
  (Kommentar) ausgewiesen, nicht mehr als Interlinearglosse.
- Das Slot-System für alle drei Felder ist fertig: Sie können in jedem
  Feld aus neun Inhalten wählen (Quellen, Notkers Text, Nhd. Übersetzung,
  Wiener Notker, Psalter G, R, H, Handschrift, Psalmtext-Vergleich,
  Anmerkungen).
- G, R und H funktionieren jetzt als eigene Filter-Gruppe im Quellenapparat
  — analog zu den patristischen Siglen können Sie damit Stellen markieren,
  an denen ein bestimmter Psalter-Zeuge verwendet wird.
- Zeilengenaue neuhochdeutsche Übersetzung: der Trennungsbindestrich bleibt
  erhalten, wie Sie es gewünscht haben. Zusätzlich lässt sich dieselbe
  Übersetzung als Fließtext im Pool-Eintrag „Nhd. Übersetzung" einblenden.
- Ihr Befund zur Vers-Drift ist korrigiert: „erlaubte es" gehört jetzt
  zum Ende von V1–2, nicht mehr zum Anfang von V3–5. Das gleiche Prinzip
  gilt für alle Cross-Verse-Fragmente.

**Zusätzliche Verbesserungen**

- Der lat./ahd.-Split funktioniert wieder in allen Schichtkombinationen.
- Das Quellen-Panel scrollt jetzt unabhängig — Sie können Augustinus 2
  zu V3–5 und V6 damit auch einsehen.
- Der Ausblenden-Button (×) schließt die Spalten tatsächlich; eine Leiste
  am unteren Rand stellt sie wieder her.
- Die Kursivdarstellung differenziert jetzt nach Quell-Sprache: Übersetzungen
  aus dem Lateinischen bleiben kursiv, Übersetzungen aus dem Althochdeutschen
  werden aufrecht gesetzt.
- Das Fade-out am unteren Rand des Quellenapparats ist weg — die Schrift
  der letzten Einträge bleibt jetzt in vollem Kontrast.
- Eine neue Seite `/vault.html` macht die zehn Entscheidungs- und
  Wissensdokumente (Domänenwissen, Anforderungen, Design, Technik etc.)
  öffentlich einsehbar — für Antrags-Kollegen zitierbar.

## Drei konkrete Rückfragen

**1. Augustinus 2 zu V3–5 und V6**

Diese Korrekturen konnten Sie wegen des Scroll-Bugs nicht prüfen. Der
Bug ist behoben, Sie können das Panel jetzt frei durchscrollen. Wenn Sie
Korrekturen finden, reicht eine kurze Liste per Mail.

**2. Sigle R: Remigius oder Romanum?**

Die Sigle R kollidiert — im patristischen Apparat steht sie für Remigius,
im Psalmtext für das Romanum. Wir haben eine Heuristik implementiert
(R in einer Psalm-Zitation wird als Romanum gelesen, sonst als Remigius),
aber eine Bestätigung oder Korrektur Ihrerseits wäre uns wichtig.

**3. Zeilenumbrüche im Grundtext**

Sie schreiben zu Recht: der Grundtext (ahd./lat.) ist nicht zeilengetreu.
Um das zu ändern, bräuchten wir die Zeilengrenzen der Handschrift CSg 0021
— entweder aus der Tax/Sehrt-Edition (gibt es dort eine Zeilenmarkierung?)
oder aus dem Facsimile manuell abgeleitet. Haben Sie dazu Daten oder
einen Vorschlag?

## Für den Antrag

Das Methodenpaket (docs/methode.html + zitierbares PDF) wird für die
Antragsphase finalisiert. Die Vault-Seite ist bereits öffentlich und kann
als Arbeitsnachweis verlinkt werden.

Für einen kurzen Videocall zu Punkt 2 und 3 stehe ich jederzeit zur
Verfügung. Idealerweise diese oder nächste Woche — vor der Antragsabgabe.

Mit freundlichen Grüßen

---

**Anhang — Deep-Links zur Prüfung**

- Prototyp: https://dhcraft.org/notker-edition
- Vault: https://dhcraft.org/notker-edition/vault.html
- Direkt auf V7 mit aktiviertem nhd.-Toggle:
  https://dhcraft.org/notker-edition/#v=7&nhd=1
