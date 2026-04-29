---
title: "Feinschliff: a typed component library for LLM-generated decks"
summary: "Feinschliff lands today. ~36 typed layouts, concept-to-component matching, brand-pluggable design system. The plugin behind every deck I ship."
date: 2026-04-29
lang: en
status: live
tags: ["agentic-toolkit", "feinschliff", "claude-code", "powerpoint", "design-systems"]
code_url: "https://github.com/marsmike/agentic-toolkit/tree/main/feinschliff"
translation_of: "feinschliff-launch"
---

![Six slides rendered from the eponymous Feinschliff brand pack](https://assets.marsmike.com/posts/feinschliff-launch/hero-grid.png)

A "Q1 update" can be a KPI grid, a 2×2 matrix, a waterfall, a stacked bar, an agenda, an executive summary, or a scorecard. Same topic, six different right answers; what's right depends on the audience and the argument. The hard part of generating a deck isn't filling slots with text. It's picking *which slot pattern* to fill in the first place. *Feinschliff* — German for *fine polish* — bets that matching content shape to component is the load-bearing problem; everything else is downstream.

[Feinschliff](https://github.com/marsmike/agentic-toolkit/tree/main/feinschliff) is a [Claude Code plugin](https://docs.claude.com/claude-code) that turns a content brief into a brand-perfect `.pptx`. Three commands. `/deck` ingests a brief and produces the deck. `/extend` adds a new layout from a screenshot when the catalog needs another shape. `/compile` regenerates the catalog when the brand's design system updates.

**The Baukasten.** The catalog ships with about 36 typed layouts, each one a different content shape: *KPI Grid* (2 to 4 quantitative figures with deltas), *2-Column Cards* (parallel concepts of equal weight), *4-Column Cards* (Q1-Q4 plans, four-phase roadmaps), *Waterfall* (financial bridges between two anchor totals), *2×2 Matrix* (prioritization with one focus quadrant), *Process Flow* (3 to 6 sequential stages with chevrons), *Stacked Bar* (multi-year mix across categories), *Scorecard* (compare options against criteria with Harvey balls), *Action Title* (McKinsey-style takeaway as the title), *Executive Summary*, *Pyramid*, *Bar Chart*, *Line Chart*, *Table*, *Key Takeaways*, *Quote*, *Agenda*, plus title and chapter variants. Each layout is a JSON schema with typed slots: `minItems`, `maxItems`, `maxLength` per field. *KPI Grid* requires 2 to 4 KPIs, each with a value, key, and optional delta. *Process Flow* requires 3 to 6 steps, each with a counter and heading. *Quote* is one slot, max 280 chars, plus attribution. The Baukasten is the design system, expressed as data.

![Slides cycling — Title, Chapter, KPI Grid, 4-Column Cards, Bar Chart, Quote](https://assets.marsmike.com/posts/feinschliff-launch/showcase.gif)

**Concept-to-component matching.** Each layout in the catalog carries metadata: when to use it (description), what it requires (slot schema), what audience and narrative role it fits. Claude walks the content plan slide-by-slide and matches: *content shape* → *audience* → *narrative frame* → *layout*. A 7-bullet idea handed to a 4-slot layout is wrong; the engine picks something else, or splits the idea across two slides. An exec-audience deck weights short-form layouts (KPI Grid, Action Title) over verbose ones (Vertical Bullets, Horizontal Bullets). A SCQA narrative gets section openers and a strong end-state slide. Matching is the place where audience, narrative frame, anti-patterns, and slot constraints all combine into one decision per slide. Most decks fail here, not in rendering.

**One Baukasten, many brands.** A brand pack is data, not code. `tokens.json` ([DTCG draft-2 design tokens](https://www.designtokens.org/)) plus a Claude Design HTML reference plus renderer adapters that read both. Every layout reads tokens. No renderer hardcodes a color or a font. `cp -R brands/feinschliff brands/myco`, edit `tokens.json` and the HTML, set `FEINSCHLIFF_BRAND=myco`. Same 36 layouts, your visual brand. The eponymous default ships under MIT (indigo plus [Noto Sans](https://fonts.google.com/noto/specimen/Noto+Sans)) so the system has a reference brand to demonstrate against from the moment you install. v0.2 will accept any [`DESIGN.md` from awesome-design-md](https://github.com/VoltAgent/awesome-design-md) (Vercel, Linear, Notion, Stripe; 76 design systems) as direct brand-pack input. Drop one in. You'll get a deck styled like that company.

**The pipeline.** Five phases. *Ingest* reads the input and produces `content_plan.json` (what every slide says) plus `design_brief.json` (audience, narrative frame, anti-patterns). The *approval gate* shows you the inferred brief before any expensive rendering. *Plan* is where the matching happens; every slide gets its layout. *Build* renders the .pptx through the active brand's Baukasten. *Verify* is the eleven-class safety net.

**The verify pass.** When matching is right, most decks pass clean. When matching is wrong, verify catches the residue. Eleven defect classes run in parallel. Five visual: *overflow*, *empty placeholder*, *layout mismatch*, *brand violation*, *density*. Six rhetorical: *claim-title* (title is a topic, not a claim), *one-idea* (slide argues two points), *bullet-dump* (no internal hierarchy), *audience-mismatch* (voice doesn't fit), *red-line-break* (narrative arc breaks), *curse-of-knowledge* (assumes context the audience doesn't have). A slide ships only when all eleven are green. Iteration budget: 3 default, 6 perfectionist. The plugin doesn't silently ship a defective deck and call it done.

```bash
/plugin marketplace add marsmike/agentic-toolkit
/deck "Q1 update: 12 launches, 3 customers, $4.2M ARR"
```

Feinschliff is the anchor of the [agentic-toolkit](https://github.com/marsmike/agentic-toolkit) because every other plugin that produces visuals (slides, video frames, infographics, social cards) inherits the same Baukasten and the same token system once the design system is right. v0.1.0 ships the catalog, the matching engine, the eleven-class verify, and the eponymous brand pack. Slow plugins, slow polish.
