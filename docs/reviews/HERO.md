# HERO review

(The three.js HERO review was cancelled mid-way by SPEC §8. Its one surviving measurement, the card inset, is carried into HV5 below.)

## Round 1: HERO-v2, video-scrub mechanics (2026-11-21)

**Verdict: PASS WITH FIXES** · **Craft 8/10 (mechanics only)**

The footage is VIDEO's placeholder (panned plates, 720p, 34 s) in both `hero-1080.mp4` and `hero-720.mp4`, so, as instructed, only the mechanics are judged.

**The scrub engine is excellent.** On the real GPU it presents **60 video frames/s** while scrolling forwards and backwards. The worst seek was 5 ms going forward and 122 ms going back (a single one), and the frame at rest is within **1 ms** of target. three.js is fully gone (171 kB JS, 63 kB gz, no canvas). The overlay system carried over intact, and the ch5 card closes to exactly `inset(57.6px round 18px)` at 1440, which is 4vw / 18px.

What keeps it from PASS:
- **The overlay runs ahead of footage that isn't there yet**, because scrubbing only works after the full download (issue 2).
- **The video download starts before first paint.**
- **A 2-second headline gap** in S1 (issue 1).

All three have concrete fixes below.

### Method
- `npx vite build` into a scratch outDir. The copy was served under `/imobiliare_landing_page/` (python static server; the blob path needs no ranges).
- Headless Chrome over CDP with `--use-angle=metal`. WebGL reports `ANGLE Metal Renderer: Apple M4 Pro`, so the GPU is real, though there is no WebGL on this page anymore.
- **1440×900:** 26 positions sampled every 4% of the pin, the displayed `currentTime` read against the target at each, the card geometry at the end of the pin, and a 10 s linear scroll forward, then 10 s back. During the scrolls I counted `requestVideoFrameCallback` callbacks, `seeking`→`seeked` latency, rAF deltas and long tasks.
- **Network:** an unthrottled run plus a **40 Mbps** desktop run. **375×812 @2x at 10 Mbps** with touch. Reduced motion.
- I confirmed that GitHub Pages answers `Range` with **206** (`accept-ranges: bytes`) on the live site.
- All servers and Chrome instances were stopped afterwards. Nothing in the tree was touched.

### Measurements

| | desktop 1440, unthrottled | desktop, 40 Mbps | mobile 375 @2x, 10 Mbps | reduced motion |
|---|---|---|---|---|
| FCP | 344 ms | 396 ms | 360 ms | 464 ms |
| video GET starts | **311 ms (before FCP)** | 395 ms (≈ FCP) | 399 ms | none ✅ |
| source picked | 1080 | 1080 | **720** ✅ | — |
| scrub usable (`loadeddata` on blob) | 407 ms | **2.8 s** for 9.7 MB | **9.0 s** for 9.7 MB | — |
| scrub forward, 10 s | rVFC **60.7 fps**, 607 seeks, max seek **5 ms**, rAF median 16.7 / p95 16.8, 0 long tasks | — | 60.7 fps, max 7 ms | — |
| scrub back, 10 s | rVFC **60.1 fps**, 601 seeks, max seek **122 ms** (one), one frame over 50 ms | — | 60.7 fps, max 6 ms | — |
| at rest | \|Δt\| = 0.001 s at the end, 0.000 s at the start | — | — | — |
| pin | 6.5 vh (5850 px) | — | 4.0 vh ✅ | no pin ✅ |
| console | 0 errors, 0 exceptions | 0 | 0 | 0 |

Extrapolating the real footage: a 25 MB 1080 file is ≈ 5–6 s to usable at 40 Mbps. A 10 MB 720 file is ≈ 9 s at 10 Mbps. During that time the visitor scrolls chapter headlines over a static poster.

### Checklist (RUBRIC rev 4)

