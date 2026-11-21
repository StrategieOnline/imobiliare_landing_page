# VIDEO review

## Pilot round (2026-11-21): spatial-plausibility gate before the bulk spend

**Verdict: CONDITIONAL GO.**
- **Models:** `gemini_omni_flash_1_2` edit for the guide-driven exterior shots (S1–S3), and keyframe edit + `minimax_h3` first/last image-to-video for the interiors (S4–S6). `seedance_2_5` video_edit is **rejected**.
- **Conditions:** the bulk spend starts only after conditions C1–C5 below are met. C1 is about the guides, not the video models.

Inputs I frame-stepped myself (the lead's grabs were cross-checked, not trusted):
- `assets-src/video/jobs/S2_gemini_0f3ab20c.mp4`: 1920×1080, 24 fps, 180 frames, **has an audio stream**.
- `S2_seedance_0c73ec94.mp4`: 1280×720, 177 frames.
- `S5_minimax_777c1632.mp4`: 2560×1440, 158 frames, **has an audio stream**.
- The guide `blender/guides/S2.mp4` (1280×720, 180 frames) and `S5_first/last.png`.

Method:
- 4×3 tiles every 15 frames of guide and edit at the same frame numbers.
- Every-2-frame steps on frames 40–86 (base and neighbours).
- A 5-frame strip over frames 120–179 (facade).
- Same-scale crops of frame 179 (guide vs edit).
- Every-3-frame steps on S5 frames 66–104 (the threshold crossing).

### Ruling 1: Gemini S2 (V4 / V5 / V6 / V13)

**What holds (the reasons Gemini wins):**
- **Camera preserved.** The push and arc match. The horizon sits at the same height. The tower is centred, and the *top* of the tower lands at the same frame row as the guide at f60, f75 and f165.
- **Neighbours stable.** Frame-stepping f40–86 at every 2nd frame, the villas, the 1970s blocks, the roads, the parked cars and the hoarded construction site stay put and move only by camera parallax. No morphing and no popping.
- **The stacking reads physically.** The tower grows from a real construction site at its foot, bottom→top. The top 3–6 storeys are bare slab and columns, with glazing climbing behind them. It reads as a construction time-lapse, which is what V6 asks for.
  - The lower 3–4 storeys stay bare until late. That reads as the podium/lobby being finished last, which is real-world plausible. Accepted.
- **V13 provenance.** It is a true video edit of a moving camera (parallax and occlusion change everywhere), not a 2D move.

**What fails (not shippable as is):**
1. **The end state is incomplete.** At f179 the top ~4 storeys are still bare and there is no crown. The guide ends fully glazed with the crown screen. (VIDEO's retake is planned.)
2. **The volume is flattened.** The guide shows the tower at 3/4: the front face plus a narrow side face with fins. Gemini renders a single frontal facade with no side face, so the tower reads as a flat slab, not a volume. This is a V4 geometry fail.
3. **Scale and storey drift.** The top matches, but Gemini's **ground plane sits lower**. The tower base moves from y≈600/720 (guide) to the frame bottom (≈705). The tower is ~17% of frame height taller and reads **~28–30 storeys**, against 24 (V5 allows ±1).
4. **No travertine band anywhere in S2**, although the prompt asks for it. The cause is the **guide**: from the S2 camera the band corner (+Z, front-right) faces away, so the guide shows a plain dark box. Gemini correctly follows the geometry it sees and ignores the prompt. The result is that S2 shows a generic glass tower, and the band only "appears" in S3. To a viewer, that reads as design drift.
5. The lit windows copy the guide's blocky barcode (expected; see ruling 4).

**Seedance S2 is rejected.** The tower **floats above the tree line** with no base, ground contact or site in most frames (row 3 of the grab), which is a V4/V6 spatial fail. It also has a CG look and costs 2.2× Gemini for 720p.

### Ruling 2: S5 minimax (V13 + continuity)

**It passes V13.** It is a genuine generated camera move, not a pan.
- **Parallax:** the near armchairs, the plant bowl and the olive trees scale and leave the frame edges faster than the back wall and shelves.
- **Occlusion:** the sliding-door mullions sweep past the edges between f78 and f93, and the occlusion order changes as the camera crosses the threshold.
- **Plausible camera path:** a drone path over the glass balustrade, past the low table, through the opening.
- **The end matches the reference:** it lands on the `interior-living` composition (sofa, block table, lamp, leather chair, lit shelves).
- **Start keyframe:** the gpt_image edit of `S5_first.png` keeps the guide layout one-for-one (planters → olives, blocks → armchairs, the table, the doors, the balustrade).

**Two continuity problems to fix before the merge:**
- **a. Time-of-day jump inside the shot (V7).** Through the living-room windows the sky is **orange sunset at f66** and **deep-blue night at f93**, about 1.1 s later. This is inherited from the two references: `loggia.webp` is at dusk, `interior-living` at blue hour.
- **b. The S5→S6 hand-off.** minimax ends on the `interior-living` framing, not on the guide's `S5_last.png`. The guide's `S6_first.png` therefore no longer matches, and an S6 generated from the guide would jump at the cut.

### Ruling 3: model choice
- **Exterior, guide-driven (S1 RISE, S2 STACK, S3 ORBIT): `gemini_omni_flash_1_2` edit at 1080p.** It is frame-accurate (180 in → 180 out), preserves the camera, keeps the neighbours stable and is the cheapest. Kling pro may be added as a tie-break on the S2 retake if it lands in time, but it does not gate the GO.
- **Interiors / threshold (S4 APPROACH, S5, S6): a keyframe image edit, then `minimax_h3` first/last image-to-video**, as S5 proved. These shots have few guide constraints beyond their endpoints, and minimax produced real parallax.
- **Seedance video_edit: no.**

### Ruling 4: should the retake prompt push "irregular lived-in lighting"?
**No. Fix it at the source, not in the prompt.** In a video-to-video edit the window pattern is geometry the model is told to keep. Asking it to re-invent the lighting invites exactly the drift we are fighting: windows toggling between frames, and the storey grid re-flowing.
- **Preferred fix:** re-render the S2/S3 guides with the 3D round-2 GLB, which has apartment-clustered, varied-intensity windows (3D fix 1). Gemini will then inherit a lived-in pattern, frame-consistently, for free.
- **Fallback, only if the guides can't be re-rendered:** a mild clause such as *"warm interior light of varied intensity; keep every window exactly where it is"*. The take then has to pass an every-2-frame flicker check: no window changes state between consecutive frames except at the stacking front.

### Conditions for the bulk spend (C1–C5)
1. **C1 · Guides first (3D-GUIDES D5).** Re-render S1–S3 with the round-2 GLB, and **change the S2/S3 camera azimuth, or rotate the tower, so the travertine corner band reads at 3/4 from S2's push onward.** It should be visible as the tower rises, as in reference t_2.0. Then re-run S2 on Gemini. Without this, S2 can only ever produce a generic glass box.
2. **C2 · S2 retake acceptance.**
   - The last ≥ 24 frames are fully glazed with the crown.
   - It reads as 24 storeys above the double-height lobby. Count them on the final frame; ±1 is allowed.
   - The base sits where the guide puts it (±5% of frame height).
   - The side face and corner volume are visible, as in the guide.
   - The prompt should state "exactly 24 storeys", "3/4 view showing two faces" and "fully glazed with the roof crown by the final second". Pass the guide's last frame as an image reference.
3. **C3 · One sky for S4–S6.** Decide blue hour or late dusk. I recommend **blue hour from S4 onward**, to match `interior-living`. Regenerate the S5 start keyframe so the room's windows already show that sky, and grade S4's exterior to match. The ΔE₀₀ < 5 check across the S3→S4 and S4→S5 cuts applies.
4. **C4 · Chain the shots.** Generate in order, using each shot's **actual last frame** (not the guide's) as the next shot's start keyframe or reference. In particular, S6 starts from minimax's S5 frame 158. The 12-frame overlaps must then match (V8).
5. **C5 · Hygiene.**
   - Strip the audio from every job output before merging (V2): the Gemini and minimax files both carry audio streams.
   - Downscale minimax 2560×1440 → 1920×1080 with lanczos.
   - Log every job, including the rejected Seedance and the pending Kling, in `## VIDEO` with its credits.
   - Spend so far is ≈ 115 of the 600 budget. Keep the S2/S3 retakes inside a stated cap, e.g. ≤ 3 takes per hard shot, and stop at a balance of 105.

When C1 and C2 are met, send me the S2 retake on its own. I'll frame-step it against the new guide before S3 is spent.

---

## S2 retake ruling: Gemini take 2 `c1a81666` on the v2 guide (2026-11-21)

**Verdict: REJECT as the final take**, so retake on 3D's S2_alt with the conditions below. **But this is the right direction.** C1 worked: the travertine band with its stacked loggias and the 3/4 side face read throughout, the stacking is physical (bare top frame, glazing following, a site at the foot), the neighbours are stable, and the last ~1 s is fully glazed with the parapet/crown.

**Why reject:**
- **The scale drift is systematic, not just the last 1.5 s.**
  - **Method:** same-scale pairs (640×360) of guide vs take at f36 / f90 / f144 / f179.
  - **The top matches** the guide's row at every sample.
  - **The base does not.** It sits ≈ **75 px / 360 ≈ 20% of frame height lower** at f36, f90 and f144 (guide base ≈ 58% / 68% / 78% of the height vs take ≈ 79% / 89% / 97%). At f179 the base is pushed past the bottom edge, while the guide's is at ≈ 88%.
  - In other words the tower is ~25–30% **longer** than the guide's at every sample: ≈ 30 storeys instead of 24 (V4 allows ±5% of frame; V5 allows ±1 storey). Early in the shot it also *looks* further along in the stacking than the guide at the same frame (f36: ~8 storeys + frame vs the guide's ~4).
  - This is the same failure mode as take 1. Gemini keeps the camera and the top, then rescales the building downwards into its own ground plane.
