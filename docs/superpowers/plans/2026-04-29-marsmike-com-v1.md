# marsmike.com v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Cloudflare Pages "Coming Soon" with a working bilingual (DE-default, EN at `/en/`) Astro blog at `marsmike.com`, shipping the agentic-toolkit OSS launch post and About page on day one.

**Architecture:** Astro 5 + MDX + content collections, Tailwind 4 (CSS-first), Zod-validated frontmatter, self-hosted Inter + JetBrains Mono via `@fontsource-variable/*` packages, Cloudflare Pages on the Free plan via GitHub integration. Drafts authored in the Obsidian vault, manually lifted to `src/content/posts/{de,en}/`. Mars-rust accent (`#b8442a`); warm-neutral palette; light + dark mode with system-preference default and persistent manual toggle.

**Tech Stack:** Astro 5, MDX, Tailwind CSS 4, TypeScript, pnpm, `@astrojs/mdx`, `@astrojs/sitemap`, `@astrojs/rss`, `@fontsource-variable/inter`, `@fontsource-variable/jetbrains-mono`, Cloudflare Pages, GitHub Actions (none — Pages handles build).

**Spec:** `~/work/marsmike.com/docs/specs/2026-04-29-marsmike-com-v1-design.md`

---

## File Structure

| File | Responsibility |
|---|---|
| `package.json` | Dependencies, scripts |
| `pnpm-lock.yaml` | Lockfile |
| `astro.config.mjs` | Astro config: integrations, i18n, site URL, Vite plugins |
| `tsconfig.json` | TypeScript config (Astro defaults) |
| `tailwind.config.ts` | (none — Tailwind 4 is CSS-first; tokens live in `global.css`) |
| `src/content/config.ts` | Zod schema for `posts` collection |
| `src/styles/global.css` | Tailwind import, font faces, design tokens, base styles |
| `src/layouts/BaseLayout.astro` | HTML scaffold, head metadata, theme + locale wiring |
| `src/layouts/PostLayout.astro` | Post page wrapping logic |
| `src/components/Header.astro` | Site header — title, nav, lang toggle, theme toggle |
| `src/components/Footer.astro` | Site footer — minimal contact strip |
| `src/components/PostCard.astro` | Single post entry on landing page |
| `src/components/LangSwitcher.astro` | DE↔EN switcher (only when sibling exists) |
| `src/components/ThemeToggle.astro` | Light/dark toggle with localStorage |
| `src/pages/index.astro` | DE landing — `/` |
| `src/pages/about.astro` | DE about — `/about` |
| `src/pages/posts/[slug].astro` | DE post route — `/posts/<slug>/` |
| `src/pages/rss.xml.ts` | DE RSS feed — `/rss.xml` |
| `src/pages/en/index.astro` | EN landing — `/en/` |
| `src/pages/en/about.astro` | EN about — `/en/about` |
| `src/pages/en/posts/[slug].astro` | EN post route — `/en/posts/<slug>/` |
| `src/pages/en/rss.xml.ts` | EN RSS feed — `/en/rss.xml` |
| `src/content/posts/de/agentic-toolkit-open-sourced.md` | DE launch post |
| `src/content/posts/en/agentic-toolkit-open-sourced.md` | EN launch post |
| `public/favicon.svg` | Wordmark "m" favicon |
| `public/robots.txt` | Allow all, sitemap pointer |
| `LICENSE` | MIT |
| `.gitignore` | Node + Astro defaults |
| `README.md` | One-paragraph repo description |

---

## Tasks

### Task 1: Initialize repo and Astro scaffold

**Files:**
- Create: `~/work/marsmike.com/package.json`
- Create: `~/work/marsmike.com/astro.config.mjs`
- Create: `~/work/marsmike.com/tsconfig.json`
- Create: `~/work/marsmike.com/.gitignore`
- Create: `~/work/marsmike.com/LICENSE`
- Create: `~/work/marsmike.com/README.md`
- Init: `~/work/marsmike.com/.git/`

- [ ] **Step 1: Confirm working directory and init git**

```bash
cd ~/work/marsmike.com
git init -b main
```

Expected: `Initialized empty Git repository in ~/work/marsmike.com/.git/`

- [ ] **Step 2: Create `.gitignore`**

```gitignore
# build
dist/
.astro/

# dependencies
node_modules/

# env
.env
.env.production
.env.local

# logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# editor
.vscode/*
!.vscode/extensions.json
.idea/

# os
.DS_Store
Thumbs.db

# wrangler / cloudflare
.wrangler/
```

- [ ] **Step 3: Create `LICENSE` (MIT)**

```
MIT License

Copyright (c) 2026 Mike Müller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 4: Create `README.md`**

```markdown
# marsmike.com

