# Asset manifest

## MEDIA

All images generated with Higgsfield, 21 Nov 2026 (round 1 + round 2 fixes after the judge's review). Originals (PNG, full
resolution, plus rejected candidates) are in `assets-src/` (gitignored, not deployed; round-2 sources are prefixed `r2_`).
Finals were centre-cropped/resized with ffmpeg (lanczos) and encoded with `cwebp -q 82 -m 6 -metadata none`. Every file is
within the SPEC §7.3 caps (2560×1440 ≤ 500 KB, 1600×2000 ≤ 400 KB, 1200×1500 ≤ 250 KB, og ≤ 150 KB, `public/img` ≤ 6 MB;
total now ≈ 3.7 MB). No text, logos, faces or palm trees in any image.

**Credits: 100.5 total** = round 1: 65.0 (balance 756.06 → 691.06) + round 2: 35.5 (691.06 → 655.56).
Models: `gpt_image_2_6` (GPT Image 2.6, quality high, 4k; 2k for og) — 13 jobs in round 1 (12 finals + 1 rejected) and
6 in round 2 (5 finals + 1 rejected); `nano_banana_pro` (4k) — 4 candidates in round 1 (1 used), 3 in round 2 (the skyline
edit used, 2 rejected); `nano_banana_2` (2k) — 6 depth maps (4 in round 1, 2 in round 2).

Consistency: `tower-exterior` was generated first and passed as an image reference to `location`, `loggia` and `og`;
`interior-living` was the reference for `materials`, `threshold` and `res-*`; round 2 used `skyline-dusk` as the grade
reference for the new `hero-rooftop` and `aerial-city`.

### Finals in `public/img/`

| file | px | KB | model | job id | credits | source file |
|---|---|---|---|---|---|---|
| `hero-rooftop.webp` (r2) | 2560×1440 | 340 | gpt_image_2_6 4k high, refs = old rooftop + skyline | b85a9daf-d02f-4756-9ed7-42ab527c2f08 | 3.25 | r2_hero-rooftop_gpt.png |
| `skyline-dusk.webp` (r2) | 2560×1440 | 224 | nano_banana_pro 4k (round 1 plate) + nano_banana_pro 4k edit composited into x 37.5–62.5 %, y ≥ 53 % | 40584312-3cb6-4624-b2be-35493aa01820 + 2b9a9211-4dfb-42ba-8439-9754844c0448 | 4 + 4 | skyline-dusk_r2_composite.png |
| `aerial-city.webp` (r2) | 2560×1440 | 307 | gpt_image_2_6 4k high, ref = skyline (grade only) | 5a697cec-1593-4cd7-a078-56337dc84ca1 | 3.25 | r2_aerial-city_gpt.png |
| `tower-exterior.webp` | 1600×2000 | 321 | gpt_image_2_6 4k high | c36cb2fc-b0f5-4e55-a435-a14da17777f5 | 3.25 | tower-exterior_gpt.png |
| `loggia.webp` | 2560×1440 | 414 | gpt_image_2_6 4k high, ref = tower | 8d1f4168-5c4a-4017-b802-158f743e527f | 3.25 | loggia_gpt.png |
| `interior-living.webp` | 2560×1440 | 310 | gpt_image_2_6 4k high | adb38c91-ae32-4722-ab8a-fc8d46277bed | 3.25 | interior-living_gpt.png |
| `threshold.webp` | 1600×2000 | 206 | gpt_image_2_6 4k high, ref = interior | 4baabbe0-4335-4306-9fc8-a35bfb26e8a4 | 3.25 | threshold_gpt.png |
| `res-loggia.webp` (r2) | 1200×1500 | 178 | gpt_image_2_6 4k high, ref = interior (palette only) | f83c73d7-05a6-4038-8cd0-e15b1ce895dd | 3.25 | r2_res-loggia_gpt.png |
| `res-corner.webp` (r2) | 1200×1500 | 128 | gpt_image_2_6 4k high, ref = interior (palette only) | cfd05090-aff1-4b3f-a993-eceed5928112 | 3.25 | r2_res-corner_gpt.png |
| `res-penthouse.webp` (r2) | 1200×1500 | 164 | gpt_image_2_6 4k high, ref = interior (palette only) | dad9cc6a-baff-42d5-bf47-ffd2cc2566a6 | 3.25 | r2_res-penthouse_gpt.png |
| `materials.webp` | 2560×1440 | 209 | gpt_image_2_6 4k high, ref = interior | c1a173f4-af92-45bf-97e9-f2cdada175c2 | 3.25 | materials_gpt.png |
| `location.webp` | 1600×2000 | 312 | gpt_image_2_6 4k high, ref = tower | c63d6736-6bea-4426-af5d-799f34d1c33b | 3.25 | location_gpt.png |
| `og.webp` | 1200×630 | 64 | gpt_image_2_6 2k high, ref = tower | 9d5b1fc6-0ed6-42fe-b8f5-b4ac998b7bfc | 2 | og_gpt.png |
| `og.jpg` | 1200×630 | 147 | same image, JPEG (q≈90) for crawlers that ignore webp | – | 0 | og_gpt.png |
| `hero-rooftop_depth.webp` (r2) | 1280×720 | 10 | nano_banana_2 2k, ref = new rooftop, hand-corrected | 061ede25-c57f-4e39-8245-83b887099380 | 2 | r2_hero-rooftop_depth_nb2.png |
| `skyline-dusk_depth.webp` (r2) | 1280×720 | 7 | round-1 map + centre from a new map of the edited plate, level-matched | 0002cfe9-4772-4957-a9d6-e772fea7189f + 95d94ab2-6439-48e9-b505-3d63f591b117 | 2 + 2 | skyline-dusk_depth_nb2.png + r2_skyline-dusk_depth_nb2.png |
| `loggia_depth.webp` (r2 fix, no credits) | 1280×720 | 7 | nano_banana_2 2k, ref = loggia; edge strips repainted near | b4ec7ebd-cfde-4806-a840-5c2f77adb197 | 2 | loggia_depth_nb2.png |
| `interior-living_depth.webp` | 1280×720 | 7 | nano_banana_2 2k, ref = interior-living | ea3e6720-3d61-44fe-b8b1-79115904fe02 | 2 | interior-living_depth_nb2.png |