- **Chaining doesn't rescue it.** If S3 starts from take 2's last frame, S3 inherits a ~30-storey tower while its guide orbits a 24-storey one. The model must then either follow the start frame and drift from the S3 guide, or follow the guide and **shrink the tower during the orbit**. The second is exactly the popping/design drift that V5 fails. Chaining is required anyway (C4), but it only works if S2's last frame is *already* on-model.

**Conditions for the retake (S2_alt):**
1. **Lock the scale in the guide, not only the framing.** Raising the base 10–15% alone won't stop the elongation. Add real-scale context next to the plot in S2_alt: two or three ~9–10-storey slab blocks within ~100–200 m, the kind Gemini paints anyway. The model then has a height yardstick against the 24-storey tower and can't stretch it. Finishing the stacking by ~f120 is good: it leaves ≥ 2 s of fully glazed tower for the merge and the S3 hand-off.
2. **Pin both ends with images.** Make photoreal keyframes of S2_alt's first and last frames (gpt_image edits of the guide PNGs, the same route that worked for S5), check them against the guide for base position and storey count, and pass them as Gemini image references, along with tower-exterior. Prompt wording: "exactly 24 storeys above a double-height lobby; the tower's base stands on the plot exactly where it is in the source; do not lengthen the tower".
3. **Acceptance (I'll measure it the same way):** the base within ±5% of frame height of the guide at f36 / f90 / f144 / last frame, the top as now, 24 ± 1 storeys on the last frame, the band and side face visible, the last ≥ 24 frames fully glazed with the crown, no window flicker in every-2-frame steps.
4. **Hygiene:** this take also carries an **audio stream** (353 packets). Strip it at the merge (V2). Log take 2 as rejected in `## VIDEO`.

---

## S2 take 3 ruling: Gemini `13860704` on S2_alt (2026-11-21)

**Verdict: ACCEPT WITH CONDITION.** The geometry passes, and the crown gets one targeted fix pass on this clip. The S1/S3 spend may start in parallel. S3's *chaining keyframe* waits for the fixed S2 last frame.

**What I checked:**
- The measure sheet (guide | take, 5% grid) at f36 / f90 / f144 / f179.
- The f179 full-res tower crop.
- The f120–178 every-2-frame strip.

**What passes:**
- **Top and base** sit on the guide's rows at every sample (within one grid step, i.e. ≤ 5%). The near slab A matches the guide's yardstick block, so the scale is locked. This was the thing takes 1 and 2 failed, and it is fixed.
- **About 24 storeys above the double-height lobby.**
- **The band and side face** read throughout, with the stacked loggias lit.
- **The stacking** is physical.
- **No flicker or morphing:** the windows hold across f120–178, and the crown frame itself is stable, not morphing.

**The open point: the crown.**
- **What's there:** at f179 the top is an open steel frame about one storey tall, with glass guard panels. Up close (full-res) it *can* read as a rooftop pergola terrace.
- **Why that's not good enough:**
  - At hero scale and at f144 it reads as the top storey(s) still being bare frame, i.e. *unfinished*. That undercuts the "finished tower" beat.
  - It contradicts the canonical silhouette (`tower-exterior` / `location` / `og`: a solid flat top with the travertine band to the roof edge).
  - It contradicts the S3 guide's solid cap. S3 orbits close, and when chained from this frame the model would have to choose between the pergola (start frame) and the cap (guide). That is a V5 drift risk at the shot people look at longest.
- **Why not accept it as a designed pergola:** that makes the pergola canonical. It forces 3D, S3's guide and the section stills to change, or else leaves the page showing two different roofs. Fixing ~1.5 s of one clip is cheaper and safer.

**Condition: one targeted fix pass (≈ 26 cr), a Gemini edit of take 3 itself, not a new take.**
- **Prompt:** "Keep every pixel, the camera, the tower geometry, the neighbours and the timing identical. Change only the roof: from the moment the facade is fully glazed, the top is a solid dark-bronze roof crown with a closed parapet; the pale travertine band runs up to the roof edge; no open frame, no pergola, no railings." Pass the f179 frame and `tower-exterior` as references.
- **Acceptance (I'll re-measure):**
  - Top and base unchanged within ±5% at f90 / f144 / f179, and slab A still matching.
  - A solid crown from ≤ f150 to the end.
  - No new flicker in the every-2-frame check over f120–178.
  - Nothing else changed: a frame-diff outside the top ~15% of the tower should show only noise.
- **If the fix pass fails acceptance:** don't spend more on S2. Accept take 3 as-is with the crown read as a *roof terrace*, and make it canonical. In that case S3 must chain from take 3's f179 and carry the same crown, with the f179 crop as an S3 image reference, and 3D adds a matching roof frame to S3's guide so the guide and the start frame agree. The section stills stay as they are: their roof is seen from far enough away that the difference is minor.
- **Hygiene, as before:** strip audio, log take 3 and the fix pass with their credits, and record the final S2 in `hero.json` / ASSETS with its job id (V13a).

---

## S2 crown fix `4ed4c4e6` and S3 ORBIT take 2 `200d0b85` (2026-11-21)

### S2 crown fix: lead decision CONFIRMED (accept)
All my stated acceptance criteria are met: top and base unchanged, a solid crown well before f150, no new flicker, nothing else changed. The "climbing top" is the only new behaviour: the cap appears at f76 and rides up as the last floors are completed beneath it (grab `S2fix_construction_f40-118`).
- **Why that's acceptable:** it never pops. It rises continuously, and the storeys below it complete bottom→top with no gaps.
- **Why it's plausible:** it reads like the climbing protection screen real high-rises wear at the top during construction.
- **Not a rule break:** V6 only forbids floors materialising in mid-air, and none do.
- **No further spend on S2** for the crown.

### S3 take 2: ACCEPT the orbit itself; the S2→S3 overlap needs ONE fix pass (on S2's tail, not S3's head)

**The orbit passes** (measure sheet f0/60/120/179 plus the constancy and flicker strips):
- Geometry tracks the guide at all four samples.
- A constant 24 storeys, the solid crown, and one continuous band with loggias through the whole orbit. The windows are stable in the every-2-frame strip.
- Photoreal from f0. Take 1's unedited-guide head is gone.
- It ends on the band with the sky cooling toward blue hour, which is exactly the C3 hand-off into S4.

**The overlap (S2-fix f168–179 vs S3 f0–11) fails as-is.** The framing and the tower match, but two things don't:
- **(a) The ground at the base:** the hoarded site pad in S2 becomes a landscaped street with trees and cars in S3.
- **(b) Slab A's facade:** a neighbouring building that already exists changes design, from S2's flat gridded facade to S3's detailed balconies.

A 0.5 s crossfade turns both into a visible **morph**. V5 says nothing appears or changes except by occlusion. V8 says a crossfade must not double-expose misaligned geometry beyond a soft dissolve.
- **(a) could be excused** as the last beat of the time-lapse (the site being finished).
- **(b) can't be excused:** slab A is the closest, largest object in frame, and an existing building cannot change its design.
- **Sky:** S2 is cloudier and more saturated than S3's hazier sky. That alone would be fine in a dissolve, and a grade match at the merge covers it.

**Cheapest correct fix: one Gemini edit pass on S2's tail, ≈ 26 cr.** Use the last 3 s, ~f108–179 (Gemini's minimum source length is 3 s), with **S3 f0 as the image reference**. Prompt:
> "Keep the camera, the tower and its crown, the timing and everything else identical. In the last second the construction hoarding and site pad around the tower base are cleared and finished into the landscaped street, trees and paving exactly as in the reference image, as the final beat of the time-lapse. The near apartment block on the left must look exactly like the reference: same balconies, windows and roof."

**Why the tail of S2, not the head of S3:**
- S2 is already a time-lapse, so the site being finished in its closing second is physically consistent.
- Keeping the hoarding into S3 would show a construction site around a "finished, lived-in" tower during the real-time orbit. It would also contradict S4–S6, and it would force S3's better slab A down to S2's flatter one.
- It touches the clip that is already approved, so S3 needs no new spend.

**Acceptance (I'll measure):**
- The tower geometry and crown are unchanged in S2 f108–179 (top/base ±5%).
- The S2 f168–179 vs S3 f0–11 overlap matches in ground, slab A and tower. Check: frame-diff of the overlap pairs, with tile crops of the base and of slab A.
- The sky is grade-matched at the merge, ΔE₀₀ < 5 on matching sky patches across the cut.
- No flicker in the edited span.

**Fallback if the pass drifts the tower:** keep the approved S2 fix untouched. Instead, cut the overlap to **6 frames** and land the dissolve while slab A is partly occluded, or **crop the overlap** so slab A is out of frame. Only take this if the pass fails, because it trades a morph for a shorter, still-visible change.

**S4 may start now:** it chains from S3 f179, which is accepted. **The merge waits for the S2-tail pass.**

---

## FINAL merged cut (2026-11-21)

**Verdict: SHIP.** Slab A ships as is, and no further credits are spent. The release gate is the `hero.json` chapter retime in HERO.md round 4, which is free.

**Craft 8/10.** It reads as one unbroken camera move through one real place at dusk sliding into blue hour: rooftop → rise over the parapet → the tower stacking → an orbit on the travertine band → the push into a loggia → through the doors → the drift in the living room. Points off for the slab A dissolve and the slightly mannered loggia hold around 25 s.

### What I checked (my own measurements, not the QA files)
- `ffprobe` on both files, `-show_frames` keyframe spacing, a byte scan for faststart.
- md5 against `assets-src/video/placeholder.mp4`.
- grep of all job ids in `docs/ASSETS.md` and `shots.tsv`.
- An overview at 1 frame/s (39 frames).
- 24-frame tiles every 2 frames around all 5 cuts.
- An every-3-frame step through S4's approach (f534–572).
- S6 start/mid/end parallax measured in pixels.
- Per-second frame-difference motion profile of the 720 file.

| ID | | evidence |
|---|---|---|
| V1 | ✅ | 1080 + 720 + poster (1920×1080 = frame 0) + `hero.json` (`final`, 39.0 s, 936 f, 24 fps) all match `ffprobe` (nb_frames 936 on both) |
| V2 | ✅ | H.264 High, yuv420p, 24/1, **keyframe every 6 frames (154 gaps of 6)**, `has_b_frames=0`, `moov`@36 < `mdat`, **no audio stream** |
| V3 | ✅ | 23.58 MB ≤ 25; 9.46 MB ≤ 10; poster 114 KB ≤ 300 |
| V4 | ✅ | per-shot fidelity ruled shot by shot (pilot, S2 take 3 + crown fix, S3 take 2). S1 rise, S4 approach (continuous dolly onto one loggia that's present and growing from f534, no swap) and S5/S6 hold on frame-stepping |
| V5 | ⚠ minor (accepted) | **slab A** changes from a flat window grid to balconies inside the 6-frame S2→S3 dissolve (f291–296), and the site pad → street changes in the same frames. Nothing else morphs or pops in any tile: the tower keeps 24 storeys, the band and the crown from S2 f~120 through S4 |
| V6 | ✅ | stacking bottom→top, a climbing top cap, crown before the end of S2 (accepted earlier) |
| V7 | ✅ | sky ΔE₀₀ at the cuts: 0.97 / **4.50** / 1.43 / 0.42 / 0.33 (all < 5). Dusk → blue hour progresses across S3–S4, with no jump inside S5 (C3 met) |
| V8 | ✅ / ⚠ | S1→S2 (12 f), S3→S4, S4→S5 and S5→S6 (2-frame joins on real last frames) are seamless in the tiles. S2→S3: see V5 |
| V9 | ✅ | photoreal throughout; no blockout or flat-shaded frame; no text, people or palms |
| V10 | ✅ | spend within cap (balance 261 > floor 105); every final job is logged, including the failed tail fix `e1169d4a` |
| V11 | ✅ | 39.0 s (30–40); shot and chapter ranges in `hero.json` match the cut frames in `shots.tsv` (frame sum 960 − 24 overlap = 936) |
| V12 | ✅ | consistent grain and texture; S3's highlight balance fade-in is invisible in the tiles |
| **V13** | ✅ | **(a)** S1 `8b520b08`, S2 `4ed4c4e6`, S3 `200d0b85`, S4 `e23c3830`, S5 `e48c6904`, S6 `cc899d95` are all in `## VIDEO`, with frame ranges in `shots.tsv`. **(b)** no 2D move anywhere. Even the slowest shot, S6, has real parallax: over f780→935 the foreground table moves +34 px against +15–21 px for the back wall/window and the lamp, and the right armchair crops out. The motion profile has **no ≥ 1 s run** below a 0.3 mean frame difference (the slowest second is 25 s at 0.35, the loggia hold). **(c)** `status: final`, md5 ≠ placeholder, nothing under `public/video` is committed yet |

### Ruling on slab A: ship as is. If a fix is ever forced, it would be (b), but I'm not recommending the spend.
- **(a) S3 retake with the flat facade: no.** S4 is chained from S3's *real* last frame. A new S3 changes that frame and breaks S4 (and S5/S6 behind it). It would also swap S3's better slab for S2's flatter one, and it reopens an orbit that took two takes.
- **(b) Full-clip S2 edit (balconies from f0): the least bad fix, but it doesn't remove the problem, it moves it.** S1's last frames show the same block with the flat lit-window grid. The facade change would migrate to the S1→S2 dissolve, where the slab is ~26% of frame width (against ~55% at S2's end) over 12 frames. That's milder, but still a change. Removing it needs S1 + S2 both edited (~52 cr). It would also re-expose the stacking shot that needed three takes plus a crown fix to the same Gemini drift that killed the tail fix `e1169d4a`.
- **(c) A shorter dissolve: no.** A 2-frame switch turns a soft morph into a pop or jump cut on the largest foreground object.
- **Why shipping is acceptable:**
  - The change happens inside a 0.25 s dissolve that is exactly the ch1→ch2 copy handover. `ETAJ CU ETAJ` blurs out and `TRAVERTIN pe verticală` masks in, bottom-left, over the slab's own screen area. The tower, which is the subject, holds rock-steady through it.
  - At scroll speed it reads as a soft dissolve, not a building transforming.
  - It's logged as a known, accepted flaw.

### Housekeeping
- §8.4: delete `assets-src/video/placeholder.mp4` now that the real cut has landed (it's gitignored, so it's hygiene only).
- RELEASE: commit `public/video/*` (23.6 + 9.5 MB, both < 50 MB). `deploy.sh` must now pass the "not placeholder" gate.