| ID | | evidence |
|---|---|---|
| HV1 | ✅ | `three` is gone from package.json, the lockfile and node_modules. `grep` finds no `from 'three'` in `src`. The bundle has 0 three.js signatures; 171.3 kB / 63.4 kB gz. 0 `<canvas>` on the page |
| HV2 | ✅ | fetch → stream reader with progress → `Blob` → object URL. `<video muted playsinline preload="auto" disablepictureinpicture>`; poster until ready; HUD hairline + %; exactly **one** full GET per video, no range traffic |
| HV3 | ✅ | see the table: ≥ 60 presented fps both ways (bar: 20); max seek 122 ms (bar: 150); at rest within 1 frame |
| HV4 | ✅ | chapters, TC, list, HUD-out and card windows all derive from `hero.json`. The split and card *fractions* (15% of S1, 20–92% of S6) are still hard-coded heuristics (fix 1 moves them into the JSON) |
| HV5 | ✅ | wordmark split, mask-in / blur-out headlines (§7.1 verbatim), crop marks, TC, list, cursor `scroll`; **card = `inset(57.6px round 18px)` = 4vw / 18px** at the end of the pin |
| HV6 | ✅ | 650vh desktop / 400vh mobile |
| HV7 | ✅ | 720 under 768 px (verified) or on `saveData` (code) |
| HV8 | ✅ | reduced motion: no `<video>` element, no pin, only the poster is fetched; stacked blocks |
| HV9 | ⚠ major | the budget passes easily (pre-paint: HTML + 29 kB CSS + 63 kB gz JS + fonts + 61 kB poster + 2 kB JSON ≈ 0.3 MB). But **the video request starts before first paint** (311 ms vs FCP 344 ms), so on slow links a 10–25 MB download competes with fonts and the poster (fix 3) |
| HV10 | ✅ | 0 console errors; works under the sub-path; on a failed fetch the code falls back to the streaming URL, and the poster stays on error (code path) |
| HV11 | ⏸ | the placeholder is in `public/video/` by design for now. It is **not** in git (`git log --all -- public/video` is empty). Ship gate in V13c / HV13 |
| HV12 | ✅ | the three.js modules are deleted (index, video, timeline, overlay, static, config, math, css only); small modules |
| HV13 | ⏸ | no still-animation code path (the only stills are the poster before ready and the reduced-motion blocks). Ship gate pending real footage (`hero.json` still says `"status": "placeholder"`) |

### Rulings on the two open issues

**Issue 1, the headline gap (~0.8 s → 3.0 s): approved, with a change.**

Today the split runs over 1–15% of S1 (0.05–0.79 s). Then the rooftop scrolls by with **no copy for ~2.2 s** (my samples at 1.36 s and 2.72 s are empty frames), and ch1 starts at 3.0 s, still inside S1. That means `ETAJ CU ETAJ` lands over the rooftop rather than the stacking.

In the reference, the split happens as the camera starts to move, and the next headline masks in ~0.2–0.5 s after the letters clear, just as the new view opens. Your proposal fixes the semantics. I'd set it as follows:
- **Split:** ~2% → **~75% of S1**, so the letters are fully gone exactly as the camera clears the parapet. The real cue is the frame where the parapet leaves the frame, so pick it in the final footage.
- **ch1 start:** = **S2 start − half the crossfade** (≈ 5.0 s with the 0.5 s overlap). The mask-in then lands as the plot comes into view, not after it.
- **Chapters:** ch0 runs `0 → S2 start`, so the list shows `01 ÎNCEPUT` for all of S1.
- **Put both numbers in `hero.json`**, e.g. `"overlay": { "split": [0.1, 3.9], "card": [30.2, 33.6] }` in seconds, with the current fractions as the fallback. VIDEO can then tune them to the real cut without a code change. This also closes the HV4 note.

**Issue 2, scrubbing only after the full blob download: approved in principle, but not as "set src, then swap src".**

The direction is right. Pages serves ranges (verified 206), and the encoding (`-g 6 -bf 0 +faststart`) makes seeks inside buffered data cheap. A 5–9 s poster-only wait is too long for the centrepiece. Two traps in the proposal as written:
- **(a) Double download.** If the element streams via ranges *and* a parallel `fetch()` pulls the whole file, a phone can pay for the video twice (up to 20 MB on 720, 50 MB on 1080).
- **(b) A visible swap.** Assigning a new `src` to the on-screen `<video>` resets `readyState` and flashes the poster or black for a few frames.