### Replaced / rejected (kept in `assets-src/`, credits counted in the total)

| candidate | model | job id | credits | why not used |
|---|---|---|---|---|
| tower-exterior_nbp.png (r1) | nano_banana_pro 4k | b9bc183c-e06d-4f53-86ab-51d4cac2ff86 | 4 | Crops the tower top and bottom; the hero needs the whole silhouette. |
| hero-rooftop_nbp.png (r1) | nano_banana_pro 4k | 47d71554-bcd2-40ea-b32f-6b51e026215a | 4 | Busy planters on the right. |
| skyline-dusk_gpt.png (r1) | gpt_image_2_6 4k | c8dc3ba9-5f33-40ea-905c-756976c1c91e | 3.25 | NBP version had the clearer plot. |
| interior-living_nbp.png (r1) | nano_banana_pro 4k | 38989f9a-289a-4e0a-b3b5-fd77a22e2e1f | 4 | Floor reads as wood. |
| hero-rooftop_gpt.png (r1 final, replaced in r2) | gpt_image_2_6 4k | c2d00ecc-c58f-4e74-9e83-5191a12b2331 | 3.25 | Judge: saturated HDR, spring blossom, sun left, wordmark zone 2.4:1. |
| aerial-city_gpt.png (r1 final, replaced in r2) | gpt_image_2_6 4k | 7f677bbd-1db3-4d8b-85be-67ab1eb288ea | 3.25 | Judge: Paris/Vienna look, 400 m altitude, horizon at 25 %, 521 KB. |
| res-loggia/corner/penthouse_gpt.png (r1, replaced in r2) | gpt_image_2_6 4k | 1bac7f03-…, ab2a67e2-…, 34c50d6d-… | 9.75 | Judge: same sofa/throw/bowl repeated in all three. |
| hero-rooftop_depth_nb2.png (r1, replaced) | nano_banana_2 2k | 84927865-7df1-4ba5-81c8-7df1a73655a0 | 2 | Plate replaced. |
| r2_skyline-edit_gpt.png | gpt_image_2_6 4k | 7a7a9fcd-af98-49d8-9ec3-03c23460f588 | 3.25 | Removed the tree but re-rendered the whole frame; NBP edit kept the geometry. |
| r2_aerial-city_nbp.png | nano_banana_pro 4k | 0483ba64-59b9-411e-87e3-162a166a171d | 4 | Horizon at ≈41 %, below the 45–55 % target. |
| r2_hero-rooftop_nbp.png | nano_banana_pro 4k | cb7ee89d-f988-46e6-b062-fe495a29320e | 4 | Wordmark zone only 3.56:1 (worst 2.65) and some blossom left. |

### Depth maps

No Higgsfield app does depth estimation (`apps_search "depth"` is empty) and there is no local torch. The maps were made
by asking `nano_banana_2` to redraw each plate as a pixel-aligned grayscale depth map (white = near), checked against the
plate edges, then blurred (σ≈2.5 at 1280 px) to remove texture. `hero-rooftop_depth` is corrected by hand with an ffmpeg
`geq` pass (the model puts the floor behind the parapet): the floor below y 66.4 % is a near→far ramp and the side olive
trees/shrubs are lifted in front of the parapet. `loggia_depth`: the facade strips at x < 10.7 % and x > 92.1 % are painted
near (205) so the frame edges do not swim. `skyline-dusk_depth`: the poplar is gone (centre merged from a map of the
edited plate, level-matched to the old map). They are relative, approximate maps: fine for a few-percent parallax only.

### Prompts (round 1; the round-1 hero-rooftop, aerial-city and res-* prompts are superseded below)