Source for [marsmike.com](https://marsmike.com) — bilingual (DE/EN) blog by Mike Müller on software delivery in the GenAI era.

## Stack

Astro · Tailwind · TypeScript · Cloudflare Pages.

## Develop

```bash
pnpm install
pnpm dev
```

## License

MIT — see [LICENSE](LICENSE).
```

- [ ] **Step 5: Create `package.json`**

```json
{
  "name": "marsmike-com",
  "type": "module",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "astro dev",
    "start": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "astro": "astro"
  },
  "dependencies": {
    "astro": "^5.0.0",
    "@astrojs/mdx": "^4.0.0",
    "@astrojs/sitemap": "^3.2.0",
    "@astrojs/rss": "^4.0.0",
    "@fontsource-variable/inter": "^5.1.0",
    "@fontsource-variable/jetbrains-mono": "^5.1.0",
    "@tailwindcss/vite": "^4.0.0",
    "tailwindcss": "^4.0.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "typescript": "^5.6.0",
    "wrangler": "^3.90.0"
  },
  "packageManager": "pnpm@9.0.0"
}
```

- [ ] **Step 6: Create `tsconfig.json`**

```json
{
  "extends": "astro/tsconfigs/strict",
  "include": [".astro/types.d.ts", "**/*"],
  "exclude": ["dist"],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "~/*": ["src/*"]
    }
  }
}
```

- [ ] **Step 7: Create `astro.config.mjs`**

```js
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://marsmike.com',
  trailingSlash: 'always',
  i18n: {
    defaultLocale: 'de',
    locales: ['de', 'en'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
  integrations: [mdx(), sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
  build: {
    format: 'directory',
  },
});
```

- [ ] **Step 8: Install dependencies**

```bash
cd ~/work/marsmike.com
pnpm install
```

Expected: lockfile generated, `node_modules/` populated, no errors.

- [ ] **Step 9: First commit**

```bash
git add .
git commit -m "chore: initial scaffold (astro 5, tailwind 4, i18n config)"
```

---

### Task 2: Content collections schema

**Files:**
- Create: `~/work/marsmike.com/src/content/config.ts`
- Create: `~/work/marsmike.com/src/content/posts/de/.gitkeep`
- Create: `~/work/marsmike.com/src/content/posts/en/.gitkeep`

- [ ] **Step 1: Create `src/content/config.ts`**

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
    translation_of: z.string().optional(),
    artifacts: z.array(z.object({
      label: z.string(),
      url: z.string().url(),
      type: z.enum(['video', 'pdf', 'pptx', 'image', 'audio', 'other']).default('other'),
    })).default([]),
  }),
});

export const collections = { posts };
```

- [ ] **Step 2: Create empty content directories**

```bash
mkdir -p src/content/posts/de src/content/posts/en
touch src/content/posts/de/.gitkeep src/content/posts/en/.gitkeep
```

- [ ] **Step 3: Verify schema compiles**

```bash
pnpm astro sync
```

Expected: `success Generated types in .astro/`. No errors.

- [ ] **Step 4: Commit**

```bash
git add src/content/
git commit -m "feat: posts content collection with bilingual schema"
```

---

### Task 3: Design tokens and global styles

**Files:**
- Create: `~/work/marsmike.com/src/styles/global.css`

- [ ] **Step 1: Create `src/styles/global.css`**

```css
@import "tailwindcss";

@import "@fontsource-variable/inter/index.css";
@import "@fontsource-variable/jetbrains-mono/index.css";

@theme {
  --color-bg: #fafaf9;
  --color-text: #1a1a1a;
  --color-muted: #6b6b68;
  --color-border: #e5e5e0;
  --color-accent: #b8442a;

  --font-sans: 'Inter Variable', ui-sans-serif, system-ui, sans-serif;
  --font-mono: 'JetBrains Mono Variable', ui-monospace, 'SF Mono', monospace;

  --text-base: 1.0625rem;
  --leading-base: 1.6;

  --container-prose: 38rem;
}

@layer base {
  :root {
    color-scheme: light dark;
  }

  html.dark {
    --color-bg: #0c0c0d;
    --color-text: #e8e8e6;
    --color-muted: #9a9a96;
    --color-border: #2a2a28;
  }

  html {
    background-color: var(--color-bg);
    color: var(--color-text);
    font-family: var(--font-sans);
    font-size: var(--text-base);
    line-height: var(--leading-base);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  body {
    min-height: 100dvh;
  }

  a {
    color: var(--color-accent);
    text-decoration: underline;
    text-underline-offset: 0.2em;
    text-decoration-thickness: 1px;
  }

  a:hover {
    text-decoration-thickness: 2px;
  }

  code, pre {
    font-family: var(--font-mono);
  }

  :not(pre) > code {
    background-color: color-mix(in srgb, var(--color-accent) 10%, transparent);
    color: var(--color-text);
    padding: 0.1em 0.35em;
    border-radius: 3px;
    font-size: 0.92em;
  }

  pre {
    background-color: color-mix(in srgb, var(--color-text) 4%, var(--color-bg));
    border: 1px solid var(--color-border);
    border-radius: 6px;
    padding: 1rem;
    overflow-x: auto;
    font-size: 0.92em;
    line-height: 1.55;
  }

  :focus-visible {
    outline: 2px solid var(--color-accent);
    outline-offset: 2px;
  }

  ::selection {
    background-color: color-mix(in srgb, var(--color-accent) 30%, transparent);
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add src/styles/
git commit -m "feat: design tokens, font faces, light/dark color scheme"
```

---

### Task 4: ThemeToggle component

**Files:**
- Create: `~/work/marsmike.com/src/components/ThemeToggle.astro`

The toggle: cycles `system → light → dark → system`. Persists choice in `localStorage` under `theme`. Inline script in `BaseLayout` head (Task 6) avoids FOUC.

- [ ] **Step 1: Create `src/components/ThemeToggle.astro`**

```astro
---
// Tiny island. No props.
---

<button
  id="theme-toggle"
  type="button"
  aria-label="Toggle theme"
  class="text-[var(--color-muted)] hover:text-[var(--color-text)] transition-colors"
>
  <span class="sr-only">Theme</span>
  <span aria-hidden="true" data-theme-icon>◐</span>
</button>

<script is:inline>
  (() => {
    const btn = document.getElementById('theme-toggle');
    if (!btn) return;
    const icon = btn.querySelector('[data-theme-icon]');

    const apply = (mode) => {
      const root = document.documentElement;
      if (mode === 'system') {
        const sys = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        root.classList.toggle('dark', sys === 'dark');
      } else {
        root.classList.toggle('dark', mode === 'dark');
      }
      icon.textContent = mode === 'system' ? '◐' : mode === 'dark' ? '●' : '○';
      btn.setAttribute('title', `Theme: ${mode}`);
    };

    let mode = localStorage.getItem('theme') || 'system';
    apply(mode);

    btn.addEventListener('click', () => {
      mode = mode === 'system' ? 'light' : mode === 'light' ? 'dark' : 'system';
      if (mode === 'system') localStorage.removeItem('theme');
      else localStorage.setItem('theme', mode);
      apply(mode);
    });

    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      if ((localStorage.getItem('theme') || 'system') === 'system') apply('system');
    });
  })();
</script>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/ThemeToggle.astro
git commit -m "feat: theme toggle (system/light/dark, persisted)"
```

---

### Task 5: LangSwitcher component

**Files:**
- Create: `~/work/marsmike.com/src/components/LangSwitcher.astro`

Renders a small `DE | EN` link pair. Hides when no sibling translation is available on the current route.

- [ ] **Step 1: Create `src/components/LangSwitcher.astro`**

```astro
---
interface Props {
  currentLang: 'de' | 'en';
  siblingPath?: string; // e.g. "/en/posts/foo/" or "/posts/foo/"
}
const { currentLang, siblingPath } = Astro.props;
const otherLang = currentLang === 'de' ? 'en' : 'de';
const otherLabel = otherLang.toUpperCase();
const currentLabel = currentLang.toUpperCase();
---

<div class="flex items-center gap-2 text-sm text-[var(--color-muted)]">
  <span aria-current="true" class="text-[var(--color-text)]">{currentLabel}</span>
  {siblingPath ? (
    <>
      <span aria-hidden="true">·</span>
      <a href={siblingPath} hreflang={otherLang} class="no-underline hover:underline">
        {otherLabel}
      </a>
    </>
  ) : null}
</div>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/LangSwitcher.astro
git commit -m "feat: lang switcher (hides when no sibling translation)"
```

---

### Task 6: BaseLayout, Header, Footer

**Files:**
- Create: `~/work/marsmike.com/src/layouts/BaseLayout.astro`
- Create: `~/work/marsmike.com/src/components/Header.astro`
- Create: `~/work/marsmike.com/src/components/Footer.astro`

- [ ] **Step 1: Create `src/components/Header.astro`**

```astro
---
import LangSwitcher from './LangSwitcher.astro';
import ThemeToggle from './ThemeToggle.astro';

interface Props {
  lang: 'de' | 'en';
  siblingPath?: string;
}
const { lang, siblingPath } = Astro.props;
const homeHref = lang === 'de' ? '/' : '/en/';
const postsHref = lang === 'de' ? '/' : '/en/';
const aboutHref = lang === 'de' ? '/about/' : '/en/about/';
const aboutLabel = lang === 'de' ? 'Über' : 'About';
const postsLabel = lang === 'de' ? 'Beiträge' : 'Posts';
---

<header class="border-b border-[var(--color-border)] sticky top-0 backdrop-blur-sm bg-[var(--color-bg)]/85 z-10">
  <div class="max-w-3xl mx-auto px-5 py-4 flex items-center justify-between">
    <a href={homeHref} class="font-semibold no-underline text-[var(--color-text)] hover:text-[var(--color-accent)]">
      marsmike.com
    </a>
    <nav class="flex items-center gap-5 text-sm">
      <a href={postsHref} class="no-underline text-[var(--color-muted)] hover:text-[var(--color-text)]">{postsLabel}</a>
      <a href={aboutHref} class="no-underline text-[var(--color-muted)] hover:text-[var(--color-text)]">{aboutLabel}</a>
      <LangSwitcher currentLang={lang} siblingPath={siblingPath} />
      <ThemeToggle />
    </nav>
  </div>
</header>
```

- [ ] **Step 2: Create `src/components/Footer.astro`**

```astro
---
interface Props {
  lang: 'de' | 'en';
}
const { lang } = Astro.props;
const rssHref = lang === 'de' ? '/rss.xml' : '/en/rss.xml';
const sourceLabel = lang === 'de' ? 'Quellcode' : 'Source';
---

<footer class="border-t border-[var(--color-border)] mt-16">
  <div class="max-w-3xl mx-auto px-5 py-6 text-sm text-[var(--color-muted)] flex flex-wrap gap-x-4 gap-y-2 justify-between">
    <div>
      <span>marsmike.com</span>
      <span aria-hidden="true"> · </span>
      <a href="https://github.com/marsmike/marsmike.com" class="no-underline hover:underline">{sourceLabel} (MIT)</a>
    </div>
    <div class="flex gap-x-4">
      <a href={rssHref} class="no-underline hover:underline">RSS</a>
      <a href="https://github.com/marsmike" class="no-underline hover:underline">GitHub</a>
      <a href="https://www.linkedin.com/in/marsmike" class="no-underline hover:underline">LinkedIn</a>
      <a href="https://x.com/marsmike" class="no-underline hover:underline">X</a>
    </div>
  </div>
</footer>
```

- [ ] **Step 3: Create `src/layouts/BaseLayout.astro`**

```astro
---
import '~/styles/global.css';
import Header from '~/components/Header.astro';
import Footer from '~/components/Footer.astro';

interface Props {
  lang: 'de' | 'en';
  title: string;
  description: string;
  canonicalPath?: string;
  siblingPath?: string;
  ogType?: 'website' | 'article';
}

const {
  lang,
  title,
  description,
  canonicalPath = Astro.url.pathname,
  siblingPath,
  ogType = 'website',
} = Astro.props;

const siteUrl = 'https://marsmike.com';
const canonical = new URL(canonicalPath, siteUrl).toString();
const sibling = siblingPath ? new URL(siblingPath, siteUrl).toString() : undefined;
const otherLang = lang === 'de' ? 'en' : 'de';
---

<!doctype html>
<html lang={lang}>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={canonical} />
    {sibling ? (
      <link rel="alternate" hreflang={otherLang} href={sibling} />
    ) : null}
    <link rel="alternate" hreflang={lang} href={canonical} />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="alternate" type="application/rss+xml" title="marsmike.com (DE)" href="/rss.xml" />
    <link rel="alternate" type="application/rss+xml" title="marsmike.com (EN)" href="/en/rss.xml" />
    <meta property="og:type" content={ogType} />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:url" content={canonical} />
    <meta property="og:locale" content={lang === 'de' ? 'de_DE' : 'en_US'} />
    {sibling ? (<meta property="og:locale:alternate" content={otherLang === 'de' ? 'de_DE' : 'en_US'} />) : null}
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:creator" content="@MarsMike" />
    <script is:inline>
      // FOUC guard: apply theme before paint
      (() => {
        const stored = localStorage.getItem('theme');
        const prefersDark = matchMedia('(prefers-color-scheme: dark)').matches;
        const dark = stored === 'dark' || (!stored && prefersDark) || (stored !== 'light' && stored !== 'system' && prefersDark);
        if (dark) document.documentElement.classList.add('dark');
      })();
    </script>
  </head>
  <body>
    <Header lang={lang} siblingPath={siblingPath} />
    <main class="max-w-3xl mx-auto px-5 py-10">
      <slot />
    </main>
    <Footer lang={lang} />
  </body>
</html>
```

- [ ] **Step 4: Create placeholder favicon**

```bash
cat > public/favicon.svg <<'EOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="10" fill="#b8442a"/>
  <text x="32" y="44" text-anchor="middle" font-family="Inter, sans-serif" font-size="38" font-weight="700" fill="#fafaf9">m</text>
</svg>
EOF
```

- [ ] **Step 5: Commit**

```bash
git add src/layouts/ src/components/Header.astro src/components/Footer.astro public/favicon.svg
git commit -m "feat: BaseLayout with head metadata, FOUC guard, header, footer, favicon"
```

---

### Task 7: PostCard and PostLayout

**Files:**
- Create: `~/work/marsmike.com/src/components/PostCard.astro`
- Create: `~/work/marsmike.com/src/layouts/PostLayout.astro`

- [ ] **Step 1: Create `src/components/PostCard.astro`**

```astro
---
interface Props {
  title: string;
  summary: string;
  date: Date;
  href: string;
  lang: 'de' | 'en';
}
const { title, summary, date, href, lang } = Astro.props;
const dateLocale = lang === 'de' ? 'de-DE' : 'en-US';
const dateStr = date.toLocaleDateString(dateLocale, {
  year: 'numeric', month: 'short', day: 'numeric',
});
---

<article class="py-5 border-b border-[var(--color-border)] last:border-b-0">
  <a href={href} class="no-underline group block">
    <div class="text-xs text-[var(--color-muted)] tabular-nums mb-1">
      <time datetime={date.toISOString()}>{dateStr}</time>
    </div>
    <h2 class="text-lg font-semibold text-[var(--color-text)] group-hover:text-[var(--color-accent)] transition-colors mb-1">
      {title}
    </h2>
    <p class="text-[var(--color-muted)]">{summary}</p>
  </a>
</article>
```

- [ ] **Step 2: Create `src/layouts/PostLayout.astro`**

```astro
---
import BaseLayout from './BaseLayout.astro';

interface Artifact {
  label: string;
  url: string;
  type: 'video' | 'pdf' | 'pptx' | 'image' | 'audio' | 'other';
}

interface Props {
  title: string;
  summary: string;
  date: Date;
  lang: 'de' | 'en';
  linkedinUrl?: string;
  codeUrl?: string;
  artifacts?: Artifact[];
  siblingPath?: string;
  prev?: { href: string; title: string };
  next?: { href: string; title: string };
}

const {
  title, summary, date, lang,
  linkedinUrl, codeUrl, artifacts = [], siblingPath,
  prev, next,
} = Astro.props;

const dateLocale = lang === 'de' ? 'de-DE' : 'en-US';
const dateStr = date.toLocaleDateString(dateLocale, {
  year: 'numeric', month: 'long', day: 'numeric',
});
const linkedinLabel = lang === 'de' ? 'LinkedIn' : 'LinkedIn';
const codeLabel = lang === 'de' ? 'Code' : 'Code';
const artifactsLabel = lang === 'de' ? 'Artefakte' : 'Artifacts';
const prevLabel = lang === 'de' ? '← Vorheriger' : '← Previous';
const nextLabel = lang === 'de' ? 'Nächster →' : 'Next →';

const typeIcon = (t: Artifact['type']) => ({
  video: '▶', pdf: '📄', pptx: '🗂', image: '🖼', audio: '🔊', other: '↗',
}[t]);
---

<BaseLayout
  lang={lang}
  title={`${title} — marsmike.com`}
  description={summary}
  siblingPath={siblingPath}
  ogType="article"
>
  <article>
    <header class="mb-8">
      <div class="text-sm text-[var(--color-muted)] tabular-nums mb-2">
        <time datetime={date.toISOString()}>{dateStr}</time>
      </div>
      <h1 class="text-3xl font-bold text-[var(--color-text)] leading-tight mb-3">{title}</h1>
      <p class="text-lg text-[var(--color-muted)] leading-snug">{summary}</p>
      {(linkedinUrl || codeUrl) && (
        <div class="mt-4 flex flex-wrap gap-3 text-sm">
          {linkedinUrl && (
            <a href={linkedinUrl} class="no-underline px-3 py-1 rounded border border-[var(--color-border)] hover:border-[var(--color-accent)] hover:text-[var(--color-accent)]">
              {linkedinLabel} ↗
            </a>
          )}
          {codeUrl && (
            <a href={codeUrl} class="no-underline px-3 py-1 rounded border border-[var(--color-border)] hover:border-[var(--color-accent)] hover:text-[var(--color-accent)]">
              {codeLabel} ↗
            </a>
          )}
        </div>
      )}
    </header>

    <div class="prose-body space-y-5 [&_h2]:text-2xl [&_h2]:font-semibold [&_h2]:mt-10 [&_h2]:mb-3 [&_h3]:text-xl [&_h3]:font-semibold [&_h3]:mt-8 [&_h3]:mb-2 [&_p]:leading-relaxed [&_ul]:list-disc [&_ul]:pl-6 [&_ol]:list-decimal [&_ol]:pl-6 [&_blockquote]:border-l-2 [&_blockquote]:border-[var(--color-accent)] [&_blockquote]:pl-4 [&_blockquote]:text-[var(--color-muted)]">
      <slot />
    </div>

    {artifacts.length > 0 && (
      <section class="mt-12 pt-6 border-t border-[var(--color-border)]">
        <h2 class="text-xs uppercase tracking-wider text-[var(--color-muted)] mb-3">{artifactsLabel}</h2>
        <ul class="space-y-2 list-none pl-0">
          {artifacts.map((a) => (
            <li>
              <a href={a.url} class="no-underline hover:underline">
                <span aria-hidden="true" class="mr-2">{typeIcon(a.type)}</span>{a.label}
              </a>
            </li>
          ))}
        </ul>
      </section>
    )}

    {(prev || next) && (
      <nav class="mt-16 pt-6 border-t border-[var(--color-border)] flex justify-between gap-4 text-sm">
        {prev ? (
          <a href={prev.href} class="no-underline text-[var(--color-muted)] hover:text-[var(--color-accent)]">
            <span class="block text-xs">{prevLabel}</span>
            <span>{prev.title}</span>
          </a>
        ) : <span></span>}
        {next ? (
          <a href={next.href} class="no-underline text-[var(--color-muted)] hover:text-[var(--color-accent)] text-right">
            <span class="block text-xs">{nextLabel}</span>
            <span>{next.title}</span>
          </a>
        ) : <span></span>}
      </nav>
    )}
  </article>
</BaseLayout>
```

- [ ] **Step 3: Commit**

```bash
git add src/components/PostCard.astro src/layouts/PostLayout.astro
git commit -m "feat: PostCard and PostLayout with badges, prev/next, semantic dates"
```

---

### Task 8: Landing pages (DE + EN)

**Files:**
- Create: `~/work/marsmike.com/src/pages/index.astro`
- Create: `~/work/marsmike.com/src/pages/en/index.astro`

- [ ] **Step 1: Create `src/pages/index.astro` (DE)**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '~/layouts/BaseLayout.astro';
import PostCard from '~/components/PostCard.astro';

const posts = (await getCollection('posts', ({ data }) => data.lang === 'de' && data.status === 'live'))
  .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

const tagline = 'Senior Software Engineer @ BSH · 25+ Jahre · Schreibe über KI × Developer-Produktivität.';

// Sibling EN home if at least one EN post exists, otherwise no switcher
const enPosts = await getCollection('posts', ({ data }) => data.lang === 'en' && data.status === 'live');
const siblingPath = enPosts.length > 0 ? '/en/' : undefined;
---

<BaseLayout
  lang="de"
  title="marsmike.com"
  description={tagline}
  siblingPath={siblingPath}
>
  <section class="mb-12">
    <h1 class="text-2xl font-semibold text-[var(--color-text)] mb-2">Mike Müller</h1>
    <p class="text-[var(--color-muted)] leading-relaxed">{tagline}</p>
  </section>

  <section>
    <h2 class="text-sm uppercase tracking-wider text-[var(--color-muted)] mb-2">Beiträge</h2>
    {posts.length === 0 ? (
      <p class="text-[var(--color-muted)] py-6">Noch nichts veröffentlicht.</p>
    ) : (
      <div>
        {posts.map((post) => (
          <PostCard
            title={post.data.title}
            summary={post.data.summary}
            date={post.data.date}
            href={`/posts/${post.slug.replace(/^de\//, '')}/`}
            lang="de"
          />
        ))}
      </div>
    )}
  </section>
</BaseLayout>
```

- [ ] **Step 2: Create `src/pages/en/index.astro` (EN)**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '~/layouts/BaseLayout.astro';
import PostCard from '~/components/PostCard.astro';

const posts = (await getCollection('posts', ({ data }) => data.lang === 'en' && data.status === 'live'))
  .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

const tagline = 'Senior Software Engineer @ BSH · 25+ years · Writing on AI × developer productivity.';

const dePosts = await getCollection('posts', ({ data }) => data.lang === 'de' && data.status === 'live');
const siblingPath = dePosts.length > 0 ? '/' : undefined;
---

<BaseLayout
  lang="en"
  title="marsmike.com"
  description={tagline}
  siblingPath={siblingPath}
>
  <section class="mb-12">
    <h1 class="text-2xl font-semibold text-[var(--color-text)] mb-2">Mike Müller</h1>
    <p class="text-[var(--color-muted)] leading-relaxed">{tagline}</p>
  </section>

  <section>
    <h2 class="text-sm uppercase tracking-wider text-[var(--color-muted)] mb-2">Posts</h2>
    {posts.length === 0 ? (
      <p class="text-[var(--color-muted)] py-6">Nothing published yet.</p>
    ) : (
      <div>
        {posts.map((post) => (
          <PostCard
            title={post.data.title}
            summary={post.data.summary}
            date={post.data.date}
            href={`/en/posts/${post.slug.replace(/^en\//, '')}/`}
            lang="en"
          />
        ))}
      </div>
    )}
  </section>
