> **Repo depreciat din 23 noiembrie 2026.** Landing-ul trăiește acum în
> [`StrategieOnline/imobiliare_demo`](https://github.com/StrategieOnline/imobiliare_demo), în `apps/site`,
> sub numele **Upstream Residence**, la https://imobiliare.strategieonline.ro.
> Acest repo rămâne doar pentru istoric și pentru sursele asset-urilor (Blender, [docs/ASSETS.md](docs/ASSETS.md)).
> Nu se mai lucrează aici.

# ORIZONT — Rezidențe private în București

A scroll-driven, cinematic landing page for ORIZONT, a fictional luxury residential tower in
north Bucharest. The copy is in Romanian.

**Live:** https://strategieonline.github.io/imobiliare_landing_page/

The hero is one continuous, 39-second video that your scroll scrubs frame by frame, in both
directions. The camera rises over a rooftop parapet at dusk and watches the tower stack floor by
floor on an empty plot. It then orbits the finished tower, dollies into a loggia and passes
through the sliding glass into the living room. A DOM overlay sits on top of the video: the
ORIZONT wordmark splits apart, chapter headlines mask in and blur out, and a HUD shows a timecode,
the chapter list and crop marks. At the end, the video shrinks into a card and hands over to the
editorial sections: manifesto with scramble stats, marquee, horizontal "three gestures",
residences list with hover previews, materials, location, viewing form, then the footer.

- Brief and amendments: [docs/SPEC.md](docs/SPEC.md) (§8 describes the video hero)
- Progress and judge verdicts: [docs/STATUS.md](docs/STATUS.md)
- Reviews: [docs/reviews/](docs/reviews/)
- Every asset with its source, prompt and job: [docs/ASSETS.md](docs/ASSETS.md)
- Decision log: [docs/DECISIONS.md](docs/DECISIONS.md)
- Deploying: [docs/DEPLOY.md](docs/DEPLOY.md)

## How the hero video is made

There is no WebGL on the page; three.js was removed. Every frame on screen comes from a
Higgsfield generation.

1. **Motion guides (Blender).** A single Blender scene holds the tower, the city context, the
   rooftop, the loggia and the living room, at real scale (3.6 m storeys, one 28 mm lens, a fixed
   back-right sun). One continuous camera spline runs through six shots: RISE, STACK, ORBIT,
   APPROACH, THRESHOLD and DRIFT. They render as 720p guide clips with 12-frame overlaps at the
   cuts. The guides are only a motion and geometry reference: they are never published.
2. **Restyle (Higgsfield).** Each guide shot is edited video-to-video into photoreal footage,
   with the approved stills in `public/img/` as image references. Where an edit drifted, the
   shot was regenerated from photoreal first and last keyframes. Every segment traces back to a
   Higgsfield job id.
3. **Merge (ffmpeg).** `tools/video/merge.sh` grade-matches the shots and crossfades them at the
   cuts. It encodes 1080p and 720p H.264 with a keyframe every 6 frames and no B-frames, so
   seeking is fast for scrubbing, and writes a poster and `hero.json` with shot and chapter
   timings. The overlay timing is driven entirely by that JSON.

The page streams `video/hero-1080.mp4`, or the 720p file under 768 px wide or with Save-Data on,
as a single range request. With `prefers-reduced-motion`, the hero is static: the poster and
still images, with no video and no pinning.

## Stack

- [Vite 5](https://vitejs.dev/), vanilla ES modules, no framework
- [GSAP 3.12](https://gsap.com/) + ScrollTrigger (pinning and scrub), [Lenis](https://lenis.darkroom.engineering/) 1.1 (smooth scroll)
- An HTML `<video>` scrubbed via `requestVideoFrameCallback` (the hero)
- Fonts from Google Fonts (latin-ext): Unbounded, Instrument Serif, JetBrains Mono, Inter Tight
- Asset pipeline: Blender (Python, headless), Higgsfield, ffmpeg

## Run, build, deploy

```bash
npm i
npm run dev        # http://localhost:5173
npm run build      # static site in dist/
npm run preview    # serve dist/
bash tools/precommit-check.sh   # before every commit (see docs/DEPLOY.md)
npm run deploy     # build committed HEAD, publish to gh-pages, verify live
```

`vite.config.js` sets `base: './'`, so all URLs are relative and the build works under the
GitHub Pages sub-path. Never write root-absolute paths (`/img/...`); `deploy.sh` refuses them.

## Rebuilding the assets

```bash
# 3D: tower model -> blender/export/tower.glb, city.glb (+ preview renders)
/Applications/Blender.app/Contents/MacOS/Blender -b -P blender/build_tower.py
# motion guides -> blender/guides/S1..S6.mp4, S#_first/last.png, guides.json (~20 min; mp4s are gitignored)
/Applications/Blender.app/Contents/MacOS/Blender -b -P blender/build_guides.py
# hero video: merge the downloaded Higgsfield shots listed in assets-src/video/shots.tsv
SPLIT_END=2.6 CH1_START=3.5 tools/video/merge.sh
```

`assets-src/` holds the raw Higgsfield downloads. It is local only and never committed, so a
fresh clone can rebuild the site but not the video. QA helpers: `tools/video/compare.sh`
(guide versus edit, frame-stepped) and `tools/video/measure.sh` (same-scale geometry check).

## How it was built

Parallel AI agent teams built the site. Each team owned its own folders, a lead coordinated, and
an independent judge reviewed every deliverable against the rubric in
[docs/reviews/RUBRIC.md](docs/reviews/RUBRIC.md) until it passed.

| team | owns | job |
|---|---|---|
| **3D** | `blender/**` | tower model, motion-guide scene and camera, `blender/export/*.glb` |
| **MEDIA / VIDEO** | `public/img/**`, `public/video/**`, `tools/video/**` | Higgsfield stills, then the Higgsfield edit and merge of the hero video |
| **HERO** | `src/hero/**` | scroll-scrubbed video hero, overlays, card handoff, reduced-motion fallback |
| **SECTIONS** | `src/sections/**` | nav, cursor, content sections, footer |
| **RELEASE** | `README.md`, `docs/DEPLOY.md`, `tools/*.sh` | git, GitHub, deploy, pre-commit and ship gates, QA |
| **Judge** | `docs/reviews/**` | reviews and verdicts |

The lead owns `index.html`, `src/main.js`, `src/styles/tokens.css`, `docs/SPEC.md` and
`docs/STATUS.md`. Each team's handoff is `docs/HANDOFF-<TEAM>.md`.

```
index.html            page shell (nav, hero, content, footer)
src/main.js           bootstrap: Lenis + GSAP ticker + team mounts
src/styles/tokens.css design tokens, fonts, base styles
src/hero/             video scrub, timeline, overlay, static fallback
src/sections/         one module per section + css/
public/img/           stills (webp) + og image
public/video/         hero-1080.mp4, hero-720.mp4, hero-poster.webp, hero.json
blender/              build scripts, .blend files, export/*.glb, guide stills + guides.json, renders, textures
tools/                deploy.sh, precommit-check.sh, check-video.sh, video/ (merge + QA)
docs/                 spec, status, decisions, assets, deploy, handoffs, reviews
```

## Credits

- **Imagery and the hero video** are AI-generated with [Higgsfield](https://higgsfield.ai/).
  The video is restyled from our own Blender motion guides. Sources, prompts and job ids are in
  [docs/ASSETS.md](docs/ASSETS.md).
- **The 3D tower and the guide scene** are modelled in [Blender](https://www.blender.org/).
- ORIZONT is a fictional project. All visuals are digitally generated and illustrative only; they
  show no real building.
