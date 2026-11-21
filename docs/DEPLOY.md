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

1. **preflight:** it refuses to deploy while any build input is uncommitted or untracked
   (`src/`, `public/`, `index.html`, `blender/`, `vite.config.js`, `package*.json`): the build
   uses the committed `HEAD`, so those files would silently be missing from the live site. It
   lists them. `DEPLOY_ALLOW_DIRTY=1` deploys `HEAD` anyway. It also warns when `HEAD` is not
   on `origin/main`.
2. checks out `HEAD` into a throwaway `git worktree`, so it ships exactly what is committed and
   never touches the shared `node_modules/`. There it runs `npm ci` (or `npm i` with no
   lockfile), then `npx vite build`.
3. **sub-path guard** (the site lives under `/imobiliare_landing_page/`): `dist/index.html`
   exists and has no root-absolute `src="/…"`, `href="/…"` or `content="/…"`; built CSS has
   no `url(/…)`; built JS has no quoted `/img/`, `/models/`, `/fonts/`, `/draco/`, `/basis/` or
   `/assets/` paths. Nothing from `reference/`, no `.mp4` and no `.blend` files are allowed in `dist/`.
4. adds `dist/.nojekyll` (so Pages serves files as-is, with no Jekyll pass)
5. makes one orphan commit of `dist/` and runs `git push -f <origin> HEAD:gh-pages`.
   `gh-pages` keeps no history; each deploy replaces it. The commit message records the `main`
   SHA it was built from.
6. **live check:** it waits (max `DEPLOY_VERIFY_TIMEOUT`, default 600 s) until
   `pages/builds/latest` is `built` for that exact gh-pages commit, failing on `errored`.
   Then it curls the page and **every file in `dist/`** on the live URL (with a `?v=<sha>`
   cache-buster) and fails on any non-200. It also checks that the live `index.html` is
   byte-identical to the build.
7. removes the worktree and prints the Pages URL

Order: run the pre-commit check, commit, push `main`, then deploy.

## Pre-commit check (before every commit)

```bash
bash tools/precommit-check.sh     # must print "precommit: ok"
```

It runs a case-insensitive grep across the whole tree (excluding `reference/`, `node_modules/`,
`assets-src/`, `dist/`, `.git/`) for the reference site's brand name and its city and
neighbourhood names. Text files are grepped normally and binary assets with `-a`, so `.glb`,
`.blend` and EXIF metadata are covered. Judge docs such as `docs/reviews/*` get the same check.
**It must return nothing before any commit.** It also fails if anything under `reference/`,
`assets-src/`, `dist/` or `node_modules/`, or any `.mp4`, `.mov` or `.blend1` file, is staged,
or if a staged file is over 50 MB. `.mp4` files may be staged only as `public/video/*.mp4`.

**Ship gate (SPEC §8.4: panned stills never ship):** `tools/check-video.sh` runs inside the
pre-commit check on the working tree, and inside `deploy.sh` on the committed worktree. It refuses
when:
- `public/video/hero.json` has `"status": "placeholder"`
- any `public/video/*.mp4` is byte-identical to `assets-src/video/placeholder.mp4` (the
  reference copy is read from the local checkout; once it is deleted there is nothing to compare,
  and only the status check applies)
- `public/models/` or `public/draco/` contains files

`deploy.sh` also fails if `dist/` contains any `.glb`, a `models/` or `draco/` folder, or an
`.mp4` outside `dist/video/`.

The search terms live in `tools/.blocklist`, one per line. That file is gitignored on purpose:
putting the names in a committed file would publish them, and the check would match itself.
On a fresh clone, get the list from the judge or lead. The equivalent one-liner is
`grep -rniE -f tools/.blocklist . --exclude-dir={reference,node_modules,assets-src,dist,.git} --exclude=.blocklist`.

## One-time Pages setup (done)

```bash
gh api -X POST repos/strategieonline/imobiliare_landing_page/pages \
  -f 'source[branch]=gh-pages' -f 'source[path]=/'
# if Pages already exists, change the source with -X PUT and the same fields
```

## Verifying a deploy

`deploy.sh` does this itself (step 6). To re-check by hand:

```bash
gh api repos/strategieonline/imobiliare_landing_page/pages/builds/latest --jq '{status,error,commit}'
gh run list -R strategieonline/imobiliare_landing_page --workflow pages-build-deployment -L 3
curl -sI https://strategieonline.github.io/imobiliare_landing_page/ | head -1
```