**Fixed looks like:**
1. **Stream first.** After first paint (fix 3), set `video.src` to the streaming URL with `preload="auto"`.
2. **Clamp scrubbing to what's buffered.** Clamp the scrub target to the buffered range that contains the current time, minus 1 frame. Show the **buffered fraction** on the HUD bar. Drive the overlay from the *displayed* time (already the case), so copy never runs ahead of the footage. Today the overlay advances over a static poster while the blob loads, and that has to stop.
3. **Measure before keeping the blob.** Once `buffered` covers the whole duration, set the network offline through CDP and scrub forward and back.
   - If there are no stalls, Chrome is serving from its media cache. **Drop the blob step entirely.** That's simpler, with one download.
   - If seeks stall, keep a blob, but only on desktop and never on `saveData`. Start it *after* the stream has finished, so the second fetch comes from the HTTP cache. **The acceptance criterion is that total video bytes on the wire are ≤ 1.15× the file size** (Network panel).
4. **If a swap is kept, double-buffer it.** Use a second hidden `<video>` with the blob URL, wait for `loadeddata`, set it to the displayed time, wait for `seeked`, then swap visibility in one rAF and dispose the old element. Never reassign `src` on the visible element.

The judge re-measures: time-to-first-scrub at 10 and 40 Mbps, bytes on the wire, and the HV3 numbers with the stream source.

### Fixes (numbered, for the team)

1. **major · `src/hero/timeline.js:26-30` + `public/video/hero.json` · Headline gap.** Implement the issue-1 ruling: split ≈ 2→75% of S1, ch1 from S2 start − crossfade/2, ch0 to S2 start, both read from `hero.json.overlay` (seconds) with the current fractions as fallback. **Done when:** no 4%-step sample from 0 to the end of S1 is copy-less for more than ~1 s, and `ETAJ CU ETAJ` first appears with the plot in view.
2. **major · `src/hero/video.js:54-90` (`load`) and `:100-111` (`tick`) · Progressive scrub.** Implement the issue-2 ruling: stream first, clamp to buffered, HUD shows the buffered fraction, the overlay never runs ahead of the footage. Keep the blob only if the offline test demands it, with the ≤ 1.15× bytes rule and a double-buffered swap. **Done when:** scrub usable within ~1 s of first paint at 40 Mbps (and ~2 s at 10 Mbps on 720); no copy past the buffered footage; no poster flash at the swap.
3. **major · `src/hero/index.js:69-75` · Fetch order.** `loadTimeline().then(… scrub.load …)` fires at module evaluation, so the video GET goes out **before** FCP (311 vs 344 ms). Start the video only after first paint: double `requestAnimationFrame` after the poster has decoded (`img.decode()`), or `requestIdleCallback` with a 300 ms timeout. `hero.json` itself can stay early. **Done when:** the video request `startTime` > FCP in all three runs.
4. **minor · `src/hero/video.js:3` · Settle speed.** `EASE = 0.12` makes a big jump settle in ~0.5–0.7 s, which is fine for wheel scrolling. On a long fling the copy (driven by displayed time) trails the scroll noticeably. Consider a distance-aware ease (e.g. `k` scaled up when `|d| > 1.5 s`) so fast flings catch up in ≤ 0.35 s while small moves stay silky.
5. **minor · `public/video/hero.json` · Placeholder status.** `"status": "placeholder"` plus identical 1080/720 files are fine now, but they are a **ship blocker** (V13c / HV13). Make `deploy.sh` (RELEASE) refuse to publish while `hero.json.status === "placeholder"`, or while the mp4 hash equals `assets-src/video/placeholder.mp4`.

**Note for RELEASE / lead (not HERO):** `public/models/` (city.glb) is still in `public/`, so it ships in `dist/` (R10). Move it to `blender/export/` per §8.1.