- **tower-exterior**: Award-winning architectural photography of a slender 24-storey luxury residential tower at blue hour dusk in north Bucharest, Romania. The tower facade is a dark bronze-tinted glass curtain wall with fine dark bronze mullions. One corner of the tower is cut by a single full-height vertical seam of pale warm travertine stone that runs from the ground to the roof with a slight diagonal shift halfway up; deep loggias are carved into this stone seam, stacked floor above floor, each glowing warm golden from interior lamps. Shot from a low three-quarter angle, 35mm lens, tilt-shift corrected verticals, tower fills the frame vertically. Behind and below: a hazy low-rise European city with mature deciduous trees (lindens, chestnuts), soft lights coming on, warm amber glow on the horizon fading to deep blue sky. Calm, cinematic, quiet luxury, subtle film grain, Hasselblad medium format quality. No people, no text, no signage, no logos, no palm trees.
- **hero-rooftop**: Photoreal architectural photography, eye level, 24mm wide lens: an empty rooftop terrace of a residential building in north Bucharest at dusk. Pale travertine floor tiles, a low pale stone parapet running across the middle of the frame, a few large terracotta and dark bronze planters with potted olive trees at the sides. Beyond the parapet: a distant low skyline of Bucharest mid-rise blocks and dense mature deciduous tree canopies (lindens, chestnuts, plane trees), soft city lights starting to glow. Warm sunset sky with a golden-amber horizon fading up to dusty pink and soft blue, a few thin clouds. The lower third of the frame is a calm, uncluttered, evenly lit expanse of travertine terrace floor, empty, for a large title overlay. Calm, cinematic, quiet luxury, natural colour grading, subtle film grain. No people, no text, no signage, no logos, no palm trees.
- **skyline-dusk**: Photoreal architectural photography of the north Bucharest business district skyline at golden hour, seen from mid-height (about 10th floor) across the city, 50mm lens, straight horizon. Several mid-rise modern glass office towers of different heights (12 to 25 storeys) catching warm golden sunlight on their facades, arranged to the left and right of the frame. Exactly in the centre of the frame there is a clear empty gap: an open vacant building plot with flat ground and nothing tall standing on it, open sky above it, so the centre third of the image has no buildings rising above the tree line. Dense mature deciduous trees and low roofs fill the bottom of the frame. Hazy warm amber sky, soft atmospheric haze, sun low out of frame. Calm, cinematic, natural colour, subtle film grain. No people, no text, no signage, no logos, no palm trees.
- **interior-living**: Photoreal interior architectural photography, eye level, 24mm: a luxury apartment living room at blue hour. One wall is dark smoked oak joinery floor to ceiling with open shelves holding a few books and ceramics, lit by warm indirect LED strips. Pale travertine stone floor. A low, long cream boucle sofa, a thick solid smoked oak coffee table, a dark leather lounge chair, a linen floor lamp glowing warm. Warm indirect cove lighting along the ceiling edge. A big floor-to-ceiling window on the right shows the deep blue dusk city with tiny warm lights far below. Contrast of warm golden interior light against cool blue window light. Calm, cinematic, quiet luxury, minimal styling, natural colour grading, subtle film grain. No people, no text, no artwork with text, no logos, no plants that look tropical.
- **aerial-city**: Photoreal high aerial photograph over a large European city at dusk, seen from about 400 metres up, looking toward the horizon at a shallow oblique angle. Endless low-rise and mid-rise city blocks with terracotta and grey roofs, wide tree-lined boulevards with warm streetlights just switching on, several large green parks and a calm lake, dense deciduous tree canopies, all receding into warm golden-amber atmospheric haze at the horizon under a soft dusk sky fading from amber to dusty blue. The centre third of the frame contains only low buildings and trees, with no tall tower or dominant landmark in the middle. Calm, cinematic, natural colour grading, subtle film grain. No people, no text, no logos, no palm trees.
- **location** (ref: tower): Use the reference image only to define the building: the exact same slender residential tower with a dark bronze glass curtain wall and the full-height pale travertine seam with stacked warm-lit loggias and the diagonal shift. New photograph: the tower seen from a distance at blue hour across Herastrau park lake in north Bucharest. The calm lake fills the lower part of the frame with soft reflections of the tower's warm loggia lights and the deep blue sky; mature deciduous trees of the park line the shore; the low-rise city and a few distant mid-rise blocks spread on either side, the tower clearly the tallest and standing alone, placed slightly right of centre. Deep blue sky with a faint warm glow at the horizon. 85mm lens compression, photoreal architectural photography, calm and cinematic, subtle film grain. No people, no boats with text, no text, no signage, no logos, no palm trees.
- **loggia** (ref: tower): Use the reference image only to define the architecture and materials: pale warm travertine stone seam, dark bronze glass and dark bronze frames, warm interior light. New photograph, close and frontal: looking straight into ONE deep loggia carved into the pale travertine seam of the tower, seen from the air just outside it at dusk, symmetrical one-point perspective. The loggia is a deep stone-framed outdoor room: travertine floor, travertine ceiling with a few small warm downlights, thick travertine side walls. At the back, floor-to-ceiling sliding glass doors with thin dark bronze frames, one panel slid fully open, revealing a warm-lit living room beyond: cream sofa, smoked oak coffee table, a glowing linen floor lamp, dark oak joinery. The glass panels faintly reflect the blue-hour city. At the far left and right edges a sliver of the dark bronze glass facade; far below on one side, a hint of the hazy dusk city. A low frameless glass balustrade at the front edge. Photoreal architectural photography, 24mm, calm, cinematic, warm golden interior against cool blue dusk, subtle film grain. No people, no text, no logos, no palm trees.
- **og** (ref: tower): Use the reference image to define the building: the exact same slender tower with dark bronze glass and a full-height pale travertine seam with stacked warm-lit loggias and a diagonal shift. New wide cinematic photograph for a social preview card: the tower stands on the right third of the frame at blue hour, seen from a moderate distance above the tree canopies of north Bucharest, deep blue to warm amber sky gradient, low-rise city lights glowing below. The left two thirds of the frame are calm open dusk sky and soft treetops, uncluttered. Photoreal architectural photography, 50mm, calm and cinematic, subtle film grain. No people, no text, no signage, no logos, no palm trees.
- **materials** (ref: interior): Same material language and lighting as the reference interior: dark smoked oak joinery, pale travertine stone, warm indirect light. New photograph: a moody, intimate, closer interior detail view. A corner where a floor-to-ceiling dark smoked oak wall with a recessed horizontal shelf meets a thick pale travertine wall and a solid travertine bench; warm hidden LED light grazing down the oak grain and across the stone; a single ceramic vessel and a folded linen throw; deep soft shadows, low key, a sliver of a blue-hour window at the far edge. Composition with calm darker negative space in the lower left third. Photoreal interior architectural photography, 35mm, calm, cinematic, quiet luxury, subtle film grain. No people, no text, no logos.
- **threshold** (ref: interior): Same material language and lighting as the reference interior: dark smoked oak, pale travertine, warm indirect light, cream furniture. New photograph: the entrance threshold of the apartment. In the foreground a tall full-height dark smoked oak pivot door stands open, rotated on its pivot, at one side of the frame. Through it, a calm pale travertine corridor with travertine floor and walls and a warm cove light along the ceiling, one-point perspective, leading to the warm-lit living room at the far end with a cream sofa, a glowing linen floor lamp and a big window showing the blue-hour city. Photoreal interior architectural photography, 28mm, eye level, verticals corrected, calm, cinematic, subtle film grain. No people, no text, no logos.
- **res-loggia** (ref: interior): Same material language and lighting as the reference interior: dark smoked oak, pale travertine floor, warm indirect cove light, cream upholstery. New photograph of a different residence: a living room that opens fully onto its deep loggia. Wide floor-to-ceiling sliding glass doors with thin dark bronze frames are slid open; the pale travertine floor continues outside onto the loggia framed by thick travertine walls, with two low outdoor lounge chairs; beyond, the blue-hour city. Inside, a low cream sofa and a smoked oak side table, a warm glowing lamp. Photoreal interior architectural photography, 28mm, calm, cinematic, quiet luxury, subtle film grain. No people, no text, no logos, no palm trees.
- **res-corner** (ref: interior): Same material language and lighting as the reference interior: dark smoked oak, pale travertine floor, warm indirect light, cream furniture. New photograph of a different residence: a corner living and dining room with a frameless two-sided glass corner, floor-to-ceiling glass on two adjacent walls meeting at a slender dark bronze corner, wrapping a wide panoramic view of the dusk city and tree canopies of north Bucharest. A round smoked oak dining table with dark chairs near the glass corner, a cream lounge chair, a low travertine plinth, a smoked oak joinery wall on the opposite side glowing with warm hidden light. Photoreal interior architectural photography, 24mm, calm, cinematic, quiet luxury, subtle film grain. No people, no text, no logos, no palm trees.
- **res-penthouse** (ref: interior): Same material language and lighting as the reference interior: dark smoked oak, pale travertine, warm indirect light, cream furniture. New photograph of a different residence: a penthouse double-height living room, about seven metres tall, with a two-storey wall of floor-to-ceiling glass looking out over the whole blue-hour city of Bucharest to the horizon. A smoked oak mezzanine gallery with a thin bronze balustrade runs along one side, a tall pale travertine fireplace wall rises the full double height, a long cream sofa and a smoked oak coffee table sit low on the travertine floor, warm cove light lines the ceiling. Photoreal interior architectural photography, 20mm, verticals corrected, calm, cinematic, quiet luxury, subtle film grain. No people, no text, no logos, no palm trees.
- **depth maps** (each with its plate as reference): Convert this exact photograph into a monocular depth map with identical framing, identical composition and pixel-aligned edges. Smooth grayscale only: nearest surfaces pure white, farthest surfaces (sky) pure black, smooth continuous gradients along the floor/ground/walls, crisp object silhouettes matching the photo exactly. No colour, no texture, no shading, no text.

