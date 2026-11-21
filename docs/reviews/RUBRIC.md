# Judge rubric

Sources: `docs/SPEC.md` (§3 structure, §4 asset contract, §5 quality bar, **§7 AMENDMENT 1**) and `docs/reviews/REFERENCE-INVENTORY.md`.
**§7 supersedes the §3 copy and settles the budgets, anchors, cursor API, Seam split, mount order and mobile/reduced-motion behaviour.** Every copy check below means the §7 copy.
Every item is pass/fail and checkable. The tag after each ID is the **severity if it fails**: **[B]** blocker, **[M]** major, **[m]** minor.
Items marked *(judge proposal)* add a number the spec still leaves open. The lead can override them in DECISIONS.md, and until then they apply.
Rev 2 (2026-11-21): aligned with §7.
Rev 3 (2026-11-21): **SPEC §8 AMENDMENT 2.** The hero is a merged, scroll-scrubbed Higgsfield video built from Blender motion guides, and three.js is removed. Added HERO-v2, VIDEO and 3D-GUIDES; the three.js HERO checklist is retired; 3D is now a production file; RELEASE gets R10–R11.
Rev 4 (2026-11-21): **SPEC §8.4 user rule:** no panned or zoomed stills; every second of the hero is Higgsfield video. Added blockers V13 and HV13.

## Verdicts and scores

- **FAIL**: any [B] fails, or 4 or more [M] fail.
- **PASS WITH FIXES**: no [B] fails, and 1–3 [M] fail or any [m] fails. The team gets a numbered fix list, then a re-review round.
- **PASS**: no [B] or [M] fails, and at most 2 [m] are open. They are listed as nice-to-have.
- **Craft score 1–10** (separate from the verdict; it judges how it looks, moves and reads, against the reference):
  - 1–3 broken or placeholder-grade.
  - 4–5 works but looks templated or generic, and the motion is linear or slideshow-like.
  - 6–7 solid and on-brief, with a few rough edges in timing, spacing or assets.
  - 8–9 reads like the reference: eased, layered motion, editorial type, and assets that hold up at 100%.
  - 10 better than the reference.
  - Each score has 2–4 sentences of justification that name the specific frames or files.
- Each review file `docs/reviews/<TEAM>.md` gets one dated round per review. A round has the verdict, the score, the checklist with ✅/❌/n.a. per ID, and numbered findings. Each finding has: severity · file:line or asset · what is wrong · what "fixed" looks like.

## Shared checks (every team that ships code or assets)

- G1 [B] `npx vite build` passes with no errors, and with no new warnings attributable to the team.
- G2 [B] The team touched only its owned paths (§1/§6) plus, for HERO and SECTIONS, at most one import line and one mount line in `src/main.js`. Checked by mtime/diff against the other teams' areas.
- G3 [B] Relative asset URLs only. `grep -rnE "[\"'\`(]/(img|models|fonts|assets)/" src index.html` finds nothing. The build works served under a sub-path: the judge serves a copy of `dist/` at `http://localhost:5104/imobiliare_landing_page/` and every request returns 200.
- G4 [B] Originality. A case-insensitive grep of `src public docs/ASSETS.md README.md index.html` for the reference brand, its city and its neighbourhood names finds nothing (the judge holds the term list; it is kept out of the repo on purpose). There is no reference copy text in English and no reference frames are used as image inputs.
- G5 [M] No console errors or warnings during a full top→bottom→top scroll in Chrome. This includes 404s, WebGL warnings and unhandled promise rejections.
- G6 [M] Romanian copy matches §7 character for character (the §3 copy is superseded; any leftover §3 line counts as a fail), including the diacritics ș ț ă î â. Comma-below Ș/Ț is used, not cedilla Ş/Ţ (U+0218–021B, not U+015E/0162). The glyphs render in the intended font with no fallback-font glyph visible at 200% zoom.
- G7 [m] Code: small modules, no dead or commented-out code, no secrets, comments only where the maths is non-obvious, no new runtime deps without a DECISIONS line.
- G8 [M] A handoff exists (`docs/HANDOFF-<TEAM>.md`) with what was built, how to verify and known gaps, and its claims are true.

## HERO-v2 (video-scrub hero, `src/hero/**`; SPEC §8.3.3, which supersedes the three.js HERO checklist of rev 2)

