import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export { gsap, ScrollTrigger };

export const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
export const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');

/** Media query strings for gsap.matchMedia contexts. */
export const MQ = {
  motion: '(prefers-reduced-motion: no-preference)',
  desktopMotion: '(min-width: 768px) and (prefers-reduced-motion: no-preference)',
  mobileOrReduced: '(max-width: 767px), (prefers-reduced-motion: reduce)',
};

export const imgSrc = (name) => `${import.meta.env.BASE_URL}img/${name}.webp`;

/**
 * Image on top of a designed gradient placeholder. The wrapper (`.ph`) owns the
 * aspect ratio so nothing shifts when the webp lands; missing files keep the gradient.
 */
export function figure({ name, alt, w, h, tone = 'dusk', cls = '', imgCls = '', eager = false }) {
  return `<div class="ph ph--${tone} ${cls}" style="--ar:${w}/${h}">
    <img class="ph__img ${imgCls}" src="${imgSrc(name)}" alt="${alt}" width="${w}" height="${h}"
      loading="${eager ? 'eager' : 'lazy'}" decoding="async" />
  </div>`;
}

/** Fade images in once decoded; drop them on 404 so the placeholder shows. */
export function wireImages(root) {
  root.querySelectorAll('.ph__img').forEach((img) => {
    const done = () => img.classList.add('is-loaded');
    if (img.complete && img.naturalWidth) done();
    else {
      img.addEventListener('load', done, { once: true });
      img.addEventListener('error', () => img.remove(), { once: true });
    }
  });
}

/** Wrap each word of a text node tree in `.w` spans, keeping inline elements (em) intact. */
export function splitWords(el) {
  const walk = (node) => {
    [...node.childNodes].forEach((child) => {
      if (child.nodeType === 3) {
        const frag = document.createDocumentFragment();
        child.textContent.split(/(\s+)/).forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) frag.append(document.createTextNode(part));
          else {
            const s = document.createElement('span');
            s.className = 'w';
            s.textContent = part;
            frag.append(s);
          }
        });
        child.replaceWith(frag);
      } else if (child.nodeType === 1) walk(child);
    });
  };
  walk(el);
  return [...el.querySelectorAll('.w')];
}

/** Split into per-letter spans grouped by word (words stay unbreakable). */
export function splitChars(el) {
  const walk = (node) => {
    [...node.childNodes].forEach((child) => {
      if (child.nodeType === 3) {
        const frag = document.createDocumentFragment();
        child.textContent.split(/(\s+)/).forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.append(document.createTextNode(' ')); return; }
          const word = document.createElement('span');
          word.className = 'cw';
          [...part].forEach((ch) => {
            const c = document.createElement('span');
            c.className = 'c';
            c.textContent = ch;
            word.append(c);
          });
          frag.append(word);
        });
        child.replaceWith(frag);
      } else if (child.nodeType === 1) walk(child);
    });
  };
  el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
  walk(el);
  [...el.children].forEach((c) => c.setAttribute('aria-hidden', 'true'));
  return [...el.querySelectorAll('.c')];
}

export const lenis = () => window.__lenis;

export function scrollToTarget(target, opts = {}) {
  const el = typeof target === 'string' ? document.querySelector(target) : target;
  const l = lenis();
  if (l) l.scrollTo(el ?? 0, { duration: reducedMotion ? 0 : 1.6, immediate: reducedMotion, ...opts });
  else if (el) el.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth' });
  else window.scrollTo(0, 0);
}

export const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
export const lerp = (a, b, t) => a + (b - a) * t;
