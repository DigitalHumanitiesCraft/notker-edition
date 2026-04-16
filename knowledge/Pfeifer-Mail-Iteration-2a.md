---
type: draft
created: 2026-04-15
tags: [notker, pfeifer, email-draft]
status: draft
---

# Mail-Draft an Pfeifer — Iteration 2a

**Betreff:** Notker-Edition: Iteration 2 umgesetzt, zwei Bitten

**An:** philipp.pfeifer@uni-graz.at
**CC:** christopher.pollin@dhcraft.org

---

Lieber Philipp,

danke für das ausführliche Feedback vom 15.04. Wir haben die komplette Liste umgesetzt und eine zweite Iteration live. Der Link ist derselbe: https://dhcraft.org/notker-edition

Konkret drin:

- Alle ~20 Textkorrekturen (Quellen-Übersetzungen und neuhochdeutsche Übersetzung, inkl. chádensie → cháden sie, Köper → Körper, abgleitet etc.)
- V6: „ze_gótes sélbes ána-sihte" ist jetzt Haupttext statt Glosse, entsprechend in der nhd. Übersetzung eingearbeitet
- Die drei Bugs aus deiner Liste behoben: die lat./ahd.-Trennung funktioniert, das Quellenpanel lässt sich scrollen, die ×-Buttons schließen die Panels wirklich
- [Optional, wenn Phase B vor Mail fertig ist] Die Quellen-Übersetzungen aus dem Lateinischen sind jetzt kursiv, aus dem Althochdeutschen aufrecht — damit siehst du sofort, welcher Teil woher kommt
- [Optional, wenn Phase C fertig] Psalter G/R/H sind als Filter verfügbar, das rechte Panel lässt sich zwischen Handschrift, Wiener Notker und den Psaltern umschalten

Methodisch haben wir die Korrekturen nicht direkt in die TEI-Datei geschrieben, sondern als wiederholbare Errata-Regeln angelegt (`data/errata.yaml`). Das heißt: wenn du später noch Korrekturen nachreichst, baue ich die dort ein, und die ganze Pipeline läuft sauber durch — auch wenn die Originaldatei irgendwann wieder neu geparst wird. Das ist für den Skalierungs-Case (150 weitere Psalmen) wichtig.

**Zwei Bitten an dich:**

**1.** Augustinus 2 bei V3–5 und V6 konntest du nicht kontrollieren, weil das Quellenpanel nicht scrollbar war. Das geht jetzt. Magst du bitte dort nachschauen und mir eventuelle weitere Korrekturen schicken (gerne wieder als Liste)?

**2.** Für die zeilengetreue Darstellung (Grundtext und Übersetzung zeilenweise nebeneinander, ohne die Bindestrich-Artefakte) brauchen wir noch die Zeilenumbrüche des Grundtextes der Handschrift. Deine Übersetzung hat die Umbrüche als Bindestriche kodiert (danke, das hilft uns), aber beim Grundtext selbst liegen sie uns nicht als Marker vor. Hättest du sie in der DOCX oder in der Tax/Sehrt-Vorlage markiert — oder können wir sie aus dem Facsimile ableiten?

**Videocall für offene Architektur-Fragen:**

Drei Punkte würde ich gern kurz mit dir besprechen, bevor wir sie umsetzen — ein 30-Minuten-Termin reicht:

- **Panel-Flexibilität.** Du hattest Dropdowns in allen drei Feldern gewünscht. Mein Vorschlag: nur das rechte Panel bekommt ein Dropdown (Handschrift | Wiener Notker | G | R | H | Anmerkungen), die mittlere Edition-Spalte bleibt fest. Damit bleibt die von dir gelobte Drei-Spalten-Klarheit, und du kannst trotzdem Notker direkt neben G/R/H oder dem Wiener Notker sehen. Ist das ok für dich, oder willst du wirklich volle Flexibilität?

- **Siglen-Semantik G/R/H.** Wir behandeln sie provisorisch als Psalter-Zeugen (Filter-Layer wie die patristischen Quellen), mit dem Vorbehalt `@cert="low"` bis du bestätigst. Frage: sind G/R/H in Notkers Kommentar textkritische Varianten, oder bezeichnen sie den Psalter, aus dem er gerade zitiert? Das Zweite ist unsere Arbeitshypothese.

- **Kursiv-Konvention.** Wir haben entschieden: kursiv für Übersetzungen aus dem Lateinischen, aufrecht für Übersetzungen aus dem Althochdeutschen. Das folgt akademischer Konvention, damit du sofort siehst, welche Sprache Notker hier wiedergibt. Ok?

**Research Vault für den Antrag:**

Du hattest gefragt, ob deine Kolleginnen Zugriff auf unseren Research Vault bekommen können, um die Methodik zu beschreiben. Lieber nicht direkt aufs Repo — das ist unser Arbeitsbereich mit laufenden Zwischenständen. Stattdessen: wir bauen dir eine öffentliche, zitierbare Methodenbeschreibung auf dhcraft.org/notker-edition/methode und liefern zusätzlich ein PDF mit dem stabilen Antrags-Stand (Version, Datum, Verweis). Damit haben deine Kolleginnen einen soliden Anker, und du behältst die Kontrolle über den zitierten Stand.

Terminvorschläge für den Videocall: [bitte 2–3 Slots einfügen]

Liebe Grüße
Christian

---

## Anwendungshinweise

- **Anpassen vor Versand:** Optionale Bullets je nach Merge-Stand von Phase B/C aktivieren oder löschen.
- **Terminvorschläge:** zwei bis drei Slots einfügen (eigene Kalender-Lage prüfen).
- **Antragseinreichungsdatum fehlt noch im Vault** — falls Pfeifer es mitteilt, ACTIVE-WORK und Projekt-Overview nachziehen.
- **Augustinus-2-Korrekturen V3-5/V6** sind der einzige Textkorrektur-Rest, der von Pfeifer noch erwartet wird (blockiert durch BUG-11.2 — jetzt entblockt).
