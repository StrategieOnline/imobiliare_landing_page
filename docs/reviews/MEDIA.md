# MEDIA review

## Round 1 (2026-11-21)

**Verdict: FAIL (narrow)** · **Craft 7/10**

The verdict is FAIL by the rubric's rule: 4 major items fail (M3, M7, M8, M9). The fail is narrow and concentrated:
- Three of those items come from **one image** (`aerial-city`).
- The fourth is a grade/continuity problem between the two opening plates.
- The other major finding is a compositing trap in `skyline-dusk`.

Eleven of the 13 images are ship-quality, and several are excellent: `interior-living`, `threshold`, `materials`, `loggia`, `location`, `skyline-dusk` as a photo. One regeneration, one matte and one regrade turn this into a PASS. 185 credits remain, so the budget allows it.

Craft justification:
- **Strengths:** the interior family (`interior-living`, `threshold`, `materials`, `res-*`) is a convincing, coherent material world of smoked oak, travertine and cove light. It holds up at 100%, and the threshold's corridor lands exactly on the interior plate's sofa, lamp and window, which is great for continuity. `skyline-dusk` genuinely reads as Pipera/Barbu Văcărescu, and the tower is consistent across `tower-exterior`, `location` and `og`.
- **Deductions:** `aerial-city` is a Paris/Vienna rooftop-scape seen from 400 m. Rooftop→skyline, which are consecutive in the hero, change season, sun side and grade. The tower photos read ~20 storeys and warm-glazed, against the 24-storey dark-bronze model.

What I checked:
- `sips` dimensions, `file` magic and `du` for every file.
- Every image read at viewing size, plus 100% crops of the skyline (left, right, plot), the rooftop parapet, the tower's mid-section and the location's waterline.
- The 4 depth maps tiled against their plates.
- Wordmark contrast measured on the plate pixels.
- The ASSETS.md credit arithmetic recomputed.

### Handoff claims

| claim | result |
|---|---|
| 13 images at exact sizes | ✅ all 13 are present, RIFF/WEBP, exact px (2560×1440 ×6, 1600×2000 ×3, 1200×1500 ×3, 1200×630) |
| 4 `*_depth.webp` + `og.jpg` | ✅ depth maps are 1280×720 (half-res, same 16:9 aspect; accepted in rubric rev 2). `og.jpg` is 147 KB |
| 3.6 MB total | ✅ `du` = 3760 KB. Under the 6 MB cap |
| 65 credits | ✅ the sum checks out: 41.75 (final colour plates) + 8 (depth) + 15.25 (rejected candidates) = 65.0. That is ≤ 250 |
| No text, logos, faces or palms | ✅ confirmed at 100% (skyline façades, rooftop skyline, tower, interiors) |
| aerial-city 521 KB | ❌ over the 500 KB cap (§7.3) |

### Checklist

| ID | | note |
|---|---|---|
| M1 | ✅ | 13 + 4 depth + og.jpg |
| M2 | ✅ | exact sizes. Depth at half-res is accepted |
| M3 | ❌ major | `aerial-city.webp` 521 KB > 500. Everything else is within its cap. `hero-rooftop` (446 KB) is the only first-view image |
| M4 | ✅ | no text, people or palms. Minor artefacts in finding 6 |
| M5 | ✅ | every brief is met literally: the rooftop's empty lower third, the skyline's central plot, no tower in the aerial's centre third, open sliding glass, pivot door, two-sided glass corner, double-height penthouse, lake at blue hour |
| M6 | ✅ (minors) | the same tower in `tower-exterior` / `location` / `og`: bronze curtain wall, travertine corner seam with a mid-height kink, stacked lit loggias. See finding 6 for storey count and glass tone |
| M7 | ❌ major | rooftop→skyline continuity (finding 3) |
| M8 | ❌ major | aerial horizon and perspective (finding 1) and skyline foreground occlusion (finding 2). Loggia and interior are good push-in targets |
| M9 | ❌ major | `aerial-city` reads as Paris/Vienna (mansard roofs, Haussmann blocks, hills on the horizon). The others read as Bucharest |
| M10 | ✅ | manifest is complete with prompts, job ids and credits. Only own images are used as references. No reference frames |
| M11 | ✅ | no visible banding or halos at 100% |
| G4 | ✅ | no reference brand or place names in the prompts or the manifest |
| G8 | ✅ | the handoff is accurate and candid about its weak spots |

