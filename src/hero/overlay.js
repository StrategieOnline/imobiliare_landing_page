import gsap from 'gsap';
import { CHAPTERS, INTRO, LIST, TIMECODE_FPS } from './config.js';
import { easeIn, easeInOut, range, smooth } from './math.js';

const WORD = 'ORIZONT';
const RING_C = 2 * Math.PI * 13;
const CARD = { inset: 4, radius: 18 };   // vw, px
const HIDE = 150;   // % offset that clears even the tall Ă/Î/Ș accents out of the mask
const pad = (n) => String(n).padStart(2, '0');

const line = (html) => `<span class="hx-line"><span>${html}</span></span>`;

function chapterHTML(ch, i) {
  const cta = ch.cta
    ? `<div class="hx-ch__cta">${ch.cta.map((b) => `<a class="${b.cls}" href="${b.href}">${b.text}</a>`).join('')}</div>`
    : '';
  return `<article class="hx-ch${ch.cta ? ' hx-ch--cta' : ''}" data-i="${i}">
    ${ch.label ? `<p class="hx-ch__label mono"><span class="hx-rule"></span>${ch.label}</p>` : ''}
    <h2 class="hx-ch__title display">${ch.title.map(line).join('')}</h2>
    ${ch.body ? `<p class="hx-ch__body">${line(ch.body)}</p>` : ''}
    ${cta}
  </article>`;
}

export function hudHTML() {
  return `<div class="hx-hud" aria-hidden="true">
    <i class="hx-crop hx-crop--tl"></i><i class="hx-crop hx-crop--tr"></i>
    <i class="hx-crop hx-crop--bl"></i><i class="hx-crop hx-crop--br"></i>
    <p class="hx-tag hx-tag--tl mono">44°28′N · 26°05′E</p>
    <p class="hx-tag hx-tag--tr mono">${INTRO.label}</p>
    <p class="hx-tc mono">TC <span>00:00:00:00</span></p>
    <p class="hx-load mono"><i class="hx-load__bar"></i><span class="hx-load__pct">0%</span></p>
    <div class="hx-rail">
      <span class="hx-ring"><svg viewBox="0 0 30 30"><circle cx="15" cy="15" r="13"/><circle class="hx-ring__p" cx="15" cy="15" r="13"/></svg></span>
      <ol class="hx-list mono">${LIST.map((t, i) => `<li><b>${pad(i + 1)}</b> ${t}<i></i></li>`).join('')}</ol>
    </div>
  </div>`;
}

export function wordmarkHTML(tag = 'h1') {
  return `<${tag} class="hx-wordmark" aria-label="ORIZONT — Rezidențe private în București">
    <span class="hx-wm" aria-hidden="true">${[...WORD].map((c) => `<span class="hx-wm__l"><span class="hx-wm__clip"><span class="hx-wm__c">${c}</span></span></span>`).join('')}</span>
  </${tag}>`;
}

/** Fit the wordmark to the frame width (spec ~19vw; Unbounded 900 is wider than that allows). */
export function fitWordmark(root) {
  const wm = root.querySelector('.hx-wm');
  if (!wm) return;
  wm.style.fontSize = '';
  const avail = root.clientWidth * 0.94;
  const w = wm.scrollWidth;
  if (w > avail) wm.style.fontSize = `${(parseFloat(getComputedStyle(wm).fontSize) * avail) / w}px`;
}

export class Overlay {
  /** tl: progress windows from buildTimeline(); replace later with setTimeline(). */
  constructor(frame, tl) {
    this.frame = frame;
    this.tl = tl;
    frame.insertAdjacentHTML('beforeend', `
      ${wordmarkHTML()}
      <div class="hx-intro">
        <p class="hx-cue mono"><span class="hx-rule"></span>${INTRO.cue}</p>
        <p class="hx-sub">${line(INTRO.sub)}</p>
        <p class="hx-lead">${line(INTRO.body)}</p>
      </div>
      <div class="hx-chapters">${CHAPTERS.map((ch, i) => (i ? chapterHTML(ch, i) : '')).join('')}</div>
      ${hudHTML()}`);

    const q = (s) => frame.querySelector(s);
    this.wordmark = q('.hx-wordmark');
    this.letters = [...frame.querySelectorAll('.hx-wm__l')];
    this.introEl = q('.hx-intro');
    this.hud = q('.hx-hud');
    this.tc = q('.hx-tc span');
    this.tag = q('.hx-tag--tr');
    this.ring = q('.hx-ring__p');
    this.items = [...frame.querySelectorAll('.hx-list li')];
    this.chapters = [...frame.querySelectorAll('.hx-ch')].map((el) => ({
      el,
      i: +el.dataset.i,
      lines: el.querySelectorAll('.hx-line > span'),
      fade: el.querySelectorAll('.hx-ch__label, .hx-ch__cta'),
      shown: false,
      k: -1,
    }));
    this.ring.style.strokeDasharray = RING_C;
    this.last = { p: -1, ci: -1, frame: -1, card: -1, hud: -1, intro: -1, wm: -1 };
    gsap.set(frame.querySelectorAll('.hx-wm__c, .hx-line > span'), { yPercent: HIDE });
    gsap.set([this.introEl.querySelector('.hx-cue'), this.hud], { opacity: 0 });
  }

  fit() { fitWordmark(this.frame); }

  setTimeline(tl) {
    this.tl = tl;
    this.last.p = this.last.wm = this.last.intro = this.last.hud = this.last.card = -1;
    this.chapters.forEach((c) => { c.k = -1; });
  }

