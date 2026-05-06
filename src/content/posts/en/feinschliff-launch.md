---
title: "Feinschliff: a typed component system for LLM-generated decks"
summary: "Feinschliff is live. 34 baked single-slide templates per brand, 11 openly licensed brand packs, and a slide-pattern atlas taking shape on the current branch."
date: 2026-04-29
lang: en
status: live
tags: ["agentic-toolkit", "feinschliff", "claude-code", "powerpoint", "design-systems"]
code_url: "https://github.com/marsmike/agentic-toolkit/tree/main/feinschliff"
translation_of: "feinschliff-launch"
---

![Six slides rendered from the eponymous Feinschliff brand pack](https://assets.marsmike.com/posts/feinschliff-launch/hero-grid.png)

A "Q1 update" can be a KPI grid, a 2×2 matrix, a waterfall, a stacked bar, an agenda, an executive summary, or a scorecard. Same topic, six different right answers; what's right depends on the audience and the argument. The hard part of generating a deck isn't rendering slides. It starts earlier: choosing the right slide pattern before rendering begins. *Feinschliff* — German for *fine polish* — is built around that decision.

[Feinschliff](https://github.com/marsmike/agentic-toolkit/tree/main/feinschliff) is a [Claude Code plugin](https://docs.claude.com/claude-code) that turns a brief or a rough deck into a brand-compliant `.pptx`. `/deck` creates, polishes, or critiques a deck. `/compile` produces a v2 template artifact and catalog entry from one design source: PowerPoint, HTML, screenshot, or brief. `/extend` still exists, but only as a deprecated thin wrapper over `/compile`.

**The Baukasten.** The current v2 model is not a hand-coded renderer choosing from abstract layout ideas. Each brand ships with **34 baked single-slide `.pptx` templates**, plus a derived catalog that records slot contracts, placeholder maps, and template hashes. The deck grammar is still familiar: *KPI Grid*, *2-Column Cards*, *4-Column Cards*, *Waterfall*, *2×2 Matrix*, *Process Flow*, *Stacked Bar*, *Scorecard*, *Action Title*, *Executive Summary*, *Pyramid*, *Bar Chart*, *Line Chart*, *Table*, *Key Takeaways*, *Quote*, *Agenda*, title and chapter variants, and the rest of the system. But the runtime path is now concrete: fill canonical templates reliably, address placeholders by `idx`, and keep the visual system stable across brands.

![Slides cycling — Title, Chapter, KPI Grid, 4-Column Cards, Bar Chart, Quote](https://assets.marsmike.com/posts/feinschliff-launch/showcase.gif)

**Atlas for planning, not for looks.** The biggest architecture shift on the current branch is a new `atlas/` layer: **39 curated slide exemplars across 6 domains**, each stored as a thumbnail plus structured metadata about narrative role, visual genre, headline pattern, what works, why it works, and the closest Feinschliff layout. The point is not to clone source slides. The point is to ground planning in real exemplars. Brand packs supply the look. The atlas supplies the message-transport bar. Phase 1 is the corpus itself. Phase 2, still deferred, is retrieval inside `/deck`'s planning step: when the system needs a problem-framing slide for a pitch deck or a before/after performance slide for a keynote, it can retrieve concrete patterns instead of leaning only on model prior.

**One Baukasten, many brands.** Brand authoring is now much cleaner than the early `cp -R` story. Feinschliff ships with **11 openly licensed brand packs** in the box: the eponymous Feinschliff variants, the full Catppuccin family, Solarized, Nord, Dracula, and Gruvbox. Five more packs ship as demo-only references because the trademarks are not redistributable. The authoring contract is a single [`DESIGN.md`](https://github.com/marsmike/agentic-toolkit/tree/main/feinschliff/docs/brand-system.md), from which the system derives templates, catalog, tokens, and HTML references. That is the real brand-pluggable move: separate the brand spec from the runtime artifacts. Broader [`awesome-design-md`](https://github.com/VoltAgent/awesome-design-md) interoperability is now a v0.3 item, not a v0.2 one.

**The pipeline.** Five phases. *Ingest* reads the input and produces `content_plan.json` plus `design_brief.json`. The *approval gate* shows the inferred brief before any expensive rendering. *Plan* picks the layouts. *Build* fills the active brand's templates into a `.pptx`. *Verify* is the eleven-class safety net. `/compile` sits beside that flow: it is the template-ingestion path that turns a design source into a runtime artifact and visually verifies it with phash before commit.

**The verify pass.** When matching is right, most decks pass clean. When matching is wrong, verify catches the residue. Eleven defect classes run in parallel. Five visual: *overflow*, *empty placeholder*, *layout mismatch*, *brand violation*, *density*. Six rhetorical: *claim-title* (title is a topic, not a claim), *one-idea* (slide argues two points), *bullet-dump* (no internal hierarchy), *audience-mismatch* (voice doesn't fit), *red-line-break* (narrative arc breaks), *curse-of-knowledge* (assumes context the audience doesn't have). A slide ships only when all eleven are green. Iteration budget: 3 default, 6 perfectionist. The plugin doesn't silently ship a defective deck and call it done.

```bash
/plugin marketplace add marsmike/agentic-toolkit
/deck "Q1 update: 12 launches, 3 customers, $4.2M ARR"
```

Feinschliff is the anchor of the [agentic-toolkit](https://github.com/marsmike/agentic-toolkit) because every other plugin that produces visuals can inherit the same brand contract once the design system is right. The current public shape is v0.2: 34 baked templates per brand, `lib/pptx_fill`, 11 open brand packs, and the eleven-class verify pass. The current branch adds the next planning layer in public: atlas phase 1, a research corpus of 39 curated slides across 6 domains. Retrieval against that atlas comes next. Slow plugins, slow polish.
