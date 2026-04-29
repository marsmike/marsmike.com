---
title: marsmike.com v1 — Launch Site Design
status: approved
created: 2026-04-29
type: design-spec
project: marsmike.com
related:
  - "~/Documents/The-Void/02_Projects/social-amplification/"
  - "~/Documents/The-Void/Mike.md (locked identity §Public Brand Identity)"
  - "~/work/agentic-toolkit-public/ (target of first post)"
  - "~/work/vault-reader-eval/ (separate concern, vault.kube.im)"
---

# marsmike.com v1 — Launch Site Design

> v1 is the first real ship of marsmike.com — replacing the Cloudflare Pages "Coming Soon" placeholder with a bilingual blog launched alongside the public OSS release of `github.com/marsmike/agentic-toolkit`. Visual identity is locked at the typographic baseline below; structural identity is locked at the IA below.

## Goals

1. Replace "Coming Soon" with a working bilingual blog at `marsmike.com` today.
2. Ship the **launch post** — DE + EN — announcing the public OSS toolkit and re-establishing the Phase-1 "step by step" editorial promise that got cut from the live NSW LinkedIn caption.
3. Set the editorial standard for every future post: LinkedIn announces, marsmike.com goes deeper, with code links and reasoning.
4. Stay narrow. Out-of-scope cuts are deliberate (see §Non-Goals).

## Non-Goals (v1)

- Vault rendering at `/vault/`. That's `~/work/vault-reader-eval/` (Quartz frontrunner) shipping at `vault.kube.im`. Separate spec, separate ship.
- Talks page, separate code page, tag/category indexes, comments, newsletter capture, analytics beyond Cloudflare Pages defaults, custom logo, photography. All explicitly deferred.
- Anti-slop pre-commit hook (skipped per direction).
- Automated vault-to-repo sync. Lift-and-publish is manual by design (see §Authoring Flow).
- R2 bucket provisioning. Schema is future-proofed for `assets.marsmike.com` (see §Content Schema), but the bucket and DNS binding are deferred until the first post needs an artifact >25 MiB or worth a permanent URL. Decision triggered on demand, not today.

## Architecture

### Stack

- **Framework:** Astro 5 with MDX integration and content collections
- **Styling:** Tailwind CSS (utility-first, build-time tree-shaken)
- **Type system:** TypeScript with Zod-validated content frontmatter
- **Hosting:** Cloudflare Pages (Free plan), GitHub-connected to `marsmike/marsmike.com` (public repo)
- **Domain:** `marsmike.com` (canonical); `marsmike.de`, `marsmike.ai`, `marsmike.dev` already 301 to `.com` (unchanged)
- **Build target:** Static output. Zero JavaScript required to read a post. Astro islands only for the lang switcher and theme toggle (both <2 KB hydrated).

### Repo Layout

```
~/work/marsmike.com/
├── src/
│   ├── content/
│   │   ├── posts/
│   │   │   ├── de/                 # German posts (.md or .mdx)
│   │   │   └── en/                 # English posts (.md or .mdx)
│   │   └── config.ts               # Zod schemas for posts
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   └── PostLayout.astro
│   ├── pages/
│   │   ├── index.astro             # / → DE landing (default locale)
│   │   ├── about.astro             # /about (DE)
│   │   ├── posts/[slug].astro      # /posts/<slug> (DE)
│   │   ├── rss.xml.ts              # /rss.xml (DE)
│   │   └── en/
│   │       ├── index.astro         # /en/
│   │       ├── about.astro         # /en/about
│   │       ├── posts/[slug].astro  # /en/posts/<slug>
│   │       └── rss.xml.ts          # /en/rss.xml
│   ├── components/
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   ├── PostCard.astro
│   │   ├── LangSwitcher.astro
│   │   └── ThemeToggle.astro
│   └── styles/
│       └── global.css              # Tailwind base + custom font faces
├── public/
│   ├── fonts/                      # Inter + JetBrains Mono (self-hosted, woff2)
│   ├── favicon.svg
│   └── robots.txt
├── docs/
│   └── specs/                      # this directory
├── astro.config.mjs                # i18n: defaultLocale 'de', locales ['de','en']
├── tailwind.config.ts
├── tsconfig.json
├── package.json
├── README.md
├── LICENSE                         # MIT
└── .gitignore
```

### URL Structure

| Route | Purpose |
|---|---|
| `/` | DE landing — tagline + 5–10 most recent DE posts |
| `/posts/<slug>/` | DE post |
| `/about` | DE about page |
| `/rss.xml` | DE RSS feed |
| `/en/` | EN landing |
| `/en/posts/<slug>/` | EN post |
| `/en/about` | EN about page |
| `/en/rss.xml` | EN RSS feed |
| `/sitemap-index.xml` | sitemap (auto via `@astrojs/sitemap`) |

