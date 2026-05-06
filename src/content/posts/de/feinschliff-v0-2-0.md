---
title: "Feinschliff v0.2.0: vom Palette-Swap zum Chrome-Swap"
summary: "v0.2.0 ist online: eine öffentliche Brand-Galerie mit sechzehn Packs, eine Architektur, die das Brand-Pluggable-Versprechen einlöst, und ein vierzehnklassiger Verify-Lauf."
date: 2026-05-06
publishTime: "12:00"
lang: de
status: live
tags: ["agentic-toolkit", "feinschliff", "claude-code", "design-systems", "powerpoint"]
code_url: "https://github.com/marsmike/agentic-toolkit/releases/tag/v0.2.0"
translation_of: "feinschliff-v0-2-0"
---

![Components-Showcase aus dem eponymen Feinschliff-Brand-Pack: die volle Komponenten-Vokabel in einer Folie](https://assets.marsmike.com/feinschliff/brand-previews/feinschliff/14-components-showcase.png)

Brand-Pluggable war in v0.1.0 ein Anspruch, kein Beweis. Der Beweis ist eine andere Sache: Das System muss vier Marken tragen, deren Chrome-Regeln sich gegenseitig ausschließen, ohne dass der Renderer Sonderfälle einbaut. Genau das ist [v0.2.0](https://github.com/marsmike/agentic-toolkit/releases/tag/v0.2.0). Parallel dazu eine [öffentliche Brand-Galerie](https://marsmike.github.io/agentic-toolkit/brands/), die alle sechzehn Packs gegen alle vierunddreißig Layouts zeigt: 544 Folien, klickbar im Browser, vor der Installation.

**Vom Palette-Swap zum Chrome-Swap.** v0.1.0 schwenkte die Farbpalette und ließ die Form. Indigo wurde Mocha; Latte wurde Nord. Schöne Konsistenz, schwacher Anspruch. v0.2.0 nimmt den Anspruch ernst. Vier neue Referenz-Packs (im Repo nicht für Redistribution markiert) tragen Chrome-Regeln, die sich gegenseitig ausschließen:

- *Pack A* setzt scharfe Ecken (Radius 0) überall, keine Schatten, 700/300-Gewichtsleiter mit explizit fehlender 500. Tiefe entsteht aus Hairlines und Helligkeitsstufen, nie aus Schatten.
- *Pack B* setzt vollständig abgerundete Pillen (`radius=9999`) für CTAs, weich abgerundete 8-px-Karten, schwere OOXML-Schatten als Standard. 700/400 binär. Dunkler Canvas.
- *Pack C* setzt ebenfalls scharfe Ecken (Radius 0), aber niemals fettes Display-Gewicht (500 als Maximum), negatives Buchstaben-Tracking als editorialer Akzent. Tiefe aus Hairlines und Foto-Helligkeit, ebenfalls keine Schatten.
- *Pack D* setzt maßgeschneiderte Produkt-DNA-Chrome (datendichte Tabellen-Kachel als Hero-Element, Farbgradient als OOXML-`gradFill`, helle Reset-Footer-Zone auf dunklem Canvas), mit strikter Trennung zwischen Numerik-Font und Copy-Font.

Wenn der Renderer das alles über denselben Primitiven-Satz bedient, also `add_button`, `add_chip`, `add_column(as_card=True)`, `add_section_marker`, ohne Brand-Sonderfälle zu setzen, ist die Architektur tragfähig. Wenn nicht, war Brand-Pluggable Marketing. Konkret: `radius.btn = 0` produziert in *Pack A* scharfe Rechtecke. `radius.btn = 9999` produziert in *Pack B* vollständig abgerundete Pillen. Beides über denselben Aufruf `add_button(...)`. *Pack B* setzt `shadow.elevated = "rgba(0,0,0,0.3) 0px 8px 8px"`. *Pack C* setzt `shadow.elevated = "none"` und ignoriert den Parameter. Vier Marken, ein Code-Pfad, vier verschiedene Decks.

![KPI-Grid in der Catppuccin-Mocha-Variante: gleicher Layout-Slot, andere offene Palette](https://assets.marsmike.com/feinschliff/brand-previews/catppuccin-mocha/07-kpi-grid.png)

**Elf offen lizenzierte Brand-Packs** sitzen MIT-lizenziert im Repo: die Catppuccin-Familie (Latte/Frappé/Macchiato/Mocha), Solarized, Nord, Dracula, Gruvbox sowie die Feinschliff-Varianten. Eigene Marke? Eine einzige `DESIGN.md` im Google-offenen Spec-Format plus ein Bake-Aufruf:

```bash
mkdir -p feinschliff/brands/myco
$EDITOR feinschliff/brands/myco/DESIGN.md
uv run python scripts/bake_palette.py from-design-md --brand myco --base feinschliff
FEINSCHLIFF_BRAND=myco /deck "..."
```

**Atlas, Phase 1.** Neununddreißig kuratierte Folienbeispiele aus sechs Domänen sitzen jetzt im Repo als `atlas/`-Korpus, jede mit Thumbnail plus strukturierten Metadaten zu Genre, Headline-Muster und nächstliegendem Feinschliff-Layout. Das ist die Planungsschicht, noch nicht im Pfad, noch nicht im Retrieval. Phase 2 ist die Retrieval-Schicht in `/deck` und kommt in einer späteren Version.

**Verify, jetzt vierzehn Klassen.** Die Defekt-Liste wuchs von elf auf vierzehn. Drei neue rhetorische Klassen: `redundancy-overload` (zwei Folien argumentieren denselben Punkt), `truncated-y-axis` (Chart-Achse beginnt nicht bei null und übertreibt visuell), `missing-baseline` (kein Vergleichswert, KPI hängt im Vakuum). Fünf visuelle plus neun rhetorische. Eine Folie geht raus, wenn alle vierzehn grün sind oder das Iterationsbudget aufgebraucht ist und die Restdefekte abgenickt werden.

**Galerie als Beweisartefakt.** 544 Folien klickbar, mit Karussell und Lightbox. Den Anspruch nicht aus dem README übernehmen, sondern aus den Pixeln. Das war der eigentliche Sprung in v0.2.0: Das Plugin liefert nicht nur ein neues Tag, sondern ein öffentliches Schaufenster, an dem sich der Anspruch falsifizieren lässt.

```bash
/plugin marketplace add marsmike/agentic-toolkit
FEINSCHLIFF_BRAND=catppuccin-mocha /deck "Q1: 12 Launches, 3 Kunden, 4,2 Mio. EUR ARR"
```

**v0.3 als Nächstes.** Drop-in für jede `DESIGN.md` aus [awesome-design-md](https://github.com/VoltAgent/awesome-design-md): Stripe, Vercel, Linear, Notion, was offen liegt. Komponenten-Treue jenseits Palette-Swap. Brand-Pluggable wird nicht im README bewiesen, sondern an dem Punkt, an dem der Renderer denselben Aufruf für Pille und scharfe Ecke macht, ohne Sonderbehandlung. v0.2.0 legt diesen Punkt offen; v0.3 öffnet die Tür für jede Marke, deren Eigentümer die Spec preisgegeben hat.
