# ORIZONT — Real-estate landing page · Build spec (single source of truth)

All teams and the judge work from this file. If something here is ambiguous, pick the option
that is closest to the reference frames in `reference/` and write the decision in
`docs/DECISIONS.md` (append-only, one line per decision, prefixed with your team name).

## 0. What we are making

A scroll-driven, cinematic **three.js** landing page for a fictional luxury residential tower,
**ORIZONT — Rezidențe private în București**. The hero is a "step inside the website"
camera journey: from a rooftop at dusk, the tower rises out of nothing, the camera flies to its
stone seam, into a loggia and finally inside an apartment, then the canvas shrinks
into a card and hands off to editorial content sections.

The reference is a screen recording of a different site, at `reference/source.mp4`, with frames in
`reference/frames/` (4 fps), cropped screen keyframes in `reference/keyframes/t_<seconds>.jpg` and
contact sheets in `reference/*.jpg`. We match the **structure, motion grammar, typography system
and component types**. We do **not** copy its name, wordmark, copy text or imagery: everything
is our own brand (ORIZONT), our own Romanian copy and our own generated assets.

Language: **Romanian** copy (diacritics ș ț ă î â must render, so fonts need the latin-ext subset).

## 1. Stack and repo layout

- Vite 5 + vanilla ES modules, `three@0.170`, `gsap@3.12` (+ ScrollTrigger), `lenis@1.1` smooth scroll. Already installed.
  No React. No other runtime deps without writing a line in DECISIONS.md.
- `vite.config.js` has `base: './'`. **All asset URLs must be relative** (`./img/...`, or via
  `import.meta.env.BASE_URL`), never absolute `/img/...`, because the site is served under
  `https://strategieonline.github.io/imobiliare_landing_page/`.
- Deployed as a static build to GitHub Pages (branch `gh-pages`, built `dist/`, plus `.nojekyll`).

```
index.html                 shell: <header id="nav">, <section id="hero">, <main id="content">, <footer id="footer">
src/main.js                bootstrap (Lenis + GSAP ticker + mounts). Owner: Lead. Teams may add ONE import + mount line each.
src/styles/tokens.css      design tokens + fonts + base. Owner: Lead. Teams request changes in DECISIONS.md, or add to their own css.
src/hero/**                Team HERO (three.js scene, camera path, hero overlays, the canvas-to-card handoff)
src/sections/**            Team SECTIONS (nav, all content sections, footer). One file per section + sections.css
public/models/**           Team 3D (Blender → glb)
blender/**                 Team 3D (.blend, export scripts, renders)
public/img/**              Team MEDIA (Higgsfield-generated images, optimised webp)
docs/ASSETS.md             Team MEDIA and Team 3D: manifest of every asset (path, size, source prompt/tool, credits)
docs/reviews/<team>.md     JUDGE: one review file per team
README.md, docs/DEPLOY.md  Team RELEASE
```

Never edit files owned by another team. If you need something from them, write it in
`docs/DECISIONS.md` under `REQUEST:` and work around it with a placeholder.

## 2. Design tokens (in src/styles/tokens.css)

| token | value | use |
|---|---|---|
| `--ink` | `#141518` | dark section background |
| `--ink-2` | `#1d1f24` | dark panels / table rows |
| `--slate` | `#3e5066` | "above the city" dusk-blue section |
| `--paper` | `#efe9df` | light editorial section bg |
| `--cream` | `#f1e7d0` | display type on photos |
| `--gold` | `#d8b26a` | italic serif accent, CTA pill |
| `--gold-soft` | `#e9d6a6` | CTA pill bg |
| `--line` | `rgba(241,231,208,.18)` | hairlines on dark |
| `--muted` | `rgba(241,231,208,.6)` | small text on dark |

Typography (Google Fonts, latin-ext):
- **Display**: `Unbounded` 700–900, UPPERCASE, tight tracking (-0.02em), line-height .9. The wide,
  heavy grotesk of the reference.
- **Accent**: `Instrument Serif` *italic*, lowercase, in `--gold` (on photos) or `--gold`/ink (on paper).
  Every headline is `CAPS DISPLAY + italic serif tail`, e.g. `ÎNTÂI, <em>lumina.</em>`
- **UI/labels**: `JetBrains Mono` 400–500, 10–12px, uppercase, letter-spacing .08em: section
  indices (`01 / PROIECTUL`), timecodes, table data.
- **Body**: `Inter Tight` 400, 15–17px.