DE has no locale prefix because it is the default locale, matching the LinkedIn default-DE profile. Each post links to its sibling translation (when one exists) via `<link rel="alternate" hreflang="...">` and the in-page lang switcher.

### Content Schema (`src/content/config.ts`)

```ts
import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    summary: z.string().max(200),
    date: z.coerce.date(),
    lang: z.enum(['de', 'en']),
    status: z.enum(['draft', 'live']).default('live'),
    tags: z.array(z.string()).default([]),
    linkedin_url: z.string().url().optional(),
    code_url: z.string().url().optional(),
    translation_of: z.string().optional(), // sibling-language slug
    artifacts: z.array(z.object({
      label: z.string(),
      url: z.string().url(),
      type: z.enum(['video', 'pdf', 'pptx', 'image', 'audio', 'other']).default('other'),
    })).default([]),
  }),
});

export const collections = { posts };
```

- `lang` drives routing, RSS feed selection, `<html lang>`, `hreflang` tags.
- `status: 'draft'` posts are filtered out of production builds via `getCollection('posts', ({ data }) => data.status === 'live')`.
- `translation_of` powers the lang switcher; absent → switcher hidden.
- `linkedin_url` and `code_url` render as small badges in the post header when present.
- `artifacts` renders a labelled list at the foot of the post body when non-empty. Convention: artifact URLs point at `https://assets.marsmike.com/<path>` once the R2 bucket is provisioned. The schema accepts any URL today so external links work in the interim. Empty array (default) renders nothing.

## Authoring Flow

The blog repo is the canonical home for **published** posts. Drafts live in the Obsidian vault, where Mike already drafts everything else.

```
Vault (drafting)                          Repo (canonical published)
─────────────────                         ──────────────────────────
02_Projects/marsmike-com/                 src/content/posts/
  drafts/                                   de/<slug>.md
    YYYY-MM-DD-<slug>-de.md      lift  →   en/<slug>.md
    YYYY-MM-DD-<slug>-en.md      lift  →
  posts-published.md                        git push → Pages build → live
   (manual index of live URLs)         ←
```

### Why lift-and-publish, not sync

- The vault contains RAISE/Betriebsrat/BSH-firewalled material in adjacent folders. A sync script that maps wikilinks AND enforces the firewall is its own project — explicitly the `vault.kube.im` work, not v1 of marsmike.com.
- Lift-and-publish makes every commit to the public repo a deliberate public-release act. Firewall enforcement is manual and visible.
- `posts-published.md` in the vault is updated manually (slug → live URL → DE/EN status → LinkedIn URL). Manual is fine at the expected weekly publish rate; automate later if friction shows up.

### Bilingual Rules

- For the **launch post specifically**: ship DE + EN simultaneously. Both LinkedIn versions go up within ~4 days; the website is the deeper artifact both posts link to.
- For **routine posts after launch**: continue the existing DE-first / EN-3-days-later LinkedIn rhythm. The blog mirrors it. DE post and EN post are independent — schema permits a DE-only or EN-only post (lang switcher hides when no sibling).
- Voice checks (banned words, em-dash count, EN contraction density, DE complete-sentence rider) run **manually before lift**, per the existing voice spec. No build-time enforcement in v1.

## Visual & Brand Baseline

### Principles

- Typography-first. No hero illustrations, gradients, or animated landings.
- Self-hosted fonts. No Google Fonts call (faster, GDPR-clean for DACH audience without a banner).
- Light + dark mode. System-preference default with manual toggle. Both pre-rendered, no FOUC.
- Mobile-first. Phase-1 audience reads LinkedIn on phones and follows links on the same device.
- Zero JS to read a post. Tiny islands only for lang switcher and theme toggle.

### Typography

| Use | Family | Notes |
|---|---|---|
| Body | Inter (variable, self-hosted woff2) | DE umlauts clean, excellent at small sizes |
| Mono | JetBrains Mono (variable, self-hosted woff2) | inline `code`, code blocks, slug accents |

Body size `1.0625rem`, line-height `1.6`, measure ~70 chars. Headings use the same family with weight + size variation; no separate display face.

### Color Tokens

```
Light mode                       Dark mode
─────────                        ─────────
bg     #fafaf9 (warm off-white)  bg     #0c0c0d
text   #1a1a1a                   text   #e8e8e6
muted  #6b6b68                   muted  #9a9a96
border #e5e5e0                   border #2a2a28
accent #b8442a (Mars-rust)       accent #b8442a
```

The accent (Mars-rust) appears on links, the LinkedIn/code badges in post headers, the focus ring, and inline `code` highlight backgrounds. Same value in both modes.

### Layout Components