### Per-image notes (art director)

| image | grade | note |
|---|---|---|
| hero-rooftop | B | Clean, Bucharest-plausible (blocks and a TV mast on the skyline). But it has an HDR real-estate look: front-lit parapet and floor while the sun sets behind, saturated, spring blossom. The lower third is only 2.4:1 against the cream wordmark |
| skyline-dusk | A− | The best "real photo" of the set: a hazy business district with a scrubby vacant plot. The centre poplar is a trap (finding 2) |
| aerial-city | C | Lovely as a picture, but the wrong city, the wrong altitude for the shot, and over the size cap |
| tower-exterior | B+ | Strong silhouette and seam gesture. It reads ~20 storeys, warm-glazed, with the same furniture on every balcony and a tree reflected in the glass 8 floors up |
| loggia | A− | A perfect one-point push-in target. Minors: Manhattan-like towers in the glass, and the box is wider than the seam's loggias |
| interior-living | A | Exactly the brief. The headline zone is 5.9:1 against cream |
| threshold | A | Pivot door, corridor, and the destination matches `interior-living` |
| materials | A | Low key, with negative space lower-left for the headline |
| location | A− | A convincing Herăstrău at blue hour, with willows and reflections. Same tower |
| res-loggia / corner / penthouse | B+ | Distinct rooms, but the same styling props repeat in all three (finding 7) |
| og | A− | Clean card composition with the tower on the right third |
| depth maps | B | Usable for subtle parallax. `loggia_depth` has the near façade strips at the edges marked far |

### Fixes (numbered, for the team)

1. **major · `public/img/aerial-city.webp` (covers M3, M8, M9) · Regenerate.** Today it is a view from ~400 m looking down about 25–30°, with the horizon at ≈25% of the frame height. The chapter 2 camera is beside the tower at roughly mid-height (40–60 m), looking almost level; in the reference (t_3.0) the backdrop horizon sits at ≈55% of the frame. Composited behind a level-camera tower, this plate will look pasted on, and HERO cannot crop it to fix that because there is not enough sky. The city is also visibly Paris/Vienna (mansard roofs, ornate perimeter blocks) with hills on the horizon.
   - **Fixed looks like:**
     - Shot from ~60–100 m with a near-level camera, the **horizon at 45–55%** of the height, and lots of hazy sky above.
     - North Bucharest character: flat terrain; a mix of 1970s apartment blocks, interwar villas with tiled roofs, and a few glass offices off to the sides; Herăstrău/Floreasca water and the park canopy.
     - No mountains. Still no dominant tower in the centre third.
     - Horizon haze matched to `skyline-dusk` (`#d08357`) and the sun on the same side as in `skyline-dusk` (right/behind).
     - Encoded **≤ 500 KB** from the PNG source. As a stop-gap, re-encoding the current file at q≈76 already gives ~492 KB, but that only fixes M3.
2. **major · `public/img/skyline-dusk.webp` (M8) · Foreground poplar in the plot.** A tall poplar stands in the foreground at x ≈ 45–52%, with its top at y ≈ 58%. That is *above* the far edge of the plot (y ≈ 60%), so any tower standing in the plot centre must be hidden behind it. If HERO composites the GLB over the plate, the tower will sit in front of the tree and the illusion breaks.
   - **Fixed looks like (pick one):**
     - Ship `skyline-dusk_fg.webp`: a full-resolution (2560×1440) alpha matte or RGBA cut-out of everything in front of the plot (the poplar, foreground canopies, the near rooftops). HERO layers it over the tower.
     - Or inpaint the poplar out of x 40–60%.
   - Either way, write in the handoff the exact base point for the tower (x%, y% of the plot centre at the far wall) and the sun direction (back-right), so HERO can light it to match.
