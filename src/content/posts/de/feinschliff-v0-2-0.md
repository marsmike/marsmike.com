---
title: "Feinschliff v0.2.0: vom Palette-Swap zum Chrome-Swap"
summary: "v0.2.0 ist online: eine öffentliche Brand-Galerie mit sechzehn Packs, eine Architektur, die das Brand-Pluggable-Versprechen einlöst, und ein Verify-Lauf mit vierzehn Defekt-Klassen."
date: 2026-05-06
publishTime: "12:00"
lang: de
status: live
tags: ["agentic-toolkit", "feinschliff", "claude-code", "design-systems", "powerpoint"]
code_url: "https://github.com/marsmike/agentic-toolkit/releases/tag/v0.2.0"
translation_of: "feinschliff-v0-2-0"
---

![Components-Showcase aus dem eponymen Feinschliff-Brand-Pack: die volle Komponenten-Vokabel in einer Folie](https://assets.marsmike.com/feinschliff/brand-previews/feinschliff/14-components-showcase.png)

In v0.1.0 war Brand-Pluggable ein Anspruch, kein Beweis. Brand-Pluggable heißt: Dasselbe Plugin soll beliebige Marken bedienen können, ohne dass der Renderer angepasst wird. Beweisen lässt sich das nur, wenn vier Marken mit gegensätzlichen Gestaltungsregeln durch dasselbe System laufen, ohne dass der Code Sonderfälle einbaut. Genau das ist [v0.2.0](https://github.com/marsmike/agentic-toolkit/releases/tag/v0.2.0). Dazu kommt eine [öffentliche Brand-Galerie](https://marsmike.github.io/agentic-toolkit/brands/), die alle sechzehn Packs in allen vierunddreißig Layouts zeigt: 544 Folien, schon vor der Installation klickbar im Browser.

**Vom Palette-Swap zum Chrome-Swap.** v0.1.0 tauschte nur die Farbpalette aus und ließ die Form unverändert. Indigo wurde Mocha; Latte wurde Nord. Das ergab schöne Konsistenz, aber einen schwachen Anspruch. v0.2.0 nimmt den Anspruch ernst: Vier neue Referenz-Packs (im Repo nicht zur Weitergabe freigegeben) bringen Gestaltungsregeln mit, die sich gegenseitig ausschließen:

- *Pack A* hat überall scharfe Ecken (Radius 0), keine Schatten, eine 700/300-Gewichtsleiter, in der die 500 explizit fehlt. Tiefe entsteht aus Hairlines und Helligkeitsstufen, nie aus Schatten.
- *Pack B* nutzt vollständig abgerundete Pillen (`radius=9999`) für CTAs, weich abgerundete 8-px-Karten und schwere OOXML-Schatten als Standard. 700/400 binär. Dunkler Canvas.
- *Pack C* hat ebenfalls scharfe Ecken (Radius 0), aber nie fettes Display-Gewicht (500 als Maximum) und negative Laufweite als redaktionellen Akzent. Tiefe aus Hairlines und Foto-Helligkeit, ebenfalls keine Schatten.
- *Pack D* bringt maßgeschneiderte Produkt-DNA-Chrome (datendichte Tabellen-Kachel als Hero-Element, Farbgradient als OOXML-`gradFill`, helle Reset-Footer-Zone auf dunklem Canvas), mit strikter Trennung zwischen Numerik-Font und Copy-Font.

Wenn der Renderer das alles über denselben Satz von Grund-Funktionen bedient, also `add_button`, `add_chip`, `add_column(as_card=True)`, `add_section_marker`, und dabei ohne markenspezifische Sonderfälle auskommt, dann trägt die Architektur. Wenn nicht, war Brand-Pluggable nur Marketing. Konkret: `radius.btn = 0` erzeugt in *Pack A* scharfe Rechtecke, `radius.btn = 9999` in *Pack B* vollständig abgerundete Pillen. Beides läuft über denselben Aufruf `add_button(...)`. *Pack B* setzt `shadow.elevated = "rgba(0,0,0,0.3) 0px 8px 8px"`, *Pack C* setzt `shadow.elevated = "none"` und ignoriert den Parameter. Vier Marken, ein Code-Pfad, vier unterschiedliche Decks.

![KPI-Grid in der Catppuccin-Mocha-Variante: gleicher Layout-Slot, andere offene Palette](https://assets.marsmike.com/feinschliff/brand-previews/catppuccin-mocha/07-kpi-grid.png)

**Elf offen lizenzierte Brand-Packs** liegen MIT-lizenziert im Repo: die Catppuccin-Familie (Latte/Frappé/Macchiato/Mocha), Solarized, Nord, Dracula, Gruvbox sowie die Feinschliff-Varianten. Eine eigene Marke einbauen? Dafür reicht eine einzige `DESIGN.md` im offenen Google-Spec-Format und ein Bake-Aufruf, der die Templates aus dieser Spec ableitet:

```bash
mkdir -p feinschliff/brands/myco
$EDITOR feinschliff/brands/myco/DESIGN.md
uv run python scripts/bake_palette.py from-design-md --brand myco --base feinschliff
FEINSCHLIFF_BRAND=myco /deck "..."
```

**Atlas, Phase 1.** Neununddreißig kuratierte Folienbeispiele aus sechs Domänen liegen jetzt im Repo als `atlas/`-Korpus, jeweils mit Thumbnail und strukturierten Metadaten zu Genre, Headline-Muster und nächstliegendem Feinschliff-Layout. Das ist erst die Planungsschicht: noch nicht im Build-Pfad, noch nicht in der Retrieval-Stufe. Phase 2 wird die Retrieval-Schicht in `/deck` und kommt in einer späteren Version.

**Verify, jetzt vierzehn Klassen.** Die Liste der geprüften Defekt-Klassen wuchs von elf auf vierzehn. Drei neue rhetorische Klassen kommen dazu: `redundancy-overload` (zwei Folien machen denselben Punkt), `truncated-y-axis` (die Chart-Achse beginnt nicht bei null und übertreibt visuell) und `missing-baseline` (kein Vergleichswert, der KPI hängt im Vakuum). Insgesamt fünf visuelle und neun rhetorische Klassen. Eine Folie wird nur ausgeliefert, wenn alle vierzehn grün sind, oder wenn das Iterationsbudget aufgebraucht ist und die verbliebenen Defekte explizit abgenickt werden.

**Galerie als Beweisartefakt.** Alle 544 Folien sind klickbar, mit Karussell und Lightbox. Wer den Anspruch prüfen will, übernimmt ihn nicht aus dem README, sondern aus den gerenderten Pixeln. Das war der eigentliche Sprung in v0.2.0: Das Plugin liefert nicht nur ein neues Release-Tag, sondern ein öffentliches Schaufenster, an dem sich der Anspruch widerlegen lässt.

```bash
/plugin marketplace add marsmike/agentic-toolkit
FEINSCHLIFF_BRAND=catppuccin-mocha /deck "Q1: 12 Launches, 3 Kunden, 4,2 Mio. EUR ARR"
```

**v0.3 als Nächstes.** Direkt einsetzbar für jede `DESIGN.md` aus [awesome-design-md](https://github.com/VoltAgent/awesome-design-md): Stripe, Vercel, Linear, Notion und alles Weitere, was offen vorliegt. Treue auf Komponenten-Ebene, nicht nur in der Farbpalette. Brand-Pluggable wird nicht im README bewiesen, sondern dort, wo der Renderer denselben Aufruf für eine Pille und für eine scharfe Ecke macht, ohne Sonderbehandlung. v0.2.0 legt diesen Punkt offen; v0.3 öffnet die Tür für jede Marke, deren Eigentümer die Spec offengelegt hat.