- HV1 [B] **No three.js anywhere.** `grep -rn "from 'three'\|three/addons\|three/examples" src` is empty. `three` is gone from package.json and the lockfile. The built JS bundle carries no three.js code (the main chunk shrinks by ~600 kB; no `WebGLRenderer`/`THREE` strings). No WebGL context is created on the page.
- HV2 [B] **Blob-fetched video.** The video is fetched with `fetch` → `blob` → `URL.createObjectURL`, then played in `<video muted playsinline preload="auto">`. The poster shows until it's ready, and a HUD loading bar tracks real fetch progress. The network panel shows one full GET per video, with no range traffic while scrubbing.
- HV3 [B] **Smooth scrub, forward and backward.** Scroll progress maps to a target time, and `currentTime` is eased toward it in rAF, using `requestVideoFrameCallback` where available. Measured in headless Chrome on the real GPU (ANGLE/Metal) at 1080p, over a 10 s scripted scroll forward and then back:
  - ≥ 20 presented video frames per second while moving (rVFC count).
  - No seek stall > 150 ms *(judge proposal)*.
  - rAF median ≤ 17.5 ms.
  - At rest, the displayed frame settles within 1 frame of the target.
- HV4 [B] **Overlay timing from `hero.json`.** Chapter windows, the chapter list, the TC and the card shrink window are derived from `public/video/hero.json` ranges, not hard-coded. Verified in code and by checking that a changed JSON moves them.
- HV5 [B] **Overlays kept, per §8.1.** All of these must be present:
  - The wordmark split (letters with their own depth, blur and scale, fanning out from the centre).
  - Mask-in / blur-out headlines with the §7.1 copy verbatim.
  - Crop marks and the TC.
  - The chapter list with its active state.
  - The cursor `scroll` state over the hero.
  - **The ch5 card shrink on the video wrapper to an inset of exactly 4vw and an 18 px radius** (measured on the computed clip/size at the end of the pin; round-1 three.js measured `inset(57.6px round 18px)` at 1440, the bar to keep).
- HV6 [M] Pin length: desktop ≈ 600vh, < 768px ≤ 400vh *(judge proposal, carried from §7.3)*. Scroll distance per video second feels even across shots, with no chapter rushing past.
- HV7 [M] `hero-720.mp4` loads under 768 px wide or with `navigator.connection.saveData`, otherwise `hero-1080.mp4`. Verified in the network panel at 375×812 and at 1440×900.
- HV8 [B] **Reduced motion:** the poster plus stacked chapter blocks (plates + §7.1 headline/body), no scrubbing and no pin. **The video is not downloaded at all.**
- HV9 [B] **First view ≤ 3 MB:** poster + HTML + JS + CSS + fonts. The video fetch starts after first paint (its request `startTime` > FCP). The hero total (with the 1080 video) is ≤ 30 MB.
- HV10 [M] No console errors. Works under the `/imobiliare_landing_page/` sub-path. If the video is missing, it degrades to the poster + overlays with scrolling still working, and no exception.
- HV11 [M] The placeholder video (`assets-src/video/placeholder.mp4`) is never in `public/` or `dist/`. The real files use the same filenames and JSON shape.
- HV12 [m] The three.js modules are deleted, not commented out or left unused. Small modules, comments only on the scrub maths.
- HV13 [B] **§8.4 in the hero.** The hero shows only the Higgsfield video: no code path animates a still (no CSS or JS scale/translate of the poster or of `img/*` plates while scrolling, and no image crossfade sequence). The poster may show static until the video is ready, and reduced motion may show static stills and blocks. Ship gate: when deployed, `hero.json.status !== 'placeholder'` and the mp4 hashes are not the placeholder (V13c). While VIDEO's placeholder is in `public/video/`, HERO-v2 is judged on mechanics only, and this item is checked at integration.

(The rev-2 three.js items H1–H25 are retired. Round-1 notes on the three.js build are kept only as history.)

## SECTIONS (`src/sections/**`, nav, cursor, 8 sections, footer)

- S0 [M] Anchor IDs per §7.2: `#proiectul` (manifesto), `#arhitectura` (gestures), `#rezidente` (apartments), `#locatie`, `#vizionare`. The nav links, the nav CTA and the hero buttons scroll to them through Lenis.