3. **major · `hero-rooftop.webp` vs `skyline-dusk.webp` (M7) · Continuity.** These are consecutive in one continuous camera rise, but:
   - The rooftop is saturated HDR with **spring** foliage (flowering horse chestnuts) and the sun low on the **left**.
   - The skyline is a hazy, filmic **autumn** scene (dry scrub, yellowing trees) with the sun **right/behind** the towers.

   The crossfade will read as two different days.
   - **Fixed looks like:**
     - Regrade `hero-rooftop` toward the skyline's look: lower saturation and local contrast, warm atmospheric haze, lifted blacks, the floor and parapet in dusk shade rather than front-lit.
     - Ideally regenerate it with late-summer/early-autumn foliage (no blossom) and the sunset glow right of centre.
     - Then put the two side by side and check them at the 12% boundary.
4. **minor · `hero-rooftop.webp` · Wordmark contrast.** The lower-third average is RGB(176,144,126), which is **2.4:1** against the cream wordmark `#f1e7d0`.
   - **Fixed looks like:** with the regrade in fix 3, bring the floor zone (y 68–92%) to ≥3:1. The floor would be in shade at dusk anyway. HERO may add a scrim, but the plate should not depend on it.
5. **minor · `loggia_depth.webp` · Wrong depth at the edges.** The near façade strips at the left and right edges are black (far), so parallax will make the frame edges swim. **Fixed:** paint those strips near-white, or document that HERO must clamp depth to the stone frame.
6. **minor · `tower-exterior.webp`, `location.webp`, `og.webp` · Tower details.**
   - The tower reads as ~19–20 storeys (18 loggias + a double-height lobby) against the 24-storey contract and model.
   - The glass is warm and interior-lit rather than dark bronze.
   - A large tree is reflected in the curtain wall 7–9 floors up, where no tree can be (`tower-exterior` ≈ x 530–790, y 1300–1450; `location` ≈ x 840–1010, y 890–1000).
   - Every balcony has the identical lamp/chair/plant set.

   **Fixed looks like:** these are acceptable to ship. If you regenerate anything, regenerate `tower-exterior` first, with 24 storeys, darker bronze glass with fewer lit rooms (mostly dark glass, warm loggias as the accent, which also matches the 3D `M_WindowGlow` idea), no impossible reflections, and varied loggia styling. Then re-derive `location` and `og` from it.
7. **minor · `res-loggia`, `res-corner`, `res-penthouse` · Repeated props.** All three repeat the same cream bouclé sofa + draped beige throw + stone bowl on a smoked-oak block. In the hover list the preview swaps will feel like one room cropped three ways.
   - **Fixed looks like:** each image leads with its own feature, with the shared props removed from at least two of them:
     - Terrace: the outdoor loggia lounge.
     - Corner: the dining table at the glass corner.
     - Penthouse: the double height, fireplace and gallery.
8. **minor · `loggia.webp` · Off-brief details.** Through the doors and in the right-hand glass there is a dense high-rise skyline (Manhattan-like). The loggia is also ~2–3 bays wide, against the one-bay loggias in `tower-exterior`. Fine for the hero. Fix only if you regenerate.
9. **minor · `docs/ASSETS.md` / `docs/HANDOFF-MEDIA.md` · Stale numbers.**
   - "gpt_image_2_6 … for 14 images": I count 13 GPT jobs (12 finals + 1 rejected).
   - "aerial-city at -q 78 to stay under 600 KB" and "budget 8 MB" predate §7. The caps are now 500 KB per plate and 6 MB total.

   Update both after the fixes.

