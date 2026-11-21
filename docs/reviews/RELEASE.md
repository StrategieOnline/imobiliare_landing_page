# RELEASE review

## Round 1 (2026-11-21, phase 1: repo, Pages, README, deploy script)

**Verdict: PASS WITH FIXES** · **Craft 8/10**

The foundations are solid and every handoff claim checks out against the remote, not just the local clone. The deploy script is careful: it builds a worktree of HEAD, uses `set -euo pipefail`, has a trap cleanup, force-pushes only `gh-pages` and records the source SHA. Two gaps in it will bite in phase 2, when all team work arrives as *untracked* files and the hero loads its assets *from JS*. The docs are clear and honest. I deducted points for the deploy guard that doesn't cover JS bundles and the silent untracked-file case.

Evidence was gathered with `git` and `gh api` against the remote, and with `curl` on the live site. **Not done:** a live Chrome console check. The claude-in-chrome extension was not connected in this session, so I inferred the console 404 from curl (finding 4). I will redo it in phase 2.

### Claims verified

| claim (DEPLOY.md / lead) | result |
|---|---|
| Public repo `StrategieOnline/imobiliare_landing_page` | ✅ `visibility: PUBLIC`, default branch `main`, description and homepage set |
| Pages serves 200 | ✅ `https://strategieonline.github.io/imobiliare_landing_page/` returns 200. The no-slash URL 301s to it. Pages `status: built`, source `gh-pages /`, HTTPS enforced |
| main at `5c649d8` | ✅ local `main` = `origin/main` = `5c649d8` |
| gh-pages at `6fa2f56` | ✅ It is an orphan commit "deploy: build of main@3aad08b", with the full source SHA in the body |
| Builds from a clean worktree of HEAD | ✅ `git worktree add --detach $TMP/src $SHA`, then `npm ci` and `vite build` there. The trap removes it, and `git worktree list` shows no leftovers |
| `reference/` never committed | ✅ `git log --all --stat -- reference` is empty. `git rev-list --all --objects` has no `reference`, `source.mp4`, `.DS_Store`, `assets-src` or `settings.local` paths. The recursive remote trees of `main` and `gh-pages` have no such paths either. The history contains no reference brand or place names (`git grep` over all revs) |
| Live build = local build | ✅ The live `index.html` is byte-identical to the local `dist/index.html`. `assets/index-aestKa_H.js` and `index-DjaUIdEH.css` return 200, and `.nojekyll` returns 200 |
| No own GitHub Actions | ✅ The only workflow is GitHub's dynamic `pages-build-deployment` |

### Checklist

| ID | | note |
|---|---|---|
| R1 | ✅ | public, default `main` |
| R2 | ✅ | see above, local and remote |
| R3 | ✅ (partial) | page and all assets 200 under the sub-path. The live Chrome console was not checked (no extension); see finding 4 |
| R4 | ✅ | `gh-pages` = `index.html`, `assets/*`, `.nojekyll`. No secrets in either branch |
| R5 | ❌ major | sub-path guard misses JS bundles (finding 1); the untracked-files note is missing (finding 2) |
| R6 | ✅ | hashes match; the deploy commit records the source SHA; DEPLOY.md has a deploy log |
| R7 | ✅ with minors | accurate for phase 1 (findings 3, 5) |
| R8 | ✅ | `.gitignore` covers everything needed, including `assets-src/` (267 MB of raw originals, correctly ignored). Nothing large is committed. The repo is 208 KiB |
| R9 | ❌ minor | `og:image` is relative, and there is no favicon, so `/favicon.ico` returns 404 (finding 4) |
| G7 | ✅ | the script is small, commented where it matters, no secrets, and the new script `deploy` in package.json is fine |

### Findings