Nav and cursor
- S1 [M] Nav content is exact: `ORIZONT` (Unbounded 800, 14px), mono `BUCUREȘTI / NORD`, links `01 PROIECTUL · 02 ARHITECTURA · 03 APARTAMENTE · 04 LOCAȚIE`, and the gold-soft pill `PROGRAMEAZĂ O VIZITĂ`. It is fixed and transparent over the hero. After the hero it switches to `mix-blend-mode: difference` or a solid ink background, and stays legible over the paper section.
- S2 [M] At 375px the links collapse (hidden or a menu), the pill fits and nothing overlaps the wordmark.
- S3 [M] Cursor ring (`src/sections/cursor.js`, §7.3): ~28 px hairline, follows with lerp, `pointer-events:none`, moves by transform only, and is disabled on `(pointer: coarse)`. It exposes `window.__cursor = { setState(name) }` with the states `default | link | scroll | view`, and each state is visibly distinct (label, dot, filled disc over images).

1 Manifesto
- S4 [B] `id="proiectul"`, label `01 / PROIECTUL`. The §7.2 paragraph (`Orizont adună 46 de apartamente …`) is character-exact with diacritics and the em dashes. Unbounded 600 at ~3.2vw, mixed cream and muted. The word-by-word opacity .15→1 is scrubbed and reverses on scroll-up.
- S5 [M] Stats row: 4 columns with hairline tops: `APARTAMENTE 46 · NIVELURI 24 · LIVRARE 2028 · ÎNĂLȚIME 96 m`. A count-up plus digit scramble settles to the **exact** final value even on a fast scroll-past. The ` m` unit stays stable and the layout does not shift (tabular widths).

2 Marquee
- S6 [M] Exact words `TRAVERTIN ✦ BRONZ ✦ STEJAR AFUMAT ✦ STICLĂ ✦ LUMINĂ ✦`, alternating filled and outlined (stroke), with a seamless infinite loop (no gap or jump at the wrap).
- S7 [M] Speed reacts to Lenis velocity, the direction flips with the scroll direction, and it eases back to base speed when scrolling stops.

3 Trei gesturi
- S8 [B] `id="arhitectura"`, `--paper` background, with a pinned horizontal scroll. The pin length matches the track width, with no vertical jump at the start or end of the pin. Headline `TREI IDEI, <em>un singur turn.</em>`.
- S9 [M] There are 3 cards with the §7.2 titles and texts: `01 PIATRA` (tower-exterior), `02 TERASA` (loggia), `03 INTRAREA` (threshold). Each has a clip-path reveal and inner image parallax, plus a huge outlined numeral (Unbounded with a text stroke).
- S10 [M] At ≤768px it becomes a vertical stack with no pin and no horizontal overflow.

4 Rezidențe
- S11 [M] `id="rezidente"`, headline `ALEGE-ȚI <em>înălțimea.</em>`, note `46 de locuințe, între 112 și 480 m²`. The 3 rows are exactly per §7.2 (`APARTAMENT CU TERASĂ`, `APARTAMENT DE COLȚ`, `PENTHOUSE`), at ~5vw with index `01–03`, their mono spec strings and an arrow.
- S12 [B] Hover: the row goes outlined→filled and the other rows dim to 35%. A 4:5 preview follows the cursor with lerp and swaps per row with a clip reveal, using `res-loggia / res-corner / res-penthouse`.
- S13 [m] Keyboard focus gives an equivalent state. Touch does not depend on hover (static thumbnail or tap).

5 Materiale
- S14 [M] `materials.webp` **inset with side margins** (gutter on each side, slight radius; §7.2), filling ~100vh, with a scrubbed scale 1.15→1. Headline `STEJAR, TRAVERTIN, <em>umbră caldă.</em>` bottom-left, plus the §7.2 body.

6 Locație
- S15 [M] `id="locatie"`, `--slate` background. Headline `LÂNGĂ PARC, <em>aproape de tot.</em>`, the right `location.webp` with parallax, and the address `Șoseaua Nordului 12, București`.
- S16 [M] The distance table has exactly the 4 rows (`Parcul Herăstrău — 3 min pe jos`, `Piața Charles de Gaulle — 6 min`, `Aeroportul Otopeni — 18 min`, `Centrul Vechi — 15 min`) in mono with hairlines, staggered in.