</BaseLayout>
```

- [ ] **Step 3: Run build to verify pages compile**

```bash
pnpm build
```

Expected: builds successfully. Both `/` and `/en/` pages emit (with empty post lists for now).

- [ ] **Step 4: Commit**

```bash
git add src/pages/index.astro src/pages/en/index.astro
git commit -m "feat: bilingual landing pages with post list"
```

---

### Task 9: Post route pages (DE + EN)

**Files:**
- Create: `~/work/marsmike.com/src/pages/posts/[slug].astro`
- Create: `~/work/marsmike.com/src/pages/en/posts/[slug].astro`

- [ ] **Step 1: Create `src/pages/posts/[slug].astro` (DE)**

```astro
---
import { getCollection } from 'astro:content';
import PostLayout from '~/layouts/PostLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('posts', ({ data }) => data.lang === 'de' && data.status === 'live');
  const sorted = posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
  return sorted.map((post, i) => ({
    params: { slug: post.slug.replace(/^de\//, '') },
    props: {
      post,
      prev: sorted[i + 1],
      next: sorted[i - 1],
    },
  }));
}

const { post, prev, next } = Astro.props;
const { Content } = await post.render();

const enPosts = post.data.translation_of
  ? await getCollection('posts', ({ data }) => data.lang === 'en' && data.status === 'live')
  : [];
const sibling = enPosts.find(p => p.slug.replace(/^en\//, '') === post.data.translation_of);
const siblingPath = sibling ? `/en/posts/${sibling.slug.replace(/^en\//, '')}/` : undefined;

const slugBare = (s: string) => s.replace(/^de\//, '');
---

<PostLayout
  title={post.data.title}
  summary={post.data.summary}
  date={post.data.date}
  lang="de"
  linkedinUrl={post.data.linkedin_url}
  codeUrl={post.data.code_url}
  artifacts={post.data.artifacts}
  siblingPath={siblingPath}
  prev={prev ? { href: `/posts/${slugBare(prev.slug)}/`, title: prev.data.title } : undefined}
  next={next ? { href: `/posts/${slugBare(next.slug)}/`, title: next.data.title } : undefined}
>
  <Content />
</PostLayout>
```

- [ ] **Step 2: Create `src/pages/en/posts/[slug].astro` (EN)**

```astro
---
import { getCollection } from 'astro:content';
import PostLayout from '~/layouts/PostLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('posts', ({ data }) => data.lang === 'en' && data.status === 'live');
  const sorted = posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
  return sorted.map((post, i) => ({
    params: { slug: post.slug.replace(/^en\//, '') },
    props: {
      post,
      prev: sorted[i + 1],
      next: sorted[i - 1],
    },
  }));
}

const { post, prev, next } = Astro.props;
const { Content } = await post.render();

const dePosts = post.data.translation_of
  ? await getCollection('posts', ({ data }) => data.lang === 'de' && data.status === 'live')
  : [];
const sibling = dePosts.find(p => p.slug.replace(/^de\//, '') === post.data.translation_of);
const siblingPath = sibling ? `/posts/${sibling.slug.replace(/^de\//, '')}/` : undefined;

const slugBare = (s: string) => s.replace(/^en\//, '');
---

<PostLayout
  title={post.data.title}
  summary={post.data.summary}
  date={post.data.date}
  lang="en"
  linkedinUrl={post.data.linkedin_url}
  codeUrl={post.data.code_url}
  artifacts={post.data.artifacts}
  siblingPath={siblingPath}
  prev={prev ? { href: `/en/posts/${slugBare(prev.slug)}/`, title: prev.data.title } : undefined}
  next={next ? { href: `/en/posts/${slugBare(next.slug)}/`, title: next.data.title } : undefined}
>
  <Content />
</PostLayout>
```

- [ ] **Step 3: Commit**

```bash
git add src/pages/posts/ src/pages/en/posts/
git commit -m "feat: bilingual post routes with sibling-translation linking and prev/next"
```

---

### Task 10: RSS feeds and sitemap

**Files:**
- Create: `~/work/marsmike.com/src/pages/rss.xml.ts`
- Create: `~/work/marsmike.com/src/pages/en/rss.xml.ts`

The sitemap is already wired by the `@astrojs/sitemap` integration — no file needed.

- [ ] **Step 1: Create `src/pages/rss.xml.ts` (DE)**

```ts
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = (await getCollection('posts', ({ data }) => data.lang === 'de' && data.status === 'live'))
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

  return rss({
    title: 'marsmike.com',
    description: 'Mike Müller — Software-Delivery im GenAI-Zeitalter.',
    site: context.site!,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.summary,
      pubDate: post.data.date,
      link: `/posts/${post.slug.replace(/^de\//, '')}/`,
    })),
    customData: '<language>de-DE</language>',
  });
}
```

- [ ] **Step 2: Create `src/pages/en/rss.xml.ts` (EN)**

```ts
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = (await getCollection('posts', ({ data }) => data.lang === 'en' && data.status === 'live'))
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

  return rss({
    title: 'marsmike.com',
    description: 'Mike Müller — software delivery in the GenAI era.',
    site: context.site!,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.summary,
      pubDate: post.data.date,
      link: `/en/posts/${post.slug.replace(/^en\//, '')}/`,
    })),
    customData: '<language>en-US</language>',
  });
}
```

- [ ] **Step 3: Create `public/robots.txt`**

```
User-agent: *
Allow: /

