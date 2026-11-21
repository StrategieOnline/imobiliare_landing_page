# FINAL acceptance: live site

**Site:** https://strategieonline.github.io/imobiliare_landing_page/ · gh-pages `2089c74` built from main `d1778f5` (main head `0e99eb7` is docs-only) · 2026-11-21

## Verdict: ACCEPTED, ready to hand to the user

Nothing blocks the handoff. Three cosmetic notes are at the end; none of them needs to be fixed first.

**Method:**
- Headless Chrome on the real GPU (ANGLE/Metal, Apple M4 Pro) against the **live Pages URL**, with the cache disabled.
- **Network accounting through CDP** (`Network.dataReceived` / `loadingFinished` per request), since my range server can't sit in front of Pages.
- Three runs: desktop 1440×900, mobile 375×812 @2x with touch, desktop with `prefers-reduced-motion`.
- Plus `curl` on the live assets, `gh api` on the gh-pages tree, `git` on main and history.
- These are real-internet numbers on this machine's connection, unthrottled.

## Live measurements

| | desktop 1440 (1080 file) | mobile 375 (720 file) | reduced motion |
|---|---|---|---|
| console errors / exceptions / failed requests | **0 / 0 / 0** | **0 / 0 / 0** | **0 / 0 / 0** |
| FCP | 548–760 ms | 600–892 ms | 728 ms |
| video request starts | 993 ms (after FCP ✅) | 1098 ms (after FCP ✅) | **none** ✅ |
| **first view (everything before the video request)** | **572 KB**: HTML 1 + JS 63 + CSS 8 + 10 font files ≈ 385 + `hero.json` 1 + poster 114. **Budget 3 MB ✅** | 509 KB ✅ | 1.5 MB (all stills, no video) ✅ |
| first presented video frame | 704–1091 ms | see note 1 | — |
| **idle at the top (RELEASE's question)** | the browser pulls **8.1 MB** (≈ 14 s of footage buffered, `[0, 14]`) within ~4 s, then **stops: 0 MB more over 20 s idle** | **3.8 MB** (`[0, 16.9]`), then 0 MB | 0 |
| bytes for a full scrub | 22.5 MiB = **1.00× the file**, one `bytes=0-` request (206) | one request (206) | — |
| scrub, 12 s forward / 12 s back | rVFC **60.4 / 60.4 fps**, max seek **10 / 9 ms**, rAF 16.7 ms, 0 frames > 50 ms | **60.4 / 60.4 fps**, max seek 8 / 11 ms | — |
| copy timing (0.5 s steps) | letters clear by 2.5 s → **ch1 `ETAJ CU ETAJ` from 3.5 s (gap ≈ 1.0 s ✅)**, held over the whole stacking until the blur-out at ~12 s → `TRAVERTIN` 12.5 s | same: ch1 at 3.5 s ✅ | static blocks ✅ |
| card at the end of the pin | `inset(57.6px round 18px)` = 4vw / 18px, over S6 ✅ | `inset(15px round 18px)` = 4vw ✅ | — |
| sections handoff after the pin | the card scrolls up and the manifesto starts exactly at the card's bottom edge (both at y = 360). Matches ref t_8.0 ✅ | same (y = 325) ✅ | no pin; the blocks flow into the manifesto ✅ |
| anchors (nav and CTA clicks through Lenis) | `#proiectul` 0 px, `#vizionare` 0 px from the top ✅ | `#rezidente` · `#locatie` · `#vizionare` · `#proiectul` all land at 0 px ✅ | all at 0 px ✅ |
| form | empty → 3 errors; valid → inline success, **0 network requests** ✅ | ✅ | ✅ |
| horizontal overflow | 0 | **0** | 0 |

**Live asset checks (curl):**
- `video/hero-1080.mp4`, `hero-720.mp4`, `hero-poster.webp` and `img/og.jpg` → **206** on Range, with the right `content-type`.
- `hero.json` → `status: final`; ch0 `0–3.5`, ch1 `3.5–12.125`; overlay `split [0.11, 2.6]`, `card [32.417, 39.0]`.
- `models/tower.glb`, `models/city.glb`, `draco/draco_decoder.js` → **404**, as intended.
- `og:image` is absolute and points at `og.jpg`. The favicon is an inline SVG.

## Release checks (R1–R11)

| ID | | evidence |
|---|---|---|
| R1 | ✅ | repo public |
| R2 | ✅ | `git rev-list --objects --all` shows **no** `reference/`, `source.mp4`, `placeholder.mp4` or `assets-src` paths. `.gitignore` covers `reference/`, `**/source.mp4`, `**/frames/`, `assets-src/`, `tools/.blocklist` and the guide MP4s |
| R3 | ✅ | page + all 26 dist files 200; video 206; 0 console errors live |
| R4 | ✅ | gh-pages = `index.html`, 2 assets, 18 stills, 4 video files, `.nojekyll`. No secrets |
| R5 | ✅ | `deploy.sh` refuses dirty or untracked site files (`DEPLOY_ALLOW_DIRTY` override), checks root-absolute URLs in JS/CSS/HTML, verifies every dist file live, and the placeholder ship gate is in place (`tools/check-video.sh`) |
| R6 | ✅ | the live `index.html` is byte-identical to the build (RELEASE log); the JS hash `BzgJfVT7` matches my local build of the same tree |
| R7 | ✅ | README checked against what shipped (below) |
| R8 | ✅ | largest committed files: `hero-1080.mp4` 23.6 MB and `hero-720.mp4` 9.5 MB (< 50 MB); renders ≤ 4 MB; `.blend1` and pyc ignored |
| R9 | ✅ | absolute `og:image`, favicon present |
| R10 | ✅ | `three` gone from `package.json` (deps: gsap, lenis); `public/models` + `public/draco` absent from dist and gh-pages (live 404); `public/video/*` deployed, 206, `video/mp4` |
| R11 | ✅ | `assets-src/` ignored; guide MP4s ignored (`blender/guides/*.mp4`); only `guides.json` and stills are committed; nothing from the guides deploys |

**README accuracy: accurate.** It describes exactly what shipped:
- The 39 s two-way scrubbed video and the overlay set.
- The handoff and the section list.
- "No WebGL; three.js removed", which is correct (0 canvas).
- Stream 1080 / 720 under 768 px or Save-Data, which matches the network log.
- The reduced-motion static mode, which matches the reduced run.
- The `-g 6`, no-B-frame encode, which matches `ffprobe`.

Every script and path it names exists on main: `tools/video/merge.sh`, `compare.sh`, `measure.sh`, `tools/check-video.sh`, `precommit-check.sh`, `deploy.sh`, `blender/build_tower.py`, `build_guides.py`, `blender/export/*.glb`, `blender/guides/guides.json`.

The honest caveat is stated too: a fresh clone can rebuild the site but not the video, because the raw Higgsfield downloads are local-only.

## Final scores per team

| team | final verdict | craft | one-line justification |
|---|---|---|---|
| **HERO** (video scrub) | PASS | **9/10** | Frame-accurate two-way scrub at 60 fps on both files. One download, zero refetch, the first view at ~0.5 MB. Copy is locked to the displayed frame and timed from JSON. The card and handoff are exact. |
| **SECTIONS** | PASS | **8.5/10** | The closest component-for-component match to the reference (hover list, marquee, inset materials, clipped footer wordmark), with flawless 375 px / reduced-motion / form behaviour. All four round-1 minors are fixed (mobile hint hidden, `orizont.example`, tighter numeral drift, lazy previews via IntersectionObserver). |
| **VIDEO** (merged hero film) | PASS (known flaw accepted) | **8/10** | One believable camera move from rooftop to living room, with physical stacking, a constant 24-storey tower and the band. Every second is traceable Higgsfield video. Points off for the slab A facade dissolve at S2→S3 (accepted). |
| **MEDIA** (stills) | PASS | **8/10** | A coherent material world and a convincing north Bucharest, used for the sections, the reduced-motion blocks and the video references. |
| **3D** (model + motion guides) | PASS | **7/10** | Contract-perfect and reproducible. The real-scale guides, with the slab yardstick, are what made the video spatially honest. The round-1 look issues mattered less once the GLB became a guide rather than an on-screen asset. |
| **RELEASE** | PASS | **9/10** | Public repo, clean history, Pages live, a deploy that refuses unsafe states and verifies itself, ship gates for the placeholder and the blocklist, an accurate README. |

**Overall craft: 8.5/10.** It hits the reference's motion grammar and editorial typography with an original brand, and every frame is traceable to its source.

## Notes (not blocking the handoff)
1. **Mobile poster flag.** On 375 px the poster `<img>` keeps its visible state after the video is ready: `readyState 4`, but `.hx-poster` never gets `is-hidden` until the first scroll. That's a benign race in `src/hero/video.js`. The first `requestVideoFrameCallback` can fire before `ready` is set, and the follow-up seek to t = 0 presents no new frame. **It's invisible**, because the poster *is* frame 0, and the first scroll hides it. Optional fix: also hide the poster on `seeked` after `loadeddata`, or call `presented()` directly in the `loadeddata` handler.
2. **Dead stills on Pages.** Four `*_depth.webp` (32 KB in total) still deploy but nothing uses them since the three.js hero went away. Remove them from `public/img/` at leisure.
3. **Known accepted video flaw:** the slab A facade changes inside the 0.25 s S2→S3 dissolve (see VIDEO.md, FINAL).