A deploy is done when the latest build is `built` for the new gh-pages commit and every
file in `dist/` returns 200 live. If a build fails, check the build's `error.message` field and
`gh run view <id> --log-failed -R strategieonline/imobiliare_landing_page`.

## Never commit or publish

- `reference/` (a third-party screen recording and its frames). It is in `.gitignore`; check with
  `git check-ignore -v reference/source.mp4` before every commit, and stage files by name, never
  `git add -A` blindly.
- `assets-src/` (MEDIA's raw originals), `*.blend1`, `node_modules/`, `dist/` (it only goes to
  `gh-pages`), `.claude/settings.local.json`, `tools/.blocklist`, and stray `source.mp4` or
  `frames/` copies anywhere (all gitignored).

## Notes for phase 2 (integration)

- Teams do not commit; RELEASE integrates. Read each `docs/HANDOFF-<TEAM>.md`, then commit per
  team (`hero: …`, `sections: …`, `3d: …`, `media: …`) with explicit paths, so history shows who
  built what.
- Before committing, check the size of `public/models/*.glb` (≤ 6 MB, city ≤ 3 MB) and
  `public/img/*` (plates ≤ 2560 px). Nothing over GitHub's 50 MB warning or 100 MB limit.
- `npx vite build` must pass, and so must the sub-path checks in `deploy.sh`.
- `blender/` is tracked, but only sources (`.blend`, scripts, renders, textures), never `.blend1`.
  At the 21 Nov check, `orizont_tower.blend` was 0.3 MB, `tower.glb` 1.9 MB and `city.glb` 0.1 MB.
- `deploy.sh` checks every deployed file returns 200 live. In addition, in a real browser, look for console errors and check that the hero
  scrolls through and loads the GLB (not the procedural fallback).
- QA list from SPEC §5: build passes, relative URLs, 375 px layout, `prefers-reduced-motion`,
  first view ≤ 8 MB, no console errors.

## Integration (phase 2, done 21 Nov)

- `three` removed (lead); `npm i` re-synced `package-lock.json`. No `three`, `GLTFLoader`,
  `DRACOLoader`, `models/` or `draco/` references are left in `src/` or `index.html`.
- `public/models/` was deleted after a `cmp` against `blender/export/*.glb` (identical).
  `public/draco/` was already gone.
- Committed from `blender/`: build scripts, both `.blend` files (0.3 and 0.5 MB),
  `export/*.glb` (1.8 MB + 0.1 MB), the guide stills `guides/S#_first/last.png` (~1 MB each,
  the keyframe references for the Higgsfield edits), `guides.json`, `S2_alt.json`, `renders/`
  (16 MB, previews used as MEDIA references) and `textures/`.
- **Not committed (gitignored):** `blender/guides/*.mp4` (13 MB of internal motion guides,
  reproducible via `build_guides.py`, never published), the `blender/guides/v1/` archive
  (22 MB, superseded), `__pycache__/`.
- The hero video ships at final cut: `hero.json` `status: final`, 1080p 23.6 MB, 720p 9.5 MB.

## Deploy log

| date | main SHA | result |
|---|---|---|
| 2026-11-21 | `3aad08b` | scaffold only (empty shell, no team work yet). gh-pages `6fa2f56`; Pages build `built`, run 44842414284 success in ~24 s; page 200, `assets/index-aestKa_H.js` 200, `assets/index-DjaUIdEH.css` 200, `.nojekyll` 200. Pages-from-branch works in this org (Actions not refused). |
| 2026-11-21 | `5c649d8` | test of the new deploy.sh (preflight refused the dirty tree; re-run with `DEPLOY_ALLOW_DIRTY=1`, same content as before). gh-pages `ee12f3f`, build `built`, live check: all 4 dist files + `/` 200, live index identical. |
| 2026-11-21 | `d1778f5` | **phase 2: full site** (video hero, sections, stills). 9 integration commits `d4ffd7a`…`d1778f5`. gh-pages `2089c74`, build `built` (run 44855384192 success, 27 s). Live check: `/` + all 26 dist files 200; `video/hero-1080.mp4` (23,580,203 B) and `hero-720.mp4` (9,464,950 B) are `video/mp4` with `accept-ranges: bytes`, and Range requests return 206 with the right `content-range`; moov is before mdat (faststart); live `index.html` byte-identical to the build. |