Sitemap: https://marsmike.com/sitemap-index.xml
```

- [ ] **Step 4: Verify build emits both feeds and sitemap**

```bash
pnpm build
ls dist/rss.xml dist/en/rss.xml dist/sitemap-index.xml dist/sitemap-0.xml
```

Expected: all four files present.

- [ ] **Step 5: Commit**

```bash
git add src/pages/rss.xml.ts src/pages/en/rss.xml.ts public/robots.txt
git commit -m "feat: per-language RSS feeds, sitemap, robots.txt"
```

---

### Task 11: About pages (DE + EN)

**Files:**
- Create: `~/work/marsmike.com/src/pages/about.astro`
- Create: `~/work/marsmike.com/src/pages/en/about.astro`

Body lifted verbatim from `~/Documents/The-Void/02_Projects/social-amplification/linkedin-about-drafts-2026-04-28.md` (already voice-checked, RAISE/Betriebsrat firewalls clean).

- [ ] **Step 1: Create `src/pages/about.astro` (DE)**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
const tagline = 'Senior Software Engineer @ BSH · 25+ Jahre · Schreibe über KI × Developer-Produktivität.';
---

<BaseLayout
  lang="de"
  title="Über — marsmike.com"
  description={tagline}
  siblingPath="/en/about/"
>
  <article class="space-y-5 leading-relaxed">
    <header class="mb-8">
      <h1 class="text-3xl font-bold text-[var(--color-text)] mb-2">Mike Müller</h1>
      <p class="text-[var(--color-muted)]">Senior Software Engineer @ BSH · Regensburg</p>
    </header>

    <p>Fünfundzwanzig Jahre Softwareentwicklung. Angefangen mit Smalltalk und OOP. Heute mache ich Small Talk mit dem System.</p>

    <p>Derzeit Senior Software Engineer im RAISE-SW GenAI-Team bei BSH. Wir bauen produktionsreife KI-Agenten in der Software-Delivery-Pipeline. Außerdem gewählter Betriebsrat — verantwortlich dafür, wie KI-Einführungen in einem Konzern mit 60.000 Mitarbeitenden tatsächlich ankommen.</p>

    <p>Worüber ich nachdenke: Software-Delivery im GenAI-Zeitalter, von der Anforderung bis in die Pipeline. Anforderungen, Architektur, Wissensmanagement, CI/CD, Background-Agenten — die alltägliche Reibung, nicht die Keynote-Version.</p>

    <p>Ich schreibe darüber hier auf marsmike.com. Kurze Videos und Notizen für erfahrene Entwickler und die Tech Leads, die sie einstellen. Praktische Antworten, kein Hype.</p>

    <p>Offen für Mentoring-Gespräche, Diskussion über Agent-Zuverlässigkeit, Fragen zur späten Karrierephase (Altersteilzeit, KI-Ära) und ernsthafte Recruiter-Anfragen.</p>

    <hr class="border-[var(--color-border)] my-8" />

    <section class="text-sm text-[var(--color-muted)]">
      <h2 class="text-xs uppercase tracking-wider mb-3">Kontakt</h2>
      <ul class="space-y-1 list-none pl-0">
        <li><a href="mailto:mike@marsmike.com" class="no-underline hover:underline">mike@marsmike.com</a></li>
        <li><a href="https://www.linkedin.com/in/marsmike" class="no-underline hover:underline">LinkedIn</a></li>
        <li><a href="https://github.com/marsmike" class="no-underline hover:underline">GitHub</a></li>
        <li><a href="https://x.com/marsmike" class="no-underline hover:underline">X (@MarsMike)</a></li>
      </ul>
    </section>
  </article>
</BaseLayout>
```

