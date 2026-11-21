# HANDOFF — Team HERO (video-scrub hero, round 3)

## What's built
`src/hero/**` is a pinned hero where one merged video is scrubbed by scroll, with the DOM overlay on top. It has no WebGL and no three.js (JS 172 kB, 63.6 kB gz). It is mounted from `src/main.js` with `mountHero(document.getElementById('hero'))`.
- **index.js** creates the pin: `refreshPriority: 1`, `scrub: true`, 650vh on desktop and 400vh below 768px.
  - Ticker loop: scroll progress → target time → `VideoScrub.tick()` → overlay at the *displayed* time. The loop is paused off screen.
  - Sets the cursor `scroll` state; exposes `destroy()`.
  - Load order: `hero.json` and the poster load at mount; the video request waits for the poster to decode and paint.
- **video.js** (`VideoScrub`):
  - The poster is an `<img>` (decoded, then a double rAF) over the `<video muted playsinline preload="auto" disablepictureinpicture>`, and fades out on the first presented frame.
  - It then sets the relative **streaming** URL (`video/hero-1080.mp4`, or `-720` under 768px or on saveData). That is one range request, with no blob and no second download.
  - The scrub target is clamped to the end of the buffered range holding the displayed frame, minus 1 frame. The HUD bar shows the buffered fraction.
  - Easing adapts to distance: lerp 0.12→0.42 per frame, plus a 1.5 s/s minimum catch-up speed.
  - A seek is issued only after the previous frame is presented (requestVideoFrameCallback, or `seeked`), with a 400 ms watchdog.
  - Never calls play().
- **timeline.js** turns `video/hero.json` into progress windows. Chapters come from `chapters[]`; the split and card windows come from `overlay.split/card` (seconds).
  - Without an `overlay` block: split = 2→80% of S1, ch0 runs to the S2 start, ch1 starts at S2 start − crossfade/2, card = 20→92% of S6.
  - If the JSON is invalid, `FALLBACK_TIMELINE` in config.js is used.
- **overlay.js**:
  - Wordmark flight (the outermost letter clears exactly at the end of the split), and mask-in / blur-out headlines (§7.1).
  - HUD: crop marks, coordinates, chapter tag, TC, ring, chapter list, buffered bar + %.
  - Card (inset 4vw / 18px) on the video wrapper.
- **static.js** handles reduced motion: poster + wordmark, then ch1–4 as image blocks, then the CTA. No video.
- **config.js** / **math.js** / **hero.css**: copy, pin and fallback timeline; easing helpers; styles.

## Changing the video
Replace `public/video/hero-1080.mp4`, `hero-720.mp4`, `hero-poster.webp` and `hero.json`. Overlay timing follows the JSON: `duration`, `fps`, `sources`, `crossfade`, `shots[]`, `chapters[]`, and optionally `overlay: { split: [s, e], card: [s, e] }` in seconds. No code change is needed.

## Placeholders (VIDEO will overwrite)
Both mp4s are copies of `assets-src/video/placeholder.mp4`; the poster is its first frame. `hero.json` has `"status": "placeholder"`, which is a ship blocker for RELEASE.

## Measurements (headless Chrome, Metal GPU, own profile; byte-counting range server, server-side throttling)
| run | file | FCP | video request | first scrubbable frame | wire bytes / file | scrub 10 s fwd / back (rVFC fps, max seek) | offline fwd / back (max seek, new requests) |
|---|---|---|---|---|---|---|---|
| 1440, unthrottled | 1080 placeholder 9.74 MB | 392 ms | after FCP | 535 ms | 9.74 / 9.74 MB (1.00×) | 57 fps, 43 ms / 57 fps, 42 ms | 38 ms / 38 ms, 0 |
| 1440, 40 Mbps | 9.74 MB | 340 ms | 371 ms | 487 ms | 1.00× | 57.7 fps, 5 ms / 57.6 fps, 6 ms | 8 ms / 6 ms, 0 |
| 1440, 40 Mbps | 20.4 MB 1080 test encode | 452 ms | 486 ms | 651 ms | 20.43 / 20.43 MB (1.00×) | 57 fps, 42 / 55 ms | 12.5 / 7.9 ms, 0 |
| 375 @2x, 10 Mbps | 720 9.74 MB | 456 ms | 703 ms | 919 ms | 1.00× | 57.6 fps, 5 / 6 ms | 4 / 8 ms, 0 |
- A 0→90% fling settles in ~380 ms.
- An early fling at 10 Mbps holds footage and copy ~0.45 s behind the buffered edge and advances at about 4.4 s of footage per second. Copy never runs ahead.
- S1 copy check (0.25 s steps): wordmark/intro until 3.75 s, empty 4.0–4.75 s (≤ 1 s), ch1 from 5.0 s as the plot appears.
- 0 console errors in every run. `npx vite build` passes.

## Known gaps
- Chrome buffers only ~16 s ahead while the video is paused at the top. The rest streams as the visitor scrubs, which the clamp handles.
- A `lenis.scrollTo` issued before ~1 s after load clamps to 0, because Lenis measures late (main.js, Lead). Native scrolling is fine.
- One earlier CDP-throttled run picked the 720 file at 1440px; it did not reproduce in later runs.
- The split and card cues should be tuned by VIDEO via `hero.json.overlay` once the real footage lands.