7 Vizionare
- S17 [B] `id="vizionare"`. Headline `HAI SĂ NE <em>vedem acolo.</em>` with the smeared reveal: per-letter or per-line scaleY stretch plus blur settling to crisp, done with CSS/GSAP. The body is exactly as in §7.2.
- S18 [B] Form: a 2-column grid of underline inputs with mono labels: Nume, Email, Telefon, Tip rezidență (a select with exactly `Apartament cu terasă`, `Apartament de colț`, `Penthouse`, `Încă nu știu`), Mesaj, and a submit pill. It collapses to 1 column at 375px.
- S19 [B] Validation without network:
  - Name and email are required.
  - The email format and a phone pattern are checked.
  - Inline Romanian error messages appear, with `aria-invalid` set and focus moved to the first invalid field.
  - A valid submit shows an inline success state.
  - **There are zero network requests on submit** (checked in the Network panel), with `preventDefault` and no navigation.

8 Footer
- S20 [M] Mono nav row plus `ÎNAPOI SUS ↑`, which scrolls to the top through Lenis. The legal line is exactly `Vizualizările sunt generate digital și au rol de prezentare; nu constituie ofertă contractuală.` The giant `ORIZONT` spans the full width, is clipped by the viewport bottom and rises in on scroll.

Global
- S21 [M] Images are lazy-loaded (`loading="lazy"` or an IntersectionObserver). Missing images fall back to a CSS gradient (tested with an image removed from a dist copy).
- S22 [B] `prefers-reduced-motion`: no pins and no scrubs, and **all text ends at full opacity**, not stuck at .15. The marquee is static or slow, and the form still works.
- S23 [M] At 375px: no horizontal overflow on any section, and the type scale is readable (body ≥15px).
- S24 [M] ScrollTrigger refreshes after `document.fonts.ready` and after image loads, so pin positions stay correct.
- S25 [M] Editorial craft matches the reference: CAPS display + italic serif tail on every headline, mono chapter labels above each headline, generous vertical rhythm, hairlines. Nothing looks like a template card grid.

## MEDIA (`public/img/**`, `docs/ASSETS.md`)

- M1 [B] These 13 files exist: `hero-rooftop, skyline-dusk, aerial-city, tower-exterior, loggia, interior-living, threshold, res-loggia, res-corner, res-penthouse, materials, location, og` `.webp`. They are real WebP (RIFF/WEBP magic). Optional `*_depth.webp` and an `og.jpg` fallback are allowed.
- M2 [B] Exact pixel sizes:
  - 2560×1440: hero-rooftop, skyline-dusk, aerial-city, loggia, interior-living, materials.
  - 1600×2000: tower-exterior, threshold, location.
  - 1200×1500: res-*.
  - 1200×630: og.
  - Depth maps have the plate's aspect ratio (half resolution is OK).
- M3 [M] Size caps (adopted in §7.3):
  - 2560×1440 ≤ 500 KB.
  - 1600×2000 ≤ 400 KB.
  - 1200×1500 ≤ 250 KB.
  - og ≤ 150 KB.
  - Depth maps ≤ 150 KB.
  - All of `public/img` ≤ 6 MB.
  - `hero-rooftop` is the only image in the first view (≤ 3 MB total, §7.3).
  - WebP quality ~82.
- M4 [B] No text, lettering, signage, logos or watermarks. No people or faces. **No palm trees.** No AI artefacts: bent verticals, melted furniture, duplicated or impossible windows, garbled reflections, smeared railings, nonsense geometry at 100% zoom.
- M5 [B] Each image fulfils its §4 brief:
  - Rooftop: a parapet and olive trees, with an **empty lower third** for the wordmark.
  - Skyline: an **empty central gap or plot**.
  - Aerial: **no dominant tower in the centre third**.
  - Loggia: open sliding glass and a warm interior.
  - Interior: smoked oak, travertine floor, cream sofa, a blue-hour window.
  - Threshold: a pivot door and a travertine corridor.
  - Corner residence: two-sided glass.
  - Penthouse: double height.
  - Location: the lake or park at blue hour.