- [ ] **Step 2: Create `src/pages/en/about.astro` (EN)**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
const tagline = 'Senior Software Engineer @ BSH · 25+ years · Writing on AI × developer productivity.';
---

<BaseLayout
  lang="en"
  title="About — marsmike.com"
  description={tagline}
  siblingPath="/about/"
>
  <article class="space-y-5 leading-relaxed">
    <header class="mb-8">
      <h1 class="text-3xl font-bold text-[var(--color-text)] mb-2">Mike Müller</h1>
      <p class="text-[var(--color-muted)]">Senior Software Engineer @ BSH · Regensburg</p>
    </header>

    <p>Twenty-five years writing software. Started with Smalltalk and OOP. These days I'm doing small-talk with the system.</p>

    <p>Currently Senior Software Engineer in BSH's RAISE-SW GenAI team, building production AI agents inside the software delivery pipeline. Also elected Betriebsrat (works council member) at BSH, responsible for how AI rollouts actually land in a 60,000-person company.</p>

    <p>What I think about: software delivery in the GenAI era, end-to-end. Requirements, architecture, knowledge management, CI/CD, background agents — the daily friction, not the keynote-talk version.</p>

    <p>I'm writing here at marsmike.com. Short videos and notes for senior engineers and the tech leads who hire them. Practical answers, not hype.</p>

    <p>Open to mentorship conversations, agent-reliability discussion, late-career engineering questions (Altersteilzeit, AI-era career arc), and serious recruiter outreach.</p>

    <hr class="border-[var(--color-border)] my-8" />

    <section class="text-sm text-[var(--color-muted)]">
      <h2 class="text-xs uppercase tracking-wider mb-3">Contact</h2>
      <ul class="space-y-1 list-none pl-0">
        <li><a href="mailto:mike@marsmike.com" class="no-underline hover:underline">mike@marsmike.com</a></li>
        <li><a href="https://www.linkedin.com/in/marsmike" class="no-underline hover:underline">LinkedIn</a></li>
        <li><a href="https://github.com/marsmike" class="no-underline hover:underline">GitHub</a></li>
        <li><a href="https://x.com/marsmike" class="no-underline hover:underline">X (@MarsMike)</a></li>
      </ul>
    </section>
  </article>
</BaseLayout>
```

- [ ] **Step 3: Commit**

```bash
git add src/pages/about.astro src/pages/en/about.astro
git commit -m "feat: bilingual About pages (lifted from locked LinkedIn About copy)"
```

---

### Task 12: Draft launch post (DE + EN) in vault

**Files:**
- Create: `~/Documents/The-Void/02_Projects/marsmike-com/drafts/2026-04-29-agentic-toolkit-open-sourced-de.md`
- Create: `~/Documents/The-Void/02_Projects/marsmike-com/drafts/2026-04-29-agentic-toolkit-open-sourced-en.md`

These are draft files in the vault — first stop in the lift-and-publish flow. Voice firewall checks happen here before lifting in Task 14.

- [ ] **Step 1: Ensure vault drafts directory exists**

```bash
mkdir -p ~/Documents/The-Void/02_Projects/marsmike-com/drafts
```

- [ ] **Step 2: Create DE draft**

```bash
cat > ~/Documents/The-Void/02_Projects/marsmike-com/drafts/2026-04-29-agentic-toolkit-open-sourced-de.md <<'EOF'
---
title: "Mein Agentic Toolkit ist jetzt open source"
summary: "github.com/marsmike/agentic-toolkit ist seit heute öffentlich. Plugins erscheinen einzeln, nicht alle auf einmal - in der Reihenfolge, in der ich sie einem Kollegen geben würde."
date: 2026-04-29
lang: de
status: live
tags: ["agentic-toolkit", "claude-code", "oss"]
linkedin_url: ""
code_url: "https://github.com/marsmike/agentic-toolkit"
translation_of: "agentic-toolkit-open-sourced"
---