Recurring details from the reference that we keep:
- Corner crop-marks `⌐` in the hero corners and a running timecode `TC 00:00:00:00` bottom-left that advances with scroll.
- A small circular "scroll cursor" ring (⊙, ~28px, hairline) that follows the mouse with lerp, and sits at the right-middle of sections.
- Chapter index labels like `02 — FORMA` above each headline, plus a right-side chapter list in the hero that highlights the active chapter.
- Pill CTA top-right: `PROGRAMEAZĂ O VIZIONARE`, `--gold-soft` bg, ink text.

## 3. Page structure and copy (top to bottom)

### NAV (Team SECTIONS), fixed, transparent over the hero
Left: `ORIZONT` wordmark (Unbounded 800, 14px) + mono `BUCUREȘTI / NORD`. Center-right links (mono):
`01 PROIECTUL · 02 ARHITECTURA · 03 REZIDENȚE · 04 LOCAȚIE`. Right: gold pill CTA. It turns
`mix-blend-mode: difference`, or gets a solid ink bg, once past the hero.

### HERO: scroll journey (Team HERO). Pinned, about 600vh of scroll, one `<canvas>`, fullscreen.
Each chapter = camera keyframe + headline + 1–2 line body + chapter index. Headlines bottom-left
at ~8vw, bottom ~10vh. Text enters with a per-line mask reveal (translateY 110%→0, 0.9s,
`power4.out`), exits with a blur + fade (filter blur 0→12px, opacity→0) as the camera moves on, as in the reference.

| # | scroll % | camera / scene | headline | body |
|---|---|---|---|---|
| 0 | 0–12 | Rooftop terrace at dusk (photo plate with depth parallax). Giant `ORIZONT` wordmark (~19vw, cream) across the lower third. | `ORIZONT` + sub `Rezidențe private în <em>București</em>` | right column: `Un turn de sticlă bronz, străbătut de o coloană de travertin.` |
| 1 | 12–30 | On scroll, the wordmark letters **split apart and fly past the camera** (each letter its own z-depth, blur rising, scale up). The camera rises above the parapet and reveals the skyline. **The 3D tower assembles floor by floor** out of nothing (floors drop/scale in from y+, staggered from the ground up) into an empty plot between the skyline buildings. | `DIN NIMIC, <em>o formă.</em>` | `Sticlă bronz închis, travertin palid. Turnul se ridică în jurul unui singur gest.` |
| 2 | 30–48 | Camera orbits and dollies close to the tower to the **vertical travertine seam** with stacked loggias glowing warm. Aerial city plate as backdrop. | `O COLOANĂ <em>de piatră.</em>` | `Un ax de travertin urcă pe toată înălțimea fațadei și deschide fiecare casă spre oraș.` |
| 3 | 48–64 | Camera pushes into one loggia: the frame fills with the loggia (photo plate with depth), through the open sliding glass. | `O CAMERĂ <em>în aer liber.</em>` | `Fiecare rezidență se deschide într-o logie săpată în piatră, suspendată deasupra orașului.` |
| 4 | 64–82 | Through the threshold into the living room (interior plate, slow dolly + parallax, warm practical lights, blue-hour window). | `ORAȘUL, <em>în liniște.</em>` | `Lemn, piatră și lumină caldă. Traficul ajunge aici doar ca ritm al luminilor.` |
| 5 | 82–100 | The whole canvas **scales down into a rounded card** (inset 4vw, radius 18px) while the next dark section slides up beneath. The card shows the interior. Headline + 2 buttons. | `VINO SĂ O <em>vezi.</em>` | buttons: `PROGRAMEAZĂ O VIZIONARE` (pill), `EXPLOREAZĂ REZIDENȚELE` (ghost) |

The hero also shows a right-side chapter list (mono, 10px): `01 TERASA · 02 FORMA · 03 COLOANA · 04 LOGIA · 05 INTERIORUL`, with the active one cream and the others muted, plus `TC` timecode bottom-left and crop marks.

Transitions between photo-plate chapters must feel like **moving through space, not a slideshow**:
the outgoing plate scales up (camera pushes in) with radial blur/zoom and a crossfade into the incoming
plate, which starts slightly scaled up and settles. Use a custom ShaderMaterial on fullscreen planes
(uniforms: progress, depth map optional, mouse parallax). The 3D tower chapters (1–2) composite the
GLB over the skyline/aerial plates with fog matched to the plate's horizon colour.