1. **major** · `tools/deploy.sh:47-55` · **The sub-path guard only inspects `dist/index.html` and the built CSS.**
   - **What's wrong:** the real risk in this project is in the JS bundle. The hero loads `tower.glb`, plates and decoders through `TextureLoader`/`GLTFLoader`/`fetch` from JS strings, and SECTIONS sets image `src` from JS. A root-absolute `'/img/x.webp'` or `'/models/tower.glb'` in `dist/assets/*.js` passes this check and 404s only on Pages, where the site lives under `/imobiliare_landing_page/`.
   - **Fixed looks like:** also fail on `grep -nE "[\"'\`](/(img|models|fonts|draco|basis)/)" dist/assets/*.js`. Better still, after the push, curl the live page, the hashed JS/CSS, `models/tower.glb` and every `img/*.webp` listed in `dist`, and exit non-zero on any non-200. That automates the DEPLOY.md "Verifying a deploy" section, which today is manual.
2. **major** · `tools/deploy.sh:20` · **Untracked work is deployed silently.**
   - **What's wrong:** the "uncommitted changes are not deployed" note uses `git status --porcelain --untracked-files=no`, so it only fires for modified tracked files. In this project the teams' output is untracked: right now there are 48 untracked files in `public/`, `src/hero/`, `src/sections/` and `blender/`. If `src/main.js` were committed with its mount lines, the note would stay silent, and Pages would get a build whose `public/img`, `models/` or hero modules are missing, or that fails to resolve its imports.
   - **Fixed looks like:** also list `git ls-files --others --exclude-standard` (excluding `docs/reviews/` if you like). Print the untracked paths under `public/` and `src/`, and refuse to deploy unless `DEPLOY_ALLOW_DIRTY=1` is set. Also warn when `HEAD` is not on `origin/main` (`git merge-base --is-ancestor HEAD origin/main`), because the SHA in the gh-pages message should be one people can find on the remote.
3. **minor** · `README.md` ("Credits") · **Broken link.** It links to `docs/ASSETS.md`, which does not exist yet.
   - **Fixed looks like:** at integration, confirm ASSETS.md is committed. Until then, word the line so it does not promise a file that isn't there.
4. **minor (owner: Lead, `index.html`; RELEASE should gate it)** · live `index.html:9` and the missing icon. There are two problems:
   - **Missing favicon.** There is no `<link rel="icon">`, so Chrome requests `https://strategieonline.github.io/favicon.ico` (origin root, not the sub-path). It returns 404, which is a console error on the live site and breaks SPEC §5.4 "no console errors". Fixed: an inline SVG data-URI icon, or a relative `./favicon.svg` with `<link rel="icon">`.
   - **Relative `og:image`.** `og:image` is `./img/og.webp`. Scrapers need an absolute URL, so social previews will not show the image, and `img/og.webp` is currently 404 (MEDIA hasn't delivered). Fixed: `https://strategieonline.github.io/imobiliare_landing_page/img/og.webp`, plus `og:url`, `og:description` and `twitter:card`.
5. **minor** · `README.md` and `docs/STATUS.md` · **Ownership and tense.**
   - **What's wrong:** the README table says RELEASE owns `docs/STATUS.md`, but STATUS.md says "Updated by the lead". Separately, the README describes the hero journey in the present tense while the live site is an empty shell.
   - **Fixed looks like:** settle the owner in one place. At integration, re-read the README against what actually shipped (for example, if depth maps or `city.glb` don't ship, don't imply them) and add one line on browser support and reduced motion.
6. **minor** · `docs/DEPLOY.md` "Never commit or publish" · **Ignored paths don't cover tracked files.**
   - **What's wrong:** the guidance to stage files by name is right. However, `docs/reviews/REFERENCE-INVENTORY.md` (judge-owned) describes the reference site's frames and English headlines. I have removed the brand and place names from it, but say explicitly in DEPLOY.md that judge docs get the same check before commit. Also, `.gitignore` covers `reference/` but not `**/source.mp4` or `**/frames/` copies elsewhere.
   - **Fixed looks like:** add a pre-commit grep step to DEPLOY.md (the term list comes from the judge, kept out of the repo).

Nothing else to report. The script's orphan force-push to `gh-pages` only, the identity passed with `-c` (no git config changes) and the explicit leak check for `reference` in `dist/` are good choices.