**Note for the lead (not MEDIA's):** `index.html` `og:image` points at `og.webp`. `og.jpg` (147 KB, ≤150 KB) is the safer choice for crawlers that ignore WebP.

**Notes for HERO from this review:**
- Fog/horizon colours: `skyline-dusk` is `#d08357` and the aerial is `#d5915e`.
- The skyline sun is back-right, so key the 3D tower from behind-right.
- Use the depth maps only for a few-percent parallax.

---

## Round 2 (2026-11-21)

**Verdict: PASS** · **Craft 8/10** (up from FAIL-narrow / 7)

All three majors are fixed, and the fixes are visibly better, not just compliant. The opening plates now read as one evening in one city.
- **Spend:** 35.5 credits this round, 100.5 in total (≤ 250).
- **Caps:** every file is within the §7.3 caps; `public/img` = 3760 KB (≤ 6 MB). The largest plate is `loggia` at 414 KB.
- **og:image:** now points at `og.jpg` (147 KB ≤ 150).

Per the lead's decision, `tower-exterior` / `location` / `og` stay as the canonical silhouette. Round-1 finding 6 is closed as "accepted", not open.

### What I checked
- Dimensions, sizes and WebP magic for all 18 files: unchanged px, all within caps.
- **`skyline-dusk` edit integrity:** I diffed the round-2 plate against my round-1 copy.
  - The sky and top-centre are effectively identical (mean |Δ| 0.5).
  - Outside the edit zone, the difference is edge-only, high-frequency re-encode noise, with no geometric shift (difference map inspected).
  - The edit zone (x 37.5–62.5 %, y ≥ 53 %) holds the only real change: the poplar is gone, replaced by plausible scrub and the near rooftop, with no seam, smear or repeated texture at 100%.
  - The plot, the far wall and the horizon are where they were.
- **`hero-rooftop` contrast:** the wordmark zone (y 68–92 %) averages RGB(126,99,85), **4.49:1** against cream. The brightest 28-px cell is **3.58:1**. This matches the handoff (4.6 / 3.55). Was 2.4:1.
- Every changed image read as an art director at viewing size, plus the depth maps tiled.

### Round-1 fixes

| # | was | now |
|---|---|---|
| 1 major · aerial-city | Paris/Vienna from 400 m, horizon ≈25 %, 521 KB | ✅ Near-level from ~80 m, **horizon ≈ 53 %**. Unmistakably north Bucharest: 1970s blocks, tiled-roof villas, lindens, a Herăstrău-like lake mid-distance, flat to the horizon, no hills. Glow right of centre, consistent with skyline-dusk. 307 KB. My favourite plate in the set now |
| 2 major · skyline-dusk poplar | blocked the plot | ✅ Removed by a clean localized edit; the geometry is unchanged; `_depth` updated (no tree) |
| 3 major · rooftop↔skyline continuity | spring HDR, sun left | ✅ Early-autumn trees, no blossom, haze, lower saturation, parapet and floor in shade, glow right of centre. Side by side with skyline-dusk it now reads as the same evening |
| 4 minor · wordmark contrast | 2.4:1 | ✅ 4.5:1 average |
| 5 minor · loggia_depth edges | facade strips marked far | ✅ Painted near; the frame edges will no longer swim |
| 6 minor · tower photos | ~20 storeys, warm glass | ⏸ **Accepted** by lead decision (canonical silhouette; 3D matches it) |
| 7 minor · res-* shared props | same sofa/throw/bowl ×3 | ✅ Three distinct rooms: terrace daybed + lantern + olive; corner dining with pendant, no sofa; penthouse double height + fireplace + gallery, two chairs only. The hover swaps will now feel like different homes |
| 8 minor · loggia skyline | Manhattan-like towers | ⏸ Unchanged (judge said fix only if regenerating). Still minor |
| 9 minor · docs | stale counts and caps | ✅ Corrected |

### Remaining notes (minor, no action required for PASS)
1. **minor · `res-penthouse.webp`:** the two-storey window shows a dense high-rise skyline (lower right), the same Manhattan-like cue as `loggia`. North Bucharest has a handful of towers, not a wall of them. If either image is ever regenerated, ask for "low-rise city lights with a few distant towers".
2. **Note for the §8 pivot (VIDEO team):** these plates are now the **image references** for the video edits, and the reduced-motion and section imagery. Treat `hero-rooftop`, `skyline-dusk` and `aerial-city` as the grade bible for S1–S3: sun low back-right, haze ≈ `#d08357`/`#d7875e`. Treat `loggia` + `interior-living` as the bible for S4–S6. The poplar edit no longer matters for compositing (the three.js mask is retired), but the cleaner plot still helps as an S2 reference.