### SECTIONS (Team SECTIONS), in order
1. **Manifesto** (`--ink`): mono label `01 / PROIECTUL`; huge paragraph (Unbounded 600, ~3.2vw, mixed cream/muted)
   revealing word-by-word on scroll (opacity .15→1 scrubbed):
   `Orizont este un nou turn rezidențial în nordul Bucureștiului: 46 de locuințe private pe 24 de etaje, deasupra copacilor din Herăstrău. O coloană de travertin palid traversează sticla și susține logiile — fiecare casă are o cameră în aer liber, adâncă și adăpostită, cu fața spre oraș.`
   Then a **stats row**, 4 columns with hairline tops: `REZIDENȚE 46` · `ETAJE 24` · `LIVRARE 2028` · `ÎNĂLȚIME 96 m`. Numbers count up and use a **glitch/scramble** reveal (random digits settle to the final value).
2. **Marquee**: infinite horizontal band of outlined + filled Unbounded words separated by `✦`:
   `TRAVERTIN ✦ BRONZ ✦ STEJAR AFUMAT ✦ STICLĂ ✦ LUMINĂ ✦`, alternating filled/outlined; speed reacts to scroll velocity (Lenis velocity), direction flips with scroll direction.
3. **Trei gesturi** (`--paper`, light). Pinned horizontal scroll. Left: headline `TREI GESTURI, <em>o clădire.</em>`.
   Then 3 cards translating horizontally: each = large image (clip-path reveal + inner image parallax) + huge outlined
   number (`01`, `02`, `03`, Unbounded outline stroke) + title + 2-line text:
   `01 COLOANA` (tower exterior), `02 LOGIA` (loggia), `03 PRAGUL` (threshold / entrance looking into the apartment).
4. **Rezidențe** (`--ink`): headline `FIECARE PLAN ÎNCEPE <em>cu logia.</em>` + right mono note `46 rezidențe, de la 112 la 480 m²`.
   An index list of 3 rows (Unbounded 700, ~5vw): `REZIDENȚA LOGIA`, `REZIDENȚA DE COLȚ`, `PENTHOUSE`; each row has an index `01..03`,
   mono specs on the right (`2–3 CAMERE · 112–160 m² · ETAJ 4–18`), an arrow. **Hover** = the row text goes outlined→filled and
   a floating image preview (aspect 4:5) follows the cursor with lerp and swaps per row with a clip reveal. Non-hovered rows dim to 35%.
5. **Materiale**: full-bleed interior image (100vh) with slow scale (1.15→1) on scroll, headline bottom-left
   `LEMN ÎNCHIS, PIATRĂ PALIDĂ, <em>lumină indirectă.</em>` + short body.
6. **Locație** (`--slate`): headline `DEASUPRA ORAȘULUI, <em>în mijlocul lui.</em>`, right image of the tower in the city (parallax).
   Below: address line (mono) `Șoseaua Nordului 12, București` and a distances table (mono rows with hairlines):
   `Parcul Herăstrău — 3 min pe jos`, `Piața Charles de Gaulle — 6 min`, `Aeroportul Otopeni — 18 min`, `Centrul Vechi — 15 min`. Rows stagger-in.
7. **Vizionare / contact** (`--ink`): `PROGRAMEAZĂ <em>o vizionare privată.</em>` (huge). Body: `Te întâmpinăm în showroom, îți arătăm planurile și disponibilitatea și te însoțim pe șantier.`
   Form in a 2-column grid of underline inputs (mono labels): Nume, Email, Telefon, Tip rezidență (select), Mesaj, submit pill.
   The form is front-end only: on submit, show an inline success state. No network calls.
   Headline letters use the reference's **distorted/smeared** reveal (scaleY stretch + blur settling), rendered with CSS/GSAP.
8. **Footer** (`--ink`): mono nav row + `ÎNAPOI SUS ↑`, a legal line (`Imaginile sunt vizualizări generate digital și au caracter ilustrativ.`), and a **giant ORIZONT wordmark** spanning the full width at the bottom, clipped by the viewport bottom edge, rising in on scroll.

Global: Lenis smooth scroll; the custom cursor ring; `prefers-reduced-motion` disables scrub-heavy effects (static images, no pin), and the page must stay readable.

## 4. Asset contract (exact filenames; consumers code against these now, with fallbacks)