- M6 [M] One tower across `tower-exterior`, `location` and `og`, consistent with the 3D model: slender, ~24 storeys, dark bronze glass, a pale travertine seam cutting diagonally on one corner, stacked warm loggias.
- M7 [M] A consistent grade and time-of-day progression (dusk → blue hour). The interiors share one material language.
- M8 [M] Plates work for the camera journey: the loggia and interior have a central vanishing point for the push-in, and the skyline and aerial horizons sit where the hero camera expects them (agreed with HERO).
- M9 [M] Plausibly north Bucharest: mid-rise glass offices, flat terrain, Herăstrău. Not LA, Manhattan, mountains or sea.
- M10 [M] `docs/ASSETS.md` lists every file with path, dimensions, KB, tool/model, prompt, job id and credits. **Total credits ≤ 250.** No reference frame is used as an input.
- M11 [m] No sky banding and no over-sharpening halos. The images hold up at 100%.
- Craft: judged as an art director. Would these pass for a real developer's marketing renders?

## VIDEO (the former MEDIA; Higgsfield edit + merge → `public/video/**`, `docs/ASSETS.md ## VIDEO`; SPEC §8.3.2)

The stills checklist above (M1–M11) still applies to `public/img/**`, which feeds the sections, the reduced-motion blocks and the video references.
- V1 [B] **Deliverables.** The four files below exist, and `ffprobe` confirms the JSON matches the files (`frameCount` = `nb_frames`, duration ±1 frame, 24 fps):
  - `public/video/hero-1080.mp4` (1920×1080)
  - `hero-720.mp4` (1280×720)
  - `hero-poster.webp` (= frame 0)
  - `hero.json` (duration, fps, frameCount, shot and chapter time ranges)
- V2 [B] **Encoding.** All of these, checked with `ffprobe -show_streams -show_frames`:
  - H.264 High, `yuv420p`, 24 fps CFR.
  - `-g 6`: a keyframe every ≤ 6 frames.
  - `-bf 0`: `has_b_frames=0`.
  - `+faststart`: `moov` before `mdat`.
  - **No audio stream.**
- V3 [B] **Size caps:** 1080 ≤ 25 MB, 720 ≤ 10 MB, poster ≤ 300 KB *(judge proposal)*, every file < 100 MB (the GitHub limit).
- V4 [B] **Spatial fidelity to the guide, per shot.** Frame-step side by side with the 3D guide every 6 frames, plus each shot's first, middle and last frame:
  - The camera path, framing, horizon height and the tower's position and scale stay within ~5% of the frame.
  - Geometry is preserved: building count and placement, the parapet line, the loggia opening and the window position.
- V5 [B] **No morphing, popping or design drift.** Frame-stepped every 2 frames at 1080:
  - The tower keeps one design across all shots: the narrow travertine corner band filled with loggias, the mid-height shift, dark bronze glass, and a storey count stable within ±1.
  - Nothing appears or vanishes except by occlusion: cars, trees, buildings and furniture.
  - No wobbling straight lines and no texture crawl.
- V6 [B] **Floors stack physically (S2).** Each floor comes down onto, or rises onto, the one below, bottom→top. No floor materialises in mid-air. The top 2–3 floors show a bare frame before glazing, and the crown comes last. It reads as a construction time-lapse.
- V7 [M] **Consistent grade and sun.**
  - The sun stays low and back-right throughout, with the dusk grade continuous.
  - Across every cut, the mean colour of matching regions differs by ΔE₀₀ < 5.
  - No luma flicker: the frame-to-frame mean-luma change stays < 2% outside intentional motion.
- V8 [B] **Seamless cuts.** The 12-frame crossfades land on spatially matching frames, with no double-exposed misaligned geometry beyond a soft dissolve. There is no step in camera speed or direction at a cut (judged by frame-stepping across each cut).
- V9 [M] **Photoreal and on-brief.** No raw render is visible in any frame: no flat Blender shading, no untextured blockout.
  - S1 matches `hero-rooftop`, S3 has the city and lake behind, S4 matches `loggia`, and S5–S6 match `interior-living`.
  - No text, logos, people, faces, palms or watermarks.
- V10 [B] **Credits.** VIDEO spends ≤ 600 credits, and the account keeps ≥ 50 in reserve.
  - Every job is logged in `docs/ASSETS.md ## VIDEO`: job id, model, mode, inputs, credits, kept or rejected.
  - **The pilot (one shot on 2 models) gets a judge verdict before the bulk spend.**
