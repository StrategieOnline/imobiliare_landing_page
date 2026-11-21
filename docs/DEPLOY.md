# Deploy

The site is a static Vite build served by GitHub Pages from the `gh-pages` branch.

- Repo: https://github.com/strategieonline/imobiliare_landing_page (public; the org is on GitHub
  Free, where Pages needs a public repo)
- Live: https://strategieonline.github.io/imobiliare_landing_page/
- Pages source: branch `gh-pages`, path `/`
- No GitHub Actions workflows of our own. Pages-from-branch still runs GitHub's internal
  `pages-build-deployment` run, which is the only Actions usage.

## How to deploy

```bash
npm run deploy      # = bash tools/deploy.sh
```

`tools/deploy.sh` (`set -euo pipefail`, no secrets, safe to re-run):

1. `npm ci` (or `npm i` when there is no lockfile)
2. `rm -rf dist && npx vite build`
3. checks: `dist/index.html` exists; no root-absolute `src="/…"` / `href="/…"` in it and no
   `url(/…)` in built CSS (the site lives under `/imobiliare_landing_page/`); nothing from
   `reference/` inside `dist/`
4. adds `dist/.nojekyll` (so Pages serves files as-is, with no Jekyll pass)
5. copies `dist/` to a temp dir, makes one orphan commit there and runs
   `git push -f <origin> HEAD:gh-pages`. `gh-pages` keeps no history; each deploy replaces it.
   The commit message records the `main` SHA it was built from.
6. prints the Pages URL

Deploy from a clean, committed `main` so the recorded SHA matches what is live.

## One-time Pages setup (done)

```bash
gh api -X POST repos/strategieonline/imobiliare_landing_page/pages \
  -f 'source[branch]=gh-pages' -f 'source[path]=/'
# if Pages already exists, change the source with -X PUT and the same fields
```

## Verifying a deploy

```bash
gh api repos/strategieonline/imobiliare_landing_page/pages/builds/latest --jq '{status,error,commit}'
gh run list -R strategieonline/imobiliare_landing_page --workflow pages-build-deployment -L 3
curl -sI https://strategieonline.github.io/imobiliare_landing_page/ | head -1
# and every JS/CSS asset that dist/index.html references:
for a in $(grep -oE '(src|href)="\./assets/[^"]+"' dist/index.html | cut -d'"' -f2); do
  curl -so /dev/null -w "%{http_code} $a\n" "https://strategieonline.github.io/imobiliare_landing_page/${a#./}"
done
```

A deploy is done when the latest build is `built`, the page returns 200 and every asset returns 200.
If a build fails, `gh run view <id> --log-failed -R strategieonline/imobiliare_landing_page` and the
build's `error.message` field say why.

## Never commit or publish

- `reference/` (a third-party screen recording and its frames). It is in `.gitignore`; check with
  `git check-ignore -v reference/source.mp4` before every commit, and stage files by name, never
  `git add -A` blindly.
- `assets-src/` (MEDIA's raw originals), `*.blend1`, `node_modules/`, `dist/` (it only goes to
  `gh-pages`), `.claude/settings.local.json`.

## Notes for phase 2 (integration)

- Teams do not commit; RELEASE integrates. Read each `docs/HANDOFF-<TEAM>.md`, then commit per
  team (`hero: …`, `sections: …`, `3d: …`, `media: …`) with explicit paths, so history shows who
  built what.
- Before committing, check the size of `public/models/*.glb` (≤ 6 MB, city ≤ 3 MB) and
  `public/img/*` (plates ≤ 2560 px). Nothing over GitHub's 50 MB warning or 100 MB limit.
- `npx vite build` must pass, and so must the sub-path checks in `deploy.sh`.
- After deploying, test the live URL itself: 200 for the page, all JS/CSS, `models/tower.glb`
  and a few `img/*.webp`. In a real browser, look for console errors and check that the hero
  scrolls through and loads the GLB (not the procedural fallback).
- QA list from SPEC §5: build passes, relative URLs, 375 px layout, `prefers-reduced-motion`,
  first view ≤ 8 MB, no console errors.

## Deploy log

| date | main SHA | result |
|---|---|---|