## 3D

Built procedurally by `blender/build_tower.py` in Blender 5.2.1, run headless (the Higgsfield bridge's Blender was not
connected). No Higgsfield generations and **0 credits**. Updated 21 Nov 2026 (Round 2).

The exported GLBs and textures are byte-identical between runs (sha256 checked). The renders differ only by EEVEE noise, and the `.blend` only by save metadata.

| file | size | tris | content | compression |
|---|---|---|---|---|
| `public/models/tower.glb` | 1.80 MB | 24,774 | ORIZONT tower: `Tower` › `Podium`(+`Seam_Podium`), `Floor_00…23`(each + `Glass_XX`, `Seam_XX`, `Loggia_XX`), `Crown`(+`Seam_Crown`). Materials `M_Glass` (+clearcoat), `M_Stone`, `M_WindowGlow` (emissive room atlas), `M_Frame`. Height: 96.0 m parapet / seam cap | none (no Draco, no meshopt); two embedded JPEGs |
| `public/models/city.glb` | 0.10 MB | 1,454 | `Ground` (1400 m square) + `City_Blocks` (110 lots, 7–75 m tall, 70 m clear plot round the tower, low-rise front approach), material `M_City` | none |
| `blender/textures/travertine.jpg` | 44 KB | – | 512² tileable travertine (FFT-filtered numpy noise: veining, pores, broad tone drift), the `M_Stone` base colour at 1.5 m per repeat | JPEG q88 |
| `blender/textures/room_atlas.jpg` | 21 KB | – | 256×512 emissive atlas of 8 room cards (2700–3300 K, 0.1–1.0 intensity, cove band, curtain/furniture silhouettes), the `M_WindowGlow` emissive texture | JPEG q85 |
| `blender/orizont_tower.blend` | ~0.3 MB | – | saved scene (tower + city + render rig with cameras/lights, which are not exported) | Blender compressed |
| `blender/renders/tower_34.png` | 1600×2000 | – | full tower, 3/4 view at dusk (EEVEE) | PNG |
| `blender/renders/seam_closeup.png` | 1600×2000 | – | the seam band, mid-height step, loggia stack | PNG |
| `blender/renders/loggia_closeup.png` | 1600×1000 | – | loggias close up | PNG |
| `blender/renders/ch1_skyline.png` | 1600×1000 | – | hero ch1 position (~250 m out, mid-height) | PNG |
| `blender/renders/ch2_seam.png` | 1600×1000 | – | hero ch2 position (close 3/4 on the seam) | PNG |
| `blender/renders/construction.png` | 1600×1000 | – | top 3 storeys with glass hidden (construction look) | PNG |

