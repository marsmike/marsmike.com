---
title: "Feinschliff: ein typisiertes Komponentensystem für LLM-generierte Decks"
summary: "Feinschliff ist live. 34 gebackene Single-Slide-Templates pro Marke, 11 offen lizenzierte Brand-Packs und ein Slide-Pattern-Atlas, der auf dem aktuellen Branch Gestalt annimmt."
date: 2026-04-29
lang: de
status: live
tags: ["agentic-toolkit", "feinschliff", "claude-code", "powerpoint", "design-systems"]
code_url: "https://github.com/marsmike/agentic-toolkit/tree/main/feinschliff"
translation_of: "feinschliff-launch"
---

![Sechs Slides aus dem gleichnamigen Feinschliff-Brand-Pack](https://assets.marsmike.com/posts/feinschliff-launch/hero-grid.png)

Ein „Q1-Update“ kann ein KPI-Grid sein, eine 2×2-Matrix, ein Waterfall, ein Stacked-Bar-Chart, eine Agenda, eine Executive Summary oder eine Scorecard. Gleiches Thema, sechs unterschiedliche richtige Antworten, je nach Zielgruppe und Argument. Der schwierige Teil beim Generieren eines Decks ist nicht das Rendern. Er beginnt vorher: die richtige Folienform zu wählen, bevor das Rendering startet. *Feinschliff* ist um genau diese Entscheidung herum gebaut.

[Feinschliff](https://github.com/marsmike/agentic-toolkit/tree/main/feinschliff) ist ein [Claude-Code-Plugin](https://docs.claude.com/claude-code), das aus einem Briefing oder einem Rohdeck eine markenkonforme `.pptx` macht. `/deck` erstellt, poliert oder kritisiert ein Deck. `/compile` erzeugt ein v2-Template-Artefakt samt Katalogeintrag aus genau einer Designquelle: PowerPoint, HTML, Screenshot oder Brief. `/extend` existiert noch, ist aber nur noch ein veralteter dünner Wrapper um `/compile`.

**Der Baukasten.** Das aktuelle v2-Modell ist kein handgeschriebener Renderer mehr, der aus abstrakten Layout-Ideen auswählt. Jede Marke bringt **34 gebackene Single-Slide-`.pptx`-Templates** mit, dazu einen abgeleiteten Katalog mit Slot-Verträgen, Placeholder-Maps und Template-Hashes. Die Deck-Grammatik bleibt vertraut: *KPI-Grid*, *2-Column Cards*, *4-Column Cards*, *Waterfall*, *2×2-Matrix*, *Process Flow*, *Stacked Bar*, *Scorecard*, *Action Title*, *Executive Summary*, *Pyramid*, *Bar Chart*, *Line Chart*, *Table*, *Key Takeaways*, *Quote*, *Agenda*, Titel- und Kapitel-Varianten und der Rest des Systems. Aber der Laufzeitpfad ist jetzt konkret: kanonische Templates zuverlässig befüllen, Platzhalter per `idx` adressieren und das visuelle System markenübergreifend stabil halten.

![Animation der Layouts: Title, Chapter, KPI-Grid, 4-Column Cards, Bar Chart, Quote](https://assets.marsmike.com/posts/feinschliff-launch/showcase.gif)

**Ein Atlas für die Planung, nicht für den Look.** Die größte Architekturverschiebung auf dem aktuellen Branch ist eine neue `atlas/`-Schicht: **39 kuratierte Folienbeispiele aus 6 Domänen**, jeweils als Thumbnail plus strukturierte Metadaten zu narrativer Rolle, visuellem Genre, Headline-Muster, „what works“, „why it works“ und dem nächstliegenden Feinschliff-Layout. Es geht nicht darum, Quellfolien zu kopieren. Es geht darum, die Planung an realen Beispielen zu erden. Die Brand-Packs liefern den Look. Der Atlas liefert den Qualitätsmaßstab für den Transport der Aussage. Phase 1 ist der Korpus selbst. Phase 2, noch vertagt, ist die Retrieval-Schicht in `/deck`: Wenn das System eine Problemfolie für ein Pitch-Deck oder ein Vorher/Nachher-Argument für eine Keynote braucht, kann es konkrete Referenzmuster ziehen, statt sich nur auf Modellprior zu verlassen.

**Ein Baukasten, viele Marken.** Das Brand-Authoring ist inzwischen deutlich sauberer als die frühe `cp -R`-Geschichte. Feinschliff bringt **11 offen lizenzierte Brand-Packs** mit: die Feinschliff-Varianten, die komplette Catppuccin-Familie, Solarized, Nord, Dracula und Gruvbox. Fünf weitere Packs dienen nur als Demos, weil die Marken nicht frei redistribuierbar sind. Der Authoring-Vertrag ist jetzt ein einziges [`DESIGN.md`](https://github.com/marsmike/agentic-toolkit/tree/main/feinschliff/docs/brand-system.md), aus dem das System Templates, Katalog, Tokens und HTML-Referenzen ableitet. Das ist die eigentliche markensteckbare Bewegung: Brand-Spezifikation von Laufzeit-Artefakten trennen. Die breitere `DESIGN.md`-Interoperabilität mit [`awesome-design-md`](https://github.com/VoltAgent/awesome-design-md) ist inzwischen sauber auf v0.3 verschoben.

**Die Pipeline.** Fünf Phasen. *Ingest* liest den Input und erzeugt `content_plan.json` plus `design_brief.json`. Das *Approval Gate* zeigt das abgeleitete Briefing, bevor das aufwendige Rendering beginnt. *Plan* wählt die Layouts. *Build* füllt die Templates der aktiven Marke zu einer `.pptx`. *Verify* ist das elfklassige Sicherheitsnetz. `/compile` läuft parallel zu diesem Pfad: Dort werden Designquellen in Laufzeit-Artefakte übersetzt und vor dem Commit per phash visuell gegengeprüft.

**Der Verify-Lauf.** Wenn das Matching stimmt, gehen die meisten Decks sauber durch. Wenn das Matching falsch ist, fängt Verify das Restliche ab. Elf Fehlerklassen laufen parallel. Fünf visuelle: *Overflow*, *Empty Placeholder*, *Layout-Mismatch*, *Brand-Violation*, *Density*. Sechs rhetorische: *Claim-Title* (Titel ist ein Thema, keine Aussage), *One-Idea* (Folie argumentiert zwei Punkte), *Bullet-Dump* (keine innere Struktur), *Audience-Mismatch* (Tonalität passt nicht), *Red-Line-Break* (erzählerischer Faden bricht ab), *Curse-of-Knowledge* (setzt Kontext voraus, den das Publikum nicht hat). Eine Folie wird nur ausgeliefert, wenn alle elf grün sind. Iterationsbudget: drei Runden im Standardmodus, sechs im Perfektionsmodus. Das Plugin liefert niemals stillschweigend ein fehlerhaftes Deck aus.

```bash
/plugin marketplace add marsmike/agentic-toolkit
/deck "Q1-Update: 12 Launches, 3 Kunden, 4,2 Mio. EUR ARR"
```

Feinschliff ist der Anker des [agentic-toolkit](https://github.com/marsmike/agentic-toolkit), weil jedes weitere Plugin, das Visuals erzeugt, denselben Brand-Vertrag erben kann, sobald das Design-System stimmt. Die aktuelle öffentliche Form ist v0.2: 34 gebackene Templates pro Marke, `lib/pptx_fill`, 11 offene Brand-Packs und der elfklassige Verify-Lauf. Der aktuelle Branch legt die nächste Planungsschicht öffentlich dazu: Atlas Phase 1, ein Forschungskorpus mit 39 kuratierten Folien aus 6 Domänen. Das Retrieval dagegen kommt als Nächstes. Slow Plugins, slow polish.