---

## Round 3: streaming scrub, overlay from JSON (2026-11-21)

**Verdict: PASS** · **Craft 9/10 (mechanics; the footage is still the placeholder)**

All three round-1 majors are fixed and independently verified. The streaming design is better than both the blob and my "stream then swap" suggestion: one download, no swap, and copy that can't outrun the footage. Your `main.js` change (ScrollTrigger refresh → `lenis.resize()`) also works: a `lenis.scrollTo(1500)` issued 600 ms after load landed at `scrollY = 1500` on both desktop and mobile.

**Method:**
- `npx vite build` (172.1 kB / 63.6 kB gz) into scratch, served from `/imobiliare_landing_page/` by my own Node server. It supports HTTP Range, counts bytes per file on the server side and throttles server-side (40 Mbps desktop, 10 Mbps mobile).
- Headless Chrome with ANGLE/Metal (real GPU), the HTTP cache enabled.
- Sequence: load → S1 copy check in 0.25 s steps → 10 s linear scroll forward and 10 s back → 0→90% fling → **CDP offline** → 6 s forward and back again.
- Servers and Chrome stopped afterwards.

| | desktop 1440, 40 Mbps, 1080 file | mobile 375 @2x, 10 Mbps |
|---|---|---|
| file picked | `hero-1080.mp4` | `hero-720.mp4` ✅ |
| FCP → first presented frame | 372 → **855 ms** | 424 → **951 ms** |
| video bytes on the wire / file | **9 735 351 / 9 735 351 = 1.00×**, 1 request (`0-9735350`) | **1.00×**, 1 request |
| scrub 10 s forward / back | rVFC **60.5 / 60.5 fps**, max seek **4 / 6 ms**, rAF 16.7, 0 frames > 50 ms | — |
| buffered after scrub | `[0, 34]` | — |
| **offline** forward / back (6 s) | **60.8 fps**, max seek 6 ms, **0 failed requests, 0 server requests** | — |
| fling 0 → 90% | settles in **337 ms**, Δ 0.027 s | — |
| pin | 6.5 vh | 4.0 vh ✅ |
| console | 0 errors / 0 exceptions | 0 / 0 |

**Copy timing in S1 (displayed time).**
- The intro copy blurs out by 1.5 s.
- The wordmark letters fly 3.25 → 4.25 s, with the last letter clearing at 80% of S1.
- **Empty 4.25 → 4.75 s (≈ 0.5–0.75 s)**.
- `ETAJ CU ETAJ` from **5.0 s**.

The ruling's ≤ 1 s bar is met, and the overlay reads `hero.json.overlay` when present.

### Checklist delta

| ID | was | now |
|---|---|---|
| HV2 (no blob) | blob | ✅ **streaming by design, approved.** One range download (1.00×), zero refetch offline, the HUD shows the buffered fraction. HV2's "blob-fetched" wording is superseded by this ruling |
| HV3 | ✅ | ✅ 60 fps both ways online *and offline*; max seek ≤ 6 ms |
| HV4 | ✅ (heuristic split/card) | ✅ `overlay.split/card` from JSON, with documented fallbacks |
| HV9 | ⚠ the video started before FCP | ✅ the request waits for `poster.decode()` + a double rAF. Desktop's first frame is at 855 ms against an FCP of 372 ms. On mobile, resource timing puts the request start at 414 ms against an FCP of 424 ms. That 10 ms difference is FCP's presentation timestamp trailing the rAF clock, after the poster is decoded and painted, not real contention. Accepted |
| HV10 | ✅ | ✅ an error makes `limit()` return ∞, so the copy runs over the poster with no crash (code path) |
| HV11 / HV13 | ⏸ | ⏸ **ship gates**: `hero.json` still says `"status": "placeholder"` and both mp4s are the placeholder. They are not committed. They must be replaced by VIDEO's merge before any deploy |

