# ORIZONT — Rezidențe private în București

A scroll-driven, cinematic **three.js** landing page for ORIZONT, a fictional luxury residential
tower in north Bucharest. The hero is a camera journey: a rooftop at dusk, the tower assembling
floor by floor, a fly-in to its travertine seam, into a loggia and the apartment. Then the canvas
shrinks into a card and hands over to editorial content sections. The copy is in Romanian.

**Live:** https://strategieonline.github.io/imobiliare_landing_page/

## Stack

- [Vite 5](https://vitejs.dev/), vanilla ES modules, no framework
- [three.js](https://threejs.org/) 0.170 (hero scene, custom shader plates, GLB tower)
- [GSAP 3.12](https://gsap.com/) + ScrollTrigger (scroll choreography)
- [Lenis](https://lenis.darkroom.engineering/) 1.1 (smooth scroll)
- Fonts from Google Fonts (latin-ext): Unbounded, Instrument Serif, JetBrains Mono, Inter Tight

## Run locally

```bash
npm i
npm run dev        # http://localhost:5173
```

## Build

```bash
npm run build      # static site in dist/
npm run preview    # serve dist/ locally
```

`vite.config.js` sets `base: './'`, so every asset URL is relative and the build works under the
GitHub Pages sub-path. Never write root-absolute URLs (`/img/...`); use `./img/...` or
`import.meta.env.BASE_URL`.

## Deploy

```bash
npm run deploy     # = bash tools/deploy.sh
```

This installs dependencies, builds, checks `dist/` for sub-path safety, then force-pushes `dist/`
(plus `.nojekyll`) as a single orphan commit to the `gh-pages` branch. GitHub Pages serves that
branch at the live URL above. Details and troubleshooting are in [docs/DEPLOY.md](docs/DEPLOY.md).

## How it was built

The site was built by parallel AI agent teams, each owning its own folders, coordinated by a lead
and reviewed by an independent judge:

| team | owns | job |
|---|---|---|
| **3D** | `blender/**`, `public/models/**` | tower model in Blender, exported as `tower.glb` |
| **MEDIA** | `public/img/**` | Higgsfield-generated photo plates and section imagery (webp) |
| **HERO** | `src/hero/**` | three.js scene, camera path, hero overlays, canvas-to-card handoff |
| **SECTIONS** | `src/sections/**` | nav, all content sections, footer |
| **RELEASE** | `README.md`, `docs/DEPLOY.md`, `docs/STATUS.md`, `tools/**` | git, GitHub, deploy, QA |
| **Judge** | `docs/reviews/**` | reviews each team against the quality bar in the spec |

Shared files: `index.html`, `src/main.js` and `src/styles/tokens.css` belong to the lead;
`docs/ASSETS.md` is the asset manifest kept by MEDIA and 3D; `docs/DECISIONS.md` is an append-only
decision log. The full brief is [docs/SPEC.md](docs/SPEC.md), progress is in
[docs/STATUS.md](docs/STATUS.md).

```
index.html            page shell (nav, hero, content, footer)
src/main.js           bootstrap: Lenis + GSAP ticker + mounts
src/styles/tokens.css design tokens, fonts, base styles
src/hero/             hero scene
src/sections/         content sections, one file each + sections.css
public/img/           imagery (webp)
public/models/        tower.glb (+ optional city.glb)
blender/              .blend sources, export scripts, renders
docs/                 spec, decisions, assets, deploy, status, reviews
tools/deploy.sh       build + publish to gh-pages
```

## Credits

- **Imagery** is AI-generated with [Higgsfield](https://higgsfield.ai/). Every image, with its
  prompt and tool, is listed in [docs/ASSETS.md](docs/ASSETS.md).
- **The 3D tower** is modelled in [Blender](https://www.blender.org/) and exported to glTF.
- ORIZONT is a fictional project. The visuals are digitally generated and illustrative only; they
  show no real building.