Team MEDIA, `public/img/` (webp, quality ~82; plates 2560×1440, others as noted). Optional depth maps `*_depth.webp`, grayscale, white = near.
| file | content |
|---|---|
| `hero-rooftop.webp` | Rooftop terrace in north Bucharest at dusk: low parapet, potted olive trees, distant low skyline and trees, warm sunset sky, empty space in the lower third for the wordmark. Eye level, 24mm, photoreal architectural photography. |
| `skyline-dusk.webp` | Bucharest north skyline at golden hour seen from mid-height: several mid-rise glass office towers, **an empty gap/plot in the center** where our tower will be composited, trees below, hazy warm sky. |
| `aerial-city.webp` | High aerial view over the city at dusk, endless low-rise blocks and parks to the horizon, warm haze, no dominant tower in the center third (backdrop behind the 3D tower). |
| `tower-exterior.webp` (1600×2000) | Hero architectural render of THE tower: slender 24-storey tower, dark bronze-tinted glass curtain wall, a full-height vertical **pale travertine seam** that cuts diagonally on one corner, with deep stacked loggias carved into it glowing warm from inside, at dusk with the city behind. |
| `loggia.webp` | Looking into one deep loggia from outside: travertine frame, floor-to-ceiling sliding glass open, warm-lit living room beyond, dusk city reflected. |
| `interior-living.webp` | Living room: dark smoked oak joinery wall with shelves, pale travertine floor, low cream sofa, wood coffee table, warm indirect cove lighting, big window to blue-hour city. |
| `threshold.webp` (1600×2000) | Entrance threshold: pivot door open, view down a travertine corridor into the warm living room. |
| `res-loggia.webp`, `res-corner.webp`, `res-penthouse.webp` (1200×1500) | Three distinct interiors in the same material language (corner one with a two-sided glass corner; penthouse double-height with city view). |
| `materials.webp` | Moody interior close-ish: dark wood, pale stone, indirect light. Full-bleed. |
| `location.webp` (1600×2000) | The tower among the city at blue hour, seen from a distance with Herăstrău lake/park. |
| `og.webp` (1200×630) | Social preview. |

Team 3D, `public/models/tower.glb` (≤ 6 MB, Draco or meshopt OK; three.js loader setup must match):
- Units in metres, Y-up after export (glTF default), origin at the base centre. ~96 m tall, ~24 floors, footprint ~28×20 m.
- Node naming contract: `Floor_00` … `Floor_23` (one node per floor slab and its glass band, for the floor-by-floor build-up),
  `Seam` (travertine seam mesh), `Loggia_00…` (loggia recesses, optional), `Crown` (top), `Podium`.
- Materials: `M_Glass` (dark bronze, metalness ~.6, roughness ~.15), `M_Stone` (warm travertine, roughness .8), `M_WindowGlow`
  (emissive warm interior, used on some window panels/loggia backs so the tower reads lit at dusk), `M_Frame` (dark bronze metal).
- Also: `public/models/city.glb` (optional, ≤ 3 MB): low-poly context blocks around the tower in the same coordinate frame.
- Renders: `blender/renders/*.png` used by MEDIA as references if helpful.

Fallback rule: Team HERO must build a **procedural placeholder tower** in three.js with the same node names, so the page
works if the GLB is missing; when `tower.glb` exists it is used instead. Team SECTIONS uses CSS gradient placeholders for missing images.

## 5. Quality bar (the judge scores against this)

1. **Fidelity to reference motion**: wordmark split, floor-by-floor rise, seam approach, push into the loggia, interior dolly, canvas→card shrink, mask text reveals and blur exits, marquee, horizontal gestures, hover list preview, scramble stats, smeared headline, giant footer wordmark.
2. **Originality**: no reference brand name, wordmark or copy. Our own assets.
3. **Visual craft**: type scale and spacing match the reference's editorial feel; nothing looks templated; diacritics render.
4. **Performance**: 60fps on an M-series laptop; DPR capped at 2 (1.5 while scrolling OK); textures ≤ 2560px; total transfer for the
   first view ≤ 8 MB; lazy-load section images; no console errors.
5. **Robustness**: `npm run build` passes; works under a sub-path (relative URLs); responsive down to 375px wide (hero
   simplifies: shorter scroll, smaller type; horizontal gestures become a vertical stack); `prefers-reduced-motion` honoured.
6. **Code**: small modules, no dead code, no secrets, comments only where the motion maths is non-obvious.

## 6. Team protocol

- Work only inside your owned paths. Log decisions/requests in `docs/DECISIONS.md`.
- Do not run `git commit` or `git push`. Team RELEASE does all git operations.
- Do not run long-lived dev servers in the foreground; for checks use `npx vite build`, or start `npx vite --port <your port>` in the background
  and kill it when done. Ports: HERO 5101, SECTIONS 5102, RELEASE 5103, JUDGE 5104.
- When done, write a short handoff at the top of `docs/HANDOFF-<TEAM>.md`: what was built, how to verify, known gaps.