- V11 [M] Total 30–40 s. The `hero.json` shot/chapter ranges follow the §8.2 order and match the real cut frames (±2 frames).
- V12 [m] A grain or texture pass is consistent across shots, so no single shot reads "cleaner" than its neighbours.
- V13 [B] **§8.4 user rule: no panned or zoomed stills, every second is Higgsfield video.** All three must hold:
  - **(a) Provenance.** Every segment of the merged video (each shot and each 12-frame overlap) traces to a Higgsfield job id in `docs/ASSETS.md ## VIDEO`: job id, model, mode, input guide or reference, output file, and the frame range it occupies in the cut. Any span without a job id fails.
  - **(b) Frame-step parallax test.** Frame-step every shot (every 2 frames, plus 24 frames either side of every cut), looking for zero-parallax pure scale or translate. If foreground and background move together with no relative parallax, no occlusion change and no perspective change of verticals (a 2D transform of one image: Ken Burns, pan, zoom, or a crossfade of stills), the segment is a pan and fails. Crossfades are allowed only between two Higgsfield video clips at the 12-frame overlaps.
  - **(c) The placeholder never ships.** `hero.json` has no `"status": "placeholder"`. The shipped mp4s differ from `assets-src/video/placeholder.mp4` (hash), and no mp4 that is a stitch of the plates is in `public/`, `dist/`, `gh-pages` or git history. Fallback shots are also Higgsfield generations (first/last-frame image-to-video, omni-reference, extension), never an animated still.
- Craft: judged as a film. Does it feel like one unbroken camera move through one real place at dusk?


## 3D (production model, now `blender/export/*.glb` per §8.1; `blender/**`)
Since §8 the GLB is no longer shipped to the site. It feeds the guides, so T2 and T10 budgets are advisory; the T3–T6 naming, pivot and material contract still applies because the guides animate it.

Checked with `python3 -I docs/reviews/tools/glb_inspect.py public/models/tower.glb`, a three r170 load in the page, and the renders.
- T1 [B] `tower.glb` is valid glTF 2.0 binary and loads in three r170 GLTFLoader without errors, with the decoder config documented.
- T2 [B] `tower.glb` ≤ **3 MB** (§7.3): uncompressed if it fits, otherwise Draco with the decoder shipped at `public/draco/`. `city.glb` ≤ 1.5 MB.
- T3 [B] Nodes per §7.3: `Floor_00…Floor_23` (exactly 24, zero-padded, separate nodes, index increasing with height). **Each `Floor_XX` has a child `Seam_XX`** (and `Loggia_XX` where present), so they rise with their floor. There is **no single full-height `Seam` node**. Plus `Crown` and `Podium`.
- T4 [B] Each `Floor_XX` holds the complete storey (slab + glass band + frames + its seam piece), so animating it moves the whole storey. **Its origin is at that storey's base on the tower's vertical axis (x=0, z=0)** (§7.3). Check that the pivot printed by `glb_inspect.py` is `[0, base_y, 0]`.
- T5 [B] Metres, Y-up, origin at the base centre: bbox min.y ≈ 0 (±0.5), height 90–100 m, footprint ≈28×20 m (±20%), X/Z centre within 1 m of the origin.
- T6 [B] Materials `M_Glass` (dark bronze, metalness ≈.6, roughness ≈.15), `M_Stone` (warm pale, roughness ≈.8), `M_WindowGlow` (warm emissive >0; `KHR_materials_emissive_strength` is OK), `M_Frame` (dark bronze metal).
- T7 [M] ≤150k triangles *(judge proposal)*. No hidden or internal junk, no flipped normals, no z-fighting where the seam meets the glass.
- T8 [M] The design reads at both distances: the silhouette in the skyline, and enough seam and loggia detail (recess depth, slab edges, frames, glow backs) for the chapter 2 close-up.
- T9 [M] The per-floor seam pieces line up into one continuous diagonal seam: no gaps, steps or z-fighting between `Seam_XX` and `Seam_XX+1` in a close render.
- T10 [m] Embedded textures ≤2048 px and compressed. Optional `city.glb` in the same coordinate frame.
- T11 [M] `blender/` has the .blend and a reproducible export script. `blender/renders/*.png` shows the tower at dusk. `docs/ASSETS.md` has an entry (size, tris, tool, compression).
- Craft: proportions, the elegance of the seam gesture, material response under the hero lighting, and how the dusk renders look.