  /** Buffered fraction of the video (0 → 1): a hairline + percentage in the HUD, gone once complete. */
  loading(f) {
    if (!this.load) {
      this.load = this.frame.querySelector('.hx-load');
      this.loadBar = this.load.querySelector('.hx-load__bar');
      this.loadPct = this.load.querySelector('.hx-load__pct');
    }
    this.loadBar.style.backgroundSize = `${f * 100}% 100%`;
    this.loadPct.textContent = `${Math.round(f * 100)}%`;
    this.load.classList.toggle('is-done', f >= 1);
  }

  /** Load-in: wordmark letters rise out of their masks, then the intro copy and the HUD. */
  intro() {
    const tl = gsap.timeline({ delay: 0.1 });
    tl.to(this.frame.querySelectorAll('.hx-wm__c'), { yPercent: 0, duration: 1.3, ease: 'power4.out', stagger: 0.06 })
      .to(this.introEl.querySelectorAll('.hx-line > span'), { yPercent: 0, duration: 0.9, ease: 'power4.out', stagger: 0.1 }, 0.45)
      .to([this.introEl.querySelector('.hx-cue'), this.hud], { opacity: 1, duration: 1, ease: 'power2.out' }, 0.7);
  }

  update(p) {
    if (p === this.last.p) return;
    this.last.p = p;
    this.flyLetters(p);

    // Intro copy blurs out as soon as the journey starts.
    const [s0, s1] = this.tl.split;
    const ki = range(p, s0, s0 + (s1 - s0) * 0.35);
    if (ki !== this.last.intro) {
      this.last.intro = ki;
      this.introEl.style.opacity = 1 - ki;
      this.introEl.style.filter = ki > 0 ? `blur(${ki * 12}px)` : '';
      this.introEl.style.visibility = ki >= 1 ? 'hidden' : '';
    }

    this.chapters.forEach((c) => this.chapter(c, p));

    let ci = 0;
    this.tl.chapters.forEach((ch, i) => { if (p >= ch.start) ci = i; });
    if (ci !== this.last.ci) {
      this.last.ci = ci;
      this.tag.textContent = CHAPTERS[ci].label || CHAPTERS[ci - 1].label;
      this.items.forEach((li, i) => li.classList.toggle('is-active', i === CHAPTERS[ci].list));
    }

    const f = Math.round(p * this.tl.duration * TIMECODE_FPS);
    if (f !== this.last.frame) {
      this.last.frame = f;
      this.tc.textContent = `00:00:${pad(Math.floor(f / TIMECODE_FPS))}:${pad(f % TIMECODE_FPS)}`;
    }
    this.ring.style.strokeDashoffset = RING_C * (1 - p);

    const hud = 1 - range(p, this.tl.hudOut[0], this.tl.hudOut[1]);
    if (hud !== this.last.hud) { this.last.hud = hud; this.hud.style.opacity = hud; }

    // Over S6 the video wrapper closes into an inset rounded card.
    const c = easeInOut(range(p, this.tl.card[0], this.tl.card[1]));
    if (c !== this.last.card) {
      this.last.card = c;
      this.frame.style.clipPath = c > 0 ? `inset(${c * CARD.inset}vw round ${c * CARD.radius}px)` : '';
    }
  }

  // Letters fly past the camera: each moves toward the viewer in z (the container's perspective
  // pushes it outward from the centre and scales it up), staggered from the centre letter outward.
  flyLetters(p) {
    const t = range(p, this.tl.split[0], this.tl.split[1]);
    if (t === this.last.wm) return;
    this.last.wm = t;
    this.wordmark.style.visibility = t >= 1 ? 'hidden' : '';
    const mid = (this.letters.length - 1) / 2;
    const span = 1 - mid * 0.07;   // the outermost letter clears exactly at the end of the window
    this.letters.forEach((el, i) => {
      const d = i - mid;
      const s = Math.abs(d) * 0.07;
      const e = easeIn(range(t, s, s + span));
      if (e === 0) { el.style.transform = ''; el.style.filter = ''; el.style.opacity = ''; return; }
      el.style.transform = `translate3d(${d * e * 9}vw, ${-e * 8}vh, ${e * 760}px)`;
      el.style.filter = `blur(${e * 16}px)`;
      el.style.opacity = 1 - smooth(range(e, 0.35, 0.92));
    });
  }

  // Per-line mask reveal when the chapter becomes current; scrubbed blur + fade on the way out.
  chapter(c, p) {
    const { start, end } = this.tl.chapters[c.i];
    const inRange = p >= start && p < end;
    if (inRange && !c.shown) {
      c.shown = true;
      gsap.killTweensOf([c.lines, c.fade]);
      gsap.fromTo(c.lines, { yPercent: HIDE }, { yPercent: 0, duration: 0.9, ease: 'power4.out', stagger: 0.08 });
      gsap.fromTo(c.fade, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out', delay: 0.15 });
      c.el.classList.add('is-on');
    } else if (!inRange && c.shown) {
      c.shown = false;
      gsap.killTweensOf([c.lines, c.fade]);
      if (p < start) gsap.to(c.lines, { yPercent: HIDE, duration: 0.45, ease: 'power3.in' });
      else gsap.set(c.lines, { yPercent: HIDE });
      gsap.to(c.fade, { opacity: 0, duration: 0.3 });
      c.el.classList.remove('is-on');
    }
    const k = p < start || end > 1 ? 0 : range(p, end - 0.035, end);   // the last chapter stays
    if (k === c.k) return;
    c.k = k;
    c.el.style.opacity = 1 - k;
    c.el.style.filter = k > 0 ? `blur(${k * 12}px)` : '';
    c.el.style.transform = k > 0 ? `translateY(${-k * 3}vh)` : '';
  }
}