- **Header:** site title (text only, `marsmike.com`) left; nav (`Posts` / `About` / lang toggle / theme toggle) right; sticky on scroll, thin border.
- **Landing (`/` and `/en/`):** one-line tagline (lifted from locked LinkedIn headline), 5–10 most recent posts as a list (date · title · 1-line summary). No hero, no email capture, no subscribe pop-up.
- **Post page:** title, date, lang switcher (when sibling exists), summary, body. Two badges in header when frontmatter sets them: `LinkedIn ↗` and `Code ↗`. Footer: prev/next post in same language + RSS link.
- **About page:** locked LinkedIn About copy lifted verbatim. One-line "Mike Müller · Senior Software Engineer @ BSH · Regensburg" header. Contact strip at bottom: `mike@marsmike.com` · LinkedIn · GitHub · X. No photo in v1.
- **Footer:** `marsmike.com · MIT-licensed source · RSS · GitHub · LinkedIn · @MarsMike`. No copyright spam, no "made with Astro" badge.

### Logo / Favicon

- Wordmark only: `marsmike` set in Inter Bold, no glyph.
- Favicon: an "m" or "mm" in Inter Bold, white-on-Mars-rust.
- A real logo is deferred until the YouTube `@MarsMikeDev` channel launch.

## First Content (v1 ship)

### Post — `agentic-toolkit-open-sourced` (DE + EN simultaneous)

**Slug:** `agentic-toolkit-open-sourced` (same in both languages, sibling via `translation_of`).

**Frontmatter (DE):**
```yaml
title: "Mein Agentic Toolkit ist jetzt open source"  # working title
summary: "..."                                        # 1-line, ≤200 chars
date: 2026-04-29
lang: de
status: live
tags: ["agentic-toolkit", "claude-code", "oss"]
linkedin_url: "<filled retroactively when LinkedIn post is live>"
code_url: "https://github.com/marsmike/agentic-toolkit"
translation_of: "agentic-toolkit-open-sourced"
```

(EN frontmatter mirrors with `lang: en` and an EN title.)

**Length:** 600–800 words.

**Structure** (paragraphs only, no inline headings — LinkedIn-import readability):

1. **Hook (stance).** Most marketplaces drop everything at once and ask the audience to figure out what matters. This one releases plugins one at a time, in the order I'd hand them to a colleague. Translation craft applied to OSS.
2. **What's there today.** Public skeleton at `github.com/marsmike/agentic-toolkit`. MIT license. DCO sign-off for contributions. One paragraph on the marketplace shape (a `.claude-plugin/marketplace.json` registering plugins as they land).
3. **Why one-at-a-time.** Each plugin is its own teaching artifact. Big-bang launches optimize for repo stars, not for the engineer who'd actually use one of these tomorrow.
4. **What's first.** `feinschliff` lands today. One paragraph: what it does (Claude Design HTML → brand-perfect PowerPoint), why it's the anchor (the most-used plugin in my own day-to-day), the post about feinschliff specifically follows once it's live.
5. **What this site is for.** Phase-1 promise restated explicitly: research and practice from this past year, posted in plain language, one piece at a time. RSS link, LinkedIn link, no email capture, no subscribe form.

**Voice firewall checks (run manually before lift):**

- Zero banned words: `leverage`, `delve`, `robust`, `holistic`, `tapestry`, `seamless`, `landscape`, `navigate`, `synergy`, `foster`, `underscore`, `resonate`, `nuanced`, `comprehensive`, `streamline`, `empower`
- Zero banned transitions: `Furthermore`, `Moreover`, `Additionally`, `That being said`
- Banned structure (intro→balanced→summary→optimistic-close) avoided
- ≤3 em-dashes per language version
- EN: ≥1 contraction per 100 words
- DE: complete sentences, conjunctions present (German voice rider — no EN-fragment rhythm)
- RAISE firewall clean (role-level only; no Feinschliff internals or BSH brand-compiler specifics)
- Betriebsrat firewall: not invoked
- BSH form: unslashed; ideally not mentioned
- Stance line in opener and closer

### About page — `/about` (DE) and `/en/about` (EN)

- Body: locked LinkedIn About copy from `02_Projects/social-amplification/linkedin-about-drafts-2026-04-28.md`, lifted verbatim. Already voice-checked and firewall-clean.
- Header: one-line "Mike Müller · Senior Software Engineer @ BSH · Regensburg".
- Footer of page: contact strip — `mike@marsmike.com` · LinkedIn · GitHub · X (`@MarsMike`).
- No photo in v1.

## Deploy & Operations

The existing Cloudflare Pages project named **`marsmike`** (subdomain `marsmike.pages.dev`, currently serving "Coming Soon") is the deploy target. Project source is **Direct Upload** (no git connection); we keep that mode and deploy via `wrangler pages deploy` from local. No new project is created and no custom-domain swap happens — `marsmike.com` stays bound to the same project throughout, eliminating the swap-window risk entirely.