## VIDEO

Team VIDEO (former MEDIA), SPEC §8. Budget: up to 600 credits, keeping ≥ 50 in reserve. Balance at the start of VIDEO: **655.56**.
Every job is logged below with its credits and the running balance.

### Placeholder (local only, not published)
`assets-src/video/placeholder.mp4`: 1280×720, 24 fps, 816 frames (34.0 s), H.264 High CRF 27, `-g 6 -bf 0`, faststart, no audio, 9.7 MB.
Built by `tools/video/placeholder.sh`. Eased zoompan per plate (S1 hero-rooftop, S2 skyline-dusk, S3 location, S4 loggia, S5/S6 interior-living) with 12-frame fades at
5.0 / 12.0 / 19.0 / 24.0 / 29.0 s. `public/video/hero.json` is the matching draft (`"status": "placeholder"`). No credits.

### Model constraints (models_explore get, 21 Nov)
| model | mode | inputs | notes |
|---|---|---|---|
| `kling_video_edit` (Kling 3.0 Omni Edit) | std / pro / 4k | exactly 1 `video_references` + ≤ 4 `image_references` | Output length follows the source. |
| `seedance_2_5` | `video_edit` | 1 `video_references` + `image_references` (≤ 30) | Billed by the source duration; set `generate_audio: false`. 480p/720p/1080p/4k. |
| `gemini_omni_flash_1_2` | `edit` | exactly 1 source video (3–15 s) + ≤ 7 `image_references` | 360p–4k; native audio (to be stripped). Can't be quoted without an uploaded source. |
| `seedance_2_5` | `omni_reference` (fallback) | `start_image` / `end_image` + refs | 4–30 s. |
| `minimax_h3` (fallback) | – | `start_image` / `end_image` + ≤ 9 refs | 2K only, 4–15 s. |
| `flux_3_video` (fallback) | – | `start_image` / `end_image` + ordered intermediate frames | 5–20 s, 720p–4k. |

### Cost estimates (estimate_video_cost, per clip)
| model / setting | 5 s | 7 s | per s |
|---|---|---|---|
| kling_video_edit std | – | 10.5 | 1.5 |
| kling_video_edit pro | 10 | 14 | 2 |
| kling_video_edit 4k | – | 42 | 6 |
| seedance_2_5 video_edit 720p | – | 53 | ≈7.6 |
| seedance_2_5 video_edit 1080p | – | 140 | 20 |
| seedance_2_5 omni_reference 720p / 1080p | – | 49 / 112 | 7 / 16 |
| minimax_h3 2K | – | 14 | 2 |
| flux_3_video 1080p | – | 56 | 8 |

### Plan (34 s of guide footage: S1 5 + S2 7 + S3 7 + S4 5 + S5 5 + S6 5, plus overlaps)
- **Pilot S2 (7 s):** kling pro (14) vs seedance video_edit 720p (53) ≈ **67**. If both fail spatially, run the fallback on S2: two keyframe image edits (≈7) plus a first/last-frame i2v (14–56).
- **If Kling pro wins:** all 6 shots ≈ 2 cr/s × ~36 s ≈ **72** per pass. Budget for 2–3 takes on the hard shots (S2 stack, S3 orbit), or re-run the winners in `4k` mode (6 cr/s ≈ 216) for the 1080p master.
- **If Seedance wins:** 720p ≈ 7.6 cr/s × 36 s ≈ **275** per pass (1080p ≈ 720 is unaffordable). That leaves room for about one re-take of S2/S3 and an upscale.
- Hard ceiling: stop spending at a balance of ≈ 105 (600 spent + 50 reserve).

