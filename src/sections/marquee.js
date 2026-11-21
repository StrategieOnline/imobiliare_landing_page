import './css/marquee.css';
import { gsap, ScrollTrigger, reducedMotion, clamp, lenis } from './util.js';

const WORDS = ['TRAVERTIN', 'BRONZ', 'STEJAR AFUMAT', 'STICLĂ', 'LUMINĂ'];

const group = (offset) => `<span class="marquee__group">${WORDS.map((w, i) =>
  `<span class="marquee__word ${(i + offset) % 2 ? 'is-outline' : ''}">${w}</span><span class="marquee__star">✦</span>`).join('')}</span>`;

export function mountMarquee(content) {
  const sec = document.createElement('section');
  sec.className = 'marquee';
  sec.setAttribute('aria-label', WORDS.join(', '));
  sec.innerHTML = [0, 1].map((r) => `<div class="marquee__row" aria-hidden="true"><div class="marquee__track">${group(r).repeat(4)}</div></div>`).join('');
  content.append(sec);
  if (reducedMotion) return;

  const rows = [...sec.querySelectorAll('.marquee__track')].map((track, i) => ({
    track, x: 0, sign: i ? 1 : -1, width: 0,
  }));
  const measure = () => rows.forEach((r) => { r.width = r.track.firstElementChild.offsetWidth; });
  measure();
  addEventListener('resize', measure);
  document.fonts?.ready.then(measure);

  let velocity = 0;      // smoothed |lenis velocity|
  let dir = 1;           // smoothed scroll direction (-1..1), flips the travel
  let targetDir = 1;
  lenis()?.on('scroll', (e) => {
    if (e.direction) targetDir = e.direction;
    velocity = Math.max(velocity, Math.abs(e.velocity));
  });

  let visible = false;
  ScrollTrigger.create({ trigger: sec, start: 'top bottom', end: 'bottom top', onToggle: (s) => { visible = s.isActive; } });

  const BASE = 60; // px/s at rest
  gsap.ticker.add((_, dt) => {
    const s = dt / 1000;
    velocity *= Math.pow(0.04, s);           // decays to ~4% per second once scrolling stops
    dir += (targetDir - dir) * clamp(s * 4, 0, 1);
    if (!visible) return;
    const speed = BASE + clamp(velocity, 0, 120) * 28;
    const skew = clamp(velocity * dir * 0.35, -7, 7);
    rows.forEach((r) => {
      r.x += r.sign * dir * speed * s;
      r.x = gsap.utils.wrap(-r.width, 0, r.x);
      r.track.style.transform = `translate3d(${r.x}px,0,0) skewX(${-skew * r.sign}deg)`;
    });
  });
}