Die meisten Plugin-Marketplaces werfen alles auf einmal raus und überlassen dem Publikum die Sortierarbeit. Dieser nicht. github.com/marsmike/agentic-toolkit ist seit heute öffentlich, und die Plugins erscheinen einzeln, in der Reihenfolge, in der ich sie einem Kollegen geben würde.

Was heute online steht, ist ein Gerüst: ein Marketplace-Manifest, eine Lizenz (MIT), eine Mitwirkungs-Vereinbarung (DCO-Sign-off) und eine Roadmap mit einem Satz: "Nächstes Plugin landet in Kürze." Auf der privaten Seite existieren einundzwanzig Plugins. Sie sind im Alltag entstanden und im Alltag erprobt - Recherche, Wissensmanagement, Deck-Produktion, Video-Pipelines, Homelab-Steuerung, Social Amplification. Sie kommen einzeln hier an, jedes als eigenes Lehrartefakt, jedes in der Form, die es verdient.

Big-Bang-Launches optimieren für GitHub-Sterne am Launch-Tag. Sie optimieren nicht für die Entwicklerin, die morgen früh tatsächlich eines dieser Tools einsetzen will. Ein einzeln veröffentlichtes Plugin bekommt den Beitrag, den es verdient: was es tut, was es nicht tut, welches Problem es löst, welche Tradeoffs man vor der Installation kennen sollte. Das ist die redaktionelle Wette. Sie ist langsamer, und sie ist besser. Sie ist auch genau die Übersetzungsarbeit, die ich an anderer Stelle beschrieben habe - Code für Menschen erklären, die keinen Code schreiben. Auf OSS angewandt heißt das: man wirft niemandem einundzwanzig Repos vor die Füße. Man reicht eins. Mit einer Geschichte.

Feinschliff erscheint heute. Es macht aus Claude-Design-HTML markenkonforme PowerPoint-Decks, das Plugin, das ich in meinem eigenen Alltag am häufigsten benutze, und der Grund, warum dieser Marketplace die Form hat, die er hat. Es ist der Anker: stimmt das Design-System, erbt jedes weitere Plugin, das Visuals produziert (Slides, Video-Frames, Infografiken, Social-Cards), die Markendisziplin automatisch. Der Beitrag zu Feinschliff selbst folgt, sobald es live ist. Dieser hier ist die Eröffnung des Marketplace und der Auftakt der Kadenz.

Heute ist auch der Tag, an dem marsmike.com die "Coming Soon"-Seite ablöst. Was hier entsteht, ist die ausführliche Version dessen, was ich auf LinkedIn poste, die gleichen Gedanken mit dem Platz, den Code zu zeigen, die Tradeoffs, und das, was nicht funktioniert hat. Genau hier wohnt jetzt das "Schritt für Schritt", das ich bei Nacht Schafft Wissen versprochen hatte. Forschung und Praxis aus dem letzten Jahr, in verständlicher Sprache, ein Stück nach dem anderen. Der RSS-Feed liegt unter /rss.xml; der englische unter /en/rss.xml. LinkedIn für die Gespräche, GitHub für den Code. Kein Newsletter, keine Popups, kein "Abonnieren, um weiterzulesen". Nur das Schreiben.
EOF
```

- [ ] **Step 3: Create EN draft**

```bash
cat > ~/Documents/The-Void/02_Projects/marsmike-com/drafts/2026-04-29-agentic-toolkit-open-sourced-en.md <<'EOF'
---
title: "My agentic toolkit is now open source"
summary: "github.com/marsmike/agentic-toolkit is public today. Plugins ship one at a time, not in a single dump — in the order I'd hand them to a colleague."
date: 2026-04-29
lang: en
status: live
tags: ["agentic-toolkit", "claude-code", "oss"]
linkedin_url: ""
code_url: "https://github.com/marsmike/agentic-toolkit"
translation_of: "agentic-toolkit-open-sourced"
---

Most plugin marketplaces drop everything at once and ask the audience to figure out what matters. This one won't. github.com/marsmike/agentic-toolkit is public today, and it'll release plugins one at a time, in the order I'd hand them to a colleague.

What's there right now is a skeleton: a marketplace manifest, a license (MIT), a contributor agreement (DCO sign-off), and a roadmap that says "next plugin lands shortly." Twenty-one plugins exist on the private side. They've been built and battle-tested across actual daily work, research, knowledge management, deck production, video pipelines, homelab control, social amplification. They'll arrive here one by one, each as its own teaching artifact, each in the shape it deserves.

Big-bang launches optimize for repo stars on launch day. They don't optimize for the engineer who's actually trying to use one of these tools tomorrow morning. A plugin released alone gets the post it deserves: what it does, what it doesn't do, the problem it was built to solve, the trade-offs you'd want to know about before installing. That's the editorial bet. It's slower; it's better. It's also the same craft I've been writing about in another shape, explaining what code does to people who don't write code. Apply that to OSS and you don't drop twenty-one repos on someone's lap. You hand them one. With a story.

Feinschliff lands today. It turns Claude Design HTML into brand-perfect PowerPoint decks — the plugin I use most days in my own work, and the reason the marketplace exists in this shape. It's the anchor: get the design system right, and every other plugin that produces visuals (slides, video frames, infographics, social cards) inherits the brand discipline for free. The post about feinschliff specifically follows once it's live; this post is the announcement that the marketplace is open and the cadence has started.

This is also the day marsmike.com replaces "Coming Soon." What you'll find here is the deeper version of what I post on LinkedIn, the same ideas with room to show the code, the trade-offs, and the things that didn't work. The "step by step" rhythm I introduced at Nacht Schafft Wissen lives here now. Research and practice from the past year, in plain language, one piece at a time. The RSS feed is at /rss.xml; the EN feed is at /en/rss.xml. LinkedIn for the conversations. GitHub for the code. No newsletter, no popups, no "subscribe to keep reading." Just the writing.
EOF
```

No commit yet — these are drafts in the vault, not the repo.

---

### Task 13: Voice firewall manual check

This task is intentionally non-automated. Run the checks manually on both drafts before lifting.

- [ ] **Step 1: Check banned words (DE + EN)**

```bash
DRAFT_DIR=~/Documents/The-Void/02_Projects/marsmike-com/drafts
# Banned words list (from mike-voice-banned-patterns)
grep -niE '\b(leverage|delve|robust|holistic|tapestry|seamless|landscape|navigate|synergy|foster|underscore|resonate|nuanced|comprehensive|streamline|empower)\b' \
  "$DRAFT_DIR"/2026-04-29-agentic-toolkit-open-sourced-*.md
```

Expected: no matches. If any: rewrite the offending line.

- [ ] **Step 2: Check banned transitions**

```bash
grep -niE '^\s*(Furthermore|Moreover|Additionally|That being said)\b' \
  "$DRAFT_DIR"/2026-04-29-agentic-toolkit-open-sourced-*.md
