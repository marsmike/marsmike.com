---
title: "Feinschliff v0.2.0: from palette-swap to chrome-swap"
summary: "v0.2.0 is online: a public brand gallery with sixteen packs, an architecture that earns the brand-pluggable claim, and a fourteen-class verify pass."
date: 2026-05-06
publishTime: "12:00"
lang: en
status: live
tags: ["agentic-toolkit", "feinschliff", "claude-code", "design-systems", "powerpoint"]
code_url: "https://github.com/marsmike/agentic-toolkit/releases/tag/v0.2.0"
translation_of: "feinschliff-v0-2-0"
---

![Components-showcase rendered from the eponymous Feinschliff brand pack: the full component vocabulary in one slide](https://assets.marsmike.com/feinschliff/brand-previews/feinschliff/14-components-showcase.png)

Brand-pluggable was a claim in v0.1.0, not a proof. The proof is a different thing: the system has to carry four brands whose chrome rules are mutually exclusive, without the renderer adding special cases. That's [v0.2.0](https://github.com/marsmike/agentic-toolkit/releases/tag/v0.2.0). Alongside it, a [public brand gallery](https://marsmike.github.io/agentic-toolkit/brands/) renders all sixteen packs against all thirty-four layouts: 544 slides, click-through in the browser, before you install.

**From palette-swap to chrome-swap.** v0.1.0 swapped the palette and kept the form. Indigo became Mocha; Latte became Nord. Tasteful consistency, weak claim. v0.2.0 takes the claim seriously. Four new reference packs (marked in the repo as not for redistribution) carry chrome rules that don't compose:

- *Pack A* enforces sharp corners (radius 0) everywhere, no shadows, a 700/300 weight ladder with weight 500 explicitly absent. Depth comes from hairlines and brightness steps, never from shadows.
- *Pack B* uses fully-rounded pills (`radius=9999`) for CTAs, soft 8px cards, heavy OOXML shadows by default. 700/400 binary. Dark canvas.
- *Pack C* also uses sharp corners (radius 0), but never bolds display weight (500 is the cap), and treats negative letter-spacing as the editorial signature. Depth from hairlines and photographic brightness, no shadows.
- *Pack D* ships bespoke product-DNA chrome (a data-dense table tile as hero element, a colour gradient via OOXML `gradFill`, a light reset-footer band on a dark canvas), with strict separation between the numerics font and the copy font.

If the renderer can serve all of that through one primitive set (`add_button`, `add_chip`, `add_column(as_card=True)`, `add_section_marker`) without setting brand-specific branches, the architecture's load-bearing. If it can't, brand-pluggable was marketing. Concretely: `radius.btn = 0` produces sharp rectangles in *Pack A*. `radius.btn = 9999` produces fully-rounded pills in *Pack B*. Same call, `add_button(...)`. *Pack B* sets `shadow.elevated = "rgba(0,0,0,0.3) 0px 8px 8px"`. *Pack C* sets `shadow.elevated = "none"` and ignores the parameter. Four brands, one code path, four different decks.

![KPI grid in the Catppuccin Mocha variant: same layout slot, different open palette](https://assets.marsmike.com/feinschliff/brand-previews/catppuccin-mocha/07-kpi-grid.png)

**Eleven openly licensed brand packs** ship MIT in the repo: the Catppuccin family (Latte/Frappé/Macchiato/Mocha), Solarized, Nord, Dracula, Gruvbox, plus the Feinschliff variants. Bring your own brand? It's a single `DESIGN.md` in Google's open spec format plus one bake call:

```bash
mkdir -p feinschliff/brands/myco
$EDITOR feinschliff/brands/myco/DESIGN.md
uv run python scripts/bake_palette.py from-design-md --brand myco --base feinschliff
FEINSCHLIFF_BRAND=myco /deck "..."
```

**Atlas, phase 1.** Thirty-nine curated slide examples from six domains now live in the repo as the `atlas/` corpus, each with a thumbnail plus structured metadata for genre, headline pattern, and nearest Feinschliff layout. That's the planning layer, not in the path yet, not in retrieval. Phase 2 is the retrieval layer in `/deck`, deferred to a later release.

**Verify, now fourteen classes.** The defect list grew from eleven to fourteen. Three new rhetorical classes: `redundancy-overload` (two slides arguing the same point), `truncated-y-axis` (chart axis doesn't start at zero and visually exaggerates), `missing-baseline` (no reference value, KPI floats in a vacuum). Five visual plus nine rhetorical. A slide ships only when all fourteen are green, or the iteration budget runs out and the residual defects get acknowledged.

**Gallery as proof artefact.** 544 slides clickable, with carousel and lightbox. Don't take the claim from the README; take it from the pixels. That's the real shift in v0.2.0: the plugin doesn't just publish a new tag, it puts up a public showroom against which the brand-pluggable claim can be falsified.

```bash
/plugin marketplace add marsmike/agentic-toolkit
FEINSCHLIFF_BRAND=catppuccin-mocha /deck "Q1: 12 launches, 3 customers, $4.2M ARR"
```

**v0.3 is next.** Drop-in support for any `DESIGN.md` from [awesome-design-md](https://github.com/VoltAgent/awesome-design-md): Stripe, Vercel, Linear, Notion, whatever's open. Component-level fidelity beyond palette swap. Brand-pluggable doesn't get proven in the README, it gets proven at the point where the renderer makes the same call for a pill and a sharp corner without special handling. v0.2.0 surfaces that point; v0.3 opens the door for any brand whose owner has put the spec out in the open.