### Per-shot prompts and references
Common tail on every prompt: *"Preserve the exact camera motion, geometry, layout and timing of the source video. Photoreal, filmed on a cinema camera. No added objects, no people, no text, no logos, no palm trees."*
Reference ids are completed Higgsfield image jobs (see ## MEDIA). The skyline reference is the poplar-free NBP edit `2b9a9211…`.

| shot | refs (≤ 4) | prompt (before the common tail) |
|---|---|---|
| S1 RISE | hero-rooftop `b85a9daf`, skyline edit `2b9a9211`, aerial-city `5a697cec` | Turn this guide into real footage of a rooftop terrace in north Bucharest at dusk: pale travertine floor and low travertine parapet, olive trees in terracotta and bronze planters, early-autumn lindens and chestnuts beyond, a hazy low-rise city of 1970s apartment blocks and tiled-roof villas, the warm sunset glow low on the right behind the skyline, soft amber haze. The camera rises over the parapet and tilts down to the city and the empty building plot ahead. Match the colours and light of the reference photos. |
| S2 STACK | skyline edit `2b9a9211`, tower-exterior `c36cb2fc`, aerial-city `5a697cec` | Real construction time-lapse footage at dusk in north Bucharest: on the empty plot between glass office towers, a slender 24-storey residential tower is built floor by floor from the ground up. Each new floor slab lands on the one below; the top two or three floors show bare concrete slabs and columns, and dark bronze glass curtain wall panels follow below them; a full-height pale travertine band on one corner with deep warm-lit loggias rises with it, shifting slightly at mid-height; the crown completes it. Same tower design as the reference. Warm hazy dusk, sun low behind on the right, matching the skyline reference. The camera pushes slowly toward the plot in a gentle arc exactly as in the source. |
| S3 ORBIT | tower-exterior `c36cb2fc`, location `c63d6736`, aerial-city `5a697cec`, og `9d5b1fc6` | Real aerial footage at dusk orbiting a finished slender 24-storey residential tower in north Bucharest: a dark bronze-tinted glass curtain wall with mostly dark glass, and a full-height pale travertine band on one corner holding stacked deep loggias glowing warm, with a slight shift at mid-height. Behind it, the flat city of apartment blocks, villas and trees, and the calm Herăstrău lake reflecting the sky; warm haze, sun low behind on the right. The tower stays exactly the same building throughout; the camera orbits and rises as in the source and ends framing the travertine band. |
| S4 APPROACH | loggia `8d1f4168`, tower-exterior `c36cb2fc`, interior-living `adb38c91` | Real footage at dusk: the camera flies straight toward one deep loggia carved into the pale travertine band of the tower: thick travertine returns, a travertine floor and ceiling with small warm downlights, a frameless glass balustrade, floor-to-ceiling sliding glass doors with thin dark bronze frames, one panel open, and the warm-lit living room beyond (cream sofa, smoked oak, a linen floor lamp). Dark bronze glass facade on either side, the hazy dusk city far below. The loggia fills the frame at the end, as in the source. |
| S5 THRESHOLD | loggia `8d1f4168`, interior-living `adb38c91`, materials `c1a173f4` | Real footage: the camera passes through the open sliding glass door of the loggia into a luxury living room at blue hour: dark smoked oak joinery wall with lit shelves, pale travertine floor, a low cream bouclé sofa, a solid smoked oak coffee table, a dark leather lounge chair, a warm linen floor lamp, warm cove light in the ceiling, and a large window to the deep-blue dusk city. Match the reference interior exactly. |
| S6 DRIFT | interior-living `adb38c91`, materials `c1a173f4`, threshold `4baabbe0` | Real footage: a slow lateral camera drift through the same luxury living room at blue hour: smoked oak joinery with warm hidden light, pale travertine floor, the cream sofa and smoked oak coffee table, warm practical lamps on, a big window showing the deep-blue city with tiny warm lights. Calm and still; nothing in the room moves. Match the reference interior exactly. |

### Job log
| # | shot | model / setting | job id | credits | balance after | verdict |
|---|---|---|---|---|---|---|
| – | – | (start) | – | – | 655.56 | – |
| 1 | S2 pilot | kling_video_edit pro, src = guide S2 (media 254ca007), refs aerial + skyline edit | 3fb922c3-d6c5-4e3c-98a0-3ee71a6404a6 | 14 | – | ◐ photoreal, but 177/180 frames, horizon/framing shifted, ~10 min render; kept for the record |
| 2 | S2 pilot | seedance_2_5 video_edit 720p, same inputs | 0c73ec94-ba28-418d-bddc-3b3ff3dcfe22 | 57 | – | ✗ tower keeps the CG look and floats, 177/180 frames |
| 3 | S2 pilot | gemini_omni_flash_1_2 edit 1080p, same inputs | 0f3ab20c-85e3-4ada-a137-4ab825183bde | 26 | – | ✓ best: 180 frames, camera/stacking preserved, photoreal; top storeys still bare at the end |
| 4 | S5 key | gpt_image_2_6 2k edit of guide S5_first.png (media 6f327175), refs loggia + interior-living | df8cc723-95ac-4bbe-b8f2-6fd34a356fbf | 2 | – | ✓ keyframe |
| 5 | S5 | minimax_h3 2K 6 s, start = df8cc723, end = interior-living adb38c91 | 777c1632-6971-4fa0-990d-8f90bdd369dc | 12 | 544.56 | ◐ fallback only: sunset→night sky jump f66→f93 (judge C3) |
| 6 | S2 retake | gemini_omni_flash_1_2 edit 1080p, same inputs, prompt: fully glazed + crown by the last second, lived-in light clusters | 596a548e-59b7-4117-b0ed-2cb185b56944 | 26 | – | ◐ fallback only: glazed + crown at the end, but built on the v1 guide (band hidden, flattened volume, reads ~28–30 storeys per judge) — S2 to be retaken on the v2 guide |
| 7 | S6 | minimax_h3 2K 6 s, start = interior-living adb38c91, slow lateral truck | 778df68f-76dd-4c76-aa30-8910c4cab273 | 12 | 506.56 | ◐ fallback only: must chain from the new S5 last frame (judge C4) |
| 8 | S5 key r2 | gpt_image_2_6 2k edit of guide S5_first (media 6f327175), refs loggia + interior-living, BLUE HOUR | 43788575-357f-4424-be4d-b2e99923143f | 2 | – | ✓ blue-hour keyframe (framing pulled back to show the loggia frame + facade; doubles as the S4 end target) |
| 9 | S5 r2 | minimax_h3 2K 6 s, start = 43788575, end = interior-living adb38c91 | e48c6904-0a69-404a-a8c8-156a96f6ef49 | 12 | – | ✓ **S5 candidate**: one blue-hour sky throughout, continuous dolly through the glass, 158 f |
| 10 | S6 r2 | minimax_h3 2K 6 s, start = S5 r2 frame 157 (upload 2df77ef6), lateral truck left | cc899d95-7b00-4f8d-b4bd-fe094c047309 | 12 | – | ✓ chains exactly from S5 r2 f157; blue hour; 158 f; the drift is subtle (mostly in the first ~1.5 s) |
| 11 | S2 v2 | gemini_omni_flash_1_2 edit 1080p, src = v2 guide S2 (media 9e31946d), refs: v2 S2_last.png (274da778), tower-exterior, aerial-city, skyline edit | a88bedd4-8754-4484-9b08-ce02dd90e919 | 26 | – | ✗ take 1/3: band + side face OK, but top storeys still bare at f179 (no crown) and the base is pushed below the frame (tower too tall) |
| 12 | S2 v2 | gemini_omni_flash_1_2 edit 1080p take 2/3, v2 guide, refs S2_last + tower-exterior + aerial; prompt: pixel-for-pixel framing, base visible, crown in the last second | c1a81666-211b-47c6-8614-a7318108b466 | 26 | – | ✗ take 2/3 REJECTED by judge: base ~20% of frame height lower than the guide at f36/f90/f144 (58/68/78% vs 79/89/97%) and at the end → reads ~30 storeys; my first check (end only) was wrong |
| 13 | S2 v2 | kling_video_edit pro (tie-break), same guide and refs | 44d50a4c-a0cf-453d-aac5-18c5d0004dba | 14 | – | ✗ 177 f; base below the frame from f90 on (tower lengthened), stacking runs ahead of the guide, oversaturated sky |
| 14 | S2 alt key | gpt_image_2_6 2k edit of S2_alt_first.png (media 34ccb30b), refs aerial + skyline edit | c8b1c1fb-1e01-49c1-9349-ca6dc3b83124 | 2 | – | ✓ slab/horizon within ±3% of the guide |
| 15 | S2 alt key | gpt_image_2_6 2k edit of S2_alt_last.png (media 7f55eb12), refs tower-exterior + aerial | c2c81861-268c-4fd2-b189-96487684ac5f | 2 | – | ✓ tower top 7% / base 86% vs guide 8% / 88%; band + side face; 24 storeys + lobby |
| 16 | S2 alt | gemini_omni_flash_1_2 edit 1080p **take 3/3**, src = S2_alt (media a8207e8e), refs: keyframes c8b1c1fb + c2c81861, S2_alt_last (7f55eb12), tower-exterior | 13860704-b247-4fe5-8678-2f36a18bdd45 | 26 | – | ◐ to judge: base/top within ±2% at f36/90/144/179; ≈24 storeys + double-height lobby; band + step + side face; no flicker f120–178 (every 2 f); 180 f. Open point: the top reads as an open pergola frame crown (no solid cap) from ~f120 on |
| 17 | S2 crown fix | gemini_omni_flash_1_2 edit 1080p, src = take 3 job 13860704, refs take-3 f179 (upload 7dc62dcd), keyframe c2c81861, tower-exterior | 4ed4c4e6-12d6-4171-8c58-2754843f7656 | 26 | – | ◐ to judge: solid dark-bronze crown + band to the roof from f76 to the end; top/base unchanged at f90/144/179; no flicker f120–178; outside-tower diff = noise (MAD 1.1–1.9/255). Side effect: the cap appears at f76 while the tower is still growing (rides up like a climbing crown), replacing the bare-slab top f76–118 |
| 18 | S1 key | gpt_image_2_6 2k edit of S1_first v2 (media 86ec9a90), refs hero-rooftop, take-3 f0 | 1345341f-6b60-4ff7-a7fa-01a0e16b136b | 2 | – | ✗ not used: framing drifted (horizon 40% vs guide 52%) |
| 19 | S1 | gemini_omni_flash_1_2 edit 1080p, src = S1 v2 guide (media 230802dd), refs take-3 f0 (upload c03e76f1), hero-rooftop, aerial-city | 8b520b08-b867-4cfe-9763-ebdc50a77a47 | 19.5 | 337.06 | ✓ **S1 candidate** take 1/3: 132 f; slab/horizon/parapet match the guide at f0/44/88/131; f120–131 match S2 f0–11 in layout; camera clears the parapet at ≈ f62 (2.6 s → SPLIT_END) |
| 20 | S3 key | gpt_image_2_6 2k edit of S3_last v2 (media dbeef89c), refs take-3 f179, tower-exterior, location | 6ca62f23-b55b-485a-8d9e-6b8d796b3fc9 | 2 | – | ✓ tower x/horizon/storey pitch within ±2% of the guide; cooler late-dusk sky |
| 21 | S3 | gemini_omni_flash_1_2 edit 1080p take 1/3, src = S3 v2 guide (media eb0fce46), refs S2 fix f179 (upload cd9263ab), S3 key 6ca62f23, tower-exterior, location | 2999a82e-9a53-4591-96ef-b2af93e3db75 | 26 | – | ✗ take 1/3: f0–~43 left as the raw guide render (CG blocks), then pops to photoreal at f44; geometry f60/120/179 fine, end matches the keyframe |
| 22 | S3 | gemini_omni_flash_1_2 edit 1080p take 2/3, same source, refs S2 fix f179, S3 key, tower-exterior; prompt insists every frame is restyled | 200d0b85-13bf-4ea9-a8aa-e0b423d462f2 | 26 | – | ◐ take 2/3 to judge: photoreal from f0; top/base/x within ±2% of the guide at f0/60/120/179; tower constant through the orbit, solid crown, band continuous with step; no flicker f120–178; ends on the band, sky cooled to lavender. Overlap with S2 f168–179: same layout, but S3 shows a street where S2 has the hoarded site pad, and different slab facade detail |

### 3D motion guides (SPEC §8; production files, never published)
`blender/build_guides.py` (headless Blender 5.2.1, EEVEE, 0 credits). Each guide is 1280×720, 24 fps, H.264 yuv420p, in `blender/guides/` (v1 archived in `blender/guides/v1/`). Frame counts include the 12-frame overlap into the next shot.

| file | frames | duration | size |
|---|---|---|---|
| `S1.mp4` | 132 | 5.5 s | 0.87 MB |
| `S2.mp4` | 180 | 7.5 s | 1.67 MB |
| `S2_alt.mp4` | 180 | 7.5 s | 1.75 MB |
| `S3.mp4` | 180 | 7.5 s | 2.16 MB |
| `S4.mp4` | 132 | 5.5 s | 2.01 MB |
| `S5.mp4` | 132 | 5.5 s | 1.45 MB |
| `S6.mp4` | 120 | 5.0 s | 0.73 MB |

Also in `blender/guides/`: `S#_first/last.png`, `guides.json` and `S2_alt.json`. The GLBs now live in `blender/export/` (copies remain in `public/models/` until RELEASE drops them).
| 23 | S4 | minimax_h3 2K 6 s, start = S3 t2 f179 (upload 033432f7), end = S5 r2 keyframe 43788575 | e23c3830-a60e-4ceb-8ece-f8fe693df5a5 | 12 | – | ✓ **S4 final**: 158 f; continuous push from the band into one loggia, sky darkening to blue hour; chain MAD S3 f179→S4 f0 1.4, S4 f157→S5 f0 0.7 (of 255) |
| 24 | S2 tail fix | gemini_omni_flash_1_2 edit 1080p on S2 fix f108–179 (3 s trim, upload ac23e5aa), ref S3 t2 f0 (upload b99be1b7) | e1169d4a-a5cb-415e-b58e-5c6c00c90428 | 9.75 | 261.31 | ✗ not used: the end matches S3 f0 (street + balconied slab A), but slab A re-flows its lit-window pattern and grows balconies progressively through all 72 frames (a slow morph + flicker), and the site pad is already a street at f0, so the splice would jump → fallback: S2 fix as is, 6-frame S2→S3 dissolve |

### Final cut (merge, no credits)
`SPLIT_END=2.6 tools/video/merge.sh` with `assets-src/video/shots.tsv`. Segments: S1 8b520b08 [0,132) · S2 4ed4c4e6 [0,177) ⨯12 · S3 200d0b85 [3,180) ⨯6 (graded: highlight colour balance toward S2's sky, faded out over 3 s) · S4 e23c3830 [0,158) ⨯2 · S5 e48c6904 [0,158) ⨯2 · S6 cc899d95 [0,158) ⨯2 (⨯ = crossfade frames with the previous segment).

| file | size | details |
|---|---|---|
| `public/video/hero-1080.mp4` | 23.6 MB | H.264 High, 1920×1080, 24 fps, 936 frames = 39.0 s, CRF 27, `-g 6 -bf 0`, yuv420p, faststart, no audio |
| `public/video/hero-720.mp4` | 9.5 MB | same, 1280×720, CRF 29 |
| `public/video/hero-poster.webp` | 114 KB | frame 0, 1920×1080 |
| `public/video/hero.json` | 1.8 KB | `status: final`, shots/chapters/overlay generated by merge.sh (`overlay.split` = [0.11, 2.6], `overlay.card` = S6) |

Sky ΔE00 across cuts (frame before vs after each dissolve, top 20 % / full frame): S1→S2 0.97 / 1.52 · S2→S3 4.50 / 1.61 · S3→S4 1.43 / 0.68 · S4→S5 0.42 / 0.78 · S5→S6 0.33 / 0.54 (`assets-src/video/qa/deltaE_cuts.txt`).
QA: `assets-src/video/qa/cuts_contact_sheet.jpg` (rows = cuts; columns = −4, first, mid, last overlap frame, +4), `overview_every2s.jpg`, `ffprobe.txt`.
**VIDEO credits: 394.25** (balance 655.56 → 261.31).