### Remaining notes (none blocking)
1. **minor · `src/hero/video.js:81` · Buffered bar vs clamp.** `measure()` only reports the range that starts at 0. If a visitor drags the scrollbar far ahead, so that Chrome buffers a later island, the bar stays at the first range while `limit()` uses the island. That's harmless (the copy stays correct). Consider reporting the range around the displayed time.
2. **For VIDEO:** tune `hero.json.overlay.split` to the frame where the real S1 camera clears the parapet, and `overlay.card` to S6's calmest stretch. No HERO change is needed.

---

## Round 4: the real footage in the live hero (2026-11-21)

**Verdict: SHIP AFTER ONE DATA FIX** (`hero.json` chapter retime, no code, no credits) · **Craft 9/10**

**Method:**
- Production build (172 kB / 63.6 kB gz) with the final `public/video/*`, served from `/imobiliare_landing_page/` by my range server (byte counts per file; throttles at 40 Mbps, 10 Mbps and unthrottled).
- Headless Chrome on the real GPU (ANGLE/Metal).
- Full sequence on desktop/1080 and on mobile/720: load → copy timing in 0.25 s steps over 0–8 s → 10 s scrub forward and back → fling → card at the end of the pin → offline scrub.

| | desktop 1440, **1080** (23.6 MB) @ 40 Mbps | mobile 375 @2x, **720** (9.5 MB) @ 10 Mbps | mobile 375, 720, unthrottled |
|---|---|---|---|
| first presented frame (FCP) | **885 ms** (396) | **927 ms** (432) | — |
| bytes on wire / file | **1.00×**, 1 request | **1.00×**, 1 request | — |
| scrub forward / back, 10 s | rVFC **60.5 / 60.5 fps**, max seek **11 / 10 ms**, 0 frames > 50 ms | — | **60.5 / 60.6 fps**, max seek 8 / 8 ms |
| offline after a full scrub | 60.8 / 61 fps, **0 failed, 0 server requests** | — | 60.8 fps, 0 / 0 |
| fling 0 → 90% | 338 ms | — | 339 ms |
| card at the end of the pin | `inset(57.6px round 18px)` = 4vw / 18px, over S6 ✅ | — | `inset(15px round 18px)` = 4vw ✅ |
| console | 0 / 0 | 0 / 0 | 0 / 0 |

### Overlay against the footage
- **Wordmark vs parapet ✅.** The camera clears the parapet between ~1.0 and 2.0 s. The intro copy is gone by 1.0 s, and the letters fan out and clear by **2.5 s** (`overlay.split` [0.11, 2.6]). It's a good lock: the letters are flying exactly while the parapet drops out of frame.
- **Card over S6 ✅.** `overlay.card` [32.417, 39.0] covers all of S6's slow drift, and the HUD fades over its first quarter.
- **ch1 and the stacking: ❌ (fix).** There is **no copy at all from 2.5 to 4.9 s (≈ 2.4 s)**, which breaks the ≤ 1 s rule from the round-1 ruling. Then `ETAJ CU ETAJ` lands at 5.0 s on an empty plot, and the first floors only become legible ~7 s.
  - **Fixed looks like:** in `hero.json` set `chapters[0].end = 3.5` and `chapters[1].start = 3.5`. Because `overlay` is present, the code uses the JSON chapter values verbatim (`timeline.js`), so no code change is needed.
  - **Result:** ch1 masks in as the camera settles on the empty plot ("from nothing… floor by floor"), the copy gap drops to ≈ 0.9 s, and the headline holds over the whole stacking (7–12 s).

### Checklist (final)
HV1–HV10 and HV12: ✅, as in round 3, now re-measured on real footage.
- **HV11 ✅:** the placeholder is gone from `public/video`; the md5 differs.
- **HV13 ✅:** no still-animation path, and `status: final`.
- **HV4 ✅:** overlay windows from JSON. It's the ch1 *value* that needs retiming, not the mechanism.

**Ship once the two `hero.json` numbers are changed.** I'll re-run the 0.25 s copy check, about 2 minutes, if you want it confirmed before deploy.
