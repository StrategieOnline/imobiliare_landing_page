import { MOBILE_MQ, videoUrl } from './config.js';
import { clamp, smooth } from './math.js';

const EASE = 0.12;          // per-60fps-frame lerp for small moves (wheel steps stay silky)
const EASE_FAST = 0.42;     // reached at ≥ 1.35 s of distance, so long flings catch up in ~0.35 s
const MIN_SPEED = 1.5;      // s of footage per s: floor on the catch-up speed, so the ease tail is short
const STUCK_MS = 400;       // give up waiting for a frame callback after this long

/**
 * Scroll-scrubbed <video> streamed with HTTP ranges (one download, no blob). The scrub target is
 * clamped to the buffered range that holds the displayed frame, so neither the footage nor the
 * overlay (driven by the displayed time) can run ahead of what has arrived. A new seek is issued
 * only after the previous frame is presented, so fast scrolling coalesces instead of queueing.
 * play() is never called.
 */
export class VideoScrub {
  constructor(frame, { onBuffered }) {
    const v = document.createElement('video');
    v.className = 'hx-video';
    v.muted = true;
    v.playsInline = true;
    v.preload = 'auto';
    for (const a of ['muted', 'playsinline', 'disablepictureinpicture', 'disableremoteplayback']) v.setAttribute(a, '');
    v.setAttribute('aria-hidden', 'true');
    const poster = document.createElement('img');
    poster.className = 'hx-poster';
    poster.alt = '';
    poster.decoding = 'async';
    poster.setAttribute('fetchpriority', 'high');
    frame.prepend(v, poster);
    this.video = v;
    this.poster = poster;
    this.onBuffered = onBuffered;
    this.fps = 24;
    this.time = 0;
    this.ready = false;
    this.failed = false;
    this.pending = false;
    this.seekAt = 0;
    this.buffered = 0;

    const presented = () => {
      if (this.ready) poster.classList.add('is-hidden');   // a real frame is on screen
      this.pending = false;
    };
    if ('requestVideoFrameCallback' in v) {
      const onFrame = () => { presented(); v.requestVideoFrameCallback(onFrame); };
      v.requestVideoFrameCallback(onFrame);
    } else {
      v.addEventListener('seeked', presented);
    }
    v.addEventListener('loadeddata', () => {
      this.ready = true;
      this.seek(this.time);
    }, { once: true });
    v.addEventListener('progress', () => this.measure());
    v.addEventListener('error', () => { this.failed = true; this.onBuffered(1); });
  }

  static pick(sources) {
    const small = matchMedia(MOBILE_MQ).matches || navigator.connection?.saveData;
    return videoUrl(small ? sources['720'] : sources['1080']);
  }

  /** Shows the poster; resolves once it is decoded and painted (the video request waits for this). */
  async showPoster(url) {
    this.poster.src = url;
    try { await this.poster.decode(); } catch { /* missing poster: carry on */ }
    await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  }

  stream(url) {
    this.video.src = url;
  }

  // Buffered fraction from the start of the file, for the HUD bar.
  measure() {
    const v = this.video;
    const d = v.duration;
    if (!(d > 0) || !v.buffered.length) return;
    const end = v.buffered.start(0) <= 0.05 ? v.buffered.end(0) : 0;
    const f = end >= d - 2 / this.fps ? 1 : end / d;
    if (f !== this.buffered) { this.buffered = f; this.onBuffered(f); }
  }

  // Latest playable time: the end of the buffered range holding the displayed frame, minus a frame.
  limit() {
    const v = this.video;
    if (this.failed) return Infinity;            // no footage at all: let the overlay run over the poster
    if (!this.ready) return 0;
    const b = v.buffered;
    for (let i = 0; i < b.length; i++) {
      if (this.time >= b.start(i) - 0.05 && this.time <= b.end(i) + 0.05) {
        return b.end(i) >= v.duration - 2 / this.fps ? v.duration : b.end(i) - 1 / this.fps;
      }
    }
    return this.time;
  }

  seek(t) {
    const v = this.video;
    this.pending = true;
    this.seekAt = performance.now();
    v.currentTime = Math.min(Math.max(t, 0), v.duration - 0.001);
  }

  /** Advances the displayed time toward `target` (seconds); returns the time now on screen. */
  tick(target, dtMs) {
    const frame = 1 / this.fps;
    const goal = Math.min(target, this.limit());
    const d = goal - this.time;
    const ease = EASE + (EASE_FAST - EASE) * smooth(clamp((Math.abs(d) - 0.15) / 1.2));
    const k = 1 - (1 - ease) ** (dtMs / 16.667);
    const step = Math.max(Math.abs(d) * k, Math.min(Math.abs(d), (MIN_SPEED * dtMs) / 1000));
    this.time = Math.abs(d) < frame ? goal : this.time + Math.sign(d) * step;
    if (!this.ready) return this.time;
    if (this.pending && performance.now() - this.seekAt > STUCK_MS) this.pending = false;
    if (!this.pending && !this.video.seeking && Math.abs(this.video.currentTime - this.time) >= frame * 0.5) {
      this.seek(this.time);
    }
    return this.time;
  }

  dispose() {
    this.video.removeAttribute('src');
    this.video.load();
  }
}