```

Expected: no matches.

- [ ] **Step 3: Em-dash count (≤3 per language)**

```bash
echo "DE em-dashes: $(grep -o '—' "$DRAFT_DIR"/2026-04-29-agentic-toolkit-open-sourced-de.md | wc -l)"
echo "EN em-dashes: $(grep -o '—' "$DRAFT_DIR"/2026-04-29-agentic-toolkit-open-sourced-en.md | wc -l)"
```

Expected: each ≤3. (DE draft uses hyphens-with-spaces per the German rider; EN draft uses one or two em-dashes.)

- [ ] **Step 4: EN contraction density (≥1 per 100 words)**

```bash
EN_FILE="$DRAFT_DIR/2026-04-29-agentic-toolkit-open-sourced-en.md"
WORDS=$(awk '/^---$/{f++; next} f==2' "$EN_FILE" | wc -w)
CONTRACTIONS=$(awk '/^---$/{f++; next} f==2' "$EN_FILE" | grep -oE "[A-Za-z]+'[a-z]+" | wc -l)
echo "EN: $CONTRACTIONS contractions in $WORDS words ($(echo "scale=2; $CONTRACTIONS / $WORDS * 100" | bc)/100)"
```

Expected: ≥1 contraction per 100 words.

- [ ] **Step 5: Read both drafts end-to-end**

Open in Obsidian, read top to bottom in each language. Look for:
- Stance line in opener AND closer (not just one)
- No autobiographical opening ("I started programming in 1999..." — bad)
- No intro→balanced→summary→optimistic-close shape
- DE: complete sentences with conjunctions and verbs (no EN-fragment rhythm)
- RAISE firewall: only role-level mention of "RAISE-SW" if at all; no Feinschliff internals, no BSH brand-compiler specifics. (The OSS feinschliff plugin is public-safe — naming it is fine.)
- Betriebsrat firewall: not invoked in this post (correct)
- BSH form: unslashed if mentioned; the current drafts don't mention BSH (correct — this post is OSS-side, not employer-side)

If any rewrite is needed, edit the vault drafts and re-run steps 1–4.

---

### Task 14: Lift posts to repo

**Files:**
- Create: `~/work/marsmike.com/src/content/posts/de/agentic-toolkit-open-sourced.md`
- Create: `~/work/marsmike.com/src/content/posts/en/agentic-toolkit-open-sourced.md`

- [ ] **Step 1: Copy DE draft into repo**

```bash
cp ~/Documents/The-Void/02_Projects/marsmike-com/drafts/2026-04-29-agentic-toolkit-open-sourced-de.md \
   ~/work/marsmike.com/src/content/posts/de/agentic-toolkit-open-sourced.md
```

- [ ] **Step 2: Copy EN draft into repo**

```bash
cp ~/Documents/The-Void/02_Projects/marsmike-com/drafts/2026-04-29-agentic-toolkit-open-sourced-en.md \
   ~/work/marsmike.com/src/content/posts/en/agentic-toolkit-open-sourced.md
```

- [ ] **Step 3: Build to verify content schema validation passes**

```bash
cd ~/work/marsmike.com
pnpm build
```

Expected: build succeeds. If schema validation fails (e.g. `summary` over 200 chars, missing required field): fix in the vault draft AND in the lifted file.

- [ ] **Step 4: Commit**

```bash
git add src/content/posts/de/agentic-toolkit-open-sourced.md src/content/posts/en/agentic-toolkit-open-sourced.md
git commit -m "post: agentic-toolkit-open-sourced (DE + EN launch post)"
```

---

### Task 15: Local build and smoke checks

- [ ] **Step 1: Clean build**

```bash
cd ~/work/marsmike.com
rm -rf dist .astro
pnpm build
```

Expected: succeeds with no errors. Output mentions both `/posts/agentic-toolkit-open-sourced/` and `/en/posts/agentic-toolkit-open-sourced/`.

- [ ] **Step 2: Verify output structure**

```bash
ls dist/index.html dist/about/index.html dist/posts/agentic-toolkit-open-sourced/index.html
ls dist/en/index.html dist/en/about/index.html dist/en/posts/agentic-toolkit-open-sourced/index.html
ls dist/rss.xml dist/en/rss.xml dist/sitemap-index.xml dist/favicon.svg dist/robots.txt
```

Expected: all files exist.

- [ ] **Step 3: Validate RSS feeds**

```bash
xmllint --noout dist/rss.xml dist/en/rss.xml && echo "RSS feeds valid XML"
```

Expected: no output from xmllint (silent success), then "RSS feeds valid XML".

- [ ] **Step 4: Preview locally**

```bash
pnpm preview
```

Open `http://localhost:4321/` in a browser. Verify by hand:
- Landing page (DE) renders, shows the launch post in the list
- Click into the post — title, date, summary, badges (Code link visible, LinkedIn link absent until set), prose body renders
- Lang switcher in header works — clicks to `/en/posts/agentic-toolkit-open-sourced/`
- Theme toggle cycles system → light → dark → system; persists across reload
- About page (`/about`, `/en/about`) renders correctly
- Footer has all expected links; RSS link works

Stop the preview server (Ctrl-C) when done.

- [ ] **Step 5: iPhone Safari smoke check (LAN)**

If on the same WiFi:

```bash
pnpm preview --host
```

The CLI prints a LAN URL (e.g. `http://192.168.x.x:4321/`). Open on iPhone Safari and verify:
- Typography legible at default zoom
- No horizontal scroll
- Dark mode kicks in when phone is in dark mode
- Tap targets in header (lang/theme toggles) are at least 32×32 px

- [ ] **Step 6: Lighthouse spot check (Chrome DevTools, mobile)**

Open `http://localhost:4321/posts/agentic-toolkit-open-sourced/` in Chrome. DevTools → Lighthouse → Mobile → Performance + Accessibility + Best Practices + SEO → Analyze.

Targets:
- Performance ≥ 95
- Accessibility ≥ 95
- Best Practices ≥ 95
- SEO ≥ 95

If any score is below target, capture the failing audit and fix before proceeding. Common fixes:
- Performance: ensure fonts are `font-display: swap` (fontsource defaults handle this)
- Accessibility: contrast check on muted text in light mode
- SEO: verify canonical and meta description present

- [ ] **Step 7: Commit any fixes**

If fixes were needed:

```bash
git add -A
git commit -m "fix: lighthouse spot-check fixes (<specific>)"
```

---

### Task 16: GitHub repo and first push

- [ ] **Step 1: Create the public repo on GitHub**

```bash
cd ~/work/marsmike.com
gh repo create marsmike/marsmike.com \
  --public \
  --source=. \
  --description "Source for marsmike.com — bilingual blog by Mike Müller" \
  --remote=origin \
  --push
```

Expected: repo created, initial push succeeds, output shows the GitHub URL.

- [ ] **Step 2: Verify on GitHub**

Open `https://github.com/marsmike/marsmike.com` in a browser. Confirm:
- Repo is public
- README renders
- Commit history matches local

---

### Task 17: Wrangler authentication and preview deploy

The existing Cloudflare Pages project named `marsmike` (Direct Upload, currently serving "Coming Soon") is the deploy target. We do NOT create a new project; we deploy the new build into the same project on a non-production branch first, verify, then promote to `main`.

Account ID: `c39458b8d8d2df9804c4668f17227835`. Existing project name: `marsmike`.

- [ ] **Step 1: Verify wrangler authenticates with the existing token**

```bash
cd ~/work/marsmike.com
source ~/.env
pnpm wrangler whoami
```

Expected: prints email + account list including the Cloudflare account that owns `marsmike.com`. If it fails ("Authentication error"), re-source `~/.env` and confirm `CLOUDFLARE_API_TOKEN` is exported.

- [ ] **Step 2: Verify the target Pages project is reachable**

```bash
pnpm wrangler pages project list
```

Expected: output includes a project with name `marsmike` (subdomain `marsmike.pages.dev`).

- [ ] **Step 3: Build for production**

```bash
pnpm build
```

Expected: clean build, `dist/` populated.

- [ ] **Step 4: Deploy to a non-production branch (preview)**

```bash
pnpm wrangler pages deploy dist \
  --project-name=marsmike \
  --branch=launch-preview \
  --commit-dirty=true
```

Expected: deploy succeeds. Output includes a URL like `https://launch-preview.marsmike.pages.dev/` (preview alias) and a per-deployment URL like `https://<hash>.marsmike.pages.dev/`. Production domain `marsmike.com` is NOT touched at this point — it still serves the old "Coming Soon" deployment.

- [ ] **Step 5: Verify on the preview URL**

```bash
PREVIEW=https://launch-preview.marsmike.pages.dev
for path in / /about/ /posts/agentic-toolkit-open-sourced/ /en/ /en/about/ /en/posts/agentic-toolkit-open-sourced/ /rss.xml /en/rss.xml /sitemap-index.xml /robots.txt /favicon.svg; do
  status=$(curl -sIo /dev/null -w '%{http_code}' "${PREVIEW}${path}")
  echo "$status  ${PREVIEW}${path}"
done
```

