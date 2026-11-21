import { FALLBACK_TIMELINE, videoUrl } from './config.js';

/**
 * Converts hero.json (seconds) into the progress windows (0 → 1 over the pin) that the overlay
 * uses. Scroll maps linearly onto the footage, so progress = time / duration.
 */
export function buildTimeline(json) {
  const src = valid(json) ? json : FALLBACK_TIMELINE;
  const d = src.duration;
  const p = (t) => t / d;
  const shot = (id, i) => src.shots.find((s) => s.id === id) || src.shots[i];
  const s1 = shot('S1', 0);
  const s6 = shot('S6', src.shots.length - 1);
  const s1Len = s1.end - s1.start;
  const s6Len = s6.end - s6.start;
  const s2 = shot('S2', 1);
  const chapters = src.chapters
    .slice()
    .sort((a, b) => a.index - b.index)
    .map((c) => ({ start: c.start, end: c.end }));
  const ov = src.overlay;
  if (!ov) {
    // Judge ruling (round 1): ch0 holds for all of S1; ch1 masks in as the plot appears.
    chapters[0].end = s2.start;
    chapters[1].start = s2.start - (src.crossfade ?? 0.5) / 2;
  }
  chapters.forEach((c) => { c.start = p(c.start); c.end = p(c.end); });
  chapters[chapters.length - 1].end = 1.0001;   // the last chapter never exits
  // Overlay windows in seconds from hero.json → overlay; otherwise derived from the shots.
  const split = ov?.split ?? [s1.start + s1Len * 0.02, s1.start + s1Len * 0.8];
  const card = ov?.card ?? [s6.start + s6Len * 0.2, s6.end - s6Len * 0.08];
  return {
    sources: { ...SOURCES, ...src.sources },
    duration: d,
    fps: src.fps || 24,
    chapters,
    // The wordmark flies apart as the camera clears the parapet; the intro copy blurs out with it.
    split: split.map(p),
    // Over S6: the HUD fades, then the video wrapper closes into the rounded card.
    hudOut: [p(s6.start), p(s6.start + s6Len * 0.25)],
    card: card.map(p),
  };
}

const SOURCES = { 1080: 'hero-1080.mp4', 720: 'hero-720.mp4', poster: 'hero-poster.webp' };

function valid(j) {
  const win = (w) => w === undefined || (Array.isArray(w) && w.length === 2 && w[1] > w[0]);
  return j && j.duration > 0 && Array.isArray(j.shots) && j.shots.length
    && (!j.overlay || (win(j.overlay.split) && win(j.overlay.card)))
    && Array.isArray(j.chapters) && j.chapters.length >= 6
    && j.chapters.every((c) => c.end > c.start && c.end <= j.duration + 0.01);
}

export async function loadTimeline() {
  try {
    const res = await fetch(videoUrl('hero.json'), { cache: 'no-cache' });
    return buildTimeline(res.ok ? await res.json() : null);
  } catch {
    return buildTimeline(null);
  }
}
