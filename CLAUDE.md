# marsmike.com — operating notes

## Asset hosting (R2)

Public assets for blog posts live in the R2 bucket **`marsmike-assets`**, served at **`https://assets.marsmike.com`**.

- Cloudflare R2 dashboard: <https://dash.cloudflare.com/c39458b8d8d2df9804c4668f17227835/r2/default/buckets/marsmike-assets>
- Account ID: `c39458b8d8d2df9804c4668f17227835`
- Convention: post assets live under `posts/<slug>/<filename>` — e.g. `https://assets.marsmike.com/posts/feinschliff-launch/hero-grid.png`.
- Upload: `pnpm wrangler r2 object put marsmike-assets/posts/<slug>/<file> --file <local-path>` (then verify with `curl -sI https://assets.marsmike.com/posts/<slug>/<file>`).
- Listing isn't a `wrangler` CLI subcommand — browse via the dashboard URL above, or use the S3-compat API at `https://c39458b8d8d2df9804c4668f17227835.r2.cloudflarestorage.com/` with an R2 token.

## Voice firewall (mandatory before lifting any DE/EN draft)

Run `python tools/voice-check.py <path-to-draft>` on every draft before committing. Catches banned words, em-dash count, EN contraction density, DE grammar (LanguageTool), markdown italic + code-span exceptions, Feinschliff-domain anglicisms.

## Posts

- DE drafts → `src/content/posts/de/<slug>.md`
- EN drafts → `src/content/posts/en/<slug>.md`
- Frontmatter schema: `src/content/config.ts` (Zod-validated).
- `translation_of: <sibling-slug>` enables the in-post lang switcher.
- Hedge plugin counts in public posts — toolkit grows weekly; use "around twenty" / "rund zwanzig" / "ca. 20" rather than precise numbers.

## Deploy

- Preview: `pnpm build && pnpm wrangler pages deploy dist --project-name=marsmike --branch=launch-preview`
- Prod: `pnpm build && pnpm wrangler pages deploy dist --project-name=marsmike --branch=main`
- Cloudflare Pages retains every prior deployment → rollback is "Promote previous", not redeploy.

## Branch protection

Direct push to `main` is blocked — open a PR (`gh pr create`) and merge.