### One-time setup

1. Create public GitHub repo `marsmike/marsmike.com` from the local `~/work/marsmike.com/` (for OSS-of-the-blog optics; the repo is the canonical source even though Pages doesn't pull from it).
2. Authenticate `wrangler` locally with the existing `CLOUDFLARE_API_TOKEN` (already in `~/.env`, scope verified to include Pages:Edit).
3. `marsmike.de`, `marsmike.ai`, `marsmike.dev` 301 redirects remain unchanged.

### Routine deploy

Two-step deploy on every release:

1. **Preview deploy** — `pnpm build && wrangler pages deploy dist --project-name=marsmike --branch=launch-preview` → URL `https://launch-preview.marsmike.pages.dev/`. Verify here.
2. **Production deploy** — `pnpm build && wrangler pages deploy dist --project-name=marsmike --branch=main` → goes live at both `marsmike.pages.dev` and `marsmike.com`.

Cloudflare Pages retains all prior deployments; rollback is a Promote-old-deployment action via API or dashboard, not a redeploy.

### Future cleanup (out of v1)

- GitHub Actions workflow that runs `pnpm build && wrangler pages deploy` on push to `main`, replacing the manual local step. Two-line addition; deferred until the manual workflow shows friction.

### Cost / Limits

- Cloudflare Pages Free plan covers v1 indefinitely:
  - 500 builds/month (we'll use ~weekly)
  - Unlimited static asset bandwidth and requests
  - 20,000 files / 25 MiB per file (well under)
  - 100 custom domains (we use 4)
  - 100k Pages Functions requests/day shared with Workers (only relevant if/when dynamic features get added)
- No paid tier needed unless dynamic features (search endpoint, contact form, auth) cross 100k requests/day. Migration would be `$5/mo` Workers Paid, not a stack rewrite.

### Out-of-band assets

- Files >25 MiB (e.g., a 4K teaser MP4) go to Cloudflare R2 or external host and embed by URL. Not in v1.

## Testing & Verification

v1 verification is intentionally light. Static site, no app behavior to test.

- **Build passes locally** (`pnpm build`) without errors or content schema violations.
- **`pnpm dev` smoke check:** landing renders, post renders, lang switcher works, theme toggle persists across reloads.
- **Lighthouse mobile spot check:** Performance ≥95, Accessibility ≥95 on `/posts/agentic-toolkit-open-sourced/`.
- **Manual link audit on the launch post:** code link resolves to repo, RSS validates (W3C feed validator).
- **DACH device check:** load on iPhone Safari (Mike's primary read device per vault-reader-eval) — typography legible, dark mode kicks in correctly, no horizontal scroll.

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Bad build hits production | Two-step deploy (`launch-preview` branch first, verify, then `main`). Cloudflare retains every prior deployment; if a bad one slips through, "Promote" the previous good deployment via API or dashboard — no redeploy needed. |
| Voice firewall fails in production | Manual checks before lift (per Authoring Flow). Mike's own readthrough. Cost of a slipped banned word is one git commit + redeploy. |
| feinschliff plugin doesn't land today | Launch post still ships — frame the feinschliff teaser as "landing in the next 24h" rather than committing to "today" if uncertain. |
| `wrangler` deploy fails (auth, quota, etc.) | API token verified before first run; quota is 500 builds/mo on Free, dwarfs publish rate; on auth failure check `CLOUDFLARE_API_TOKEN` scope still includes Pages:Edit. |

## Open Questions Left in v1 (intentionally deferred)

- **Comments / engagement loop.** None in v1. Reasonable later additions: Giscus (GitHub Discussions backed) or no comments at all. Decide when traffic justifies it.
- **Analytics.** Cloudflare Pages dashboard ships with basic numbers free. If/when richer attribution is wanted, evaluate Plausible / Umami self-hosted on `srv.kube.im`. Not v1.
- **Search.** Pagefind (build-time static search) is the natural fit when post count crosses ~10. Not v1.
- **Logo.** Wordmark only in v1. Real logo when YouTube `@MarsMikeDev` channel launch warrants it.

## Implementation Path (high level — full plan follows in writing-plans phase)

1. Scaffold Astro project in `~/work/marsmike.com/`.
2. Wire Tailwind + content schema + i18n config.
3. Build layouts, components, pages.
4. Self-host Inter + JetBrains Mono.
5. Lift LinkedIn About copy → DE + EN about pages.
6. Draft launch post (DE + EN) in vault, run voice checks, lift to repo.
7. Local build + smoke checks.
8. Push to GitHub, connect Cloudflare Pages, verify on preview URL.
9. Switch `marsmike.com` custom domain to new project.
10. Verify production. Update vault `posts-published.md` index.
11. Once feinschliff lands today, update launch post's `linkedin_url` if/when LinkedIn post follows.