Expected: all return `200`.

Then open `${PREVIEW}/posts/agentic-toolkit-open-sourced/` in a browser. Verify by hand:
- Page renders correctly, dates correct, badges (Code link present, LinkedIn link absent), prose body intact
- Lang switcher cross-links to `${PREVIEW}/en/posts/agentic-toolkit-open-sourced/`
- Theme toggle works and persists
- Mobile / iPhone Safari: typography legible, dark mode kicks in, no horizontal scroll

If anything is wrong, fix locally, re-run Steps 3 and 4. The production domain remains untouched throughout.

---

### Task 18: Promote to production

- [ ] **Step 1: Deploy to the production branch**

```bash
cd ~/work/marsmike.com
pnpm build
pnpm wrangler pages deploy dist \
  --project-name=marsmike \
  --branch=main \
  --commit-dirty=true
```

Expected: deploy succeeds. The `marsmike` Pages project's production deployment is updated; `marsmike.com` and `www.marsmike.com` switch to serving the new build within seconds (no DNS change, no cert reissue, same project binding throughout).

- [ ] **Step 2: Verify production**

```bash
for path in / /about/ /posts/agentic-toolkit-open-sourced/ /en/ /en/about/ /en/posts/agentic-toolkit-open-sourced/ /rss.xml /en/rss.xml /sitemap-index.xml /robots.txt; do
  status=$(curl -sIo /dev/null -w '%{http_code}' "https://marsmike.com${path}")
  echo "$status  https://marsmike.com${path}"
done
```

Expected: all return `200`. Open `https://marsmike.com/` in an incognito window — confirms the "Coming Soon" page is gone and the new site is live.

- [ ] **Step 3: Verify alias domains still 301 to apex**

```bash
for d in marsmike.de marsmike.ai marsmike.dev www.marsmike.com; do
  echo "=== $d ==="
  curl -sI "https://$d" | grep -iE '^(HTTP|location)'
done
```

Expected: each returns `HTTP/2 301` with `location: https://marsmike.com/`.

- [ ] **Step 4: Capture rollback target**

Cloudflare Pages retains every prior deployment. Record the deployment ID of the previous production deploy (the "Coming Soon" one) for emergency rollback:

```bash
ACCT="c39458b8d8d2df9804c4668f17227835"
source ~/.env
rtk proxy curl -s -X GET \
  "https://api.cloudflare.com/client/v4/accounts/$ACCT/pages/projects/marsmike/deployments?env=production&per_page=5" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); [print(x["id"], x["created_on"], x.get("deployment_trigger",{}).get("metadata",{}).get("commit_message",""))[:80] for x in d.get("result",[])[:5]]' \
  > /tmp/cf_recent_deploys.txt
cat /tmp/cf_recent_deploys.txt
```

Note the deployment ID immediately preceding today's deploy — this is the rollback target if needed.

To roll back (if ever needed): `pnpm wrangler pages deployment rollback <deployment-id> --project-name=marsmike` or use the Cloudflare dashboard "Promote" action.

---

### Task 19: Deeper production verification

(HTTP-status sanity already covered in Task 18 Step 2. This task adds the verification steps that benefit from being against the live URL specifically.)

- [ ] **Step 1: Validate RSS feeds via W3C**

Visit:
- `https://validator.w3.org/feed/check.cgi?url=https%3A%2F%2Fmarsmike.com%2Frss.xml`
- `https://validator.w3.org/feed/check.cgi?url=https%3A%2F%2Fmarsmike.com%2Fen%2Frss.xml`

Both should report "This is a valid RSS feed" (warnings about recommended elements are OK).

- [ ] **Step 2: Verify on iPhone Safari (production)**

Open `https://marsmike.com/posts/agentic-toolkit-open-sourced/` on iPhone Safari. Verify the same items as in Task 15 step 5, but on production.

- [ ] **Step 3: Run Lighthouse on production URL**

DevTools → Lighthouse → Mobile against `https://marsmike.com/posts/agentic-toolkit-open-sourced/`. Performance, Accessibility, Best Practices, SEO all ≥ 95.

If any score drops vs. local: usually CDN cache or fonts. Re-run after a minute. Otherwise capture and fix.

---

### Task 20: Update vault index and close out

- [ ] **Step 1: Create or update `posts-published.md` in the vault**

```bash
cat > ~/Documents/The-Void/02_Projects/marsmike-com/posts-published.md <<'EOF'
---
title: marsmike.com — Posts Published Index
type: project-index
status: active
created: 2026-04-29
project: marsmike.com
description: Manual ledger of posts published to marsmike.com — slug, language, live URL, LinkedIn URL when announced.
tags:
  - project/marsmike-com
---

# marsmike.com — Posts Published

| Date | Slug | DE | EN | LinkedIn DE | LinkedIn EN |
|---|---|---|---|---|---|
| 2026-04-29 | agentic-toolkit-open-sourced | [DE](https://marsmike.com/posts/agentic-toolkit-open-sourced/) | [EN](https://marsmike.com/en/posts/agentic-toolkit-open-sourced/) | _TBD_ | _TBD_ |

## Process

1. Draft DE and EN in `02_Projects/marsmike-com/drafts/YYYY-MM-DD-<slug>-{de,en}.md`
2. Run voice firewall checks (banned words, em-dashes, contractions, RAISE/Betriebsrat clean)
3. `cp` to `~/work/marsmike.com/src/content/posts/{de,en}/<slug>.md`
4. `pnpm build` locally to verify schema, push to `main`
5. Cloudflare Pages auto-deploys; verify live URL
6. Add row to this table, including LinkedIn URLs once posts go up
EOF
```

- [ ] **Step 2: Add today's journal entry**

```bash
JOURNAL=~/Documents/The-Void/00_Memory/journal/2026-04-29.md
TIME=$(date +"%H:%M")
cat >> "$JOURNAL" <<EOF
- [$TIME] marsmike.com | v1 SHIPPED — Astro + Cloudflare Pages bilingual blog live; first post (agentic-toolkit-open-sourced) DE+EN published; old "Coming Soon" project parked for 1-week rollback window
EOF
```

- [ ] **Step 3: When the LinkedIn announcement post goes live (now or later today)**

Once the LinkedIn DE post URL exists:

```bash
DE_POST=~/work/marsmike.com/src/content/posts/de/agentic-toolkit-open-sourced.md
sed -i.bak 's|^linkedin_url: ""|linkedin_url: "<paste-LinkedIn-URL-here>"|' "$DE_POST" && rm "$DE_POST.bak"
```

Repeat for EN post once that LinkedIn URL exists. Commit and push:

```bash
cd ~/work/marsmike.com
git add src/content/posts/
git commit -m "post: link launch posts to LinkedIn URLs"
git push
```

Update `posts-published.md` in the vault with the same URLs.

- [ ] **Step 4: No old project to clean up**

Because Option A redeploys into the existing `marsmike` Pages project (rather than creating a new one), there is no separate "Coming Soon" project to delete. Rollback target is the prior production deployment ID captured in Task 18 Step 4. No follow-up cleanup needed.

---

## Verification Summary

Plan is complete when:

- [ ] `https://marsmike.com/` shows the new bilingual blog landing (DE)
- [ ] `https://marsmike.com/posts/agentic-toolkit-open-sourced/` renders the launch post
- [ ] `https://marsmike.com/en/` and `https://marsmike.com/en/posts/agentic-toolkit-open-sourced/` render the EN versions
- [ ] `https://marsmike.com/about/` and `/en/about/` render
- [ ] `/rss.xml` and `/en/rss.xml` validate as RSS
- [ ] `/sitemap-index.xml` lists all pages
- [ ] Lighthouse mobile ≥ 95 on all four core pillars on the launch post URL
- [ ] iPhone Safari renders cleanly with working dark mode
- [ ] All four domains (`.com`, `.de`, `.ai`, `.dev`) resolve correctly (`.com` direct; the others 301 to `.com`)
- [ ] Vault `posts-published.md` index reflects the new live URL
- [ ] Today's journal has a `[HH:MM] marsmike.com | ...` entry per Mike's standard journal format