## 3D-GUIDES (motion guides for VIDEO, `blender/guides/**`, `blender/build_guides.py`; SPEC §8.3.1)

- D1 [B] **Deliverables and reproducibility.** These exist:
  - `blender/build_guides.py`.
  - One MP4 per shot S1–S6 at 1280×720, 24 fps.
  - First- and last-frame PNGs per shot.
  - `guides.json` (shot → frame range, camera notes).

  A headless re-run gives the same `guides.json`, the same frame counts and visually identical MP4s (per-frame PSNR ≥ 45 dB against the originals). The judge backs up the files and restores them afterwards.
- D2 [B] **One continuous camera.** A single camera animation spans S1–S6.
  - At each cut, the 12 overlap frames at the end of shot N and the start of shot N+1 are the same camera path and the same render (PSNR ≥ 40 dB frame-for-frame).
  - Camera position and speed are continuous: no teleport, and no frame-to-frame speed change > 25% outside deliberate eases (from an exported camera track, or `guides.json` notes plus frame-stepping).
  - Focal length 18–50 mm, with no FOV jump at a cut.
- D3 [B] **Real scale, physically plausible.**
  - Rooftop eye height ≈ 1.6 m, parapet ≈ 1.1 m.
  - Storey 3.6 m, tower 92–99 m, footprint ≈ 28×20 m.
  - Loggia ≈ 5 m wide × 3.6 m deep × ~3 m clear. Living-room ceiling ≈ 3 m. Door/glass height 2.4–2.7 m.
  - City blocks at believable sizes.
  - The camera never passes through solid geometry; the only threshold crossed is the open sliding door.
- D4 [B] **The stacking reads.** In S2 the storeys arrive bottom→top. Each lands onto the one below (contact; no mid-air pop) and gets ≥ 6 frames of visible motion, so a video model can follow it.
  - The top 2–3 rising floors show a bare frame and get their glass as the next floor appears; the crown comes last.
  - Each `Seam_XX` and `Loggia_XX` travels with its floor.
  - At least 24 distinct steps are visible when frame-stepping.
- D5 [M] **Canonical tower.** It matches `tower-exterior.webp` and the round-2 GLB: a narrow travertine corner band filled with loggias, the mid-height shift, dark bronze glass, and a lit-window pattern that reads as homes rather than a barcode.
- D6 [M] **Environment matches the plates.**
  - S1: the rooftop matches `hero-rooftop` (parapet line, olive planters, the view over trees).
  - S2: the plot and flanking offices like `skyline-dusk`.
  - S3: a lake behind like `aerial-city` / `location`.
  - S4: the loggia blockout has `loggia.webp` proportions (symmetric, sliding glass, glass balustrade).
  - S5–S6: the living room has the `interior-living.webp` layout (sofa left of centre, window right, joinery wall).
  - Throughout: a dusk world, the sun low back-right, readable shading (not flat grey), lit windows and practicals.
- D7 [M] Shot lengths are within ±30% of §8.2, with a 30–40 s total at exactly 24 fps. Each MP4's frame count equals `guides.json`.
- D8 [M] **Legible for video models.** Clear silhouettes and value separation, no z-fighting, flicker or aliasing shimmer when frame-stepped, motion blur either off or consistent.
- D9 [m] Guides and their PNGs never land in `public/` or `dist/`. GLBs live in `blender/export/` (§8.1).

## RELEASE (repo, Pages, README, deploy)

- R1 [B] The GitHub repo exists and is **public** (`gh repo view --json visibility,url,defaultBranchRef`).
- R2 [B] `reference/` has **never** been committed, on any ref, locally or on the remote:
  - `git log --all --stat -- reference` is empty.
  - `git rev-list --all --objects | grep -i reference/` is empty.
  - No `source.mp4` blob exists.
  - The remote branch trees (through `gh api …/git/trees/<sha>?recursive=1`) have no `reference/`.
