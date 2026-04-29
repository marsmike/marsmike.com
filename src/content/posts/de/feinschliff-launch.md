---
title: "Feinschliff: eine typisierte Komponentenbibliothek für LLM-generierte Decks"
summary: "Feinschliff ist heute live. Rund 36 typisierte Layouts, Konzept-zu-Komponente-Matching, brand-pluggable Design-System. Das Plugin hinter jedem Deck, das ich ausliefere."
date: 2026-04-29
lang: de
status: live
tags: ["agentic-toolkit", "feinschliff", "claude-code", "powerpoint", "design-systems"]
code_url: "https://github.com/marsmike/agentic-toolkit/tree/main/feinschliff"
translation_of: "feinschliff-launch"
---

![Sechs Slides aus dem gleichnamigen Feinschliff-Brand-Pack](https://assets.marsmike.com/posts/feinschliff-launch/hero-grid.png)

Ein "Q1-Update" kann ein KPI-Grid sein, eine 2×2-Matrix, ein Waterfall, ein Stacked-Bar-Chart, eine Agenda, eine Executive Summary oder ein Scorecard. Gleiches Thema, sechs unterschiedliche richtige Antworten, je nach Zielgruppe und Argument. Der schwierige Teil beim Generieren eines Decks ist nicht das Befüllen der Slots mit Text. Es ist die Wahl, *welches Slot-Muster* überhaupt gefüllt werden soll. *Feinschliff* setzt darauf, dass das Matching von Inhaltsform auf Komponente das tragende Problem ist - alles andere kommt danach.

[Feinschliff](https://github.com/marsmike/agentic-toolkit/tree/main/feinschliff) ist ein [Claude-Code-Plugin](https://docs.claude.com/claude-code), das aus einem Content-Brief eine markenkonforme `.pptx` macht. Drei Befehle. `/deck` liest den Brief und produziert das Deck. `/extend` ergänzt ein neues Layout aus einem Screenshot, wenn der Katalog eine zusätzliche Form braucht. `/compile` regeneriert den Katalog, wenn sich das Design-System der Marke verändert.

**Der Baukasten.** Der Katalog liefert rund 36 typisierte Layouts, jedes eine andere Inhaltsform: *KPI-Grid* (2 bis 4 quantitative Werte mit Deltas), *2-Column Cards* (parallele Konzepte gleichen Gewichts), *4-Column Cards* (Q1-Q4-Pläne, Vier-Phasen-Roadmaps), *Waterfall* (Finanz-Brücken zwischen zwei Anker-Totalen), *2×2-Matrix* (Priorisierung mit einem Fokus-Quadranten), *Process Flow* (3 bis 6 sequenzielle Stufen mit Pfeilen), *Stacked Bar* (Mehrjahres-Mix über Kategorien), *Scorecard* (Optionen gegen Kriterien mit Harvey Balls), *Action Title* (McKinsey-typische Takeaway-Schlagzeile als Titel), *Executive Summary*, *Pyramid*, *Bar Chart*, *Line Chart*, *Table*, *Key Takeaways*, *Quote*, *Agenda*, plus Titel- und Kapitel-Varianten. Jedes Layout ist ein JSON-Schema mit typisierten Slots: `minItems`, `maxItems`, `maxLength` pro Feld. *KPI-Grid* verlangt 2 bis 4 KPIs, jeweils mit Wert, Key und optionalem Delta. *Process Flow* verlangt 3 bis 6 Steps, jeweils mit Counter und Heading. *Quote* ist ein einziger Slot, maximal 280 Zeichen, plus Attribution. Der Baukasten ist das Design-System, ausgedrückt als Daten.

![Animation der Layouts: Title, Chapter, KPI-Grid, 4-Column Cards, Bar Chart, Quote](https://assets.marsmike.com/posts/feinschliff-launch/showcase.gif)

**Konzept-zu-Komponente-Matching.** Jedes Layout im Katalog trägt Metadaten: wann es einzusetzen ist (Description), was es benötigt (Slot-Schema), zu welcher Zielgruppe und welcher narrativen Rolle es passt. Claude geht den Content-Plan Folie für Folie durch und matcht: *Inhaltsform* → *Zielgruppe* → *narrativer Rahmen* → *Layout*. Eine Idee mit sieben Bullets, die einem Vier-Slot-Layout übergeben wird, ist falsch; das Plugin wählt ein anderes Layout oder verteilt die Idee auf zwei Folien. Ein Exec-Publikum gewichtet kompakte Layouts wie *KPI-Grid* oder *Action Title* stärker als prosaische wie *Vertical Bullets* oder *Horizontal Bullets*. Ein SCQA-Narrativ bekommt Sektions-Eröffner und eine starke End-Folie. Beim Matching kommen Zielgruppe, narrativer Rahmen, Anti-Patterns und Slot-Beschränkungen in einer einzigen Entscheidung pro Folie zusammen. Die meisten Decks scheitern hier, nicht beim Rendern.

**Ein Baukasten, viele Marken.** Ein Brand-Pack ist Daten, kein Code. `tokens.json` ([DTCG-Draft-2-Design-Tokens](https://www.designtokens.org/)) plus eine Claude-Design-HTML-Referenz plus Renderer-Adapter, die beides lesen. Jedes Layout liest Tokens. Kein Renderer fest verdrahtet eine Farbe oder eine Schrift. `cp -R brands/feinschliff brands/meinco`, `tokens.json` und HTML anpassen, `FEINSCHLIFF_BRAND=meinco` setzen. Gleiche 36 Layouts, eigene visuelle Marke. Die gleichnamige Default-Marke kommt unter MIT (Indigo plus [Noto Sans](https://fonts.google.com/noto/specimen/Noto+Sans)), damit das System ab dem Moment der Installation eine Referenzmarke zum Demonstrieren hat. v0.2 nimmt jede [`DESIGN.md` aus awesome-design-md](https://github.com/VoltAgent/awesome-design-md) (Vercel, Linear, Notion, Stripe; 76 Design-Systeme) als direkten Brand-Pack-Input an. Eine reinwerfen, ein Deck im Stil der Firma rauskriegen.

**Die Pipeline.** Fünf Phasen. *Ingest* liest den Input und erzeugt `content_plan.json` (was jede Folie sagt) plus `design_brief.json` (Zielgruppe, narrativer Rahmen, Anti-Patterns). Das *Approval Gate* zeigt das abgeleitete Briefing, bevor das aufwendige Rendering beginnt. *Plan* ist der Ort, an dem das Matching passiert; jede Folie bekommt ihr Layout. *Build* rendert die .pptx über den Baukasten der aktiven Marke. *Verify* ist das elf-klassige Sicherheitsnetz.

**Der Verify-Lauf.** Wenn das Matching stimmt, gehen die meisten Decks sauber durch. Wenn das Matching falsch ist, fängt Verify das Restliche ab. Elf Defekt-Klassen laufen parallel. Fünf visuelle: *Overflow*, *Empty Placeholder*, *Layout-Mismatch*, *Brand-Violation*, *Density*. Sechs rhetorische: *Claim-Title* (Titel ist ein Thema, keine Aussage), *One-Idea* (Folie argumentiert zwei Punkte), *Bullet-Dump* (keine innere Struktur), *Audience-Mismatch* (Tonalität passt nicht), *Red-Line-Break* (erzählerischer Faden bricht ab), *Curse-of-Knowledge* (setzt Kontext voraus, den das Publikum nicht hat). Eine Folie wird nur ausgeliefert, wenn alle elf grün sind. Iterations-Budget: drei Runden im Standardmodus, sechs im Perfektionsmodus. Das Plugin liefert niemals stillschweigend ein fehlerhaftes Deck aus.

```bash
/plugin marketplace add marsmike/agentic-toolkit
/deck "Q1-Update: 12 Launches, 3 Kunden, 4,2 Mio. EUR ARR"
```

Feinschliff ist der Anker des [agentic-toolkit](https://github.com/marsmike/agentic-toolkit), weil jedes weitere Plugin, das Visuals erzeugt (Slides, Video-Frames, Infografiken, Social-Cards), denselben Baukasten und dasselbe Token-System erbt, sobald das Design-System stimmt. v0.1.0 liefert den Katalog, die Matching-Engine, den elf-klassigen Verify-Lauf und das gleichnamige Brand-Pack. Slow Plugins, slow polish.