- R3 [B] The Pages URL returns 200, and every asset referenced by the live `index.html` and its JS/CSS (assets, img, models, fonts) returns 200 under the sub-path. The live site renders in Chrome without console errors.
- R4 [B] `gh-pages` holds the built `dist` plus `.nojekyll`. No secrets are in any branch (`.env`, tokens, `.claude/settings.local.json`).
- R5 [M] The deploy script is sub-path safe (base `./` or `/imobiliare_landing_page/`) and builds from committed state (a clean worktree or tree). It is idempotent, fails loudly (`set -euo pipefail`), never force-pushes `main`, and does not touch the user's working tree or stash.
- R6 [M] The live build matches the reviewed commit (hashed asset names in the live HTML equal a local build of that commit). The deploy records which commit it shipped.
- R7 [M] README is accurate: what the project is, the live URL, the stack, `npm i / dev / build / deploy`, structure and ownership, and a note that the assets are AI-generated. It claims nothing that is not built, and has no reference-brand mentions.
- R8 [M] Hygiene:
  - `.gitignore` covers node_modules, dist (on main), .DS_Store, reference/, *.blend1 and .claude/settings.local.json.
  - No `.DS_Store` is committed.
  - No file is >50 MB, and none is >100 MB (the hard limit).
  - Large binaries (.blend) are a conscious decision.
- R9 [m] The deployed HTML has an absolute `og:image` URL and a favicon, so there is no 404 in the console. The repo description and homepage URL are set.
- R10 [B] §8 build: `three` removed from package.json and the lockfile (with the lead's approval). `public/models/` and `public/draco/` are absent from `dist/` and from `gh-pages`. `public/video/*` deploys, returns 200 on Pages with `content-type: video/mp4` / `image/webp` / `application/json`, and serves byte ranges. Every committed file is < 100 MB, and nothing > 50 MB lands without a DECISIONS line.
- R11 [M] `assets-src/` (raw Higgsfield outputs, the placeholder video) stays ignored. Guide MP4s are committed only if small (≤ 50 MB total) or kept out, and they are never deployed.

## Integration (lead-owned; checked when everything is merged)

- I1 [B] One continuous page: hero → card → manifesto with no gap, jump or double scrollbar, and Lenis drives everything.
- I2 [M] Pins stack correctly (hero, then gestures) in both scroll directions and after a resize.
- I3 [M] Whole-page 375px pass and whole-page reduced-motion pass.
- I4 [M] Live Pages site: first view (poster + HTML + JS + CSS + fonts) ≤ 3 MB, the video streamed after first paint, no console errors, and the scrub is smooth on the live URL (HV3 repeated against Pages).

## How the judge measures (repeatable)

- FPS: `javascript_tool` installs a rAF delta sampler, scripts `__lenis.scrollTo(y, {duration})` through the hero, and reports the median and p95.
- Transfer: `performance.getEntriesByType('resource').reduce((s,e)=>s+(e.transferSize||e.encodedBodySize),0)` before the first scroll.
- Overflow: `document.documentElement.scrollWidth - innerWidth` at 375px, sampled at each section.
- Pins: `ScrollTrigger.getAll().map(t=>[t.trigger?.id||t.trigger?.className, t.start, t.end, !!t.pin])` (exposed through `window.ScrollTrigger` or module devtools).
- Sub-path and fallbacks: a scratch copy of `dist/` served from `/imobiliare_landing_page/`, with `tower.glb` or an image deleted **in the copy only**.
- Images: `sips -g pixelWidth -g pixelHeight`, `file`, `ls -l`, then Read each image at full size and judge it as an art director.
- Video files: `ffprobe -v error -show_streams -show_format -of json hero-1080.mp4` (codec/profile/pix_fmt/fps/nb_frames/has_b_frames/audio). Keyframe spacing: `ffprobe -select_streams v -show_frames -show_entries frame=key_frame,pkt_pts_time -of csv`. Faststart: `moov` atom offset < `mdat`.
- Spatial fidelity: guide and video frame-stepped side by side (`ffmpeg -vf "select=not(mod(n\,6)),scale=640:-2,tile=6x4"` on both, same frame numbers). Cut checks: 24 frames either side of every cut tiled, plus ΔE₀₀ of matching regions.
- Guide reproducibility: back up `blender/guides/`, re-run `Blender -b -P blender/build_guides.py`, compare `guides.json` and per-frame PSNR (`ffmpeg -lavfi psnr`), then restore the originals byte for byte.
- Scrub smoothness: CDP headless Chrome with `--use-angle=metal` (it reported `ANGLE Metal Renderer: Apple M4 Pro` in round 1), a `requestVideoFrameCallback` counter plus rAF deltas during `__lenis.scrollTo` forward and back over 10 s, and `video.currentTime` against the target at rest.
